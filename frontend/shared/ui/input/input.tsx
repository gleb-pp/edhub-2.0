import clsx from "clsx";
import React, { InputHTMLAttributes, memo } from "react";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  className?: string;
}

export const Input = memo(function Input({ className, ...props }: InputProps) {
  return (
    <input
      className={clsx(
        `h-full w-full font-light text-dark bg-white border border-outline rounded-md shadow-sm
        placeholder:text-dark/50 placeholder:font-normal outline-none transition-all duration-300 focus:bg-bg-outline`,
        className
      )}
      {...props}
    />
  );
});
