"use client"

import { useState, useEffect } from "react"
import RapportDiocese from "./components/RapportDiocese"
import { RapportDioceseData, DioceseSummary, SearchResult } from "./types"
import { Search, Loader2, Globe, ChevronRight } from "lucide-react"

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

// Données de démo pour le mode statique / fallback
const DEMO_DATA: Record<string, RapportDioceseData> = {
  paris: {
    id: "paris",
    nom: "Archidiocèse de Paris",
    type: "Archidiocèse",
    pays: "France",
    continent: "Europe",
    population_totale: 2161000,
    population_catholique: 1297000,
    pourcentage_catholique: 60.0,
    superficie_km2: 105.4,
    nombre_pretres: 718,
    nombre_pretres_diocesains: 420,
    nombre_pretres_religieux: 298,
    nombre_diacres: 312,
    nombre_seminaristes: 89,
    nombre_parishes: 113,
    nombre_missions: 0,
    nombre_chapelles: 45,
    nombre_religieux_hommes: 1250,
    nombre_religieuses: 3400,
    annee_donnees: 2024,
    idh: 0.903,
    pib_par_habitant: 43500,
    taux_pauvrete: 8.1,
    taux_urbanisation: 81.0,
    indice_liberte_religion: "libre",
    score_persecution: 0,
    contexte_liberte: "Liberté religieuse totale. Laïcité constitutionnelle. Relations État-Église régies par les concordats.",
    defis_liberte: ["Sécularisation avancée", "Désaffection des jeunes", "Entretien du patrimoine"],
    tendances: [
      { annee: 2014, catholiques: 1380000, pretres: 892, seminaristes: 156 },
      { annee: 2019, catholiques: 1340000, pretres: 810, seminaristes: 124 },
      { annee: 2024, catholiques: 1297000, pretres: 718, seminaristes: 89 },
    ],
    indicateurs: [
      { nom: "Catholiques par prêtre", valeur: 1806, unite: "cath./prêtre", ref_monde: 3350, ref_cont: 1800, percentile: 15.0, interpretation: "Ratio favorable. Richesse pastorale à partager, potentiel missionnaire." },
      { nom: "Catholiques par paroisse", valeur: 11478, unite: "cath./paroisse", ref_monde: 6130, percentile: 78.0, interpretation: "Paroisses surchargées. Réflexion sur la création de nouvelles unités pastorales." },
      { nom: "Pourcentage de catholiques", valeur: 60.0, unite: "%", ref_monde: 17.0, ref_cont: 40.0, percentile: 92.0, interpretation: "Catholicisme majoritaire. Enjeu : évangélisation des marginaux et nouvelles formes de sécularisation." },
      { nom: "Taux de vocations", valeur: 12.4, unite: "%", ref_monde: 15.0, ref_cont: 8.0, percentile: 55.0, interpretation: "Dynamique vocationnelle saine. Maintenir l'accompagnement et la qualité de formation." },
      { nom: "Densité pastorale", valeur: 1072.0, unite: "paroisses/1000km²", percentile: 95.0, interpretation: "Densité pastorale exceptionnelle. Territoire très couvert." },
    ],
    pistes: [
      "**Nouvelle évangélisation** : Dans un contexte de sécularisation avancée (60.0% de catholiques mais pratique en déclin), l'approche pastorale doit évoluer. Comment toucher les 'sans-religion' ? Comment proposer une foi crédible et engagée dans la cité ?",
      "**Renforcer la présence des laïcs** : Avec un ratio de 1806 catholiques par prêtre, la structuration des communautés ecclésiales de base et la formation des catéchistes deviennent prioritaires. Comment déléguer davantage de responsabilités pastorales aux laïcs ?",
      "**Pastorale urbaine** : L'urbanisation rapide (81.0%) transforme les territoires. Les paroisses historiques ne correspondent plus aux nouvelles zones d'habitation. Comment anticiper la création de nouvelles communautés en périphérie ?",
    ],
    questions: [
      "Comment les paroisses peuvent-elles devenir des 'maisons d'accueil' pour les personnes en quête de sens ?",
      "Comment structurer des 'mini-paroisses' animées par des laïcs formés dans les zones où un prêtre ne peut passer qu'une fois par mois ?",
    ],
    qualite: "complete",
    sources: ["GCatholic.org", "Annuarium Statisticum Ecclesiae 2024", "World Bank", "ACN International"],
  },
  kinshasa: {
    id: "kinshasa",
    nom: "Archidiocèse de Kinshasa",
    type: "Archidiocèse",
    pays: "RDC",
    continent: "Afrique",
    population_totale: 15000000,
    population_catholique: 9750000,
    pourcentage_catholique: 65.0,
    superficie_km2: 8750,
    nombre_pretres: 1250,
    nombre_pretres_diocesains: 890,
    nombre_pretres_religieux: 360,
    nombre_diacres: 45,
    nombre_seminaristes: 520,
    nombre_parishes: 180,
    nombre_missions: 320,
    nombre_chapelles: 850,
    nombre_religieux_hommes: 2100,
    nombre_religieuses: 6800,
    annee_donnees: 2024,
    idh: 0.481,
    pib_par_habitant: 600,
    taux_pauvrete: 62.0,
    taux_urbanisation: 46.0,
    indice_liberte_religion: "libre",
    score_persecution: 15,
    contexte_liberte: "Liberté religieuse formelle, mais instabilité sécuritaire. L'Église est un pilier social majeur.",
    defis_liberte: ["Conflits armés", "Déplacés massifs", "Pauvreté structurelle", "Infrastructure détruite"],
    tendances: [
      { annee: 2014, catholiques: 7200000, pretres: 980, seminaristes: 380 },
      { annee: 2019, catholiques: 8500000, pretres: 1120, seminaristes: 450 },
      { annee: 2024, catholiques: 9750000, pretres: 1250, seminaristes: 520 },
    ],
    indicateurs: [
      { nom: "Catholiques par prêtre", valeur: 7800, unite: "cath./prêtre", ref_monde: 3350, ref_cont: 5200, percentile: 85.0, interpretation: "Déficit pastoral significatif. Nécessité de renforcer la formation des laïcs et la catéchèse communautaire." },
      { nom: "Catholiques par paroisse", valeur: 54167, unite: "cath./paroisse", ref_monde: 6130, percentile: 98.0, interpretation: "Paroisses surchargées. Réflexion sur la création de nouvelles unités pastorales." },
      { nom: "Pourcentage de catholiques", valeur: 65.0, unite: "%", ref_monde: 17.0, ref_cont: 19.0, percentile: 95.0, interpretation: "Catholicisme majoritaire. Enjeu : évangélisation des marginaux et nouvelles formes de sécularisation." },
      { nom: "Taux de vocations", valeur: 41.6, unite: "%", ref_monde: 15.0, ref_cont: 25.0, percentile: 92.0, interpretation: "Dynamique vocationnelle exceptionnelle. Capitaliser pour l'avenir et partager le modèle." },
      { nom: "Densité pastorale", valeur: 20.6, unite: "paroisses/1000km²", percentile: 25.0, interpretation: "Territoire étendu. Enjeu : moyens de transport et prêtres itinérants." },
    ],
    pistes: [
      "**Renforcer la présence des laïcs** : Avec un ratio de 7800 catholiques par prêtre, la structuration des communautés ecclésiales de base et la formation des catéchistes deviennent prioritaires. Comment déléguer davantage de responsabilités pastorales aux laïcs ?",
      "**Capitaliser sur la dynamique vocationnelle** : Avec 41.6% de séminaristes, ce diocèse est un modèle. Comment partager cette expérience avec d'autres diocèses ? Comment assurer la qualité de la formation malgré les effectifs ?",
      "**Caritas et action sociale** : Dans un contexte de pauvreté élevée (62.0%), l'Église est souvent le dernier filet de sécurité. Comment prioriser les œuvres de charité sans sacrifier la mission proprement spirituelle ?",
      "**Église en persécution** : Avec un score de persécution de 15/100, la survie de la communauté est en jeu. Comment maintenir l'unité et l'espérance ? Comment s'organiser clandestinement si nécessaire ? Comment solliciter la solidarité internationale ?",
    ],
    questions: [
      "Comment structurer des 'mini-paroisses' animées par des laïcs formés dans les zones où un prêtre ne peut passer qu'une fois par mois ?",
      "Quels témoins de vie consacrée peuvent accompagner les jeunes dans la découverte de leur vocation ?",
      "Comment articuler l'annonce de l'Évangile et l'action sociale dans un contexte de pauvreté structurelle ?",
    ],
    qualite: "complete",
    sources: ["GCatholic.org", "Annuarium Statisticum Ecclesiae 2024", "World Bank", "ACN International"],
  },
}

