"use client"

import { useState } from "react"
import Link from "next/link"
import { usePathname, useRouter } from "next/navigation"
import { User, Grid3X3, Trophy, LogOut, Menu, X } from "lucide-react"
import Image from "next/image"

interface DashboardLayoutProps {
  children: React.ReactNode
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  const pathname = usePathname()
  const router = useRouter()
  const [collapsed, setCollapsed] = useState(false)

  const navigation = [
    { 
      name: "Editar Perfil", 
      href: "/dashboard/perfil", 
      icon: User,
      active: pathname === "/dashboard/perfil"
    },
    { 
      name: "Ver Malla", 
      href: "/dashboard/malla", 
      icon: Grid3X3,
      active: pathname === "/dashboard/malla"
    },
    { 
      name: "Ver Logros", 
      href: "/dashboard/logros", 
      icon: Trophy,
      active: pathname === "/dashboard/logros"
    },
  ]

  const handleLogout = () => {
    router.push("/")
  }

  return (
    <div className="relative flex min-h-screen">
      {/* Background Image */}
      <div 
        className="fixed inset-0 bg-cover bg-center bg-no-repeat"
        style={{ backgroundImage: "url('/images/fondo-dashboard.png')" }}
      />
      
      {/* Sidebar */}
      <aside className={`fixed left-0 top-0 z-40 flex h-screen flex-col shadow-lg transition-all duration-300 ${collapsed ? 'w-20' : 'w-64'}`}>
        {/* White background area */}
        <div className="absolute inset-0 bg-white/95 backdrop-blur-sm" />
        
        {/* UTB Logo Image (positioned at bottom, responsive to sidebar state) */}
        <div className="pointer-events-none absolute bottom-16 left-0 z-0 w-full overflow-hidden px-2">
          <Image 
            src="/images/utb-logo.svg"
            alt="UTB Logo"
            width={200}
            height={200}
            className={`opacity-90 transition-all duration-300 ${collapsed ? 'h-16 w-16' : 'h-48 w-48'}`}
          />
        </div>
        
        {/* Sidebar Content (above the logo) */}
        <div className="relative z-10 flex h-full flex-col">
          {/* Toggle Button */}
          <div className="flex items-center justify-end p-4">
            <button
              onClick={() => setCollapsed(!collapsed)}
              className="flex h-10 w-10 items-center justify-center rounded-lg bg-white/80 text-[#1a1a2e]/60 shadow-sm transition-colors hover:bg-white hover:text-[#1a1a2e]"
            >
              {collapsed ? <Menu className="h-5 w-5" /> : <X className="h-5 w-5" />}
            </button>
          </div>
          
          {/* User Info */}
          <div className={`p-6 pt-2 ${collapsed ? 'px-4 text-center' : ''}`}>
            <h2 className={`font-bold text-[#1a1a2e] ${collapsed ? 'text-xs' : 'text-xl'}`}>
              JUSERPA
            </h2>
            {!collapsed && (
              <p className="text-xs text-[#1a1a2e]/50">ID T000XXXXX</p>
            )}
          </div>
          
          {/* Navigation */}
          <nav className="flex-1 space-y-2 px-3">
            {navigation.map((item) => {
              const Icon = item.icon
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`group flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-medium transition-all ${
                    item.active 
                      ? 'bg-[#1BB9EB] text-white shadow-md' 
                      : 'bg-white/80 text-[#1a1a2e] shadow-sm hover:bg-[#1BB9EB]/10 hover:text-[#1BB9EB]'
                  }`}
                >
                  <Icon className={`h-5 w-5 flex-shrink-0 ${item.active ? 'text-white' : 'text-[#1a1a2e]/70 group-hover:text-[#1BB9EB]'}`} />
                  {!collapsed && <span className="uppercase tracking-wide">{item.name}</span>}
                </Link>
              )
            })}
          </nav>
          
          {/* Logout Button */}
          <div className="p-4">
            <button
              onClick={handleLogout}
              className={`flex w-full items-center gap-3 rounded-lg bg-white/80 px-4 py-3 text-sm font-medium text-[#1a1a2e]/70 shadow-sm transition-all hover:bg-red-50 hover:text-red-600 ${collapsed ? 'justify-center' : ''}`}
            >
              <LogOut className="h-5 w-5 flex-shrink-0" />
              {!collapsed && <span className="uppercase tracking-wide">Cerrar Sesión</span>}
            </button>
          </div>
        </div>
      </aside>
      
      {/* Main Content */}
      <main className={`relative z-10 flex-1 transition-all duration-300 ${collapsed ? 'ml-20' : 'ml-64'}`}>
        {/* Header */}
        <header className="flex items-center justify-end px-8 py-4">
          <div className="flex items-center gap-2 text-xs font-medium tracking-widest text-[#1a1a2e]/60">
            <span>STUDENT</span>
            <span className="text-[#1a1a2e]/30">//</span>
            <span>PROGRESS</span>
            <span className="text-[#1a1a2e]/30">//</span>
            <span>SYSTEM</span>
            <span className="ml-2 h-3 w-3 rounded-sm bg-[#C2F542]" />
          </div>
        </header>
        
        {/* Page Content */}
        <div className="px-8 pb-8">
          {children}
        </div>
      </main>
    </div>
  )
}
