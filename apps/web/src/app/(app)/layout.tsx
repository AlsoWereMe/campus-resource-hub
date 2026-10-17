import { AppFrame } from "@/shell/AppFrame";
import { RequireAuth } from "@/shell/auth";

export default function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <RequireAuth>
      <AppFrame>{children}</AppFrame>
    </RequireAuth>
  );
}
