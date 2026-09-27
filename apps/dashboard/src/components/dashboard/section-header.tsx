import type { ReactNode } from "react";
import { ArrowUpRight } from "lucide-react";

type SectionHeaderProps = {
  title: string;
  description?: string;
  action?: ReactNode;
};

export function SectionHeader({
  title,
  description,
  action,
}: SectionHeaderProps) {
  return (
    <div className="flex items-start justify-between gap-4">
      <div className="min-w-0">
        <h3 className="font-semibold tracking-tight text-card-foreground">
          {title}
        </h3>

        {description && (
          <p className="mt-1 text-sm leading-relaxed text-muted-foreground">
            {description}
          </p>
        )}
      </div>

      {action}
    </div>
  );
}

type SectionLinkProps = {
  label?: string;
};

export function SectionLink({
  label = "View details",
}: SectionLinkProps) {
  return (
    <button
      type="button"
      className="group inline-flex shrink-0 items-center gap-1.5 text-xs font-medium text-muted-foreground transition-colors hover:text-foreground"
    >
      <span>{label}</span>

      <ArrowUpRight
        className="h-3.5 w-3.5 transition-transform duration-200 group-hover:-translate-y-0.5 group-hover:translate-x-0.5"
        strokeWidth={1.8}
      />
    </button>
  );
}