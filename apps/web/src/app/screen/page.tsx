import { TodoPage } from "@/shell/Todo";

/** 自习室屏幕端：全屏、无需登录，用设备令牌取签到码。 */
export default function ScreenPage() {
  return (
    <main className="p-6">
      <TodoPage href="/screen" />
    </main>
  );
}
