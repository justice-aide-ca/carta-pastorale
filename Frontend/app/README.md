Carta Pastorale — Frontend
Frontend Next.js 14 pour la visualisation des rapports pastoraux par diocèse.
Architecture
plain
frontend/
├── app/
│   ├── layout.tsx              # Layout racine + polices
│   ├── globals.css             # Tailwind + variables CSS
│   ├── page.tsx                # Page d'accueil (recherche + rapport)
│   ├── types.ts                # Types TypeScript
│   └── components/
│       ├── RapportDiocese.tsx  # Composant rapport complet
│       └── TrendChart.tsx      # Graphique SVG d'évolution
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── postcss.config.js
└── next.config.js
Installation
bash
cd frontend
npm install
Développement
bash
npm run dev
Le frontend sera disponible sur http://localhost:3000.
Build statique
bash
npm run build
Le build statique est généré dans dist/ (configuré via output: 'export').
Connexion à l'API
Par défaut, le frontend tente de se connecter à http://localhost:8000 (API FastAPI).
Pour changer l'URL de l'API :
bash
NEXT_PUBLIC_API_URL=http://mon-api.com npm run dev
En l'absence d'API, le frontend bascule automatiquement en mode démo avec les données de Paris et Kinshasa.
Fonctionnalités
🔍 Recherche de diocèses par nom ou pays
📊 Vue d'ensemble : métriques clés + graphique d'évolution
📈 Indicateurs pastoraux : barres de percentile + références monde/continent
💡 Pistes pastorales contextualisées
❓ Questions de discernement
🛡️ Contexte de liberté religieuse
🏛️ Contexte socio-économique (PIB, IDH, pauvreté)