// components/design/ResultsPage.tsx
// The main results screen showing the design plan + render.

"use client"

import { useEffect, useState } from "react"
import FurniturePanel from "@/components/design/FurniturePanel"
import { useDesignStore } from "@/lib/store"
import { getImageStatus, refineDesign } from "@/lib/api"
import {
  Sparkles, ImageIcon, RefreshCw, Send,
  RotateCcw, ChevronDown, ChevronUp
} from "lucide-react"

export default function ResultsPage() {
  const {
    designPlan, sessionId, imageStatus, imageUrl,
    setImageStatus, setImageUrl, resetSession,
    conversationHistory, addConversationTurn,
    setDesignPlan, setSessionState,
  } = useDesignStore()

  const [refineInput, setRefineInput]   = useState("")
  const [isRefining, setIsRefining]     = useState(false)
  const [openSection, setOpenSection]   = useState<string>("furniture")

  /* Poll image status */
  useEffect(() => {
    if (!sessionId || imageStatus === "complete" || imageStatus === "failed") return
    const iv = setInterval(async () => {
      try {
        const r = await getImageStatus(sessionId)
        setImageStatus(r.image_status)
        if (r.image_url) setImageUrl(r.image_url)
      } catch { /* keep polling */ }
    }, 5000)
    return () => clearInterval(iv)
  }, [sessionId, imageStatus])

  const handleRefine = async () => {
  if (!refineInput.trim() || !sessionId) return

  setIsRefining(true)
  addConversationTurn("user", refineInput)
  const msg = refineInput
  setRefineInput("")

  try {
    const res = await refineDesign(sessionId, msg)
    setDesignPlan(res.design_plan)
    setSessionState(res.session_state)

    addConversationTurn(
      "assistant",
      `Design updated to version ${res.design_plan.version}. ${
        res.requires_visual_update
          ? "Generating new render..."
          : "Text updated — render unchanged."
      }`
    )

    // Reset image if regeneration was triggered
    if (res.requires_visual_update) {
      setImageUrl("")
      setImageStatus("generating")
    }

  } catch {
    addConversationTurn(
      "assistant",
      "Sorry, I had trouble updating the design. Please try again."
    )
  } finally {
    setIsRefining(false)
  }
}

  if (!designPlan) return null

  const toggle = (s: string) => setOpenSection(openSection === s ? "" : s)

  return (
    <div className="min-h-screen bg-[#0a0a0a] text-white">

      {/* Top bar */}
      <div className="w-full border-b border-[#1e1e1e] px-6 py-4 sticky top-0 bg-[#0a0a0a] z-10">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-[#c9a96e]" />
            <span className="font-semibold text-sm">AI Interior Designer</span>
            <span className="text-xs px-2 py-0.5 rounded-full bg-[#c9a96e]/10 text-[#c9a96e]">
              v{designPlan.version}
            </span>
          </div>
          <button
            onClick={resetSession}
            className="flex items-center gap-1.5 text-sm text-gray-400 hover:text-white border border-[#2a2a2a] px-3 py-1.5 rounded-lg hover:border-[#3a3a3a] transition-all"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            New Design
          </button>
        </div>
      </div>

      {/* Body */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-2 gap-6 items-start">

          {/* ── LEFT: Plan ── */}
          <div className="space-y-4">

            {/* Room summary */}
            <div className="bg-[#141414] border border-[#2a2a2a] rounded-2xl p-6">
              <p className="text-xs font-semibold uppercase tracking-widest text-[#c9a96e] mb-2">
                Room Summary
              </p>
              <p className="text-xl font-bold text-white">{designPlan.room_type}</p>
              <p className="text-sm text-gray-400 mt-1">{designPlan.room_dimensions_summary}</p>
              <div className="mt-3 space-y-1">
                {designPlan.spatial_observations.map((o, i) => (
                  <p key={i} className="text-xs text-gray-600">· {o}</p>
                ))}
              </div>
            </div>

            {/* Theme */}
            <div className="bg-[#141414] border border-[#2a2a2a] rounded-2xl p-6">
              <div className="flex items-center justify-between mb-3">
                <p className="font-semibold text-white">Recommended Theme</p>
                <span className="text-xs px-3 py-1 rounded-full border border-[#c9a96e]/30 text-[#c9a96e]">
                  {designPlan.recommended_theme}
                </span>
              </div>
              <p className="text-sm text-gray-400 leading-relaxed">{designPlan.theme_rationale}</p>
            </div>

            {/* Palette */}
            <div className="bg-[#141414] border border-[#2a2a2a] rounded-2xl p-6">
              <p className="font-semibold text-white mb-4">Color Palette</p>
              <div className="flex gap-4">
                {designPlan.color_palette.map(c => (
                  <div key={c.hex_code} className="flex-1 text-center">
                    <div
                      className="w-10 h-10 rounded-full mx-auto mb-2 border border-[#2a2a2a]"
                      style={{ backgroundColor: c.hex_code }}
                    />
                    <p className="text-xs text-gray-300 font-medium">{c.name}</p>
                    <p className="text-xs text-gray-600">{c.hex_code}</p>
                  </div>
                ))}
              </div>
              <p className="text-xs text-gray-500 mt-4">{designPlan.color_palette_notes}</p>
            </div>

            {/* Furniture */}
            <div className="bg-[#141414] border border-[#2a2a2a] rounded-2xl overflow-hidden">
              <button
                onClick={() => toggle("furniture")}
                className="w-full flex items-center justify-between p-6"
              >
                <span className="font-semibold text-white">Furniture Plan</span>
                {openSection === "furniture"
                  ? <ChevronUp className="w-4 h-4 text-gray-400" />
                  : <ChevronDown className="w-4 h-4 text-gray-400" />}
              </button>
              {openSection === "furniture" && (
                <div className="px-6 pb-6 space-y-3 border-t border-[#2a2a2a] pt-4">
                  {designPlan.furniture_plan.map(item => (
                    <div key={item.id} className="bg-[#0f0f0f] rounded-xl p-4 border border-[#2a2a2a]">
                      <div className="flex items-center justify-between mb-1">
                        <span className="font-medium text-white text-sm">{item.name}</span>
                        <span className={`text-xs px-2 py-0.5 rounded-full ${
                          item.priority === "essential"
                            ? "bg-[#c9a96e]/10 text-[#c9a96e]"
                            : "bg-[#2a2a2a] text-gray-400"
                        }`}>
                          {item.priority}
                        </span>
                      </div>
                      <p className="text-xs text-gray-600 mb-2">{item.recommended_dimensions}</p>
                      <p className="text-xs text-gray-400">📍 {item.placement}</p>
                      <p className="text-xs text-gray-600 italic mt-1">{item.placement_reasoning}</p>
                      <p className="text-xs text-[#c9a96e] mt-2 font-medium">₹{item.estimated_cost_range}</p>
                    </div>
                  ))}
                  <p className="text-xs text-gray-500 pt-1">{designPlan.traffic_flow_notes}</p>
                </div>
              )}
            </div>

            {/* Lighting */}
            <div className="bg-[#141414] border border-[#2a2a2a] rounded-2xl overflow-hidden">
              <button
                onClick={() => toggle("lighting")}
                className="w-full flex items-center justify-between p-6"
              >
                <span className="font-semibold text-white">Lighting Plan</span>
                {openSection === "lighting"
                  ? <ChevronUp className="w-4 h-4 text-gray-400" />
                  : <ChevronDown className="w-4 h-4 text-gray-400" />}
              </button>
              {openSection === "lighting" && (
                <div className="px-6 pb-6 space-y-3 border-t border-[#2a2a2a] pt-4">
                  {designPlan.lighting_plan.map((light, i) => (
                    <div key={i} className="bg-[#0f0f0f] rounded-xl p-4">
                      <div className="flex items-center gap-2 mb-2">
                        <span className="text-xs px-2 py-0.5 rounded-full bg-[#c9a96e]/10 text-[#c9a96e]">
                          {light.type}
                        </span>
                        <span className="text-sm text-white">{light.description}</span>
                      </div>
                      <p className="text-xs text-gray-500">📍 {light.placement}</p>
                      <p className="text-xs text-gray-600 italic mt-1">{light.reasoning}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Budget */}
            <div className="bg-[#141414] border border-[#2a2a2a] rounded-2xl p-6">
              <div className="flex items-center justify-between mb-2">
                <p className="font-semibold text-white">Budget Estimate</p>
                <span className="text-lg font-bold text-[#c9a96e]">
                  ₹{designPlan.estimated_total_range}
                </span>
              </div>
              <p className="text-sm text-gray-400">{designPlan.budget_notes}</p>
            </div>
          </div>

          {/* ── RIGHT: Render + Chat ── */}
          <div className="space-y-4 lg:sticky lg:top-24">

            {/* Render */}
            <div className="bg-[#141414] border border-[#2a2a2a] rounded-2xl overflow-hidden">
              <div className="flex items-center justify-between px-5 py-3.5 border-b border-[#2a2a2a]">
                <span className="text-sm font-medium text-white">Concept Render</span>
                {imageStatus === "complete" && (
                  <button className="flex items-center gap-1.5 text-xs text-gray-400 hover:text-white transition-colors">
                    <RefreshCw className="w-3.5 h-3.5" />
                    Regenerate
                  </button>
                )}
              </div>

              <div className="aspect-video bg-[#0f0f0f] relative flex items-center justify-center">
                {imageStatus === "complete" && imageUrl ? (
                  <img
                    src={imageUrl}
                    alt="Concept render"
                    className="w-full h-full object-cover fade-in"
                  />
                ) : (
                  <div className="text-center space-y-3">
                    {(imageStatus === "generating" || imageStatus === "pending") ? (
                      <>
                      <div className="w-10 h-10 border-2 border-[#c9a96e]/20 border-t-[#c9a96e] rounded-full animate-spin mx-auto" />
                      <p className="text-sm text-gray-400 mt-3">
                        Generating your concept render...
                      </p>
                      <p className="text-xs text-gray-600 mt-1">
                        Stable Diffusion XL is painting your room
                      </p>
                      <p className="text-xs text-gray-700 mt-1">
                        This may take 30–90 seconds
                      </p>
                      </>
                    ) : imageStatus === "failed" ? (
                      <>
                        <ImageIcon className="w-10 h-10 text-gray-700 mx-auto" />
                        <p className="text-sm text-gray-500">Render unavailable</p>
                      </>
                    ) : (
                      <>
                        <ImageIcon className="w-10 h-10 text-gray-700 mx-auto" />
                        <p className="text-sm text-gray-500">Preparing render...</p>
                      </>
                    )}
                  </div>
                )}
              </div>

              {imageStatus === "complete" && (
                <p className="px-5 py-2 text-xs text-gray-700 border-t border-[#2a2a2a]">
                  AI-generated concept render — for visual reference only
                </p>
              )}
            </div>

            {/* Furniture Recommendations */}
            {sessionId && (
              <FurniturePanel sessionId={sessionId} />
            )}

            {/* Refinement chat */}
            <div className="bg-[#141414] border border-[#2a2a2a] rounded-2xl p-5">
              <p className="font-semibold text-white mb-4">Refine Your Design</p>

              {/* Suggestions */}
              <div className="flex flex-wrap gap-2 mb-4">
                {["Make it more minimalist","Change the color palette","Tighter budget","Remove the rug"].map(s => (
                  <button
                    key={s}
                    onClick={() => setRefineInput(s)}
                    className="text-xs px-3 py-1.5 rounded-full border border-[#2a2a2a] text-gray-400 hover:border-[#c9a96e] hover:text-[#c9a96e] transition-colors"
                  >
                    {s}
                  </button>
                ))}
              </div>

              {/* History */}
              {conversationHistory.length > 0 && (
                <div className="max-h-40 overflow-y-auto space-y-2 mb-4">
                  {conversationHistory.slice(-6).map((turn, i) => (
                    <div
                      key={i}
                      className={`text-xs rounded-xl px-3 py-2 ${
                        turn.role === "user"
                          ? "bg-[#c9a96e]/10 text-[#c9a96e] ml-6"
                          : "bg-[#1e1e1e] text-gray-300 mr-6"
                      }`}
                    >
                      {turn.content}
                    </div>
                  ))}
                </div>
              )}

              {/* Input */}
              <div className="flex gap-2">
                <input
                  type="text"
                  value={refineInput}
                  onChange={e => setRefineInput(e.target.value)}
                  onKeyDown={e => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleRefine() } }}
                  placeholder="Ask me to change anything..."
                  className="flex-1 bg-[#0f0f0f] border border-[#2a2a2a] rounded-xl px-3 py-2.5 text-sm text-white placeholder-gray-700 focus:border-[#c9a96e] focus:outline-none transition-colors"
                />
                <button
                  onClick={handleRefine}
                  disabled={!refineInput.trim() || isRefining}
                  className="px-4 py-2.5 rounded-xl bg-[#c9a96e] text-black hover:bg-[#a07840] disabled:opacity-40 disabled:cursor-not-allowed transition-all flex-shrink-0"
                >
                  {isRefining
                    ? <div className="w-4 h-4 border-2 border-black/30 border-t-black rounded-full animate-spin" />
                    : <Send className="w-4 h-4" />
                  }
                </button>
              </div>
            </div>

            {/* Design principles */}
            <div className="bg-[#141414] border border-[#2a2a2a] rounded-2xl p-5">
              <p className="font-semibold text-white mb-3">Design Principles Applied</p>
              <div className="space-y-2">
                {designPlan.key_design_principles.map((p, i) => (
                  <div key={i} className="flex items-start gap-2 text-sm text-gray-400">
                    <span className="w-1.5 h-1.5 rounded-full bg-[#c9a96e] flex-shrink-0 mt-1.5" />
                    {p}
                  </div>
                ))}
              </div>
              {designPlan.design_warnings.length > 0 && (
                <div className="mt-4 border border-yellow-500/20 bg-yellow-500/5 rounded-xl p-3">
                  <p className="text-xs font-semibold text-yellow-500 mb-1">Notes</p>
                  {designPlan.design_warnings.map((w, i) => (
                    <p key={i} className="text-xs text-yellow-400/70">{w}</p>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}