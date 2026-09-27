import {
  ArrowUpRight,
  BarChart3,
  ShoppingCart,
  Target,
  Users,
} from "lucide-react";

import { DashboardShell } from "@/components/layout/dashboard-shell";
import { KpiCard } from "@/components/dashboard/kpi-card";
import { PageContainer } from "@/components/ui/page-container";
import { RevenueChart } from "@/components//dashboard/revenue-charts"; // Adjusted the path to the correct location.
import { DateRangeSelector } from "@/components/dashboard/date-range-selector";
import {
  SectionHeader,
  SectionLink,
} from "@/components/dashboard/section-header";
import { ChannelBreakdown } from "@/components/dashboard/channel-breakdown";
import { InsightCard } from "@/components/dashboard/insight-card";

export default function Home() {
  return (
    <DashboardShell title="Overview">
      <PageContainer>
        <div className="space-y-8">
          {/* Page introduction */}
          <section>
            <div className="flex items-end justify-between gap-4">
              <div>
                <p className="text-sm font-medium text-primary">
                  Commerce performance
                </p>

                <h2 className="mt-1 text-2xl font-semibold tracking-tight">
                  Overview
                </h2>

                <p className="mt-2 max-w-2xl text-sm text-muted-foreground">
                  Monitor sales, customers, conversion, and business
                  performance from one intelligence workspace.
                </p>
              </div>

              <div className="hidden sm:block">
  <DateRangeSelector />
</div>
            </div>
          </section>

          {/* KPI cards */}
          <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            <KpiCard
              label="Revenue"
              value="$284.6K"
              change="+12.8%"
              icon={<BarChart3 className="h-4 w-4" />}
            />

            <KpiCard
              label="Orders"
              value="8,421"
              change="+8.4%"
              icon={<ShoppingCart className="h-4 w-4" />}
            />

            <KpiCard
              label="Average Order Value"
              value="$33.80"
              change="+3.2%"
              icon={<ArrowUpRight className="h-4 w-4" />}
            />

            <KpiCard
              label="Conversion Rate"
              value="3.84%"
              change="+0.6%"
              icon={<Target className="h-4 w-4" />}
            />
          </section>

          {/* Main analytics */}
          <section className="grid gap-4 xl:grid-cols-[minmax(0,2fr)_minmax(320px,1fr)]">
            {/* Revenue chart placeholder */}
            <div className="rounded-xl border border-border bg-card p-5">
            <SectionHeader
  title="Revenue performance"
  description="Revenue trend across the selected period."
  action={<SectionLink />}
/>

              <RevenueChart />
            </div>

            {/* Customer snapshot */}
            <div className="rounded-xl border border-border bg-card p-5">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="font-semibold tracking-tight">
                    Customer snapshot
                  </h3>

                  <p className="mt-1 text-sm text-muted-foreground">
                    Current customer activity.
                  </p>
                </div>

                <Users className="h-5 w-5 text-muted-foreground" />
              </div>

              <div className="mt-6 space-y-5">
                <div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-muted-foreground">
                      Active customers
                    </span>

                    <span className="font-semibold">
                      12,482
                    </span>
                  </div>

                  <div className="mt-2 h-2 overflow-hidden rounded-full bg-muted">
                    <div className="h-full w-[72%] rounded-full bg-primary" />
                  </div>
                </div>

                <div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-muted-foreground">
                      Returning customers
                    </span>

                    <span className="font-semibold">
                      38.6%
                    </span>
                  </div>

                  <div className="mt-2 h-2 overflow-hidden rounded-full bg-muted">
                    <div className="h-full w-[39%] rounded-full bg-primary" />
                  </div>
                </div>

                <div className="border-t border-border pt-5">
                  <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
                    Customer revenue
                  </p>

                  <p className="mt-2 text-2xl font-semibold tracking-tight">
                    $167.4K
                  </p>

                  <p className="mt-1 text-xs text-success">
                    +14.2% vs. previous period
                  </p>
                </div>
              </div>
            </div>
          </section>

          {/* Lower analytics */}
          <section className="grid gap-4 lg:grid-cols-2">
            <div className="rounded-xl border border-border bg-card p-5">
              <h3 className="font-semibold tracking-tight">
                Sales by channel
              </h3>

              <p className="mt-1 text-sm text-muted-foreground">
                Revenue contribution across acquisition channels.
              </p>

              <ChannelBreakdown />
            </div>
            <div className="rounded-xl border border-border bg-card p-5">
  <SectionHeader
    title="Intelligence"
    description="Signals detected across your commerce data."
    action={<SectionLink label="View all" />}
  />

  <div className="mt-6 space-y-3">
    <InsightCard
      type="positive"
      title="Revenue growth detected"
      description="Revenue is trending above the previous 30-day period."
    />

    <InsightCard
      type="positive"
      title="Customer retention improving"
      description="Returning customer revenue has increased during the selected period."
    />

    <InsightCard
      type="info"
      title="Forecasting pipeline"
      description="Historical data will feed the forecasting models in the analytics layer."
    />
  </div>
</div>
          </section>
        </div>
      </PageContainer>
    </DashboardShell>
  );
}
