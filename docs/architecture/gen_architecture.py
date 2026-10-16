"""Generate the abstract architecture diagram as SVG.

Usage: python3 gen_architecture.py <out.svg> [--themed]
  default : fixed light colours (for the repo / GitHub)
  --themed: colours via CSS variables (for an HTML page with light/dark themes)
"""
import sys
from xml.sax.saxutils import escape

FONT = '"PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans CJK SC","Source Han Sans SC",sans-serif'
MONO = 'ui-monospace,"SF Mono",Menlo,Consolas,monospace'

PALETTE = {
    # name: (light, dark)
    "page": ("#ffffff", "#15171c"),
    "layer": ("#f6f7f9", "#1d2027"),
    "layer-s": ("#d5dae1", "#343944"),
    "ink": ("#1f2937", "#e6e8ec"),
    "muted": ("#5b6472", "#9aa3b2"),
    "arrow": ("#4b5563", "#a3abb8"),
    "card": ("#ffffff", "#232731"),
    "card-s": ("#a7b1bf", "#4a5160"),
    "m1": ("#1d5fd1", "#7fb0ff"), "m1-f": ("#eaf2ff", "#1a2a45"), "m1-c": ("#a9c5f3", "#3a5a8f"), "m1-h": ("#d8e6ff", "#22385e"),
    "m2": ("#178048", "#6fd39a"), "m2-f": ("#e9f7ee", "#173326"), "m2-c": ("#a6dbbb", "#2f6b4a"), "m2-h": ("#d3f0de", "#1d4331"),
    "m3": ("#b8650f", "#f3b06a"), "m3-f": ("#fff3e3", "#3a2a16"), "m3-c": ("#f0c896", "#7a5426"), "m3-h": ("#ffe6c4", "#4a351b"),
    "d": ("#6a3fc8", "#b9a0f5"), "d-f": ("#f2ecfd", "#2a2240"), "d-c": ("#cdbbf2", "#54457e"),
    "x": ("#5d6876", "#a9b2bf"), "x-f": ("#eef1f4", "#22262e"), "x-c": ("#c3cad3", "#454c58"),
}


def css(themed):
    if not themed:
        v = {k: a for k, (a, b) in PALETTE.items()}
        col = lambda k: v[k]
    else:
        col = lambda k: f"var(--a-{k})"
    rules = f"""
    text{{font-family:{FONT};fill:{col('ink')}}}
    .mono{{font-family:{MONO}}}
    .page{{fill:{col('page')}}}
    .layer{{fill:{col('layer')};stroke:{col('layer-s')};stroke-width:1}}
    .lt{{font-size:16px;font-weight:700}}
    .ls{{font-size:12.5px;fill:{col('muted')}}}
    .h{{font-size:15px;font-weight:700}}
    .t{{font-size:12.5px}}
    .tm{{font-size:12px;fill:{col('muted')}}}
    .tt{{font-size:11.5px;fill:{col('muted')}}}
    .card{{fill:{col('card')};stroke:{col('card-s')};stroke-width:1}}
    .ar{{stroke:{col('arrow')};stroke-width:1.6;fill:none}}
    .ar.async{{stroke-dasharray:6 4}}
    .ah{{fill:{col('arrow')}}}
    """
    for m in ("m1", "m2", "m3", "d", "x"):
        rules += f"""
    .box-{m}{{fill:{col(m + '-f')};stroke:{col(m)};stroke-width:1.4}}
    .chip-{m}{{fill:{col('card')};stroke:{col(m + '-c')};stroke-width:1}}
    .c-{m}{{fill:{col(m)}}}
    .dot-{m}{{fill:{col(m)}}}"""
    for m in ("m1", "m2", "m3"):
        rules += f"""
    .hl-{m}{{fill:{col(m + '-h')};stroke:{col(m)};stroke-width:1.4}}"""
    themed_vars = ""
    if themed:
        light = ";".join(f"--a-{k}:{a}" for k, (a, b) in PALETTE.items())
        dark = ";".join(f"--a-{k}:{b}" for k, (a, b) in PALETTE.items())
        themed_vars = (
            f":root{{{light}}}"
            f"@media (prefers-color-scheme: dark){{:root:not([data-theme=\"light\"]){{{dark}}}}}"
            f":root[data-theme=\"dark\"]{{{dark}}}"
        )
    return themed_vars, rules


