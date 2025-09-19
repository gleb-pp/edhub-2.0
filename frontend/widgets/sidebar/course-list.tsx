"use client";
import { Button } from "@/shared/ui/button/button";
import Image from "next/image";
import clsx from "clsx";
import { ChevronDown } from "lucide-react";
import React, { useState } from "react";
import { SidebarButton } from "./sidebar-button";
import { useAnimatedPresence } from "@/shared/hooks";
import "./sidebar.css";

interface CourseItem {
  courseName: string;
  courseIcon: string;
  courseId: string;
}

interface Props {
  className?: string;
  courseList: CourseItem[];
  isOpenSidebar?: boolean;
}

export const CourseList: React.FC<Props> = ({
  className,
  courseList,
  isOpenSidebar = false,
}) => {
  const [isOpen, setOpen] = useState(false);

  const handleToggleList = () => {
    setOpen((prev) => !prev);
  };

  const isVisibleList = useAnimatedPresence(isOpen, 200);

  return (
    <div className={clsx("text-dark", className)}>
      <Button
        onClick={handleToggleList}
        variant="clean"
        className="flex items-center w-full mb-3 transition-all duration-200"
      >
        <p
          className={clsx(
            "transition-all overflow-hidden duration-200",
            isOpen ? "text-dark" : "font-light text-dark/80",
            isOpenSidebar
              ? "opacity-100 translate-x-0 max-w-[260px]"
              : "opacity-0 -translate-x-6 max-w-0"
          )}
        >
          Courses
        </p>

        <ChevronDown
          className={clsx(
            "ml-auto transition-transform duration-200",
            isOpen ? "rotate-180" : "rotate-0",
            isOpenSidebar ? "translate-x-0" : "-translate-x-[14px]"
          )}
          strokeWidth={1.6}
        />
      </Button>

      {isVisibleList && (
        <ul
          className={
            (clsx("mt-[10px] ml-[6px]"),
            isOpen ? "fade-translate-in" : "fade-translate-out")
          }
        >
          {courseList.map((course) => (
            <li key={course.courseId}>
              <SidebarButton
                className="w-full"
                href={"#"}
                icon={
                  <Image
                    src={course.courseIcon}
                    height={28}
                    width={28}
                    alt={"Edhub"}
                  />
                }
                text={course.courseName}
                isOpen={isOpenSidebar}
              />
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};
