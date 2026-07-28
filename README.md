Carta Pastorale
Carte pastorale interactive : données, indicateurs et pistes missionnaires pour chaque diocèse du monde.
📁 Structure du projet
plain
Carta-Pastorale/
├── backend/          # API FastAPI + pipeline de données
├── frontend/         # Next.js 14 + Tailwind CSS
├── data/             # Données générées (JSON)
├── docker-compose.yml
└── DEPLOY.md         # Guide de déploiement
🚀 Démarrage rapide
bash
# 1. Cloner / copier le projet
cd Carta-Pastorale

# 2. Lancer le backend
cd backend
pip install -r requirements.txt
python api.py

# 3. Lancer le frontend (autre terminal)
cd frontend
npm install
npm run dev
Frontend : http://localhost:3000
API : http://localhost:8000
📊 Pipeline de données
plain
JSON bruts (GCatholic)
    ↓
consolidator.py      → dioceses.json
    ↓
worldbank_fetcher.py → dioceses_enriched.json
    ↓
contextualizer.py    → rapports/*.json
    ↓
api.py               → REST API
    ↓
RapportDiocese.tsx   → Interface web
📖 Documentation
Guide de déploiement
README Frontend
🛠️ Stack technique
Feuilles de calcul
Couche	Technologie
Scraping	Python + BeautifulSoup
Enrichissement	World Bank API
Contextualisation	Python (règles métier)
API	FastAPI + Uvicorn
Frontend	Next.js 14 + React 18
Styling	Tailwind CSS
Icons	Lucide React
Charts	SVG natif
Déploiement	Vercel (frontend) + Render (API)
📜 Licence
MIT — libre d'utilisation et de modification.