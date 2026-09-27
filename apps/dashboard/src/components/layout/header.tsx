import { CIQLogo } from "@/components/brand/ciq-logo";
import { ThemeToggle } from "@/components/ui/theme-toggle";

type HeaderProps = {
  title?: string;
};

export function Header({ title = "Overview" }: HeaderProps) {
  return (
    <header className="flex h-16 items-center justify-between border-b border-border bg-background/95 px-4 backdrop-blur sm:px-6 lg:px-8">
      {/* Page title */}
      <div className="min-w-0">
        <h1 className="truncate text-lg font-semibold tracking-tight text-foreground">
          {title}
        </h1>
      </div>

      {/* Header actions */}
      <div className="flex items-center gap-3">
        {/* CIQ brand */}
        <div className="hidden items-center sm:flex">
          <CIQLogo size="md" />
        </div>

        {/* Divider */}
        <div className="hidden h-6 w-px bg-border sm:block" />

        {/* Theme toggle */}
        <ThemeToggle />

        {/* Profile */}
        <div
          aria-label="User profile"
          className="flex h-9 w-9 items-center justify-center rounded-full border border-border bg-muted text-xs font-semibold tracking-wide text-foreground"
        >
          HP
        </div>
      </div>
    </header>
  );
}
