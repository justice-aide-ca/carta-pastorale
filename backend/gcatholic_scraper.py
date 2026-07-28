"""
============================================================
GCATHOLIC SCRAPER — Carta Pastorale
============================================================
Scraper structuré et respectueux pour extraire les données
de tous les diocèses listés sur GCatholic.org.

Usage:
    python gcatholic_scraper.py --output data/dioceses.json
    python gcatholic_scraper.py --resume --output data/dioceses.json
    python gcatholic_scraper.py --diocese pari0 --output data/paris.json

Auteur: Carta Pastorale
"""

import requests
import json
import csv
import time
import re
import os
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# ============================================================
# CONFIGURATION
# ============================================================
BASE_URL = "https://www.gcatholic.org"
DIOCESES_LIST_URL = "https://www.gcatholic.org/dioceses/data.htm"
DIOCESE_BASE_URL = "https://www.gcatholic.org/dioceses/diocese/"

HEADERS = {
    "User-Agent": "CartaPastorale-Bot/1.0 (pastoral@carta-pastorale.org; Research Project)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

RATE_LIMIT_SECONDS = 2.5  # Respectueux : 2.5s entre chaque requête
MAX_RETRIES = 3
TIMEOUT = 30

# ============================================================
# STRUCTURE DE DONNÉES
# ============================================================

@dataclass
class DioceseData:
    """Structure complète des données d'un diocèse."""

    # Identification
    gcatholic_id: str = ""
    nom: str = ""
    nom_latin: str = ""
    type: str = ""  # Diocese, Archdiocese, Prefecture, etc.
    rite: str = ""  # Roman, Byzantine, etc.
    pays: str = ""
    continent: str = ""

    # Géographie
    superficie_km2: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    # Population
    population_totale: Optional[int] = None
    population_catholique: Optional[int] = None
    pourcentage_catholique: Optional[float] = None
    annee_donnees: Optional[int] = None

    # Clergé
    nombre_pretres: Optional[int] = None
    nombre_pretres_diocesains: Optional[int] = None
    nombre_pretres_religieux: Optional[int] = None
    nombre_diacres: Optional[int] = None

    # Vocations
    nombre_seminaristes: Optional[int] = None
    nombre_seminaristes_diocesains: Optional[int] = None
    nombre_seminaristes_religieux: Optional[int] = None

    # Structures
    nombre_parishes: Optional[int] = None
    nombre_missions: Optional[int] = None
    nombre_chapelles: Optional[int] = None
    nombre_stationes: Optional[int] = None

    # Religieux
    nombre_religieux_hommes: Optional[int] = None
    nombre_religieuses: Optional[int] = None

    # Éducation et santé
    nombre_ecoles_catholiques_primaires: Optional[int] = None
    nombre_ecoles_catholiques_secondaires: Optional[int] = None
    nombre_universites_catholiques: Optional[int] = None
    nombre_hopitaux_catholiques: Optional[int] = None

    # Historique
    date_creation: Optional[str] = None
    date_elevation: Optional[str] = None

    # Métadonnées
    source_url: str = ""
    date_extraction: str = ""
    statut_extraction: str = "success"  # success, partial, failed
    champs_manquants: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return asdict(self)


# ============================================================
# UTILITAIRES
# ============================================================

def clean_number(text: str) -> Optional[int]:
    """Extrait un nombre entier d'une chaîne de caractères."""
    if not text:
        return None
    # Supprime tout sauf les chiffres et les points
    cleaned = re.sub(r"[^\d.]", "", text.replace(",", ""))
    if not cleaned:
        return None
    try:
        return int(float(cleaned))
    except ValueError:
        return None


def clean_float(text: str) -> Optional[float]:
    """Extrait un nombre flottant d'une chaîne de caractères."""
    if not text:
        return None
    cleaned = re.sub(r"[^\d.]", "", text.replace(",", ""))
    if not cleaned:
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


def extract_year(text: str) -> Optional[int]:
    """Extrait une année à 4 chiffres d'un texte."""
    match = re.search(r"(19|20)\d{2}", text)
    if match:
        return int(match.group())
    return None


# ============================================================
# SCRAPING
# ============================================================

class GCatholicScraper:
    """Scraper principal pour GCatholic.org."""

    def __init__(self, rate_limit: float = RATE_LIMIT_SECONDS):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.rate_limit = rate_limit
        self.last_request_time = 0
        self.stats = {
            "total": 0,
            "success": 0,
            "partial": 0,
            "failed": 0,
            "skipped": 0,
        }

    def _wait_rate_limit(self):
        """Attend le rate limit entre les requêtes."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self.last_request_time = time.time()

    def _fetch(self, url: str, retries: int = 0) -> Optional[BeautifulSoup]:
        """Récupère une page avec retry et rate limiting."""
        self._wait_rate_limit()

        try:
            response = self.session.get(url, timeout=TIMEOUT)
            response.raise_for_status()
            return BeautifulSoup(response.content, "html.parser")
        except requests.exceptions.RequestException as e:
            if retries < MAX_RETRIES:
                wait_time = (retries + 1) * 5
                print(f"  ⚠️ Erreur sur {url}, retry {retries + 1}/{MAX_RETRIES} dans {wait_time}s...")
                time.sleep(wait_time)
                return self._fetch(url, retries + 1)
            else:
                print(f"  ❌ Échec définitif sur {url}: {e}")
                return None

    def get_all_diocese_ids(self) -> List[str]:
        """Récupère la liste de tous les IDs de diocèses."""
        print(f"🔍 Récupération de la liste des diocèses depuis {DIOCESES_LIST_URL}...")

        soup = self._fetch(DIOCESES_LIST_URL)
        if not soup:
            print("❌ Impossible de récupérer la liste des diocèses.")
            return []

        diocese_ids = []

        # Cherche les liens vers les pages de diocèses
        # Format: /dioceses/diocese/XXXX.htm
        for link in soup.find_all("a", href=re.compile(r"/dioceses/diocese/[a-z0-9]+\.htm")):
            href = link.get("href", "")
            match = re.search(r"/dioceses/diocese/([a-z0-9]+)\.htm", href)
            if match:
                diocese_id = match.group(1)
                if diocese_id not in diocese_ids:
                    diocese_ids.append(diocese_id)

        print(f"✅ {len(diocese_ids)} diocèses trouvés.")
        return diocese_ids

    def parse_diocese_page(self, diocese_id: str) -> DioceseData:
        """Parse une page de diocèse et extrait toutes les données."""
        url = f"{DIOCESE_BASE_URL}{diocese_id}.htm"
        data = DioceseData(
            gcatholic_id=diocese_id,
            source_url=url,
            date_extraction=time.strftime("%Y-%m-%d %H:%M:%S"),
        )

        print(f"  📄 Extraction de {diocese_id}...")
        soup = self._fetch(url)

        if not soup:
            data.statut_extraction = "failed"
            return data

        try:
            # === NOM ET TYPE ===
            title = soup.find("h1") or soup.find("h2")
            if title:
                full_title = title.get_text(strip=True)
                # Extrait le type (Archdiocese, Diocese, etc.)
                type_match = re.search(r"(Archdiocese|Diocese|Apostolic\s+Vicariate|Apostolic\s+Prefecture|Territorial\s+Prelature|Apostolic\s+Exarchate|Eparchy|Patriarchate)", full_title, re.IGNORECASE)
                if type_match:
                    data.type = type_match.group(1).title()

                # Nom propre (tout sauf le type)
                data.nom = re.sub(r"^(Archdiocese\s+of\s+|Diocese\s+of\s+|Apostolic\s+Vicariate\s+of\s+|Apostolic\s+Prefecture\s+of\s+|Territorial\s+Prelature\s+of\s+)", "", full_title, flags=re.IGNORECASE).strip()

            # === TABLEAU PRINCIPAL DE DONNÉES ===
            # GCatholic organise les données dans des tableaux
            tables = soup.find_all("table")

            for table in tables:
                rows = table.find_all("tr")
                for row in rows:
                    cells = row.find_all(["td", "th"])
                    if len(cells) >= 2:
                        label = cells[0].get_text(strip=True).lower()
                        value = cells[1].get_text(strip=True)

                        # Population
                        if "population" in label and "total" in label:
                            data.population_totale = clean_number(value)
                        elif "population" in label and "catholic" in label:
                            data.population_catholique = clean_number(value)
                        elif "percentage" in label and "catholic" in label:
                            data.pourcentage_catholique = clean_float(value)
                        elif "year" in label and ("data" in label or "statistics" in label):
                            data.annee_donnees = extract_year(value) or clean_number(value)

                        # Superficie
                        elif "area" in label or "square" in label or "km" in label:
                            data.superficie_km2 = clean_float(value)

                        # Clergé
                        elif "priest" in label and "total" in label:
                            data.nombre_pretres = clean_number(value)
                        elif "priest" in label and "diocesan" in label:
                            data.nombre_pretres_diocesains = clean_number(value)
                        elif "priest" in label and "religious" in label:
                            data.nombre_pretres_religieux = clean_number(value)
                        elif "deacon" in label:
                            data.nombre_diacres = clean_number(value)

                        # Vocations
                        elif "seminarian" in label and "total" in label:
                            data.nombre_seminaristes = clean_number(value)
                        elif "seminarian" in label and "diocesan" in label:
                            data.nombre_seminaristes_diocesains = clean_number(value)
                        elif "seminarian" in label and "religious" in label:
                            data.nombre_seminaristes_religieux = clean_number(value)

                        # Structures
                        elif "parish" in label:
                            data.nombre_parishes = clean_number(value)
                        elif "mission" in label:
                            data.nombre_missions = clean_number(value)
                        elif "chapel" in label:
                            data.nombre_chapelles = clean_number(value)
                        elif "station" in label:
                            data.nombre_stationes = clean_number(value)

                        # Religieux
                        elif "religious" in label and "men" in label:
                            data.nombre_religieux_hommes = clean_number(value)
                        elif "religious" in label and ("women" in label or "sister" in label):
                            data.nombre_religieuses = clean_number(value)

                        # Éducation
                        elif "primary" in label and "school" in label:
                            data.nombre_ecoles_catholiques_primaires = clean_number(value)
                        elif "secondary" in label and "school" in label:
                            data.nombre_ecoles_catholiques_secondaires = clean_number(value)
                        elif "universit" in label or "college" in label:
                            data.nombre_universites_catholiques = clean_number(value)
                        elif "hospital" in label:
                            data.nombre_hopitaux_catholiques = clean_number(value)

                        # Pays et rite
                        elif "country" in label:
                            data.pays = value
                        elif "rite" in label:
                            data.rite = value
                        elif "continent" in label:
                            data.continent = value

                        # Historique
                        elif "established" in label or "created" in label:
                            data.date_creation = value
                        elif "elevated" in label:
                            data.date_elevation = value

            # === COORDONNÉES GÉOGRAPHIQUES ===
            # Cherche dans les scripts ou les métadonnées
            for script in soup.find_all("script"):
                script_text = script.string or ""
                lat_match = re.search(r'latitude["']?\s*[:=]\s*([\d.\-]+)', script_text)
                lng_match = re.search(r'longitude["']?\s*[:=]\s*([\d.\-]+)', script_text)
                if lat_match and lng_match:
                    data.latitude = float(lat_match.group(1))
                    data.longitude = float(lng_match.group(1))
                    break

            # Alternative : chercher dans les meta tags
            if not data.latitude:
                meta_geo = soup.find("meta", attrs={"name": re.compile(r"geo.position", re.I)})
                if meta_geo:
                    coords = meta_geo.get("content", "").split(";")
                    if len(coords) == 2:
                        data.latitude = clean_float(coords[0])
                        data.longitude = clean_float(coords[1])

            # === VÉRIFICATION DES CHAMPS MANQUANTS ===
            critical_fields = [
                ("population_totale", "Population totale"),
                ("population_catholique", "Population catholique"),
                ("nombre_pretres", "Nombre de prêtres"),
                ("nombre_parishes", "Nombre de paroisses"),
                ("pays", "Pays"),
            ]

            for field_name, field_label in critical_fields:
                if getattr(data, field_name) is None:
                    data.champs_manquants.append(field_label)

            if data.champs_manquants:
                data.statut_extraction = "partial"
            else:
                data.statut_extraction = "success"

        except Exception as e:
            print(f"  ⚠️ Erreur de parsing sur {diocese_id}: {e}")
            data.statut_extraction = "partial"
            data.champs_manquants.append(f"Erreur parsing: {str(e)}")

        return data

    def scrape_all(self, output_path: str, resume: bool = False, limit: Optional[int] = None):
        """Scrape tous les diocèses et sauvegarde les résultats."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Charger les données existantes si resume
        existing_data = {}
        if resume and output_file.exists():
            with open(output_file, "r", encoding="utf-8") as f:
                existing = json.load(f)
                existing_data = {d["gcatholic_id"]: d for d in existing}
            print(f"📂 Reprise : {len(existing_data)} diocèses déjà extraits.")

        # Récupérer la liste des diocèses
        diocese_ids = self.get_all_diocese_ids()

        if limit:
            diocese_ids = diocese_ids[:limit]

        self.stats["total"] = len(diocese_ids)

        # Filtrer ceux déjà extraits si resume
        if resume:
            diocese_ids = [d for d in diocese_ids if d not in existing_data]
            print(f"🔄 {len(diocese_ids)} diocèses restants à extraire.")

        results = list(existing_data.values()) if resume else []

        print(f"\n🚀 Début de l'extraction de {len(diocese_ids)} diocèses...")
        print("=" * 60)

        for i, diocese_id in enumerate(diocese_ids, 1):
            data = self.parse_diocese_page(diocese_id)
            results.append(data.to_dict())

            # Stats
            self.stats[data.statut_extraction] += 1

            # Affichage progressif
            status_icon = "✅" if data.statut_extraction == "success" else "⚠️" if data.statut_extraction == "partial" else "❌"
            print(f"  {status_icon} [{i}/{len(diocese_ids)}] {diocese_id}: {data.nom or 'N/A'} ({data.pays or 'N/A'}) — {data.statut_extraction}")

            # Sauvegarde intermédiaire toutes les 50 entrées
            if i % 50 == 0:
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)
                print(f"  💾 Sauvegarde intermédiaire ({i} diocèses)")

        # Sauvegarde finale
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        # Export CSV
        csv_path = output_file.with_suffix(".csv")
        self._export_csv(results, csv_path)

        # Résumé
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DE L'EXTRACTION")
        print(f"   Total traités : {self.stats['total']}")
        print(f"   ✅ Complets    : {self.stats['success']}")
        print(f"   ⚠️  Partiels    : {self.stats['partial']}")
        print(f"   ❌ Échecs      : {self.stats['failed']}")
        print(f"\n💾 Fichiers sauvegardés :")
        print(f"   JSON: {output_file}")
        print(f"   CSV : {csv_path}")

    def _export_csv(self, data: List[Dict], path: Path):
        """Exporte les données en CSV."""
        if not data:
            return

        fieldnames = list(data[0].keys())
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

    def scrape_single(self, diocese_id: str) -> DioceseData:
        """Scrape un seul diocèse (utile pour les tests)."""
        return self.parse_diocese_page(diocese_id)


