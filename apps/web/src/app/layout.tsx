import type { Metadata, Viewport } from "next";

import { Providers } from "@/shell/providers";

import "./globals.css";

export const metadata: Metadata = { title: "校园资源服务平台" };
export const viewport: Viewport = { width: "device-width", initialScale: 1 };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
