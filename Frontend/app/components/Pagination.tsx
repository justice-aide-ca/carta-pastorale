"use client"

import { ChevronLeft, ChevronRight } from "lucide-react"
import { useI18n } from "../i18n/context"

interface PaginationProps {
  currentPage: number
  totalPages: number
  onPageChange: (page: number) => void
}

export default function Pagination({ currentPage, totalPages, onPageChange }: PaginationProps) {
  const { t } = useI18n()
  if (totalPages <= 1) return null

  return (
    <div className="flex items-center justify-between px-3 py-2 border-t border-border bg-secondary">
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 0}
        className="flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground disabled:opacity-30 disabled:cursor-not-allowed"
      >
        <ChevronLeft className="w-3.5 h-3.5" />
        {t.pagination.previous}
      </button>
      <span className="text-xs text-muted-foreground">
        {t.pagination.page} {currentPage + 1} {t.pagination.of} {totalPages}
      </span>
      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage >= totalPages - 1}
        className="flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground disabled:opacity-30 disabled:cursor-not-allowed"
      >
        {t.pagination.next}
        <ChevronRight className="w-3.5 h-3.5" />
      </button>
    </div>
  )
}
