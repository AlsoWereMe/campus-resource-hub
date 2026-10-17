"use client";

// 已实现的参考页：读取当前用户、调用接口、处理统一错误。实现其他页面时照此写法。

import { useState } from "react";

import { api } from "@/shell/api/client";
import { useAuth } from "@/shell/auth";
import { errorMessage } from "@/shell/errors";
import { Alert, Badge, Button, Card, Field, Input, PageHeader } from "@/shell/ui";

export default function AccountPage() {
  const { me } = useAuth();
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [result, setResult] = useState<{ ok: boolean; text: string } | null>(null);

  async function changePassword(event: React.FormEvent) {
    event.preventDefault();
    const { error } = await api.iam.POST("/api/iam/v1/auth/password", {
      body: { oldPassword, newPassword },
    });
    setResult(error ? { ok: false, text: errorMessage(error) } : { ok: true, text: "口令已修改" });
    if (!error) {
      setOldPassword("");
      setNewPassword("");
    }
  }

  if (!me) return null;
  return (
    <div className="max-w-xl space-y-5">
      <PageHeader title="账号与口令" />
      <Card title="基本信息">
        <dl className="grid grid-cols-[6rem_1fr] gap-y-2 text-sm">
          <dt className="text-slate-500">学号 / 工号</dt>
          <dd>{me.username}</dd>
          <dt className="text-slate-500">姓名</dt>
          <dd>{me.name}</dd>
          <dt className="text-slate-500">院系</dt>
          <dd>{me.departmentName ?? "—"}</dd>
          <dt className="text-slate-500">角色</dt>
          <dd className="flex flex-wrap gap-1">
            {me.roles.map((r) => (
              <Badge key={r} tone="blue">
                {r}
              </Badge>
            ))}
          </dd>
        </dl>
      </Card>
      <Card title="修改口令">
        <form className="space-y-4" onSubmit={changePassword}>
          <Field label="原口令">
            <Input type="password" value={oldPassword} onChange={(e) => setOldPassword(e.target.value)} required />
          </Field>
          <Field label="新口令（至少 8 位）">
            <Input
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              minLength={8}
              required
            />
          </Field>
          {result && <Alert tone={result.ok ? "success" : "error"}>{result.text}</Alert>}
          <Button type="submit">保存</Button>
        </form>
      </Card>
    </div>
  );
}
