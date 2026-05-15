import Link from "next/link"
import Image from "next/image"

export default function LandingPage() {
  return (
    <main className="relative min-h-screen w-full overflow-hidden">
      {/* Background Image - contains all the text/graphics as per design */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{ backgroundImage: "url('/images/fondo-landing.jpg')" }}
      />
      
      {/* UTB Logo - Top Left */}
      <div className="absolute top-8 left-8 z-10">
        <Image
          src="/images/utb-logo-original.svg"
          alt="UTB - Universidad Tecnológica de Bolívar"
          width={120}
          height={60}
          className="h-12 w-auto"
        />
      </div>
      
      {/* Left Content Section */}
      <div className="relative z-10 flex min-h-screen flex-col justify-center px-8 lg:px-16">
        <div className="max-w-xl">
          {/* URL Style Text */}
          <p className="mb-4 font-mono text-sm tracking-wider text-[#1a1a2e]/60">
            \_UTB.EDU.CO\SPS_
          </p>
          
          {/* Main Title - Large Green Text */}
          <h1 className="mb-12 text-balance">
            <span className="block text-6xl font-black uppercase tracking-tight text-[#C2F542] lg:text-7xl xl:text-8xl">
              Student
            </span>
            <span className="block text-6xl font-black uppercase tracking-tight text-[#C2F542] lg:text-7xl xl:text-8xl">
              Progress
            </span>
            <span className="block text-6xl font-black uppercase tracking-tight text-[#C2F542] lg:text-7xl xl:text-8xl">
              System
            </span>
          </h1>
          
          {/* Login Button */}
          <Link
            href="/login"
            className="group inline-flex items-center gap-3 border-2 border-[#1a1a2e] bg-[#C2F542] px-8 py-4 text-sm font-bold uppercase tracking-widest text-[#1a1a2e] transition-all hover:bg-[#1a1a2e] hover:text-[#C2F542]"
          >
            Iniciar Sesión
            <svg
              className="h-5 w-5 transition-transform group-hover:translate-x-1"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
            </svg>
          </Link>
        </div>
      </div>
      
      {/* Decorative Circuit Line - Bottom Left */}
      <div className="absolute bottom-32 left-0 z-10">
        <svg width="200" height="60" viewBox="0 0 200 60" fill="none" className="text-[#1a1a2e]/30">
          <path d="M0 30 H150 Q160 30 160 40 V60" stroke="currentColor" strokeWidth="2" fill="none"/>
          <circle cx="150" cy="30" r="4" fill="currentColor"/>
        </svg>
      </div>
    </main>
  )
}
