import clsx from 'clsx'
import React, { forwardRef, HTMLAttributes, memo } from 'react'

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  className?: string
}

export const Card = memo(
  forwardRef<HTMLDivElement, CardProps>(function Card(
    { className, children, ...props },
    ref,
  ) {
    return (
      <div
        ref={ref}
        role="group"
        className={clsx(
          'bg-white border border-outline rounded-xl shadow-sm',
          className,
        )}
        {...props}
      >
        {children}
      </div>
    )
  }),
)

Card.displayName = 'Card'
