import type { Metadata } from "next";
import { Exo_2, Rajdhani, Share_Tech_Mono } from "next/font/google";
import { Analytics } from "@vercel/analytics/next";
import "./globals.css";

/* ──────────────────────────────────────────────────────────
     UTB Typography System
   ────────────────────────────────────────────────────────── */

const exo = Exo_2({
  subsets: ["latin"],
  variable: "--font-exo",
});

const rajdhani = Rajdhani({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
  variable: "--font-rajdhani",
});

const mono = Share_Tech_Mono({
  subsets: ["latin"],
  weight: "400",
  variable: "--font-mono-tech",
});

export const metadata: Metadata = {
  title: "Student Progress System | UTB",
  description:
    "Sistema de Progreso Académico - Universidad Tecnológica de Bolívar",
    icons: {
    icon: "/images/sps-icon.jpeg",
    shortcut: "/images/sps-icon.jpeg",
    apple: "/images/sps-icon.jpeg",
  },
};


export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="es"
      className={`
        ${exo.variable}
        ${rajdhani.variable}
        ${mono.variable}
      `}
    >
      <body className="font-body antialiased bg-surface-0 text-foreground">
        {children}
        {process.env.NODE_ENV === "production" && <Analytics />}
      </body>
    </html>
  );
}
