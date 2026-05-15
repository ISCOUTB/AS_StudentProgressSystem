"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import Image from "next/image"
import Link from "next/link"
import { Mail, Lock, Eye, EyeOff, ArrowRight } from "lucide-react"

export default function LoginPage() {
  const router = useRouter()
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [showPassword, setShowPassword] = useState(false)
  const [rememberMe, setRememberMe] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // For demo purposes, redirect to dashboard
    router.push("/dashboard/logros")
  }

  return (
    <main className="relative min-h-screen w-full overflow-hidden">
      {/* Background Image */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{ backgroundImage: "url('/images/fondo-login.png')" }}
      />
      
      {/* Login Card Container */}
      <div className="relative z-10 flex min-h-screen items-center justify-center px-4">
        <div className="w-full max-w-4xl overflow-hidden rounded-2xl bg-white/80 shadow-2xl backdrop-blur-sm">
          <div className="flex flex-col lg:flex-row">
            {/* Left Side - Logo Section */}
            <div className="flex flex-col items-center justify-center bg-gradient-to-br from-[#e0f7fa]/50 to-[#b2ebf2]/30 p-8 lg:w-2/5 lg:p-12">
              <div className="flex flex-col items-center">
                <Image
                  src="/images/utb-logo-original.svg"
                  alt="UTB Logo"
                  width={200}
                  height={100}
                  className="mb-4 h-20 w-auto lg:h-24"
                />
                <h2 className="text-center text-lg font-semibold text-[#1a1a2e]">
                  Universidad Tecnológica
                </h2>
                <p className="text-center text-lg font-semibold text-[#1a1a2e]">
                  de Bolívar
                </p>
              </div>
              
              {/* Decorative dots */}
              <div className="mt-12 grid grid-cols-2 gap-1">
                {[...Array(8)].map((_, i) => (
                  <div key={i} className="h-2 w-2 rounded-sm bg-[#1BB9EB]" />
                ))}
              </div>
            </div>
            
            {/* Right Side - Form Section */}
            <div className="flex flex-col justify-center p-8 lg:w-3/5 lg:p-12">
              <div className="mx-auto w-full max-w-sm">
                <h1 className="mb-2 text-3xl font-bold text-[#1a1a2e] lg:text-4xl">
                  Student Progress
                </h1>
                <p className="mb-8 text-[#1a1a2e]/70">
                  Sistema de Progreso Académico
                </p>
                
                {/* Login Tab Indicator */}
                <div className="mb-8 flex items-center gap-4">
                  <span className="font-semibold text-[#1BB9EB]">Iniciar sesión</span>
                  <div className="h-px flex-1 bg-[#1BB9EB]/30" />
                  <div className="h-3 w-3 rounded-full bg-[#1BB9EB]" />
                </div>
                
                <form onSubmit={handleSubmit} className="space-y-6">
                  {/* Email Field */}
                  <div className="relative rounded-xl border border-gray-200 bg-white p-4 transition-all focus-within:border-[#1BB9EB] focus-within:shadow-sm">
                    <div className="flex items-start gap-4">
                      <Mail className="mt-1 h-5 w-5 text-[#1a1a2e]/40" />
                      <div className="flex-1">
                        <label className="mb-1 block text-xs font-medium uppercase tracking-wider text-[#1a1a2e]/50">
                          Correo institucional
                        </label>
                        <input
                          type="email"
                          value={email}
                          onChange={(e) => setEmail(e.target.value)}
                          placeholder="usuario@utb.edu.co"
                          className="w-full bg-transparent text-[#1a1a2e] placeholder-[#1a1a2e]/40 outline-none"
                        />
                      </div>
                    </div>
                  </div>
                  
                  {/* Password Field */}
                  <div className="relative rounded-xl border border-gray-200 bg-white p-4 transition-all focus-within:border-[#1BB9EB] focus-within:shadow-sm">
                    <div className="flex items-start gap-4">
                      <Lock className="mt-1 h-5 w-5 text-[#1a1a2e]/40" />
                      <div className="flex-1">
                        <label className="mb-1 block text-xs font-medium uppercase tracking-wider text-[#1a1a2e]/50">
                          Contraseña
                        </label>
                        <div className="flex items-center">
                          <input
                            type={showPassword ? "text" : "password"}
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="••••••••"
                            className="w-full bg-transparent text-[#1a1a2e] placeholder-[#1a1a2e]/40 outline-none"
                          />
                          <button
                            type="button"
                            onClick={() => setShowPassword(!showPassword)}
                            className="text-[#1a1a2e]/40 hover:text-[#1a1a2e]"
                          >
                            {showPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  {/* Remember Me & Forgot Password */}
                  <div className="flex items-center justify-between">
                    <label className="flex cursor-pointer items-center gap-2">
                      <input
                        type="checkbox"
                        checked={rememberMe}
                        onChange={(e) => setRememberMe(e.target.checked)}
                        className="h-4 w-4 rounded border-gray-300 text-[#1BB9EB] focus:ring-[#1BB9EB]"
                      />
                      <span className="text-sm text-[#1a1a2e]/70">Recordarme</span>
                    </label>
                    <Link 
                      href="#" 
                      className="text-sm font-medium text-[#1BB9EB] hover:underline"
                    >
                      ¿Olvidaste tu contraseña?
                    </Link>
                  </div>
                  
                  {/* Submit Button */}
                  <button
                    type="submit"
                    className="group flex w-full items-center justify-center gap-3 rounded-xl bg-gradient-to-r from-[#1BB9EB] to-[#0891b2] py-4 font-semibold text-white transition-all hover:from-[#0891b2] hover:to-[#1BB9EB] hover:shadow-lg"
                  >
                    Iniciar sesión
                    <ArrowRight className="h-5 w-5 transition-transform group-hover:translate-x-1" />
                  </button>
                </form>
                
                {/* Footer */}
                <div className="mt-8 text-center text-xs text-[#1a1a2e]/50">
                  <p>�� 2025 Universidad Tecnológica de Bolívar</p>
                  <p>Todos los derechos reservados.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}
