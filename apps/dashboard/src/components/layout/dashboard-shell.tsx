import type { ReactNode } from "react";

import { Header } from "@/components/layout/header";
import { Sidebar } from "@/components/layout/sidebar";

type DashboardShellProps = {
  children: ReactNode;
  title?: string;
};

export function DashboardShell({
  children,
  title = "Overview",
}: DashboardShellProps) {
  return (
    <div className="h-screen overflow-hidden bg-background text-foreground">
      <div className="flex h-screen">
        {/* Persistent sidebar */}
        <Sidebar />

        {/* Application area */}
        <div className="flex min-w-0 flex-1 flex-col">
          {/* Persistent header */}
          <div className="z-30 shrink-0">
            <Header title={title} />
          </div>

          {/* Scrollable page content */}
          <main className="min-h-0 flex-1 overflow-y-auto">
            {children}
          </main>
        </div>
      </div>
    </div>
  );
}