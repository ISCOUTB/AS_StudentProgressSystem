"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { isTokenExpired } from "@/lib/api";

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("sps_token");
    
    // If token exists and is valid, go to dashboard
    if (token && !isTokenExpired(token)) {
      router.replace("/dashboard");
    } else {
      // Otherwise, go to login
      router.replace("/login");
    }
  }, [router]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-100">
      <div className="w-10 h-10 border-4 border-[#0ea5e9] border-t-transparent rounded-full animate-spin" />
    </div>
  );
}
