"use client";

import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const revenueData = [
  { month: "May 1", revenue: 16800 },
  { month: "May 5", revenue: 19200 },
  { month: "May 9", revenue: 18100 },
  { month: "May 13", revenue: 22400 },
  { month: "May 17", revenue: 24800 },
  { month: "May 21", revenue: 23100 },
  { month: "May 25", revenue: 27600 },
  { month: "May 29", revenue: 30200 },
  { month: "Jun 2", revenue: 28900 },
  { month: "Jun 6", revenue: 32400 },
  { month: "Jun 10", revenue: 31100 },
  { month: "Jun 14", revenue: 34700 },
  { month: "Jun 18", revenue: 33200 },
  { month: "Jun 22", revenue: 37100 },
  { month: "Jun 26", revenue: 39800 },
  { month: "Jun 30", revenue: 42100 },
];

function formatCurrency(value: number) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(value);
}

function RevenueTooltip({
  active,
  payload,
  label,
}: {
  active?: boolean;
  payload?: Array<{
    value?: number;
  }>;
  label?: string;
}) {
  if (!active || !payload?.length) {
    return null;
  }

  const value = payload[0]?.value;

  return (
    <div className="rounded-lg border border-border bg-card px-3 py-2.5 shadow-lg">
      <p className="text-xs font-medium text-muted-foreground">
        {label}
      </p>

      <p className="mt-1 text-sm font-semibold text-card-foreground">
        {typeof value === "number" ? formatCurrency(value) : "—"}
      </p>
    </div>
  );
}

export function RevenueChart() {
  return (
    <div className="mt-6 h-[300px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart
          data={revenueData}
          margin={{
            top: 8,
            right: 8,
            left: -12,
            bottom: 0,
          }}
        >
          <CartesianGrid
            strokeDasharray="3 3"
            className="stroke-border"
            vertical={false}
          />

          <XAxis
            dataKey="month"
            tickLine={false}
            axisLine={false}
            tickMargin={10}
            minTickGap={28}
            className="text-[11px] fill-muted-foreground"
          />

          <YAxis
            tickLine={false}
            axisLine={false}
            tickMargin={8}
            width={55}
            tickFormatter={(value) =>
              `$${Number(value) / 1000}K`
            }
            className="text-[11px] fill-muted-foreground"
          />

          <Tooltip
            cursor={{
              stroke: "var(--border)",
              strokeWidth: 1,
            }}
            content={<RevenueTooltip />}
          />

          <Line
            type="monotone"
            dataKey="revenue"
            stroke="var(--primary)"
            strokeWidth={2.5}
            dot={false}
            activeDot={{
              r: 5,
              strokeWidth: 2,
              fill: "var(--card)",
            }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}