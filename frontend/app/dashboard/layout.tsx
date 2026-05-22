"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import {
  User,
  Grid3X3,
  Trophy,
  LogOut,
  Menu,
  X,
  Map,
  ChevronRight,
  Activity,
} from "lucide-react";
import Image from "next/image";
import { useCurrentUser } from "@/hooks/useCurrentUser";

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export default function DashboardLayout({ children }: DashboardLayoutProps) {
  const pathname = usePathname();
  const router = useRouter();
  const [collapsed, setCollapsed] = useState(false);
  const { user, displayName, loading } = useCurrentUser();

  const navigation = [
    { name: "Perfil", href: "/dashboard/perfil", icon: User, id: "perfil" },
    {
      name: "Ruta Académica",
      href: "/dashboard/malla",
      icon: Grid3X3,
      id: "malla",
    },
    { name: "Quests", href: "/dashboard/quests", icon: Map, id: "quests" },
  ];

  const handleLogout = () => {
    localStorage.removeItem("sps_token");
    router.push("/");
  };

  return (
    <div
      className="relative flex min-h-screen"
      style={{ backgroundColor: "var(--surface-0)" }}
    >
      {/* ─── Background fondo ──────────────────────────────── */}
      <div
        className="fixed inset-0 bg-cover bg-center bg-no-repeat opacity-30"
        style={{ backgroundImage: "url('/images/fondo-dashboard.png')" }}
      />

      {/* ─── Sidebar HUD ───────────────────────────────────── */}
      <aside
        className={`hud-sidebar fixed left-0 top-0 z-40 flex h-screen flex-col transition-all duration-300 ${collapsed ? "w-16" : "w-60"}`}
      >
        {/* Top strip accent */}
        <div
          className="absolute top-0 left-0 right-0 h-[2px]"
          style={{
            background:
              "linear-gradient(90deg, var(--utb-cyan), var(--utb-emerald))",
          }}
        />

        {/* Sidebar content */}
        <div className="relative z-10 flex h-full flex-col">
          {/* Logo + toggle */}
          <div
            className={`flex items-center border-b p-3 ${collapsed ? "justify-center" : "justify-between"}`}
            style={{ borderColor: "var(--surface-3)" }}
          >
            {!collapsed && (
              <div className="flex items-center gap-2">
                <div
                  className="w-1 h-6 flex-shrink-0"
                  style={{
                    background:
                      "linear-gradient(180deg, var(--utb-cyan), var(--utb-emerald))",
                  }}
                />
                <div>
                  <p
                    className="hud-label"
                    style={{ color: "var(--utb-cyan)", fontSize: "9px" }}
                  >
                    UTB // SPS
                  </p>
                  <p
                    className="font-display font-bold text-xs uppercase tracking-widest"
                    style={{ color: "var(--text-primary)", fontSize: "11px" }}
                  >
                    Student Progress
                  </p>
                </div>
              </div>
            )}
            <button
              onClick={() => setCollapsed(!collapsed)}
              className="flex h-7 w-7 items-center justify-center transition-colors"
              style={{
                color: "var(--text-muted)",
                border: "1px solid var(--surface-3)",
                clipPath: "var(--clip-corner-sm)",
              }}
            >
              {collapsed ? (
                <Menu className="h-3.5 w-3.5" />
              ) : (
                <X className="h-3.5 w-3.5" />
              )}
            </button>
          </div>

          {/* User info */}
          <div
            className={`border-b p-3 ${collapsed ? "flex justify-center" : ""}`}
            style={{ borderColor: "var(--surface-3)" }}
          >
            {loading ? (
              <div className="space-y-1.5">
                <div className="hud-skeleton h-3 w-24" />
                {!collapsed && <div className="hud-skeleton h-2 w-16" />}
              </div>
            ) : collapsed ? (
              <div className="hex-avatar h-8 w-8 text-xs font-black">
                {(displayName ?? "?").charAt(0)}
              </div>
            ) : (
              <div className="flex items-center gap-2.5">
                <div className="hex-avatar h-9 w-9 text-sm font-black shrink-0">
                  {(displayName ?? "?").charAt(0)}
                </div>
                <div className="min-w-0">
                  <p
                    className="font-display font-bold text-xs uppercase truncate"
                    style={{
                      color: "var(--text-primary)",
                      letterSpacing: "0.05em",
                    }}
                  >
                    {displayName ?? "—"}
                  </p>
                  <p className="hud-label truncate" style={{ fontSize: "9px" }}>
                    ID · {user?.codigo ?? "—"}
                  </p>
                </div>
              </div>
            )}
          </div>

          {/* Navigation */}
          <nav className="flex-1 space-y-1 p-2 overflow-y-auto">
            {!collapsed && (
              <div className="hud-divider mb-2 px-1">
                <span className="hud-divider-label" style={{ fontSize: "9px" }}>
                  Navigation
                </span>
                <div className="hud-divider-line" />
              </div>
            )}
            {navigation.map((item) => {
              const Icon = item.icon;
              const isActive =
                pathname === item.href ||
                (item.href !== "/dashboard" && pathname.startsWith(item.href));
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`nav-item ${isActive ? "active" : ""} ${collapsed ? "justify-center px-2" : ""}`}
                >
                  <Icon className="h-4 w-4 flex-shrink-0" />
                  {!collapsed && <span>{item.name}</span>}
                  {!collapsed && isActive && (
                    <ChevronRight className="h-3 w-3 ml-auto opacity-60" />
                  )}
                </Link>
              );
            })}
          </nav>

          {/* UTB logo watermark */}
          {!collapsed && (
            <div className="p-3 opacity-20 pointer-events-none">
              <Image
                src="/images/utb-logo.svg"
                alt="UTB"
                width={80}
                height={40}
                className="w-16"
              />
            </div>
          )}

          {/* Logout */}
          <div
            className="p-2 border-t"
            style={{ borderColor: "var(--surface-3)" }}
          >
            <button
              onClick={handleLogout}
              className={`nav-item w-full ${collapsed ? "justify-center px-2" : ""}`}
              style={{ color: "var(--text-muted)" }}
              onMouseEnter={(e) => {
                (e.currentTarget as HTMLElement).style.color = "#DC2626";
                (e.currentTarget as HTMLElement).style.borderColor =
                  "rgba(220,38,38,0.25)";
                (e.currentTarget as HTMLElement).style.background =
                  "rgba(220,38,38,0.05)";
              }}
              onMouseLeave={(e) => {
                (e.currentTarget as HTMLElement).style.color =
                  "var(--text-muted)";
                (e.currentTarget as HTMLElement).style.borderColor =
                  "transparent";
                (e.currentTarget as HTMLElement).style.background =
                  "transparent";
              }}
            >
              <LogOut className="h-4 w-4 flex-shrink-0" />
              {!collapsed && <span>Cerrar Sesión</span>}
            </button>
          </div>
        </div>
      </aside>

      {/* ─── Main content area ─────────────────────────────── */}
      <main
        className={`relative z-10 flex-1 transition-all duration-300 ${collapsed ? "ml-16" : "ml-60"}`}
      >
        {/* Top bar */}
        <header
          className="sticky top-0 z-30 flex items-center justify-between px-6 py-3"
          style={{
            background: "rgba(245,247,250,0.92)",
            backdropFilter: "blur(12px)",
            borderBottom: "1px solid var(--surface-3)",
          }}
        >
          {/* Breadcrumb */}
          <div className="flex items-center gap-2">
            <Activity
              className="h-3.5 w-3.5"
              style={{ color: "var(--utb-cyan)" }}
            />
            <span className="hud-label" style={{ color: "var(--text-muted)" }}>
              dashboard
            </span>
            <span className="hud-label" style={{ color: "var(--surface-3)" }}>
              //
            </span>
            <span className="hud-label" style={{ color: "var(--utb-cyan)" }}>
              {navigation.find((n) => pathname.startsWith(n.href))?.name ?? "—"}
            </span>
          </div>

          {/* System tag */}
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1.5">
              <div
                className="h-1.5 w-1.5 rounded-full animate-pulse"
                style={{ background: "var(--utb-emerald)" }}
              />
              <span
                className="hud-label"
                style={{ color: "var(--text-muted)", fontSize: "9px" }}
              >
                SISTEMA ACTIVO
              </span>
            </div>
            <div
              className="hud-label"
              style={{ fontSize: "9px", color: "var(--surface-4)" }}
            >
              UTB · SPS · v2.0
            </div>
          </div>
        </header>

        {/* Page content */}
        <div className="px-6 py-6">{children}</div>
      </main>
    </div>
  );
}
