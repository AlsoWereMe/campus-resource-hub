"use client";

import { usePathname, useRouter } from "next/navigation";
import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";

import { api, type IamSchemas } from "./api/client";
import { hasTokens, logout } from "./tokens";

export type Me = IamSchemas["schemas"]["MeOut"];

type AuthState = {
  me: Me | null;
  loading: boolean;
  /** 是否持有任一权限点；不传参数表示只要已登录。 */
  can: (...perms: string[]) => boolean;
  reload: () => Promise<void>;
  signOut: () => Promise<void>;
};

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [me, setMe] = useState<Me | null>(null);
  const [loading, setLoading] = useState(true);

  const reload = useCallback(async () => {
    setLoading(true);
    if (!hasTokens()) {
      setMe(null);
    } else {
      const { data } = await api.iam.GET("/api/iam/v1/me");
      setMe(data ?? null);
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    void reload();
  }, [reload]);

  const value = useMemo<AuthState>(
    () => ({
      me,
      loading,
      can: (...perms) =>
        me !== null && (perms.length === 0 || perms.some((p) => me.permissions.includes(p))),
      reload,
      signOut: async () => {
        await logout();
        setMe(null);
      },
    }),
    [me, loading, reload],
  );
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthState {
  const state = useContext(AuthContext);
  if (!state) throw new Error("useAuth 必须在 AuthProvider 内使用");
  return state;
}

/** 未登录时跳转到登录页，登录后回到当前页面。 */
export function RequireAuth({ children }: { children: React.ReactNode }) {
  const { me, loading } = useAuth();
  const router = useRouter();
  const pathname = usePathname();
  useEffect(() => {
    if (!loading && !me) router.replace(`/login/?next=${encodeURIComponent(pathname)}`);
  }, [loading, me, pathname, router]);
  if (loading || !me) return <p className="p-6 text-sm text-slate-500">加载中…</p>;
  return <>{children}</>;
}
