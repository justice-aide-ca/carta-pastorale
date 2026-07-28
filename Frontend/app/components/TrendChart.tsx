"use client"

import { Tendance } from "../types"

interface TrendChartProps {
  tendances: Tendance[]
}

function fmt(n: number): string {
  if (n >= 1_000_000) return (n / 1_000_000).toFixed(1).replace(".0", "") + "M"
  if (n >= 1_000) return (n / 1_000).toFixed(1).replace(".0", "") + "K"
  return n.toString()
}

export default function TrendChart({ tendances }: TrendChartProps) {
  const years = tendances.map((t) => t.annee)
  const cath = tendances.map((t) => t.catholiques)
  const pret = tendances.map((t) => t.pretres)
  const sem = tendances.map((t) => t.seminaristes)

  const maxC = Math.max(...cath)
  const maxP = Math.max(...pret)
  const maxS = Math.max(...sem)

  const w = 600
  const h = 180
  const pad = { t: 20, r: 20, b: 30, l: 50 }
  const gw = w - pad.l - pad.r
  const gh = h - pad.t - pad.b

  const x = (i: number) => pad.l + (i / (years.length - 1)) * gw
  const yC = (v: number) => pad.t + gh - (v / maxC) * gh
  const yP = (v: number) => pad.t + gh - (v / maxP) * gh
  const yS = (v: number) => pad.t + gh - (v / maxS) * gh

  const path = (vals: number[], yFn: (v: number) => number) =>
    vals.map((v, i) => `${i === 0 ? "M" : "L"} ${x(i)} ${yFn(v)}`).join(" ")

  return (
    <div className="w-full">
      <svg viewBox={`0 0 ${w} ${h}`} className="w-full h-auto">
        <g stroke="hsl(var(--border))" strokeWidth={0.5}>
          <line x1={pad.l} y1={pad.t} x2={pad.l} y2={h - pad.b} />
          <line x1={pad.l} y1={h - pad.b} x2={w - pad.r} y2={h - pad.b} />
        </g>
        {years.map((yr, i) => (
          <text
            key={yr}
            x={x(i)}
            y={h - 8}
            textAnchor="middle"
            fontSize={11}
            fill="hsl(var(--muted-foreground))"
          >
            {yr}
          </text>
        ))}
        <text
          x={pad.l - 8}
          y={pad.t + 5}
          textAnchor="end"
          fontSize={10}
          fill="hsl(var(--muted-foreground))"
        >
          {fmt(maxC)}
        </text>
        <text
          x={pad.l - 8}
          y={h - pad.b}
          textAnchor="end"
          fontSize={10}
          fill="hsl(var(--muted-foreground))"
        >
          0
        </text>

        <path
          d={path(cath, yC)}
          fill="none"
          stroke="#2563eb"
          strokeWidth={2.5}
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        <path
          d={path(pret, yP)}
          fill="none"
          stroke="#dc2626"
          strokeWidth={2.5}
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeDasharray="6,4"
        />
        <path
          d={path(sem, yS)}
          fill="none"
          stroke="#16a34a"
          strokeWidth={2.5}
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeDasharray="3,3"
        />

        {tendances.map((t, i) => (
          <g key={t.annee}>
            <circle cx={x(i)} cy={yC(t.catholiques)} r={4} fill="#2563eb" />
            <circle cx={x(i)} cy={yP(t.pretres)} r={4} fill="#dc2626" />
            <circle cx={x(i)} cy={yS(t.seminaristes)} r={4} fill="#16a34a" />
          </g>
        ))}
      </svg>
      <div className="flex justify-center gap-6 mt-2.5 text-xs text-muted-foreground">
        <span className="flex items-center gap-1">
          <span className="w-2 h-2 rounded-sm bg-blue-600" />
          catholiques
        </span>
        <span className="flex items-center gap-1">
          <span className="w-2 h-2 rounded-sm bg-red-600" />
          prêtres
        </span>
        <span className="flex items-center gap-1">
          <span className="w-2 h-2 rounded-sm bg-green-600" />
          séminaristes
        </span>
      </div>
    </div>
  )
}