// app/page.tsx
// The landing page — first thing users see.
// Shows what the product does and has one clear CTA button.

"use client"

import { useRouter } from "next/navigation"
import Button from "@/components/ui/Button"
import {
  Sparkles,
  Layout,
  Palette,
  ImageIcon,
  ArrowRight,
  CheckCircle,
} from "lucide-react"

export default function LandingPage() {
  const router = useRouter()

  return (
    <main className="min-h-screen bg-[#0a0a0a] text-white">

      {/* ── Navigation ── */}
      <nav className="border-b border-[#1e1e1e] px-6 py-4">
        <div className="mx-auto flex max-w-6xl items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-[#c9a96e]" />
            <span className="font-semibold text-white">
              AI Interior Designer
            </span>
          </div>
          <Button
            size="sm"
            onClick={() => router.push("/design")}
          >
            Start Designing
          </Button>
        </div>
      </nav>

      {/* ── Hero Section ── */}
      <section className="mx-auto max-w-6xl px-6 py-24 text-center">
        <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-[#c9a96e]/30 bg-[#c9a96e]/10 px-4 py-1.5 text-sm text-[#c9a96e]">
          <Sparkles className="h-3.5 w-3.5" />
          Powered by Llama 3 + Stable Diffusion XL
        </div>

        <h1 className="mb-6 text-5xl font-bold leading-tight tracking-tight md:text-6xl">
          Your AI Interior
          <span className="block text-[#c9a96e]">Design Assistant</span>
        </h1>

        <p className="mx-auto mb-10 max-w-2xl text-lg text-gray-400">
          Describe your room. Get a professional design plan with furniture
          layout, color palette, lighting recommendations, and a concept
          render — all in under 60 seconds.
        </p>

        <div className="flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
          <Button
            size="lg"
            onClick={() => router.push("/design")}
            className="group w-full sm:w-auto"
          >
            Design My Room
            <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
          </Button>
          <Button
            size="lg"
            variant="secondary"
            onClick={() =>
              document
                .getElementById("how-it-works")
                ?.scrollIntoView({ behavior: "smooth" })
            }
            className="w-full sm:w-auto"
          >
            See How It Works
          </Button>
        </div>
      </section>

      {/* ── Example Output Preview ── */}
      <section className="mx-auto max-w-6xl px-6 pb-20">
        <div className="overflow-hidden rounded-2xl border border-[#2a2a2a] bg-[#141414]">
          <div className="border-b border-[#2a2a2a] px-6 py-3">
            <div className="flex items-center gap-2">
              <div className="h-3 w-3 rounded-full bg-red-500/60" />
              <div className="h-3 w-3 rounded-full bg-yellow-500/60" />
              <div className="h-3 w-3 rounded-full bg-green-500/60" />
              <span className="ml-2 text-xs text-gray-500">
                AI Interior Designer — Example Output
              </span>
            </div>
          </div>
          <div className="grid md:grid-cols-2">
            {/* Left: Sample plan text */}
            <div className="border-r border-[#2a2a2a] p-8">
              <div className="mb-3 text-xs font-medium uppercase tracking-wider text-[#c9a96e]">
                Design Plan
              </div>
              <div className="mb-6">
                <div className="mb-1 text-xs text-gray-500">Theme</div>
                <div className="font-medium text-white">
                  Scandinavian Minimalist
                </div>
              </div>
              <div className="mb-6">
                <div className="mb-2 text-xs text-gray-500">
                  Color Palette
                </div>
                <div className="flex gap-2">
                  {["#F5F5F0", "#C4A265", "#4A4A4A", "#B8A99A"].map(
                    (color) => (
                      <div
                        key={color}
                        className="h-8 w-8 rounded-full border border-[#2a2a2a]"
                        style={{ backgroundColor: color }}
                      />
                    )
                  )}
                </div>
              </div>
              <div>
                <div className="mb-2 text-xs text-gray-500">
                  Key Furniture
                </div>
                <div className="space-y-2">
                  {[
                    "3-Seater Linen Sofa — North wall, centered",
                    "Oak Coffee Table — 45cm from sofa",
                    "Slim TV Unit — South wall focal point",
                  ].map((item) => (
                    <div
                      key={item}
                      className="flex items-start gap-2 text-sm text-gray-300"
                    >
                      <CheckCircle className="mt-0.5 h-3.5 w-3.5 flex-shrink-0 text-[#c9a96e]" />
                      {item}
                    </div>
                  ))}
                </div>
              </div>
            </div>
            {/* Right: Sample render placeholder */}
            <div className="flex items-center justify-center bg-[#0f0f0f] p-8">
              <div className="text-center">
                <ImageIcon className="mx-auto mb-3 h-12 w-12 text-gray-600" />
                <div className="text-sm text-gray-500">
                  AI Concept Render
                </div>
                <div className="mt-1 text-xs text-gray-600">
                  Generated by Stable Diffusion XL
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── How It Works ── */}
      <section
        id="how-it-works"
        className="mx-auto max-w-6xl px-6 pb-24"
      >
        <h2 className="mb-12 text-center text-3xl font-bold">
          How It Works
        </h2>
        <div className="grid gap-8 md:grid-cols-3">
          {[
            {
              icon: Layout,
              step: "01",
              title: "Describe Your Room",
              description:
                "Tell us your room type, dimensions, budget, and style " +
                "preferences using our simple guided form.",
            },
            {
              icon: Sparkles,
              step: "02",
              title: "AI Plans Your Space",
              description:
                "Our AI analyzes your constraints and generates a " +
                "complete design plan with furniture placement, colors, " +
                "and lighting — with reasoning for every decision.",
            },
            {
              icon: Palette,
              step: "03",
              title: "See Your Design",
              description:
                "Receive a concept render of your room alongside a " +
                "detailed design report. Refine anything by simply " +
                "asking the AI to change it.",
            },
          ].map(({ icon: Icon, step, title, description }) => (
            <div key={step} className="relative">
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-[#c9a96e]/10">
                <Icon className="h-6 w-6 text-[#c9a96e]" />
              </div>
              <div className="absolute right-0 top-0 text-5xl font-bold text-[#1e1e1e]">
                {step}
              </div>
              <h3 className="mb-2 text-lg font-semibold">{title}</h3>
              <p className="text-sm text-gray-400">{description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── CTA Banner ── */}
      <section className="mx-auto max-w-6xl px-6 pb-24">
        <div className="rounded-2xl bg-gradient-to-r from-[#c9a96e]/20 to-[#a07840]/20 border border-[#c9a96e]/30 p-12 text-center">
          <h2 className="mb-4 text-3xl font-bold">
            Ready to Design Your Room?
          </h2>
          <p className="mb-8 text-gray-400">
            Free to use. No account required. Results in under 60 seconds.
          </p>
          <Button size="lg" onClick={() => router.push("/design")}>
            Start Designing Now
            <ArrowRight className="ml-2 h-4 w-4" />
          </Button>
        </div>
      </section>

      {/* ── Footer ── */}
      <footer className="border-t border-[#1e1e1e] px-6 py-8 text-center text-sm text-gray-600">
        Built with Next.js · FastAPI · Llama 3 · Stable Diffusion XL
      </footer>
    </main>
  )
}