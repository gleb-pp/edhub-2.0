import { Sidebar } from "@/widgets/sidebar/ui/sidebar";
import { Header } from "@/widgets/header/header";

export default function AuthRootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="h-screen w-screen flex items-center justify-center bg-zinc-50">
      {children}
    </div>
  );
}
