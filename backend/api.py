"""
============================================================
API CARTA PASTORALE — FastAPI
============================================================
Sert les rapports de diocèses au frontend via une API REST.

Usage:
    uvicorn api:app --reload --host 0.0.0.0 --port 8000

Endpoints:
    GET /                    → Info API
    GET /dioceses            → Liste des diocèses (paginée)
    GET /dioceses/{id}       → Rapport complet d'un diocèse
    GET /dioceses/{id}/raw   → Données brutes (sortie du scraper)
    GET /search?q=paris      → Recherche floue
    GET /stats               → Statistiques globales
    GET /continents          → Liste des continents avec stats
    GET /countries           → Liste des pays avec stats
    GET /compare?ids=a,b     → Comparaison de diocèses

Auteur: Carta Pastorale
"""

import json
import os
import re
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ============================================================
# CONFIGURATION
# ============================================================

DATA_DIR = Path(__file__).parent / "data"
RAPPORTS_DIR = DATA_DIR / "rapports"
DIOCESES_JSON = DATA_DIR / "dioceses.json"

app = FastAPI(
    title="Carta Pastorale API",
    description="API d'observation et de discernement pastoral",
    version="2.0.0",
)

# CORS — autorise le frontend Netlify/Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# MODÈLES Pydantic
# ============================================================

class DioceseSummary(BaseModel):
    id: str
    nom: str
    type: str
    pays: str
    continent: str
    population_catholique: Optional[int]
    nombre_pretres: Optional[int]
    catholiques_par_pretre: Optional[float]
    qualite_donnees: str

class SearchResult(BaseModel):
    dioceses: List[DioceseSummary]
    total: int
    query: str

class StatsGlobal(BaseModel):
    total_dioceses: int
    total_pays: int
    total_continents: int
    population_catholique_totale: Optional[int]
    nombre_pretres_total: Optional[int]
    catholiques_par_pretre_moyen: Optional[float]
    dioceses_complets: int
    dioceses_partiels: int
    date_generation: str

# ============================================================
# CACHE EN MÉMOIRE
# ============================================================

class DataStore:
    """Cache des données en mémoire pour performances."""

    def __init__(self):
        self._dioceses_raw: List[Dict] = []
        self._rapports: Dict[str, Dict] = {}
        self._last_load: Optional[datetime] = None
        self._load()

    def _load(self):
        """Charge toutes les données en mémoire."""
        # Données brutes
        if DIOCESES_JSON.exists():
            with open(DIOCESES_JSON, "r", encoding="utf-8") as f:
                self._dioceses_raw = json.load(f)

        # Rapports contextualisés
        if RAPPORTS_DIR.exists():
            for rapport_file in RAPPORTS_DIR.glob("*.json"):
                diocese_id = rapport_file.stem
                try:
                    with open(rapport_file, "r", encoding="utf-8") as f:
                        self._rapports[diocese_id] = json.load(f)
                except Exception:
                    pass

        self._last_load = datetime.now()

    def reload(self):
        """Force le rechargement des données."""
        self._dioceses_raw.clear()
        self._rapports.clear()
        self._load()

    @property
    def dioceses_raw(self) -> List[Dict]:
        return self._dioceses_raw

    @property
    def rapports(self) -> Dict[str, Dict]:
        return self._rapports

    def get_rapport(self, diocese_id: str) -> Optional[Dict]:
        return self._rapports.get(diocese_id)

    def get_raw(self, diocese_id: str) -> Optional[Dict]:
        return next((d for d in self._dioceses_raw if d.get("gcatholic_id") == diocese_id), None)


store = DataStore()

# ============================================================
# ENDPOINTS
# ============================================================

@app.get("/")
def root():
    """Info de l'API."""
    return {
        "name": "Carta Pastorale API",
        "version": "2.0.0",
        "description": "Outil d'observation et de discernement pastoral",
        "endpoints": [
            "/dioceses",
            "/dioceses/{id}",
            "/search",
            "/stats",
            "/continents",
            "/countries",
            "/compare",
        ],
        "dioceses_loaded": len(store.dioceses_raw),
        "rapports_loaded": len(store.rapports),
        "last_load": store._last_load.isoformat() if store._last_load else None,
    }


