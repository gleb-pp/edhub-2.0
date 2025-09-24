'use client'
import clsx from 'clsx'
import React, {
  createContext,
  FC,
  ReactNode,
  useContext,
  useLayoutEffect,
  useRef,
  useState,
  useMemo,
  useCallback,
  useId,
} from 'react'
import { Button } from '../button/button'
import { useAnimatedPresence } from '@/shared/hooks/useAnimatedPresence'
import { ChevronDown } from 'lucide-react'
import { useClickOutside } from '@/shared/hooks/useClickOutside'
import './select.css'

interface SelectContextType {
  isOpen: boolean
  toggle: () => void
  select: (value: string) => void
  selected: string | null
  triggerWidth: number
  ids: { trigger: string; list: string }
}

interface SelectComponentType {
  children: ReactNode
  className?: string
}

interface SelectListElementType {
  value: string
}

interface SelectProps extends SelectComponentType {
  value: string | null
  onChange: (value: string | null) => void
}

interface SelectType {
  Trigger: typeof Trigger
  List: typeof List
  ListElement: typeof ListElement
}

const SelectContext = createContext<SelectContextType | null>(null)

export const Select: FC<SelectProps> & SelectType = ({
  className,
  children,
  value,
  onChange,
}) => {
  const [isOpen, setOpen] = useState(false)
  const [triggerWidth, setTriggerWidth] = useState<number>(0)
  const selectRef = useRef<HTMLDivElement>(null)

  const baseId = useId()
  const ids = useMemo(
    () => ({
      trigger: `select-trigger-${baseId}`,
      list: `select-list-${baseId}`,
    }),
    [baseId],
  )

  const toggleOff = useCallback(() => setOpen(false), [])
  const toggle = useCallback(() => setOpen((prev) => !prev), [])
  const select = useCallback(
    (val: string) => {
      const newValue = value === val ? null : val
      onChange(newValue)
      setOpen(false)
    },
    [value, onChange],
  )

  useClickOutside(selectRef, toggleOff)

  useLayoutEffect(() => {
    if (selectRef.current) {
      setTriggerWidth(selectRef.current.offsetWidth)
    }
  }, [isOpen])

  const contextValue = useMemo(
    () => ({ isOpen, toggle, select, selected: value, triggerWidth, ids }),
    [isOpen, toggle, select, value, triggerWidth, ids],
  )

  return (
    <SelectContext.Provider value={contextValue}>
      <div ref={selectRef} className={clsx('relative w-fit', className)}>
        {children}
      </div>
    </SelectContext.Provider>
  )
}

const Trigger: FC<SelectComponentType> = ({ className, children }) => {
  const ctx = useContext(SelectContext)
  if (!ctx) throw new Error('Select.Trigger must be used within <Select>')

  const { toggle, selected, isOpen, ids } = ctx

  return (
    <Button
      variant="outline"
      className={clsx('!justify-between text-dark/70 rounded-lg', className)}
      onClick={toggle}
      id={ids.trigger}
      aria-haspopup="listbox"
      aria-expanded={isOpen}
      aria-controls={ids.list}
    >
      {selected ?? children ?? 'Select...'}{' '}
      <ChevronDown
        className={clsx(
          'w-[1em] h-[1em] shrink-0 transition-transform transform-gpu duration-200',
          isOpen ? 'rotate-180' : 'rotate-0',
        )}
      />
    </Button>
  )
}

const List: FC<SelectComponentType> = ({ className, children }) => {
  const ctx = useContext(SelectContext)
  if (!ctx) throw new Error('Select.List must be used within <Select>')

  const { isOpen, triggerWidth, ids } = ctx
  const isVisible = useAnimatedPresence(isOpen, 200) // select.css -> animattion: * 200ms *

  if (!isVisible) return null

  return (
    <ul
      id={ids.list}
      role="listbox"
      aria-labelledby={ids.trigger}
      className={clsx(
        'absolute flex flex-col w-fit h-fit bg-white border border-outline rounded-xl shadow-md',
        isOpen ? 'fade-translate-in' : 'fade-translate-out',
        className,
      )}
      style={{ minWidth: triggerWidth }}
    >
      {children}
    </ul>
  )
}

const ListElement: FC<SelectComponentType & SelectListElementType> = ({
  className,
  children,
  value,
}) => {
  const ctx = useContext(SelectContext)
  if (!ctx) throw new Error('Select.ListElement must be used within <Select>')

  const { select, selected } = ctx

  return (
    <li
      role="option"
      aria-selected={selected === value}
      onClick={() => select(value)}
      className={clsx(
        'rounded-md transition-all duration-300 hover:bg-bg-outline/80 cursor-pointer',
        selected === value ? 'bg-bg-outline' : 'bg-white',
        className,
      )}
    >
      {children}
    </li>
  )
}

Select.Trigger = Trigger
Select.List = List
Select.ListElement = ListElement
