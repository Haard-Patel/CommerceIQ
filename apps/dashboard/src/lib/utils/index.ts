export function formatCurrency(
    value: number,
    currency = "USD",
  ): string {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency,
      maximumFractionDigits: 2,
    }).format(value);
  }
  
  export function formatNumber(value: number): string {
    return new Intl.NumberFormat("en-US").format(value);
  }
  
  export function formatPercentage(
    value: number,
    fractionDigits = 1,
  ): string {
    return `${value.toFixed(fractionDigits)}%`;
  }
  
  export function formatDuration(hours: number): string {
    if (hours < 1) {
      return `${Math.round(hours * 60)} min`;
    }
  
    if (hours < 24) {
      return `${hours.toFixed(1)} hrs`;
    }
  
    return `${(hours / 24).toFixed(1)} days`;
  }