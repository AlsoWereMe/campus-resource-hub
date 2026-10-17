// 全部页面的登记表：菜单按权限点显示；页面未实现时，占位页从这里读取任务、需求与接口。
// 实现页面时只需改对应的 page.tsx，本文件一般不用改（新增页面时才在此登记）。

export type MenuItem = {
  href: string;
  title: string;
  group: string;
  /** 持有任一即可见；空数组表示登录即可见 */
  perms: string[];
  task?: string;
  requirements?: string[];
  endpoints?: string[];
};

export const MENU: MenuItem[] = [
  // ---------- 学生端：自习座位（M1） ----------
  {
    href: "/m1/search",
    title: "找座位",
    group: "自习座位",
    perms: ["m1:seat:search"],
    task: "M1-T03",
    requirements: ["M1-RSV-01", "M1-SRH-01", "M1-SRH-02", "M1-RSV-02（预约弹窗，M1-T04）"],
    endpoints: [
      "GET /api/m1/v1/rooms",
      "GET /api/m1/v1/seats/search",
      "GET /api/m1/v1/seats/{seat_id}/timeline",
      "POST /api/m1/v1/bookings（M1-T04）",
    ],
  },
  {
    href: "/m1/bookings",
    title: "我的预约",
    group: "自习座位",
    perms: ["m1:booking:view-own"],
    task: "M1-T04",
    requirements: ["M1-RSV-03", "M1-RSV-04", "M1-CHK-03（签到，M1-T09）"],
    endpoints: [
      "GET /api/m1/v1/bookings/current",
      "POST /api/m1/v1/bookings/{booking_id}/cancel",
      "POST /api/m1/v1/bookings/{booking_id}/checkin（M1-T09）",
    ],
  },
  {
    href: "/m1/history",
    title: "历史预约",
    group: "自习座位",
    perms: ["m1:booking:view-own"],
    task: "M1-T05",
    requirements: ["M1-HIS-01", "M1-HIS-02"],
    endpoints: ["GET /api/m1/v1/bookings/history", "GET /api/m1/v1/bookings/{booking_id}/rebook"],
  },
  {
    href: "/m1/violations",
    title: "我的违约",
    group: "自习座位",
    perms: ["m1:violation:view-own"],
    task: "M1-T11",
    requirements: ["M1-VIO-02", "M1-VIO-03"],
    endpoints: ["GET /api/m1/v1/violations/mine"],
  },
  // ---------- 整间教室（M2） ----------
  {
    href: "/m2/rooms",
    title: "申请整间教室",
    group: "整间教室",
    perms: ["m2:application:create"],
    task: "M2-T04",
    requirements: ["M2-ROOM-01（M2-T01）", "M2-ELG-01 ~ 05（M2-T02）", "M2-APP-01"],
    endpoints: [
      "GET /api/m2/v1/rooms（M2-T01）",
      "GET /api/m2/v1/rooms/{room_id}/conflicts（M2-T01）",
      "POST /api/m2/v1/applications/check（M2-T02）",
      "POST /api/m2/v1/applications",
    ],
  },
  {
    href: "/m2/applications",
    title: "我的申请",
    group: "整间教室",
    perms: ["m2:application:manage-own"],
    task: "M2-T04",
    requirements: ["M2-QRY-01", "M2-APV-04", "M2-APP-03", "M2-APP-04"],
    endpoints: [
      "GET /api/m2/v1/applications/mine",
      "GET /api/m2/v1/applications/{application_id}",
      "POST /api/m2/v1/applications/{application_id}/withdraw",
      "POST /api/m2/v1/applications/{application_id}/cancel",
    ],
  },
  {
    href: "/m2/approvals",
    title: "待我审批",
    group: "整间教室",
    perms: ["m2:approval:act"],
    task: "M2-T05",
    requirements: ["M2-APV-01 ~ 05"],
    endpoints: [
      "GET /api/m2/v1/approvals/pending",
      "GET /api/m2/v1/approvals/done",
      "POST /api/m2/v1/applications/{application_id}/approve",
      "POST /api/m2/v1/applications/{application_id}/reject",
    ],
  },
  // ---------- 报修（M3） ----------
  {
    href: "/m3/report",
    title: "我要报修",
    group: "报修",
    perms: ["m3:workorder:create"],
    task: "M3-T01",
    requirements: ["M3-RPT-01", "M3-RPT-03"],
    endpoints: [
      "GET /api/m3/v1/categories",
      "GET /api/space/v1/buildings、/rooms、/rooms/{room_id}/seats（位置级联，已实现）",
      "GET /api/m3/v1/workorders/duplicates",
      "POST /api/m3/v1/workorders",
    ],
  },
  {
    href: "/m3/mine",
    title: "我的报修",
    group: "报修",
    perms: ["m3:workorder:manage-own"],
    task: "M3-T01",
    requirements: ["M3-QRY-01", "M3-RPT-04", "M3-ACC-01、02（验收评价，M3-T04）"],
    endpoints: [
      "GET /api/m3/v1/workorders/mine",
      "GET /api/m3/v1/workorders/{work_order_id}",
      "POST /api/m3/v1/workorders/{work_order_id}/cancel",
      "POST /api/m3/v1/workorders/{work_order_id}/accept（M3-T04）",
    ],
  },
  {
    href: "/m3/workbench",
    title: "工单工作台",
    group: "报修",
    perms: ["m3:dispatch:act", "m3:repair:act"],
    task: "M3-T06",
    requirements: ["M3-QRY-02", "M3-DSP-01（M3-T02）", "M3-WRK-01、04（M3-T03）"],
    endpoints: [
      "GET /api/m3/v1/workorders",
      "POST /api/m3/v1/workorders/{work_order_id}/assign（M3-T02）",
      "POST /api/m3/v1/workorders/{work_order_id}/start、/complete（M3-T03）",
    ],
  },
  // ---------- 消息与账号 ----------
  {
    href: "/inbox",
    title: "消息",
    group: "我的",
    perms: [],
    task: "D-T05",
    requirements: ["NTF-03"],
    endpoints: [
      "GET /api/notify/v1/inbox",
      "GET /api/notify/v1/inbox/unread-count",
      "POST /api/notify/v1/inbox/{message_id}/read",
    ],
  },
  { href: "/account", title: "账号与口令", group: "我的", perms: [] },
  // ---------- 管理：座位运营（M1） ----------
  {
    href: "/admin/m1/dashboard",
    title: "运营看板",
    group: "座位运营",
    perms: ["m1:stats:view"],
    task: "M1-T13",
    requirements: ["M1-OPS-01", "M1-OPS-03", "M1-OPS-04", "M1-OPS-05"],
    endpoints: [
      "GET /api/m1/v1/admin/dashboard",
      "GET /api/m1/v1/admin/stats",
      "GET /api/m1/v1/admin/stats/flags",
      "GET /api/m1/v1/admin/export/stats.csv",
    ],
  },
  {
    href: "/admin/m1/bookings",
    title: "预约明细",
    group: "座位运营",
    perms: ["m1:booking:view-all"],
    task: "M1-T13",
    requirements: ["M1-OPS-02", "M1-RSV-07（处置，M1-T12）"],
    endpoints: [
      "GET /api/m1/v1/admin/bookings",
      "POST /api/m1/v1/admin/bookings/{booking_id}/cancel（M1-T12）",
    ],
  },
  {
    href: "/admin/m1/violations",
    title: "违约管理",
    group: "座位运营",
    perms: ["m1:violation:view-all"],
    task: "M1-T11",
    requirements: ["M1-VIO-02", "M1-VIO-04"],
    endpoints: [
      "GET /api/m1/v1/admin/violations",
      "POST /api/m1/v1/admin/violations/{violation_id}/revoke",
    ],
  },
  {
    href: "/admin/m1/screens",
    title: "屏幕终端",
    group: "座位运营",
    perms: ["m1:screen:manage"],
    task: "M1-T08",
    requirements: ["M1-CHK-02"],
    endpoints: ["GET /api/m1/v1/admin/screens", "POST /api/m1/v1/admin/screens"],
  },
  {
    href: "/admin/m1/trace",
    title: "座位状态追溯",
    group: "座位运营",
    perms: ["m1:trace:view"],
    task: "M1-T01",
    requirements: ["M1-INT-06"],
    endpoints: ["GET /api/m1/v1/admin/trace", "GET /api/m1/v1/admin/trace/history"],
  },
  {
    href: "/admin/m1/settings",
    title: "预约参数",
    group: "座位运营",
    perms: ["m1:setting:manage"],
    task: "M1-T02",
    requirements: ["M1-CFG-01"],
    endpoints: ["GET /api/m1/v1/admin/settings", "PUT /api/m1/v1/admin/settings"],
  },
  // ---------- 管理：整间预约（M2） ----------
  {
    href: "/admin/m2/applications",
    title: "申请管理",
    group: "整间预约管理",
    perms: ["m2:application:view-all"],
    task: "M2-T07",
    requirements: ["M2-QRY-02", "M2-APP-06", "M2-INT-03"],
    endpoints: [
      "GET /api/m2/v1/admin/applications",
      "POST /api/m2/v1/admin/applications/{application_id}/revoke",
    ],
  },
  {
    href: "/admin/m2/flows",
    title: "审批链与参数",
    group: "整间预约管理",
    perms: ["m2:flow:manage"],
    task: "M2-T03",
    requirements: ["M2-FLOW-01", "M2-FLOW-02"],
    endpoints: ["GET /api/m2/v1/admin/flows", "POST /api/m2/v1/admin/flows", "PUT /api/m2/v1/admin/settings"],
  },
  // ---------- 管理：物业（M3） ----------
  {
    href: "/admin/m3/settings",
    title: "处理时限与类别",
    group: "物业管理",
    perms: ["m3:config:manage"],
    task: "M3-T05",
    requirements: ["M3-ESC-04"],
    endpoints: ["GET /api/m3/v1/admin/settings", "PUT /api/m3/v1/admin/categories"],
  },
  {
    href: "/admin/m3/stats",
    title: "工单统计",
    group: "物业管理",
    perms: ["m3:stats:view"],
    task: "M3-T06",
    requirements: ["M3-QRY-03", "M3-QRY-04"],
    endpoints: ["GET /api/m3/v1/admin/stats"],
  },
  // ---------- 管理：空间（D） ----------
  {
    href: "/admin/space/rooms",
    title: "房间与开放时间",
    group: "空间管理",
    perms: ["space:room:manage"],
    task: "D-T06",
    requirements: ["SPC-ROOM-01 ~ 06", "SPC-ROOM-03（开放时间，D-T07）"],
    endpoints: [
      "GET /api/space/v1/rooms（已实现）",
      "POST /api/space/v1/rooms",
      "POST /api/space/v1/rooms/{room_id}/study",
      "PUT /api/space/v1/rooms/{room_id}/opening-hours（D-T07）",
    ],
  },
  {
    href: "/admin/space/seats",
    title: "座位与标记",
    group: "空间管理",
    perms: ["space:seat:manage", "space:tag:manage"],
    task: "D-T08",
    requirements: ["SPC-SEAT-01 ~ 03", "SPC-TAG-01"],
    endpoints: [
      "GET /api/space/v1/rooms/{room_id}/seats（已实现）",
      "POST /api/space/v1/rooms/{room_id}/seats/batch",
      "POST /api/space/v1/seats/status",
      "POST /api/space/v1/seats/tags",
    ],
  },
  // ---------- 管理：账号与权限、通知与审计（D） ----------
  {
    href: "/admin/iam/users",
    title: "用户与院系",
    group: "账号与权限",
    perms: ["iam:user:manage"],
    task: "D-T02",
    requirements: ["IAM-AUTH-02", "IAM-USER-01"],
    endpoints: ["GET /api/iam/v1/users", "POST /api/iam/v1/users/import", "GET /api/iam/v1/departments"],
  },
  {
    href: "/admin/iam/roles",
    title: "角色与授权",
    group: "账号与权限",
    perms: ["iam:role:manage"],
    task: "D-T03",
    requirements: ["IAM-ROLE-01 ~ 04"],
    endpoints: ["GET /api/iam/v1/roles", "PATCH /api/iam/v1/roles/{role_id}", "PUT /api/iam/v1/users/{user_id}/roles"],
  },
  {
    href: "/admin/notify",
    title: "通知模板与投递",
    group: "通知与审计",
    perms: ["notify:template:manage", "notify:delivery:view"],
    task: "D-T05",
    requirements: ["NTF-02", "NTF-04"],
    endpoints: ["GET /api/notify/v1/templates", "GET /api/notify/v1/deliveries"],
  },
  {
    href: "/admin/audit",
    title: "审计查询",
    group: "通知与审计",
    perms: ["audit:log:view"],
    task: "D-T04",
    requirements: ["AUD-02"],
    endpoints: ["GET /api/audit/v1/logs"],
  },
];

