import clsx from "clsx";
import React, { ButtonHTMLAttributes } from "react";

type ButtonTypesParams = "primary" | "outline" | "cancel";
type ButtonTypes = ButtonTypesParams | "base";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  className?: string;
  variant?: ButtonTypesParams;
  loading?: boolean;
}

const ButtonStyles: Record<ButtonTypes, string> = {
  base: "flex items-center justify-center min-w-10 min-h-10 text-sm font-light rounded-md cursor-pointer transition-all duration-300 disabled:cursor-not-allowed",
  primary: "text-white bg-dark hover:bg-dark/90",
  outline: "text-dark bg-white border-2 border-outline hover:bg-bg-outline",
  cancel: "text-white bg-ui-red hover:bg-ui-red/90",
} as const;

export const Button: React.FC<ButtonProps> = ({
  className,
  variant = "primary",
  loading = false,
  children,
  ...props
}) => {
  return (
    <button
      aria-busy={loading ? "true" : undefined}
      className={clsx(ButtonStyles["base"], ButtonStyles[variant], className)}
      {...props}
      disabled={props.disabled || loading}
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
};
