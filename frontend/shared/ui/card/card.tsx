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
        "bg-white border border-outline rounded-xl shadow-md",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};