@app.get("/dioceses")
def list_dioceses(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    continent: Optional[str] = None,
    pays: Optional[str] = None,
    qualite: Optional[str] = None,
):
    """Liste paginée des diocèses avec filtres."""
    dioceses = store.dioceses_raw

    # Filtres
    if continent:
        dioceses = [d for d in dioceses if continent.lower() in (d.get("continent", "")).lower()]
    if pays:
        dioceses = [d for d in dioceses if pays.lower() in (d.get("pays", "")).lower()]
    if qualite:
        dioceses = [d for d in dioceses if d.get("statut_extraction", "").lower() == qualite.lower()]

    # Pagination
    total = len(dioceses)
    start = (page - 1) * per_page
    end = start + per_page
    page_data = dioceses[start:end]

    # Résumé
    results = []
    for d in page_data:
        pop_cath = d.get("population_catholique")
        pretres = d.get("nombre_pretres")
        ratio = round(pop_cath / pretres, 1) if pop_cath and pretres and pretres > 0 else None

        results.append({
            "id": d.get("gcatholic_id", ""),
            "nom": d.get("nom", ""),
            "type": d.get("type", ""),
            "pays": d.get("pays", ""),
            "continent": d.get("continent", ""),
            "population_catholique": pop_cath,
            "nombre_pretres": pretres,
            "catholiques_par_pretre": ratio,
            "qualite_donnees": d.get("statut_extraction", "unknown"),
        })

    return {
        "dioceses": results,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": (total + per_page - 1) // per_page,
        },
    }


@app.get("/dioceses/{diocese_id}")
def get_rapport(diocese_id: str):
    """Rapport contextualisé complet d'un diocèse."""
    rapport = store.get_rapport(diocese_id)
    if not rapport:
        raise HTTPException(status_code=404, detail=f"Diocèse {diocese_id} non trouvé")
    return rapport


@app.get("/dioceses/{diocese_id}/raw")
def get_raw(diocese_id: str):
    """Données brutes (sortie du scraper) d'un diocèse."""
    raw = store.get_raw(diocese_id)
    if not raw:
        raise HTTPException(status_code=404, detail=f"Diocèse {diocese_id} non trouvé")
    return raw


@app.get("/search")
def search(q: str = Query(..., min_length=2)):
    """Recherche floue dans les diocèses."""
    query = q.lower()
    results = []

    for d in store.dioceses_raw:
        score = 0
        nom = (d.get("nom", "") or "").lower()
        pays = (d.get("pays", "") or "").lower()
        continent = (d.get("continent", "") or "").lower()
        diocese_id = (d.get("gcatholic_id", "") or "").lower()

        if query in nom:
            score += 10
        if query in pays:
            score += 5
        if query in continent:
            score += 3
        if query in diocese_id:
            score += 2

        # Fuzzy matching simple
        if any(part in nom for part in query.split()):
            score += 3

        if score > 0:
            pop_cath = d.get("population_catholique")
            pretres = d.get("nombre_pretres")
            ratio = round(pop_cath / pretres, 1) if pop_cath and pretres and pretres > 0 else None

            results.append({
                "id": d.get("gcatholic_id", ""),
                "nom": d.get("nom", ""),
                "type": d.get("type", ""),
                "pays": d.get("pays", ""),
                "continent": d.get("continent", ""),
                "population_catholique": pop_cath,
                "nombre_pretres": pretres,
                "catholiques_par_pretre": ratio,
                "qualite_donnees": d.get("statut_extraction", "unknown"),
                "score": score,
            })

    # Trie par score décroissant
    results.sort(key=lambda x: x["score"], reverse=True)

    return {
        "dioceses": results[:20],  # Max 20 résultats
        "total": len(results),
        "query": q,
    }