/** 不在菜单中出现、但同样待实现的页面 */
export const HIDDEN_PAGES: MenuItem[] = [
  {
    href: "/screen",
    title: "自习室屏幕端",
    group: "",
    perms: [],
    task: "M1-T08",
    requirements: ["M1-CHK-02"],
    endpoints: ["GET /api/m1/v1/screen/code（请求头 X-Device-Token）"],
  },
  {
    href: "/checkin",
    title: "扫码签到",
    group: "",
    perms: ["m1:checkin:do"],
    task: "M1-T09",
    requirements: ["M1-CHK-04"],
    endpoints: ["GET /api/m1/v1/checkin/candidate", "POST /api/m1/v1/bookings/{booking_id}/checkin"],
  },
];

export function findPage(href: string): MenuItem | undefined {
  return [...MENU, ...HIDDEN_PAGES].find((item) => item.href === href);
}

/** 按权限点过滤并按分组排列菜单。 */
export function visibleMenu(permissions: string[]): { group: string; items: MenuItem[] }[] {
  const groups = new Map<string, MenuItem[]>();
  for (const item of MENU) {
    if (item.perms.length > 0 && !item.perms.some((p) => permissions.includes(p))) continue;
    groups.set(item.group, [...(groups.get(item.group) ?? []), item]);
  }
  return [...groups.entries()].map(([group, items]) => ({ group, items }));
}
