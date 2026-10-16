from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from campus_common.contracts.permissions import PRESET_ROLES, SERVICE_CLIENTS
from campus_common.contracts.space import SeatTag
from platform_service.config import Settings
from platform_service.iam.models import Role, RolePermission, ServiceClient, User, UserRole
from platform_service.iam.security import hash_password
from platform_service.space.models import Tag

TAG_NAMES = {SeatTag.FIXED_OUTLET: "固定插座", SeatTag.RAIL_OUTLET: "移动导轨插座"}


async def seed_roles(session: AsyncSession) -> dict[str, Role]:
    """预置角色不存在则创建；系统管理员角色每次都同步为全部权限点（不可减少）。"""
    roles: dict[str, Role] = {}
    for spec in PRESET_ROLES:
        role = await session.scalar(select(Role).where(Role.code == spec.code))
        if role is None:
            role = Role(code=spec.code, name=spec.name, description=spec.description, builtin=True)
            session.add(role)
            await session.flush()
            session.add_all(RolePermission(role_id=role.id, permission=p) for p in spec.permissions)
        elif spec.code == "sys_admin":
            await session.execute(delete(RolePermission).where(RolePermission.role_id == role.id))
            session.add_all(RolePermission(role_id=role.id, permission=p) for p in spec.permissions)
        roles[spec.code] = role
    await session.flush()
    return roles


async def seed_admin(session: AsyncSession, settings: Settings, roles: dict[str, Role]) -> None:
    if await session.scalar(select(User).where(User.username == "admin")) is not None:
        return
    admin = User(
        username="admin",
        password_hash=hash_password(settings.initial_admin_password),
        name="系统管理员",
        user_type="staff",
    )
    session.add(admin)
    await session.flush()
    session.add(UserRole(user_id=admin.id, role_id=roles["sys_admin"].id, scope_all=True))


async def seed_service_clients(session: AsyncSession, settings: Settings) -> None:
    """服务凭证口令来自环境变量 SERVICE_CLIENT_SECRETS；每次同步口令与权限。"""
    for item in filter(None, (x.strip() for x in settings.service_client_secrets.split(","))):
        client_id, _, secret = item.partition(":")
        if client_id not in SERVICE_CLIENTS or not secret:
            raise ValueError(f"SERVICE_CLIENT_SECRETS 中的条目无效：{client_id}")
        client = await session.get(ServiceClient, client_id) or ServiceClient(client_id=client_id)
        client.secret_hash = hash_password(secret)
        client.permissions = list(SERVICE_CLIENTS[client_id])
        session.add(client)


async def seed_tags(session: AsyncSession) -> None:
    for code, name in TAG_NAMES.items():
        if await session.get(Tag, code.value) is None:
            session.add(Tag(code=code.value, name=name))


async def seed_base(session: AsyncSession, settings: Settings) -> None:
    roles = await seed_roles(session)
    await seed_admin(session, settings, roles)
    await seed_service_clients(session, settings)
    await seed_tags(session)