@app.get("/stats")
def get_stats():
    """Statistiques globales."""
    dioceses = store.dioceses_raw

    total_cath = sum(d.get("population_catholique", 0) or 0 for d in dioceses)
    total_pretres = sum(d.get("nombre_pretres", 0) or 0 for d in dioceses)
    ratio_moyen = round(total_cath / total_pretres, 1) if total_pretres > 0 else None

    pays_set = set(d.get("pays", "") for d in dioceses if d.get("pays"))
    continent_set = set(d.get("continent", "") for d in dioceses if d.get("continent"))

    complets = sum(1 for d in dioceses if d.get("statut_extraction") == "success")
    partiels = sum(1 for d in dioceses if d.get("statut_extraction") == "partial")

    return {
        "total_dioceses": len(dioceses),
        "total_pays": len(pays_set),
        "total_continents": len(continent_set),
        "population_catholique_totale": total_cath if total_cath > 0 else None,
        "nombre_pretres_total": total_pretres if total_pretres > 0 else None,
        "catholiques_par_pretre_moyen": ratio_moyen,
        "dioceses_complets": complets,
        "dioceses_partiels": partiels,
        "date_generation": store._last_load.isoformat() if store._last_load else None,
    }


@app.get("/continents")
def get_continents():
    """Stats par continent."""
    from collections import defaultdict
    stats = defaultdict(lambda: {"count": 0, "catholiques": 0, "pretres": 0})

    for d in store.dioceses_raw:
        cont = d.get("continent", "Inconnu")
        stats[cont]["count"] += 1
        stats[cont]["catholiques"] += d.get("population_catholique", 0) or 0
        stats[cont]["pretres"] += d.get("nombre_pretres", 0) or 0

    results = []
    for cont, s in sorted(stats.items()):
        ratio = round(s["catholiques"] / s["pretres"], 1) if s["pretres"] > 0 else None
        results.append({
            "continent": cont,
            "nombre_dioceses": s["count"],
            "population_catholique": s["catholiques"] if s["catholiques"] > 0 else None,
            "nombre_pretres": s["pretres"] if s["pretres"] > 0 else None,
            "catholiques_par_pretre": ratio,
        })

    return {"continents": results}


@app.get("/countries")
def get_countries():
    """Stats par pays."""
    from collections import defaultdict
    stats = defaultdict(lambda: {"count": 0, "catholiques": 0, "pretres": 0, "continent": ""})

    for d in store.dioceses_raw:
        pays = d.get("pays", "Inconnu")
        stats[pays]["count"] += 1
        stats[pays]["catholiques"] += d.get("population_catholique", 0) or 0
        stats[pays]["pretres"] += d.get("nombre_pretres", 0) or 0
        if not stats[pays]["continent"]:
            stats[pays]["continent"] = d.get("continent", "")

    results = []
    for pays, s in sorted(stats.items()):
        ratio = round(s["catholiques"] / s["pretres"], 1) if s["pretres"] > 0 else None
        results.append({
            "pays": pays,
            "continent": s["continent"],
            "nombre_dioceses": s["count"],
            "population_catholique": s["catholiques"] if s["catholiques"] > 0 else None,
            "nombre_pretres": s["pretres"] if s["pretres"] > 0 else None,
            "catholiques_par_pretre": ratio,
        })

    return {"countries": results}


@app.get("/compare")
def compare_dioceses(ids: str = Query(..., description="IDs séparés par des virgules")):
    """Compare plusieurs diocèses."""
    id_list = [id.strip() for id in ids.split(",")]

    results = []
    for diocese_id in id_list[:5]:  # Max 5 comparaisons
        rapport = store.get_rapport(diocese_id)
        if rapport:
            results.append({
                "id": diocese_id,
                "nom": rapport.get("nom", ""),
                "pays": rapport.get("pays", ""),
                "continent": rapport.get("continent", ""),
                "population_catholique": rapport.get("population_catholique"),
                "nombre_pretres": rapport.get("nombre_pretres"),
                "catholiques_par_pretre": next(
                    (i.get("valeur") for i in rapport.get("indicateurs", []) if i.get("nom") == "Catholiques par prêtre"),
                    None
                ),
                "pourcentage_catholique": next(
                    (i.get("valeur") for i in rapport.get("indicateurs", []) if i.get("nom") == "Pourcentage de catholiques"),
                    None
                ),
                "idh": rapport.get("idh"),
                "score_persecution": rapport.get("score_persecution"),
            })

    return {"comparison": results}


@app.post("/reload")
def reload_data():
    """Force le rechargement des données (après une mise à jour)."""
    store.reload()
    return {
        "message": "Données rechargées",
        "dioceses_loaded": len(store.dioceses_raw),
        "rapports_loaded": len(store.rapports),
        "last_load": store._last_load.isoformat() if store._last_load else None,
    }


# ============================================================
# LANCEMENT
# ============================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)