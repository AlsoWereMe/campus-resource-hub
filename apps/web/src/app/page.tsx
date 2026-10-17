"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";

import { useAuth } from "@/shell/auth";
import { visibleMenu } from "@/shell/menu";

/** 入口：未登录去登录页；已登录去菜单中的第一个页面。 */
export default function Home() {
  const { me, loading } = useAuth();
  const router = useRouter();
  useEffect(() => {
    if (loading) return;
    const first = me ? visibleMenu(me.permissions)[0]?.items[0]?.href : undefined;
    router.replace(first ? `${first}/` : "/login/");
  }, [loading, me, router]);
  return <p className="p-6 text-sm text-slate-500">加载中…</p>;
}
