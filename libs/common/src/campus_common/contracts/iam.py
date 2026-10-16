"""IAM 对其他服务提供的模型（IAM-AUTH-03、IAM-USER-02）。"""

from typing import Literal

from campus_common.models import ApiModel


class UserBrief(ApiModel):
    id: int
    username: str
    name: str
    user_type: Literal["student", "staff"]
    department_id: int | None
    email: str | None


class ServiceTokenRequest(ApiModel):
    client_id: str
    client_secret: str


class TokenResponse(ApiModel):
    access_token: str
    token_type: Literal["Bearer"] = "Bearer"  # noqa: S105
    expires_in: int
    refresh_token: str | None = None
