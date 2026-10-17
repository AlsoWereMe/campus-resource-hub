"""按 docs/tasks.md 在 GitHub 上创建标签、里程碑与任务 Issue（幂等，已存在的跳过）。

    uv run python scripts/sync_issues.py            # 创建缺少的
    uv run python scripts/sync_issues.py --dry-run  # 只打印将要创建的

需要已登录的 gh。任务卡改动后由组长运行；已存在的 Issue 不会被修改。
"""

import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "docs" / "tasks.md"
BLOB = "https://github.com/AlsoWereMe/campus-resource-hub/blob/main/docs/tasks.md"

MILESTONES = {"R1": "R1 第一次 Review", "R2": "R2 第二次 Review", "R3": "R3 期末展示"}
MODULES = {"M1": "m1", "M2": "m2", "M3": "m3", "D": "platform", "X": "cross"}
SEAT_CLAIM_TITLE = "席位认领"


@dataclass
class Card:
    task_id: str
    title: str
    seat: str
    priority: str
    milestone: str
    lines: list[str] = field(default_factory=list)

    @property
    def issue_title(self) -> str:
        return f"[{self.task_id}] {self.title}"

    @property
    def labels(self) -> list[str]:
        module = MODULES[self.task_id.split("-")[0]]
        return ["task", f"seat:{self.seat}", f"module:{module}", self.priority]


def parse_cards(text: str) -> list[Card]:
    cards: list[Card] = []
    pattern = re.compile(r"^### ((?:M[123]|D|X)-T\d{2}) (.+)$")
    meta = re.compile(r"^`(\w+)` `(P\d)` `(R\d)`(.*)$")
    current: Card | None = None
    for line in text.splitlines():
        heading = pattern.match(line)
        if heading:
            current = Card(heading.group(1), heading.group(2).strip(), "", "", "")
            cards.append(current)
            continue
        if current is None:
            continue
        if line.startswith("#"):
            current = None
            continue
        found = meta.match(line)
        if found and not current.seat:
            current.seat, current.priority, current.milestone = found.group(1, 2, 3)
            current.lines.append(found.group(4).strip(" ·"))
        elif line.strip():
            current.lines.append(line)
    return cards


def gh(*args: str) -> str:
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


def issue_body(card: Card) -> str:
    anchor = re.sub(r"[^\w\- ]", "", f"{card.task_id} {card.title}".lower()).replace(" ", "-")
    return "\n".join(
        [
            f"席位 **{card.seat}** · {card.priority} · 里程碑 {MILESTONES[card.milestone]}",
            "",
            *card.lines,
            "",
            f"任务卡：[docs/tasks.md]({BLOB}#{anchor})",
            f"开工：在 agent 中输入「做任务 {card.task_id}」。",
        ]
    )


SEAT_CLAIM_BODY = """在下面留言认领席位（一人一个），组长确认后会把你加入 CODEOWNERS 并在 docs/adr.md ADR-003 记录确认。

| 席位 | 范围 |
| --- | --- |
| A1 | M1 预约域：占用块、参数、检索、预约、历史 |
| A2 | M1 履约域：签到码与屏幕端、签到、提醒与违约、运营统计 |
| B1 | M2 整教室预约与审批 |
| B2 | 公共层：身份权限、审计；持续部署 |
| C1 | M3 物业报修工单 |
| C2 | 公共层：空间管理、通知；会话代理（附加） |

任务卡见 docs/tasks.md；认领后在 agent 中输入「做任务 <编号>」开工。"""


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    cards = parse_cards(TASKS.read_text("utf-8"))
    existing = {
        i["title"]
        for i in json.loads(
            gh("issue", "list", "--state", "all", "--limit", "500", "--json", "title")
        )
    }
    milestones = {
        m["title"] for m in json.loads(gh("api", "repos/{owner}/{repo}/milestones?state=all"))
    }

    labels = {label for card in cards for label in card.labels}
    for name in sorted(labels):
        print(f"标签 {name}")
        if not dry_run:
            gh(
                "label",
                "create",
                name,
                "--force",
                "--color",
                "0e8a16" if name == "task" else "ededed",
            )
    for title in MILESTONES.values():
        if title not in milestones:
            print(f"里程碑 {title}")
            if not dry_run:
                gh("api", "repos/{owner}/{repo}/milestones", "-f", f"title={title}")

    if SEAT_CLAIM_TITLE not in existing:
        print(f"Issue {SEAT_CLAIM_TITLE}")
        if not dry_run:
            gh("issue", "create", "--title", SEAT_CLAIM_TITLE, "--body", SEAT_CLAIM_BODY)
    for card in cards:
        if card.issue_title in existing:
            continue
        print(f"Issue {card.issue_title}")
        if not dry_run:
            gh(
                "issue",
                "create",
                "--title",
                card.issue_title,
                "--body",
                issue_body(card),
                "--milestone",
                MILESTONES[card.milestone],
                *[arg for label in card.labels for arg in ("--label", label)],
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())
