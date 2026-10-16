"""种子数据（NFR-07）：脚本化、幂等、与迁移分离。

- base：所有环境都需要的基础数据（预置角色、系统管理员、服务凭证、标记字典）；
- demo：只用于 dev / test 的演示数据（院系、演示账号、校区楼宇房间座位）。

运行：python -m platform_service.seeds base|demo（容器启动时自动执行，见 deploy/run-service.sh）
"""
