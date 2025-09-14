import type { Metadata } from "next";
import { Rubik } from "next/font/google";
import "./globals.css";

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
      <body className={`${rubikSans.className} antialiased`}>{children}</body>
    </html>
  );
}
