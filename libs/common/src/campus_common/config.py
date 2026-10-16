"""服务配置：全部来自环境变量，同一镜像可运行在 dev / test / prod（架构 §9）。"""

from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

ServiceName = Literal["platform", "seat", "room", "repair"]


class ServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore")

    service_name: ServiceName
    env: Literal["dev", "test", "prod"] = "dev"

    database_url: str = "postgresql+psycopg://postgres:postgres-dev@127.0.0.1:5432/campus"
    rabbitmq_url: str = "amqp://campus:campus-dev@127.0.0.1:5672/"
    redis_url: str = "redis://127.0.0.1:6379/0"

    # 各服务的内网地址，用于服务间调用
    platform_url: str = "http://127.0.0.1:8001"
    seat_url: str = "http://127.0.0.1:8002"
    room_url: str = "http://127.0.0.1:8003"
    repair_url: str = "http://127.0.0.1:8004"

    # 服务凭证（client credentials），向 IAM 换取服务令牌
    service_client_id: str = ""
    service_client_secret: str = ""

    # 只在测试中使用：直接提供 IAM 公钥（PEM），不经 JWKS 获取
    jwt_public_key: str | None = None

    # 是否启动后台任务（消息消费、定时任务、Outbox 投递）；单元 / 集成测试中关闭
    background_tasks: bool = True
    outbox_max_attempts: int = 10

    # 版本信息，由构建流程注入
    app_version: str = "dev"
    git_sha: str = "unknown"
    build_time: str = "unknown"

    @property
    def test_endpoints_enabled(self) -> bool:
        """时间推进、立即触发任务等测试端点只在非生产环境开放（NFR-09）。"""
        return self.env != "prod"

    def service_url(self, service: ServiceName) -> str:
        urls: dict[ServiceName, str] = {
            "platform": self.platform_url,
            "seat": self.seat_url,
            "room": self.room_url,
            "repair": self.repair_url,
        }
        return urls[service]

    @property
    def jwks_url(self) -> str:
        return f"{self.platform_url}/internal/iam/v1/jwks"

    @property
    def service_token_url(self) -> str:
        return f"{self.platform_url}/internal/iam/v1/service-token"
