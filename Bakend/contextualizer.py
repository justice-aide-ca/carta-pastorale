"""
============================================================
MOTEUR DE CONTEXTUALISATION — Carta Pastorale
============================================================
Enrichit les données brutes des diocèses avec des données
socio-économiques (World Bank) et génère un rapport de
discernement contextualisé.

Usage:
    python contextualizer.py --input data/dioceses.json --output data/rapports/
    python contextualizer.py --diocese pari0 --input data/dioceses.json

Auteur: Carta Pastorale
"""

import json
import csv
import math
import os
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Tuple
from datetime import datetime

# ============================================================
# DONNÉES DE RÉFÉRENCE MONDIALES (Annuarium Statisticum 2024)
# ============================================================

REFERENCE_MONDIALE = {
    "population_catholique_mondiale": 1360000000,
    "population_totale_mondiale": 8000000000,
    "pourcentage_catholique_mondial": 17.0,
    "nombre_pretres_mondial": 406000,
    "nombre_parishes_mondial": 222000,
    "nombre_seminaristes_mondial": 110000,
    "nombre_dioceses_mondial": 3200,
    "catholiques_par_pretre_mondial": 3350,
    "catholiques_par_parish_mondial": 6130,
}

# Données de référence par continent (approximatives, à affiner)
REFERENCE_PAR_CONTINENT = {
    "Europe": {
        "catholiques_par_pretre": 1800,
        "pourcentage_catholique": 40.0,
        "taux_seminaristes": 0.08,  # seminaristes / prêtres
    },
    "Afrique": {
        "catholiques_par_pretre": 5200,
        "pourcentage_catholique": 19.0,
        "taux_seminaristes": 0.25,
    },
    "Amériques": {
        "catholiques_par_pretre": 2800,
        "pourcentage_catholique": 62.0,
        "taux_seminaristes": 0.12,
    },
    "Asie": {
        "catholiques_par_pretre": 4200,
        "pourcentage_catholique": 3.5,
        "taux_seminaristes": 0.18,
    },
    "Océanie": {
        "catholiques_par_pretre": 2200,
        "pourcentage_catholique": 26.0,
        "taux_seminaristes": 0.10,
    },
}

