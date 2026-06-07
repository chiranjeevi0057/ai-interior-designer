// app/layout.tsx
// Root layout — wraps every page in the app.
// Sets fonts, metadata, and global structure.

import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: "AI Interior Designer",
  description:
    "Intelligent AI-powered interior design assistant. " +
    "Get professional room layouts, furniture recommendations, " +
    "and concept renders instantly.",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        {children}
      </body>
    </html>
  )
}