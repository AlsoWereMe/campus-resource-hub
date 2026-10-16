#!/usr/bin/env bash
# 创建各模块的 schema 与服务账号（架构 §4.5、§7）：
#   platform_svc → iam、space、notify、audit（公共层 D）
#   seat_svc     → m1
#   room_svc     → m2
#   repair_svc   → m3
# 每个账号只拥有自己的 schema，对其他 schema 与 public 没有任何权限。
# 由 postgres 镜像在数据卷为空时执行一次；脚本本身幂等，可重复运行。
set -euo pipefail

psql -v ON_ERROR_STOP=1 \
  --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" \
  -v db="$POSTGRES_DB" \
  -v platform_pw="$PLATFORM_DB_PASSWORD" \
  -v seat_pw="$SEAT_DB_PASSWORD" \
  -v room_pw="$ROOM_DB_PASSWORD" \
  -v repair_pw="$REPAIR_DB_PASSWORD" <<'SQL'
-- 服务账号：不存在则创建，存在则同步口令
SELECT format('CREATE ROLE %I LOGIN', r)
FROM unnest(ARRAY['platform_svc', 'seat_svc', 'room_svc', 'repair_svc']) AS r
WHERE NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = r) \gexec

ALTER ROLE platform_svc PASSWORD :'platform_pw';
ALTER ROLE seat_svc     PASSWORD :'seat_pw';
ALTER ROLE room_svc     PASSWORD :'room_pw';
ALTER ROLE repair_svc   PASSWORD :'repair_pw';

-- 只有四个服务账号能连接本库；任何人都不能在 public 中建对象
REVOKE ALL ON DATABASE :"db" FROM PUBLIC;
GRANT CONNECT, TEMPORARY ON DATABASE :"db" TO platform_svc, seat_svc, room_svc, repair_svc;
REVOKE ALL ON SCHEMA public FROM PUBLIC;

-- 每个 schema 归属唯一的服务账号
CREATE SCHEMA IF NOT EXISTS iam    AUTHORIZATION platform_svc;
CREATE SCHEMA IF NOT EXISTS space  AUTHORIZATION platform_svc;
CREATE SCHEMA IF NOT EXISTS notify AUTHORIZATION platform_svc;
CREATE SCHEMA IF NOT EXISTS audit  AUTHORIZATION platform_svc;
CREATE SCHEMA IF NOT EXISTS m1     AUTHORIZATION seat_svc;
CREATE SCHEMA IF NOT EXISTS m2     AUTHORIZATION room_svc;
CREATE SCHEMA IF NOT EXISTS m3     AUTHORIZATION repair_svc;

-- M1 用排他约束防止同一座位的预约区间重叠，需要 btree_gist；
-- 扩展只能由超级用户创建，装在 m1 中，只供 M1 使用
CREATE EXTENSION IF NOT EXISTS btree_gist SCHEMA m1;

-- 默认 search_path 指向本服务的 schema（代码中仍应显式写 schema）
ALTER ROLE platform_svc SET search_path = iam, space, notify, audit;
ALTER ROLE seat_svc     SET search_path = m1;
ALTER ROLE room_svc     SET search_path = m2;
ALTER ROLE repair_svc   SET search_path = m3;
SQL
