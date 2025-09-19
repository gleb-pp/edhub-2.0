import { useAnimatedPresence } from "@/shared/hooks";
import clsx from "clsx";
import Link from "next/link";
import React, { ReactNode } from "react";

interface Props {
  className?: string;
  href: string;
  icon: ReactNode;
  text: string;
  isListElement?: boolean;
  isOpen?: boolean;
}

export const SidebarButton: React.FC<Props> = ({
  className,
  href,
  icon,
  text,
  isOpen = false,
}) => {
  const isVisible = useAnimatedPresence(isOpen, 200);
  return (
    <Link
      className={clsx(
        "flex items-center px-[6px] w-full py-1 text-xl font-light rounded-md transition-all duration-200 hover:bg-bg-outline group text-dark/80",
        className
      )}
      href={href}
    >
      <div
        className={clsx(
          "shrink-0 w-10 h-10 flex items-center justify-center transition-colors duration-200 group-hover:text-dark"
        )}
      >
        {icon}
      </div>

      {isVisible && (
        <p
          className={clsx(
            "ml-2 whitespace-nowrap transition-all duration-200 group-hover:text-dark",
            isOpen ? "opacity-100" : "opacity-0"
          )}
        >
          {text}
        </p>
      )}
    </Link>
  );
};
