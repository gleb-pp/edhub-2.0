"use client";
import React, { useEffect, FC, useRef } from "react";
import clsx from "clsx";
import { Card } from "../card/card";
import "./modal.css";
import { useAnimatedPresence } from "@/shared/hooks/useAnimatedPresence";

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
  const modalRef = useRef<HTMLDivElement>(null);

  const isVisible = useAnimatedPresence(isOpen, 200); // modal.css -> animation: * 200ms *;

  useEffect(() => {
    if (isOpen && modalRef.current) {
      modalRef.current.focus();
    }
  }, [isOpen]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Tab" && modalRef.current) {
      const focusable = modalRef.current.querySelectorAll<
        | HTMLButtonElement
        | HTMLInputElement
        | HTMLTextAreaElement
        | HTMLAnchorElement
      >(
        'a[href], button:not([disabled]), textarea, input:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])'
      );
      const first = focusable[0];
      const last = focusable[focusable.length - 1];

      if (!first || !last) return;

      if (e.shiftKey && document.activeElement === first) {
        e.preventDefault();
        last.focus();
      } else if (!e.shiftKey && document.activeElement === last) {
        e.preventDefault();
        first.focus();
      }
    }
  };

  if (!isVisible) return null;

  return (
    <div
      ref={modalRef}
      className={clsx(
        "fixed inset-0 flex items-center justify-center bg-black/50 z-50",
        isOpen ? "fade-in" : "fade-out"
      )}
      onClick={onClose}
    >
      <Card
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        aria-describedby="modal-body"
        tabIndex={-1}
        onKeyDown={handleKeyDown}
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
  <div id="modal-title" className={className}>
    {children}
  </div>
);
Modal.Header.displayName = "Modal.Header";

Modal.Body = ({ className, children }) => (
  <div id="modal-body" className={clsx("flex-1 overflow-auto", className)}>
    {children}
  </div>
);
Modal.Body.displayName = "Modal.Body";

Modal.Footer = ({ className, children }) => (
  <div className={clsx("gap-2", className)}>{children}</div>
);
Modal.Footer.displayName = "Modal.Footer";

export { Modal };
