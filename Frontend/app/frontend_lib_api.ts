"use client"

import { RapportDioceseData, DioceseSummary, SearchResult } from "../types"

const API_BASE = process.env.NEXT_PUBLIC_API_URL || ""

function getBase(): string {
  // En production (Render), l'API est sur le même domaine
  if (typeof window !== "undefined" && window.location.hostname.includes("onrender.com")) {
    return ""
  }
  return API_BASE
}

export async function fetchDioceses(): Promise<DioceseSummary[]> {
  const res = await fetch(`${getBase()}/dioceses`)
  if (!res.ok) throw new Error("Erreur chargement diocèses")
  return res.json()
}

export async function searchDioceses(query: string): Promise<SearchResult> {
  const res = await fetch(`${getBase()}/search?q=${encodeURIComponent(query)}`)
  if (!res.ok) throw new Error("Erreur recherche")
  return res.json()
}

export async function fetchDioceseDetail(id: string): Promise<RapportDioceseData> {
  const res = await fetch(`${getBase()}/dioceses/${id}`)
  if (!res.ok) throw new Error("Diocèse non trouvé")
  const raw = await res.json()
  return mapRawToRapport(raw)
}

function safeNum(val: any): number {
  const n = Number(val)
  return isNaN(n) ? 0 : n
}

function mapRawToRapport(raw: any): RapportDioceseData {
  const terr = raw.territoire || {}
  const ress = raw.ressources || {}

  return {
    id: raw.id || "",
    nom: raw.nom || "Inconnu",
    type: (raw.type || raw.categorie || "Diocèse").split(" Name:")[0],
    pays: raw.pays_nom || raw.pays || "Inconnu",
    continent: raw.continent || "Inconnu",
    population_totale: safeNum(terr.population_totale),
    population_catholique: safeNum(terr.catholiques),
    pourcentage_catholique: safeNum(terr.pourcentage_catholiques),
    superficie_km2: safeNum(terr.superficie_km2),
    nombre_pretres: safeNum(ress.total_pretres),
    nombre_pretres_diocesains: safeNum(ress.pretres_diocesains),
    nombre_pretres_religieux: safeNum(ress.pretres_religieux),
    nombre_diacres: safeNum(ress.diacres_permanents),
    nombre_seminaristes: 0,
    nombre_parishes: safeNum(ress.paroisses),
    nombre_missions: 0,
    nombre_chapelles: 0,
    nombre_religieux_hommes: 0,
    nombre_religieuses: safeNum(ress.religieuses),
    annee_donnees: 2024,
    idh: 0,
    pib_par_habitant: 0,
    taux_pauvrete: 0,
    taux_urbanisation: 0,
    indice_liberte_religion: "inconnu",
    score_persecution: 0,
    contexte_liberte: "Données détaillées non disponibles pour ce diocèse.",
    defis_liberte: [],
    tendances: [],
    indicateurs: [],
    pistes: [
      "**Données pastorales** : Les rapports détaillés avec pistes missionnaires et indicateurs comparés nécessitent une génération spécifique. Les données brutes affichées proviennent de GCatholic.org.",
    ],
    questions: [
      "Comment enrichir les données de ce diocèse avec des indicateurs pastoraux et des pistes missionnaires ?",
    ],
    qualite: "partiel",
    sources: raw.source ? [raw.source] : ["GCatholic.org"],
  }
}