# ============================================================
# VALIDATEUR DE DONNÉES
# ============================================================

class DataValidator:
    """Valide la qualité des données extraites."""

    @staticmethod
    def validate_dataset(data_path: str) -> Dict:
        """Analyse un fichier JSON de diocèses et identifie les problèmes."""
        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        total = len(data)

        # Compte les champs manquants par type
        missing_stats = {
            "population_totale": 0,
            "population_catholique": 0,
            "nombre_pretres": 0,
            "nombre_parishes": 0,
            "superficie_km2": 0,
            "nombre_seminaristes": 0,
            "pays": 0,
        }

        incomplete_dioceses = []

        for d in data:
            missing = []
            for field in missing_stats.keys():
                if d.get(field) is None:
                    missing_stats[field] += 1
                    missing.append(field)

            if missing:
                incomplete_dioceses.append({
                    "id": d["gcatholic_id"],
                    "nom": d.get("nom", "N/A"),
                    "pays": d.get("pays", "N/A"),
                    "champs_manquants": missing,
                })

        report = {
            "total_dioceses": total,
            "completude_globale": round((1 - len(incomplete_dioceses) / total) * 100, 2) if total > 0 else 0,
            "champs_manquants_par_type": {k: f"{v} ({round(v/total*100, 1)}%)" for k, v in missing_stats.items()},
            "dioceses_incomplets": incomplete_dioceses[:20],  # Top 20
            "dioceses_sans_aucune_donnee": [d for d in data if d.get("statut_extraction") == "failed"],
        }

        return report

    @staticmethod
    def print_report(report: Dict):
        """Affiche un rapport de validation."""
        print("\n" + "=" * 60)
        print("📋 RAPPORT DE VALIDATION DES DONNÉES")
        print("=" * 60)
        print(f"Total de diocèses : {report['total_dioceses']}")
        print(f"Complétude globale : {report['completude_globale']}%")
        print("\nChamps manquants :")
        for field, count in report["champs_manquants_par_type"].items():
            print(f"  • {field}: {count}")

        print(f"\nDiocèses incomplets (top 20) : {len(report['dioceses_incomplets'])}")
        for d in report["dioceses_incomplets"][:5]:
            print(f"  • {d['nom']} ({d['pays']}): {', '.join(d['champs_manquants'])}")

        if report["dioceses_sans_aucune_donnee"]:
            print(f"\n❌ Diocèses sans aucune donnée : {len(report['dioceses_sans_aucune_donnee'])}")


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Scraper GCatholic.org pour Carta Pastorale")
    parser.add_argument("--output", "-o", default="data/dioceses.json", help="Chemin du fichier de sortie")
    parser.add_argument("--resume", "-r", action="store_true", help="Reprendre une extraction interrompue")
    parser.add_argument("--limit", "-l", type=int, help="Limiter le nombre de diocèses (test)")
    parser.add_argument("--diocese", "-d", help="Scraper un seul diocèse par ID")
    parser.add_argument("--validate", "-v", help="Valider un fichier JSON existant")
    parser.add_argument("--rate-limit", type=float, default=RATE_LIMIT_SECONDS, help="Délai entre requêtes (secondes)")

    args = parser.parse_args()

    if args.validate:
        report = DataValidator.validate_dataset(args.validate)
        DataValidator.print_report(report)
        return

    scraper = GCatholicScraper(rate_limit=args.rate_limit)

    if args.diocese:
        data = scraper.scrape_single(args.diocese)
        print("\n" + "=" * 60)
        print("📄 DONNÉES EXTRAITES")
        print("=" * 60)
        print(json.dumps(data.to_dict(), ensure_ascii=False, indent=2))
    else:
        scraper.scrape_all(args.output, resume=args.resume, limit=args.limit)


if __name__ == "__main__":
    main()