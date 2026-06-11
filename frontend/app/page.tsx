// app/page.tsx
// The landing page — first thing users see.
// Shows what the product does and has one clear CTA button.
"use client"

import { useRouter } from "next/navigation"
import {
  Sparkles, ArrowRight, Layout,
  Palette, ImageIcon, CheckCircle
} from "lucide-react"

export default function LandingPage() {
  const router = useRouter()

  return (
    <main className="min-h-screen bg-[#0a0a0a] text-white w-full">

      {/* Nav */}
      <nav className="w-full border-b border-[#1e1e1e] px-6 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-[#c9a96e]" />
            <span className="font-semibold text-white text-sm">
              AI Interior Designer
            </span>
          </div>
          <button
            onClick={() => router.push("/design")}
            className="bg-[#c9a96e] text-black text-sm font-medium px-4 py-2 rounded-lg hover:bg-[#a07840] transition-colors"
          >
            Start Designing
          </button>
        </div>
      </nav>

      {/* Hero */}
      <section className="max-w-6xl mx-auto px-6 pt-24 pb-16 text-center">
        <div className="inline-flex items-center gap-2 border border-[#c9a96e]/30 bg-[#c9a96e]/10 text-[#c9a96e] text-xs px-4 py-1.5 rounded-full mb-6">
          <Sparkles className="w-3 h-3" />
          Powered by Llama 3 + Stable Diffusion XL
        </div>

        <h1 className="text-5xl md:text-6xl font-bold leading-tight mb-6">
          Your AI Interior
          <span className="block text-[#c9a96e]">Design Assistant</span>
        </h1>

        <p className="text-gray-400 text-lg max-w-xl mx-auto mb-10 leading-relaxed">
          Describe your room and get a professional design plan with
          furniture layout, color palette, and a concept render in under
          60 seconds.
        </p>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
          <button
            onClick={() => router.push("/design")}
            className="flex items-center gap-2 bg-[#c9a96e] text-black font-semibold px-8 py-3.5 rounded-xl hover:bg-[#a07840] transition-all w-full sm:w-auto justify-center"
          >
            Design My Room
            <ArrowRight className="w-4 h-4" />
          </button>
          <button
            onClick={() =>
              document
                .getElementById("how-it-works")
                ?.scrollIntoView({ behavior: "smooth" })
            }
            className="flex items-center gap-2 bg-[#1e1e1e] text-white font-medium px-8 py-3.5 rounded-xl border border-[#2a2a2a] hover:bg-[#2a2a2a] transition-all w-full sm:w-auto justify-center"
          >
            See How It Works
          </button>
        </div>
      </section>

      {/* Preview Card */}
      <section className="max-w-6xl mx-auto px-6 pb-20">
        <div className="rounded-2xl border border-[#2a2a2a] bg-[#141414] overflow-hidden">
          {/* Window bar */}
          <div className="flex items-center gap-2 px-4 py-3 border-b border-[#2a2a2a] bg-[#0f0f0f]">
            <div className="w-3 h-3 rounded-full bg-red-500/50" />
            <div className="w-3 h-3 rounded-full bg-yellow-500/50" />
            <div className="w-3 h-3 rounded-full bg-green-500/50" />
            <span className="ml-2 text-xs text-gray-600">
              Example Output
            </span>
          </div>
          <div className="grid md:grid-cols-2 min-h-[280px]">
            {/* Plan side */}
            <div className="p-8 border-r border-[#2a2a2a]">
              <div className="text-xs font-semibold uppercase tracking-widest text-[#c9a96e] mb-4">
                Design Plan
              </div>
              <div className="mb-4">
                <p className="text-xs text-gray-500 mb-1">Theme</p>
                <p className="font-semibold text-white">
                  Scandinavian Minimalist
                </p>
              </div>
              <div className="mb-4">
                <p className="text-xs text-gray-500 mb-2">Color Palette</p>
                <div className="flex gap-2">
                  {["#F5F5F0","#C4A265","#4A4A4A","#B8A99A"].map(c => (
                    <div
                      key={c}
                      className="w-8 h-8 rounded-full border border-[#2a2a2a]"
                      style={{ backgroundColor: c }}
                    />
                  ))}
                </div>
              </div>
              <div>
                <p className="text-xs text-gray-500 mb-2">Key Furniture</p>
                <div className="space-y-1.5">
                  {[
                    "3-Seater Sofa — North wall, centered",
                    "Oak Coffee Table — 45cm from sofa",
                    "Slim TV Unit — South wall focal point",
                  ].map(item => (
                    <div key={item} className="flex items-center gap-2 text-sm text-gray-300">
                      <CheckCircle className="w-3.5 h-3.5 text-[#c9a96e] flex-shrink-0" />
                      {item}
                    </div>
                  ))}
                </div>
              </div>
            </div>
            {/* Render side */}
            <div className="flex flex-col items-center justify-center bg-[#0f0f0f] p-8 gap-3">
              <div className="w-16 h-16 rounded-2xl bg-[#1e1e1e] border border-[#2a2a2a] flex items-center justify-center">
                <ImageIcon className="w-7 h-7 text-gray-600" />
              </div>
              <p className="text-sm text-gray-500">AI Concept Render</p>
              <p className="text-xs text-gray-700">
                Generated by Stable Diffusion XL
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section
        id="how-it-works"
        className="max-w-6xl mx-auto px-6 pb-24"
      >
        <h2 className="text-3xl font-bold text-center mb-12">
          How It Works
        </h2>
        <div className="grid md:grid-cols-3 gap-8">
          {[
            {
              icon: Layout,
              step: "01",
              title: "Describe Your Room",
              desc: "Tell us your room type, dimensions, budget, and style preferences using our simple guided form.",
            },
            {
              icon: Sparkles,
              step: "02",
              title: "AI Plans Your Space",
              desc: "Our AI analyzes your constraints and generates a complete design plan with furniture placement, colors, and lighting — with reasoning for every decision.",
            },
            {
              icon: Palette,
              step: "03",
              title: "See Your Design",
              desc: "Receive a concept render alongside a detailed design report. Refine anything by simply asking the AI to change it.",
            },
          ].map(({ icon: Icon, step, title, desc }) => (
            <div key={step} className="relative p-6 rounded-2xl bg-[#141414] border border-[#2a2a2a]">
              <div className="absolute top-4 right-4 text-4xl font-bold text-[#1e1e1e]">
                {step}
              </div>
              <div className="w-11 h-11 rounded-xl bg-[#c9a96e]/10 flex items-center justify-center mb-4">
                <Icon className="w-5 h-5 text-[#c9a96e]" />
              </div>
              <h3 className="font-semibold text-white mb-2">{title}</h3>
              <p className="text-sm text-gray-400 leading-relaxed">{desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="max-w-6xl mx-auto px-6 pb-24">
        <div className="rounded-2xl bg-gradient-to-br from-[#1a1408] to-[#141414] border border-[#c9a96e]/20 p-12 text-center">
          <h2 className="text-3xl font-bold mb-3">
            Ready to Design Your Room?
          </h2>
          <p className="text-gray-400 mb-8">
            Free to use. No account required. Results in under 60 seconds.
          </p>
          <button
            onClick={() => router.push("/design")}
            className="inline-flex items-center gap-2 bg-[#c9a96e] text-black font-semibold px-8 py-3.5 rounded-xl hover:bg-[#a07840] transition-all"
          >
            Start Designing Now
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-[#1e1e1e] py-8 text-center text-xs text-gray-700">
        Built with Next.js · FastAPI · Llama 3 · Stable Diffusion XL
      </footer>
    </main>
  )
}