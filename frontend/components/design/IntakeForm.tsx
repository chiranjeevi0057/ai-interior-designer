// components/design/IntakeForm.tsx
// The 4-step room intake form.
// Collects all the information the AI needs to design the room.

"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { useDesignStore } from "@/lib/store"
import { generateDesign, IntakePayload } from "@/lib/api"
import Button from "@/components/ui/Button"
import { Card } from "@/components/ui/Card"
import {
  ChevronLeft,
  ChevronRight,
  Sparkles,
  Home,
  Palette,
  DollarSign,
  CheckCircle,
} from "lucide-react"

// Form options
const ROOM_TYPES = [
  "Living Room",
  "Bedroom",
  "Home Office",
  "Dining Room",
  "Studio Apartment",
]

const STYLE_OPTIONS = [
  { value: "Minimalist", desc: "Clean, simple, functional" },
  { value: "Scandinavian", desc: "Warm, natural, cozy" },
  { value: "Industrial", desc: "Raw, urban, edgy" },
  { value: "Bohemian", desc: "Eclectic, colorful, free-spirited" },
  { value: "Contemporary", desc: "Modern, sleek, current" },
  { value: "Traditional", desc: "Classic, timeless, elegant" },
  { value: "Mid-Century Modern", desc: "Retro, organic, iconic" },
  { value: "Japandi", desc: "Japanese-Scandinavian fusion" },
]

const COLOR_MOODS = [
  { value: "Warm and Cozy", color: "#c9a96e" },
  { value: "Cool and Calm", color: "#6e9ac9" },
  { value: "Bold and Vibrant", color: "#c96e6e" },
  { value: "Neutral and Clean", color: "#a0a0a0" },
]

const LIGHT_LEVELS = ["Bright", "Moderate", "Low"]

const BUDGET_RANGES = [
  { value: "Under 50000", label: "Under ₹50,000", desc: "Budget friendly" },
  { value: "50000 to 150000", label: "₹50K – ₹1.5L", desc: "Mid range" },
  { value: "150000 to 400000", label: "₹1.5L – ₹4L", desc: "Premium" },
  { value: "Above 400000", label: "Above ₹4L", desc: "Luxury" },
]

const MUST_HAVE_OPTIONS: Record<string, string[]> = {
  "Living Room": ["Sofa", "Coffee Table", "TV Unit", "Bookshelf", "Armchair"],
  Bedroom: ["Bed", "Wardrobe", "Study Desk", "Side Tables", "Dresser"],
  "Home Office": ["Desk", "Office Chair", "Bookshelf", "Filing Cabinet"],
  "Dining Room": ["Dining Table", "Dining Chairs", "Sideboard", "Display Cabinet"],
  "Studio Apartment": ["Sofa Bed", "Kitchen Island", "Wardrobe", "Study Desk"],
}

const STEP_ICONS = [Home, Palette, DollarSign, CheckCircle]
const STEP_LABELS = ["Room Basics", "Style & Mood", "Constraints", "Review"]

