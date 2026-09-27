export const APP_NAME = "CommerceIQ";

export const APP_DESCRIPTION =
  "E-Commerce Intelligence & Analytics Platform";

export const DEFAULT_DATE_RANGE = {
  from: "30d",
  to: "today",
} as const;

export const NAVIGATION_ITEMS = [
  {
    label: "Overview",
    href: "/",
  },
  {
    label: "Sales",
    href: "/sales",
  },
  {
    label: "Customers",
    href: "/customers",
  },
  {
    label: "Products",
    href: "/products",
  },
  {
    label: "Marketing",
    href: "/marketing",
  },
  {
    label: "Funnel",
    href: "/funnel",
  },
  {
    label: "Forecasting",
    href: "/forecasting",
  },
  {
    label: "Anomalies",
    href: "/anomalies",
  },
] as const;