import { Sidebar } from '@/widgets/sidebar/ui/sidebar'
import { Header } from '@/widgets/header/header'

export default function AuthRootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <div
      className={`h-screen w-screen antialiased bg-zinc-50 flex items-center justify-center`}
    >
      <Sidebar />
      <div className="h-full w-full flex flex-col">
        <Header />
        <div className="flex-1 min-h-0 overflow-hidden">{children}</div>
      </div>
    </div>
  )
}
