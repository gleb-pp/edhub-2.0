import type { Metadata } from "next";
import { Rubik } from "next/font/google";
import "./globals.css";
import { Sidebar } from "@/widgets/sidebar/sidebar";
import { Header } from "@/widgets/header/header";

const rubikSans = Rubik({
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Edhub",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${rubikSans.className} h-screen w-screen antialiased bg-zinc-100 flex items-center justify-center`}
      >
        <Sidebar />
        <div className="h-full w-full">
          <Header />
          {children}
        </div>
      </body>
    </html>
  );
}
