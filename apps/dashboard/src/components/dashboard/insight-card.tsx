import {
    ArrowUpRight,
    BrainCircuit,
    CircleAlert,
    TrendingUp,
  } from "lucide-react";
  
  type InsightType = "positive" | "info" | "warning";
  
  type InsightCardProps = {
    type: InsightType;
    title: string;
    description: string;
  };
  
  const insightConfig = {
    positive: {
      icon: TrendingUp,
      iconClassName: "text-success",
      iconBackground: "bg-success/10",
    },
    info: {
      icon: BrainCircuit,
      iconClassName: "text-info",
      iconBackground: "bg-info/10",
    },
    warning: {
      icon: CircleAlert,
      iconClassName: "text-warning",
      iconBackground: "bg-warning/10",
    },
  };
  
  export function InsightCard({
    type,
    title,
    description,
  }: InsightCardProps) {
    const config = insightConfig[type];
    const Icon = config.icon;
  
    return (
      <div className="group rounded-lg border border-border bg-background p-4 transition-all duration-200 hover:border-ring/60 hover:shadow-sm">
        <div className="flex items-start gap-3">
          <div
            className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-lg ${config.iconBackground}`}
          >
            <Icon
              className={`h-4 w-4 ${config.iconClassName}`}
              strokeWidth={2}
            />
          </div>
  
          <div className="min-w-0 flex-1">
            <div className="flex items-start justify-between gap-3">
              <p className="text-sm font-medium text-card-foreground">
                {title}
              </p>
  
              <ArrowUpRight
                className="h-3.5 w-3.5 shrink-0 text-muted-foreground opacity-0 transition-all duration-200 group-hover:-translate-y-0.5 group-hover:translate-x-0.5 group-hover:opacity-100"
                strokeWidth={1.8}
              />
            </div>
  
            <p className="mt-1 text-xs leading-relaxed text-muted-foreground">
              {description}
            </p>
          </div>
        </div>
      </div>
    );
  }