🚀 Guide de déploiement — Carta Pastorale
Architecture déployée
plain
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Vercel    │────▶│   Render    │────▶│  Fichiers   │
│  (Frontend) │     │   (API)     │     │   JSON      │
│   Next.js   │     │   FastAPI   │     │  (rapports) │
└─────────────┘     └─────────────┘     └─────────────┘
Option A : Déploiement gratuit (Recommandé pour commencer)
1. Backend — Render (https://render.com)
Créer un compte Render (gratuit)
New → Web Service
Connecter votre repo GitHub ou uploader les fichiers
Configurer :
Root directory : backend/
Build command : pip install -r requirements.txt
Start command : uvicorn api:app --host 0.0.0.0 --port $PORT
Environment variables :
DATA_DIR = /app/data
RAPPORTS_DIR = /app/data/rapports
DIOCESES_FILE = /app/data/dioceses_enriched.json
Ajouter les données JSON dans le repo (dossier data/)
Deploy → obtenir l'URL (ex: https://carta-pastorale-api.onrender.com)
⚠️ Le free tier de Render "dort" après 15 min d'inactivité. Le premier appel peut prendre 30 sec.
2. Frontend — Vercel (https://vercel.com)
Créer un compte Vercel (gratuit)
Add New Project
Connecter votre repo GitHub
Configurer :
Framework preset : Next.js
Root directory : frontend/
Build command : npm run build
Output directory : dist
Environment variables :
NEXT_PUBLIC_API_URL = https://votre-api-render.onrender.com
Deploy → obtenir l'URL (ex: https://carta-pastorale.vercel.app)
Option B : Docker (auto-hébergé ou VPS)
bash
# À la racine du projet
docker-compose up --build

# Le frontend sera sur http://localhost:3000
# L'API sera sur http://localhost:8000
Option C : Déploiement local (développement)
Terminal 1 — Backend
bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python api.py
# → http://localhost:8000
Terminal 2 — Frontend
bash
cd frontend
npm install
npm run dev
# → http://localhost:3000
🔧 Post-déploiement
Mettre à jour les données
bash
# Relancer le pipeline avec de nouveaux fichiers JSON
cd backend
python run_all.py --raw ../data/raw
# Les rapports sont régénérés dans data/rapports/
# Commit + push → redeploy automatique
Ajouter un pays manquant au mapping
Éditer backend/mapping_pays.py (ou la variable MAPPING_PAYS dans consolidator.py) :
Python
"NouveauPays": {
    "continent": "Europe",
    "wb_code": "XXX",
    "region_wb": "Europe & Central Asia",
    "langue_principale": "français"
}
Puis relancer le pipeline.
🚀 Déploiement automatique avec deploy.sh
Un script bash interactif est fourni pour automatiser tout le workflow.
Utilisation interactive (menu)
bash
./deploy.sh
Menu proposé :
plain
🗺️  Carta Pastorale — Déploiement automatique
═══════════════════════════════════════════════════════════════

  1) Déploiement complet (pipeline + build + push)
  2) Build frontend uniquement
  3) Pipeline données uniquement
  4) Push git uniquement
  5) Vérifier l'état du déploiement
  q) Quitter
Utilisation rapide (ligne de commande)
bash
# Déploiement complet (équivalent au menu option 1)
./deploy.sh --full

# Ou raccourci
./deploy.sh -f

# Pipeline de données uniquement
./deploy.sh --pipeline
./deploy.sh -p

# Build frontend uniquement
./deploy.sh --build
./deploy.sh -b

# Push git uniquement
./deploy.sh --push
Ce que fait le script (mode complet)
Feuilles de calcul
Étape	Action	Temps estimé
1	Vérification des prérequis (git, node, python)	< 1 sec
2	Pipeline de données (si nouveaux JSON dans data/raw/)	10-30 sec
3	Build Next.js (npm run build)	15-45 sec
4	Commit git avec timestamp	< 1 sec
5	Push sur GitHub	2-5 sec
6	Vérification du déploiement Render	5-10 sec
Total		~1-2 min
Prérequis
git configuré avec un remote (GitHub)
node ≥ 18 et npm
python3 ≥ 3.10
Repo initialisé : git init && git remote add origin https://github.com/votre-repo.git
📋 Checklist avant mise en production
[ ] Changer CORS_ORIGINS dans api.py (remplacer ["*"] par votre domaine Vercel)
[ ] Ajouter un rate limiter sur l'API (ex: slowapi)
[ ] Activer HTTPS sur Render (fait automatiquement)
[ ] Configurer un CDN pour les assets statiques (Vercel le fait)
[ ] Monitorer les logs (data/logs/pipeline.log)
[ ] Planifier le re-run du pipeline (cron hebdomadaire)