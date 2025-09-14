"use client";
import React, { useState, useEffect, FC, ReactNode } from "react";
import clsx from "clsx";
import { Card } from "../card/card";
import "./modal.css";

interface ModalProps {
  isOpen: boolean;
  className?: string;
  onClose: () => void;
  children: React.ReactNode;
}

interface ModalElementProps {
  className?: string;
  children: React.ReactNode;
}

interface ModalType extends FC<ModalProps> {
  Header: FC<ModalElementProps>;
  Body: FC<ModalElementProps>;
  Footer: FC<ModalElementProps>;
}

const ModalComponent: FC<ModalProps> = ({
  isOpen,
  onClose,
  children,
  className,
}) => {
  const [isVisible, setIsVisible] = useState(isOpen);

  useEffect(() => {
    if (isOpen) {
      setIsVisible(true);
    } else {
      setTimeout(() => setIsVisible(false), 200); // fade-in, fade-out animation time 0.2s -> modal.css
    }
  }, [isOpen]);

  if (!isVisible) return null;

  return (
    <div
      className={clsx(
        "fixed inset-0 flex items-center justify-center bg-black/50 z-50",
        isOpen ? "fade-in" : "fade-out"
      )}
      onClick={onClose}
    >
      <Card
        className={clsx(
          "flex flex-col",
          isOpen ? "scale-in" : "scale-out",
          className
        )}
        onClick={(e) => e.stopPropagation()}
      >
        {children}
      </Card>
    </div>
  );
};

const Modal = ModalComponent as ModalType;

Modal.Header = ({ className, children }) => (
  <div className={className}>{children}</div>
);

Modal.Body = ({ className, children }) => (
  <div className={clsx("flex-1 overflow-auto", className)}>{children}</div>
);

Modal.Footer = ({ className, children }) => (
  <div className={clsx("gap-2", className)}>{children}</div>
);

export { Modal };
