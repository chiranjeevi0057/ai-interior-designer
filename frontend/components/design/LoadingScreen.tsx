// components/design/LoadingScreen.tsx
// Shown while the AI is generating the design plan.
// Shows animated progress steps so users know what's happening.

"use client"

import { useEffect, useState } from "react"
import { Sparkles } from "lucide-react"

const LOADING_STEPS = [
  { label: "Analyzing your room dimensions...", duration: 3000 },
  { label: "Planning furniture layout...", duration: 5000 },
  { label: "Selecting your design theme...", duration: 5000 },
  { label: "Preparing your design plan...", duration: 4000 },
]

export default function LoadingScreen() {
  const [currentStep, setCurrentStep] = useState(0)
  const [elapsed, setElapsed] = useState(0)

  useEffect(() => {
    const timer = setInterval(() => {
      setElapsed((prev) => {
        const next = prev + 1
        // Advance step based on elapsed seconds
        if (next === 3) setCurrentStep(1)
        if (next === 8) setCurrentStep(2)
        if (next === 13) setCurrentStep(3)
        return next
      })
    }, 1000)

    return () => clearInterval(timer)
  }, [])

  return (
    <div className="flex min-h-screen items-center justify-center bg-[#0a0a0a] px-4">
      <div className="w-full max-w-md text-center">

        {/* Animated Icon */}
        <div className="mb-8 flex justify-center">
          <div className="relative">
            <div className="h-20 w-20 rounded-full border-2 border-[#c9a96e]/20 flex items-center justify-center">
              <Sparkles className="h-8 w-8 text-[#c9a96e] animate-pulse" />
            </div>
            {/* Rotating ring */}
            <div className="absolute inset-0 rounded-full border-2 border-transparent border-t-[#c9a96e] animate-spin" />
          </div>
        </div>

        <h2 className="mb-2 text-2xl font-bold text-white">
          Creating Your Design
        </h2>
        <p className="mb-10 text-gray-400">
          Our AI is analyzing your room and planning the perfect layout
        </p>

        {/* Progress Steps */}
        <div className="space-y-4 text-left">
          {LOADING_STEPS.map((step, index) => (
            <div key={index} className="flex items-center gap-4">
              {/* Step indicator */}
              <div className="flex-shrink-0">
                {index < currentStep ? (
                  // Completed
                  <div className="h-6 w-6 rounded-full bg-[#c9a96e] flex items-center justify-center">
                    <svg className="h-3 w-3 text-black" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                    </svg>
                  </div>
                ) : index === currentStep ? (
                  // Active
                  <div className="h-6 w-6 rounded-full border-2 border-[#c9a96e] flex items-center justify-center">
                    <div className="h-2 w-2 rounded-full bg-[#c9a96e] animate-pulse" />
                  </div>
                ) : (
                  // Pending
                  <div className="h-6 w-6 rounded-full border-2 border-[#2a2a2a]" />
                )}
              </div>

              {/* Step label */}
              <span
                className={`text-sm transition-colors duration-300 ${
                  index <= currentStep ? "text-white" : "text-gray-600"
                }`}
              >
                {step.label}
              </span>
            </div>
          ))}
        </div>

        {/* Time indicator */}
        <p className="mt-8 text-xs text-gray-600">
          {elapsed}s elapsed · Usually takes 15–20 seconds
        </p>
      </div>
    </div>
  )
}