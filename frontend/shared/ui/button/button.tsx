import clsx from "clsx";
import React, { ButtonHTMLAttributes, memo } from "react";

type ButtonTypesParams = "primary" | "outline" | "cancel" | "clean";
type ButtonTypes = ButtonTypesParams | "base";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  className?: string;
  variant?: ButtonTypesParams;
  loading?: boolean;
}

const ButtonStyles: Record<ButtonTypes, string> = {
  base: "flex items-center justify-center cursor-pointer transition-all duration-300 disabled:cursor-not-allowed",
  primary: "text-white bg-dark hover:bg-dark/90",
  outline:
    "text-dark bg-white border-[1.5px] border-outline shadow-md hover:bg-bg-outline",
  cancel: "text-white bg-ui-red hover:bg-ui-red/90",
  clean: "text-dark",
} as const;

export const Button = memo(function Button({
  className,
  variant = "primary",
  loading = false,
  children,
  type,
  ...props
}: ButtonProps) {
  return (
    <button
      type={type ?? "button"}
      aria-busy={loading ? "true" : undefined}
      aria-disabled={props.disabled || loading ? true : undefined}
      className={clsx(ButtonStyles["base"], ButtonStyles[variant], className)}
      disabled={props.disabled || loading}
      {...props}
    >
      {loading ? (
        <span
          className={clsx(
            "w-4 h-4 border-2 border-t-transparent rounded-full animate-spin",
            variant === "outline" ? "border-dark" : "border-white"
          )}
        />
      ) : (
        children
      )}
    </button>
  );
});
