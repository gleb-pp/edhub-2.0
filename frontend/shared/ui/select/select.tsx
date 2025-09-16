"use client";
import clsx from "clsx";
import {
  createContext,
  FC,
  ReactNode,
  useContext,
  useEffect,
  useRef,
  useState,
} from "react";
import { Button } from "../button/button";
import { useAnimatedPresence } from "@/shared/hooks/useAnimatedPresence";
import { ChevronDown } from "lucide-react";
import "./select.css";
import { useClickOutside } from "@/shared/hooks/useClickOutside";

interface SelectContextType {
  isOpen: boolean;
  toggle: () => void;
  select: (value: string) => void;
  selected: string | null;
  triggerWidth: number;
}

interface SelectComponentType {
  children: ReactNode;
  className?: string;
}

interface SelectListElementType {
  value: string;
}

interface SelectProps extends SelectComponentType {
  value?: string | null;
  onChange?: (value: string | null) => void;
  defaultValue?: string | null;
}

interface SelectType {
  Trigger: typeof Trigger;
  List: typeof List;
  ListElement: typeof ListElement;
}

const SelectContext = createContext<SelectContextType>({
  isOpen: false,
  toggle: () => {},
  select: () => {},
  selected: null,
  triggerWidth: 0,
});

export const Select: FC<SelectProps> & SelectType = ({
  className,
  children,
  value,
  onChange,
  defaultValue = null,
}) => {
  const [isOpen, setOpen] = useState(false);
  const [internalSelected, setInternalSelected] = useState<string | null>(
    defaultValue
  );
  const [triggerWidth, setTriggerWidth] = useState<number>(0);

  const selectRef = useRef<HTMLDivElement>(null);

  const toggleOff = () => setOpen(false);
  const toggle = () => setOpen((prev) => !prev);

  const selected = value !== undefined ? value : internalSelected;

  const select = (val: string) => {
    const newValue = selected === val ? null : val;

    if (value !== undefined) {
      onChange?.(newValue);
    } else {
      setInternalSelected(newValue);
      onChange?.(newValue);
    }

    setOpen(false);
  };

  useClickOutside(selectRef, toggleOff);

  useEffect(() => {
    if (selectRef.current) {
      setTriggerWidth(selectRef.current.offsetWidth);
    }
  }, [isOpen]);

  return (
    <SelectContext.Provider
      value={{ isOpen, toggle, select, selected, triggerWidth }}
    >
      <div
        ref={selectRef}
        className={clsx("relative w-fit", className)}
        role="combobox"
        aria-expanded={isOpen}
        aria-haspopup="listbox"
        aria-owns="select-list"
        aria-controls="select-list"
      >
        {children}
      </div>
    </SelectContext.Provider>
  );
};

const Trigger: FC<SelectComponentType> = ({ className, children }) => {
  const { toggle, selected, isOpen } = useContext(SelectContext);
  return (
    <Button
      variant="outline"
      className={clsx("!justify-between text-dark/70 rounded-lg", className)}
      onClick={toggle}
      id="select-trigger"
      aria-haspopup="listbox"
      aria-expanded={isOpen}
      aria-controls="select-list"
    >
      {selected ?? children ?? "Select..."}{" "}
      <ChevronDown
        className={clsx(
          "w-[1em] h-[1em] shrink-0 transition-transform transform-gpu duration-200",
          isOpen ? "rotate-180" : "rotate-0"
        )}
      />
    </Button>
  );
};

const List: FC<SelectComponentType> = ({ className, children }) => {
  const { isOpen, triggerWidth } = useContext(SelectContext);

  const isVisible = useAnimatedPresence(isOpen, 200); // select.css -> animate: * 200ms *

  if (!isVisible) return;

  return (
    <ul
      id="select-list"
      role="listbox"
      aria-labelledby="select-trigger"
      className={clsx(
        "absolute flex flex-col w-fit h-fit bg-white border border-outline rounded-xl shadow-md",
        isOpen ? "fade-translate-in" : "fade-translate-out",
        className
      )}
      style={{ minWidth: triggerWidth }}
    >
      {children}
    </ul>
  );
};

const ListElement: FC<SelectComponentType & SelectListElementType> = ({
  className,
  children,
  value,
}) => {
  const { select, selected } = useContext(SelectContext);

  function handleSelectValue() {
    select(value);
  }

  return (
    <li
      role="option"
      aria-selected={selected === value}
      onClick={handleSelectValue}
      className={clsx(
        "rounded-md transition-all duration-300 hover:bg-bg-outline/80 cursor-pointer",
        selected === value ? "bg-bg-outline" : "bg-white",
        className
      )}
    >
      {children}
    </li>
  );
};

Select.Trigger = Trigger;
Select.List = List;
Select.ListElement = ListElement;
