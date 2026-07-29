"use client"

import { useEffect, useState, Suspense } from "react"
import { useSearchParams, useRouter } from "next/navigation"
import { RapportDioceseData } from "../types"
import { fetchCompare, fetchDioceseDetail } from "../lib/api"
import { useI18n } from "../i18n/context"
import RapportDiocese from "../components/RapportDiocese"
import { ArrowLeft, Loader2, Globe } from "lucide-react"

function CompareContent() {
  const { t } = useI18n()
  const router = useRouter()
  const searchParams = useSearchParams()
  const ids = searchParams.get("ids") || ""

  const [dioceses, setDioceses] = useState<RapportDioceseData[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!ids) return
    const idList = ids.split(",").filter(Boolean)
    if (idList.length < 2) {
      setError("Sélectionnez 2 diocèses")
      setLoading(false)
      return
    }
    setLoading(true)
    Promise.all(idList.map((id) => fetchDioceseDetail(id)))
      .then((data) => {
        setDioceses(data)
        setLoading(false)
      })
      .catch((e) => {
        setError(e.message)
        setLoading(false)
      })
  }, [ids])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center text-muted-foreground">
        <Loader2 className="w-6 h-6 animate-spin mr-2" />
        {t.search.loading}
      </div>
    )
  }

  if (error || dioceses.length < 2) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center text-muted-foreground">
        <p className="text-sm">{error || t.sidebar.selectTwo}</p>
        <button
          onClick={() => router.push("/")}
          className="mt-4 px-4 py-2 bg-primary text-primary-foreground rounded-lg text-sm"
        >
          {t.compare.back}
        </button>
      </div>
    )
  }

  const [d1, d2] = dioceses

  return (
    <main className="min-h-screen bg-background">
      <header className="border-b border-border">
        <div className="max-w-6xl mx-auto px-4 py-5">
          <div className="flex items-center gap-2 mb-1">
            <Globe className="w-5 h-5 text-foreground" />
            <h1 className="text-lg font-medium">{t.compare.title}</h1>
          </div>
          <p className="text-sm text-muted-foreground">
            {d1.nom} {t.compare.vs} {d2.nom}
          </p>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-4 py-6">
        <button
          onClick={() => router.push("/")}
          className="flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground mb-4"
        >
          <ArrowLeft className="w-4 h-4" />
          {t.compare.back}
        </button>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div>
            <div className="text-xs font-medium text-muted-foreground mb-2 px-1">{d1.nom}</div>
            <RapportDiocese data={d1} />
          </div>
          <div>
            <div className="text-xs font-medium text-muted-foreground mb-2 px-1">{d2.nom}</div>
            <RapportDiocese data={d2} />
          </div>
        </div>
      </div>
    </main>
  )
}

export default function ComparePage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen flex items-center justify-center text-muted-foreground">
        <Loader2 className="w-6 h-6 animate-spin mr-2" />
        Loading...
      </div>
    }>
      <CompareContent />
    </Suspense>
  )
}
