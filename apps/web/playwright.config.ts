import { defineConfig } from "@playwright/test";

// E2E：需先 make up 与 make web，再运行 pnpm e2e（首次运行前：pnpm exec playwright install chromium）。
export default defineConfig({
  testDir: "./e2e",
  use: { baseURL: process.env.E2E_BASE_URL ?? "http://127.0.0.1:8080" },
});
