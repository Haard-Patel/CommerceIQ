"use client";

import { CalendarDays, ChevronDown } from "lucide-react";

type DateRangeSelectorProps = {
  label?: string;
};

export function DateRangeSelector({
  label = "Last 30 days",
}: DateRangeSelectorProps) {
  return (
    <button
      type="button"
      className="group inline-flex h-9 items-center gap-2 rounded-lg border border-border bg-card px-3 text-sm font-medium text-foreground shadow-sm transition-all hover:bg-muted"
      aria-label="Select date range"
    >
      <CalendarDays className="h-4 w-4 text-muted-foreground" />

      <span>{label}</span>

      <ChevronDown className="h-3.5 w-3.5 text-muted-foreground transition-transform group-hover:translate-y-px" />
    </button>
  );
}