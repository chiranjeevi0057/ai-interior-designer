// components/design/FurniturePanel.tsx
// Displays enriched furniture recommendations with
// real products, pricing and shopping links.

"use client"

import { useEffect, useState } from "react"
import {
  getFurnitureRecommendations,
  FurnitureRecommendation,
} from "@/lib/api"
import {
  ShoppingBag, ExternalLink,
  ChevronDown, ChevronUp, Package
} from "lucide-react"

interface FurniturePanelProps {
  sessionId: string
}

export default function FurniturePanel({ sessionId }: FurniturePanelProps) {
  const [recommendations, setRecommendations] = useState<FurnitureRecommendation[]>([])
  const [budgetSummary, setBudgetSummary] = useState<{
    total_range: string
    essential_range: string
  } | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [expandedItem, setExpandedItem] = useState<string | null>(null)

  useEffect(() => {
    const load = async () => {
      try {
        setIsLoading(true)
        const data = await getFurnitureRecommendations(sessionId)
        setRecommendations(data.recommendations)
        setBudgetSummary(data.budget_summary)
      } catch {
        setError("Could not load furniture recommendations.")
      } finally {
        setIsLoading(false)
      }
    }
    load()
  }, [sessionId])

  if (isLoading) {
    return (
      <>
        <div className="bg-[#141414] border border-[#2a2a2a] rounded-2xl p-6">
          <div className="flex items-center gap-3 mb-4">
            <ShoppingBag className="w-5 h-5 text-[#c9a96e]" />
            <h3 className="font-semibold text-white">Shop the Look</h3>
          </div>
          <div className="space-y-3">
            {[1, 2, 3].map(i => (
              <div key={i} className="h-16 bg-[#1e1e1e] rounded-xl animate-pulse" />
            ))}
          </div>
        </div>
      </>
    )
  }

  if (error) {
    return (
      <div className="bg-[#141414] border border-[#2a2a2a] rounded-2xl p-6">
        <p className="text-sm text-gray-500">{error}</p>
      </div>
    )
  }

  return (
    <>
    <div className="bg-[#141414] border border-[#2a2a2a] rounded-2xl p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-5">
        <div className="flex items-center gap-2">
          <ShoppingBag className="w-5 h-5 text-[#c9a96e]" />
          <h3 className="font-semibold text-white">Shop the Look</h3>
        </div>
        {budgetSummary && (
          <div className="text-right">
            <p className="text-xs text-gray-500">Estimated Total</p>
            <p className="text-sm font-semibold text-[#c9a96e]">
              {budgetSummary.total_range}
            </p>
          </div>
        )}
      </div>

      {/* Budget Summary */}
      {budgetSummary && (
        <div className="grid grid-cols-2 gap-3 mb-5">
          <div className="bg-[#0f0f0f] rounded-xl p-3 text-center">
            <p className="text-xs text-gray-500 mb-1">Essential Items</p>
            <p className="text-sm font-semibold text-white">
              {budgetSummary.essential_range}
            </p>
          </div>
          <div className="bg-[#0f0f0f] rounded-xl p-3 text-center">
            <p className="text-xs text-gray-500 mb-1">Full Room</p>
            <p className="text-sm font-semibold text-white">
              {budgetSummary.total_range}
            </p>
          </div>
        </div>
      )}

      {/* Recommendations */}
      <div className="space-y-3">
        {recommendations.map((rec, index) => (
          <div
            key={index}
            className="border border-[#2a2a2a] rounded-xl overflow-hidden"
          >
            {/* Item Header */}
            <button
              onClick={() =>
                setExpandedItem(
                  expandedItem === rec.ai_item.name
                    ? null
                    : rec.ai_item.name
                )
              }
              className="w-full flex items-center justify-between p-4 hover:bg-[#1e1e1e] transition-colors"
            >
              <div className="flex items-center gap-3 text-left">
                <div className="w-8 h-8 rounded-lg bg-[#c9a96e]/10 flex items-center justify-center flex-shrink-0">
                  <Package className="w-4 h-4 text-[#c9a96e]" />
                </div>
                <div>
                  <p className="text-sm font-medium text-white">
                    {rec.ai_item.name}
                  </p>
                  <p className="text-xs text-gray-500">
                    {rec.products.length > 0
                      ? `${rec.products.length} options found`
                      : "No matches found"}
                    {" · "}
                    <span className={
                      rec.ai_item.priority === "essential"
                        ? "text-[#c9a96e]"
                        : "text-gray-600"
                    }>
                      {rec.ai_item.priority}
                    </span>
                  </p>
                </div>
              </div>
              {expandedItem === rec.ai_item.name
                ? <ChevronUp className="w-4 h-4 text-gray-400 flex-shrink-0" />
                : <ChevronDown className="w-4 h-4 text-gray-400 flex-shrink-0" />
              }
            </button>

            {/* Expanded Products */}
            {expandedItem === rec.ai_item.name && (
              <div className="border-t border-[#2a2a2a] p-4 space-y-3 bg-[#0f0f0f]">

                {/* AI Placement Note */}
                <div className="text-xs text-gray-500 italic mb-3">
                  📍 {rec.ai_item.placement}
                </div>

                {rec.products.length === 0 ? (
                  <p className="text-xs text-gray-600">
                    No exact matches in database. Search manually on Pepperfry or Urban Ladder.
                  </p>
                ) : (
                  rec.products.map((product, pIndex) => (
                    <div
                      key={pIndex}
                      className="bg-[#141414] rounded-xl p-4 border border-[#2a2a2a]"
                    >
                      <div className="flex items-start justify-between mb-2">
                        <div>
                          <p className="text-sm font-medium text-white">
                            {product.name}
                          </p>
                          <p className="text-xs text-gray-500 mt-0.5">
                            {product.material}
                          </p>
                        </div>
                        <div className="text-right flex-shrink-0 ml-3">
                          <p className="text-xs text-gray-500">Price Range</p>
                          <p className="text-sm font-semibold text-[#c9a96e]">
                            ₹{product.min_price.toLocaleString()} –{" "}
                            ₹{product.max_price.toLocaleString()}
                          </p>
                        </div>
                      </div>

                      <p className="text-xs text-gray-500 mb-3">
                        {product.description}
                      </p>

                      <p className="text-xs text-gray-600 mb-3">
                        📐 {product.dimensions}
                      </p>

                      {/* Buy Links */}
                      <div className="flex flex-wrap gap-2">
                        {product.buy_links.map((link, lIndex) => (
                          <a
                            key={lIndex}
                            href={link.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-lg border border-[#2a2a2a] text-gray-300 hover:border-[#c9a96e] hover:text-[#c9a96e] transition-colors"
                          >
                            <ExternalLink className="w-3 h-3" />
                            {link.store}
                          </a>
                        ))}
                      </div>
                    </div>
                  ))
                )}
              </div>
            )}
          </div>
        ))}
      </div>

      <p className="text-xs text-gray-700 mt-4 text-center">
        Prices are approximate. Check stores for current availability.
      </p>
    </div>
  </>)
}