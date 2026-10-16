from campus_common.config import ServiceName, ServiceSettings


class Settings(ServiceSettings):
    service_name: ServiceName = "platform"

    # 基础种子：系统管理员 admin 的初始口令（生产环境必须通过密钥注入覆盖）
    initial_admin_password: str = "admin-dev"  # noqa: S105  仅本地默认值
    # 基础种子：服务凭证，格式 "seat:口令,room:口令,repair:口令"
    service_client_secrets: str = ""
    # 演示种子：演示账号的统一口令（只用于 dev / test）
    demo_password: str = "Passw0rd!"  # noqa: S105  仅演示数据

    access_token_minutes: int = 15
    refresh_token_days: int = 7
    max_failed_logins: int = 5
    lock_minutes: int = 15

    # 通知（NTF）：dev / test 指向 Mailpit
    smtp_host: str = "127.0.0.1"
    smtp_port: int = 1025
    smtp_sender: str = "campus-hub@example.edu"
