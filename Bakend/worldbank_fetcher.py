"""
============================================================
WORLD BANK API INTEGRATION — Carta Pastorale
============================================================
Récupère automatiquement les indicateurs socio-économiques
via l'API World Bank Open Data.

Usage:
    python worldbank_fetcher.py --output data/worldbank.json
    python worldbank_fetcher.py --country FRA --output data/france.json
    python worldbank_fetcher.py --update-mapping mapping_pays.py

Auteur: Carta Pastorale
"""

import requests
import json
import time
import argparse
from pathlib import Path
from typing import Dict, List, Optional

# ============================================================
# CONFIGURATION
# ============================================================

WORLD_BANK_API = "https://api.worldbank.org/v2/country"

# Indicateurs clés pour la contextualisation pastorale
INDICATORS = {
    # Développement humain
    "NY.GDP.PCAP.CD": "pib_par_habitant_usd",           # PIB par habitant ($)
    "NY.GDP.MKTP.CD": "pib_total_usd",                   # PIB total ($)
    "SP.POP.TOTL": "population_totale",                  # Population totale
    "SP.URB.TOTL.IN.ZS": "taux_urbanisation",            # % urbain
    "SI.POV.DDAY": "taux_pauvrete_extreme",              # Pauvreté <$2.15/jour
    "SI.POV.NAHC": "taux_pauvrete_nationale",            # Pauvreté seuil national

    # Éducation et santé
    "SE.PRM.ENRR": "taux_scolarisation_primaire",        # Scolarisation primaire
    "SE.SEC.ENRR": "taux_scolarisation_secondaire",      # Scolarisation secondaire
    "SE.TER.ENRR": "taux_scolarisation_superieure",      # Scolarisation supérieure
    "SP.DYN.LE00.IN": "esperance_vie",                   # Espérance de vie
    "SH.DYN.MORT": "mortalite_infantile",                # Mortalité infantile (/1000)

    # Inégalités
    "SI.POV.GINI": "coefficient_gini",                   # Coefficient de Gini

    # Emploi
    "SL.UEM.TOTL.ZS": "taux_chomage",                    # Taux de chômage

    # Migration
    "SM.POP.NETM": "solde_migratoire",                   # Solde migratoire net
}

# Mapping ISO3 -> nom GCatholic (sous-ensemble, à compléter)
ISO3_TO_GCATHOLIC = {
    "FRA": "France", "ITA": "Italy", "USA": "United States",
    "BRA": "Brazil", "NGA": "Nigeria", "COD": "Congo, Democratic Republic of the",
    "IND": "India", "PHL": "Philippines", "CHN": "China",
    "MEX": "Mexico", "DEU": "Germany", "POL": "Poland",
    "ARG": "Argentina", "COL": "Colombia", "VEN": "Venezuela",
    "EGY": "Egypt", "ETH": "Ethiopia", "KEN": "Kenya",
    "UGA": "Uganda", "TZA": "Tanzania", "PAK": "Pakistan",
    "IDN": "Indonesia", "VNM": "Vietnam", "AUS": "Australia",
    "CAN": "Canada", "ESP": "Spain", "PRT": "Portugal",
    "ROU": "Romania", "UKR": "Ukraine", "RUS": "Russia",
    "TUR": "Turkey", "IRQ": "Iraq", "SYR": "Syria",
    "LBN": "Lebanon", "SSD": "South Sudan", "SDN": "Sudan",
    "SOM": "Somalia", "AFG": "Afghanistan", "KOR": "Korea, South",
    "JPN": "Japan", "THA": "Thailand", "CUB": "Cuba",
    "HTI": "Haiti", "GTM": "Guatemala", "PER": "Peru",
    "CHL": "Chile", "ECU": "Ecuador", "BOL": "Bolivia",
    "PRY": "Paraguay", "URY": "Uruguay", "CMR": "Cameroon",
    "CIV": "Ivory Coast", "GHA": "Ghana", "MDG": "Madagascar",
    "MLI": "Mali", "BFA": "Burkina Faso", "NER": "Niger",
    "TCD": "Chad", "CAF": "Central African Republic", "LKA": "Sri Lanka",
    "MMR": "Myanmar", "BGD": "Bangladesh", "NPL": "Nepal",
    "MNG": "Mongolia", "KAZ": "Kazakhstan", "UZB": "Uzbekistan",
    "TKM": "Turkmenistan", "TJK": "Tajikistan", "KGZ": "Kyrgyzstan",
    "GEO": "Georgia", "ARM": "Armenia", "AZE": "Azerbaijan",
    "BLR": "Belarus", "MDA": "Moldova", "LTU": "Lithuania",
    "LVA": "Latvia", "EST": "Estonia", "HUN": "Hungary",
    "CZE": "Czech Republic", "SVK": "Slovakia", "SVN": "Slovenia",
    "HRV": "Croatia", "BIH": "Bosnia and Herzegovina", "SRB": "Serbia",
    "MNE": "Montenegro", "MKD": "North Macedonia", "ALB": "Albania",
    "XKX": "Kosovo", "GRC": "Greece", "CYP": "Cyprus",
    "MLT": "Malta", "ISL": "Iceland", "IRL": "Ireland",
    "GBR": "United Kingdom", "NLD": "Netherlands", "BEL": "Belgium",
    "LUX": "Luxembourg", "CHE": "Switzerland", "AUT": "Austria",
    "DNK": "Denmark", "SWE": "Sweden", "NOR": "Norway",
    "FIN": "Finland",
}

GCATHOLIC_TO_ISO3 = {v: k for k, v in ISO3_TO_GCATHOLIC.items()}

