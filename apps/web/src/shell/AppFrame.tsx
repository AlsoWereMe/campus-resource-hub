"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useState } from "react";

import { useAuth } from "./auth";
import { visibleMenu } from "./menu";
import { cn } from "./ui";

const VERSION = `${process.env.NEXT_PUBLIC_APP_VERSION} · ${process.env.NEXT_PUBLIC_GIT_SHA}`;

/** 已登录区域的框架：顶栏、按权限生成的菜单（移动端折叠）、页脚版本号。 */
export function AppFrame({ children }: { children: React.ReactNode }) {
  const { me, signOut } = useAuth();
  const pathname = usePathname();
  const router = useRouter();
  const [open, setOpen] = useState(false);
  const groups = visibleMenu(me?.permissions ?? []);

  return (
    <div className="flex min-h-screen flex-col">
      <header className="flex items-center justify-between bg-slate-900 px-4 py-3 text-white">
        <button className="md:hidden" onClick={() => setOpen(!open)} aria-label="菜单">
          ☰
        </button>
        <Link href="/" className="font-semibold">
          校园资源服务平台
        </Link>
        <div className="flex items-center gap-3 text-sm">
          <span className="hidden sm:inline">{me?.name}</span>
          <button
            className="rounded bg-slate-700 px-2 py-1 hover:bg-slate-600"
            onClick={async () => {
              await signOut();
              router.replace("/login/");
            }}
          >
            退出
          </button>
        </div>
      </header>
      <div className="flex flex-1">
        <nav
          className={cn(
            "w-56 shrink-0 border-r border-slate-200 bg-white p-3 text-sm",
            open ? "block" : "hidden md:block",
          )}
        >
          {groups.map(({ group, items }) => (
            <div key={group} className="mb-4">
              <p className="px-2 pb-1 text-xs font-semibold text-slate-400">{group}</p>
              {items.map((item) => (
                <Link
                  key={item.href}
                  href={`${item.href}/`}
                  onClick={() => setOpen(false)}
                  className={cn(
                    "block rounded px-2 py-1.5 text-slate-700 hover:bg-slate-100",
                    pathname.startsWith(item.href) && "bg-blue-50 font-medium text-blue-700",
                  )}
                >
                  {item.title}
                </Link>
              ))}
            </div>
          ))}
        </nav>
        <main className="min-w-0 flex-1 p-4 md:p-6">{children}</main>
      </div>
      <footer className="border-t border-slate-200 px-4 py-2 text-xs text-slate-400">版本 {VERSION}</footer>
    </div>
  );
}
