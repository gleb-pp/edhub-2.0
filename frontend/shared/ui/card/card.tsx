import clsx from "clsx";
import React, { HTMLAttributes } from "react";

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  className?: string;
}

export const Card: React.FC<CardProps> = ({
  className,
  children,
  ...props
}) => {
  return (
    <div
      role="group"
      className={clsx(
        "min-w-10 min-h-10 w-10 h-10 p-2 bg-white border border-outline rounded-xl shadow-md",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};
