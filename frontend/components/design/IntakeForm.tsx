// components/design/IntakeForm.tsx
// The 4-step room intake form.
// Collects all the information the AI needs to design the room.

"use client"

import { useState } from "react"
import { useDesignStore } from "@/lib/store"
import { generateDesign, IntakePayload } from "@/lib/api"
import {
  ChevronLeft, ChevronRight,
  Sparkles, Home, Palette, DollarSign, CheckCircle
} from "lucide-react"

const ROOM_TYPES = [
  "Living Room","Bedroom","Home Office",
  "Dining Room","Studio Apartment",
]

const STYLE_OPTIONS = [
  { value: "Minimalist",        desc: "Clean, simple, functional" },
  { value: "Scandinavian",      desc: "Warm, natural, cozy" },
  { value: "Industrial",        desc: "Raw, urban, edgy" },
  { value: "Bohemian",          desc: "Eclectic, colorful, free-spirited" },
  { value: "Contemporary",      desc: "Modern, sleek, current" },
  { value: "Traditional",       desc: "Classic, timeless, elegant" },
  { value: "Mid-Century Modern",desc: "Retro, organic, iconic" },
  { value: "Japandi",           desc: "Japanese-Scandinavian fusion" },
]

const COLOR_MOODS = [
  { value: "Warm and Cozy",    color: "#c9a96e" },
  { value: "Cool and Calm",    color: "#6e9ac9" },
  { value: "Bold and Vibrant", color: "#c96e6e" },
  { value: "Neutral and Clean",color: "#a0a0a0" },
]

const LIGHT_LEVELS = ["Bright","Moderate","Low"]

const BUDGET_RANGES = [
  { value: "Under 50000",        label: "Under ₹50K",    desc: "Budget friendly" },
  { value: "50000 to 150000",    label: "₹50K – ₹1.5L",  desc: "Mid range" },
  { value: "150000 to 400000",   label: "₹1.5L – ₹4L",   desc: "Premium" },
  { value: "Above 400000",       label: "Above ₹4L",     desc: "Luxury" },
]

const MUST_HAVE_OPTIONS: Record<string, string[]> = {
  "Living Room":      ["Sofa","Coffee Table","TV Unit","Bookshelf","Armchair"],
  "Bedroom":          ["Bed","Wardrobe","Study Desk","Side Tables","Dresser"],
  "Home Office":      ["Desk","Office Chair","Bookshelf","Filing Cabinet"],
  "Dining Room":      ["Dining Table","Dining Chairs","Sideboard","Display Cabinet"],
  "Studio Apartment": ["Sofa Bed","Kitchen Island","Wardrobe","Study Desk"],
}

const STEP_LABELS = ["Room Basics","Style & Mood","Constraints","Review"]

