"use client";

import { useState, useEffect } from "react";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

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
      <button
        onClick={onClose}
        className="ml-2 opacity-70 hover:opacity-100 text-lg leading-none"
      >
        ×
      </button>
    </div>
  );
}

function InputField({
  label,
  type,
  value,
  onChange,
  placeholder,
  icon,
  error,
  autoComplete,
}) {
  const [show, setShow] = useState(false);
  const [focused, setFocused] = useState(false);

  const isPassword = type === "password";

  return (
    <div className="flex flex-col gap-1.5">
      <label className="text-xs font-semibold tracking-widest text-slate-300 uppercase">
        {label}
      </label>

      <div
        className={`relative flex items-center rounded-xl border transition-all duration-200 ${
          focused
            ? "border-cyan-400 shadow-[0_0_0_3px_rgba(34,211,238,0.15)]"
            : error
            ? "border-red-400/60"
            : "border-white/20 hover:border-white/30"
        }`}
        style={{
          background: "rgba(255,255,255,0.07)",
        }}
      >
        <span className="absolute left-4 text-slate-300 text-base select-none">
          {icon}
        </span>

        <input
          type={isPassword && show ? "text" : type}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          autoComplete={autoComplete}
          onFocus={() => setFocused(true)}
          onBlur={() => setFocused(false)}
          className="w-full bg-transparent py-3.5 pl-11 pr-11 text-sm text-slate-100 placeholder-slate-400 outline-none font-light tracking-wide"
        />

        {isPassword && (
          <button
            type="button"
            onClick={() => setShow(!show)}
            className="absolute right-4 text-slate-300 hover:text-white transition-colors text-base"
          >
            {show ? "◻" : "◼"}
          </button>
        )}
      </div>

      {error && (
        <p className="text-xs text-red-300 flex items-center gap-1">
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

  useEffect(() => {
    const saved = localStorage.getItem("sps_email");

    if (saved) {
      setEmail(saved);
      setRemember(true);
    }
  }, []);

  const validate = () => {
    const errs = {};

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
        window.location.href = "/dashboard";
      }, 1000);
    } catch (err) {
      setToast({
        message: err.message,
        type: "error",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

        * {
          box-sizing: border-box;
          margin: 0;
          padding: 0;
        }

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
        }

        .bg-image {
          position: absolute;
          inset: 0;
          background-image: url('/login-bg.png');
          background-size: cover;
          background-position: center;
          opacity: 1;
        }

        .bg-overlay {
          position: absolute;
          inset: 0;
          background:
            linear-gradient(
              135deg,
              rgba(255,255,255,0.78) 0%,
              rgba(255,255,255,0.60) 35%,
              rgba(10,14,26,0.25) 100%
            );
        }

        .login-card {
          position: relative;
          z-index: 10;
          width: 100%;
          max-width: 440px;
          margin: 24px;
          background: rgba(15, 23, 42, 0.82);
          border: 1px solid rgba(255,255,255,0.08);
          border-radius: 28px;
          padding: 48px 44px;
          backdrop-filter: blur(22px);
          box-shadow:
            0 25px 80px rgba(0,0,0,0.35),
            0 0 0 1px rgba(255,255,255,0.03) inset;
          animation: cardIn 0.7s cubic-bezier(0.16,1,0.3,1) both;
        }

        @keyframes cardIn {
          from {
            opacity: 0;
            transform: translateY(24px) scale(0.97);
          }

          to {
            opacity: 1;
            transform: translateY(0) scale(1);
          }
        }

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

        .animate-slide-in {
          animation: slide-in 0.3s ease both;
        }

        .logo-mark {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          width: 52px;
          height: 52px;
          background: linear-gradient(135deg, #06b6d4, #2563eb);
          border-radius: 16px;
          font-family: 'Syne', sans-serif;
          font-weight: 800;
          color: white;
          letter-spacing: -1px;
          box-shadow: 0 8px 24px rgba(6,182,212,0.35);
        }

        .title {
          font-family: 'Syne', sans-serif;
          font-weight: 700;
          font-size: 27px;
          color: #f8fafc;
          letter-spacing: -0.7px;
          line-height: 1.2;
        }

        .subtitle {
          font-size: 13px;
          color: #cbd5e1;
          margin-top: 6px;
          font-weight: 400;
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
          background: rgba(255,255,255,0.10);
        }

        .divider-text {
          font-size: 11px;
          color: #cbd5e1;
          font-weight: 600;
          letter-spacing: 1px;
          text-transform: uppercase;
        }

        .accent-dot {
          width: 6px;
          height: 6px;
          border-radius: 50%;
          background: linear-gradient(135deg, #06b6d4, #3b82f6);
          box-shadow: 0 0 8px rgba(6,182,212,0.6);
        }

        .checkbox-row {
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin-top: -2px;
        }

        .checkbox-label {
          display: flex;
          align-items: center;
          gap: 8px;
          cursor: pointer;
          font-size: 13px;
          color: #cbd5e1;
          user-select: none;
        }

        .checkbox-label input[type="checkbox"] {
          width: 16px;
          height: 16px;
          accent-color: #06b6d4;
          cursor: pointer;
        }

        .forgot-link {
          font-size: 13px;
          color: #67e8f9;
          text-decoration: none;
          font-weight: 500;
          transition: color 0.2s;
        }

        .forgot-link:hover {
          color: white;
        }

        .btn-primary {
          width: 100%;
          padding: 15px;
          background: linear-gradient(135deg, #06b6d4, #2563eb);
          border: none;
          border-radius: 16px;
          color: white;
          font-family: 'Syne', sans-serif;
          font-weight: 600;
          font-size: 14px;
          letter-spacing: 0.3px;
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

        .btn-primary:disabled {
          opacity: 0.7;
          cursor: not-allowed;
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
          to {
            transform: rotate(360deg);
          }
        }

        .footer-text {
          text-align: center;
          font-size: 11.5px;
          color: #cbd5e1;
          margin-top: 30px;
        }

        @media (max-width: 480px) {
          .login-card {
            padding: 36px 28px;
            border-radius: 24px;
            margin: 16px;
          }

          .title {
            font-size: 22px;
          }
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

        <div className="login-card">
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "14px",
              marginBottom: "32px",
            }}
          >
            <div className="logo-mark">
              <span style={{ fontSize: "15px" }}>UTB</span>
            </div>

            <div>
              <p className="title">
                Sistema de Progreso Académico
              </p>

              <p className="subtitle">
                Accede con tu correo institucional
              </p>
            </div>
          </div>

          <div
            className="divider"
            style={{ marginBottom: "28px" }}
          >
            <div className="divider-line" />
            <div className="accent-dot" />
            <span className="divider-text">
              Acceso institucional
            </span>
            <div className="accent-dot" />
            <div className="divider-line" />
          </div>

          <form
            onSubmit={handleSubmit}
            style={{
              display: "flex",
              flexDirection: "column",
              gap: "22px",
            }}
          >
            <InputField
              label="Correo institucional"
              type="email"
              value={email}
              onChange={(e) => {
                setEmail(e.target.value);
                setErrors((p) => ({
                  ...p,
                  email: "",
                }));
              }}
              placeholder="usuario@utb.edu.co"
              error={errors.email}
              autoComplete="email"
            />

            <InputField
              label="Contraseña"
              type="password"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value);
                setErrors((p) => ({
                  ...p,
                  password: "",
                }));
              }}
              placeholder="••••••••"
              error={errors.password}
              autoComplete="current-password"
            />

            <div className="checkbox-row">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={remember}
                  onChange={(e) =>
                    setRemember(e.target.checked)
                  }
                />
                Recordarme
              </label>

              <a
                href="/forgot-password"
                className="forgot-link"
              >
                ¿Olvidaste tu contraseña?
              </a>
            </div>

            <button
              type="submit"
              className="btn-primary"
              disabled={loading}
              style={{ marginTop: "10px" }}
            >
              {loading ? (
                <span
                  style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    gap: "10px",
                  }}
                >
                  <span className="spinner" />
                  Verificando credenciales...
                </span>
              ) : (
                <span
                  style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    gap: "10px",
                  }}
                >
                  Acceder al sistema
                  <span style={{ fontSize: "16px" }}>
                    →
                  </span>
                </span>
              )}
            </button>
          </form>

          <p className="footer-text">
            © 2025 Universidad Tecnológica de Bolívar
            <br />
            Sistema de Seguimiento Estudiantil
          </p>
        </div>
      </div>
    </>
  );
}