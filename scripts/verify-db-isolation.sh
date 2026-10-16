#!/usr/bin/env bash
# 验证数据库按 schema 隔离（架构 §4.5、§10.1）：
#   - 每个服务账号能在自己的 schema 中建表；
#   - 访问其他服务的 schema 或 public 时被拒绝；
#   - seat_svc 能在 m1 中使用 btree_gist 排他约束（M1 防重叠预约所需）。
# 用法：先 make up，再 make verify-db。连接走容器网络并校验口令，与服务的连接方式一致。
set -euo pipefail

cd "$(dirname "$0")/.."
set -a
# shellcheck disable=SC1091
source ./.env
set +a

compose=(docker compose --env-file .env -f deploy/compose.yml)
failures=0

# 以指定账号执行 SQL，输出 psql 的结果与错误
run_sql() {
  local role="$1" password="$2" sql="$3"
  "${compose[@]}" exec -T -e PGPASSWORD="$password" postgres \
    psql -h postgres -U "$role" -d "$POSTGRES_DB" -v ON_ERROR_STOP=1 -qAt -c "$sql" 2>&1
}

probe_sql() {
  local schema="$1"
  echo "CREATE TABLE ${schema}.isolation_probe (id int); DROP TABLE ${schema}.isolation_probe;"
}

expect_allowed() {
  local role="$1" password="$2" schema="$3"
  if output=$(run_sql "$role" "$password" "$(probe_sql "$schema")"); then
    echo "  通过  ${role} 可在 ${schema} 中建表"
  else
    echo "  失败  ${role} 应能在 ${schema} 中建表：${output}"
    failures=$((failures + 1))
  fi
}

expect_denied() {
  local role="$1" password="$2" schema="$3"
  if output=$(run_sql "$role" "$password" "$(probe_sql "$schema")"); then
    echo "  失败  ${role} 不应能在 ${schema} 中建表"
    failures=$((failures + 1))
  elif grep -q "permission denied" <<<"$output"; then
    echo "  通过  ${role} 访问 ${schema} 被拒绝"
  else
    echo "  失败  ${role} 访问 ${schema} 出现非权限错误：${output}"
    failures=$((failures + 1))
  fi
}

all_schemas=(iam space notify audit m1 m2 m3 public)

check_role() {
  local role="$1" password="$2"
  shift 2
  local own=("$@")
  echo "${role}："
  for schema in "${all_schemas[@]}"; do
    if [[ " ${own[*]} " == *" ${schema} "* ]]; then
      expect_allowed "$role" "$password" "$schema"
    else
      expect_denied "$role" "$password" "$schema"
    fi
  done
}

check_role platform_svc "$PLATFORM_DB_PASSWORD" iam space notify audit
check_role seat_svc "$SEAT_DB_PASSWORD" m1
check_role room_svc "$ROOM_DB_PASSWORD" m2
check_role repair_svc "$REPAIR_DB_PASSWORD" m3

echo "seat_svc（排他约束）："
exclusion_sql="CREATE TABLE m1.exclusion_probe (
  seat_id int, during tstzrange,
  EXCLUDE USING gist (seat_id WITH =, during WITH &&)
); DROP TABLE m1.exclusion_probe;"
if output=$(run_sql seat_svc "$SEAT_DB_PASSWORD" "$exclusion_sql"); then
  echo "  通过  seat_svc 可在 m1 中创建 btree_gist 排他约束"
else
  echo "  失败  seat_svc 无法创建排他约束：${output}"
  failures=$((failures + 1))
fi

if ((failures > 0)); then
  echo "共 ${failures} 项未通过"
  exit 1
fi
echo "数据库隔离验证全部通过"
