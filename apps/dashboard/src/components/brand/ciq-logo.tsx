
type CIQLogoProps = {
  size?: "sm" | "md" | "lg";
};

export function CIQLogo({ size = "md" }: CIQLogoProps) {
  const sizes = {
    sm: "text-[17px]",
    md: "text-[20px]",
    lg: "text-[28px]",
  };

  return (
    <div
      aria-label="CommerceIQ"
      className={`select-none font-sans font-extrabold tracking-[-0.075em] text-foreground ${sizes[size]}`}
    >
      <span>C</span>
      <span className="relative mx-[1px] font-black">
        I
      </span>
      <span className="relative">
        Q
        <span
          aria-hidden="true"
          className="absolute bottom-[18%] right-[3%] h-[24%] w-[18%] rounded-full bg-background"
        />
      </span>
    </div>
  );
}
