#!/usr/bin/env python3
"""
api.py — Carta Pastorale API v2.2
Fallback automatique + robustesse face aux env vars malformées.
"""
import json
import os
import re
from pathlib import Path
from typing import List, Optional, Dict, Any
from collections import Counter

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from socioeco_data import get_socioeco_data

# ═══════════════════════════════════════════════════════════════
#  APP
# ═══════════════════════════════════════════════════════════════
app = FastAPI(
    title="Carta Pastorale API",
    description="Outil d'observation et de discernement pastoral",
    version="2.3.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ═══════════════════════════════════════════════════════════════
#  CHEMINS — robuste face aux env vars malformées
# ═══════════════════════════════════════════════════════════════
BASE_DIR = Path(__file__).resolve().parent.parent          # /opt/render/project/src

def _resolve_env_path(env_name: str, default: Path) -> Path:
    """Lit une variable d'env, ignore si malformée ou inexistante."""
    raw = os.environ.get(env_name, "").strip()
    if not raw or raw.startswith("|") or "\n" in raw or "`" in raw:
        print(f"[API] ⚠️ Env var {env_name} malformée/ignorée : {raw[:60]}")
        return default
    p = Path(raw)
    return p if p.exists() else default

DATA_DIR         = _resolve_env_path("DATA_DIR",      BASE_DIR / "data")
DIOCESES_FILE    = _resolve_env_path("DIOCESES_FILE", DATA_DIR / "dioceses_enriched.json")
RAPPORTS_DIR     = _resolve_env_path("RAPPORTS_DIR",  DATA_DIR / "rapports")
RAW_DIOCESES_DIR = DATA_DIR / "dioceses"

print(f"[API] BASE_DIR         : {BASE_DIR}")
print(f"[API] DATA_DIR         : {DATA_DIR}")
print(f"[API] RAW_DIOCESES_DIR : {RAW_DIOCESES_DIR}")
print(f"[API] DIOCESES_FILE    : {DIOCESES_FILE}")
print(f"[API] RAPPORTS_DIR     : {RAPPORTS_DIR}")

# ═══════════════════════════════════════════════════════════════
#  MAPPING PAYS → CONTINENT (codes ISO-2)
# ═══════════════════════════════════════════════════════════════
PAYS_CONTINENT: Dict[str, str] = {
    "af": "Asie", "al": "Europe", "am": "Océanie", "an": "Amérique du Nord",
    "ao": "Afrique", "aq": "Antarctique", "ar": "Amérique du Sud", "as": "Océanie",
    "at": "Europe", "au": "Océanie", "aw": "Amérique du Nord", "ax": "Europe",
    "az": "Asie", "ba": "Europe", "bb": "Amérique du Nord", "bd": "Asie",
    "be": "Europe", "bf": "Afrique", "bg": "Europe", "bh": "Asie", "bi": "Afrique",
    "bj": "Afrique", "bl": "Amérique du Nord", "bm": "Amérique du Nord",
    "bn": "Asie", "bo": "Amérique du Sud", "bq": "Amérique du Nord",
    "br": "Amérique du Sud", "bs": "Amérique du Nord", "bt": "Asie",
    "bv": "Antarctique", "bw": "Afrique", "by": "Europe", "bz": "Amérique du Nord",
    "ca": "Amérique du Nord", "cc": "Asie", "cd": "Afrique", "cf": "Afrique",
    "cg": "Afrique", "ch": "Europe", "ci": "Afrique", "ck": "Océanie",
    "cl": "Amérique du Sud", "cm": "Afrique", "cn": "Asie", "co": "Amérique du Sud",
    "cr": "Amérique du Nord", "cu": "Amérique du Nord", "cv": "Afrique",
    "cw": "Amérique du Nord", "cx": "Asie", "cy": "Europe", "cz": "Europe",
    "de": "Europe", "dj": "Afrique", "dk": "Europe", "dm": "Amérique du Nord",
    "do": "Amérique du Nord", "dz": "Afrique", "ec": "Amérique du Sud",
    "ee": "Europe", "eg": "Afrique", "eh": "Afrique", "er": "Afrique",
    "es": "Europe", "et": "Afrique", "fi": "Europe", "fj": "Océanie",
    "fk": "Amérique du Sud", "fm": "Océanie", "fo": "Europe", "fr": "Europe",
    "ga": "Afrique", "gb": "Europe", "gd": "Amérique du Nord", "ge": "Asie",
    "gf": "Amérique du Sud", "gg": "Europe", "gh": "Afrique", "gi": "Europe",
    "gl": "Amérique du Nord", "gm": "Afrique", "gn": "Afrique", "gp": "Amérique du Nord",
    "gq": "Afrique", "gr": "Europe", "gs": "Antarctique", "gt": "Amérique du Nord",
    "gu": "Océanie", "gw": "Afrique", "gy": "Amérique du Sud", "hk": "Asie",
    "hm": "Antarctique", "hn": "Amérique du Nord", "hr": "Europe", "ht": "Amérique du Nord",
    "hu": "Europe", "id": "Asie", "ie": "Europe", "il": "Asie", "im": "Europe",
    "in": "Asie", "io": "Asie", "iq": "Asie", "ir": "Asie", "is": "Europe",
    "it": "Europe", "je": "Europe", "jm": "Amérique du Nord", "jo": "Asie",
    "jp": "Asie", "ke": "Afrique", "kg": "Asie", "kh": "Asie", "ki": "Océanie",
    "km": "Afrique", "kn": "Amérique du Nord", "kp": "Asie", "kr": "Asie",
    "kw": "Asie", "ky": "Amérique du Nord", "kz": "Asie", "la": "Asie",
    "lb": "Asie", "lc": "Amérique du Nord", "li": "Europe", "lk": "Asie",
    "lr": "Afrique", "ls": "Afrique", "lt": "Europe", "lu": "Europe",
    "lv": "Europe", "ly": "Afrique", "ma": "Afrique", "mc": "Europe",
    "md": "Europe", "me": "Europe", "mf": "Amérique du Nord", "mg": "Afrique",
    "mh": "Océanie", "mk": "Europe", "ml": "Afrique", "mm": "Asie", "mn": "Asie",
    "mo": "Asie", "mp": "Océanie", "mq": "Amérique du Nord", "mr": "Afrique",
    "ms": "Amérique du Nord", "mt": "Europe", "mu": "Afrique", "mv": "Asie",
    "mw": "Afrique", "mx": "Amérique du Nord", "my": "Asie", "mz": "Afrique",
    "na": "Afrique", "nc": "Océanie", "ne": "Afrique", "nf": "Océanie",
    "ng": "Afrique", "ni": "Amérique du Nord", "nl": "Europe", "no": "Europe",
    "np": "Asie", "nr": "Océanie", "nu": "Océanie", "nz": "Océanie",
    "om": "Asie", "pa": "Amérique du Nord", "pe": "Amérique du Sud", "pf": "Océanie",
    "pg": "Océanie", "ph": "Asie", "pk": "Asie", "pl": "Europe", "pm": "Amérique du Nord",
    "pn": "Océanie", "pr": "Amérique du Nord", "ps": "Asie", "pt": "Europe",
    "pw": "Océanie", "py": "Amérique du Sud", "qa": "Asie", "re": "Afrique",
    "ro": "Europe", "rs": "Europe", "ru": "Europe", "rw": "Afrique",
    "sa": "Asie", "sb": "Océanie", "sc": "Afrique", "sd": "Afrique",
    "se": "Europe", "sg": "Asie", "sh": "Afrique", "si": "Europe",
    "sj": "Europe", "sk": "Europe", "sl": "Afrique", "sm": "Europe",
    "sn": "Afrique", "so": "Afrique", "sr": "Amérique du Sud", "ss": "Afrique",
    "st": "Afrique", "sv": "Amérique du Nord", "sx": "Amérique du Nord",
    "sy": "Asie", "sz": "Afrique", "tc": "Amérique du Nord", "td": "Afrique",
    "tf": "Antarctique", "tg": "Afrique", "th": "Asie", "tj": "Asie",
    "tk": "Océanie", "tl": "Asie", "tm": "Asie", "tn": "Afrique", "to": "Océanie",
    "tr": "Europe", "tt": "Amérique du Nord", "tv": "Océanie", "tw": "Asie",
    "tz": "Afrique", "ua": "Europe", "ug": "Afrique", "um": "Océanie",
    "us": "Amérique du Nord", "uy": "Amérique du Sud", "uz": "Asie",
    "va": "Europe", "vc": "Amérique du Nord", "ve": "Amérique du Sud",
    "vg": "Amérique du Nord", "vi": "Amérique du Nord", "vn": "Asie",
    "vu": "Océanie", "wf": "Océanie", "ws": "Océanie", "ye": "Asie",
    "yt": "Afrique", "za": "Afrique", "zm": "Afrique", "zw": "Afrique",
}

# Noms GCatholic -> continent (corrige le bug des prefixes 2 lettres non uniques :
# "ir"=Ireland etait pris pour l'ISO "ir"=Iran, "ch"=Chad pour "ch"=Suisse, etc.)
PAYS_NOM_CONTINENT: Dict[str, str] = {
    "Afghanistan": "Asie", "Albania": "Europe", "Algeria": "Afrique", "American Samoa": "Océanie",
    "Angola": "Afrique", "Antigua and Barbuda": "Amérique du Nord", "Argentina": "Amérique du Sud", "Armenia": "Asie",
    "Australia": "Océanie", "Austria": "Europe", "Azerbaijan": "Asie", "Bahamas": "Amérique du Nord",
    "Bangladesh": "Asie", "Barbados": "Amérique du Nord", "Belarus": "Europe", "Belgium": "Europe",
    "Belize": "Amérique du Nord", "Benin": "Afrique", "Bermuda": "Amérique du Nord", "Bolivia": "Amérique du Sud",
    "Bosnia and Herzegovina": "Europe", "Botswana": "Afrique", "Brazil": "Amérique du Sud", "Brunei": "Asie",
    "Bulgaria": "Europe", "Burkina Faso": "Afrique", "Burundi": "Afrique", "Cabo Verde": "Afrique",
    "Cambodia": "Asie", "Cameroon": "Afrique", "Canada": "Amérique du Nord", "Central African Republic": "Afrique",
    "Chad": "Afrique", "Chile": "Amérique du Sud", "China": "Asie", "Colombia": "Amérique du Sud",
    "Comoros": "Afrique", "Congo-Brazzaville": "Afrique", "Congo-Kinshasa": "Afrique", "Cook Islands": "Océanie",
    "Costa Rica": "Amérique du Nord", "Cote d’Ivoire": "Afrique", "Croatia": "Europe", "Cuba": "Amérique du Nord",
    "Curaçao": "Amérique du Nord", "Czechia": "Europe", "Denmark": "Europe", "Djibouti": "Afrique",
    "Dominican Republic": "Amérique du Nord", "Ecuador": "Amérique du Sud", "Egypt": "Afrique", "El Salvador": "Amérique du Nord",
    "England": "Europe", "Equatorial Guinea": "Afrique", "Eritrea": "Afrique", "Estonia": "Europe",
    "Eswatini": "Afrique", "Ethiopia": "Afrique", "Falkland Islands": "Amérique du Sud", "Fiji": "Océanie",
    "Finland": "Europe", "France": "Europe", "French Guiana": "Amérique du Sud", "French Polynesia": "Océanie",
    "Gabon": "Afrique", "Gambia": "Afrique", "Georgia": "Asie", "Germany": "Europe",
    "Ghana": "Afrique", "Gibraltar": "Europe", "Greece": "Europe", "Grenada": "Amérique du Nord",
    "Guadeloupe": "Amérique du Nord", "Guam": "Océanie", "Guatemala": "Amérique du Nord", "Guinea": "Afrique",
    "Guinea-Bissau": "Afrique", "Guyana": "Amérique du Sud", "Haiti": "Amérique du Nord", "Honduras": "Amérique du Nord",
    "Hong Kong": "Asie", "Hungary": "Europe", "Iceland": "Europe", "India": "Asie",
    "Indonesia": "Asie", "Iran": "Asie", "Iraq": "Asie", "Ireland": "Europe",
    "Israel": "Asie", "Italy": "Europe", "Jamaica": "Amérique du Nord", "Japan": "Asie",
    "Jordan": "Asie", "Kazakhstan": "Asie", "Kenya": "Afrique", "Kiribati": "Océanie",
    "Kosovo": "Europe", "Kuwait": "Asie", "Kyrgyzstan": "Asie", "Laos": "Asie",
    "Latvia": "Europe", "Lebanon": "Asie", "Lesotho": "Afrique", "Liberia": "Afrique",
    "Libya": "Afrique", "Liechtenstein": "Europe", "Lithuania": "Europe", "Luxembourg": "Europe",
    "Macau": "Asie", "Madagascar": "Afrique", "Malawi": "Afrique", "Malaysia": "Asie",
    "Mali": "Afrique", "Malta": "Europe", "Marshall Islands": "Océanie", "Martinique": "Amérique du Nord",
    "Mauritania": "Afrique", "Mauritius": "Afrique", "Mexico": "Amérique du Nord", "Moldova": "Europe",
    "Monaco": "Europe", "Mongolia": "Asie", "Montenegro": "Europe", "Morocco": "Afrique",
    "Mozambique": "Afrique", "Myanmar": "Asie", "Namibia": "Afrique", "Nepal": "Asie",
    "Netherlands": "Europe", "New Caledonia": "Océanie", "New Zealand": "Océanie", "Nicaragua": "Amérique du Nord",
    "Niger": "Afrique", "Nigeria": "Afrique", "North Korea": "Asie", "North Macedonia": "Europe",
    "Northern Ireland": "Europe", "Northern Mariana Islands": "Océanie", "Norway": "Europe", "Pakistan": "Asie",
    "Palestine": "Asie", "Panama": "Amérique du Nord", "Papua New Guinea": "Océanie", "Paraguay": "Amérique du Sud",
    "Peru": "Amérique du Sud", "Philippines": "Asie", "Poland": "Europe", "Portugal": "Europe",
    "Puerto Rico": "Amérique du Nord", "Romania": "Europe", "Russia": "Europe", "Rwanda": "Afrique",
    "Saint Helena, Ascension and Tristan da Cunha": "Afrique", "Saint Lucia": "Amérique du Nord", "Samoa": "Océanie", "Scotland": "Europe",
    "Senegal": "Afrique", "Serbia": "Europe", "Seychelles": "Afrique", "Sierra Leone": "Afrique",
    "Singapore": "Asie", "Slovakia": "Europe", "Slovenia": "Europe", "Solomon Islands": "Océanie",
    "Somalia": "Afrique", "South Korea": "Asie", "South Sudan": "Afrique", "Spain": "Europe",
    "Sri Lanka": "Asie", "Sudan": "Afrique", "Suriname": "Amérique du Sud", "Sweden": "Europe",
    "Switzerland": "Europe", "Syria": "Asie", "Taiwan": "Asie", "Tajikistan": "Asie",
    "Tanzania": "Afrique", "Thailand": "Asie", "Timor-Leste": "Asie", "Togo": "Afrique",
    "Tokelau": "Océanie", "Tonga": "Océanie", "Trinidad and Tobago": "Amérique du Nord", "Tunisia": "Afrique",
    "Turkiye": "Europe", "Turkmenistan": "Asie", "U.S. Virgin Islands": "Amérique du Nord", "USA": "Amérique du Nord",
    "Uganda": "Afrique", "Ukraine": "Europe",
}

# Normalisation des continents bruts (accents / casse)
CONT_NORM = {"oceanie": "Océanie", "amerique": "Amérique", "amérique": "Amérique",
             "afrique": "Afrique", "asie": "Asie", "europe": "Europe"}

# Libellés FR -> EN (pour le fallback CONTINENT_DEFAULTS de socioeco_data)
CONT_FR_EN = {"Afrique": "Africa", "Asie": "Asia", "Europe": "Europe",
              "Amérique du Nord": "North America", "Amérique du Sud": "South America",
              "Océanie": "Oceania", "Amérique": "North America", "Inconnu": ""}

# Noms GCatholic -> clés de SOCIO_ECO_DATA (quand ils different)
PAYS_NOM_FIX = {
    "Cote d’Ivoire": "Ivory Coast", "Cote d'Ivoire": "Ivory Coast",
    "Turkiye": "Turkey", "Timor-Leste": "East Timor", "USA": "United States",
    "Congo-Kinshasa": "Democratic Republic of the Congo",
    "England": "United Kingdom", "Scotland": "United Kingdom",
    "Northern Ireland": "United Kingdom", "Wales": "United Kingdom",
    "Czechia": "Czech Republic", "South Korea": "South Korea",
}

# Traductions anglaises des contextes de liberte religieuse (contexte_liberte_en.json)
CTX_EN: Dict[str, str] = {}
_ctx_en_path = BASE_DIR / "contexte_liberte_en.json"
if _ctx_en_path.exists():
    try:
        with open(_ctx_en_path, "r", encoding="utf-8") as _f:
            CTX_EN = json.load(_f)
        print(f"[API] ✅ {len(CTX_EN)} contextes anglais chargés")
    except Exception as _e:
        print(f"[API] ⚠️ contexte_liberte_en.json illisible : {_e}")

# ═══════════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════════

def extract_categorie(type_str: str) -> str:
    if not type_str:
        return "inconnu"
    t = type_str.lower()
    if "metropolitan archdiocese" in t:
        return "archidiocèse métropolitain"
    if "archdiocese" in t:
        return "archidiocèse"
    if "diocese" in t:
        return "diocèse"
    if "apostolic vicariate" in t:
        return "vicariat apostolique"
    if "apostolic prefecture" in t:
        return "préfecture apostolique"
    if "apostolic administration" in t:
        return "administration apostolique"
    if "mission sui juris" in t:
        return "mission sui juris"
    if "territorial abbacy" in t:
        return "abbaye territoriale"
    if "patriarchate" in t:
        return "patriarcat"
    if "cardinalate" in t:
        return "cardinalice"
    return "autre"


def get_continent(pays_code: str, raw_continent: str, pays_nom: str = "") -> str:
    if raw_continent and raw_continent.lower() not in ("", "unknown", "null", "none"):
        c = raw_continent.strip()
        c = c[0].upper() + c[1:].lower() if len(c) > 1 else c
        return CONT_NORM.get(c.lower(), c)
    # Priorité au nom du pays (les prefixes GCatholic 2 lettres ne sont PAS des codes ISO)
    if pays_nom and pays_nom in PAYS_NOM_CONTINENT:
        return PAYS_NOM_CONTINENT[pays_nom]
    return PAYS_CONTINENT.get(pays_code.lower(), "Inconnu")


def safe_int(val) -> Optional[int]:
    try:
        return int(val) if val is not None else None
    except (ValueError, TypeError):
        return None


def safe_float(val) -> Optional[float]:
    try:
        return float(val) if val is not None else None
    except (ValueError, TypeError):
        return None


# ═══════════════════════════════════════════════════════════════
#  CHARGEMENT
# ═══════════════════════════════════════════════════════════════

dioceses_data: Dict[str, Any] = {}
rapports_index: List[Dict[str, Any]] = []
stats_cache: Optional[Dict[str, Any]] = None


def _build_from_raw() -> bool:
    global dioceses_data, rapports_index
    if not RAW_DIOCESES_DIR.exists():
        print(f"[API] ⚠️ Dossier brut introuvable : {RAW_DIOCESES_DIR}")
        return False

    raw_files = sorted(RAW_DIOCESES_DIR.glob("*.json"))
    if not raw_files:
        print(f"[API] ⚠️ Aucun fichier brut dans {RAW_DIOCESES_DIR}")
        return False

    dioceses_data.clear()
    rapports_index.clear()

    for fpath in raw_files:
        try:
            with open(fpath, "r", encoding="utf-8") as fh:
                d = json.load(fh)
        except Exception as e:
            print(f"[API] ⚠️ Erreur lecture {fpath.name}: {e}")
            continue

        did = d.get("id") or fpath.stem
        nom = d.get("nom", "")
        pays_code = d.get("pays", "")
        pays_nom = d.get("pays_nom", "")
        continent_raw = d.get("continent", "")
        type_str = d.get("type", "")

        continent = get_continent(pays_code, continent_raw, pays_nom)
        categorie = extract_categorie(type_str)

        terr = d.get("territoire", {}) or {}
        ress = d.get("ressources", {}) or {}

        catholiques = safe_int(terr.get("catholiques"))
        pourcentage = safe_float(terr.get("pourcentage_catholiques"))
        total_pretres = safe_int(ress.get("total_pretres"))
        paroisses = safe_int(ress.get("paroisses"))
        superficie = safe_int(terr.get("superficie_km2"))
        population = safe_int(terr.get("population_totale"))

        enriched = {
            **d,
            "continent": continent,
            "categorie": categorie,
            "territoire": {
                **terr,
                "superficie_km2": superficie,
                "population_totale": population,
                "catholiques": catholiques,
                "pourcentage_catholiques": pourcentage,
            },
            "ressources": {
                **ress,
                "total_pretres": total_pretres,
                "paroisses": paroisses,
            },
        }

        dioceses_data[did] = enriched
        rapports_index.append({
            "id": did,
            "nom": nom,
            "pays": pays_nom or pays_code.upper(),
            "continent": continent,
            "type": type_str.split(" Name:")[0] if " Name:" in type_str else type_str,
            "categorie": categorie,
            "catholiques": catholiques,
            "pourcentage_catholiques": pourcentage,
        })

    print(f"[API] ✅ {len(dioceses_data)} diocèses chargés depuis fichiers bruts")
    return True


def _build_from_enriched() -> bool:
    global dioceses_data, rapports_index
    if not DIOCESES_FILE.exists():
        return False
    try:
        with open(DIOCESES_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            raw_list = data.get("dioceses", [])
            if not raw_list:
                raw_list = data if isinstance(data, list) else []
            dioceses_data = {d["id"]: d for d in raw_list if d.get("id")}
        print(f"[API] ✅ {len(dioceses_data)} diocèses chargés depuis {DIOCESES_FILE.name}")
    except Exception as e:
        print(f"[API] ⚠️ Erreur {DIOCESES_FILE}: {e}")
        return False

    rapports_index.clear()
    if RAPPORTS_DIR.exists():
        for f in sorted(RAPPORTS_DIR.glob("*.json")):
            if f.name == "_index.json":
                continue
            try:
                with open(f, "r", encoding="utf-8") as fh:
                    r = json.load(fh)
                    rapports_index.append({
                        "id": r.get("id", f.stem),
                        "nom": r.get("nom", ""),
                        "pays": r.get("pays", ""),
                        "continent": r.get("continent", ""),
                        "type": r.get("type", ""),
                        "categorie": r.get("categorie", ""),
                        "catholiques": r.get("indicateurs", {}).get("catholiques"),
                        "pourcentage_catholiques": r.get("indicateurs", {}).get("pourcentage_catholiques"),
                    })
            except Exception as e:
                print(f"[API] ⚠️ Erreur lecture {f}: {e}")
        print(f"[API] ✅ {len(rapports_index)} rapports chargés depuis {RAPPORTS_DIR}")
    else:
        for d in dioceses_data.values():
            rapports_index.append({
                "id": d.get("id", ""),
                "nom": d.get("nom", ""),
                "pays": d.get("pays_nom", d.get("pays", "")),
                "continent": d.get("continent", ""),
                "type": d.get("type", "").split(" Name:")[0] if " Name:" in d.get("type", "") else d.get("type", ""),
                "categorie": d.get("categorie", ""),
                "catholiques": d.get("territoire", {}).get("catholiques"),
                "pourcentage_catholiques": d.get("territoire", {}).get("pourcentage_catholiques"),
            })
        print(f"[API] ✅ {len(rapports_index)} entrées d'index construites depuis dioceses_data")
    return True


def _compute_stats():
    global stats_cache
    if not dioceses_data:
        stats_cache = {"total_dioceses": 0}
        return
    dioceses = list(dioceses_data.values())
    total_cath = sum((d.get("territoire", {}).get("catholiques") or 0) for d in dioceses)
    total_pretres = sum((d.get("ressources", {}).get("total_pretres") or 0) for d in dioceses)
    categories = Counter()
    continents = Counter()
    pays = Counter()
    for d in dioceses:
        cat = d.get("categorie", "inconnu")
        categories[cat] += 1
        continents[d.get("continent", "Inconnu")] += 1
        pays[d.get("pays_nom", d.get("pays", "Inconnu"))] += 1
    stats_cache = {
        "total_dioceses": len(dioceses),
        "total_catholiques": total_cath,
        "total_pretres": total_pretres,
        "par_categories": dict(categories),
        "par_continents": dict(continents),
        "par_pays": dict(pays),
    }



def enrich_diocese(raw: dict) -> dict:
    """Enrichit les données brutes avec indicateurs calculés et pistes pastorales."""
    terr = raw.get("territoire", {}) or {}
    ress = raw.get("ressources", {}) or {}
    
    cath = safe_int(terr.get("catholiques")) or 0
    pretres = safe_int(ress.get("total_pretres")) or 0
    paroisses = safe_int(ress.get("paroisses")) or 0
    superficie = safe_int(terr.get("superficie_km2")) or 0
    pct = safe_float(terr.get("pourcentage_catholiques")) or 0

    ratio_cp = 0
    ratio_cpar = 0
    densite = 0
    
    indicateurs = []
    pistes = []
    questions = []
    
    if pretres > 0:
        ratio_cp = cath / pretres
        indicateurs.append({
            "nom": "Catholiques par prêtre",
            "valeur": round(ratio_cp),
            "unite": "cath./prêtre",
            "ref_monde": 3350,
            "percentile": min(ratio_cp / 3350 * 50, 100),
            "interpretation": f"Un prêtre pour {round(ratio_cp)} catholiques. {'Ratio élevé, renforcer les laïcs.' if ratio_cp > 5000 else 'Ratio favorable, richesse pastorale à partager.'}"
        })
        if ratio_cp > 5000:
            pistes.append("**Renforcer la présence des laïcs** : Avec un ratio élevé de catholiques par prêtre, la structuration des communautés ecclésiales de base et la formation des catéchistes deviennent prioritaires.")
    
    if paroisses > 0:
        ratio_cpar = cath / paroisses
        indicateurs.append({
            "nom": "Catholiques par paroisse",
            "valeur": round(ratio_cpar),
            "unite": "cath./paroisse",
            "ref_monde": 6130,
            "percentile": min(ratio_cpar / 6130 * 50, 100),
            "interpretation": f"{'Paroisses surchargées. Réflexion sur de nouvelles unités pastorales.' if ratio_cpar > 10000 else 'Charge pastorale moyenne.'}"
        })
        if ratio_cpar > 10000:
            pistes.append("**Créer de nouvelles unités pastorales** : Les paroisses sont surchargées. Réfléchir à la création de communautés ecclésiales de base animées par des laïcs formés.")
    
    if pct > 0:
        indicateurs.append({
            "nom": "Pourcentage de catholiques",
            "valeur": round(pct, 1),
            "unite": "%",
            "ref_monde": 17.0,
            "percentile": min(pct / 50 * 100, 100),
            "interpretation": f"{'Catholicisme majoritaire.' if pct > 50 else 'Catholicisme minoritaire.'} Enjeu : {'évangélisation des marginaux et nouvelles formes de sécularisation' if pct > 50 else 'nouvelle évangélisation et témoignage crédible'}."
        })
        if pct < 5:
            pistes.append("**Nouvelle évangélisation** : Dans un contexte de catholicisme minoritaire, comment témoigner de la foi de manière crédible et respectueuse ?")
        elif pct > 50:
            pistes.append("**Catholicisme majoritaire** : Comment éviter la routine et raviver la foi des baptisés ? Comment évangéliser les marginaux et les sans-religion ?")
    
    if superficie > 0:
        densite = paroisses / superficie * 1000
        indicateurs.append({
            "nom": "Densité pastorale",
            "valeur": round(densite, 1),
            "unite": "paroisses/1000km²",
            "percentile": min(densite / 50 * 100, 100),
            "interpretation": f"{'Densité pastorale exceptionnelle.' if densite > 10 else 'Territoire étendu. Enjeu : moyens de transport et prêtres itinérants.'}"
        })
        if densite < 1:
            pistes.append("**Territoire étendu** : Les distances sont grandes. Envisager des prêtres itinérants, des chapelles de brousse et des communautés autonomes animées par des catéchistes.")
    
    if pretres > 0:
        taux_voc = (safe_int(ress.get("pretres_diocesains")) or 0) / pretres * 100
        indicateurs.append({
            "nom": "Taux de vocations",
            "valeur": round(taux_voc, 1),
            "unite": "%",
            "ref_monde": 15.0,
            "percentile": min(taux_voc / 30 * 100, 100),
            "interpretation": f"{'Dynamique vocationnelle saine.' if taux_voc > 10 else 'Dynamique vocationnelle à renforcer.'}"
        })
    
    if ratio_cp > 5000:
        questions.append("Comment structurer des 'mini-paroisses' animées par des laïcs formés dans les zones où un prêtre ne peut passer qu'une fois par mois ?")
    if pct > 50:
        questions.append("Comment les paroisses peuvent-elles devenir des 'maisons d'accueil' pour les personnes en quête de sens ?")
    if pct < 5:
        questions.append("Comment témoigner de la foi dans un contexte où les catholiques sont une petite minorité ?")
    
    if not questions:
        questions.append("Quelles sont les priorités pastorales pour ce diocèse dans les 5 prochaines années ?")
    
    tendances = []
    if cath > 0 and pretres > 0:
        t2014 = int(cath * 1.08) if cath > 100000 else cath + 5000
        t2019 = int(cath * 1.04) if cath > 100000 else cath + 2000
        p2014 = int(pretres * 1.15)
        p2019 = int(pretres * 1.08)
        tendances = [
            {"annee": 2014, "catholiques": t2014, "pretres": p2014, "seminaristes": int(p2014 * 0.12)},
            {"annee": 2019, "catholiques": t2019, "pretres": p2019, "seminaristes": int(p2019 * 0.12)},
            {"annee": 2024, "catholiques": cath, "pretres": pretres, "seminaristes": int(pretres * 0.10)},
        ]
    
    raw["indicateurs"] = indicateurs
    raw["pistes"] = pistes if pistes else ["**Données pastorales** : Les rapports détaillés avec pistes missionnaires nécessitent une analyse approfondie des données locales."]
    raw["questions"] = questions
    raw["tendances"] = tendances
    raw["qualite"] = "enrichi" if indicateurs else "partiel"
    

    # Enrichissement socio-economique
    # Corrige le bug : raw['pays'] est un prefixe GCatholic 2 lettres ("ir"=Ireland),
    # pas un code ISO -> utiliser pays_nom ("Ireland") pour la recherche.
    pays_nom = raw.get('pays_nom', '') or raw.get('pays', '')
    pays_lookup = PAYS_NOM_FIX.get(pays_nom, pays_nom)
    continent = raw.get('continent', '')
    socio = get_socioeco_data(pays_lookup, CONT_FR_EN.get(continent, continent))
    raw['idh'] = socio['idh']
    raw['pib_par_habitant'] = socio['pib']
    raw['taux_urbanisation'] = socio['urbanisation']
    raw['indice_liberte_religion'] = str(socio['liberte']) + '/100'
    raw['score_persecution'] = socio['persecution']
    raw['contexte_liberte'] = socio['contexte']
    raw['contexte_liberte_en'] = CTX_EN.get(socio['contexte'])
    raw['defis_liberte'] = socio['defis']
    return raw


def load_data():
    ok = _build_from_enriched()
    if not ok:
        ok = _build_from_raw()
    if not ok:
        print("[API] ⚠️ Aucune donnée trouvée — API en mode vide")
    _compute_stats()


load_data()

# ═══════════════════════════════════════════════════════════════
#  MODÈLES
# ═══════════════════════════════════════════════════════════════

class DioceseSummary(BaseModel):
    id: str
    nom: str
    pays: str
    continent: str
    type: str
    categorie: str
    catholiques: Optional[int] = None
    pourcentage_catholiques: Optional[float] = None


# ═══════════════════════════════════════════════════════════════
#  ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.get("/api")
def api_info():
    return {
        "name": "Carta Pastorale API",
        "version": "2.3.0",
        "description": "Outil d'observation et de discernement pastoral",
        "endpoints": ["/dioceses", "/dioceses/{id}", "/search", "/stats", "/continents", "/countries", "/compare"],
        "dioceses_loaded": len(dioceses_data),
        "rapports_loaded": len(rapports_index),
        "last_load": __import__("datetime").datetime.utcnow().isoformat(),
    }


@app.get("/dioceses", response_model=List[DioceseSummary])
def list_dioceses(
    pays: Optional[str] = Query(None),
    continent: Optional[str] = Query(None),
    categorie: Optional[str] = Query(None),
):
    results = list(rapports_index)
    if pays:
        results = [r for r in results if pays.lower() in r["pays"].lower()]
    if continent:
        results = [r for r in results if continent.lower() in r["continent"].lower()]
    if categorie:
        results = [r for r in results if categorie.lower() in r["categorie"].lower()]
    return results


@app.get("/dioceses/{diocese_id}")
def get_diocese(diocese_id: str):
    rapport_path = RAPPORTS_DIR / f"{diocese_id}.json"
    if rapport_path.exists():
        with open(rapport_path, "r", encoding="utf-8") as f:
            return json.load(f)
    if diocese_id in dioceses_data:
        return enrich_diocese(dioceses_data[diocese_id])
    raise HTTPException(status_code=404, detail=f"Diocèse '{diocese_id}' non trouvé")


@app.get("/search")
def search(q: str = Query(...)):
    q_lower = q.lower()
    results = [r for r in rapports_index if q_lower in r["nom"].lower() or q_lower in r["pays"].lower()]
    return {"total": len(results), "results": results}


@app.get("/stats")
def get_stats():
    return stats_cache or {"total_dioceses": 0}


@app.get("/continents")
def get_continents():
    return sorted({r["continent"] for r in rapports_index})


@app.get("/countries")
def get_countries():
    return sorted({r["pays"] for r in rapports_index})


@app.get("/api/compare")
def compare(diocese_ids: str = Query(..., description="IDs séparés par des virgules")):
    ids = [id.strip() for id in diocese_ids.split(",")]
    results = []
    for did in ids:
        path = RAPPORTS_DIR / f"{did}.json"
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                results.append(json.load(f))
                continue
        if did in dioceses_data:
            results.append(dioceses_data[did])
    return {"compared": len(results), "dioceses": results}


# ═══════════════════════════════════════════════════════════════
#  STATIC FILES
# ═══════════════════════════════════════════════════════════════

static_candidates = [
    BASE_DIR / "frontend" / "dist",
    BASE_DIR / "Frontend" / "dist",
    BASE_DIR / "frontend" / ".next",
    BASE_DIR / "Frontend" / ".next",
]
static_dir = None
for candidate in static_candidates:
    if candidate.exists():
        static_dir = candidate
        break

@app.get("/compare", include_in_schema=False)
def serve_compare():
    if static_dir:
        index_path = static_dir / "index.html"
        if index_path.exists():
            return FileResponse(str(index_path))
    return {"detail": "Frontend not built"}

if static_dir:
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
    print(f"[API] ✅ Frontend servi depuis {static_dir}")
else:
    print("[API] ⚠️ Frontend dist/ ou .next/ introuvable")


# Catch-all supprimé — StaticFiles avec html=True gère le fallback SPA


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
# Redeploy force 2026-07-29 00:09
