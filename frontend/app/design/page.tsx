// app/design/page.tsx
// The main design flow page.
// Manages which screen to show based on the current app state:
// Step 1-4: Intake form
// Loading: AI is generating the plan
// Results: Design plan + concept render + refinement chat

"use client"

import { useDesignStore } from "@/lib/store"
import IntakeForm from "@/components/design/IntakeForm"
import LoadingScreen from "@/components/design/LoadingScreen"
import ResultsPage from "@/components/design/ResultsPage"

export default function DesignPage() {
  const { sessionState, designPlan, isLoading } = useDesignStore()

  // Show loading screen while AI is working
  if (sessionState === "planning" || isLoading) {
    return <LoadingScreen />
  }

  // Show results if we have a design plan — regardless of session state
  if (designPlan !== null) {
    return <ResultsPage />
  }

  // Default: show the intake form
  return <IntakeForm />
}