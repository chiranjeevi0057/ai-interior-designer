// lib/store.ts
// Global state using Zustand — simpler than Redux,
// works perfectly for this project's scale.

import { create } from "zustand"
import { DesignPlan, IntakePayload } from "./api"

type ImageStatus = "idle" | "pending" | "generating" | "complete" | "failed"

interface ConversationTurn {
  role: "user" | "assistant"
  content: string
  timestamp: string
}

interface DesignStore {
  // Session
  sessionId: string | null
  sessionState: string

  // Form
  intake: Partial<IntakePayload>
  currentStep: number

  // Output
  designPlan: DesignPlan | null
  imageStatus: ImageStatus
  imageUrl: string | null

  // Conversation
  conversationHistory: ConversationTurn[]

  // UI
  isLoading: boolean
  error: string | null

  // Actions
  setSessionId: (id: string) => void
  setSessionState: (state: string) => void
  updateIntake: (data: Partial<IntakePayload>) => void
  setCurrentStep: (step: number) => void
  setDesignPlan: (plan: DesignPlan) => void
  setImageStatus: (status: ImageStatus) => void
  setImageUrl: (url: string) => void
  addConversationTurn: (role: "user" | "assistant", content: string) => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
  resetSession: () => void
}

export const useDesignStore = create<DesignStore>((set) => ({
  // Initial state
  sessionId: null,
  sessionState: "idle",
  intake: {},
  currentStep: 1,
  designPlan: null,
  imageStatus: "idle",
  imageUrl: null,
  conversationHistory: [],
  isLoading: false,
  error: null,

  // Actions — each updates one piece of state
  setSessionId: (id) => set({ sessionId: id }),
  setSessionState: (state) => set({ sessionState: state }),
  updateIntake: (data) => set((s) => ({ intake: { ...s.intake, ...data } })),
  setCurrentStep: (step) => set({ currentStep: step }),
  setDesignPlan: (plan) => set({ designPlan: plan }),
  setImageStatus: (status) => set({ imageStatus: status }),
  setImageUrl: (url) => set({ imageUrl: url }),
  addConversationTurn: (role, content) =>
    set((s) => ({
      conversationHistory: [
        ...s.conversationHistory,
        { role, content, timestamp: new Date().toISOString() },
      ],
    })),
  setLoading: (loading) => set({ isLoading: loading }),
  setError: (error) => set({ error }),
  resetSession: () =>
    set({
      sessionId: null,
      sessionState: "idle",
      intake: {},
      currentStep: 1,
      designPlan: null,
      imageStatus: "idle",
      imageUrl: null,
      conversationHistory: [],
      isLoading: false,
      error: null,
    }),
}))