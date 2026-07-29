"use client"

import { useState, useEffect, useMemo } from "react"
import { useRouter } from "next/navigation"
import RapportDiocese from "./components/RapportDiocese"
import Pagination from "./components/Pagination"
import { RapportDioceseData, DioceseSummary } from "./types"
import { fetchDioceses, searchDioceses, fetchDioceseDetail, fetchContinents } from "./lib/api"
import { useI18n } from "./i18n/context"
import { Search, Loader2, Globe, ChevronRight, Filter, Languages, ArrowLeftRight } from "lucide-react"

const ITEMS_PER_PAGE = 20

export default function Home() {
  const { t, lang, setLang } = useI18n()
  const router = useRouter()

  const [searchQuery, setSearchQuery] = useState("")
  const [searchResults, setSearchResults] = useState<DioceseSummary[]>([])
  const [selectedDiocese, setSelectedDiocese] = useState<RapportDioceseData | null>(null)
  const [loading, setLoading] = useState(false)
  const [apiAvailable, setApiAvailable] = useState(false)
  const [allDioceses, setAllDioceses] = useState<DioceseSummary[]>([])
  const [continents, setContinents] = useState<string[]>([])
  const [error, setError] = useState<string | null>(null)

  const [currentPage, setCurrentPage] = useState(0)
  const [filterContinent, setFilterContinent] = useState("")
  const [filterCategory, setFilterCategory] = useState("")
  const [compareMode, setCompareMode] = useState(false)
  const [compareSelection, setCompareSelection] = useState<string[]>([])

  useEffect(() => {
    fetchDioceses()
      .then((data) => {
        setAllDioceses(data)
        setApiAvailable(true)
      })
      .catch(() => setApiAvailable(false))
    fetchContinents().then(setContinents)
  }, [])

  const categories = useMemo(() => {
    const cats = new Set(allDioceses.map((d) => d.categorie))
    return Array.from(cats).sort()
  }, [allDioceses])

  const filteredDioceses = useMemo(() => {
    let list = allDioceses
    if (filterContinent) list = list.filter((d) => d.continent === filterContinent)
    if (filterCategory) list = list.filter((d) => d.categorie === filterCategory)
    return list
  }, [allDioceses, filterContinent, filterCategory])

  const paginatedDioceses = useMemo(() => {
    const start = currentPage * ITEMS_PER_PAGE
    return filteredDioceses.slice(start, start + ITEMS_PER_PAGE)
  }, [filteredDioceses, currentPage])

  const totalPages = Math.ceil(filteredDioceses.length / ITEMS_PER_PAGE)

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      setSearchResults([])
      return
    }
    setLoading(true)
    setError(null)
    try {
      const data = await searchDioceses(searchQuery)
      setSearchResults(data.results)
    } catch (e: any) {
      setError(e.message)
      setSearchResults([])
    } finally {
      setLoading(false)
    }
  }

  const handleSelectDiocese = async (id: string) => {
    if (compareMode) {
      if (compareSelection.includes(id)) {
        setCompareSelection(compareSelection.filter((x) => x !== id))
      } else if (compareSelection.length < 2) {
        const next = [...compareSelection, id]
        setCompareSelection(next)
        if (next.length === 2) {
          router.push(`/compare?ids=${next.join(",")}`)
        }
      }
      return
    }

    setLoading(true)
    setError(null)
    try {
      const data = await fetchDioceseDetail(id)
      setSelectedDiocese(data)
    } catch (e: any) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const displayList = searchResults.length > 0 ? searchResults : paginatedDioceses

  return (
    <main className="min-h-screen bg-background">
      <header className="border-b border-border">
        <div className="max-w-5xl mx-auto px-4 py-5">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 mb-1">
              <Globe className="w-5 h-5 text-foreground" />
              <h1 className="text-lg font-medium">{t.app.title}</h1>
              {apiAvailable ? (
                <span className="ml-2 text-xs px-2 py-0.5 rounded-full bg-green-50 text-green-700 border border-green-200">
                  {allDioceses.length.toLocaleString(lang)} {t.app.dioceses}
                </span>
              ) : (
                <span className="ml-2 text-xs px-2 py-0.5 rounded-full bg-amber-50 text-amber-700 border border-amber-200">
                  {t.app.offline}
                </span>
              )}
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setCompareMode(!compareMode)}
                className={`flex items-center gap-1.5 px-3 py-1.5 text-xs rounded-lg border transition-colors ${
                  compareMode
                    ? "bg-blue-50 text-blue-700 border-blue-200"
                    : "bg-secondary text-secondary-foreground border-border hover:bg-secondary/80"
                }`}
              >
                <ArrowLeftRight className="w-3.5 h-3.5" />
                {t.sidebar.compare}
                {compareMode && compareSelection.length > 0 && ` (${compareSelection.length}/2)`}
              </button>
              <button
                onClick={() => setLang(lang === "fr" ? "en" : "fr")}
                className="flex items-center gap-1.5 px-3 py-1.5 text-xs rounded-lg border border-border bg-secondary text-secondary-foreground hover:bg-secondary/80"
              >
                <Languages className="w-3.5 h-3.5" />
                {lang === "fr" ? "EN" : "FR"}
              </button>
            </div>
          </div>
          <p className="text-sm text-muted-foreground">{t.app.subtitle}</p>
        </div>
      </header>

      <div className="max-w-5xl mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-1 space-y-4">
            <div className="border border-border rounded-xl p-3">
              <div className="flex gap-2">
                <input
                  type="text"
                  placeholder={t.search.placeholder}
                  value={searchQuery}
                  onChange={(e) => { setSearchQuery(e.target.value); setSearchResults([]) }}
                  onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                  className="flex-1 px-3 py-2 text-sm border border-border rounded-lg bg-background focus:outline-none focus:ring-1 focus:ring-ring"
                />
                <button
                  onClick={handleSearch}
                  disabled={loading}
                  className="px-3 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors disabled:opacity-50"
                >
                  <Search className="w-4 h-4" />
                </button>
              </div>
            </div>

            {compareMode && (
              <div className="text-xs text-blue-700 bg-blue-50 border border-blue-200 rounded-lg px-3 py-2">
                {t.sidebar.selectTwo}
              </div>
            )}

            {error && (
              <div className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">
                {error}
              </div>
            )}

            <div className="border border-border rounded-xl overflow-hidden">
              <div className="px-3 py-2 text-xs font-medium text-muted-foreground bg-secondary border-b border-border flex items-center gap-1.5">
                <Filter className="w-3.5 h-3.5" />
                {t.sidebar.filters}
              </div>
              <div className="p-3 space-y-2">
                <select
                  value={filterContinent}
                  onChange={(e) => { setFilterContinent(e.target.value); setCurrentPage(0) }}
                  className="w-full px-2.5 py-1.5 text-xs border border-border rounded-md bg-background"
                >
                  <option value="">{t.sidebar.allContinents}</option>
                  {continents.map((c) => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
                <select
                  value={filterCategory}
                  onChange={(e) => { setFilterCategory(e.target.value); setCurrentPage(0) }}
                  className="w-full px-2.5 py-1.5 text-xs border border-border rounded-md bg-background"
                >
                  <option value="">{t.sidebar.allCategories}</option>
                  {categories.map((c) => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
              </div>
            </div>

            {searchResults.length > 0 && (
              <div className="text-xs text-muted-foreground px-1">
                {searchResults.length} {t.search.results}{searchResults.length > 1 ? "s" : ""}
              </div>
            )}

            <div className="border border-border rounded-xl overflow-hidden">
              <div className="px-3 py-2 text-xs font-medium text-muted-foreground bg-secondary border-b border-border">
                {searchResults.length > 0 ? t.search.results : t.sidebar.quickAccess}
              </div>
              <div className="divide-y divide-border max-h-96 overflow-y-auto">
                {displayList.map((d) => (
                  <button
                    key={d.id}
                    onClick={() => handleSelectDiocese(d.id)}
                    className={`w-full px-3 py-2.5 text-left hover:bg-secondary transition-colors flex items-center justify-between ${
                      selectedDiocese?.id === d.id ? "bg-secondary" : ""
                    } ${compareSelection.includes(d.id) ? "bg-blue-50" : ""}`}
                  >
                    <div>
                      <div className="text-sm font-medium">{d.nom}</div>
                      <div className="text-xs text-muted-foreground">
                        {d.pays} · {d.type}
                      </div>
                    </div>
                    <ChevronRight className="w-4 h-4 text-muted-foreground" />
                  </button>
                ))}
              </div>
              {searchResults.length === 0 && (
                <Pagination
                  currentPage={currentPage}
                  totalPages={totalPages}
                  onPageChange={setCurrentPage}
                />
              )}
            </div>

            {loading && (
              <div className="flex items-center justify-center py-4 text-muted-foreground">
                <Loader2 className="w-4 h-4 animate-spin mr-2" />
                <span className="text-sm">{t.search.loading}</span>
              </div>
            )}
          </div>

          <div className="lg:col-span-2">
            {selectedDiocese ? (
              <RapportDiocese data={selectedDiocese} />
            ) : (
              <div className="border border-border rounded-xl p-8 text-center text-muted-foreground">
                <Globe className="w-10 h-10 mx-auto mb-3 opacity-40" />
                <p className="text-sm">{t.diocese.select}</p>
                <p className="text-xs mt-1 opacity-60">
                  {apiAvailable
                    ? `${allDioceses.length.toLocaleString(lang)} ${t.app.dioceses} ${t.app.available}.`
                    : t.app.offline}
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  )
}
