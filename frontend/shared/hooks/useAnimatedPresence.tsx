"use client";
import { useEffect, useState } from "react";

export const useAnimatedPresence = (isOpen: boolean, animationTime: number) => {
  const [isVisible, setVisible] = useState(isOpen);

  useEffect(() => {
    if (isOpen) {
      setVisible(true);
    } else {
      const timer = setTimeout(() => {
        setVisible(false);
      }, animationTime);
      return () => clearTimeout(timer);
    }
  }, [isOpen, animationTime]);

  return isVisible;
};
