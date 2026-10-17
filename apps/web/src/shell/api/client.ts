// 各模块的类型化 API 客户端。类型由 contracts/ 生成（pnpm gen:api），不要手写请求与响应类型。
// 用法：const { data, error } = await api.m1.GET("/api/m1/v1/bookings/current");
// 规则：模块页面只调用本模块的客户端；需要其他模块时用页面跳转（apps/README.md）。

import createClient, { type Middleware } from "openapi-fetch";

import { accessToken } from "../tokens";
import type { paths as AuditPaths } from "./types/audit";
import type { paths as IamPaths } from "./types/iam";
import type { paths as M1Paths } from "./types/m1";
import type { paths as M2Paths } from "./types/m2";
import type { paths as M3Paths } from "./types/m3";
import type { paths as NotifyPaths } from "./types/notify";
import type { paths as SpacePaths } from "./types/space";

const withToken: Middleware = {
  async onRequest({ request }) {
    const token = await accessToken();
    if (token) request.headers.set("Authorization", `Bearer ${token}`);
    return request;
  },
};

// eslint-disable-next-line @typescript-eslint/no-empty-object-type
function client<Paths extends {}>() {
  const c = createClient<Paths>({ baseUrl: "" });
  c.use(withToken);
  return c;
}

export const api = {
  iam: client<IamPaths>(),
  space: client<SpacePaths>(),
  notify: client<NotifyPaths>(),
  audit: client<AuditPaths>(),
  m1: client<M1Paths>(),
  m2: client<M2Paths>(),
  m3: client<M3Paths>(),
};

export type { components as IamSchemas } from "./types/iam";
export type { components as M1Schemas } from "./types/m1";
export type { components as M2Schemas } from "./types/m2";
export type { components as M3Schemas } from "./types/m3";
export type { components as NotifySchemas } from "./types/notify";
export type { components as SpaceSchemas } from "./types/space";
