type Channel = {
    name: string;
    percentage: number;
    revenue: number;
  };
  
  const channels: Channel[] = [
    {
      name: "Organic",
      percentage: 42,
      revenue: 119500,
    },
    {
      name: "Paid",
      percentage: 27,
      revenue: 76800,
    },
    {
      name: "Direct",
      percentage: 18,
      revenue: 51200,
    },
    {
      name: "Referral",
      percentage: 13,
      revenue: 37100,
    },
  ];
  
  function formatCurrency(value: number) {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      maximumFractionDigits: 0,
    }).format(value);
  }
  
  export function ChannelBreakdown() {
    return (
      <div className="mt-6 space-y-5">
        {channels.map((channel) => (
          <div key={channel.name}>
            <div className="flex items-center justify-between gap-4">
              <div className="flex min-w-0 items-center gap-2.5">
                <span className="h-2 w-2 shrink-0 rounded-full bg-primary" />
  
                <span className="truncate text-sm font-medium text-card-foreground">
                  {channel.name}
                </span>
              </div>
  
              <div className="flex shrink-0 items-center gap-3 text-xs">
                <span className="font-semibold text-card-foreground">
                  {channel.percentage}%
                </span>
  
                <span className="text-muted-foreground">
                  {formatCurrency(channel.revenue)}
                </span>
              </div>
            </div>
  
            <div className="mt-2 h-2 overflow-hidden rounded-full bg-muted">
              <div
                className="h-full rounded-full bg-primary transition-all duration-500"
                style={{
                  width: `${channel.percentage}%`,
                }}
              />
            </div>
          </div>
        ))}
      </div>
    );
  }