# ============================================================
# FETCHER
# ============================================================

class WorldBankFetcher:
    """Récupère les données de la Banque Mondiale."""

    def __init__(self, rate_limit: float = 0.5):
        self.rate_limit = rate_limit
        self.last_request = 0

    def _wait(self):
        elapsed = time.time() - self.last_request
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self.last_request = time.time()

    def fetch_indicator(self, iso3: str, indicator: str, year: Optional[int] = None) -> Optional[float]:
        """Récupère un indicateur pour un pays."""
        self._wait()

        url = f"{WORLD_BANK_API}/{iso3}/indicator/{indicator}"
        params = {"format": "json", "per_page": 10, "date": "2020:2024"}

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if len(data) < 2 or not data[1]:
                return None

            # Prend la valeur la plus récente non nulle
            for entry in data[1]:
                value = entry.get("value")
                if value is not None:
                    return float(value)
            return None

        except Exception as e:
            print(f"  ⚠️ Erreur {indicator} pour {iso3}: {e}")
            return None

    def fetch_country(self, iso3: str) -> Dict:
        """Récupère tous les indicateurs pour un pays."""
        print(f"📊 Récupération des données pour {iso3}...")

        result = {"iso3": iso3, "gcatholic_name": ISO3_TO_GCATHOLIC.get(iso3, iso3)}

        for wb_code, field_name in INDICATORS.items():
            value = self.fetch_indicator(iso3, wb_code)
            result[field_name] = value
            if value is not None:
                print(f"  ✅ {field_name}: {value}")
            else:
                print(f"  ⚠️ {field_name}: non disponible")

        return result

    def fetch_all(self, output_path: str, countries: Optional[List[str]] = None):
        """Récupère les données pour tous les pays ou une liste donnée."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        target_countries = countries or list(ISO3_TO_GCATHOLIC.keys())

        print(f"🌍 Récupération des données World Bank pour {len(target_countries)} pays...")
        print("=" * 60)

        results = {}
        for i, iso3 in enumerate(target_countries, 1):
            gcatholic_name = ISO3_TO_GCATHOLIC.get(iso3, iso3)
            data = self.fetch_country(iso3)
            results[gcatholic_name] = data

            # Sauvegarde intermédiaire
            if i % 10 == 0:
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)
                print(f"💾 Sauvegarde intermédiaire ({i}/{len(target_countries)})")

        # Sauvegarde finale
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"\n✅ Données sauvegardées dans {output_file}")
        print(f"   Pays traités: {len(results)}")

        # Rapport de complétude
        self._print_completeness_report(results)

        return results

    def _print_completeness_report(self, results: Dict):
        """Affiche un rapport de complétude des données."""
        print("\n📋 RAPPORT DE COMPLETUDE")
        print("=" * 60)

        total = len(results)
        for field in INDICATORS.values():
            available = sum(1 for d in results.values() if d.get(field) is not None)
            pct = (available / total) * 100 if total > 0 else 0
            print(f"  {field}: {available}/{total} ({pct:.1f}%)")

    def update_mapping_file(self, mapping_file: str, worldbank_file: str, output_file: str):
        """Met à jour le fichier mapping_pays.py avec les données fraîches de World Bank."""
        print(f"🔄 Mise à jour de {mapping_file} avec les données World Bank...")

        with open(worldbank_file, "r", encoding="utf-8") as f:
            wb_data = json.load(f)

        # Génère un nouveau fichier Python avec les données actualisées
        new_data = []
        for gcatholic_name, data in wb_data.items():
            pib = data.get("pib_par_habitant_usd")
            pauvrete = data.get("taux_pauvrete_extreme") or data.get("taux_pauvrete_nationale")
            urban = data.get("taux_urbanisation")
            pop = data.get("population_totale")

            if pib is not None or pauvrete is not None or urban is not None:
                new_data.append({
                    "name": gcatholic_name,
                    "pib_par_habitant_usd": round(pib, 0) if pib else None,
                    "taux_pauvrete": round(pauvrete, 1) if pauvrete else None,
                    "taux_urbanisation": round(urban, 1) if urban else None,
                    "population_totale": int(pop) if pop else None,
                })

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(new_data, f, ensure_ascii=False, indent=2)

        print(f"✅ Données actualisées sauvegardées dans {output_file}")
        print(f"   Pays avec données fraîches: {len(new_data)}")


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Fetch World Bank data for Carta Pastorale")
    parser.add_argument("--output", "-o", default="data/worldbank.json", help="Fichier de sortie")
    parser.add_argument("--country", "-c", help="ISO3 d\'un seul pays (ex: FRA)")
    parser.add_argument("--countries", nargs="+", help="Liste d\'ISO3")
    parser.add_argument("--update-mapping", dest="update_mapping", help="Met à jour le mapping avec les données fraîches")
    parser.add_argument("--mapping-file", default="mapping_pays.py", help="Fichier mapping à mettre à jour")
    parser.add_argument("--rate-limit", type=float, default=0.5, help="Délai entre requêtes (secondes)")

    args = parser.parse_args()

    fetcher = WorldBankFetcher(rate_limit=args.rate_limit)

    if args.country:
        result = fetcher.fetch_country(args.country)
        print("\n" + "=" * 60)
        print("📄 RÉSULTAT")
        print("=" * 60)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.countries:
        fetcher.fetch_all(args.output, countries=args.countries)
    elif args.update_mapping:
        fetcher.update_mapping_file(args.mapping_file, args.update_mapping, args.output)
    else:
        fetcher.fetch_all(args.output)


if __name__ == "__main__":
    main()