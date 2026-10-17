import type { NextConfig } from "next";

// 静态导出（架构 §9、ADR-011）：生产由 Nginx 托管 out/，不需要 Node 运行时。
// 开发时经网关 http://127.0.0.1:8080 访问，/api 由网关转发到各服务。
const config: NextConfig = {
  output: "export",
  trailingSlash: true,
  images: { unoptimized: true },
  allowedDevOrigins: ["127.0.0.1", "localhost"],
  // 不让 next dev 自动生成 AGENTS.md；Next 16 的注意事项已写入 apps/README.md
  agentRules: false,
  env: {
    NEXT_PUBLIC_APP_VERSION: process.env.APP_VERSION ?? "dev",
    NEXT_PUBLIC_GIT_SHA: process.env.GIT_SHA ?? "local",
  },
};

export default config;
