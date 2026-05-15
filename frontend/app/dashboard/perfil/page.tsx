"use client"

import { useState } from "react"
import { Lock, Eye, EyeOff, ChevronRight } from "lucide-react"

export default function ProfilePage() {
  const [currentPassword, setCurrentPassword] = useState("")
  const [newPassword, setNewPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [showCurrentPassword, setShowCurrentPassword] = useState(false)
  const [showNewPassword, setShowNewPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)

  return (
    <div className="mx-auto max-w-2xl">
      {/* Password Section */}
      <div className="overflow-hidden rounded-2xl bg-white/90 shadow-lg backdrop-blur-sm">
        {/* Header */}
        <div className="flex items-center gap-4 p-6 pb-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-[#1BB9EB]">
            <Lock className="h-6 w-6 text-white" />
          </div>
          <div>
            <h2 className="text-xl font-bold uppercase tracking-wide text-[#1a1a2e]">
              Contraseña
            </h2>
            <p className="text-sm text-[#1a1a2e]/60">
              Asegúrate de usar una contraseña segura.
            </p>
          </div>
        </div>
        
        {/* Content */}
        <div className="space-y-6 p-6 pt-2">
          {/* Current Password */}
          <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:gap-8">
            <label className="w-48 flex-shrink-0 text-xs font-medium uppercase tracking-wider text-[#1a1a2e]/50">
              Contraseña Actual
            </label>
            <div className="relative flex-1">
              <input
                type={showCurrentPassword ? "text" : "password"}
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                placeholder="Ingresa tu contraseña actual"
                className="w-full rounded-xl border border-gray-200 bg-[#f8f8f8] px-4 py-3 pr-12 text-[#1a1a2e] placeholder-[#1a1a2e]/40 outline-none transition-colors focus:border-[#1BB9EB]"
              />
              <button
                type="button"
                onClick={() => setShowCurrentPassword(!showCurrentPassword)}
                className="absolute right-4 top-1/2 -translate-y-1/2 text-[#1a1a2e]/40 hover:text-[#1a1a2e]"
              >
                {showCurrentPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
              </button>
            </div>
          </div>
          
          {/* New Password */}
          <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:gap-8">
            <label className="w-48 flex-shrink-0 text-xs font-medium uppercase tracking-wider text-[#1a1a2e]/50">
              Nueva Contraseña
            </label>
            <div className="relative flex-1">
              <input
                type={showNewPassword ? "text" : "password"}
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                placeholder="Ingresa tu nueva contraseña"
                className="w-full rounded-xl border border-gray-200 bg-[#f8f8f8] px-4 py-3 pr-12 text-[#1a1a2e] placeholder-[#1a1a2e]/40 outline-none transition-colors focus:border-[#1BB9EB]"
              />
              <button
                type="button"
                onClick={() => setShowNewPassword(!showNewPassword)}
                className="absolute right-4 top-1/2 -translate-y-1/2 text-[#1a1a2e]/40 hover:text-[#1a1a2e]"
              >
                {showNewPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
              </button>
            </div>
          </div>
          
          {/* Confirm Password */}
          <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:gap-8">
            <label className="w-48 flex-shrink-0 text-xs font-medium uppercase tracking-wider text-[#1a1a2e]/50">
              Confirmar Nueva Contraseña
            </label>
            <div className="relative flex-1">
              <input
                type={showConfirmPassword ? "text" : "password"}
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Confirma tu nueva contraseña"
                className="w-full rounded-xl border border-gray-200 bg-[#f8f8f8] px-4 py-3 pr-12 text-[#1a1a2e] placeholder-[#1a1a2e]/40 outline-none transition-colors focus:border-[#1BB9EB]"
              />
              <button
                type="button"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                className="absolute right-4 top-1/2 -translate-y-1/2 text-[#1a1a2e]/40 hover:text-[#1a1a2e]"
              >
                {showConfirmPassword ? <EyeOff className="h-5 w-5" /> : <Eye className="h-5 w-5" />}
              </button>
            </div>
          </div>
          
          {/* Update Button */}
          <div className="flex justify-end pt-4">
            <button className="group flex items-center gap-2 rounded-lg bg-[#1BB9EB] px-6 py-3 font-bold uppercase tracking-wide text-white transition-all hover:bg-[#0891b2]">
              Actualizar Contraseña
              <ChevronRight className="h-5 w-5 transition-transform group-hover:translate-x-1" />
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
