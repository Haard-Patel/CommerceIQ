"use client";

import { Moon, Sun } from "lucide-react";

export function ThemeToggle() {
  function toggleTheme() {
    const root = document.documentElement;
    const currentTheme = root.getAttribute("data-theme");
    const nextTheme = currentTheme === "dark" ? "light" : "dark";

    root.setAttribute("data-theme", nextTheme);
    localStorage.setItem("commerceiq-theme", nextTheme);
  }

  return (
    <button
      type="button"
      onClick={toggleTheme}
      aria-label="Toggle theme"
      title="Toggle theme"
      className="group relative flex h-9 w-9 items-center justify-center rounded-lg border border-border bg-background text-muted-foreground transition-all duration-200 hover:bg-muted hover:text-foreground"
    >
      <Sun className="h-4 w-4 transition-all duration-200 dark:hidden" />

      <Moon className="absolute h-4 w-4 transition-all duration-200 hidden dark:block" />
    </button>
  );
}
