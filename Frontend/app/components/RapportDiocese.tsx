"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { RapportDioceseData } from "../types"
import { useI18n } from "../i18n/context"
import TrendChart from "./TrendChart"
import {
  Users, Church, MapPin, GraduationCap, BookOpen, Shield,
  TrendingUp, AlertTriangle, Lightbulb, HelpCircle, Globe,
  DollarSign, Heart, Building2, Cross, Scale, Info, ArrowLeftRight,
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
  "bg-blue-50 text-blue-600", "bg-red-50 text-red-600",
  "bg-green-50 text-green-600", "bg-purple-50 text-purple-600", "bg-gray-50 text-gray-600",
]
const BAR_COLORS = ["bg-blue-600", "bg-red-600", "bg-green-600", "bg-purple-600", "bg-gray-500"]

export default function RapportDiocese({ data }: RapportDioceseProps) {
  const { t, lang } = useI18n()
  const router = useRouter()
  const [activeTab, setActiveTab] = useState<"overview" | "indicators" | "pastoral" | "context">("overview")

  const liberteScore = typeof data.indice_liberte_religion === 'string'
    ? parseInt(data.indice_liberte_religion.split('/')[0])
    : (data.indice_liberte_religion || 0);

  const liberteStatus =
    liberteScore >= 80
      ? { label: t.diocese.freedom, color: "text-green-600", bg: "bg-green-50" }
      : liberteScore >= 50
      ? { label: t.diocese.freedom, color: "text-amber-600", bg: "bg-amber-50" }
      : { label: t.diocese.freedom, color: "text-red-600", bg: "bg-red-50" }

  const identityCards = [
    { label: t.diocese.catholics, value: fmt(data.population_catholique), sub: data.population_totale > 0 ? `${data.pourcentage_catholique.toFixed(1)}% de ${fmt(data.population_totale)}` : "—", icon: Users },
    { label: t.diocese.priests, value: data.nombre_pretres > 0 ? data.nombre_pretres.toString() : "—", sub: `${data.nombre_pretres_diocesains} + ${data.nombre_pretres_religieux}`, icon: Cross },
    { label: t.diocese.parishes, value: data.nombre_parishes > 0 ? data.nombre_parishes.toString() : "—", sub: `${data.nombre_missions} missions · ${data.nombre_chapelles} chapelles`, icon: Church },
    { label: t.diocese.seminarians, value: data.nombre_seminaristes > 0 ? data.nombre_seminaristes.toString() : "—", sub: `${data.nombre_diacres} diacres`, icon: GraduationCap },
    { label: t.diocese.religious, value: (data.nombre_religieux_hommes + data.nombre_religieuses) > 0 ? (data.nombre_religieux_hommes + data.nombre_religieuses).toString() : "—", sub: `${data.nombre_religieux_hommes} H · ${data.nombre_religieuses} F`, icon: Heart },
    { label: t.diocese.area, value: data.superficie_km2 >= 1000 ? (data.superficie_km2 / 1000).toFixed(1) + "K" : data.superficie_km2 > 0 ? data.superficie_km2.toString() : "—", sub: `km²`, icon: MapPin },
  ]

  const socioCards = [
    { label: "PIB/hab", value: data.pib_par_habitant > 0 ? `$${fmt(data.pib_par_habitant)}` : "—", icon: DollarSign },
    { label: "IDH", value: data.idh > 0 ? data.idh.toFixed(3) : "—", icon: TrendingUp },
    { label: t.diocese.priests, value: data.taux_pauvrete > 0 ? `${data.taux_pauvrete}%` : "—", icon: AlertTriangle },
    { label: t.diocese.year, value: data.annee_donnees.toString(), icon: BookOpen },
  ]

  const hasTendances = data.tendances && data.tendances.length > 0
  const hasIndicateurs = data.indicateurs && data.indicateurs.length > 0
  const hasPistes = data.pistes && data.pistes.length > 0
  const hasQuestions = data.questions && data.questions.length > 0

  return (
    <div className="max-w-3xl mx-auto">
      <div className="mb-6">
        <div className="flex items-center gap-2 text-sm text-muted-foreground mb-1">
          <Globe className="w-3.5 h-3.5" />
          <span>{data.continent}</span>
          <span className="text-border">·</span>
          <MapPin className="w-3.5 h-3.5" />
          <span>{data.pays}</span>
          <span className="text-border">·</span>
          <span className="px-2 py-0.5 rounded-md bg-secondary text-secondary-foreground text-xs font-medium">{data.type}</span>
          {data.qualite === "partiel" && (
            <span className="px-2 py-0.5 rounded-md bg-amber-50 text-amber-700 text-xs font-medium border border-amber-200">{t.diocese.partial}</span>
          )}
        </div>
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-medium tracking-tight">{data.nom}</h1>
          <button
            onClick={() => router.push(`/compare?ids=${data.id}`)}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs rounded-lg border border-border bg-secondary text-secondary-foreground hover:bg-secondary/80"
          >
            <ArrowLeftRight className="w-3.5 h-3.5" />
            {t.diocese.compareWith}
          </button>
        </div>
      </div>

      <div className="flex gap-1 mb-6 border-b border-border">
        {([
          { id: "overview", label: t.diocese.overview },
          { id: "indicators", label: t.diocese.indicators },
          { id: "pastoral", label: t.diocese.pastoral },
          { id: "context", label: t.diocese.context },
        ] as const).map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2.5 text-sm font-medium border-b-2 transition-colors ${
              activeTab === tab.id ? "border-foreground text-foreground" : "border-transparent text-muted-foreground hover:text-foreground"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {activeTab === "overview" && (
        <div className="space-y-6">
          <div className="grid grid-cols-3 gap-3">
            {identityCards.map((card) => (
              <div key={card.label} className="border border-border rounded-xl p-3.5 text-center">
                <div className="text-xs text-muted-foreground mb-1 lowercase">{card.label}</div>
                <div className="text-xl font-medium tabular-nums">{card.value}</div>
                <div className="text-xs text-muted-foreground mt-0.5">{card.sub}</div>
              </div>
            ))}
          </div>
          {hasTendances ? (
            <div>
              <h2 className="text-base font-medium mb-3">{t.diocese.evolution}</h2>
              <div className="border border-border rounded-xl p-4"><TrendChart tendances={data.tendances} /></div>
            </div>
          ) : (
            <div className="border border-border rounded-xl p-6 text-center text-muted-foreground">
              <Info className="w-6 h-6 mx-auto mb-2 opacity-40" />
              <p className="text-sm">{t.diocese.notAvailable}</p>
            </div>
          )}
          <div className="grid grid-cols-4 gap-3">
            {socioCards.map((card) => (
              <div key={card.label} className="border border-border rounded-xl p-3 text-center">
                <div className="text-xs text-muted-foreground mb-1">{card.label}</div>
                <div className="text-lg font-medium tabular-nums">{card.value}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === "indicators" && (
        <div className="space-y-0">
          {hasIndicateurs ? (
            data.indicateurs.map((ind, i) => {
              const Icon = INDICATOR_ICONS[i % INDICATOR_ICONS.length]
              const pct = Math.min(ind.percentile ?? 50, 100)
              return (
                <div key={ind.nom} className="flex gap-3.5 py-4 border-b border-border last:border-b-0">
                  <div className={`w-9 h-9 rounded-lg flex items-center justify-center shrink-0 mt-0.5 ${INDICATOR_COLORS[i % INDICATOR_COLORS.length]}`}>
                    <Icon className="w-4.5 h-4.5" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex justify-between items-baseline mb-1.5">
                      <span className="text-sm font-medium">{ind.nom}</span>
                      <span className="text-lg font-medium tabular-nums">{ind.valeur.toLocaleString(lang)} <span className="text-sm font-normal text-muted-foreground">{ind.unite}</span></span>
                    </div>
                    <div className="h-1.5 bg-secondary rounded-full overflow-hidden mb-1.5">
                      <div className={`h-full rounded-full ${BAR_COLORS[i % BAR_COLORS.length]}`} style={{ width: `${pct}%`, transition: "width 0.6s ease" }} />
                    </div>
                    <p className="text-sm text-muted-foreground mt-1.5 leading-relaxed">{ind.interpretation}</p>
                  </div>
                </div>
              )
            })
          ) : (
            <div className="border border-border rounded-xl p-8 text-center text-muted-foreground">
              <Info className="w-8 h-8 mx-auto mb-3 opacity-40" />
              <p className="text-sm">{t.diocese.pastoralTracksNotAvailable}</p>
            </div>
          )}
        </div>
      )}

      {activeTab === "pastoral" && (
        <div className="space-y-6">
          <div>
            <h2 className="text-base font-medium mb-3 flex items-center gap-2"><Lightbulb className="w-4 h-4" />{t.diocese.pastoral}</h2>
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
                <p className="text-sm">{t.diocese.notAvailable}</p>
              </div>
            )}
          </div>
          <div>
            <h2 className="text-base font-medium mb-3 flex items-center gap-2"><HelpCircle className="w-4 h-4" />{t.diocese.questions}</h2>
            {hasQuestions ? (
              <div className="space-y-2">
                {data.questions.map((q, i) => (
                  <div key={i} className="bg-secondary rounded-lg px-4 py-3 text-sm text-muted-foreground italic leading-relaxed">{q}</div>
                ))}
              </div>
            ) : (
              <div className="border border-border rounded-xl p-6 text-center text-muted-foreground">
                <Info className="w-6 h-6 mx-auto mb-2 opacity-40" />
                <p className="text-sm">{t.diocese.notAvailable}</p>
              </div>
            )}
          </div>
        </div>
      )}

      {activeTab === "context" && (
        <div className="space-y-6">
          <div>
            <h2 className="text-base font-medium mb-3 flex items-center gap-2"><Shield className="w-4 h-4" />{t.diocese.freedom}</h2>
            <div className="border border-border rounded-xl p-4">
              <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-medium mb-3 ${liberteStatus.bg} ${liberteStatus.color}`}>
                {liberteStatus.label} · score {data.indice_liberte_religion}/100
              </span>
              <p className="text-sm text-muted-foreground leading-relaxed">{data.contexte_liberte}</p>
              {data.defis_liberte.length > 0 && (
                <ul className="mt-3 space-y-1">
                  {data.defis_liberte.map((def, i) => (
                    <li key={i} className="text-xs text-muted-foreground pl-4 relative"><span className="absolute left-0 text-border">—</span>{def}</li>
                  ))}
                </ul>
              )}
            </div>
          </div>
          <div>
            <h2 className="text-base font-medium mb-3 flex items-center gap-2"><Building2 className="w-4 h-4" />{t.diocese.socioEconomic}</h2>
            <div className="grid grid-cols-4 gap-3">
              {socioCards.map((card) => (
                <div key={card.label} className="border border-border rounded-xl p-3 text-center">
                  <div className="text-xs text-muted-foreground mb-1">{card.label}</div>
                  <div className="text-lg font-medium tabular-nums">{card.value}</div>
                </div>
              ))}
            </div>
          </div>
          <div className="text-xs text-muted-foreground pt-3 border-t border-border">{t.diocese.sources} : {data.sources.join(" · ")}</div>
        </div>
      )}
    </div>
  )
}
