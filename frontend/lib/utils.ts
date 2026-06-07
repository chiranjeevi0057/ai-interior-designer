// lib/utils.ts
// Utility functions used throughout the frontend.

import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

// Combines Tailwind classes without conflicts
// Usage: cn("px-4 py-2", isActive && "bg-blue-500")
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}