// 占位页：页面未实现时显示对应的任务、需求与接口。实现页面时把整个 page.tsx 换成真实内容。

import { Badge, Card, PageHeader } from "./ui";
import { findPage, type MenuItem } from "./menu";

export function Todo({ page }: { page: MenuItem }) {
  return (
    <div>
      <PageHeader title={page.title}>
        {page.task && <Badge tone="amber">待实现 · 任务 {page.task}</Badge>}
      </PageHeader>
      <Card>
        <div className="space-y-4 text-sm text-slate-700">
          {page.task && (
            <p>
              在 agent 中输入 <code className="rounded bg-slate-100 px-1.5 py-0.5">做任务 {page.task}</code>
              ，任务卡见 <code className="rounded bg-slate-100 px-1.5 py-0.5">docs/tasks.md</code>。
            </p>
          )}
          {page.requirements && (
            <div>
              <p className="font-medium text-slate-900">需求</p>
              <ul className="mt-1 list-disc pl-5">
                {page.requirements.map((r) => (
                  <li key={r}>{r}</li>
                ))}
              </ul>
            </div>
          )}
          {page.endpoints && (
            <div>
              <p className="font-medium text-slate-900">接口（契约见 contracts/）</p>
              <ul className="mt-1 list-disc pl-5 font-mono text-xs">
                {page.endpoints.map((e) => (
                  <li key={e}>{e}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </Card>
    </div>
  );
}

/** 按路径从页面登记表中取出占位信息。 */
export function TodoPage({ href }: { href: string }) {
  const page = findPage(href);
  if (!page) throw new Error(`页面 ${href} 未在 src/shell/menu.ts 登记`);
  return <Todo page={page} />;
}
