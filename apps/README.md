# apps/

| 目录 | 内容 |
| --- | --- |
| `web/` | 前端单一工程：Next.js（App Router）+ TypeScript，静态导出后由 Nginx 托管 |

## web/ 的目录约定

```text
apps/web/src/
├── app/            # 路由与布局：(student) 学生端、(admin) 管理后台、screen 自习室屏幕端
├── shell/          # 前端公共壳（D）：登录态、按权限生成菜单、API Client、统一错误处理、版本号
└── modules/
    ├── m1/  m2/  m3/   # 各模块的页面与组件（M1 的屏幕端也在 m1/ 中）
    └── platform/       # 公共层的管理页面（D）
```

## 规则

- 模块页面只通过本模块的 API Client 调用本模块后端；需要其他模块时用页面跳转，不在前端拼装其他模块的业务逻辑。
- 不使用 Route Handlers、Server Actions 实现业务逻辑；详情页等用查询参数传 ID（静态导出不支持运行时动态路由段）。
- API Client 由 `contracts/` 中的 OpenAPI 生成，不手写请求类型。
