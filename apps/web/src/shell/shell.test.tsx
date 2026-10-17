import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { errorMessage } from "./errors";
import { MENU, visibleMenu } from "./menu";
import { TodoPage } from "./Todo";

describe("菜单按权限点显示", () => {
  it("学生只看到自习座位、报修与「我的」", () => {
    const groups = visibleMenu([
      "m1:seat:search",
      "m1:booking:view-own",
      "m1:violation:view-own",
      "m3:workorder:create",
      "m3:workorder:manage-own",
    ]).map((g) => g.group);
    expect(groups).toEqual(["自习座位", "报修", "我的"]);
  });

  it("持有任一权限点即可见", () => {
    const items = visibleMenu(["m3:repair:act"]).flatMap((g) => g.items.map((i) => i.href));
    expect(items).toContain("/m3/workbench");
    expect(items).not.toContain("/admin/m3/stats");
  });

  it("每个待实现页面都标注了任务编号", () => {
    const missing = MENU.filter((i) => i.href !== "/account" && !i.task).map((i) => i.href);
    expect(missing).toEqual([]);
  });
});

describe("错误提示", () => {
  it("接口桩提示对应任务", () => {
    expect(errorMessage({ code: "NOT_IMPLEMENTED", message: "x", details: { task: "M1-T04" } })).toBe(
      "该功能尚未实现（任务 M1-T04）",
    );
  });

  it("业务错误附带 traceId", () => {
    expect(errorMessage({ code: "RULE_VIOLATION", message: "单次最长 4 小时", traceId: "abc" })).toBe(
      "单次最长 4 小时（traceId abc）",
    );
  });
});

describe("占位页", () => {
  it("显示任务与接口", () => {
    render(<TodoPage href="/m1/history" />);
    expect(screen.getByText("待实现 · 任务 M1-T05")).toBeDefined();
    expect(screen.getByText("GET /api/m1/v1/bookings/history")).toBeDefined();
  });
});
