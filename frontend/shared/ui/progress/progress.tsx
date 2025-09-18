"use client";
import clsx from "clsx";
import React, { FC, memo, useMemo } from "react";

interface ProgressBarProps {
  value: number;
  maxValue: number;
  className?: string;
  ariaLabel?: string;
  ariaLabelledBy?: string;
}

export const ProgressBar: FC<ProgressBarProps> = memo(function ProgressBar({
  value,
  maxValue,
  className,
  ariaLabel,
  ariaLabelledBy,
}) {
  const progressPercent = Math.min(
    Math.max((maxValue === 0 ? 0 : value / maxValue) * 100, 0),
    100
  );

  const colorClass = useMemo(() => {
    if (progressPercent >= 70) return "bg-ui-green";
    if (progressPercent >= 40) return "bg-ui-yellow";
    return "bg-ui-red";
  }, [progressPercent]);

  return (
    <div
      role="progressbar"
      aria-valuenow={Math.round(value)}
      aria-valuemin={0}
      aria-valuemax={Math.round(maxValue)}
      aria-valuetext={`${Math.round(progressPercent)}%`}
      aria-label={ariaLabel}
      aria-labelledby={ariaLabelledBy}
      className={clsx("relative overflow-hidden", className)}
    >
      <div className="absolute w-full h-full bg-zinc-200" />
      <div
        style={{ transform: `translateX(-${100 - progressPercent}%)` }}
        className={clsx(
          "absolute top-0 left-0 w-full h-full transition-transform",
          colorClass
        )}
      />
    </div>
  );
});
