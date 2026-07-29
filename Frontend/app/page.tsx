"use client"

import { useState, useEffect } from "react"
import RapportDiocese from "./components/RapportDiocese"
import { RapportDioceseData, DioceseSummary } from "./types"
import { fetchDioceses, searchDioceses, fetchDioceseDetail } from "./lib/api"
import { Search, Loader2, Globe, ChevronRight } from "lucide-react"

export default function Home() {
  const [searchQuery, setSearchQuery] = useState("")
  const [searchResults, setSearchResults] = useState<DioceseSummary[]>([])
  const [selectedDiocese, setSelectedDiocese] = useState<RapportDioceseData | null>(null)
  const [loading, setLoading] = useState(false)
  const [apiAvailable, setApiAvailable] = useState(false)
  const [allDioceses, setAllDioceses] = useState<DioceseSummary[]>([])
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchDioceses()
      .then((data) => {
        setAllDioceses(data)
        setApiAvailable(true)
      })
      .catch(() => setApiAvailable(false))
  }, [])

  const handleSearch = async () => {
    if (!searchQuery.trim()) return
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

  return (
    <main className="min-h-screen bg-background">
      <header className="border-b border-border">
        <div className="max-w-5xl mx-auto px-4 py-5">
          <div className="flex items-center gap-2 mb-1">
            <Globe className="w-5 h-5 text-foreground" />
            <h1 className="text-lg font-medium">Carta Pastorale</h1>
            {apiAvailable ? (
              <span className="ml-2 text-xs px-2 py-0.5 rounded-full bg-green-50 text-green-700 border border-green-200">
                {allDioceses.length.toLocaleString("fr-FR")} diocèses
              </span>
            ) : (
              <span className="ml-2 text-xs px-2 py-0.5 rounded-full bg-amber-50 text-amber-700 border border-amber-200">
                hors ligne
              </span>
            )}
          </div>
          <p className="text-sm text-muted-foreground">
            Rapports pastoraux par diocèse — données, indicateurs et pistes missionnaires
          </p>
        </div>
      </header>

      <div className="max-w-5xl mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-1 space-y-4">
            <div className="border border-border rounded-xl p-3">
              <div className="flex gap-2">
                <input
                  type="text"
                  placeholder="Rechercher un diocèse..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
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

            {error && (
              <div className="text-sm text-red-600 bg-red-50 border border-red-200 rounded-lg px-3 py-2">
                {error}
              </div>
            )}

            {searchResults.length > 0 && (
              <div className="border border-border rounded-xl overflow-hidden">
                <div className="px-3 py-2 text-xs font-medium text-muted-foreground bg-secondary border-b border-border">
                  {searchResults.length} résultat{searchResults.length > 1 ? "s" : ""}
                </div>
                <div className="divide-y divide-border max-h-80 overflow-y-auto">
                  {searchResults.map((d) => (
                    <button
                      key={d.id}
                      onClick={() => handleSelectDiocese(d.id)}
                      className={`w-full px-3 py-2.5 text-left hover:bg-secondary transition-colors flex items-center justify-between ${
                        selectedDiocese?.id === d.id ? "bg-secondary" : ""
                      }`}
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
              </div>
            )}

            {loading && (
              <div className="flex items-center justify-center py-4 text-muted-foreground">
                <Loader2 className="w-4 h-4 animate-spin mr-2" />
                <span className="text-sm">Chargement...</span>
              </div>
            )}

            {allDioceses.length > 0 && searchResults.length === 0 && (
              <div className="border border-border rounded-xl overflow-hidden">
                <div className="px-3 py-2 text-xs font-medium text-muted-foreground bg-secondary border-b border-border">
                  Accès rapide
                </div>
                <div className="divide-y divide-border max-h-80 overflow-y-auto">
                  {allDioceses.slice(0, 8).map((d) => (
                    <button
                      key={d.id}
                      onClick={() => handleSelectDiocese(d.id)}
                      className={`w-full px-3 py-2.5 text-left hover:bg-secondary transition-colors flex items-center justify-between ${
                        selectedDiocese?.id === d.id ? "bg-secondary" : ""
                      }`}
                    >
                      <div>
                        <div className="text-sm font-medium">{d.nom}</div>
                        <div className="text-xs text-muted-foreground">{d.pays}</div>
                      </div>
                      <ChevronRight className="w-4 h-4 text-muted-foreground" />
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div className="lg:col-span-2">
            {selectedDiocese ? (
              <RapportDiocese data={selectedDiocese} />
            ) : (
              <div className="border border-border rounded-xl p-8 text-center text-muted-foreground">
                <Globe className="w-10 h-10 mx-auto mb-3 opacity-40" />
                <p className="text-sm">Sélectionnez un diocèse pour consulter son rapport pastoral.</p>
                <p className="text-xs mt-1 opacity-60">
                  {apiAvailable
                    ? `${allDioceses.length.toLocaleString("fr-FR")} diocèses disponibles. Recherchez ou sélectionnez dans la liste.`
                    : "L'API semble hors ligne. Vérifiez la connexion."}
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  )
}
