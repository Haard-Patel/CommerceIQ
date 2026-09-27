/**
 * CommerceIQ shared application types.
 *
 * These types describe common structures used across
 * dashboard features, API responses, filters, and analytics.
 */

export type DateRange = {
    from: string;
    to: string;
  };
  
  export type MetricValue = {
    value: number;
    previousValue?: number;
    changePercent?: number;
  };
  
  export type MetricCardData = {
    label: string;
    value: string;
    description?: string;
    change?: number;
    trend?: "up" | "down" | "neutral";
  };
  
  export type AnalyticsStatus =
    | "loading"
    | "success"
    | "error"
    | "empty";
  
  export type SelectOption = {
    label: string;
    value: string;
  };
  
  export type Pagination = {
    page: number;
    pageSize: number;
    total: number;
    totalPages: number;
  };