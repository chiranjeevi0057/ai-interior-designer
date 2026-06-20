// lib/api.ts
// All communication with the FastAPI backend goes through here.
// No component should ever call fetch() or axios directly —
// they always use these functions instead.
// This makes it easy to change the backend URL in one place.

import axios from "axios"

// Base URL from environment variable
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

// Create axios instance with default settings
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  timeout: 180000,
  headers: {
    "Content-Type": "application/json",
  },
})

// TypeScript Types
// These mirror the Pydantic models in the backend exactly

export interface ColorSwatch {
  name: string
  hex_code: string
  usage: string
}

export interface FurnitureItem {
  id: string
  name: string
  category: string
  recommended_dimensions: string
  placement: string
  placement_reasoning: string
  priority: "essential" | "recommended" | "optional"
  estimated_cost_range: string
}

export interface LightingItem {
  type: string
  description: string
  placement: string
  reasoning: string
}

export interface DesignPlan {
  session_id: string
  version: number
  room_type: string
  room_dimensions_summary: string
  spatial_observations: string[]
  recommended_theme: string
  theme_rationale: string
  color_palette: ColorSwatch[]
  color_palette_notes: string
  furniture_plan: FurnitureItem[]
  furniture_plan_notes: string
  traffic_flow_notes: string
  lighting_plan: LightingItem[]
  key_design_principles: string[]
  design_warnings: string[]
  budget_tier: string
  estimated_total_range: string
  budget_notes: string
  image_prompt_keywords: string[]
  style_descriptors: string[]
  requires_visual_update: boolean
}

export interface IntakePayload {
  room_type: string
  length: number
  width: number
  ceiling_height: number
  unit: "feet" | "meters"
  style_preference: string
  color_mood: string
  light_level: string
  budget_range: string
  must_have_items: string[]
  items_to_avoid?: string
  special_constraints?: string
}

export interface GenerateDesignResponse {
  success: boolean
  session_id: string
  session_state: string
  design_plan: DesignPlan
  image_status: string
  requires_visual_update: boolean
  message: string
}

export interface ImageStatusResponse {
  success: boolean
  session_id: string
  image_status: "pending" | "generating" | "complete" | "failed"
  image_url?: string
  message: string
}

// API Functions

// Generate a new design plan from intake form data
export async function generateDesign(
  intake: IntakePayload
): Promise<GenerateDesignResponse> {
  const response = await api.post("/api/design/generate", intake)
  return response.data
}

// Refine an existing design plan
export async function refineDesign(
  sessionId: string,
  message: string
): Promise<GenerateDesignResponse> {
  const response = await api.post(
    `/api/design/refine?session_id=${sessionId}&user_message=${encodeURIComponent(message)}`
  )
  return response.data
}

// Check image generation status (used for polling)
export async function getImageStatus(
  sessionId: string
): Promise<ImageStatusResponse> {
  const response = await api.get(`/api/status/image/${sessionId}`)
  return response.data
}

// Health check — verify backend is reachable
export async function checkHealth(): Promise<boolean> {
  try {
    await api.get("/health")
    return true
  } catch {
    return false
  }
}

// Furniture recommendation types
export interface FurnitureProduct {
  id: string
  name: string
  category: string
  style_tags: string[]
  min_price: number
  max_price: number
  dimensions: string
  material: string
  description: string
  buy_links: Array<{ store: string; url: string }>
  suitable_rooms: string[]
  budget_tiers: string[]
}

export interface FurnitureRecommendation {
  ai_item: {
    name: string
    placement: string
    reasoning: string
    priority: string
    estimated_cost: string
  }
  products: FurnitureProduct[]
}

export interface FurnitureSummaryResponse {
  success: boolean
  session_id: string
  recommendations: FurnitureRecommendation[]
  budget_summary: {
    total_min: number
    total_max: number
    essential_min: number
    essential_max: number
    total_range: string
    essential_range: string
  }
}

// Get furniture recommendations for a session
export async function getFurnitureRecommendations(
  sessionId: string
): Promise<FurnitureSummaryResponse> {
  const response = await api.get(`/api/design/${sessionId}/furniture`)
  return response.data
}