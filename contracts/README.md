# contracts/

模块之间、前后端之间的接口契约，是各模块对外承诺的唯一依据（架构 §5）。

## 目录约定

```text
contracts/
├── iam/openapi.yaml       # 公共层 D 的四个子模块各一份
├── space/openapi.yaml
├── notify/openapi.yaml
├── audit/openapi.yaml
├── m1/openapi.yaml        # 含公开接口 /api/m1/v1 与内部接口 /internal/m1/v1
├── m2/openapi.yaml
├── m3/openapi.yaml
└── events/                # 消息契约：每个主题一份 JSON Schema
    ├── space.<event>.schema.json
    ├── m3.workorder.<event>.schema.json
    └── notify.send.schema.json
```

每份契约由**提供方**维护，即目录名对应的模块。

## 变更流程（契约先行）

1. 提供方先写路由签名与 Pydantic 模型，实现可以先返回 501；
2. 导出 OpenAPI，更新本目录中的对应文件；
3. 在合并请求中评审契约差异，消费方须参与评审；
4. 契约合入后再写实现。消费方可先用由契约生成的桩并行开发。

## 兼容性

- 默认只做兼容变更：可以新增接口、新增可选字段，不能删除或改名已有字段，不能把可选改为必填。
- 不兼容变更须在提交说明中使用 `!` 与 `BREAKING CHANGE`，并与所有消费方约定切换顺序。
- CI 校验本目录与代码导出的 OpenAPI 一致，并检测破坏性变更。
