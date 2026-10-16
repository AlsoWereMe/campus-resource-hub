"""从代码导出契约到 contracts/（契约先行：先写路由签名与模型，再导出评审）。

    uv run python scripts/export_contracts.py           # 导出
    uv run python scripts/export_contracts.py --check   # 只检查是否一致，不一致时退出码 1

输出：
    contracts/<api>/openapi.yaml       iam、space、notify、audit、m1、m2、m3 各一份
    contracts/events/<路由键>.json     消息体 JSON Schema
    contracts/permissions.yaml         权限点、预置角色、服务凭证权限
"""

import json
import sys
from pathlib import Path
from typing import Any

import yaml
from fastapi import FastAPI

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "contracts"
DUMMY_DB = "postgresql+psycopg://export:export@127.0.0.1:1/export"

# API 名称 → (服务, 路径前缀)
APIS: dict[str, tuple[str, tuple[str, ...]]] = {
    "iam": ("platform", ("/api/iam/", "/internal/iam/")),
    "space": ("platform", ("/api/space/", "/internal/space/")),
    "notify": ("platform", ("/api/notify/", "/internal/notify/")),
    "audit": ("platform", ("/api/audit/", "/internal/audit/")),
    "m1": ("seat", ("/api/m1/", "/internal/m1/")),
    "m2": ("room", ("/api/m2/", "/internal/m2/")),
    "m3": ("repair", ("/api/m3/", "/internal/m3/")),
}


def build_app(service: str) -> FastAPI:
    if service == "platform":
        from platform_service.config import Settings as PlatformSettings
        from platform_service.main import create_app as create_platform

        return create_platform(PlatformSettings(database_url=DUMMY_DB, background_tasks=False))
    if service == "seat":
        from seat_service.config import Settings as SeatSettings
        from seat_service.main import create_app as create_seat

        return create_seat(SeatSettings(database_url=DUMMY_DB, background_tasks=False))
    if service == "room":
        from room_service.config import Settings as RoomSettings
        from room_service.main import create_app as create_room

        return create_room(RoomSettings(database_url=DUMMY_DB, background_tasks=False))
    from repair_service.config import Settings as RepairSettings
    from repair_service.main import create_app as create_repair

    return create_repair(RepairSettings(database_url=DUMMY_DB, background_tasks=False))


def _refs(node: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(node, dict):
        ref = node.get("$ref")
        if isinstance(ref, str) and ref.startswith("#/components/schemas/"):
            found.add(ref.rsplit("/", 1)[1])
        for value in node.values():
            found |= _refs(value)
    elif isinstance(node, list):
        for value in node:
            found |= _refs(value)
    return found


def split_spec(spec: dict[str, Any], api: str, prefixes: tuple[str, ...]) -> dict[str, Any]:
    paths = {p: v for p, v in spec.get("paths", {}).items() if p.startswith(prefixes)}
    schemas = spec.get("components", {}).get("schemas", {})
    needed: set[str] = set()
    pending = _refs(paths)
    while pending:
        name = pending.pop()
        if name in needed or name not in schemas:
            continue
        needed.add(name)
        pending |= _refs(schemas[name]) - needed
    components: dict[str, Any] = {}
    if needed:
        components["schemas"] = {k: schemas[k] for k in sorted(needed)}
    if "securitySchemes" in spec.get("components", {}):
        components["securitySchemes"] = spec["components"]["securitySchemes"]
    tags = [
        t
        for t in spec.get("tags", [])
        if any(t["name"] in op.get("tags", []) for item in paths.values() for op in item.values())
    ]
    result: dict[str, Any] = {
        "openapi": spec["openapi"],
        "info": {"title": f"{api} API", "version": "v1"},
        "paths": paths,
    }
    if tags:
        result["tags"] = tags
    if components:
        result["components"] = components
    return result


def render() -> dict[Path, str]:
    from campus_common.contracts.events import EVENTS
    from campus_common.contracts.permissions import PERMISSIONS, PRESET_ROLES, SERVICE_CLIENTS

    files: dict[Path, str] = {}
    specs: dict[str, dict[str, Any]] = {}
    for api, (service, prefixes) in APIS.items():
        if service not in specs:
            specs[service] = build_app(service).openapi()
        doc = split_spec(specs[service], api, prefixes)
        files[CONTRACTS / api / "openapi.yaml"] = yaml.safe_dump(
            doc, allow_unicode=True, sort_keys=False, width=100
        )
    for key, model in sorted(EVENTS.items()):
        schema = model.model_json_schema(by_alias=True)
        files[CONTRACTS / "events" / f"{key}.json"] = (
            json.dumps(schema, ensure_ascii=False, indent=2) + "\n"
        )
    permissions = {
        "permissions": PERMISSIONS,
        "roles": [
            {
                "code": r.code,
                "name": r.name,
                "description": r.description,
                "defaultScope": r.default_scope,
                "permissions": list(r.permissions),
            }
            for r in PRESET_ROLES
        ],
        "serviceClients": {k: list(v) for k, v in SERVICE_CLIENTS.items()},
    }
    files[CONTRACTS / "permissions.yaml"] = yaml.safe_dump(
        permissions, allow_unicode=True, sort_keys=False, width=100
    )
    return files


def main() -> int:
    check = "--check" in sys.argv
    files = render()
    stale = [p for p, text in files.items() if not p.exists() or p.read_text("utf-8") != text]
    if check:
        if stale:
            print("contracts/ 与代码不一致，请运行 make contracts 并在合并请求中评审差异：")
            for path in stale:
                print(f"  {path.relative_to(ROOT)}")
            return 1
        print("contracts/ 与代码一致")
        return 0
    for path in stale:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(files[path], "utf-8")
        print(f"已更新 {path.relative_to(ROOT)}")
    if not stale:
        print("contracts/ 已是最新")
    return 0


if __name__ == "__main__":
    sys.exit(main())
