// components/ui/Button.tsx

import { cn } from "@/lib/utils"
import { ButtonHTMLAttributes, forwardRef } from "react"

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost" | "danger"
  size?: "sm" | "md" | "lg"
  isLoading?: boolean
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      className,
      variant = "primary",
      size = "md",
      isLoading = false,
      children,
      disabled,
      ...props
    },
    ref
  ) => {
    const baseStyles =
      "inline-flex items-center justify-center rounded-lg font-medium " +
      "transition-all duration-200 focus:outline-none focus:ring-2 " +
      "focus:ring-offset-2 focus:ring-offset-black disabled:opacity-50 " +
      "disabled:cursor-not-allowed"

    const variants = {
      primary:
        "bg-[#c9a96e] text-black hover:bg-[#a07840] " +
        "focus:ring-[#c9a96e]",
      secondary:
        "bg-[#1e1e1e] text-white border border-[#2a2a2a] " +
        "hover:bg-[#2a2a2a] focus:ring-gray-500",
      ghost:
        "bg-transparent text-[#c9a96e] hover:bg-[#1e1e1e] " +
        "focus:ring-[#c9a96e]",
      danger:
        "bg-red-900 text-red-100 hover:bg-red-800 " +
        "focus:ring-red-500",
    }

    const sizes = {
      sm: "px-3 py-1.5 text-sm",
      md: "px-5 py-2.5 text-sm",
      lg: "px-8 py-3.5 text-base",
    }

    return (
      <button
        ref={ref}
        className={cn(baseStyles, variants[variant], sizes[size], className)}
        disabled={disabled || isLoading}
        {...props}
      >
        {isLoading ? (
          <>
            <svg
              className="mr-2 h-4 w-4 animate-spin"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
              />
            </svg>
            Processing...
          </>
        ) : (
          children
        )}
      </button>
    )
  }
)

Button.displayName = "Button"
export default Button