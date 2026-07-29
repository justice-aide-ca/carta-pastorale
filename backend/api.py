#!/usr/bin/env python3
"""
api.py
API FastAPI pour Carta Pastorale.
Chemins absolus pour fonctionner sur Render (Root Directory = backend).
"""
import json
import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(
    title="Carta Pastorale API",
    description="Outil d'observation et de discernement pastoral",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Chemins des données ─────────────────────────────────────────
# Sur Render : Root Directory = backend/ → working dir = /app/backend/
# Les données sont à /app/data/ (au même niveau que backend/)
BASE_DIR = Path(__file__).resolve().parent.parent  # /app/
DATA_DIR = Path(os.environ.get("DATA_DIR", str(BASE_DIR / "data")))
RAPPORTS_DIR = Path(os.environ.get("RAPPORTS_DIR", str(DATA_DIR / "rapports")))
DIOCESES_FILE = Path(os.environ.get("DIOCESES_FILE", str(DATA_DIR / "dioceses_enriched.json")))

print(f"[API] DATA_DIR: {DATA_DIR}")
print(f"[API] RAPPORTS_DIR: {RAPPORTS_DIR}")
print(f"[API] DIOCESES_FILE: {DIOCESES_FILE}")

# ─── Chargement des données ────────────────────────────────────────

dioceses_data: Dict[str, Any] = {}
rapports_index: List[Dict[str, Any]] = []
stats_cache: Optional[Dict[str, Any]] = None

def load_data():
    global dioceses_data, rapports_index, stats_cache
    
    if DIOCESES_FILE.exists():
        with open(DIOCESES_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            dioceses_data = {d['id']: d for d in data.get('dioceses', [])}
        print(f"[API] ✅ {len(dioceses_data)} diocèses chargés")
    else:
        print(f"[API] ⚠️ Fichier introuvable: {DIOCESES_FILE}")
        fallback = DATA_DIR / "dioceses.json"
        if fallback.exists():
            with open(fallback, 'r', encoding='utf-8') as f:
                data = json.load(f)
                dioceses_data = {d['id']: d for d in data.get('dioceses', [])}
            print(f"[API] ✅ {len(dioceses_data)} diocèses chargés (fallback)")
    
    rapports_index.clear()
    if RAPPORTS_DIR.exists():
        for f in sorted(RAPPORTS_DIR.glob("*.json")):
            if f.name == "_index.json":
                continue
            try:
                with open(f, 'r', encoding='utf-8') as fh:
                    r = json.load(fh)
                    rapports_index.append({
                        "id": r.get('id', f.stem),
                        "nom": r.get('nom', ''),
                        "pays": r.get('pays', ''),
                        "continent": r.get('continent', ''),
                        "type": r.get('type', ''),
                        "categorie": r.get('categorie', ''),
                        "catholiques": r.get('indicateurs', {}).get('catholiques'),
                        "pourcentage_catholiques": r.get('indicateurs', {}).get('pourcentage_catholiques'),
                    })
            except Exception as e:
                print(f"[API] ⚠️ Erreur lecture {f}: {e}")
        print(f"[API] ✅ {len(rapports_index)} rapports chargés")
    else:
        print(f"[API] ⚠️ Dossier rapports introuvable: {RAPPORTS_DIR}")
    
    _compute_stats()

def _compute_stats():
    global stats_cache
    if not dioceses_data:
        stats_cache = {"total_dioceses": 0}
        return
    
    dioceses = list(dioceses_data.values())
    from collections import Counter
    
    total_cath = sum(d.get('territoire', {}).get('catholiques', 0) or 0 for d in dioceses)
    total_pretres = sum(d.get('ressources', {}).get('total_pretres', 0) or 0 for d in dioceses)
    
    categories = Counter()
    continents = Counter()
    pays = Counter()
    
    for d in dioceses:
        cat = d.get('categorie', 'inconnu')
        categories[cat] += 1
        continents[d.get('continent', 'inconnu')] += 1
        pays[d.get('pays_nom', 'inconnu')] += 1
    
    stats_cache = {
        "total_dioceses": len(dioceses),
        "total_catholiques": total_cath,
        "total_pretres": total_pretres,
        "par_categories": dict(categories),
        "par_continents": dict(continents),
        "par_pays": dict(pays),
    }

load_data()

# ─── Modèles ─────────────────────────────────────────────────────

class DioceseSummary(BaseModel):
    id: str
    nom: str
    pays: str
    continent: str
    type: str
    categorie: str
    catholiques: Optional[int] = None
    pourcentage_catholiques: Optional[float] = None

# ─── Endpoints ─────────────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "name": "Carta Pastorale API",
        "version": "2.0.0",
        "dioceses_loaded": len(dioceses_data),
        "rapports_loaded": len(rapports_index),
    }

@app.get("/dioceses", response_model=List[DioceseSummary])
def list_dioceses(
    pays: Optional[str] = Query(None),
    continent: Optional[str] = Query(None),
    categorie: Optional[str] = Query(None),
):
    results = rapports_index
    if pays:
        results = [r for r in results if r['pays'].lower() == pays.lower()]
    if continent:
        results = [r for r in results if r['continent'].lower() == continent.lower()]
    if categorie:
        results = [r for r in results if r['categorie'].lower() == categorie.lower()]
    return results

@app.get("/dioceses/{diocese_id}")
def get_diocese(diocese_id: str):
    rapport_path = RAPPORTS_DIR / f"{diocese_id}.json"
    if rapport_path.exists():
        with open(rapport_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    if diocese_id in dioceses_data:
        return dioceses_data[diocese_id]
    raise HTTPException(status_code=404, detail=f"Diocèse '{diocese_id}' non trouvé")

@app.get("/search")
def search(q: str = Query(...)):
    q_lower = q.lower()
    results = [r for r in rapports_index if q_lower in r['nom'].lower() or q_lower in r['pays'].lower()]
    return {"total": len(results), "results": results}

@app.get("/stats")
def get_stats():
    return stats_cache or {"total_dioceses": 0}

@app.get("/continents")
def get_continents():
    return list(set(r['continent'] for r in rapports_index))

@app.get("/countries")
def get_countries():
    return sorted(list(set(r['pays'] for r in rapports_index)))

@app.get("/compare")
def compare(diocese_ids: str = Query(..., description="IDs séparés par des virgules")):
    ids = [id.strip() for id in diocese_ids.split(",")]
    results = []
    for id in ids:
        path = RAPPORTS_DIR / f"{id}.json"
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                results.append(json.load(f))
    return {"compared": len(results), "dioceses": results}

# ─── Static files (frontend) ───────────────────────────────────────

static_candidates = [
    BASE_DIR / "frontend" / "dist",
    BASE_DIR / "Frontend" / "dist",
]
static_dir = None
for candidate in static_candidates:
    if candidate.exists():
        static_dir = candidate
        break

if static_dir:
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
    print(f"[API] ✅ Frontend servi depuis {static_dir}")
else:
    print("[API] ⚠️ Frontend dist/ introuvable")

@app.get("/{path:path}", include_in_schema=False)
def serve_spa(path: str):
    if static_dir:
        index_path = static_dir / "index.html"
        if index_path.exists():
            return FileResponse(str(index_path))
    return {"detail": "Frontend not built"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)