export default function IntakeForm() {
  const { currentStep, intake, updateIntake, setCurrentStep,
          setDesignPlan, setSessionId, setSessionState, setLoading,
          setError } = useDesignStore()

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
      const payload = intake as IntakePayload
      const response = await generateDesign(payload)

      setSessionId(response.session_id)
      setDesignPlan(response.design_plan)
      setSessionState(response.session_state)
    } catch (err: unknown) {
      const message =
        err instanceof Error ? err.message : "Failed to generate design."
      setError(message)
      setSessionState("idle")
    } finally {
      setIsSubmitting(false)
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-[#0a0a0a] px-4 py-12">
      <div className="mx-auto max-w-2xl">

        {/* Header */}
        <div className="mb-10 text-center">
          <div className="mb-3 inline-flex items-center gap-2 text-[#c9a96e]">
            <Sparkles className="h-5 w-5" />
            <span className="text-sm font-medium">AI Interior Designer</span>
          </div>
          <h1 className="text-3xl font-bold text-white">
            Tell us about your room
          </h1>
          <p className="mt-2 text-gray-400">
            Step {currentStep} of 4 — {STEP_LABELS[currentStep - 1]}
          </p>
        </div>

        {/* Progress Bar */}
        <div className="mb-8 flex gap-2">
          {[1, 2, 3, 4].map((step) => (
            <div
              key={step}
              className={`h-1 flex-1 rounded-full transition-all duration-300 ${
                step <= currentStep ? "bg-[#c9a96e]" : "bg-[#2a2a2a]"
              }`}
            />
          ))}
        </div>

        {/* Step Content */}
        <Card variant="bordered">

          {/* ── STEP 1: Room Basics ── */}
          {currentStep === 1 && (
            <div className="space-y-6">
              <h2 className="text-xl font-semibold text-white">
                Room Basics
              </h2>

              {/* Room Type */}
              <div>
                <label className="mb-3 block text-sm font-medium text-gray-300">
                  Room Type
                </label>
                <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
                  {ROOM_TYPES.map((type) => (
                    <button
                      key={type}
                      onClick={() => updateIntake({ room_type: type as IntakePayload["room_type"] })}
                      className={`rounded-lg border p-3 text-left text-sm transition-all ${
                        intake.room_type === type
                          ? "border-[#c9a96e] bg-[#c9a96e]/10 text-[#c9a96e]"
                          : "border-[#2a2a2a] text-gray-400 hover:border-[#3a3a3a]"
                      }`}
                    >
                      {type}
                    </button>
                  ))}
                </div>
              </div>

              {/* Dimensions */}
              <div>
                <label className="mb-3 block text-sm font-medium text-gray-300">
                  Room Dimensions (in feet)
                </label>
                <div className="grid grid-cols-3 gap-3">
                  {(["length", "width", "ceiling_height"] as const).map(
                    (field) => (
                      <div key={field}>
                        <label className="mb-1 block text-xs text-gray-500 capitalize">
                          {field.replace("_", " ")}
                        </label>
                        <input
                          type="number"
                          placeholder="ft"
                          value={intake[field] || ""}
                          onChange={(e) =>
                            updateIntake({
                              [field]: parseFloat(e.target.value),
                            })
                          }
                          className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2.5 text-sm text-white placeholder-gray-600 focus:border-[#c9a96e] focus:outline-none"
                        />
                      </div>
                    )
                  )}
                </div>
              </div>

              {/* Natural Light */}
              <div>
                <label className="mb-3 block text-sm font-medium text-gray-300">
                  Natural Light Level
                </label>
                <div className="flex gap-3">
                  {LIGHT_LEVELS.map((level) => (
                    <button
                      key={level}
                      onClick={() =>
                        updateIntake({
                          light_level: level as IntakePayload["light_level"],
                        })
                      }
                      className={`flex-1 rounded-lg border p-3 text-sm transition-all ${
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

          {/* ── STEP 2: Style & Mood ── */}
          {currentStep === 2 && (
            <div className="space-y-6">
              <h2 className="text-xl font-semibold text-white">
                Style & Mood
              </h2>

              {/* Style */}
              <div>
                <label className="mb-3 block text-sm font-medium text-gray-300">
                  Interior Style
                </label>
                <div className="grid grid-cols-2 gap-2">
                  {STYLE_OPTIONS.map(({ value, desc }) => (
                    <button
                      key={value}
                      onClick={() =>
                        updateIntake({
                          style_preference:
                            value as IntakePayload["style_preference"],
                        })
                      }
                      className={`rounded-lg border p-3 text-left transition-all ${
                        intake.style_preference === value
                          ? "border-[#c9a96e] bg-[#c9a96e]/10"
                          : "border-[#2a2a2a] hover:border-[#3a3a3a]"
                      }`}
                    >
                      <div
                        className={`text-sm font-medium ${
                          intake.style_preference === value
                            ? "text-[#c9a96e]"
                            : "text-white"
                        }`}
                      >
                        {value}
                      </div>
                      <div className="mt-0.5 text-xs text-gray-500">
                        {desc}
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Color Mood */}
              <div>
                <label className="mb-3 block text-sm font-medium text-gray-300">
                  Color Mood
                </label>
                <div className="grid grid-cols-2 gap-2">
                  {COLOR_MOODS.map(({ value, color }) => (
                    <button
                      key={value}
                      onClick={() =>
                        updateIntake({
                          color_mood: value as IntakePayload["color_mood"],
                        })
                      }
                      className={`flex items-center gap-3 rounded-lg border p-3 text-left transition-all ${
                        intake.color_mood === value
                          ? "border-[#c9a96e] bg-[#c9a96e]/10"
                          : "border-[#2a2a2a] hover:border-[#3a3a3a]"
                      }`}
                    >
                      <div
                        className="h-6 w-6 rounded-full flex-shrink-0"
                        style={{ backgroundColor: color }}
                      />
                      <span
                        className={`text-sm ${
                          intake.color_mood === value
                            ? "text-[#c9a96e]"
                            : "text-gray-300"
                        }`}
                      >
                        {value}
                      </span>
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* ── STEP 3: Constraints ── */}
          {currentStep === 3 && (
            <div className="space-y-6">
              <h2 className="text-xl font-semibold text-white">
                Constraints & Preferences
              </h2>

              {/* Budget */}
              <div>
                <label className="mb-3 block text-sm font-medium text-gray-300">
                  Budget Range
                </label>
                <div className="grid grid-cols-2 gap-2">
                  {BUDGET_RANGES.map(({ value, label, desc }) => (
                    <button
                      key={value}
                      onClick={() =>
                        updateIntake({
                          budget_range:
                            value as IntakePayload["budget_range"],
                        })
                      }
                      className={`rounded-lg border p-3 text-left transition-all ${
                        intake.budget_range === value
                          ? "border-[#c9a96e] bg-[#c9a96e]/10"
                          : "border-[#2a2a2a] hover:border-[#3a3a3a]"
                      }`}
                    >
                      <div
                        className={`text-sm font-medium ${
                          intake.budget_range === value
                            ? "text-[#c9a96e]"
                            : "text-white"
                        }`}
                      >
                        {label}
                      </div>
                      <div className="mt-0.5 text-xs text-gray-500">
                        {desc}
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Must Have Items */}
              {intake.room_type && (
                <div>
                  <label className="mb-3 block text-sm font-medium text-gray-300">
                    Must-Have Items
                  </label>
                  <div className="flex flex-wrap gap-2">
                    {(
                      MUST_HAVE_OPTIONS[intake.room_type] ||
                      MUST_HAVE_OPTIONS["Living Room"]
                    ).map((item) => {
                      const selected = (
                        intake.must_have_items || []
                      ).includes(item)
                      return (
                        <button
                          key={item}
                          onClick={() => {
                            const current = intake.must_have_items || []
                            updateIntake({
                              must_have_items: selected
                                ? current.filter((i) => i !== item)
                                : [...current, item],
                            })
                          }}
                          className={`rounded-full border px-3 py-1.5 text-sm transition-all ${
                            selected
                              ? "border-[#c9a96e] bg-[#c9a96e]/10 text-[#c9a96e]"
                              : "border-[#2a2a2a] text-gray-400 hover:border-[#3a3a3a]"
                          }`}
                        >
                          {selected ? "✓ " : "+ "}
                          {item}
                        </button>
                      )
                    })}
                  </div>
                </div>
              )}

              {/* Items to Avoid */}
              <div>
                <label className="mb-2 block text-sm font-medium text-gray-300">
                  Items or Styles to Avoid{" "}
                  <span className="text-gray-500">(optional)</span>
                </label>
                <input
                  type="text"
                  placeholder='e.g. "No dark colors, no open shelving"'
                  value={intake.items_to_avoid || ""}
                  onChange={(e) =>
                    updateIntake({ items_to_avoid: e.target.value })
                  }
                  className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2.5 text-sm text-white placeholder-gray-600 focus:border-[#c9a96e] focus:outline-none"
                />
              </div>

              {/* Special Constraints */}
              <div>
                <label className="mb-2 block text-sm font-medium text-gray-300">
                  Special Constraints{" "}
                  <span className="text-gray-500">(optional)</span>
                </label>
                <textarea
                  placeholder='e.g. "Window on north wall, door opens inward on east side"'
                  value={intake.special_constraints || ""}
                  onChange={(e) =>
                    updateIntake({ special_constraints: e.target.value })
                  }
                  rows={3}
                  className="w-full rounded-lg border border-[#2a2a2a] bg-[#0f0f0f] px-3 py-2.5 text-sm text-white placeholder-gray-600 focus:border-[#c9a96e] focus:outline-none resize-none"
                />
              </div>
            </div>
          )}

          {/* ── STEP 4: Review ── */}
          {currentStep === 4 && (
            <div className="space-y-6">
              <h2 className="text-xl font-semibold text-white">
                Review Your Details
              </h2>

              <div className="space-y-4">
                {[
                  {
                    label: "Room",
                    value: `${intake.room_type} — ${intake.length}ft × ${intake.width}ft × ${intake.ceiling_height}ft ceiling`,
                  },
                  {
                    label: "Light",
                    value: intake.light_level,
                  },
                  {
                    label: "Style",
                    value: intake.style_preference,
                  },
                  {
                    label: "Color Mood",
                    value: intake.color_mood,
                  },
                  {
                    label: "Budget",
                    value: BUDGET_RANGES.find(
                      (b) => b.value === intake.budget_range
                    )?.label,
                  },
                  {
                    label: "Must-Have Items",
                    value:
                      intake.must_have_items?.join(", ") ||
                      "None selected",
                  },
                ].map(({ label, value }) => (
                  <div
                    key={label}
                    className="flex justify-between rounded-lg bg-[#0f0f0f] px-4 py-3"
                  >
                    <span className="text-sm text-gray-400">{label}</span>
                    <span className="text-right text-sm font-medium text-white">
                      {value || "—"}
                    </span>
                  </div>
                ))}
              </div>

              <div className="rounded-lg border border-[#c9a96e]/20 bg-[#c9a96e]/5 p-4 text-sm text-[#c9a96e]">
                <Sparkles className="mb-1 h-4 w-4" />
                Design plan ready in ~15 seconds. Concept render in ~60 seconds.
              </div>
            </div>
          )}
        </Card>

        {/* Navigation Buttons */}
        <div className="mt-6 flex justify-between">
          <Button
            variant="secondary"
            onClick={handleBack}
            disabled={currentStep === 1}
          >
            <ChevronLeft className="mr-1 h-4 w-4" />
            Back
          </Button>

          {currentStep < 4 ? (
            <Button onClick={handleNext}>
              Next
              <ChevronRight className="ml-1 h-4 w-4" />
            </Button>
          ) : (
            <Button
              onClick={handleSubmit}
              isLoading={isSubmitting}
              className="min-w-[160px]"
            >
              <Sparkles className="mr-2 h-4 w-4" />
              Generate My Design
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}