export default function Home() {
  const [searchQuery, setSearchQuery] = useState("")
  const [searchResults, setSearchResults] = useState<DioceseSummary[]>([])
  const [selectedDiocese, setSelectedDiocese] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [apiAvailable, setApiAvailable] = useState(false)
  const [allDioceses, setAllDioceses] = useState<DioceseSummary[]>([])

  // Vérifier si l'API est disponible
  useEffect(() => {
    fetch(`${API_BASE}/`)
      .then((r) => r.ok && setApiAvailable(true))
      .catch(() => setApiAvailable(false))
  }, [])

  // Charger la liste des diocèses
  useEffect(() => {
    if (apiAvailable) {
      fetch(`${API_BASE}/dioceses`)
        .then((r) => r.json())
        .then((data: DioceseSummary[]) => setAllDioceses(data))
        .catch(() => setAllDioceses([]))
    }
  }, [apiAvailable])

  const handleSearch = async () => {
    if (!searchQuery.trim()) return
    setLoading(true)
    try {
      if (apiAvailable) {
        const res = await fetch(`${API_BASE}/search?q=${encodeURIComponent(searchQuery)}`)
        const data: SearchResult = await res.json()
        setSearchResults(data.results)
      } else {
        // Mode fallback : recherche dans les données démo
        const results = Object.values(DEMO_DATA).filter(
          (d) =>
            d.nom.toLowerCase().includes(searchQuery.toLowerCase()) ||
            d.pays.toLowerCase().includes(searchQuery.toLowerCase())
        ).map((d) => ({
          id: d.id,
          nom: d.nom,
          pays: d.pays,
          continent: d.continent,
          type: d.type,
          categorie: d.pourcentage_catholique > 50 ? "etabli" : "emergent",
          description_categorie: "",
          catholiques: d.population_catholique,
          pourcentage_catholiques: d.pourcentage_catholique,
        }))
        setSearchResults(results)
      }
    } catch {
      setSearchResults([])
    } finally {
      setLoading(false)
    }
  }

  const currentData = selectedDiocese
    ? DEMO_DATA[selectedDiocese] || null
    : null

  return (
    <main className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border">
        <div className="max-w-5xl mx-auto px-4 py-5">
          <div className="flex items-center gap-2 mb-1">
            <Globe className="w-5 h-5 text-foreground" />
            <h1 className="text-lg font-medium">Carta Pastorale</h1>
            {!apiAvailable && (
              <span className="ml-2 text-xs px-2 py-0.5 rounded-full bg-amber-50 text-amber-700 border border-amber-200">
                mode démo
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
          {/* Sidebar */}
          <div className="lg:col-span-1 space-y-4">
            {/* Search */}
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
                  className="px-3 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
                >
                  <Search className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Results */}
            {searchResults.length > 0 && (
              <div className="border border-border rounded-xl overflow-hidden">
                <div className="px-3 py-2 text-xs font-medium text-muted-foreground bg-secondary border-b border-border">
                  {searchResults.length} résultat{searchResults.length > 1 ? "s" : ""}
                </div>
                <div className="divide-y divide-border">
                  {searchResults.map((d) => (
                    <button
                      key={d.id}
                      onClick={() => setSelectedDiocese(d.id)}
                      className={`w-full px-3 py-2.5 text-left hover:bg-secondary transition-colors flex items-center justify-between ${
                        selectedDiocese === d.id ? "bg-secondary" : ""
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
                <span className="text-sm">Recherche...</span>
              </div>
            )}

            {/* Quick access */}
            <div className="border border-border rounded-xl overflow-hidden">
              <div className="px-3 py-2 text-xs font-medium text-muted-foreground bg-secondary border-b border-border">
                Accès rapide
              </div>
              <div className="divide-y divide-border">
                {Object.values(DEMO_DATA).map((d) => (
                  <button
                    key={d.id}
                    onClick={() => setSelectedDiocese(d.id)}
                    className={`w-full px-3 py-2.5 text-left hover:bg-secondary transition-colors flex items-center justify-between ${
                      selectedDiocese === d.id ? "bg-secondary" : ""
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

            {/* Stats */}
            {apiAvailable && allDioceses.length > 0 && (
              <div className="border border-border rounded-xl p-3">
                <div className="text-xs font-medium text-muted-foreground mb-2">Base de données</div>
                <div className="text-2xl font-medium tabular-nums">{allDioceses.length}</div>
                <div className="text-xs text-muted-foreground">diocèses indexés</div>
              </div>
            )}
          </div>

          {/* Main content */}
          <div className="lg:col-span-2">
            {currentData ? (
              <RapportDiocese data={currentData} />
            ) : (
              <div className="border border-border rounded-xl p-8 text-center text-muted-foreground">
                <Globe className="w-10 h-10 mx-auto mb-3 opacity-40" />
                <p className="text-sm">Sélectionnez un diocèse pour consulter son rapport pastoral.</p>
                <p className="text-xs mt-1 opacity-60">
                  {apiAvailable
                    ? "L'API est connectée. Recherchez un diocèse dans la barre latérale."
                    : "Mode démo actif. Utilisez les données de Paris ou Kinshasa."}
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  )
}