# Données socio-économiques par pays (exemples, à enrichir via API World Bank)
# Structure: {pays: {idh, pib_par_habitant, taux_pauvrete, taux_urbanisation, indice_liberte_religion}}
DONNEES_PAYS = {
    "France": {
        "idh": 0.903,
        "pib_par_habitant_usd": 43500,
        "taux_pauvrete": 8.1,
        "taux_urbanisation": 81.0,
        "indice_liberte_religion": "libre",
        "score_persecution": 0,
        "contexte_liberte": "Liberté religieuse totale. Laïcité constitutionnelle. Relations État-Église régies par les concordats.",
        "defis_specifiques": ["Sécularisation avancée", "Désaffection des jeunes", "Entretien du patrimoine"],
    },
    "Italie": {
        "idh": 0.895,
        "pib_par_habitant_usd": 36000,
        "taux_pauvrete": 11.0,
        "taux_urbanisation": 71.0,
        "indice_liberte_religion": "libre",
        "score_persecution": 0,
        "contexte_liberte": "Liberté religieuse. Relations privilégiées avec le Vatican (Latran).",
        "defis_specifiques": ["Sécularisation urbaine", "Immigration et intégration", "Déclin des vocations"],
    },
    "États-Unis": {
        "idh": 0.920,
        "pib_par_habitant_usd": 76300,
        "taux_pauvrete": 11.5,
        "taux_urbanisation": 83.0,
        "indice_liberte_religion": "libre",
        "score_persecution": 0,
        "contexte_liberte": "Liberté religieuse constitutionnelle. Séparation Église-État.",
        "defis_specifiques": ["Polarisation politique", "Déclin des affiliations", "Scandales et confiance"],
    },
    "Brésil": {
        "idh": 0.760,
        "pib_par_habitant_usd": 8900,
        "taux_pauvrete": 24.3,
        "taux_urbanisation": 87.0,
        "indice_liberte_religion": "libre",
        "score_persecution": 0,
        "contexte_liberte": "Liberté religieuse. Plus grand pays catholique du monde.",
        "defis_specifiques": ["Pentecôtisme concurrent", "Inégalités sociales", "Déforestation Amazonie"],
    },
    "Nigeria": {
        "idh": 0.535,
        "pib_par_habitant_usd": 2200,
        "taux_pauvrete": 40.1,
        "taux_urbanisation": 53.0,
        "indice_liberte_religion": "tensions",
        "score_persecution": 78,  # Indice ACN/Portes Ouvertes (0-100)
        "contexte_liberte": "Tensions interreligieuses significatives. Violence jihadiste au nord. Discriminations légales dans certains États.",
        "defis_specifiques": ["Persécution active", "Déplacements internes", "Pauvreté extrême", "Accès à l'éducation"],
    },
    "RDC": {
        "idh": 0.481,
        "pib_par_habitant_usd": 600,
        "taux_pauvrete": 62.0,
        "taux_urbanisation": 46.0,
        "indice_liberte_religion": "libre",
        "score_persecution": 15,
        "contexte_liberte": "Liberté religieuse formelle, mais instabilité sécuritaire. L'Église est un pilier social majeur.",
        "defis_specifiques": ["Conflits armés", "Déplacés massifs", "Pauvreté structurelle", "Infrastructure détruite"],
    },
    "Inde": {
        "idh": 0.644,
        "pib_par_habitant_usd": 2400,
        "taux_pauvrete": 21.9,
        "taux_urbanisation": 35.0,
        "indice_liberte_religion": "tensions",
        "score_persecution": 65,
        "contexte_liberte": "Liberté religieuse constitutionnelle mais tensions croissantes. Lois anti-conversion dans plusieurs États. Violence communautaire.",
        "defis_specifiques": ["Nationalisme hindou", "Lois anti-conversion", "Discriminations sociales", "Pauvreté rurale"],
    },
    "Philippines": {
        "idh": 0.710,
        "pib_par_habitant_usd": 3500,
        "taux_pauvrete": 18.1,
        "taux_urbanisation": 47.0,
        "indice_liberte_religion": "libre",
        "score_persecution": 5,
        "contexte_liberte": "Liberté religieuse. 3ème pays catholique du monde. Relations historiques avec l'Église.",
        "defis_specifiques": ["Droits de l'homme", "Inégalités", "Déclin des vocations", "Diaspora"],
    },
    "Chine": {
        "idh": 0.768,
        "pib_par_habitant_usd": 12500,
        "taux_pauvrete": 0.0,
        "taux_urbanisation": 64.0,
        "indice_liberte_religion": "restreinte",
        "score_persecution": 82,
        "contexte_liberte": "Religion contrôlée par l'État. Accord provisoire Vatican-Chine sur les nominations épiscopales. Surveillance intense.",
        "defis_specifiques": ["Contrôle étatique", "Église clandestine", "Surveillance digitale", "Démographie vieillissante"],
    },
}

# ============================================================
# STRUCTURES DE DONNÉES
# ============================================================

@dataclass
class IndicateurContextualise:
    """Un indicateur avec sa valeur, sa référence, et son interprétation."""
    nom: str
    valeur: Optional[float]
    unite: str
    reference_mondiale: Optional[float]
    reference_continentale: Optional[float]
    reference_nationale: Optional[float]
    percentile: Optional[float] = None  # 0-100, position du diocèse
    tendance: Optional[str] = None  # "hausse", "baisse", "stable"
    interpretation: str = ""


