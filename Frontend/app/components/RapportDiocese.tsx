"use client"

import { useState } from "react"
import { RapportDioceseData } from "../types"
import TrendChart from "./TrendChart"
import {
  Users,
  Church,
  MapPin,
  GraduationCap,
  BookOpen,
  Shield,
  TrendingUp,
  AlertTriangle,
  Lightbulb,
  HelpCircle,
  Globe,
  DollarSign,
  Heart,
  Building2,
  Cross,
  Scale,
  Info,
} from "lucide-react"

interface RapportDioceseProps {
  data: RapportDioceseData
}

function fmt(n: number): string {
  if (n >= 1_000_000) return (n / 1_000_000).toFixed(1).replace(".0", "") + "M"
  if (n >= 1_000) return (n / 1_000).toFixed(1).replace(".0", "") + "K"
  return n.toLocaleString("fr-FR")
}

const INDICATOR_ICONS = [Users, Church, Scale, GraduationCap, MapPin]
const INDICATOR_COLORS = [
  "bg-blue-50 text-blue-600",
  "bg-red-50 text-red-600",
  "bg-green-50 text-green-600",
  "bg-purple-50 text-purple-600",
  "bg-gray-50 text-gray-600",
]
const BAR_COLORS = ["bg-blue-600", "bg-red-600", "bg-green-600", "bg-purple-600", "bg-gray-500"]

