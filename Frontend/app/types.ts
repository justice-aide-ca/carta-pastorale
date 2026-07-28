export interface Indicateur {
  nom: string
  valeur: number
  unite: string
  ref_monde?: number
  ref_cont?: number
  percentile?: number
  interpretation: string
}

export interface Tendance {
  annee: number
  catholiques: number
  pretres: number
  seminaristes: number
}

export interface RapportDioceseData {
  id: string
  nom: string
  type: string
  pays: string
  continent: string
  population_totale: number
  population_catholique: number
  pourcentage_catholique: number
  superficie_km2: number
  nombre_pretres: number
  nombre_pretres_diocesains: number
  nombre_pretres_religieux: number
  nombre_diacres: number
  nombre_seminaristes: number
  nombre_parishes: number
  nombre_missions: number
  nombre_chapelles: number
  nombre_religieux_hommes: number
  nombre_religieuses: number
  annee_donnees: number
  idh: number
  pib_par_habitant: number
  taux_pauvrete: number
  taux_urbanisation: number
  indice_liberte_religion: string
  score_persecution: number
  contexte_liberte: string
  defis_liberte: string[]
  tendances: Tendance[]
  indicateurs: Indicateur[]
  pistes: string[]
  questions: string[]
  qualite: string
  sources: string[]
}

export interface DioceseSummary {
  id: string
  nom: string
  pays: string
  continent: string
  type: string
  categorie: string
  description_categorie: string
  catholiques?: number
  pourcentage_catholiques?: number
}

export interface SearchResult {
  total: number
  page: number
  per_page: number
  results: DioceseSummary[]
}