@dataclass
class RapportDiocese:
    """Rapport complet et contextualisé d'un diocèse."""

    # 1. Snapshot
    diocese_id: str
    nom: str
    type: str
    pays: str
    continent: str
    date_rapport: str

    # Données brutes
    population_totale: Optional[int]
    population_catholique: Optional[int]
    pourcentage_catholique: Optional[float]
    superficie_km2: Optional[float]
    nombre_pretres: Optional[int]
    nombre_parishes: Optional[int]
    nombre_seminaristes: Optional[int]
    nombre_diacres: Optional[int]
    nombre_religieux_hommes: Optional[int]
    nombre_religieuses: Optional[int]
    annee_donnees: Optional[int]

    # 2. Indicateurs contextualisés
    indicateurs: List[IndicateurContextualise]

    # 3. Contexte socio-économique
    idh: Optional[float]
    pib_par_habitant: Optional[float]
    taux_pauvrete: Optional[float]
    taux_urbanisation: Optional[float]
    contexte_socioeco: str

    # 4. Contexte liberté religieuse
    indice_liberte_religion: str
    score_persecution: Optional[int]
    contexte_liberte: str
    defis_liberte: List[str]

    # 5. Tendances historiques (si disponibles)
    tendances: List[Dict]

    # 6. Pistes de discernement
    pistes_discernement: List[str]
    questions_pastorales: List[str]

    # Métadonnées
    qualite_donnees: str  # "complete", "partielle", "minimale"
    champs_manquants: List[str]
    sources: List[str]


# ============================================================
# MOTEUR DE CONTEXTUALISATION
# ============================================================

