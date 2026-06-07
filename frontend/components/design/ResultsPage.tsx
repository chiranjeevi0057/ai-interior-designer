// components/design/ResultsPage.tsx
// The main results screen showing the design plan + render.

"use client"

import { useEffect, useState } from "react"
import { useDesignStore } from "@/lib/store"
import { getImageStatus, refineDesign } from "@/lib/api"
import Button from "@/components/ui/Button"
import { Card, CardHeader, CardTitle } from "@/components/ui/Card"
import {
  Sparkles, ImageIcon, RefreshCw,
  Send, RotateCcw, ChevronDown, ChevronUp
} from "lucide-react"

export default function ResultsPage() {
  const {
    designPlan, sessionId, imageStatus, imageUrl,
    setImageStatus, setImageUrl, resetSession,
    conversationHistory, addConversationTurn,
    setDesignPlan, setSessionState,
  } = useDesignStore()

  const [refineInput, setRefineInput] = useState("")
  const [isRefining, setIsRefining] = useState(false)
  const [expandedSection, setExpandedSection] = useState<string | null>("furniture")

  // Poll for image status every 5 seconds
  useEffect(() => {
    if (!sessionId || imageStatus === "complete" || imageStatus === "failed") return

    const interval = setInterval(async () => {
      try {
        const result = await getImageStatus(sessionId)
        setImageStatus(result.image_status)
        if (result.image_url) setImageUrl(result.image_url)
      } catch {
        // Silently fail — keep polling
      }
    }, 5000)

    return () => clearInterval(interval)
  }, [sessionId, imageStatus])

  const handleRefine = async () => {
    if (!refineInput.trim() || !sessionId) return

    setIsRefining(true)
    addConversationTurn("user", refineInput)
    const message = refineInput
    setRefineInput("")

    try {
      const response = await refineDesign(sessionId, message)
      setDesignPlan(response.design_plan)
      setSessionState(response.session_state)
      addConversationTurn(
        "assistant",
        `Updated to version ${response.design_plan.version}. ${
          response.requires_visual_update
            ? "Generating new render..."
            : "Minor update — render unchanged."
        }`
      )
      if (response.requires_visual_update) {
        setImageStatus("generating")
        setImageUrl("")
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

  const toggleSection = (section: string) => {
    setExpandedSection(expandedSection === section ? null : section)
  }

  return (
    <div className="min-h-screen bg-[#0a0a0a]">

      {/* Header */}
      <div className="border-b border-[#1e1e1e] px-6 py-4">
        <div className="mx-auto flex max-w-7xl items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-[#c9a96e]" />
            <span className="font-semibold text-white">AI Interior Designer</span>
            <span className="rounded-full bg-[#c9a96e]/10 px-2 py-0.5 text-xs text-[#c9a96e]">
              v{designPlan.version}
            </span>
          </div>
          <Button variant="secondary" size="sm" onClick={resetSession}>
            <RotateCcw className="mr-1.5 h-3.5 w-3.5" />
            New Design
          </Button>
        </div>
      </div>

      {/* Main Content */}
      <div className="mx-auto max-w-7xl px-4 py-8">
        <div className="grid gap-6 lg:grid-cols-2">

          {/* ── LEFT: Design Plan ── */}
          <div className="space-y-4">

            {/* Room Summary */}
            <Card variant="bordered">
              <div className="mb-1 text-xs font-medium uppercase tracking-wider text-[#c9a96e]">
                Room Summary
              </div>
              <div className="text-lg font-semibold text-white">
                {designPlan.room_type}
              </div>
              <div className="text-sm text-gray-400">
                {designPlan.room_dimensions_summary}
              </div>
              <div className="mt-3 space-y-1">
                {designPlan.spatial_observations.map((obs, i) => (
                  <div key={i} className="flex items-start gap-2 text-xs text-gray-500">
                    <span className="mt-0.5 text-[#c9a96e]">·</span>
                    {obs}
                  </div>
                ))}
              </div>
            </Card>

            {/* Theme */}
            <Card variant="bordered">
              <CardHeader>
                <CardTitle>Recommended Theme</CardTitle>
                <span className="rounded-full border border-[#c9a96e]/30 px-3 py-1 text-xs text-[#c9a96e]">
                  {designPlan.recommended_theme}
                </span>
              </CardHeader>
              <p className="text-sm text-gray-400">{designPlan.theme_rationale}</p>
            </Card>

            {/* Color Palette */}
            <Card variant="bordered">
              <CardHeader>
                <CardTitle>Color Palette</CardTitle>
              </CardHeader>
              <div className="flex gap-3">
                {designPlan.color_palette.map((color) => (
                  <div key={color.hex_code} className="flex-1 text-center">
                    <div
                      className="mx-auto mb-2 h-10 w-10 rounded-full border border-[#2a2a2a]"
                      style={{ backgroundColor: color.hex_code }}
                    />
                    <div className="text-xs text-gray-400">{color.name}</div>
                    <div className="text-xs text-gray-600">{color.hex_code}</div>
                  </div>
                ))}
              </div>
              <p className="mt-3 text-xs text-gray-500">
                {designPlan.color_palette_notes}
              </p>
            </Card>

            {/* Furniture Plan */}
            <Card variant="bordered">
              <button
                onClick={() => toggleSection("furniture")}
                className="flex w-full items-center justify-between"
              >
                <CardTitle>Furniture Plan</CardTitle>
                {expandedSection === "furniture"
                  ? <ChevronUp className="h-4 w-4 text-gray-400" />
                  : <ChevronDown className="h-4 w-4 text-gray-400" />
                }
              </button>
              {expandedSection === "furniture" && (
                <div className="mt-4 space-y-4">
                  {designPlan.furniture_plan.map((item) => (
                    <div
                      key={item.id}
                      className="rounded-lg border border-[#2a2a2a] p-4"
                    >
                      <div className="mb-1 flex items-center justify-between">
                        <span className="font-medium text-white text-sm">
                          {item.name}
                        </span>
                        <span className={`rounded-full px-2 py-0.5 text-xs ${
                          item.priority === "essential"
                            ? "bg-[#c9a96e]/10 text-[#c9a96e]"
                            : "bg-[#2a2a2a] text-gray-400"
                        }`}>
                          {item.priority}
                        </span>
                      </div>
                      <div className="text-xs text-gray-500 mb-2">
                        {item.recommended_dimensions}
                      </div>
                      <div className="text-xs text-gray-400">
                        📍 {item.placement}
                      </div>
                      <div className="mt-1 text-xs text-gray-600 italic">
                        {item.placement_reasoning}
                      </div>
                      <div className="mt-2 text-xs text-[#c9a96e]">
                        ₹{item.estimated_cost_range}
                      </div>
                    </div>
                  ))}
                  <p className="text-xs text-gray-500">
                    {designPlan.traffic_flow_notes}
                  </p>
                </div>
              )}
            </Card>

            {/* Lighting */}
            <Card variant="bordered">
              <button
                onClick={() => toggleSection("lighting")}
                className="flex w-full items-center justify-between"
              >
                <CardTitle>Lighting Plan</CardTitle>
                {expandedSection === "lighting"
                  ? <ChevronUp className="h-4 w-4 text-gray-400" />
                  : <ChevronDown className="h-4 w-4 text-gray-400" />
                }
              </button>
              {expandedSection === "lighting" && (
                <div className="mt-4 space-y-3">
                  {designPlan.lighting_plan.map((light, i) => (
                    <div key={i} className="rounded-lg bg-[#0f0f0f] p-3">
                      <div className="mb-1 flex items-center gap-2">
                        <span className="rounded-full bg-[#c9a96e]/10 px-2 py-0.5 text-xs text-[#c9a96e]">
                          {light.type}
                        </span>
                        <span className="text-sm text-white">
                          {light.description}
                        </span>
                      </div>
                      <div className="text-xs text-gray-500">
                        📍 {light.placement}
                      </div>
                      <div className="mt-1 text-xs text-gray-600 italic">
                        {light.reasoning}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </Card>

            {/* Budget */}
            <Card variant="bordered">
              <CardHeader>
                <CardTitle>Budget Estimate</CardTitle>
                <span className="text-sm font-semibold text-[#c9a96e]">
                  ₹{designPlan.estimated_total_range}
                </span>
              </CardHeader>
              <p className="text-sm text-gray-400">{designPlan.budget_notes}</p>
            </Card>
          </div>

          {/* ── RIGHT: Render + Chat ── */}
          <div className="space-y-4">

            {/* Concept Render */}
            <Card variant="bordered" className="overflow-hidden p-0">
              <div className="border-b border-[#2a2a2a] px-4 py-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium text-white">
                    Concept Render
                  </span>
                  {imageStatus === "complete" && (
                    <Button variant="ghost" size="sm">
                      <RefreshCw className="mr-1 h-3.5 w-3.5" />
                      Regenerate
                    </Button>
                  )}
                </div>
              </div>

              <div className="aspect-[4/3] relative bg-[#0f0f0f]">
                {imageStatus === "complete" && imageUrl ? (
                  <img
                    src={imageUrl}
                    alt="AI-generated concept render"
                    className="h-full w-full object-cover fade-in"
                  />
                ) : (
                  <div className="flex h-full flex-col items-center justify-center gap-3">
                    {imageStatus === "generating" || imageStatus === "pending" ? (
                      <>
                        <div className="h-10 w-10 rounded-full border-2 border-[#c9a96e]/20 border-t-[#c9a96e] animate-spin" />
                        <p className="text-sm text-gray-400">
                          Generating your concept render...
                        </p>
                        <p className="text-xs text-gray-600">
                          This may take up to 60 seconds
                        </p>
                      </>
                    ) : imageStatus === "failed" ? (
                      <>
                        <ImageIcon className="h-10 w-10 text-gray-600" />
                        <p className="text-sm text-gray-500">
                          Render unavailable
                        </p>
                        <Button variant="secondary" size="sm">
                          Retry
                        </Button>
                      </>
                    ) : (
                      <>
                        <ImageIcon className="h-10 w-10 text-gray-600" />
                        <p className="text-sm text-gray-500">
                          Preparing render...
                        </p>
                      </>
                    )}
                  </div>
                )}
              </div>

              {imageStatus === "complete" && (
                <div className="px-4 py-2 text-xs text-gray-600">
                  AI-generated concept render — for visual reference only
                </div>
              )}
            </Card>

            {/* Refinement Chat */}
            <Card variant="bordered">
              <CardHeader>
                <CardTitle>Refine Your Design</CardTitle>
              </CardHeader>

              {/* Quick suggestions */}
              <div className="mb-3 flex flex-wrap gap-2">
                {[
                  "Make it more minimalist",
                  "Change the color palette",
                  "Tighter budget",
                  "Remove the rug",
                ].map((suggestion) => (
                  <button
                    key={suggestion}
                    onClick={() => setRefineInput(suggestion)}
                    className="rounded-full border border-[#2a2a2a] px-3 py-1 text-xs text-gray-400 hover:border-[#c9a96e] hover:text-[#c9a96e] transition-colors"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>

              {/* Conversation History */}
              {conversationHistory.length > 0 && (
                <div className="mb-3 max-h-40 overflow-y-auto space-y-2">
                  {conversationHistory.slice(-6).map((turn, i) => (
                    <div
                      key={i}
                      className={`rounded-lg px-3 py-2 text-xs ${
                        turn.role === "user"
                          ? "bg-[#c9a96e]/10 text-[#c9a96e] ml-4"
                          : "bg-[#1e1e1e] text-gray-300 mr-4"
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
                  onChange={(e) => setRefineInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && !e.shiftKey) {
                      e.preventDefault()
                      handleRefine()
                    }
                  }}
                  placeholder="Ask me to change anything..."
                  className="flex-1 rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2.5 text-sm text-white placeholder-gray-600 focus:border-[#c9a96e] focus:outline-none"
                />
                <Button
                  onClick={handleRefine}
                  isLoading={isRefining}
                  disabled={!refineInput.trim()}
                  size="md"
                  className="flex-shrink-0"
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
            </Card>

            {/* Design Principles */}
            <Card variant="bordered">
              <CardHeader>
                <CardTitle>Design Principles Applied</CardTitle>
              </CardHeader>
              <div className="space-y-2">
                {designPlan.key_design_principles.map((principle, i) => (
                  <div key={i} className="flex items-start gap-2 text-sm text-gray-400">
                    <span className="mt-1 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-[#c9a96e]" />
                    {principle}
                  </div>
                ))}
              </div>

              {designPlan.design_warnings.length > 0 && (
                <div className="mt-4 rounded-lg border border-yellow-500/20 bg-yellow-500/5 p-3">
                  <div className="text-xs font-medium text-yellow-500 mb-1">
                    Design Notes
                  </div>
                  {designPlan.design_warnings.map((warning, i) => (
                    <div key={i} className="text-xs text-yellow-400/70">
                      {warning}
                    </div>
                  ))}
                </div>
              )}
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}