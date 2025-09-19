import clsx from "clsx";
import React from "react";

interface Props {
  className?: string;
}

export const Header: React.FC<Props> = ({ className }) => {
  return (
    <div
      className={clsx(
        "w-full h-20 bg-white border-b border-outline shadow-xs",
        className
      )}
    ></div>
  );
};
