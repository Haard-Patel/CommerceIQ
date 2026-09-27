import type { ReactNode } from "react";
import { ArrowDownRight, ArrowUpRight } from "lucide-react";

type KpiCardProps = {
  label: string;
  value: string;
  change: string;
  changeLabel?: string;
  icon: ReactNode;
  positive?: boolean;
};

export function KpiCard({
  label,
  value,
  change,
  changeLabel = "vs. previous period",
  icon,
  positive = true,
}: KpiCardProps) {
  const TrendIcon = positive ? ArrowUpRight : ArrowDownRight;

  return (
    <div className="group rounded-xl border border-border bg-card p-5 transition-all duration-200 hover:-translate-y-0.5 hover:shadow-md">
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <p className="text-sm font-medium text-muted-foreground">
            {label}
          </p>

          <p className="mt-2 truncate text-2xl font-semibold tracking-tight text-card-foreground">
            {value}
          </p>
        </div>

        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg border border-border bg-background text-muted-foreground transition-colors group-hover:text-foreground">
          {icon}
        </div>
      </div>

      <div className="mt-4 flex items-center gap-1.5 text-xs">
        <span
          className={`inline-flex items-center gap-0.5 font-semibold ${
            positive ? "text-success" : "text-danger"
          }`}
        >
          <TrendIcon className="h-3.5 w-3.5" strokeWidth={2.2} />
          {change}
        </span>

        <span className="text-muted-foreground">
          {changeLabel}
        </span>
      </div>
    </div>
  );
}