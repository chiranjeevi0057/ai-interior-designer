// components/ui/Card.tsx

import { cn } from "@/lib/utils"
import { HTMLAttributes } from "react"

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  variant?: "default" | "elevated" | "bordered"
}

export function Card({
  className,
  variant = "default",
  children,
  ...props
}: CardProps) {
  const variants = {
    default: "bg-[#141414] rounded-xl p-6",
    elevated: "bg-[#1e1e1e] rounded-xl p-6 shadow-xl",
    bordered:
      "bg-[#141414] rounded-xl p-6 border border-[#2a2a2a]",
  }

  return (
    <div className={cn(variants[variant], className)} {...props}>
      {children}
    </div>
  )
}

export function CardHeader({
  className,
  children,
  ...props
}: HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn("mb-4 flex items-center justify-between", className)}
      {...props}
    >
      {children}
    </div>
  )
}

export function CardTitle({
  className,
  children,
  ...props
}: HTMLAttributes<HTMLHeadingElement>) {
  return (
    <h3
      className={cn("text-lg font-semibold text-white", className)}
      {...props}
    >
      {children}
    </h3>
  )
}