out = []
bg = []


def add(s):
    out.append(s)


def text(x, y, s, cls="t", anchor=None, extra=""):
    a = f' text-anchor="{anchor}"' if anchor else ""
    add(f'<text x="{x}" y="{y}" class="{cls}"{a}{extra}>{escape(s)}</text>')


def rich(x, y, parts, cls="t", anchor=None):
    """parts: list of (text, cls or None)"""
    a = f' text-anchor="{anchor}"' if anchor else ""
    spans = "".join(
        f'<tspan class="{c}">{escape(t)}</tspan>' if c else escape(t) for t, c in parts
    )
    add(f'<text x="{x}" y="{y}" class="{cls}"{a}>{spans}</text>')


def rect(x, y, w, h, cls, rx=8, back=False):
    (bg.append if back else add)(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{cls}"/>')


def chip(x, y, w, h, label, mod):
    rect(x, y, w, h, f"chip-{mod}", rx=6)
    text(x + w / 2, y + h / 2 + 4.5, label, "t", "middle")


def bullet(x, y, s, mod):
    add(f'<circle cx="{x + 4}" cy="{y - 4.5}" r="4" class="dot-{mod}"/>')
    text(x + 14, y, s, "t")


def arrow(points, async_=False, both=False):
    d = "M" + " L".join(f"{x},{y}" for x, y in points)
    cls = "ar async" if async_ else "ar"
    add(f'<path d="{d}" class="{cls}" marker-end="url(#ah)"' + (' marker-start="url(#ahs)"' if both else "") + "/>")


def layer(y, h, num, title, sub):
    rect(40, y, 1180, h, "layer", rx=10, back=True)
    rich(60, y + 26, [(f"{num} {title}", "lt"), ("    " + sub, "ls")], "t")


def build(themed):
    W, H = 1600, 1262
    v, rules = css(themed)
    add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-labelledby="ttl desc">')
    add('<title id="ttl">校园资源服务平台 · 抽象架构图</title>')
    add('<desc id="desc">五层架构：客户端层、接入层、业务服务层（M1/M2/M3）、公共服务层 D、数据与中间件层，右侧为交付与运行支撑。</desc>')
    add(f"<style>{v}{rules}</style>")
    add('<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ah"/></marker>'
        '<marker id="ahs" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ah"/></marker></defs>')
    rect(0, 0, W, H, "page", rx=0, back=True)
    head = len(out)

    # Title
    text(40, 46, "校园资源服务平台 · 抽象架构图", "h", extra=' style="font-size:24px"')
    rich(40, 72, [("v0.1 · 2026-10-17 · 颜色表示建议归属：", "ls"), ("■ M1 ", "c-m1"), ("■ M2 ", "c-m2"),
                  ("■ M3 ", "c-m3"), ("■ 公共层 D ", "c-d"), ("■ 基础设施", "c-x")], "t")

    # ---------- Layer 1: clients ----------
    layer(90, 200, "①", "客户端层", "Web 前端为单一工程、按模块划分页面目录；Agent 为附加项，独立于前端")
    bw, bx = 273, [60, 349, 638, 927]
    boxes = [
        ("学生端（移动优先 H5）", [("座位检索 · 预约 · 签到 · 历史 · 违约", "m1"), ("整教室申请 · 进度 · 撤销", "m2"), ("故障上报 · 进度 · 验收评价", "m3")]),
        ("管理后台（桌面）", [("用户 · 角色权限 · 空间座位 · 审计", "d"), ("参数 · 运营看板 · 违约 · 状态追溯", "m1"), None]),
        ("自习室屏幕端（全屏）", [("签到码 / 二维码轮换展示", "m1"), ("设备令牌，只读本室签到码", "m1"), ("自动刷新，换码 ≤ 30 秒可见", "m1")]),
    ]
    for i, (ttl, lines) in enumerate(boxes):
        x = bx[i]
        rect(x, 130, bw, 104, "card")
        text(x + 14, 153, ttl, "h")
        for j, ln in enumerate(lines):
            if ln:
                bullet(x + 14, 177 + j * 21, ln[0], ln[1])
    # admin line 3: two bullets
    bullet(bx[1] + 14, 219, "审批工作台", "m2")
    bullet(bx[1] + 128, 219, "派单与工单监控", "m3")
    # agent
    x = bx[3]
    rect(x, 130, bw, 144, "box-x")
    text(x + 14, 153, "会话代理 Agent（附加项）", "h")
    for j, ln in enumerate(["DSH 插件，安装配置纳入流水线", "意图不明确时追问，不擅自执行", "只调用各模块公开 API", "不访问任何模块的数据库"]):
        bullet(x + 14, 177 + j * 21, ln, "x")
    # shell band
    rect(60, 244, 851, 34, "box-d", rx=6)
    rich(74, 266, [("前端公共壳 ", "c-d"), ("登录态与令牌刷新 · 按权限生成菜单 · 由 OpenAPI 生成的 API Client · 统一错误处理 · 版本号显示", None)], "t")

    # arrows clients -> gateway
    arrow([(300, 278), (300, 338)])
    text(310, 314, "HTTPS · REST/JSON · Bearer JWT", "tt")
    arrow([(700, 278), (700, 338)])
    text(710, 314, "HTTPS 轮询 · 设备令牌", "tt")
    arrow([(1063, 274), (1063, 338)])
    text(1053, 314, "公开 API · 用户委托令牌", "tt", "end")

    # ---------- Layer 2: gateway ----------
    rect(40, 340, 1180, 78, "layer", rx=10, back=True)
    rich(60, 366, [("② 接入层", "lt"), ("    Nginx 反向代理（无业务逻辑）", "ls")])
    cx = 60
    for label, w in [("TLS 终止", 80), ("静态资源托管", 100), ("/api/{模块}/v1/** 按前缀路由", 206), ("对外屏蔽 /internal/**", 160),
                     ("登录 / 签到限流", 118), ("注入 traceId", 100), ("不做鉴权：各服务以 JWKS 本地验签", 250)]:
        chip(cx, 378, w, 28, label, "x")
        cx += w + 8

    # arrows gateway -> services
    for xx in (191, 620, 1049):
        arrow([(xx, 418), (xx, 466)])
    text(634, 452, "HTTP（内网）· 按路径前缀转发 · 透传用户 JWT", "tt")
    # gateway -> D (route on the right edge)
    arrow([(1203, 418), (1203, 820)])
    text(1196, 452, "→ 公共层 D 公开 API", "tt", "end")

    # ---------- Layer 3: business services ----------
    layer(468, 304, "③", "业务服务层", "每个模块一个独立服务：独立进程 · 独立 schema · 独立 OpenAPI；服务内分层 API → 应用 → 领域 → 基础设施")
    svc = {
        "m2": dict(x=60, w=262, name="M2 整教室预约与审批", sid="room-service", cols=2,
                   chips=["准入校验（门槛）", "申请管理", "多级审批流", "超时自动撤销", "申请查询", "审批链配置"],
                   bar=("占用写回 → M1", "本地事务 + Outbox 重试"), api="/api/m2/v1"),
        "m1": dict(x=398, w=444, name="M1 自习座位预约", sid="seat-service", cols=3,
                   chips=["座位检索", "预约管理", "历史与再次预约", "签到与签到码", "提醒与超时调度", "违约与处罚",
                          "运营统计", "业务参数", "主数据变更处理"],
                   bar=("占用块与来源追溯（跨模块写回的唯一入口）", "来源：M1 预约 · M2 整间占用 · M3 维修下架 · 管理员停用"),
                   api="/api/m1/v1 · /internal/m1/v1"),
        "m3": dict(x=918, w=262, name="M3 物业报修工单", sid="repair-service", cols=2,
                   chips=["故障上报", "派单", "维修状态流转", "超时升级", "完工验收", "评价"],
                   bar=("下架写回 → M1", "本地事务 + Outbox 重试"), api="/api/m3/v1"),
    }
    for m, s in svc.items():
        x, w, cols = s["x"], s["w"], s["cols"]
        rect(x, 508, w, 250, f"box-{m}")
        text(x + 14, 532, s["name"], f"h c-{m}")
        cw = (w - 28 - (cols - 1) * 8) / cols
        for k, c in enumerate(s["chips"]):
            r, cc = divmod(k, cols)
            chip(x + 14 + cc * (cw + 8), 546 + r * 38, cw, 30, c, m)
        rect(x + 14, 664, w - 28, 50, f"hl-{m}", rx=6)
        text(x + w / 2, 684, s["bar"][0], "t", "middle", ' style="font-weight:700"')
        text(x + w / 2, 704, s["bar"][1], "tt", "middle")
        text(x + 14, 742, s["sid"] + " · " + s["api"], "tm mono")
    # write-back arrows
    arrow([(308, 689), (410, 689)])
    text(360, 680, "同步 REST", "tt", "middle")
    text(360, 707, "幂等键", "tt", "middle")
    arrow([(932, 689), (830, 689)])
    text(880, 680, "同步 REST", "tt", "middle")
    text(880, 707, "幂等键", "tt", "middle")

    # arrows services <-> D
    arrow([(560, 758), (560, 820)])
    text(550, 792, "各服务 → D：同步 REST 查询 · JWKS 验签", "tt", "end")
    arrow([(590, 822), (590, 760)], async_=True)
    text(600, 814, "异步 MQ · space.* 变更事件 → M1", "tt")
    arrow([(1000, 758), (1000, 820)], async_=True)
    text(990, 792, "异步 MQ · notify.send / audit.record", "tt", "end")

    # ---------- Layer 4: D ----------
    layer(822, 170, "④", "公共服务层 D", "platform-service：4 个子模块按包与 schema 隔离；归属可按子域拆分给各模块组（须形成决策记录）")
    dw = (1120 - 3 * 16) / 4
    dboxes = [
        ("IAM 身份与权限", ["认证 · JWT 签发 / JWKS", "用户与院系", "角色 · 权限点 · 数据范围", "服务凭证（client credentials）"]),
        ("空间与座位主数据", ["校区 · 楼宇 · 房间 · 自习开放", "座位 · 特殊标记 · 开放时间", "启用 / 停用 / 注销", "发布 space.* 变更事件"]),
        ("通知服务", ["消费 notify 命令 · 模板渲染", "邮件 / 站内信渠道", "幂等 · 重试 · 投递记录", "消息中心 API"]),
        ("操作审计", ["消费 audit 事件", "只增不改存储", "按操作者 / 对象 / 时间查询", "traceId 关联跨服务链路"]),
    ]
    for i, (ttl, lines) in enumerate(dboxes):
        x = 60 + i * (dw + 16)
        rect(x, 862, dw, 114, "box-d")
        text(x + 14, 885, ttl, "h c-d")
        for j, ln in enumerate(lines):
            bullet(x + 14, 908 + j * 20, ln, "d")

    # arrows D -> data layer
    arrow([(300, 976), (300, 1038)])
    text(310, 1018, "各服务 JDBC（只访问本 schema）", "tt")
    arrow([(700, 976), (700, 1038)], async_=True)
    text(710, 1018, "AMQP", "tt")
    arrow([(860, 976), (860, 1038)])
    text(870, 1018, "SMTP", "tt")
    arrow([(1090, 976), (1090, 1038)])
    text(1100, 1018, "Redis", "tt")

    # ---------- Layer 5: data & middleware ----------
    layer(1040, 140, "⑤", "数据与中间件层", "每个环境一套，全部容器化")
    rect(60, 1080, 500, 86, "card")
    text(74, 1101, "PostgreSQL 16 · 单实例多 schema", "h")
    for k, (sname, m) in enumerate([("iam", "d"), ("space", "d"), ("notify", "d"), ("audit", "d"), ("m1", "m1"), ("m2", "m2"), ("m3", "m3")]):
        rect(74 + k * 67, 1110, 61, 24, f"box-{m}", rx=5)
        text(74 + k * 67 + 30.5, 1126.5, sname, f"tt mono c-{m}", "middle")
    text(74, 1155, "每服务独立账号只授权本 schema · Alembic 版本化迁移 · 种子脚本幂等", "tm")
    for (x, w, ttl, lines) in [
        (576, 210, "RabbitMQ", ["domain.events（topic）", "notify / audit 队列 · 死信队列"]),
        (802, 186, "邮件网关", ["dev / test：Mailpit 捕获", "prod：SMTP"]),
        (1004, 176, "Redis", ["主数据缓存 · 签到码", "限流计数 · 幂等键"]),
    ]:
        rect(x, 1080, w, 86, "card")
        text(x + 14, 1101, ttl, "h")
        for j, ln in enumerate(lines):
            text(x + 14, 1124 + j * 20, ln, "t")

    # ---------- Right column: delivery ----------
    rect(1250, 90, 310, 1090, "layer", rx=10, back=True)
    text(1270, 116, "⑥ 交付与运行支撑", "lt")
    rx_, rw = 1266, 278
    blocks = [
        (134, 112, "代码与评审", ["GitHub 单仓库 · 分支保护", "合并请求评审 · CODEOWNERS 按模块", "跨模块 / 公共层 / schema 变更组内评审", "契约 contracts/（OpenAPI、事件）"]),
        (272, 132, "CI · GitHub Actions", ["构建 · 静态检查", "单元 / 集成（Testcontainers）", "契约测试 · 变异测试", "任一失败即中止后续阶段", "镜像 tag = 提交 SHA → GHCR"]),
    ]
    for (y, h, ttl, lines) in blocks:
        rect(rx_, y, rw, h, "box-x")
        text(rx_ + 14, y + 23, ttl, "h")
        for j, ln in enumerate(lines):
            bullet(rx_ + 14, y + 46 + j * 20, ln, "x")
    arrow([(1405, 246), (1405, 270)])
    arrow([(1405, 404), (1405, 428)])
    # environments
    rect(rx_, 430, rw, 252, "box-x")
    text(rx_ + 14, 453, "环境（每环境一套 Compose）", "h")
    envs = [
        ("dev", ["开发者本地 Compose", "Mailpit · 可控时钟 · 演示数据"]),
        ("test", ["合并主干后自动部署 · 部署锁", "健康检查通过后跑集成 / E2E"]),
        ("prod", ["版本 tag + 人工审批后发布", "一键回滚到上一个 tag"]),
    ]
    for k, (name, lines) in enumerate(envs):
        y = 466 + k * 70
        rect(rx_ + 12, y, rw - 24, 62, "card", rx=6)
        text(rx_ + 24, y + 22, name, "h mono")
        for j, ln in enumerate(lines):
            text(rx_ + 74, y + 22 + j * 21, ln, "t")
    arrow([(1405, 682), (1405, 706)])
    rect(rx_, 708, rw, 96, "box-x")
    text(rx_ + 14, 731, "发布顺序（一次部署覆盖全部模块）", "h")
    text(rx_ + 14, 756, "迁移 → D → M1 → M2/M3 → 前端 → Agent", "t")
    text(rx_ + 14, 780, "迁移先扩展后收缩，保证可回滚", "tm")
    rect(rx_, 822, rw, 132, "box-x")
    text(rx_ + 14, 845, "可观测与版本", "h")
    for j, ln in enumerate(["结构化日志 + traceId 贯穿全链路", "/health 存活与就绪，作部署门禁", "/version 版本号 · SHA · 构建时间", "前端页脚显示当前版本"]):
        bullet(rx_ + 14, 868 + j * 21, ln, "x")
    rect(rx_, 972, rw, 192, "box-x")
    text(rx_ + 14, 995, "测试辅助（仅 dev / test）", "h")
    for j, ln in enumerate(["时间推进 / 立即触发调度", "邮件沙箱断言提醒内容", "种子数据：基础数据 + 演示数据", "契约桩：依赖未就绪时并行开发", "变异测试：故意破坏实现看是否失败"]):
        bullet(rx_ + 14, 1018 + j * 21, ln, "x")

    # ---------- Legend ----------
    ly = 1222
    arrow([(40, ly), (90, ly)])
    text(98, ly + 4.5, "同步调用（HTTP / JDBC）", "tm")
    arrow([(270, ly), (320, ly)], async_=True)
    text(328, ly + 4.5, "异步消息（RabbitMQ）", "tm")
    rect(490, ly - 10, 30, 20, "chip-x", rx=5)
    text(528, ly + 4.5, "子模块：建议的最小分工单元", "tm")
    rect(740, ly - 10, 30, 20, "hl-m1", rx=5)
    text(778, ly + 4.5, "跨模块集成点", "tm")
    text(1560, ly + 4.5, "详见 docs/architecture/architecture.md", "tm", "end")

    add("</svg>")
    return "\n".join(out[:head] + bg + out[head:])


if __name__ == "__main__":
    themed = "--themed" in sys.argv
    svg = build(themed)
    with open(sys.argv[1], "w", encoding="utf-8") as f:
        f.write(svg + "\n")