class Contextualizer:
    """Moteur principal de contextualisation."""

    def __init__(self, dioceses_data: List[Dict]):
        self.dioceses = dioceses_data
        self._build_statistics()

    def _build_statistics(self):
        """Calcule les statistiques de référence sur l'ensemble des diocèses."""
        # Calcul des percentiles pour chaque indicateur clé
        self.stats = {
            "catholiques_par_pretre": [],
            "catholiques_par_parish": [],
            "pourcentage_catholique": [],
            "superficie_par_parish": [],
            "taux_seminaristes": [],
        }

        for d in self.dioceses:
            if d.get("population_catholique") and d.get("nombre_pretres") and d["nombre_pretres"] > 0:
                ratio = d["population_catholique"] / d["nombre_pretres"]
                self.stats["catholiques_par_pretre"].append(ratio)

            if d.get("population_catholique") and d.get("nombre_parishes") and d["nombre_parishes"] > 0:
                ratio = d["population_catholique"] / d["nombre_parishes"]
                self.stats["catholiques_par_parish"].append(ratio)

            if d.get("pourcentage_catholique"):
                self.stats["pourcentage_catholique"].append(d["pourcentage_catholique"])

            if d.get("superficie_km2") and d.get("nombre_parishes") and d["nombre_parishes"] > 0:
                ratio = d["superficie_km2"] / d["nombre_parishes"]
                self.stats["superficie_par_parish"].append(ratio)

            if d.get("nombre_seminaristes") and d.get("nombre_pretres") and d["nombre_pretres"] > 0:
                ratio = d["nombre_seminaristes"] / d["nombre_pretres"]
                self.stats["taux_seminaristes"].append(ratio)

        # Trie pour calcul des percentiles
        for key in self.stats:
            self.stats[key].sort()

    def _percentile(self, value: float, distribution: List[float]) -> float:
        """Calcule le percentile d'une valeur dans une distribution."""
        if not distribution:
            return 50.0
        count = sum(1 for v in distribution if v <= value)
        return (count / len(distribution)) * 100

    def _get_pays_data(self, pays: str) -> Dict:
        """Récupère les données socio-économiques d'un pays."""
        # Mapping des noms de pays (à enrichir)
        pays_mapping = {
            "France": "France",
            "Italy": "Italie",
            "United States": "États-Unis",
            "Brazil": "Brésil",
            "Nigeria": "Nigeria",
            "Democratic Republic of the Congo": "RDC",
            "India": "Inde",
            "Philippines": "Philippines",
            "China": "Chine",
        }

        key = pays_mapping.get(pays, pays)
        return DONNEES_PAYS.get(key, {
            "idh": None,
            "pib_par_habitant_usd": None,
            "taux_pauvrete": None,
            "taux_urbanisation": None,
            "indice_liberte_religion": "inconnu",
            "score_persecution": None,
            "contexte_liberte": "Données non disponibles.",
            "defis_specifiques": [],
        })

    def _get_reference_continent(self, continent: str) -> Dict:
        """Récupère les références pour un continent."""
        return REFERENCE_PAR_CONTINENT.get(continent, {
            "catholiques_par_pretre": 3500,
            "pourcentage_catholique": 17.0,
            "taux_seminaristes": 0.15,
        })

    def _calculer_indicateurs(self, d: Dict) -> List[IndicateurContextualise]:
        """Calcule tous les indicateurs contextualisés."""
        indicateurs = []
        continent = d.get("continent", "")
        ref_cont = self._get_reference_continent(continent)

        # 1. Catholiques par prêtre
        if d.get("population_catholique") and d.get("nombre_pretres") and d["nombre_pretres"] > 0:
            valeur = d["population_catholique"] / d["nombre_pretres"]
            pct = self._percentile(valeur, self.stats["catholiques_par_pretre"])

            if valeur > 8000:
                interp = "Déficit pastoral critique. La présence des laïcs et les communautés ecclésiales de base sont essentielles."
            elif valeur > 5000:
                interp = "Déficit pastoral significatif. Nécessité de renforcer la formation des laïcs et la catéchèse communautaire."
            elif valeur > 3000:
                interp = "Ratio conforme à la moyenne mondiale. Maintenir l'équilibre entre prêtres et laïcs."
            else:
                interp = "Ratio favorable. Richesse pastorale à partager, potentiel missionnaire."

            indicateurs.append(IndicateurContextualise(
                nom="Catholiques par prêtre",
                valeur=round(valeur, 1),
                unite="cath./prêtre",
                reference_mondiale=REFERENCE_MONDIALE["catholiques_par_pretre_mondial"],
                reference_continentale=ref_cont["catholiques_par_pretre"],
                reference_nationale=None,
                percentile=round(pct, 1),
                interpretation=interp,
            ))

        # 2. Catholiques par paroisse
        if d.get("population_catholique") and d.get("nombre_parishes") and d["nombre_parishes"] > 0:
            valeur = d["population_catholique"] / d["nombre_parishes"]
            pct = self._percentile(valeur, self.stats["catholiques_par_parish"])

            indicateurs.append(IndicateurContextualise(
                nom="Catholiques par paroisse",
                valeur=round(valeur, 0),
                unite="cath./paroisse",
                reference_mondiale=REFERENCE_MONDIALE["catholiques_par_parish_mondial"],
                reference_continentale=None,
                reference_nationale=None,
                percentile=round(pct, 1),
                interpretation="" if valeur < 10000 else "Paroisses surchargées. Réflexion sur la création de nouvelles unités pastorales.",
            ))

        # 3. Pourcentage catholique
        if d.get("pourcentage_catholique"):
            valeur = d["pourcentage_catholique"]
            pct = self._percentile(valeur, self.stats["pourcentage_catholique"])

            if valeur > 70:
                interp = "Catholicisme majoritaire. Enjeu : évangélisation des marginaux et nouvelles formes de sécularisation."
            elif valeur > 30:
                interp = "Catholicisme significatif. Enjeu : dialogue interreligieux et témoignage dans la société."
            elif valeur > 5:
                interp = "Catholicisme minoritaire. Enjeu : présence qualitative et dialogue avec la majorité."
            else:
                interp = "Catholicisme très minoritaire. Enjeu : survie communautaire et témoignage discret."

            indicateurs.append(IndicateurContextualise(
                nom="Pourcentage de catholiques",
                valeur=valeur,
                unite="%",
                reference_mondiale=REFERENCE_MONDIALE["pourcentage_catholique_mondial"],
                reference_continentale=ref_cont["pourcentage_catholique"],
                reference_nationale=None,
                percentile=round(pct, 1),
                interpretation=interp,
            ))

        # 4. Taux de vocations (séminaristes / prêtres)
        if d.get("nombre_seminaristes") and d.get("nombre_pretres") and d["nombre_pretres"] > 0:
            valeur = (d["nombre_seminaristes"] / d["nombre_pretres"]) * 100
            pct = self._percentile(valeur / 100, self.stats["taux_seminaristes"])

            if valeur > 20:
                interp = "Dynamique vocationnelle exceptionnelle. Capitaliser pour l'avenir et partager le modèle."
            elif valeur > 10:
                interp = "Dynamique vocationnelle saine. Maintenir l'accompagnement et la qualité de formation."
            elif valeur > 5:
                interp = "Dynamique vocationnelle fragile. Intensifier la pastorale des vocations."
            else:
                interp = "Dynamique vocationnelle critique. Urgence pastorale des vocations et redéfinition du ministère."

            indicateurs.append(IndicateurContextualise(
                nom="Taux de vocations",
                valeur=round(valeur, 2),
                unite="%",
                reference_mondiale=15.0,
                reference_continentale=ref_cont["taux_seminaristes"] * 100,
                reference_nationale=None,
                percentile=round(pct, 1),
                interpretation=interp,
            ))

        # 5. Densité pastorale (paroisses / km²)
        if d.get("superficie_km2") and d.get("nombre_parishes") and d["superficie_km2"] > 0:
            valeur = d["nombre_parishes"] / d["superficie_km2"]
            pct = self._percentile(valeur, self.stats["superficie_par_parish"])

            if valeur < 0.01:
                interp = "Territoire vaste et peu densifié pastoralement. Enjeu : itinérance et chapelles de brousse."
            elif valeur < 0.1:
                interp = "Territoire étendu. Enjeu : moyens de transport et prêtres itinérants."
            else:
                interp = "Densité pastorale satisfaisante."

            indicateurs.append(IndicateurContextualise(
                nom="Densité pastorale",
                valeur=round(valeur * 1000, 3),
                unite="paroisses/1000km²",
                reference_mondiale=None,
                reference_continentale=None,
                reference_nationale=None,
                percentile=round(pct, 1),
                interpretation=interp,
            ))

        return indicateurs

    def _generer_pistes(self, d: Dict, indicateurs: List[IndicateurContextualise], 
                        pays_data: Dict) -> Tuple[List[str], List[str]]:
        """Génère les pistes de discernement et questions pastorales."""
        pistes = []
        questions = []

        # Piste 1 : Clergé
        cath_par_pretre = next((i for i in indicateurs if i.nom == "Catholiques par prêtre"), None)
        if cath_par_pretre and cath_par_pretre.valeur and cath_par_pretre.valeur > 5000:
            pistes.append(
                "**Renforcer la présence des laïcs** : Avec un ratio de "
                f"{cath_par_pretre.valeur:.0f} catholiques par prêtre, la structuration des "
                "communautés ecclésiales de base et la formation des catéchistes deviennent "
                "prioritaires. Comment déléguer davantage de responsabilités pastorales aux laïcs ?"
            )
            questions.append(
                "Comment structurer des 'mini-paroisses' animées par des laïcs formés "
                "dans les zones où un prêtre ne peut passer qu'une fois par mois ?"
            )

        # Piste 2 : Vocations
        taux_voc = next((i for i in indicateurs if i.nom == "Taux de vocations"), None)
        if taux_voc and taux_voc.valeur and taux_voc.valeur < 5:
            pistes.append(
                "**Pastorale des vocations** : Le taux de vocations est faible ("
                f"{taux_voc.valeur:.1f}%). Il est urgent de créer un environnement favorable "
                "aux vocations : groupes de prière, témoins de vie consacrée, accompagnement "
                "personnel des jeunes."
            )
            questions.append(
                "Quels témoins de vie consacrée peuvent accompagner les jeunes dans la "
                "découverte de leur vocation ?"
            )
        elif taux_voc and taux_voc.valeur and taux_voc.valeur > 20:
            pistes.append(
                "**Capitaliser sur la dynamique vocationnelle** : Avec "
                f"{taux_voc.valeur:.1f}% de séminaristes, ce diocèse est un modèle. "
                "Comment partager cette expérience avec d'autres diocèses ? Comment assurer "
                "la qualité de la formation malgré les effectifs ?"
            )

        # Piste 3 : Contexte socio-économique
        if pays_data.get("taux_pauvrete") and pays_data["taux_pauvrete"] > 30:
            pistes.append(
                "**Caritas et action sociale** : Dans un contexte de pauvreté élevée "
                f"({pays_data['taux_pauvrete']:.0f}%), l'Église est souvent le dernier filet "
                "de sécurité. Comment prioriser les œuvres de charité sans sacrifier la mission "
                "proprement spirituelle ?"
            )
            questions.append(
                "Comment articuler l'annonce de l'Évangile et l'action sociale dans un "
                "contexte de pauvreté structurelle ?"
            )

        if pays_data.get("taux_urbanisation") and pays_data["taux_urbanisation"] > 60:
            pistes.append(
                "**Pastorale urbaine** : L'urbanisation rapide ("
                f"{pays_data['taux_urbanisation']:.0f}%) transforme les territoires. "
                "Les paroisses historiques ne correspondent plus aux nouvelles zones d'habitation. "
                "Comment anticiper la création de nouvelles communautés en périphérie ?"
            )

        # Piste 4 : Liberté religieuse
        if pays_data.get("score_persecution") and pays_data["score_persecution"] > 50:
            pistes.append(
                "**Église en persécution** : Avec un score de persécution de "
                f"{pays_data['score_persecution']}/100, la survie de la communauté est en jeu. "
                "Comment maintenir l'unité et l'espérance ? Comment s'organiser clandestinement "
                "si nécessaire ? Comment solliciter la solidarité internationale ?"
            )
            questions.append(
                "Comment former les fidèles à la résilience spirituelle face à la persécution ?"
            )
        elif pays_data.get("indice_liberte_religion") == "restreinte":
            pistes.append(
                "**Liberté religieuse restreinte** : Le contexte politique limite l'action "
                "de l'Église. Comment adapter les structures pastorales sans compromettre "
                "l'identité catholique ?"
            )

        # Piste 5 : Sécularisation (pour les pays développés)
        pct_cath = next((i for i in indicateurs if i.nom == "Pourcentage de catholiques"), None)
        if pct_cath and pct_cath.valeur and pct_cath.valeur < 10 and pays_data.get("idh") and pays_data["idh"] > 0.8:
            pistes.append(
                "**Nouvelle évangélisation** : Dans un contexte de sécularisation avancée "
                f"({pct_cath.valeur:.1f}% de catholiques), l'approche pastorale doit évoluer. "
                "Comment toucher les 'sans-religion' ? Comment proposer une foi crédible et "
                "engagée dans la cité ?"
            )
            questions.append(
                "Comment les paroisses peuvent-elles devenir des 'maisons d'accueil' pour "
                "les personnes en quête de sens ?"
            )

        # Piste 6 : Éducation et santé
        if d.get("nombre_ecoles_catholiques_primaires") or d.get("nombre_hopitaux_catholiques"):
            pistes.append(
                "**Réseau éducatif et sanitaire** : L'Église dispose d'un réseau d'œuvres "
                "(écoles, hôpitaux) qui structure la société. Comment éviter que ces institutions "
                "ne perdent leur identité catholique ? Comment les faire rayonner comme "
                "lieux d'évangélisation ?"
            )

        # Piste générique si peu de pistes
        if len(pistes) < 2:
            pistes.append(
                "**Discernement global** : Les données disponibles suggèrent une situation "
                "pastorale stable. Le discernement doit porter sur la qualité de la vie "
                "chrétienne, la profondeur de la catéchèse, et la capacité d'accueil."
            )

        return pistes, questions

    def generate_report(self, diocese_id: str) -> Optional[RapportDiocese]:
        """Génère le rapport complet pour un diocèse."""
        # Trouver le diocèse
        diocese = next((d for d in self.dioceses if d.get("gcatholic_id") == diocese_id), None)
        if not diocese:
            print(f"❌ Diocèse {diocese_id} non trouvé.")
            return None

        # Données pays
        pays = diocese.get("pays", "")
        pays_data = self._get_pays_data(pays)

        # Indicateurs
        indicateurs = self._calculer_indicateurs(diocese)

        # Pistes
        pistes, questions = self._generer_pistes(diocese, indicateurs, pays_data)

        # Qualité des données
        champs_manquants = diocese.get("champs_manquants", [])
        if len(champs_manquants) == 0:
            qualite = "complete"
        elif len(champs_manquants) <= 2:
            qualite = "partielle"
        else:
            qualite = "minimale"

        # Tendances historiques (placeholder - à enrichir avec données historiques)
        tendances = []
        if diocese.get("annee_donnees"):
            tendances.append({
                "annee": diocese["annee_donnees"],
                "population_catholique": diocese.get("population_catholique"),
                "nombre_pretres": diocese.get("nombre_pretres"),
                "nombre_seminaristes": diocese.get("nombre_seminaristes"),
            })

        rapport = RapportDiocese(
            diocese_id=diocese_id,
            nom=diocese.get("nom", ""),
            type=diocese.get("type", ""),
            pays=pays,
            continent=diocese.get("continent", ""),
            date_rapport=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            population_totale=diocese.get("population_totale"),
            population_catholique=diocese.get("population_catholique"),
            pourcentage_catholique=diocese.get("pourcentage_catholique"),
            superficie_km2=diocese.get("superficie_km2"),
            nombre_pretres=diocese.get("nombre_pretres"),
            nombre_parishes=diocese.get("nombre_parishes"),
            nombre_seminaristes=diocese.get("nombre_seminaristes"),
            nombre_diacres=diocese.get("nombre_diacres"),
            nombre_religieux_hommes=diocese.get("nombre_religieux_hommes"),
            nombre_religieuses=diocese.get("nombre_religieuses"),
            annee_donnees=diocese.get("annee_donnees"),
            indicateurs=indicateurs,
            idh=pays_data.get("idh"),
            pib_par_habitant=pays_data.get("pib_par_habitant_usd"),
            taux_pauvrete=pays_data.get("taux_pauvrete"),
            taux_urbanisation=pays_data.get("taux_urbanisation"),
            contexte_socioeco=self._generer_contexte_socioeco(pays_data),
            indice_liberte_religion=pays_data.get("indice_liberte_religion", "inconnu"),
            score_persecution=pays_data.get("score_persecution"),
            contexte_liberte=pays_data.get("contexte_liberte", ""),
            defis_liberte=pays_data.get("defis_specifiques", []),
            tendances=tendances,
            pistes_discernement=pistes,
            questions_pastorales=questions,
            qualite_donnees=qualite,
            champs_manquants=champs_manquants,
            sources=["GCatholic.org", "Annuarium Statisticum Ecclesiae", "World Bank", "ACN International"],
        )

        return rapport

    def _generer_contexte_socioeco(self, pays_data: Dict) -> str:
        """Génère un texte de contexte socio-économique."""
        parts = []

        if pays_data.get("idh"):
            if pays_data["idh"] > 0.8:
                parts.append(f"Pays développé (IDH {pays_data['idh']:.3f}).")
            elif pays_data["idh"] > 0.6:
                parts.append(f"Pays en développement (IDH {pays_data['idh']:.3f}).")
            else:
                parts.append(f"Pays à faible développement humain (IDH {pays_data['idh']:.3f}).")

        if pays_data.get("taux_pauvrete"):
            if pays_data["taux_pauvrete"] > 40:
                parts.append(f"Pauvreté extrême ({pays_data['taux_pauvrete']:.0f}% de la population).")
            elif pays_data["taux_pauvrete"] > 20:
                parts.append(f"Pauvreté significative ({pays_data['taux_pauvrete']:.0f}%).")
            else:
                parts.append(f"Pauvreté modérée ({pays_data['taux_pauvrete']:.0f}%).")

        if pays_data.get("taux_urbanisation"):
            if pays_data["taux_urbanisation"] > 70:
                parts.append(f"Fortement urbanisé ({pays_data['taux_urbanisation']:.0f}%).")
            elif pays_data["taux_urbanisation"] > 40:
                parts.append(f"Transition urbaine en cours ({pays_data['taux_urbanisation']:.0f}%).")
            else:
                parts.append(f"Majoritairement rural ({pays_data['taux_urbanisation']:.0f}%).")

        return " ".join(parts) if parts else "Données socio-économiques non disponibles."

    def generate_all_reports(self, output_dir: str):
        """Génère les rapports pour tous les diocèses."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        print(f"🚀 Génération des rapports pour {len(self.dioceses)} diocèses...")

        for i, diocese in enumerate(self.dioceses, 1):
            diocese_id = diocese.get("gcatholic_id", "")
            if not diocese_id:
                continue

            rapport = self.generate_report(diocese_id)
            if rapport:
                file_path = output_path / f"{diocese_id}.json"
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(asdict(rapport), f, ensure_ascii=False, indent=2)

            if i % 100 == 0:
                print(f"  ✅ {i}/{len(self.dioceses)} rapports générés...")

        print(f"\n✅ Tous les rapports sauvegardés dans {output_dir}")

    def export_csv_summary(self, output_path: str):
        """Exporte un résumé CSV de tous les rapports."""
        rows = []

        for diocese in self.dioceses:
            diocese_id = diocese.get("gcatholic_id", "")
            rapport = self.generate_report(diocese_id)
            if not rapport:
                continue

            # Extraire les indicateurs clés
            cath_pretre = next((i.valeur for i in rapport.indicateurs if i.nom == "Catholiques par prêtre"), None)
            pct_cath = next((i.valeur for i in rapport.indicateurs if i.nom == "Pourcentage de catholiques"), None)
            taux_voc = next((i.valeur for i in rapport.indicateurs if i.nom == "Taux de vocations"), None)

            rows.append({
                "id": diocese_id,
                "nom": rapport.nom,
                "pays": rapport.pays,
                "continent": rapport.continent,
                "population_catholique": rapport.population_catholique,
                "nombre_pretres": rapport.nombre_pretres,
                "catholiques_par_pretre": cath_pretre,
                "pourcentage_catholique": pct_cath,
                "taux_vocations": taux_voc,
                "idh": rapport.idh,
                "score_persecution": rapport.score_persecution,
                "qualite_donnees": rapport.qualite_donnees,
                "nombre_pistes": len(rapport.pistes_discernement),
            })

        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys() if rows else [])
            writer.writeheader()
            writer.writerows(rows)

        print(f"✅ Résumé CSV exporté : {output_path}")


# ============================================================
# MAIN
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Moteur de contextualisation Carta Pastorale")
    parser.add_argument("--input", "-i", required=True, help="Fichier JSON des diocèses (sortie du scraper)")
    parser.add_argument("--output", "-o", default="data/rapports", help="Dossier de sortie des rapports")
    parser.add_argument("--diocese", "-d", help="Générer un seul rapport par ID")
    parser.add_argument("--csv", "-c", help="Exporter un résumé CSV")

    args = parser.parse_args()

    # Chargement
    print(f"📂 Chargement des données depuis {args.input}...")
    with open(args.input, "r", encoding="utf-8") as f:
        dioceses = json.load(f)
    print(f"✅ {len(dioceses)} diocèses chargés.")

    # Initialisation
    engine = Contextualizer(dioceses)

    if args.diocese:
        rapport = engine.generate_report(args.diocese)
        if rapport:
            print("\n" + "=" * 70)
            print(f"📄 RAPPORT : {rapport.nom}")
            print("=" * 70)
            print(json.dumps(asdict(rapport), ensure_ascii=False, indent=2))
    else:
        engine.generate_all_reports(args.output)

        if args.csv:
            engine.export_csv_summary(args.csv)


if __name__ == "__main__":
    main()