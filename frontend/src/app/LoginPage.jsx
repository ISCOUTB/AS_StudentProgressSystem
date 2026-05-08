"use client";

import { useState, useEffect } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

function Toast({ message, type, onClose }) {
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
      <button onClick={onClose} className="ml-2 opacity-70 hover:opacity-100 text-lg leading-none">×</button>
    </div>
  );
}

function InputField({ label, type, value, onChange, placeholder, icon, error, autoComplete }) {
  const [show, setShow] = useState(false);
  const [focused, setFocused] = useState(false);
  const isPassword = type === "password";

  return (
    <div className="flex flex-col gap-1.5">
      <label className="text-xs font-semibold tracking-widest text-slate-400 uppercase">
        {label}
      </label>
      <div className={`relative flex items-center rounded-xl border transition-all duration-200 bg-white/5 ${
        focused
          ? "border-cyan-400 shadow-[0_0_0_3px_rgba(34,211,238,0.15)]"
          : error
          ? "border-red-400/60"
          : "border-white/10 hover:border-white/25"
      }`}>
        <span className="absolute left-4 text-slate-400 text-base select-none">{icon}</span>
        <input
          type={isPassword && show ? "text" : type}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          autoComplete={autoComplete}
          onFocus={() => setFocused(true)}
          onBlur={() => setFocused(false)}
          className="w-full bg-transparent py-3.5 pl-11 pr-11 text-sm text-white placeholder-slate-500 outline-none font-light tracking-wide"
        />
        {isPassword && (
          <button
            type="button"
            onClick={() => setShow(!show)}
            className="absolute right-4 text-slate-400 hover:text-slate-200 transition-colors text-base"
          >
            {show ? "◻" : "◼"}
          </button>
        )}
      </div>
      {error && (
        <p className="text-xs text-red-400 flex items-center gap-1">
          <span>⚠</span> {error}
        </p>
      )}
    </div>
  );
}

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [remember, setRemember] = useState(false);
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState(null);
  const [errors, setErrors] = useState({});
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const saved = localStorage.getItem("sps_email");
    if (saved) {
      setEmail(saved);
      setRemember(true);
    }
  }, []);

  const validate = () => {
    const errs = {};
    if (!email) errs.email = "El correo es requerido";
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))
      errs.email = "Ingresa un correo válido";
    if (!password) errs.password = "La contraseña es requerida";
    else if (password.length < 6)
      errs.password = "Mínimo 6 caracteres";
    return errs;
  };

  const handleSubmit = async (e) => {
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
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Credenciales incorrectas");
      }

      const data = await res.json();
      localStorage.setItem("sps_token", data.access_token);
      if (remember) localStorage.setItem("sps_email", email);
      else localStorage.removeItem("sps_email");

      setToast({ message: "Bienvenido al sistema", type: "success" });
      setTimeout(() => {
        window.location.href = "/dashboard";
      }, 1000);
    } catch (err) {
      setToast({ message: err.message, type: "error" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
          font-family: 'DM Sans', sans-serif;
          background: #0a0e1a;
        }

        .login-root {
          min-height: 100vh;
          width: 100%;
          display: flex;
          align-items: center;
          justify-content: center;
          position: relative;
          overflow: hidden;
          background: #0a0e1a;
        }

        .bg-image {
          position: absolute;
          inset: 0;
          background-image: url('/login-bg.png');
          background-size: cover;
          background-position: center;
          opacity: 0.18;
          filter: saturate(1.4) brightness(0.8);
          mix-blend-mode: luminosity;
        }

        .bg-overlay {
          position: absolute;
          inset: 0;
          background: radial-gradient(ellipse 80% 60% at 50% 0%, rgba(6,182,212,0.08) 0%, transparent 70%),
                      radial-gradient(ellipse 60% 80% at 80% 100%, rgba(59,130,246,0.06) 0%, transparent 70%),
                      linear-gradient(160deg, #0a0e1a 0%, #0d1629 50%, #0a1a1f 100%);
        }

        .grid-lines {
          position: absolute;
          inset: 0;
          background-image:
            linear-gradient(rgba(255,255,255,0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.02) 1px, transparent 1px);
          background-size: 60px 60px;
          mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 30%, transparent 100%);
        }

        .login-card {
          position: relative;
          z-index: 10;
          width: 100%;
          max-width: 440px;
          margin: 24px;
          background: rgba(255,255,255,0.04);
          border: 1px solid rgba(255,255,255,0.08);
          border-radius: 28px;
          padding: 48px 44px;
          backdrop-filter: blur(40px);
          box-shadow:
            0 0 0 1px rgba(255,255,255,0.04) inset,
            0 40px 80px rgba(0,0,0,0.5),
            0 0 120px rgba(6,182,212,0.04);
          animation: cardIn 0.7s cubic-bezier(0.16,1,0.3,1) both;
        }

        @keyframes cardIn {
          from { opacity: 0; transform: translateY(24px) scale(0.97); }
          to   { opacity: 1; transform: translateY(0) scale(1); }
        }

        @keyframes slide-in {
          from { opacity: 0; transform: translateX(24px); }
          to   { opacity: 1; transform: translateX(0); }
        }

        .animate-slide-in { animation: slide-in 0.3s ease both; }

        .logo-mark {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          width: 48px;
          height: 48px;
          background: linear-gradient(135deg, #06b6d4, #3b82f6);
          border-radius: 14px;
          font-family: 'Syne', sans-serif;
          font-weight: 800;
          font-size: 18px;
          color: white;
          letter-spacing: -1px;
          box-shadow: 0 8px 24px rgba(6,182,212,0.3);
        }

        .title {
          font-family: 'Syne', sans-serif;
          font-weight: 700;
          font-size: 26px;
          color: #f1f5f9;
          letter-spacing: -0.5px;
          line-height: 1.2;
        }

        .subtitle {
          font-size: 13px;
          color: #64748b;
          margin-top: 6px;
          font-weight: 400;
          letter-spacing: 0.1px;
        }

        .divider {
          display: flex;
          align-items: center;
          gap: 12px;
          margin: 4px 0;
        }

        .divider-line {
          flex: 1;
          height: 1px;
          background: rgba(255,255,255,0.07);
        }

        .divider-text {
          font-size: 11px;
          color: #334155;
          font-weight: 500;
          letter-spacing: 1px;
          text-transform: uppercase;
        }

        .btn-primary {
          width: 100%;
          padding: 14px;
          background: linear-gradient(135deg, #06b6d4, #3b82f6);
          border: none;
          border-radius: 14px;
          color: white;
          font-family: 'Syne', sans-serif;
          font-weight: 600;
          font-size: 14px;
          letter-spacing: 0.5px;
          cursor: pointer;
          transition: all 0.2s ease;
          position: relative;
          overflow: hidden;
          box-shadow: 0 8px 24px rgba(6,182,212,0.25);
        }

        .btn-primary:hover:not(:disabled) {
          transform: translateY(-1px);
          box-shadow: 0 12px 32px rgba(6,182,212,0.35);
        }

        .btn-primary:active:not(:disabled) {
          transform: translateY(0);
        }

        .btn-primary:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        .btn-google {
          width: 100%;
          padding: 12px;
          background: rgba(255,255,255,0.04);
          border: 1px solid rgba(255,255,255,0.08);
          border-radius: 14px;
          color: #94a3b8;
          font-size: 13px;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.2s;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 10px;
        }

        .btn-google:hover {
          background: rgba(255,255,255,0.07);
          border-color: rgba(255,255,255,0.14);
          color: #cbd5e1;
        }

        .checkbox-row {
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin: 2px 0;
        }

        .checkbox-label {
          display: flex;
          align-items: center;
          gap: 8px;
          cursor: pointer;
          font-size: 13px;
          color: #64748b;
          user-select: none;
        }

        .checkbox-label input[type="checkbox"] {
          width: 16px;
          height: 16px;
          accent-color: #06b6d4;
          cursor: pointer;
          border-radius: 4px;
        }

        .forgot-link {
          font-size: 13px;
          color: #06b6d4;
          text-decoration: none;
          font-weight: 500;
          transition: color 0.2s;
        }

        .forgot-link:hover {
          color: #67e8f9;
        }

        .spinner {
          width: 18px;
          height: 18px;
          border: 2px solid rgba(255,255,255,0.3);
          border-top-color: white;
          border-radius: 50%;
          animation: spin 0.7s linear infinite;
          display: inline-block;
        }

        @keyframes spin {
          to { transform: rotate(360deg); }
        }

        .loading-shimmer {
          position: absolute;
          inset: 0;
          background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
          animation: shimmer 1.5s infinite;
        }

        @keyframes shimmer {
          from { transform: translateX(-100%); }
          to   { transform: translateX(100%); }
        }

        .accent-dot {
          width: 6px;
          height: 6px;
          border-radius: 50%;
          background: linear-gradient(135deg, #06b6d4, #3b82f6);
          box-shadow: 0 0 8px rgba(6,182,212,0.6);
        }

        .footer-text {
          text-align: center;
          font-size: 11.5px;
          color: #1e293b;
          margin-top: 32px;
          letter-spacing: 0.2px;
        }

        @media (max-width: 480px) {
          .login-card {
            padding: 36px 28px;
            border-radius: 24px;
            margin: 16px;
          }
          .title { font-size: 22px; }
        }
      `}</style>

      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}

      <div className="login-root">
        <div className="bg-image" />
        <div className="bg-overlay" />
        <div className="grid-lines" />

        <div className="login-card">
          {/* Header */}
          <div style={{ display: "flex", alignItems: "center", gap: "14px", marginBottom: "32px" }}>
            <div className="logo-mark">UTB</div>
            <div>
              <p className="title">Student Progress</p>
              <p className="subtitle">Universidad Tecnológica de Bolívar</p>
            </div>
          </div>

          {/* Divider */}
          <div className="divider" style={{ marginBottom: "28px" }}>
            <div className="divider-line" />
            <div className="accent-dot" />
            <span className="divider-text">Acceso institucional</span>
            <div className="accent-dot" />
            <div className="divider-line" />
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
            <InputField
              label="Correo institucional"
              type="email"
              value={email}
              onChange={(e) => { setEmail(e.target.value); setErrors(p => ({ ...p, email: "" })); }}
              placeholder="usuario@utb.edu.co"
              icon="✉"
              error={errors.email}
              autoComplete="email"
            />

            <InputField
              label="Contraseña"
              type="password"
              value={password}
              onChange={(e) => { setPassword(e.target.value); setErrors(p => ({ ...p, password: "" })); }}
              placeholder="••••••••"
              icon="⚿"
              error={errors.password}
              autoComplete="current-password"
            />

            <div className="checkbox-row">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={remember}
                  onChange={(e) => setRemember(e.target.checked)}
                />
                Recordarme
              </label>
              <a href="/forgot-password" className="forgot-link">
                ¿Olvidaste tu contraseña?
              </a>
            </div>

            <button type="submit" className="btn-primary" disabled={loading} style={{ marginTop: "4px" }}>
              {loading ? (
                <span style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: "10px" }}>
                  <span className="spinner" />
                  Verificando...
                  <span className="loading-shimmer" />
                </span>
              ) : (
                "Iniciar sesión →"
              )}
            </button>

            {/* Divider */}
            <div className="divider">
              <div className="divider-line" />
              <span className="divider-text">o continúa con</span>
              <div className="divider-line" />
            </div>

            <button type="button" className="btn-google">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
                <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
              </svg>
              Continuar con Google
            </button>
          </form>

          <p className="footer-text">
            © 2025 Universidad Tecnológica de Bolívar · Sistema de Progreso Académico
          </p>
        </div>
      </div>
    </>
  );
}
