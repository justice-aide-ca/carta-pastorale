"""
============================================================
PIPELINE CARTA PASTORALE — run_all.py
============================================================
Orchestre l'extraction, la contextualisation et la génération
des rapports en une seule commande.

Usage:
    python run_all.py --full                    # Pipeline complet
    python run_all.py --scrape-only             # Uniquement le scraping
    python run_all.py --contextualize-only      # Uniquement la contextualisation
    python run_all.py --limit 50                # Test sur 50 diocèses
    python run_all.py --diocese pari0           # Un seul diocèse
    python run_all.py --worldbank               # Inclure l'actualisation World Bank

Auteur: Carta Pastorale
"""

import argparse
import json
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime

# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
RAPPORTS_DIR = DATA_DIR / "rapports"
LOGS_DIR = BASE_DIR / "logs"

# Fichiers
DIOCESES_JSON = DATA_DIR / "dioceses.json"
DIOCESES_CSV = DATA_DIR / "dioceses.csv"
WORLDBANK_JSON = DATA_DIR / "worldbank.json"
SUMMARY_CSV = DATA_DIR / "summary.csv"

# ============================================================
# UTILITAIRES
# ============================================================

class Logger:
    """Logger simple avec fichier et console."""

    def __init__(self):
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        self.log_file = LOGS_DIR / f"pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        self.start_time = time.time()

    def log(self, message: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        line = f"[{timestamp}] [{level}] {message}"
        print(line)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(line + "
")

    def success(self, message: str):
        self.log(message, "SUCCESS")

    def error(self, message: str):
        self.log(message, "ERROR")

    def warning(self, message: str):
        self.log(message, "WARNING")

    def elapsed(self) -> str:
        elapsed = time.time() - self.start_time
        return f"{int(elapsed // 60)}m {int(elapsed % 60)}s"

    def finalize(self):
        self.success(f"Pipeline terminé en {self.elapsed()}")


def run_command(cmd: list, logger: Logger, description: str) -> bool:
    """Exécute une commande et logue le résultat."""
    logger.log(f"▶️  {description}")
    logger.log(f"   Commande: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=3600,  # 1h max
        )

        if result.returncode == 0:
            logger.success(f"✅ {description} — terminé")
            if result.stdout:
                for line in result.stdout.strip().split("
")[-5:]:  # Dernières 5 lignes
                    logger.log(f"   {line}")
            return True
        else:
            logger.error(f"❌ {description} — échec (code {result.returncode})")
            if result.stderr:
                for line in result.stderr.strip().split("
")[-5:]:
                    logger.error(f"   {line}")
            return False

    except subprocess.TimeoutExpired:
        logger.error(f"⏱️  {description} — timeout")
        return False
    except Exception as e:
        logger.error(f"💥 {description} — exception: {e}")
        return False


# ============================================================
# ÉTAPES DU PIPELINE
# ============================================================

class Pipeline:
    """Orchestre le pipeline complet."""

    def __init__(self, logger: Logger, args):
        self.logger = logger
        self.args = args
        self.results = {
            "scrape": False,
            "worldbank": False,
            "contextualize": False,
            "summary": False,
        }

    def setup_directories(self):
        """Crée les répertoires nécessaires."""
        self.logger.log("📁 Création des répertoires...")
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        RAPPORTS_DIR.mkdir(parents=True, exist_ok=True)
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        self.logger.success("Répertoires prêts")

    def step_scrape(self) -> bool:
        """Étape 1 : Scraping GCatholic."""
        self.logger.log("=" * 60)
        self.logger.log("ÉTAPE 1/4 : EXTRACTION DES DONNÉES GCATHOLIC")
        self.logger.log("=" * 60)

        cmd = [sys.executable, "gcatholic_scraper.py", "--output", str(DIOCESES_JSON)]

        if self.args.limit:
            cmd.extend(["--limit", str(self.args.limit)])

        if DIOCESES_JSON.exists() and not self.args.no_resume:
            cmd.append("--resume")
            self.logger.log("🔄 Reprise d'une extraction précédente")

        success = run_command(cmd, self.logger, "Scraping GCatholic.org")
        self.results["scrape"] = success

        if success and DIOCESES_JSON.exists():
            with open(DIOCESES_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.logger.success(f"📊 {len(data)} diocèses extraits")

        return success

    def step_worldbank(self) -> bool:
        """Étape 1b : Actualisation World Bank (optionnel)."""
        self.logger.log("=" * 60)
        self.logger.log("ÉTAPE 1b : ACTUALISATION WORLD BANK (optionnel)")
        self.logger.log("=" * 60)

        if not self.args.worldbank:
            self.logger.log("⏭️  Ignoré (utiliser --worldbank pour activer)")
            self.results["worldbank"] = True  # Considéré comme OK
            return True

        cmd = [sys.executable, "worldbank_fetcher.py", "--output", str(WORLDBANK_JSON)]

        # Limiter aux pays présents dans les diocèses extraits
        if DIOCESES_JSON.exists():
            with open(DIOCESES_JSON, "r", encoding="utf-8") as f:
                dioceses = json.load(f)

            # Extraire les pays uniques
            pays = list(set(d.get("pays", "") for d in dioceses if d.get("pays")))

            # Mapping vers ISO3
            from mapping_pays import GCATHOLIC_TO_STANDARD, DONNEES_PAYS
            iso3_list = []
            for p in pays:
                std = GCATHOLIC_TO_STANDARD.get(p, p)
                for iso3, gc_name in ISO3_TO_GCATHOLIC.items():
                    if gc_name == p or gc_name == std:
                        iso3_list.append(iso3)
                        break

            if iso3_list:
                cmd.extend(["--countries"] + iso3_list[:20])  # Max 20 pour le rate limit
                self.logger.log(f"🎯 Ciblage de {len(iso3_list)} pays présents dans les diocèses")

        success = run_command(cmd, self.logger, "Fetch World Bank API")
        self.results["worldbank"] = success
        return success

    def step_contextualize(self) -> bool:
        """Étape 2 : Contextualisation."""
        self.logger.log("=" * 60)
        self.logger.log("ÉTAPE 2/4 : CONTEXTUALISATION DES RAPPORTS")
        self.logger.log("=" * 60)

        if not DIOCESES_JSON.exists():
            self.logger.error("❌ Fichier dioceses.json introuvable. Lancer le scraping d'abord.")
            return False

        cmd = [
            sys.executable, "contextualizer.py",
            "--input", str(DIOCESES_JSON),
            "--output", str(RAPPORTS_DIR),
            "--csv", str(SUMMARY_CSV),
        ]

        if self.args.diocese:
            cmd.extend(["--diocese", self.args.diocese])

        success = run_command(cmd, self.logger, "Génération des rapports contextualisés")
        self.results["contextualize"] = success

        if success:
            # Compter les rapports générés
            rapport_files = list(RAPPORTS_DIR.glob("*.json"))
            self.logger.success(f"📄 {len(rapport_files)} rapports générés dans {RAPPORTS_DIR}")

            if SUMMARY_CSV.exists():
                self.logger.success(f"📋 Résumé CSV exporté : {SUMMARY_CSV}")

        return success

    def step_validate(self) -> bool:
        """Étape 3 : Validation."""
        self.logger.log("=" * 60)
        self.logger.log("ÉTAPE 3/4 : VALIDATION DES DONNÉES")
        self.logger.log("=" * 60)

        if not DIOCESES_JSON.exists():
            self.logger.warning("Fichier dioceses.json introuvable, validation impossible")
            return False

        cmd = [sys.executable, "gcatholic_scraper.py", "--validate", str(DIOCESES_JSON)]
        success = run_command(cmd, self.logger, "Validation des données")
        return success

    def step_report(self):
        """Étape 4 : Rapport final."""
        self.logger.log("=" * 60)
        self.logger.log("ÉTAPE 4/4 : RAPPORT FINAL")
        self.logger.log("=" * 60)

        report = {
            "timestamp": datetime.now().isoformat(),
            "elapsed": self.logger.elapsed(),
            "results": self.results,
            "files": {
                "dioceses_json": str(DIOCESES_JSON) if DIOCESES_JSON.exists() else None,
                "dioceses_csv": str(DIOCESES_CSV) if DIOCESES_CSV.exists() else None,
                "worldbank_json": str(WORLDBANK_JSON) if WORLDBANK_JSON.exists() else None,
                "summary_csv": str(SUMMARY_CSV) if SUMMARY_CSV.exists() else None,
                "rapports_dir": str(RAPPORTS_DIR) if RAPPORTS_DIR.exists() else None,
            },
        }

        report_file = DATA_DIR / "pipeline_report.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        self.logger.success(f"📋 Rapport sauvegardé : {report_file}")

        # Affichage résumé
        self.logger.log("")
        self.logger.log("╔" + "═" * 58 + "╗")
        self.logger.log("║" + " RÉSUMÉ DU PIPELINE".center(58) + "║")
        self.logger.log("╠" + "═" * 58 + "╣")
        self.logger.log("║" + f" Scraping GCatholic  : {'✅ OK' if self.results['scrape'] else '❌ ÉCHEC'}".ljust(58) + "║")
        self.logger.log("║" + f" World Bank          : {'✅ OK' if self.results['worldbank'] else '❌ ÉCHEC'}".ljust(58) + "║")
        self.logger.log("║" + f" Contextualisation   : {'✅ OK' if self.results['contextualize'] else '❌ ÉCHEC'}".ljust(58) + "║")
        self.logger.log("╠" + "═" * 58 + "╣")
        self.logger.log("║" + f" Temps total         : {self.logger.elapsed()}".ljust(58) + "║")
        self.logger.log("║" + f" Log                 : {self.logger.log_file.name}".ljust(58) + "║")
        self.logger.log("╚" + "═" * 58 + "╝")

    def run(self):
        """Exécute le pipeline complet."""
        self.logger.log("🚀 DÉMARRAGE DU PIPELINE CARTA PASTORALE")
        self.logger.log(f"   Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.log(f"   Mode : {'FULL' if self.args.full else 'PARTIEL'}")

        self.setup_directories()

        if self.args.scrape_only:
            self.step_scrape()
        elif self.args.contextualize_only:
            self.step_contextualize()
        elif self.args.diocese:
            # Mode single diocese
            self.step_scrape()
            self.step_contextualize()
        else:
            # Pipeline complet
            if self.step_scrape():
                self.step_worldbank()
                self.step_contextualize()
                self.step_validate()

        self.step_report()
        self.logger.finalize()


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Pipeline complet Carta Pastorale")
    parser.add_argument("--full", action="store_true", help="Pipeline complet (défaut)")
    parser.add_argument("--scrape-only", action="store_true", help="Uniquement le scraping")
    parser.add_argument("--contextualize-only", action="store_true", help="Uniquement la contextualisation")
    parser.add_argument("--worldbank", action="store_true", help="Inclure l'actualisation World Bank")
    parser.add_argument("--limit", type=int, help="Limiter le nombre de diocèses (test)")
    parser.add_argument("--diocese", help="Traiter un seul diocèse")
    parser.add_argument("--no-resume", action="store_true", help="Ne pas reprendre une extraction interrompue")

    args = parser.parse_args()

    logger = Logger()
    pipeline = Pipeline(logger, args)
    pipeline.run()


if __name__ == "__main__":
    main()