import clsx from "clsx";
import React, { InputHTMLAttributes } from "react";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  className?: string;
}

export const Input: React.FC<InputProps> = ({ className, ...props }) => {
  return (
    <input
      className={clsx(
        `px-4 h-10 w-25 text-sm font-light text-dark bg-white border border-outline rounded-md shadow-sm
        placeholder:text-dark/50 placeholder:font-normal outline-none transition-all duration-300 focus:bg-bg-outline`,
        className
      )}
      {...props}
    />
  );
};