export default function IntakeForm() {
  const {
    currentStep, intake, updateIntake, setCurrentStep,
    setDesignPlan, setSessionId, setSessionState,
    setLoading, setError,
  } = useDesignStore()

  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleNext = () => {
    if (currentStep < 4) setCurrentStep(currentStep + 1)
  }
  const handleBack = () => {
    if (currentStep > 1) setCurrentStep(currentStep - 1)
  }

  const handleSubmit = async () => {
    setIsSubmitting(true)
    setSessionState("planning")
    setLoading(true)
    setError(null)
    try {
      const response = await generateDesign(intake as IntakePayload)
      setSessionId(response.session_id)
      setDesignPlan(response.design_plan)
      setSessionState(response.session_state)
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to generate design.")
      setSessionState("idle")
    } finally {
      setIsSubmitting(false)
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-[#0a0a0a] flex flex-col items-center justify-start px-4 py-12">
      <div className="w-full max-w-2xl">

        {/* Header */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 text-[#c9a96e] mb-3">
            <Sparkles className="w-4 h-4" />
            <span className="text-sm font-medium">AI Interior Designer</span>
          </div>
          <h1 className="text-3xl font-bold text-white">
            Tell us about your room
          </h1>
          <p className="text-gray-500 text-sm mt-2">
            Step {currentStep} of 4 — {STEP_LABELS[currentStep - 1]}
          </p>
        </div>

        {/* Progress */}
        <div className="flex gap-1.5 mb-8">
          {[1,2,3,4].map(s => (
            <div
              key={s}
              className={`h-1 flex-1 rounded-full transition-all duration-300 ${
                s <= currentStep ? "bg-[#c9a96e]" : "bg-[#2a2a2a]"
              }`}
            />
          ))}
        </div>

        {/* Card */}
        <div className="w-full bg-[#141414] border border-[#2a2a2a] rounded-2xl p-8">

          {/* STEP 1 */}
          {currentStep === 1 && (
            <div className="space-y-7">
              <h2 className="text-xl font-semibold text-white">Room Basics</h2>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-3">
                  Room Type
                </label>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                  {ROOM_TYPES.map(type => (
                    <button
                      key={type}
                      onClick={() => updateIntake({ room_type: type as IntakePayload["room_type"] })}
                      className={`p-3 rounded-xl border text-sm text-left transition-all ${
                        intake.room_type === type
                          ? "border-[#c9a96e] bg-[#c9a96e]/10 text-[#c9a96e]"
                          : "border-[#2a2a2a] text-gray-400 hover:border-[#3a3a3a] hover:text-gray-300"
                      }`}
                    >
                      {type}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-3">
                  Room Dimensions (in feet)
                </label>
                <div className="grid grid-cols-3 gap-3">
                  {(["length","width","ceiling_height"] as const).map(field => (
                    <div key={field}>
                      <label className="block text-xs text-gray-500 mb-1.5 capitalize">
                        {field.replace("_"," ")}
                      </label>
                      <input
                        type="number"
                        placeholder="ft"
                        value={intake[field] || ""}
                        onChange={e => updateIntake({ [field]: parseFloat(e.target.value) })}
                        className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded-xl px-3 py-2.5 text-sm text-white placeholder-gray-700 focus:border-[#c9a96e] focus:outline-none transition-colors"
                      />
                    </div>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-3">
                  Natural Light Level
                </label>
                <div className="grid grid-cols-3 gap-2">
                  {LIGHT_LEVELS.map(level => (
                    <button
                      key={level}
                      onClick={() => updateIntake({ light_level: level as IntakePayload["light_level"] })}
                      className={`p-3 rounded-xl border text-sm transition-all ${
                        intake.light_level === level
                          ? "border-[#c9a96e] bg-[#c9a96e]/10 text-[#c9a96e]"
                          : "border-[#2a2a2a] text-gray-400 hover:border-[#3a3a3a]"
                      }`}
                    >
                      {level}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* STEP 2 */}
          {currentStep === 2 && (
            <div className="space-y-7">
              <h2 className="text-xl font-semibold text-white">Style & Mood</h2>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-3">
                  Interior Style
                </label>
                <div className="grid grid-cols-2 gap-2">
                  {STYLE_OPTIONS.map(({ value, desc }) => (
                    <button
                      key={value}
                      onClick={() => updateIntake({ style_preference: value as IntakePayload["style_preference"] })}
                      className={`p-3 rounded-xl border text-left transition-all ${
                        intake.style_preference === value
                          ? "border-[#c9a96e] bg-[#c9a96e]/10"
                          : "border-[#2a2a2a] hover:border-[#3a3a3a]"
                      }`}
                    >
                      <div className={`text-sm font-medium ${intake.style_preference === value ? "text-[#c9a96e]" : "text-white"}`}>
                        {value}
                      </div>
                      <div className="text-xs text-gray-500 mt-0.5">{desc}</div>
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-3">
                  Color Mood
                </label>
                <div className="grid grid-cols-2 gap-2">
                  {COLOR_MOODS.map(({ value, color }) => (
                    <button
                      key={value}
                      onClick={() => updateIntake({ color_mood: value as IntakePayload["color_mood"] })}
                      className={`flex items-center gap-3 p-3 rounded-xl border text-left transition-all ${
                        intake.color_mood === value
                          ? "border-[#c9a96e] bg-[#c9a96e]/10"
                          : "border-[#2a2a2a] hover:border-[#3a3a3a]"
                      }`}
                    >
                      <div className="w-6 h-6 rounded-full flex-shrink-0" style={{ backgroundColor: color }} />
                      <span className={`text-sm ${intake.color_mood === value ? "text-[#c9a96e]" : "text-gray-300"}`}>
                        {value}
                      </span>
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* STEP 3 */}
          {currentStep === 3 && (
            <div className="space-y-7">
              <h2 className="text-xl font-semibold text-white">Constraints & Preferences</h2>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-3">
                  Budget Range
                </label>
                <div className="grid grid-cols-2 gap-2">
                  {BUDGET_RANGES.map(({ value, label, desc }) => (
                    <button
                      key={value}
                      onClick={() => updateIntake({ budget_range: value as IntakePayload["budget_range"] })}
                      className={`p-3 rounded-xl border text-left transition-all ${
                        intake.budget_range === value
                          ? "border-[#c9a96e] bg-[#c9a96e]/10"
                          : "border-[#2a2a2a] hover:border-[#3a3a3a]"
                      }`}
                    >
                      <div className={`text-sm font-medium ${intake.budget_range === value ? "text-[#c9a96e]" : "text-white"}`}>
                        {label}
                      </div>
                      <div className="text-xs text-gray-500 mt-0.5">{desc}</div>
                    </button>
                  ))}
                </div>
              </div>

              {intake.room_type && (
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-3">
                    Must-Have Items
                  </label>
                  <div className="flex flex-wrap gap-2">
                    {(MUST_HAVE_OPTIONS[intake.room_type] || MUST_HAVE_OPTIONS["Living Room"]).map(item => {
                      const selected = (intake.must_have_items || []).includes(item)
                      return (
                        <button
                          key={item}
                          onClick={() => {
                            const current = intake.must_have_items || []
                            updateIntake({
                              must_have_items: selected
                                ? current.filter(i => i !== item)
                                : [...current, item],
                            })
                          }}
                          className={`px-3 py-1.5 rounded-full border text-sm transition-all ${
                            selected
                              ? "border-[#c9a96e] bg-[#c9a96e]/10 text-[#c9a96e]"
                              : "border-[#2a2a2a] text-gray-400 hover:border-[#3a3a3a]"
                          }`}
                        >
                          {selected ? "✓ " : "+ "}{item}
                        </button>
                      )
                    })}
                  </div>
                </div>
              )}

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Items to Avoid{" "}
                  <span className="text-gray-600 font-normal">(optional)</span>
                </label>
                <input
                  type="text"
                  placeholder='e.g. "No dark colors, no open shelving"'
                  value={intake.items_to_avoid || ""}
                  onChange={e => updateIntake({ items_to_avoid: e.target.value })}
                  className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded-xl px-3 py-2.5 text-sm text-white placeholder-gray-700 focus:border-[#c9a96e] focus:outline-none transition-colors"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Special Constraints{" "}
                  <span className="text-gray-600 font-normal">(optional)</span>
                </label>
                <textarea
                  rows={3}
                  placeholder='e.g. "Window on north wall, door opens inward on east side"'
                  value={intake.special_constraints || ""}
                  onChange={e => updateIntake({ special_constraints: e.target.value })}
                  className="w-full bg-[#0f0f0f] border border-[#2a2a2a] rounded-xl px-3 py-2.5 text-sm text-white placeholder-gray-700 focus:border-[#c9a96e] focus:outline-none transition-colors resize-none"
                />
              </div>
            </div>
          )}

          {/* STEP 4 */}
          {currentStep === 4 && (
            <div className="space-y-6">
              <h2 className="text-xl font-semibold text-white">Review Your Details</h2>
              <div className="space-y-2">
                {[
                  { label: "Room", value: `${intake.room_type} — ${intake.length}ft × ${intake.width}ft × ${intake.ceiling_height}ft` },
                  { label: "Light", value: intake.light_level },
                  { label: "Style", value: intake.style_preference },
                  { label: "Color Mood", value: intake.color_mood },
                  { label: "Budget", value: BUDGET_RANGES.find(b => b.value === intake.budget_range)?.label },
                  { label: "Must-Have", value: intake.must_have_items?.join(", ") || "None" },
                ].map(({ label, value }) => (
                  <div key={label} className="flex justify-between items-center bg-[#0f0f0f] rounded-xl px-4 py-3">
                    <span className="text-sm text-gray-500">{label}</span>
                    <span className="text-sm font-medium text-white text-right max-w-xs">{value || "—"}</span>
                  </div>
                ))}
              </div>
              <div className="flex items-start gap-3 bg-[#c9a96e]/5 border border-[#c9a96e]/20 rounded-xl p-4">
                <Sparkles className="w-4 h-4 text-[#c9a96e] mt-0.5 flex-shrink-0" />
                <p className="text-sm text-[#c9a96e]">
                  Design plan ready in ~15 seconds. Concept render in ~60 seconds.
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Navigation */}
        <div className="flex justify-between mt-6">
          <button
            onClick={handleBack}
            disabled={currentStep === 1}
            className="flex items-center gap-1.5 px-5 py-2.5 rounded-xl bg-[#1e1e1e] border border-[#2a2a2a] text-sm text-gray-300 hover:bg-[#2a2a2a] disabled:opacity-30 disabled:cursor-not-allowed transition-all"
          >
            <ChevronLeft className="w-4 h-4" />
            Back
          </button>

          {currentStep < 4 ? (
            <button
              onClick={handleNext}
              className="flex items-center gap-1.5 px-5 py-2.5 rounded-xl bg-[#c9a96e] text-black text-sm font-semibold hover:bg-[#a07840] transition-all"
            >
              Next
              <ChevronRight className="w-4 h-4" />
            </button>
          ) : (
            <button
              onClick={handleSubmit}
              disabled={isSubmitting}
              className="flex items-center gap-2 px-8 py-2.5 rounded-xl bg-[#c9a96e] text-black text-sm font-semibold hover:bg-[#a07840] disabled:opacity-60 disabled:cursor-not-allowed transition-all"
            >
              {isSubmitting ? (
                <>
                  <div className="w-4 h-4 border-2 border-black/30 border-t-black rounded-full animate-spin" />
                  Generating...
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4" />
                  Generate My Design
                </>
              )}
            </button>
          )}
        </div>
      </div>
    </div>
  )
}