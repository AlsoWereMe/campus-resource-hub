# contracts/

模块之间、前后端之间的接口契约。**本目录由代码导出，不要手改**：契约的源头是各服务 `api/*.py` 中的路由签名与模型，以及 `libs/common/src/campus_common/contracts/`（跨服务模型、权限点、消息）。

```text
contracts/
├── iam/ space/ notify/ audit/openapi.yaml   # 公共层 D 的四个子模块
├── m1/ m2/ m3/openapi.yaml                  # 业务模块（含 /internal 内部接口）
├── events/<路由键>.json                      # 消息体 JSON Schema，如 space.room.updated.json
└── permissions.yaml                          # 权限点、预置角色、服务凭证权限
```

每份契约由提供方（目录名对应的模块）维护。

## 变更流程

1. 改路由签名或模型（实现可以先返回 501）；
2. `make contracts`：更新本目录，并重新生成前端类型；
3. 合并请求中评审契约差异，所有消费方参与；
4. 合并后再写实现，消费方可先用替身并行开发。

`make contracts-check` 检查本目录与代码一致，是 `make check` 的一部分。

## 兼容性

- 默认只做兼容变更：可以新增接口、新增可选字段；不能删除、改名已有字段，不能把可选改为必填。
- 不兼容变更须在提交说明中使用 `!` 与 `BREAKING CHANGE`，并与所有消费方约定切换顺序。
