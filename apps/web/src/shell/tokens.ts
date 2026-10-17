// 登录令牌的保存与刷新（IAM-AUTH-01）。
// 取舍：令牌存 localStorage，刷新页面后仍保持登录；代价是 XSS 时可能被窃取，
// 因此前端不得渲染未转义的 HTML（禁止 dangerouslySetInnerHTML 渲染用户输入）。

export type Tokens = { accessToken: string; refreshToken: string; expiresAt: number };

const KEY = "campus.tokens";
const IAM = "/api/iam/v1";

function read(): Tokens | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = window.localStorage.getItem(KEY);
    return raw ? (JSON.parse(raw) as Tokens) : null;
  } catch {
    return null;
  }
}

function write(tokens: Tokens | null): void {
  if (typeof window === "undefined") return;
  if (tokens) window.localStorage.setItem(KEY, JSON.stringify(tokens));
  else window.localStorage.removeItem(KEY);
}

type TokenResponse = { accessToken: string; refreshToken?: string | null; expiresIn: number };

function save(body: TokenResponse, fallbackRefresh = ""): string {
  write({
    accessToken: body.accessToken,
    refreshToken: body.refreshToken ?? fallbackRefresh,
    expiresAt: Date.now() + body.expiresIn * 1000,
  });
  return body.accessToken;
}

let refreshing: Promise<string | null> | null = null;

async function refresh(): Promise<string | null> {
  const current = read();
  if (!current) return null;
  const response = await fetch(`${IAM}/auth/refresh`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refreshToken: current.refreshToken }),
  });
  if (!response.ok) {
    write(null);
    return null;
  }
  return save((await response.json()) as TokenResponse);
}

/** 有效的访问令牌：快过期时自动刷新（多个请求只刷新一次）；未登录返回 null。 */
export async function accessToken(): Promise<string | null> {
  const current = read();
  if (!current) return null;
  if (current.expiresAt - Date.now() > 60_000) return current.accessToken;
  refreshing ??= refresh().finally(() => {
    refreshing = null;
  });
  return refreshing;
}

export function hasTokens(): boolean {
  return read() !== null;
}

/** 登录成功返回 null；失败返回后端错误体。 */
export async function login(
  username: string,
  password: string,
): Promise<{ code: string; message: string } | null> {
  const response = await fetch(`${IAM}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  const body = await response.json();
  if (!response.ok) return body as { code: string; message: string };
  save(body as TokenResponse);
  return null;
}

export async function logout(): Promise<void> {
  const current = read();
  write(null);
  if (current) {
    await fetch(`${IAM}/auth/logout`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refreshToken: current.refreshToken }),
    }).catch(() => undefined);
  }
}
