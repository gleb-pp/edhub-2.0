import { useRef, useLayoutEffect, useState, FC } from "react";
import clsx from "clsx";

interface SwitchProps {
  checked: boolean;
  onClick: (value: boolean) => void;
  disabled?: boolean;
  className?: string;
}

export const Switch: FC<SwitchProps> = ({
  checked,
  onClick,
  disabled,
  className,
}) => {
  const btnRef = useRef<HTMLButtonElement>(null);
  const thumbRef = useRef<HTMLDivElement>(null);
  const [offset, setOffset] = useState(0);

  useLayoutEffect(() => {
    const btn = btnRef.current;
    const thumb = thumbRef.current;
    if (btn && thumb) {
      const computed = window.getComputedStyle(btn);
      const paddings =
        parseFloat(computed.paddingRight) + parseFloat(computed.paddingLeft);

      const available = btn.clientWidth - thumb.offsetWidth - paddings;
      setOffset(available);
    }
  }, [btnRef, thumbRef]);

  return (
    <button
      ref={btnRef}
      type="button"
      role="switch"
      aria-checked={checked}
      onClick={() => !disabled && onClick(!checked)}
      disabled={disabled}
      className={clsx(
        "relative flex items-center transition-colors duration-200 origin-left",
        checked ? "bg-dark" : "bg-[#D9D9D9]",
        className
      )}
    >
      <div
        ref={thumbRef}
        style={{ transform: `translateX(${checked ? offset : 0}px)` }}
        className="h-full aspect-square bg-white rounded-full shadow-sm transition-transform transform-cpu"
      />
    </button>
  );
};