export default function RapportDiocese({ data }: RapportDioceseProps) {
  const [activeTab, setActiveTab] = useState<"overview" | "indicators" | "pastoral" | "context">("overview")

  const liberteStatus =
    data.score_persecution === 0
      ? { label: "Liberté totale", color: "text-green-600", bg: "bg-green-50" }
      : data.score_persecution < 30
      ? { label: "Liberté relative", color: "text-amber-600", bg: "bg-amber-50" }
      : { label: "Persécution active", color: "text-red-600", bg: "bg-red-50" }

  const identityCards = [
    {
      label: "catholiques",
      value: fmt(data.population_catholique),
      sub: data.population_totale > 0
        ? `${data.pourcentage_catholique.toFixed(1)}% de ${fmt(data.population_totale)}`
        : "—",
      icon: Users,
    },
    {
      label: "prêtres",
      value: data.nombre_pretres > 0 ? data.nombre_pretres.toString() : "—",
      sub: data.nombre_pretres > 0
        ? `${data.nombre_pretres_diocesains} diocésains + ${data.nombre_pretres_religieux} religieux`
        : "—",
      icon: Cross,
    },
    {
      label: "paroisses",
      value: data.nombre_parishes > 0 ? data.nombre_parishes.toString() : "—",
      sub: `${data.nombre_missions} missions · ${data.nombre_chapelles} chapelles`,
      icon: Church,
    },
    {
      label: "séminaristes",
      value: data.nombre_seminaristes > 0 ? data.nombre_seminaristes.toString() : "—",
      sub: `${data.nombre_diacres} diacres`,
      icon: GraduationCap,
    },
    {
      label: "religieux",
      value: (data.nombre_religieux_hommes + data.nombre_religieuses) > 0
        ? (data.nombre_religieux_hommes + data.nombre_religieuses).toString()
        : "—",
      sub: `${data.nombre_religieux_hommes} H · ${data.nombre_religieuses} F`,
      icon: Heart,
    },
    {
      label: "superficie",
      value: data.superficie_km2 >= 1000
        ? (data.superficie_km2 / 1000).toFixed(1) + "K"
        : data.superficie_km2 > 0
        ? data.superficie_km2.toString()
        : "—",
      sub: `km² · ${data.taux_urbanisation > 0 ? data.taux_urbanisation + "% urbain" : "—"}`,
      icon: MapPin,
    },
  ]

  const socioCards = [
    { label: "PIB/hab", value: data.pib_par_habitant > 0 ? `$${fmt(data.pib_par_habitant)}` : "—", icon: DollarSign },
    { label: "IDH", value: data.idh > 0 ? data.idh.toFixed(3) : "—", icon: TrendingUp },
    { label: "Pauvreté", value: data.taux_pauvrete > 0 ? `${data.taux_pauvrete}%` : "—", icon: AlertTriangle },
    { label: "Données", value: data.annee_donnees.toString(), icon: BookOpen },
  ]

  const hasTendances = data.tendances && data.tendances.length > 0
  const hasIndicateurs = data.indicateurs && data.indicateurs.length > 0
  const hasPistes = data.pistes && data.pistes.length > 0
  const hasQuestions = data.questions && data.questions.length > 0

  return (
    <div className="max-w-3xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center gap-2 text-sm text-muted-foreground mb-1">
          <Globe className="w-3.5 h-3.5" />
          <span>{data.continent}</span>
          <span className="text-border">·</span>
          <MapPin className="w-3.5 h-3.5" />
          <span>{data.pays}</span>
          <span className="text-border">·</span>
          <span className="px-2 py-0.5 rounded-md bg-secondary text-secondary-foreground text-xs font-medium">
            {data.type}
          </span>
          {data.qualite === "partiel" && (
            <span className="px-2 py-0.5 rounded-md bg-amber-50 text-amber-700 text-xs font-medium border border-amber-200">
              données partielles
            </span>
          )}
        </div>
        <h1 className="text-2xl font-medium tracking-tight">{data.nom}</h1>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 mb-6 border-b border-border">
        {([
          { id: "overview", label: "Vue d'ensemble" },
          { id: "indicators", label: "Indicateurs" },
          { id: "pastoral", label: "Pistes pastorales" },
          { id: "context", label: "Contexte" },
        ] as const).map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2.5 text-sm font-medium border-b-2 transition-colors ${
              activeTab === tab.id
                ? "border-foreground text-foreground"
                : "border-transparent text-muted-foreground hover:text-foreground"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Overview Tab */}
      {activeTab === "overview" && (
        <div className="space-y-6">
          <div className="grid grid-cols-3 gap-3">
            {identityCards.map((card) => (
              <div
                key={card.label}
                className="border border-border rounded-xl p-3.5 text-center"
              >
                <div className="text-xs text-muted-foreground mb-1 lowercase">{card.label}</div>
                <div className="text-xl font-medium tabular-nums">{card.value}</div>
                <div className="text-xs text-muted-foreground mt-0.5">{card.sub}</div>
              </div>
            ))}
          </div>

          {hasTendances ? (
            <div>
              <h2 className="text-base font-medium mb-3">Évolution 2014 – 2024</h2>
              <div className="border border-border rounded-xl p-4">
                <TrendChart tendances={data.tendances} />
              </div>
            </div>
          ) : (
            <div className="border border-border rounded-xl p-6 text-center text-muted-foreground">
              <Info className="w-6 h-6 mx-auto mb-2 opacity-40" />
              <p className="text-sm">Données d'évolution non disponibles pour ce diocèse.</p>
            </div>
          )}

          <div className="grid grid-cols-4 gap-3">
            {socioCards.map((card) => (
              <div
                key={card.label}
                className="border border-border rounded-xl p-3 text-center"
              >
                <div className="text-xs text-muted-foreground mb-1">{card.label}</div>
                <div className="text-lg font-medium tabular-nums">{card.value}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Indicators Tab */}
      {activeTab === "indicators" && (
        <div className="space-y-0">
          {hasIndicateurs ? (
            data.indicateurs.map((ind, i) => {
              const Icon = INDICATOR_ICONS[i % INDICATOR_ICONS.length]
              const pct = Math.min(ind.percentile ?? 50, 100)
              return (
                <div
                  key={ind.nom}
                  className="flex gap-3.5 py-4 border-b border-border last:border-b-0"
                >
                  <div
                    className={`w-9 h-9 rounded-lg flex items-center justify-center shrink-0 mt-0.5 ${INDICATOR_COLORS[i % INDICATOR_COLORS.length]}`}
                  >
                    <Icon className="w-4.5 h-4.5" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex justify-between items-baseline mb-1.5">
                      <span className="text-sm font-medium">{ind.nom}</span>
                      <span className="text-lg font-medium tabular-nums">
                        {ind.valeur.toLocaleString("fr-FR")}{" "}
                        <span className="text-sm font-normal text-muted-foreground">
                          {ind.unite}
                        </span>
                      </span>
                    </div>
                    <div className="h-1.5 bg-secondary rounded-full overflow-hidden mb-1.5">
                      <div
                        className={`h-full rounded-full ${BAR_COLORS[i % BAR_COLORS.length]}`}
                        style={{ width: `${pct}%`, transition: "width 0.6s ease" }}
                      />
                    </div>
                    <div className="text-xs text-muted-foreground">
                      Réf. monde: {ind.ref_monde !== undefined ? ind.ref_monde.toLocaleString("fr-FR") : "—"} ·{" "}
                      Réf. {data.continent.toLowerCase()}: {ind.ref_cont !== undefined ? ind.ref_cont.toLocaleString("fr-FR") : "—"} ·{" "}
                      percentile: {ind.percentile !== undefined ? ind.percentile + "%" : "—"}
                    </div>
                    <p className="text-sm text-muted-foreground mt-1.5 leading-relaxed">
                      {ind.interpretation}
                    </p>
                  </div>
                </div>
              )
            })
          ) : (
            <div className="border border-border rounded-xl p-8 text-center text-muted-foreground">
              <Info className="w-8 h-8 mx-auto mb-3 opacity-40" />
              <p className="text-sm">Indicateurs pastoraux détaillés non disponibles pour ce diocèse.</p>
              <p className="text-xs mt-1 opacity-60">
                Les indicateurs comparés (percentiles, références mondiales) nécessitent une génération de rapport spécifique.
              </p>
            </div>
          )}
        </div>
      )}

      {/* Pastoral Tab */}
      {activeTab === "pastoral" && (
        <div className="space-y-6">
          <div>
            <h2 className="text-base font-medium mb-3 flex items-center gap-2">
              <Lightbulb className="w-4 h-4" />
              Pistes pastorales
            </h2>
            {hasPistes ? (
              <div className="space-y-2">
                {data.pistes.map((piste, i) => {
                  const parts = piste.split(" : ")
                  const title = parts[0].replace(/\*\*/g, "")
                  const body = parts.slice(1).join(" : ")
                  return (
                    <div key={i} className="border border-border rounded-xl p-3.5 text-sm text-muted-foreground leading-relaxed">
                      <span className="font-medium text-foreground">{title}</span> : {body}
                    </div>
                  )
                })}
              </div>
            ) : (
              <div className="border border-border rounded-xl p-6 text-center text-muted-foreground">
                <Info className="w-6 h-6 mx-auto mb-2 opacity-40" />
                <p className="text-sm">Aucune piste pastorale générée pour ce diocèse.</p>
              </div>
            )}
          </div>

          <div>
            <h2 className="text-base font-medium mb-3 flex items-center gap-2">
              <HelpCircle className="w-4 h-4" />
              Questions pour le discernement
            </h2>
            {hasQuestions ? (
              <div className="space-y-2">
                {data.questions.map((q, i) => (
                  <div
                    key={i}
                    className="bg-secondary rounded-lg px-4 py-3 text-sm text-muted-foreground italic leading-relaxed"
                  >
                    {q}
                  </div>
                ))}
              </div>
            ) : (
              <div className="border border-border rounded-xl p-6 text-center text-muted-foreground">
                <Info className="w-6 h-6 mx-auto mb-2 opacity-40" />
                <p className="text-sm">Aucune question de discernement pour ce diocèse.</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Context Tab */}
      {activeTab === "context" && (
        <div className="space-y-6">
          <div>
            <h2 className="text-base font-medium mb-3 flex items-center gap-2">
              <Shield className="w-4 h-4" />
              Liberté religieuse
            </h2>
            <div className="border border-border rounded-xl p-4">
              <span
                className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-medium mb-3 ${liberteStatus.bg} ${liberteStatus.color}`}
              >
                {liberteStatus.label} · score {data.score_persecution}/100
              </span>
              <p className="text-sm text-muted-foreground leading-relaxed">
                {data.contexte_liberte}
              </p>
              {data.defis_liberte.length > 0 && (
                <ul className="mt-3 space-y-1">
                  {data.defis_liberte.map((def, i) => (
                    <li
                      key={i}
                      className="text-xs text-muted-foreground pl-4 relative"
                    >
                      <span className="absolute left-0 text-border">—</span>
                      {def}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>

          <div>
            <h2 className="text-base font-medium mb-3 flex items-center gap-2">
              <Building2 className="w-4 h-4" />
              Contexte socio-économique
            </h2>
            <div className="grid grid-cols-4 gap-3">
              {socioCards.map((card) => (
                <div
                  key={card.label}
                  className="border border-border rounded-xl p-3 text-center"
                >
                  <div className="text-xs text-muted-foreground mb-1">{card.label}</div>
                  <div className="text-lg font-medium tabular-nums">{card.value}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="text-xs text-muted-foreground pt-3 border-t border-border">
            Sources : {data.sources.join(" · ")}
          </div>
        </div>
      )}
    </div>
  )
}