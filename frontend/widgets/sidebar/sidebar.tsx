"use client";
import clsx from "clsx";
import React, { FC, useState } from "react";
import Image from "next/image";
import { Monomaniac_One } from "next/font/google";
import { Button } from "@/shared/ui/button/button";
import { Bolt, ChevronsLeft, House, ListTodo, Package } from "lucide-react";
import { SidebarButton } from "./sidebar-button";
import { CourseList } from "./course-list";
import { useAnimatedPresence } from "@/shared/hooks";

const monomaniacOne = Monomaniac_One({ weight: "400" });

const courseList = [
  { courseName: "Python", courseIcon: "/logo.svg", courseId: "course-1" },
  { courseName: "Python", courseIcon: "/logo.svg", courseId: "course-2" },
  { courseName: "Python", courseIcon: "/logo.svg", courseId: "course-3" },
];

interface Props {
  className?: string;
}

export const Sidebar: FC<Props> = ({ className }) => {
  const [isOpen, setOpen] = useState(true);

  const handleToggleSidebar = () => {
    setOpen((prev) => !prev);
  };

  const isVisible = useAnimatedPresence(isOpen, 200);

  return (
    <div
      className={clsx(
        "flex flex-col pb-7 h-full text-lg font-light bg-white border-r border-outline shadow-xs transition-all duration-200",
        isOpen ? "w-94" : "w-24",
        className
      )}
    >
      <div
        className={clsx(
          "h-20 px-5 flex items-center justify-between border-b shadow-xs border-outline"
        )}
      >
        <div className={clsx("flex items-center w-full h-full")}>
          <div className="flex-shrink-0">
            <Image
              className="size-12"
              src={"/logo.svg"}
              width={48}
              height={48}
              alt={"Edhub"}
            />
          </div>

          {isVisible && (
            <p
              className={clsx(
                "text-4xl overflow-hidden transition-all duration-200",
                monomaniacOne.className,
                isOpen
                  ? "max-w-[200px] opacity-100 translate-x-2"
                  : "max-w-0 opacity-0 translate-x-4"
              )}
            >
              Edhub
            </p>
          )}
        </div>
      </div>

      <div className="flex-1 px-5 py-8">
        <div className="flex flex-col gap-1">
          <SidebarButton
            className="group text-dark/80"
            icon={<House width={32} strokeWidth={1.7} />}
            text="Home"
            href="#"
            isOpen={isOpen}
          />
          <SidebarButton
            className="group text-dark/80"
            icon={<ListTodo width={32} strokeWidth={1.7} />}
            text="Tasks"
            href="#"
            isOpen={isOpen}
          />
        </div>
        <CourseList
          isOpenSidebar={isOpen}
          className="mt-6"
          courseList={courseList}
        />
      </div>

      <div className={clsx("px-5 relative flex transition-all duration-200")}>
        <div
          className={clsx(
            "flex flex-col gap-1 w-full transition-all duration-200",
            isOpen ? "translate-y-0" : "-translate-y-14"
          )}
        >
          <SidebarButton
            className="group text-dark/80"
            icon={<Package width={32} strokeWidth={1.7} />}
            text="Сourse archive"
            href="#"
            isOpen={isOpen}
          />
          <SidebarButton
            className="group text-dark/80"
            icon={<Bolt width={32} strokeWidth={1.7} />}
            text="Settings"
            href="#"
            isOpen={isOpen}
          />
        </div>
        <div
          className={clsx(
            "absolute w-full bottom-[6px] right-0 size-10 flex items-center px-6 transition-all duration-200 pointer-events-none",
            isOpen ? "justify-end" : "justify-center"
          )}
        >
          <Button
            onClick={handleToggleSidebar}
            className="size-9 rounded-md pointer-events-auto"
            variant="outline"
          >
            <ChevronsLeft
              size={22}
              className={clsx(
                "text-dark/80 mr-[1px] transition-transform duration-200",
                isOpen ? "rotate-0" : "rotate-180"
              )}
            />
          </Button>
        </div>
      </div>
    </div>
  );
};
