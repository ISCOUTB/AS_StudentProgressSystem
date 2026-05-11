"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Mail, Lock, ArrowRight, Eye, EyeOff } from "lucide-react";
import { isTokenExpired } from "@/lib/api";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

function Toast({ message, type, onClose }: { message: string; type: "error" | "success"; onClose: () => void }) {
  useEffect(() => {
    const t = setTimeout(onClose, 3500);
    return () => clearTimeout(t);
  }, [onClose]);

  return (
    <div
      className={`fixed top-6 right-6 z-50 flex items-center gap-3 px-5 py-4 rounded-2xl shadow-2xl text-sm font-medium transition-all duration-300 animate-slide-in ${
        type === "error"
          ? "bg-red-500/95 text-white"
          : "bg-emerald-500/95 text-white"
      }`}
      style={{ backdropFilter: "blur(12px)" }}
    >
      <span className="text-lg">{type === "error" ? "✕" : "✓"}</span>
      {message}
      <button
        onClick={onClose}
        className="ml-2 opacity-70 hover:opacity-100 text-lg leading-none"
      >
        ×
      </button>
    </div>
  );
}

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [remember, setRemember] = useState(false);
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState<{ message: string; type: "error" | "success" } | null>(null);
  const [errors, setErrors] = useState<{ email?: string; password?: string }>({});
  const [emailFocused, setEmailFocused] = useState(false);
  const [passwordFocused, setPasswordFocused] = useState(false);

  useEffect(() => {
    // Check if already logged in
    const token = localStorage.getItem("sps_token");
    if (token && !isTokenExpired(token)) {
      router.replace("/dashboard");
      return;
    }

    const saved = localStorage.getItem("sps_email");
    if (saved) {
      setEmail(saved);
      setRemember(true);
    }
  }, [router]);

  const validate = () => {
    const errs: { email?: string; password?: string } = {};

    if (!email) {
      errs.email = "El correo es requerido";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      errs.email = "Ingresa un correo válido";
    }

    if (!password) {
      errs.password = "La contraseña es requerida";
    } else if (password.length < 6) {
      errs.password = "Mínimo 6 caracteres";
    }

    return errs;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const errs = validate();

    if (Object.keys(errs).length > 0) {
      setErrors(errs);
      return;
    }

    setErrors({});
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
        }),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Credenciales incorrectas");
      }

      const data = await res.json();

      localStorage.setItem("sps_token", data.access_token);

      if (remember) {
        localStorage.setItem("sps_email", email);
      } else {
        localStorage.removeItem("sps_email");
      }

      setToast({
        message: "Bienvenido al sistema",
        type: "success",
      });

      setTimeout(() => {
        router.push("/dashboard");
      }, 1000);
    } catch (err) {
      setToast({
        message: err instanceof Error ? err.message : "Error de conexión",
        type: "error",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <style jsx global>{`
        @keyframes slide-in {
          from {
            opacity: 0;
            transform: translateX(24px);
          }
          to {
            opacity: 1;
            transform: translateX(0);
          }
        }

        @keyframes card-in {
          from {
            opacity: 0;
            transform: translateY(20px) scale(0.98);
          }
          to {
            opacity: 1;
            transform: translateY(0) scale(1);
          }
        }

        .animate-slide-in {
          animation: slide-in 0.3s ease both;
        }

        .animate-card-in {
          animation: card-in 0.6s cubic-bezier(0.16, 1, 0.3, 1) both;
        }
      `}</style>

      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}

      <div className="min-h-screen w-full flex items-center justify-center relative overflow-hidden">
        {/* Background Image */}
        <div 
          className="absolute inset-0 bg-cover bg-center"
          style={{ backgroundImage: "url('/login-bg.png')" }}
        />

        {/* Main Card */}
        <div className="relative z-10 w-full max-w-[800px] mx-4 animate-card-in">
          <div 
            className="flex rounded-[24px] overflow-hidden shadow-2xl"
            style={{ 
              background: "rgba(255, 255, 255, 0.85)",
              backdropFilter: "blur(20px)",
              boxShadow: "0 25px 80px rgba(0, 0, 0, 0.12), 0 0 0 1px rgba(255, 255, 255, 0.5)"
            }}
          >
            {/* Left Panel - Logo */}
            <div className="hidden md:flex flex-col items-center justify-center w-[280px] p-10 border-r border-slate-200/60">
              {/* UTB Logo */}
              <div className="mb-4">
                <img 
                  src="/logo-utb.png" 
                  alt="UTB - Universidad Tecnológica de Bolívar" 
                  className="w-32 h-auto"
                  style={{
                    filter: "brightness(0) saturate(100%) invert(10%) sepia(30%) saturate(1500%) hue-rotate(180deg) brightness(95%) contrast(95%)"
                  }}
                />
              </div>
              <p className="text-[#0B2131] text-center font-semibold text-sm leading-tight">
                Universidad Tecnológica<br />de Bolívar
              </p>
            </div>

            {/* Right Panel - Form */}
            <div className="flex-1 p-8 md:p-10">
              {/* Header */}
              <div className="mb-6">
                <h1 className="text-[#1e3a5f] text-2xl md:text-[28px] font-bold tracking-tight">
                  Student Progress
                </h1>
                <p className="text-slate-500 text-sm mt-1">
                  Sistema de Progreso Académico
                </p>
              </div>

              {/* Section Title with Line */}
              <div className="flex items-center gap-3 mb-6">
                <span className="text-[#0ea5e9] text-sm font-semibold">Iniciar sesión</span>
                <div className="flex-1 h-px bg-slate-200" />
                <div className="w-2 h-2 rounded-full bg-[#0ea5e9]" />
              </div>

              <form onSubmit={handleSubmit} className="space-y-5">
                {/* Email Field */}
                <div 
                  className={`flex items-center gap-3 px-4 py-3 rounded-xl border-2 transition-all duration-200 bg-white ${
                    emailFocused 
                      ? "border-[#0ea5e9] shadow-[0_0_0_3px_rgba(14,165,233,0.1)]" 
                      : errors.email 
                        ? "border-red-300" 
                        : "border-slate-200 hover:border-slate-300"
                  }`}
                >
                  <Mail className="w-5 h-5 text-slate-400 flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <label className="block text-xs text-slate-400 font-medium mb-0.5">
                      Correo institucional
                    </label>
                    <input
                      type="email"
                      value={email}
                      onChange={(e) => {
                        setEmail(e.target.value);
                        setErrors((p) => ({ ...p, email: undefined }));
                      }}
                      onFocus={() => setEmailFocused(true)}
                      onBlur={() => setEmailFocused(false)}
                      placeholder="usuario@utb.edu.co"
                      autoComplete="email"
                      className="w-full bg-transparent text-sm text-slate-700 placeholder-slate-300 outline-none"
                    />
                  </div>
                </div>
                {errors.email && (
                  <p className="text-xs text-red-500 flex items-center gap-1 -mt-3">
                    <span>⚠</span> {errors.email}
                  </p>
                )}

                {/* Password Field */}
                <div 
                  className={`flex items-center gap-3 px-4 py-3 rounded-xl border-2 transition-all duration-200 bg-white ${
                    passwordFocused 
                      ? "border-[#0ea5e9] shadow-[0_0_0_3px_rgba(14,165,233,0.1)]" 
                      : errors.password 
                        ? "border-red-300" 
                        : "border-slate-200 hover:border-slate-300"
                  }`}
                >
                  <Lock className="w-5 h-5 text-slate-400 flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <label className="block text-xs text-slate-400 font-medium mb-0.5">
                      Contraseña
                    </label>
                    <input
                      type={showPassword ? "text" : "password"}
                      value={password}
                      onChange={(e) => {
                        setPassword(e.target.value);
                        setErrors((p) => ({ ...p, password: undefined }));
                      }}
                      onFocus={() => setPasswordFocused(true)}
                      onBlur={() => setPasswordFocused(false)}
                      placeholder="••••••••"
                      autoComplete="current-password"
                      className="w-full bg-transparent text-sm text-slate-700 placeholder-slate-300 outline-none"
                    />
                  </div>
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="p-1 text-slate-400 hover:text-[#0ea5e9] transition-colors flex-shrink-0"
                    aria-label={showPassword ? "Ocultar contraseña" : "Mostrar contraseña"}
                  >
                    {showPassword ? (
                      <EyeOff className="w-5 h-5" />
                    ) : (
                      <Eye className="w-5 h-5" />
                    )}
                  </button>
                </div>
                {errors.password && (
                  <p className="text-xs text-red-500 flex items-center gap-1 -mt-3">
                    <span>⚠</span> {errors.password}
                  </p>
                )}

                {/* Remember & Forgot */}
                <div className="flex items-center justify-between">
                  <label className="flex items-center gap-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={remember}
                      onChange={(e) => setRemember(e.target.checked)}
                      className="w-4 h-4 rounded border-slate-300 text-[#0ea5e9] focus:ring-[#0ea5e9] focus:ring-offset-0"
                    />
                    <span className="text-sm text-slate-600">Recordarme</span>
                  </label>
                  <a 
                    href="/forgot-password" 
                    className="text-sm text-[#0ea5e9] hover:text-[#0284c7] font-medium transition-colors"
                  >
                    ¿Olvidaste tu contraseña?
                  </a>
                </div>

                {/* Submit Button */}
                <button
                  type="submit"
                  disabled={loading}
                  className="w-full py-3.5 rounded-xl text-white font-semibold text-sm transition-all duration-200 flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed hover:shadow-lg hover:shadow-cyan-500/25 active:scale-[0.99]"
                  style={{
                    background: "linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%)"
                  }}
                >
                  {loading ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                      Verificando...
                    </>
                  ) : (
                    <>
                      Iniciar sesión
                      <ArrowRight className="w-4 h-4" />
                    </>
                  )}
                </button>
              </form>

              {/* Footer */}
              <p className="text-center text-xs text-slate-400 mt-8 leading-relaxed">
                © 2025 Universidad Tecnológica de Bolívar<br />
                Todos los derechos reservados.
              </p>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
