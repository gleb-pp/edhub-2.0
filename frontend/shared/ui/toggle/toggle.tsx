import clsx from "clsx";
import { FC } from "react";

interface ToggleGroupProps {
  value: string;
  onClick: (val: string) => void;
  options: { label: string; value: string }[];
  className?: string;
}

export const ToggleGroup: FC<ToggleGroupProps> = ({
  value,
  onClick,
  options,
  className,
}) => {
  return (
    <div
      role="radiogroup"
      className={clsx(
        "inline-flex items-center bg-white shadow-md border border-gray-300",
        className
      )}
    >
      {options.map((opt, i) => (
        <button
          key={opt.value}
          type="button"
          role="radio"
          aria-checked={value === opt.value}
          tabIndex={value === opt.value ? 0 : -1}
          onClick={() => onClick(opt.value)}
          className={clsx(
            "px-3 py-1.5 text-sm transition-colors cursor-pointer",
            value === opt.value ? "text-dark" : "text-dark/30 hover:text-dark",
            i > 0 && "border-l border-gray-300"
          )}
        >
          {opt.label}
        </button>
      ))}
    </div>
  );
};
