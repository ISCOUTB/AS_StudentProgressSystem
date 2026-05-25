"use client";

/**
 * Login Page — UTB Design System
 */

import { useState } from "react";
import { useRouter } from "next/navigation";
import Image from "next/image";
import Link from "next/link";
import { Mail, Lock, Eye, EyeOff, ArrowRight, Shield } from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const body = new URLSearchParams();
      body.append("username", email);
      body.append("password", password);
      const res = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: body.toString(),
      });
      if (!res.ok) {
        const data = await res.json();
        setError(data.detail || "Credenciales incorrectas");
        return;
      }
      const data = await res.json();
      localStorage.setItem("sps_token", data.access_token);
      if (rememberMe) localStorage.setItem("sps_email", email);
      else localStorage.removeItem("sps_email");
      router.push("/dashboard/perfil");
    } catch {
      setError("No se pudo conectar con el servidor. Intenta de nuevo.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main
      className="relative min-h-screen w-full overflow-hidden flex items-center justify-center"
      style={{
        backgroundColor: "var(--surface-0)",
        fontFamily: "var(--font-body)",
      }}
    >
      {/* Background image */}
      <div
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: "url('/images/fondo-login.png')",
          opacity: 0.18,
        }}
      />

      {/* HUD grid overlay */}
      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          backgroundImage:
            "linear-gradient(rgba(27,185,235,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(27,185,235,0.04) 1px, transparent 1px)",
          backgroundSize: "32px 32px",
        }}
      />

      {/* Diagonal accent bar — top left */}
      <div
        className="absolute top-0 left-0 pointer-events-none"
        style={{
          width: "360px",
          height: "4px",
          background:
            "linear-gradient(90deg, var(--utb-cyan), var(--utb-emerald), transparent)",
        }}
      />
      <div
        className="absolute top-0 left-0 pointer-events-none"
        style={{
          width: "4px",
          height: "180px",
          background: "linear-gradient(180deg, var(--utb-cyan), transparent)",
        }}
      />

      {/* Bottom right accent */}
      <div
        className="absolute bottom-0 right-0 pointer-events-none"
        style={{
          width: "240px",
          height: "2px",
          background:
            "linear-gradient(270deg, var(--utb-emerald), transparent)",
        }}
      />

      {/* System tag */}
      <div
        className="absolute top-5 right-6 flex items-center gap-2 pointer-events-none"
        style={{
          fontFamily: "var(--font-mono)",
          fontSize: "9px",
          letterSpacing: "0.14em",
          color: "var(--surface-4)",
        }}
      >
        <div
          className="h-1.5 w-1.5 rounded-full"
          style={{
            background: "var(--utb-emerald)",
            boxShadow: "0 0 6px var(--utb-emerald)",
          }}
        />
        UTB · SPS · v2.0
      </div>

      {/* Main card */}
      <div
        className="relative z-10 w-full max-w-3xl mx-4 overflow-hidden"
        style={{
          background: "var(--surface-1)",
          clipPath:
            "polygon(20px 0%, 100% 0%, 100% calc(100% - 20px), calc(100% - 20px) 100%, 0% 100%, 0% 20px)",
          border: "1px solid var(--surface-3)",
          boxShadow:
            "0 0 40px rgba(27,185,235,0.08), 0 20px 60px rgba(10,14,26,0.12)",
        }}
      >
        {/* Top accent line */}
        <div
          style={{
            height: "2px",
            background:
              "linear-gradient(90deg, var(--utb-cyan) 0%, var(--utb-emerald) 50%, transparent 100%)",
          }}
        />

        <div className="flex flex-col lg:flex-row">
          {/* ── Left panel — branding ──────────────────────────── */}
          <div
            className="relative flex flex-col items-center justify-center p-8 lg:w-[42%] lg:p-10"
            style={{
              background:
                "linear-gradient(160deg, rgba(27,185,235,0.06) 0%, rgba(100,237,42,0.04) 100%)",
              borderRight: "1px solid var(--surface-3)",
            }}
          >
            {/* Corner bracket decorations */}
            <span
              className="absolute"
              style={{
                top: "12px",
                left: "12px",
                width: "14px",
                height: "14px",
                borderTop: "1px solid var(--utb-cyan)",
                borderLeft: "1px solid var(--utb-cyan)",
                opacity: 0.5,
              }}
            />
            <span
              className="absolute"
              style={{
                bottom: "12px",
                right: "12px",
                width: "14px",
                height: "14px",
                borderBottom: "1px solid var(--utb-emerald)",
                borderRight: "1px solid var(--utb-emerald)",
                opacity: 0.5,
              }}
            />

            {/* Logo */}
            <div className="mb-6">
              <Image
                src="/images/utb-logo-original.svg"
                alt="UTB"
                width={120}
                height={60}
                className="h-14 w-auto opacity-90"
              />
            </div>

            {/* University name */}
            <div className="text-center mb-8">
              <p
                style={{
                  fontFamily: "var(--font-display)",
                  fontSize: "0.95rem",
                  fontWeight: 700,
                  letterSpacing: "0.06em",
                  textTransform: "uppercase",
                  color: "var(--text-primary)",
                  lineHeight: 1.3,
                }}
              >
                Universidad
                <br />
                Tecnológica
                <br />
                de Bolívar
              </p>
            </div>

            {/* System name block */}
            <div
              style={{
                border: "1px solid var(--surface-3)",
                clipPath: "var(--clip-corner-sm)",
                padding: "0.875rem 1.25rem",
                background: "var(--surface-1)",
                textAlign: "center",
              }}
            >
              <p
                style={{
                  fontFamily: "var(--font-mono)",
                  fontSize: "8px",
                  letterSpacing: "0.2em",
                  color: "var(--utb-cyan)",
                  textTransform: "uppercase",
                  marginBottom: "4px",
                }}
              >
                Sistema Académico
              </p>
              <p
                style={{
                  fontFamily: "var(--font-display)",
                  fontSize: "1rem",
                  fontWeight: 800,
                  letterSpacing: "0.08em",
                  textTransform: "uppercase",
                  color: "var(--text-primary)",
                }}
              >
                Student Progress System
              </p>
              <div
                className="mt-2 mx-auto"
                style={{
                  height: "2px",
                  width: "40px",
                  background:
                    "linear-gradient(90deg, var(--utb-cyan), var(--utb-emerald))",
                }}
              />
            </div>

            {/* Decorative dots grid */}
            <div className="mt-8 grid grid-cols-4 gap-2 opacity-30">
              {Array.from({ length: 16 }).map((_, i) => (
                <div
                  key={i}
                  style={{
                    width: "4px",
                    height: "4px",
                    clipPath: "var(--clip-corner-sm)",
                    background:
                      i % 3 === 0 ? "var(--utb-cyan)" : "var(--surface-3)",
                  }}
                />
              ))}
            </div>
          </div>

          {/* ── Right panel — form ─────────────────────────────── */}
          <div className="flex flex-col justify-center p-8 lg:flex-1 lg:p-10">
            {/* Form heading */}
            <div className="mb-7">
              <div className="flex items-center gap-2 mb-2">
                <div
                  style={{
                    width: "3px",
                    height: "20px",
                    background:
                      "linear-gradient(180deg, var(--utb-cyan), var(--utb-emerald))",
                  }}
                />
                <h1
                  style={{
                    fontFamily: "var(--font-display)",
                    fontSize: "1.4rem",
                    fontWeight: 900,
                    letterSpacing: "0.06em",
                    textTransform: "uppercase",
                    color: "var(--text-primary)",
                  }}
                >
                  Acceso al Sistema
                </h1>
              </div>
              <p
                style={{
                  fontFamily: "var(--font-mono)",
                  fontSize: "10px",
                  letterSpacing: "0.12em",
                  color: "var(--text-muted)",
                  paddingLeft: "11px",
                }}
              >
                Ingresa tus credenciales institucionales
              </p>
            </div>

            {/* Error */}
            {error && (
              <div
                className="mb-5 flex items-center gap-2"
                style={{
                  border: "1px solid rgba(220,38,38,0.35)",
                  background: "rgba(220,38,38,0.06)",
                  clipPath: "var(--clip-corner-sm)",
                  padding: "0.625rem 0.875rem",
                }}
              >
                <div
                  style={{
                    width: "2px",
                    height: "100%",
                    background: "#DC2626",
                    flexShrink: 0,
                    alignSelf: "stretch",
                  }}
                />
                <p
                  style={{
                    fontFamily: "var(--font-mono)",
                    fontSize: "11px",
                    letterSpacing: "0.05em",
                    color: "#DC2626",
                  }}
                >
                  {error}
                </p>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Email field */}
              <div>
                <label
                  htmlFor="email"
                  style={{
                    display: "block",
                    fontFamily: "var(--font-mono)",
                    fontSize: "9px",
                    letterSpacing: "0.18em",
                    textTransform: "uppercase",
                    color: "var(--utb-cyan)",
                    marginBottom: "6px",
                  }}
                >
                  Correo Institucional
                </label>
                <div
                  className="flex items-center gap-3"
                  style={{
                    background: "var(--surface-2)",
                    border: "1px solid var(--surface-3)",
                    clipPath: "var(--clip-corner-sm)",
                    padding: "0.75rem 1rem",
                    transition: "border-color 0.15s ease",
                  }}
                  onFocus={() => {}}
                >
                  <Mail
                    className="h-4 w-4 flex-shrink-0"
                    style={{ color: "var(--utb-cyan)" }}
                  />
                  <input
                    id="email"
                    type="email"
                    value={email}
                    onChange={(e) => {
                      setEmail(e.target.value);
                      setError("");
                    }}
                    placeholder="usuario@utb.edu.co"
                    required
                    style={{
                      flex: 1,
                      background: "transparent",
                      border: "none",
                      outline: "none",
                      fontFamily: "var(--font-body)",
                      fontSize: "0.875rem",
                      color: "var(--text-primary)",
                    }}
                  />
                </div>
              </div>

              {/* Password field */}
              <div>
                <label
                  htmlFor="password"
                  style={{
                    display: "block",
                    fontFamily: "var(--font-mono)",
                    fontSize: "9px",
                    letterSpacing: "0.18em",
                    textTransform: "uppercase",
                    color: "var(--utb-cyan)",
                    marginBottom: "6px",
                  }}
                >
                  Contraseña
                </label>
                <div
                  className="flex items-center gap-3"
                  style={{
                    background: "var(--surface-2)",
                    border: "1px solid var(--surface-3)",
                    clipPath: "var(--clip-corner-sm)",
                    padding: "0.75rem 1rem",
                  }}
                >
                  <Lock
                    className="h-4 w-4 flex-shrink-0"
                    style={{ color: "var(--utb-cyan)" }}
                  />
                  <input
                    id="password"
                    type={showPassword ? "text" : "password"}
                    value={password}
                    onChange={(e) => {
                      setPassword(e.target.value);
                      setError("");
                    }}
                    placeholder="••••••••"
                    required
                    style={{
                      flex: 1,
                      background: "transparent",
                      border: "none",
                      outline: "none",
                      fontFamily: "var(--font-body)",
                      fontSize: "0.875rem",
                      color: "var(--text-primary)",
                    }}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    style={{
                      color: "var(--text-muted)",
                      background: "none",
                      border: "none",
                      cursor: "pointer",
                    }}
                  >
                    {showPassword ? (
                      <EyeOff className="h-4 w-4" />
                    ) : (
                      <Eye className="h-4 w-4" />
                    )}
                  </button>
                </div>
              </div>

              {/* Remember + forgot */}
              <div className="flex items-center justify-between">
                <label className="flex cursor-pointer items-center gap-2">
                  <input
                    type="checkbox"
                    checked={rememberMe}
                    onChange={(e) => setRememberMe(e.target.checked)}
                    style={{
                      accentColor: "var(--utb-cyan)",
                      width: "13px",
                      height: "13px",
                    }}
                  />
                  <span
                    style={{
                      fontFamily: "var(--font-mono)",
                      fontSize: "10px",
                      letterSpacing: "0.08em",
                      color: "var(--text-muted)",
                    }}
                  >
                    Recordarme
                  </span>
                </label>
              </div>

              {/* Submit */}
              <button
                type="submit"
                disabled={loading}
                className="btn-hud-solid w-full"
                style={{
                  justifyContent: "center",
                  padding: "0.875rem",
                  fontSize: "0.8rem",
                  opacity: loading ? 0.7 : 1,
                  cursor: loading ? "not-allowed" : "pointer",
                }}
              >
                {loading ? (
                  <>
                    <svg
                      className="h-4 w-4 animate-spin"
                      viewBox="0 0 24 24"
                      fill="none"
                    >
                      <circle
                        className="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        strokeWidth="3"
                      />
                      <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8v4l3-3-3-3v4a8 8 0 00-8 8h4z"
                      />
                    </svg>
                    Verificando acceso...
                  </>
                ) : (
                  <>
                    Iniciar Sesión
                    <ArrowRight className="h-4 w-4" />
                  </>
                )}
              </button>
            </form>

            {/* Footer */}
            <div
              className="mt-7 pt-5"
              style={{ borderTop: "1px solid var(--surface-3)" }}
            >
              <div className="flex items-center gap-2">
                <Shield
                  className="h-3 w-3"
                  style={{ color: "var(--surface-4)" }}
                />
                <p
                  style={{
                    fontFamily: "var(--font-mono)",
                    fontSize: "9px",
                    letterSpacing: "0.10em",
                    color: "var(--surface-4)",
                  }}
                >
                  © 2026 Universidad Tecnológica de Bolívar · Todos los derechos
                  reservados
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom accent line */}
        <div
          style={{
            height: "1px",
            background:
              "linear-gradient(90deg, transparent, var(--utb-emerald) 60%, transparent)",
            opacity: 0.6,
          }}
        />
      </div>
    </main>
  );
}
