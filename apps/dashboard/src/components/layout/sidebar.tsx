"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  BarChart3,
  Boxes,
  BrainCircuit,
  ChevronRight,
  CircleAlert,
  FileBarChart,
  LayoutDashboard,
  Settings,
  ShoppingCart,
  Users,
} from "lucide-react";

import { APP_NAME, NAVIGATION_ITEMS } from "@/lib/constants/app";

const ICONS = {
  "/": LayoutDashboard,
  "/sales": BarChart3,
  "/orders": ShoppingCart,
  "/products": Boxes,
  "/customers": Users,
  "/marketing": BrainCircuit,
  "/reports": FileBarChart,
  "/anomalies": CircleAlert,
  "/settings": Settings,
} as const;

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="flex h-screen w-64 shrink-0 flex-col border-r border-border bg-card">
      {/* Brand */}
      <div className="flex h-16 items-center border-b border-border px-5">
        <Link
          href="/"
          className="group flex items-center gap-3"
          aria-label={APP_NAME}
        >
          <div className="flex h-9 w-9 items-center justify-center rounded-lg border border-border bg-background transition-colors group-hover:bg-muted">
            <span className="text-sm font-black tracking-[-0.08em] text-foreground">
              CIQ
            </span>
          </div>

          <div className="flex flex-col leading-none">
            <span className="text-[15px] font-bold tracking-tight text-foreground">
              CommerceIQ
            </span>

            <span className="mt-1 text-[10px] font-medium uppercase tracking-[0.14em] text-muted-foreground">
              Intelligence
            </span>
          </div>
        </Link>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto p-3">
        <div className="mb-3 px-3 text-[10px] font-semibold uppercase tracking-[0.14em] text-muted-foreground">
          Workspace
        </div>

        <div className="space-y-1">
          {NAVIGATION_ITEMS.map((item) => {
            const Icon =
              ICONS[item.href as keyof typeof ICONS] ?? LayoutDashboard;

            const isActive =
              pathname === item.href ||
              (item.href !== "/" && pathname.startsWith(`${item.href}/`));

            return (
              <Link
                key={item.href}
                href={item.href}
                className={`group flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-all ${
                  isActive
                    ? "bg-muted text-foreground"
                    : "text-muted-foreground hover:bg-muted/70 hover:text-foreground"
                }`}
              >
                <Icon
                  className={`h-[17px] w-[17px] shrink-0 transition-colors ${
                    isActive
                      ? "text-foreground"
                      : "text-muted-foreground group-hover:text-foreground"
                  }`}
                  strokeWidth={isActive ? 2.2 : 1.8}
                />

                <span className="flex-1 truncate">{item.label}</span>

                {isActive && (
                  <ChevronRight
                    className="h-3.5 w-3.5 text-muted-foreground"
                    strokeWidth={2}
                  />
                )}
              </Link>
            );
          })}
        </div>
      </nav>

      {/* Bottom section */}
      <div className="border-t border-border p-3">
        <div className="rounded-lg bg-muted/60 px-3 py-3">
          <p className="text-xs font-medium text-foreground">
            Commerce Intelligence
          </p>

          <p className="mt-1 text-[11px] leading-relaxed text-muted-foreground">
            Turn commerce data into actionable insights.
          </p>
        </div>
      </div>
    </aside>
  );
}
