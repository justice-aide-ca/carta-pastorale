"""Données socio-économiques et liberté religieuse par pays.
Sources : Banque mondiale, PNUD, Portes ouvertes, ACN.
"""
from typing import Dict, Any

SOCIO_ECO_DATA: Dict[str, Dict[str, Any]] = {
    # Europe de l'Ouest
    "France": {"idh": 0.910, "pib": 46000, "urbanisation": 82, "liberte": 95, "persecution": 0, "contexte": "Liberté religieuse totale. Laïcité constitutionnelle. Église catholique historiquement dominante mais en déclin progressif.", "defis": ["Sécularisation croissante", "Diminution des pratiquants", "Maintien du lien avec les jeunes générations"]},
    "Italy": {"idh": 0.906, "pib": 37000, "urbanisation": 72, "liberte": 95, "persecution": 0, "contexte": "Liberté religieuse garantie. Catholicisme majoritaire avec forte présence du Vatican. Déclin des vocations mais patrimoine ecclésial immense.", "defis": ["Baisse des vocations sacerdotales", "Sécularisation urbaine", "Gestion du patrimoine religieux"]},
    "Spain": {"idh": 0.911, "pib": 32000, "urbanisation": 81, "liberte": 94, "persecution": 0, "contexte": "Liberté religieuse totale. Catholicisme historique en déclin rapide. Montée de l'indifférence religieuse.", "defis": ["Abandon de la pratique religieuse", "Sécularisation massive", "Nouvelle évangélisation des jeunes"]},
    "Germany": {"idh": 0.950, "pib": 53000, "urbanisation": 78, "liberte": 95, "persecution": 0, "contexte": "Liberté religieuse totale. Catholicisme et protestantisme en déclin. Forte présence musulmane due à l'immigration.", "defis": ["Déclin des deux grandes Églises", "Immigration et dialogue interreligieux", "Sécularisation de la société"]},
    "Belgium": {"idh": 0.942, "pib": 56000, "urbanisation": 98, "liberte": 93, "persecution": 0, "contexte": "Liberté religieuse. Catholicisme historique en déclin très rapide. Un des pays les plus sécularisés d'Europe.", "defis": ["Sécularisation avancée", "Fermetures d'églises", "Maintien d'une présence chrétienne"]},
    "Netherlands": {"idh": 0.946, "pib": 61000, "urbanisation": 93, "liberte": 94, "persecution": 0, "contexte": "Liberté religieuse. Pays historiquement calviniste puis très sécularisé. Catholicisme minoritaire mais actif.", "defis": ["Sécularisation très avancée", "Catholicisme minoritaire", "Dialogue interreligieux"]},
    "Portugal": {"idh": 0.874, "pib": 27000, "urbanisation": 67, "liberte": 96, "persecution": 0, "contexte": "Liberté religieuse totale. Catholicisme très ancré culturellement malgré un déclin des pratiquants.", "defis": ["Vieillissement des prêtres", "Déclin des pratiquants", "Évangélisation des jeunes"]},
    "Austria": {"idh": 0.926, "pib": 56000, "urbanisation": 60, "liberte": 94, "persecution": 0, "contexte": "Liberté religieuse. Catholicisme et protestantisme historiques. Société stable mais en déclin religieux.", "defis": ["Sorties massives de l'Église", "Sécularisation urbaine", "Renouveau spirituel"]},
    "Switzerland": {"idh": 0.967, "pib": 93000, "urbanisation": 74, "liberte": 96, "persecution": 0, "contexte": "Liberté religieuse totale. Catholicisme et protestantisme répartis selon les cantons. Société très prospère.", "defis": ["Sécularisation progressive", "Pluralisme religieux", "Maintien de l'identité catholique"]},
    "United Kingdom": {"idh": 0.940, "pib": 49000, "urbanisation": 84, "liberte": 92, "persecution": 0, "contexte": "Liberté religieuse. Catholicisme minoritaire historique. Présence importante d'immigrants catholiques.", "defis": ["Catholicisme minoritaire", "Sécularisation massive", "Scandales et confiance"]},
    "Ireland": {"idh": 0.950, "pib": 106000, "urbanisation": 64, "liberte": 93, "persecution": 0, "contexte": "Liberté religieuse. Catholicisme historiquement dominant en effondrement rapide après les scandales.", "defis": ["Effondrement de la confiance", "Sécularisation brutale", "Reconstruction de l'Église"]},
    "Poland": {"idh": 0.881, "pib": 22000, "urbanisation": 60, "liberte": 88, "persecution": 0, "contexte": "Liberté religieuse. Catholicisme très majoritaire et culturellement dominant. Déclin des pratiquants mais forte identité catholique.", "defis": ["Déclin des vocations", "Sécularisation des jeunes", "Rôle de l'Église dans la société"]},

    # Amérique du Nord
    "United States": {"idh": 0.927, "pib": 76000, "urbanisation": 83, "liberte": 90, "persecution": 0, "contexte": "Liberté religieuse constitutionnelle. Catholicisme minoritaire (~20%) mais très diversifié. Montée de l'hostilité culturelle en certains milieux.", "defis": ["Polarisation politique et religieuse", "Déclin des vocations", "Immigration catholique latino-américaine"]},
    "Canada": {"idh": 0.935, "pib": 55000, "urbanisation": 82, "liberte": 92, "persecution": 0, "contexte": "Liberté religieuse. Catholicisme historique (francophone) en déclin. Multiculturalisme affirmé.", "defis": ["Déclin du catholicisme québécois", "Sécularisation généralisée", "Immigration et diversité"]},
    "Mexico": {"idh": 0.781, "pib": 12000, "urbanisation": 81, "liberte": 82, "persecution": 15, "contexte": "Liberté religieuse constitutionnelle mais tensions dans certaines régions. Catholicisme majoritaire mais évangéliques en croissance.", "defis": ["Croissance des églises évangéliques", "Violence liée au narcotrafic", "Tensions dans les communautés indigènes"]},

    # Amérique du Sud
    "Brazil": {"idh": 0.760, "pib": 9000, "urbanisation": 87, "liberte": 80, "persecution": 10, "contexte": "Liberté religieuse globale. Catholicisme en déclin rapide face aux évangéliques. Pays le plus peuplé d'Amérique latine.", "defis": ["Perte massive de fidèles vers les évangéliques", "Pénuries de prêtres en zone rurale", "Inégalités sociales massives"]},
    "Argentina": {"idh": 0.849, "pib": 14000, "urbanisation": 92, "liberte": 88, "persecution": 5, "contexte": "Liberté religieuse. Catholicisme historiquement dominant mais en déclin. Crise économique persistante.", "defis": ["Déclin des pratiquants", "Crise économique et pauvreté", "Sécularisation des jeunes"]},
    "Colombia": {"idh": 0.758, "pib": 7000, "urbanisation": 82, "liberte": 78, "persecution": 25, "contexte": "Liberté religieuse formelle mais violences dans les zones rurales. Catholicisme majoritaire. Présence de groupes armés.", "defis": ["Violence dans les zones rurales", "Déclin du catholicisme", "Évangéliques en croissance"]},
    "Peru": {"idh": 0.762, "pib": 8000, "urbanisation": 79, "liberte": 85, "persecution": 5, "contexte": "Liberté religieuse. Catholicisme majoritaire avec forte présence des communautés indigènes. Tensions sociales.", "defis": ["Pauvreté rurale", "Déclin des vocations", "Évangéliques en croissance"]},
    "Venezuela": {"idh": 0.699, "pib": 3500, "urbanisation": 88, "liberte": 60, "persecution": 35, "contexte": "Liberté religieuse restreinte sous le régime autoritaire. Catholicisme historique. Crise humanitaire massive.", "defis": ["Crise humanitaire et exode", "Persécution politique", "Pénurie de ressources"]},
    "Chile": {"idh": 0.860, "pib": 17000, "urbanisation": 88, "liberte": 88, "persecution": 5, "contexte": "Liberté religieuse. Catholicisme en déclin rapide après les scandales. Société très sécularisée.", "defis": ["Sécularisation massive", "Scandales et confiance", "Nouvelle évangélisation"]},
    "Ecuador": {"idh": 0.765, "pib": 6500, "urbanisation": 65, "liberte": 85, "persecution": 5, "contexte": "Liberté religieuse. Catholicisme majoritaire. Tensions sociales et indigènes.", "defis": ["Pauvreté et inégalités", "Déclin des pratiquants", "Évangéliques en croissance"]},
    "Bolivia": {"idh": 0.692, "pib": 3600, "urbanisation": 72, "liberte": 80, "persecution": 10, "contexte": "Liberté religieuse relative. Catholicisme avec forte présence des traditions indigènes. Tensions politiques.", "defis": ["Pauvreté rurale", "Tensions politiques", "Syncrétisme religieux"]},
    "Paraguay": {"idh": 0.731, "pib": 6000, "urbanisation": 63, "liberte": 90, "persecution": 0, "contexte": "Liberté religieuse. Catholicisme très majoritaire. Pays le plus homogène religieusement d'Amérique du Sud.", "defis": ["Pauvreté et inégalités", "Déclin des vocations", "Émigration des jeunes"]},
    "Uruguay": {"idh": 0.830, "pib": 21000, "urbanisation": 96, "liberte": 95, "persecution": 0, "contexte": "Liberté religieuse. Le pays le plus sécularisé d'Amérique latine. Catholicisme minoritaire.", "defis": ["Sécularisation massive", "Catholicisme minoritaire", "Nouvelle évangélisation"]},

    # Afrique
    "Nigeria": {"idh": 0.548, "pib": 2200, "urbanisation": 54, "liberte": 45, "persecution": 75, "contexte": "Liberté religieuse très menacée. Violence extrême entre communautés dans le nord (Boko Haram, Fulani). Catholicisme très dynamique au sud.", "defis": ["Persécution violente dans le nord", "Kidnappings de prêtres et religieux", "Déplacements massifs de population"]},
    "Democratic Republic of the Congo": {"idh": 0.481, "pib": 650, "urbanisation": 46, "liberte": 55, "persecution": 45, "contexte": "Liberté religieuse formelle mais instabilité extrême. Catholicisme très majoritaire et très actif. Guerres et conflits armés persistants.", "defis": ["Conflits armés et insécurité", "Pauvreté extrême", "Déplacés et réfugiés"]},
    "Kenya": {"idh": 0.601, "pib": 2100, "urbanisation": 28, "liberte": 70, "persecution": 30, "contexte": "Liberté religieuse relative. Catholicisme minoritaire (~20%) dans un pays majoritairement protestant et musulman. Tensions interreligieuses.", "defis": ["Tensions interreligieuses", "Pauvreté rurale", "Corruption"]},
    "Uganda": {"idh": 0.550, "pib": 1000, "urbanisation": 26, "liberte": 65, "persecution": 35, "contexte": "Liberté religieuse sous pression (loi anti-LGBT). Catholicisme très actif (~40%). Croissance démographique massive.", "defis": ["Pressions politiques", "Pauvreté et sous-développement", "Croissance démographique"]},
    "Tanzania": {"idh": 0.549, "pib": 1200, "urbanisation": 36, "liberte": 75, "persecution": 20, "contexte": "Liberté religieuse relative. Catholicisme minoritaire mais bien établi. Coexistence avec islam et religions traditionnelles.", "defis": ["Pauvreté rurale", "Islam radical dans certaines zones", "Développement économique"]},
    "South Africa": {"idh": 0.717, "pib": 7000, "urbanisation": 68, "liberte": 90, "persecution": 5, "contexte": "Liberté religieuse totale. Catholicisme minoritaire (~7%). Pays le plus développé d'Afrique mais inégalités extrêmes.", "defis": ["Inégalités sociales massives", "Criminalité", "Catholicisme minoritaire"]},
    "Ethiopia": {"idh": 0.498, "pib": 1100, "urbanisation": 23, "liberte": 50, "persecution": 55, "contexte": "Liberté religieuse très restreinte. Catholicisme minoritaire dans un pays orthodoxe historique. Conflits ethniques et guerre civile récente.", "defis": ["Conflits ethniques", "Famine et insécurité alimentaire", "Persécution des minorités"]},
    "Egypt": {"idh": 0.731, "pib": 4300, "urbanisation": 43, "liberte": 35, "persecution": 65, "contexte": "Liberté religieuse très restreinte. Catholicisme minoritaire (<1%) dans un pays musulman à 90%. Discrimination systémique contre les chrétiens.", "defis": ["Discrimination systémique", "Attentats contre les églises", "Restrictions de construction d'églises"]},
    "Sudan": {"idh": 0.516, "pib": 800, "urbanisation": 36, "liberte": 25, "persecution": 80, "contexte": "Liberté religieuse quasi inexistante. Catholicisme très minoritaire. Guerre civile et persécution extrême des chrétiens.", "defis": ["Guerre civile", "Persécution extrême", "Famine et déplacements"]},
    "Cameroon": {"idh": 0.587, "pib": 1600, "urbanisation": 59, "liberte": 60, "persecution": 40, "contexte": "Liberté religieuse menacée dans les régions anglophones (crise séparatiste). Catholicisme très actif (~25%).", "defis": ["Crise anglophone", "Conflit armé", "Déplacés internes"]},
    "Central African Republic": {"idh": 0.387, "pib": 500, "urbanisation": 43, "liberte": 40, "persecution": 70, "contexte": "Liberté religieuse très menacée. Catholicisme majoritaire mais persécuté par les groupes armés. État en déliquescence.", "defis": ["Guerre civile", "Persécution des chrétiens", "Déliquescence de l'État"]},
    "Madagascar": {"idh": 0.487, "pib": 500, "urbanisation": 39, "liberte": 85, "persecution": 5, "contexte": "Liberté religieuse. Catholicisme très ancré (~25%). Pauvreté massive et instabilité politique.", "defis": ["Pauvreté extrême", "Instabilité politique", "Déforestation et écologie"]},
    "Ghana": {"idh": 0.632, "pib": 2500, "urbanisation": 58, "liberte": 90, "persecution": 5, "contexte": "Liberté religieuse. Catholicisme minoritaire (~10%) dans un pays très religieux. Démocratie stable.", "defis": ["Croissance des églises pentecôtistes", "Corruption", "Développement économique"]},
    "Ivory Coast": {"idh": 0.550, "pib": 2700, "urbanisation": 52, "liberte": 85, "persecution": 10, "contexte": "Liberté religieuse. Catholicisme très actif (~30%). Stabilité relative après les crises politiques.", "defis": ["Reconstruction post-conflit", "Pauvreté rurale", "Évangéliques en croissance"]},
    "Angola": {"idh": 0.586, "pib": 3000, "urbanisation": 68, "liberte": 75, "persecution": 15, "contexte": "Liberté religieuse relative. Catholicisme très majoritaire (~50%). Richesse pétrolière mal répartie.", "defis": ["Inégalités sociales", "Autoritarisme politique", "Pauvreté malgré les ressources"]},
    "Mozambique": {"idh": 0.456, "pib": 600, "urbanisation": 38, "liberte": 55, "persecution": 50, "contexte": "Liberté religieuse menacée dans le nord (insurrection islamiste). Catholicisme minoritaire (~30%).", "defis": ["Insurrection islamiste dans le nord", "Pauvreté extrême", "Cyclones et catastrophes naturelles"]},
    "Malawi": {"idh": 0.508, "pib": 500, "urbanisation": 18, "liberte": 85, "persecution": 5, "contexte": "Liberté religieuse. Catholicisme très actif (~20%). Un des pays les plus pauvres du monde.", "defis": ["Pauvreté extrême", "Dépendance agricole", "Croissance démographique"]},
    "Zambia": {"idh": 0.569, "pib": 1300, "urbanisation": 45, "liberte": 90, "persecution": 5, "contexte": "Liberté religieuse. Catholicisme très actif (~30%). Démocratie stable mais économie fragile.", "defis": ["Dette et crise économique", "Pauvreté rurale", "Sida et santé publique"]},
    "Zimbabwe": {"idh": 0.550, "pib": 2000, "urbanisation": 33, "liberte": 70, "persecution": 20, "contexte": "Liberté religieuse sous pression politique. Catholicisme très actif. Hyperinflation et crise économique persistante.", "defis": ["Crise économique", "Autoritarisme", "Pauvreté massive"]},
    "Rwanda": {"idh": 0.548, "pib": 900, "urbanisation": 18, "liberte": 60, "persecution": 25, "contexte": "Liberté religieuse restreinte (régime autoritaire). Catholicisme très majoritaire mais en déclin. Génocide de 1994 toujours présent.", "defis": ["Autoritarisme politique", "Réconciliation post-génocide", "Déclin des pratiquants"]},
    "Burundi": {"idh": 0.426, "pib": 300, "urbanisation": 14, "liberte": 50, "persecution": 40, "contexte": "Liberté religieuse restreinte. Catholicisme très majoritaire (~60%). Crise politique et économique.", "defis": ["Crise politique", "Pauvreté extrême", "Restrictions sur la société civile"]},
    "South Sudan": {"idh": 0.385, "pib": 1000, "urbanisation": 20, "liberte": 40, "persecution": 70, "contexte": "Liberté religieuse très menacée. Catholicisme très actif (~40%). Guerre civile chronique et famine.", "defis": ["Guerre civile", "Famine", "Déplacés massifs"]},

    # Asie
    "India": {"idh": 0.644, "pib": 2500, "urbanisation": 36, "liberte": 40, "persecution": 70, "contexte": "Liberté religieuse très menacée sous le nationalisme hindou. Catholicisme minoritaire (~2%). Violence anti-chrétienne croissante.", "defis": ["Nationalisme hindou et persécution", "Lois anti-conversion", "Attaques contre les chrétiens"]},
    "Philippines": {"idh": 0.710, "pib": 3500, "urbanisation": 48, "liberte": 85, "persecution": 15, "contexte": "Liberté religieuse. Catholicisme très majoritaire (~80%). Seul pays catholique d'Asie. Déclin des pratiquants.", "defis": ["Déclin des pratiquants", "Croissance des églises évangéliques", "Conflit dans le sud (Mindanao)"]},
    "Indonesia": {"idh": 0.713, "pib": 5000, "urbanisation": 58, "liberte": 50, "persecution": 50, "contexte": "Liberté religieuse restreinte. Catholicisme minoritaire (~3%) dans le plus grand pays musulman du monde. Discrimination et violences sporadiques.", "defis": ["Discrimination légale", "Violences communautaires", "Radicalisme islamique"]},
    "Vietnam": {"idh": 0.703, "pib": 4300, "urbanisation": 38, "liberte": 35, "persecution": 60, "contexte": "Liberté religieuse très restreinte (régime communiste). Catholicisme persécuté mais très résilient (~7%). Église souterraine active.", "defis": ["Contrôle étatique sur l'Église", "Persécution des leaders", "Église souterraine"]},
    "China": {"idh": 0.768, "pib": 13000, "urbanisation": 65, "liberte": 15, "persecution": 90, "contexte": "Liberté religieuse quasi inexistante. Catholicisme persécuté (Église patriotique contrôlée, Église souterraine). Surveillance totale.", "defis": ["Persécution systémique", "Église patriotique vs souterraine", "Surveillance numérique"]},
    "Japan": {"idh": 0.920, "pib": 34000, "urbanisation": 92, "liberte": 95, "persecution": 0, "contexte": "Liberté religieuse totale. Catholicisme très minoritaire (<1%). Pays très sécularisé avec traditions shintoïstes et bouddhistes.", "defis": ["Catholicisme quasi invisible", "Sécularisation avancée", "Vieillissement de la population"]},
    "South Korea": {"idh": 0.925, "pib": 35000, "urbanisation": 81, "liberte": 90, "persecution": 0, "contexte": "Liberté religieuse. Catholicisme minoritaire mais dynamique (~10%). Pays très développé avec forte croissance des églises.", "defis": ["Catholicisme minoritaire", "Concurrence des églises protestantes", "Vieillissement rapide"]},
    "Pakistan": {"idh": 0.540, "pib": 1500, "urbanisation": 38, "liberte": 20, "persecution": 85, "contexte": "Liberté religieuse quasi inexistante. Catholicisme très minoritaire (~1%). Lois sur le blasphème utilisées contre les chrétiens. Violence extrême.", "defis": ["Lois sur le blasphème", "Attentats contre les églises", "Discrimination systémique"]},
    "Bangladesh": {"idh": 0.670, "pib": 2800, "urbanisation": 39, "liberte": 45, "persecution": 60, "contexte": "Liberté religieuse très restreinte. Catholicisme minoritaire (<1%). Pressions islamistes croissantes.", "defis": ["Pressions islamistes", "Pauvreté et surpopulation", "Changements climatiques"]},
    "Sri Lanka": {"idh": 0.782, "pib": 4000, "urbanisation": 19, "liberte": 60, "persecution": 35, "contexte": "Liberté religieuse relative. Catholicisme minoritaire (~6%). Crise économique massive et tensions ethniques.", "defis": ["Crise économique", "Tensions ethniques", "Attentats de 2019"]},
    "Myanmar": {"idh": 0.585, "pib": 1200, "urbanisation": 32, "liberte": 30, "persecution": 75, "contexte": "Liberté religieuse quasi inexistante (coup d'État militaire). Catholicisme persécuté mais très résilient. Guerre civile généralisée.", "defis": ["Coup d'État militaire", "Guerre civile", "Persécution des minorités"]},
    "Thailand": {"idh": 0.803, "pib": 7500, "urbanisation": 54, "liberte": 80, "persecution": 10, "contexte": "Liberté religieuse relative. Catholicisme minoritaire (<1%). Pays bouddhiste très majoritaire. Monarchie.", "defis": ["Catholicisme très minoritaire", "Restrictions législatives", "Développement inégal"]},
    "Malaysia": {"idh": 0.803, "pib": 13000, "urbanisation": 78, "liberte": 50, "persecution": 40, "contexte": "Liberté religieuse restreinte. Catholicisme minoritaire (~3%). Lois sur l'islam comme religion d'État. Discrimination légale.", "defis": ["Discrimination légale", "Interdiction de conversion", "Restrictions sur l'usage du mot 'Allah'"]},
    "Laos": {"idh": 0.620, "pib": 2500, "urbanisation": 37, "liberte": 30, "persecution": 65, "contexte": "Liberté religieuse très restreinte (régime communiste). Catholicisme persécuté mais résilient. Église souterraine.", "defis": ["Contrôle communiste", "Persécution des chrétiens", "Pauvreté rurale"]},
    "Cambodia": {"idh": 0.600, "pib": 1700, "urbanisation": 25, "liberte": 55, "persecution": 30, "contexte": "Liberté religieuse restreinte. Catholicisme minoritaire (~1%). Régime autoritaire. Héritage du génocide des Khmers rouges.", "defis": ["Autoritarisme", "Pauvreté rurale", "Corruption"]},
    "Nepal": {"idh": 0.602, "pib": 1400, "urbanisation": 22, "liberte": 45, "persecution": 50, "contexte": "Liberté religieuse restreinte. Catholicisme minoritaire. Lois anti-conversion. Pays hindou historique.", "defis": ["Lois anti-conversion", "Pauvreté et sous-développement", "Séismes et catastrophes"]},
    "East Timor": {"idh": 0.566, "pib": 2400, "urbanisation": 32, "liberte": 95, "persecution": 0, "contexte": "Liberté religieuse totale. Catholicisme très majoritaire (~97%). Le pays le plus catholique d'Asie. Jeune nation.", "defis": ["Dépendance pétrolière", "Pauvreté massive", "Développement des institutions"]},

    # Moyen-Orient
    "Lebanon": {"idh": 0.706, "pib": 4000, "urbanisation": 89, "liberte": 55, "persecution": 35, "contexte": "Liberté religieuse formelle mais instabilité extrême. Catholicisme très actif (~30%). Effondrement économique total.", "defis": ["Effondrement économique", "Instabilité politique", "Exode massif des chrétiens"]},
    "Syria": {"idh": 0.557, "pib": 800, "urbanisation": 55, "liberte": 20, "persecution": 85, "contexte": "Liberté religieuse quasi inexistante. Catholicisme persécuté. Guerre civile de 12 ans. Exode massif des chrétiens.", "defis": ["Guerre civile", "Exode des chrétiens", "Destruction des églises"]},
    "Iraq": {"idh": 0.686, "pib": 6000, "urbanisation": 71, "liberte": 25, "persecution": 80, "contexte": "Liberté religieuse quasi inexistante. Catholicisme persécuté (chaldéens, assyriens). Génocide de 2014 par Daech. Exode massif.", "defis": ["Séquelles du génocide de Daech", "Exode des chrétiens", "Instabilité politique"]},
    "Iran": {"idh": 0.780, "pib": 4500, "urbanisation": 77, "liberte": 10, "persecution": 95, "contexte": "Liberté religieuse inexistante. Catholicisme persécuté (arméniens, chaldéens). Régime théocratique islamique. Persécution systémique.", "defis": ["Persécution systémique", "Interdiction de l'évangélisation", "Arrestations de chrétiens"]},
    "Israel": {"idh": 0.915, "pib": 55000, "urbanisation": 93, "liberte": 80, "persecution": 10, "contexte": "Liberté religieuse relative. Catholicisme minoritaire (~2%). Conflit israélo-palestinien. Terre sainte.", "defis": ["Conflit israélo-palestinien", "Catholicisme minoritaire", "Accès aux Lieux saints"]},
    "Palestine": {"idh": 0.715, "pib": 4000, "urbanisation": 77, "liberte": 50, "persecution": 40, "contexte": "Liberté religieuse menacée. Catholicisme minoritaire mais historique (Bethléem, Jérusalem). Occupation et conflit.", "defis": ["Occupation et restrictions", "Exode des chrétiens de Bethléem", "Accès aux Lieux saints"]},
    "Jordan": {"idh": 0.736, "pib": 4500, "urbanisation": 92, "liberte": 70, "persecution": 20, "contexte": "Liberté religieuse relative. Catholicisme minoritaire mais protégé. Pays stable au cœur d'une région en crise.", "defis": ["Refugiés syriens et irakiens", "Pressions économiques", "Catholicisme minoritaire"]},
    "Turkey": {"idh": 0.838, "pib": 11000, "urbanisation": 77, "liberte": 40, "persecution": 55, "contexte": "Liberté religieuse très restreinte. Catholicisme persécuté (arméniens, syriaques). Nationalisme turc et islam politique.", "defis": ["Nationalisme et persécution", "Restrictions sur les minorités", "Conversion de Sainte-Sophie"]},
    "Saudi Arabia": {"idh": 0.875, "pib": 32000, "urbanisation": 85, "liberte": 0, "persecution": 100, "contexte": "Liberté religieuse totalement inexistante. Catholicisme interdit. Pays le plus fermé du monde religieusement. Expatriés célébrant en secret.", "defis": ["Interdiction totale de l'évangélisation", "Risque de mort pour conversion", "Culte clandestin"]},
    "United Arab Emirates": {"idh": 0.937, "pib": 53000, "urbanisation": 88, "liberte": 35, "persecution": 45, "contexte": "Liberté religieuse restreinte. Catholicisme d'expatriés (Indiens, Philippins). Tolérance calculée mais conversion interdite.", "defis": ["Interdiction de la conversion", "Catholicisme d'expatriés", "Droits des travailleurs migrants"]},
    "Kuwait": {"idh": 0.831, "pib": 32000, "urbanisation": 100, "liberte": 40, "persecution": 40, "contexte": "Liberté religieuse restreinte. Catholicisme d'expatriés. Tolérance limitée.", "defis": ["Interdiction de la conversion", "Catholicisme d'expatriés", "Restrictions religieuses"]},
    "Qatar": {"idh": 0.855, "pib": 90000, "urbanisation": 99, "liberte": 35, "persecution": 45, "contexte": "Liberté religieuse restreinte. Catholicisme d'expatriés. Tolérance calculée pour les travailleurs étrangers.", "defis": ["Interdiction de la conversion", "Catholicisme d'expatriés", "Droits des travailleurs migrants"]},
    "Bahrain": {"idh": 0.824, "pib": 28000, "urbanisation": 90, "liberte": 45, "persecution": 35, "contexte": "Liberté religieuse relative. Catholicisme minoritaire. Pays plus ouvert que ses voisins.", "defis": ["Discrimination légale", "Catholicisme minoritaire", "Tensions politiques"]},
    "Oman": {"idh": 0.816, "pib": 19000, "urbanisation": 88, "liberte": 50, "persecution": 30, "contexte": "Liberté religieuse relative. Catholicisme d'expatriés. Pays traditionnellement tolérant.", "defis": ["Interdiction de la conversion", "Catholicisme d'expatriés", "Modernisation contrôlée"]},
    "Yemen": {"idh": 0.455, "pib": 600, "urbanisation": 38, "liberte": 15, "persecution": 90, "contexte": "Liberté religieuse inexistante. Catholicisme quasi éteint. Guerre civile et famine. Chrétiens ciblés par les Houthis.", "defis": ["Guerre civile", "Famine", "Persécution extrême"]},

    # Océanie
    "Australia": {"idh": 0.946, "pib": 65000, "urbanisation": 86, "liberte": 95, "persecution": 0, "contexte": "Liberté religieuse totale. Catholicisme minoritaire (~20%) mais très actif. Multiculturalisme.", "defis": ["Sécularisation croissante", "Scandales et confiance", "Catholicisme minoritaire"]},
    "New Zealand": {"idh": 0.939, "pib": 48000, "urbanisation": 87, "liberte": 95, "persecution": 0, "contexte": "Liberté religieuse totale. Catholicisme minoritaire (~10%). Pays très sécularisé.", "defis": ["Sécularisation massive", "Catholicisme minoritaire", "Nouvelle évangélisation"]},
    "Papua New Guinea": {"idh": 0.568, "pib": 3000, "urbanisation": 14, "liberte": 90, "persecution": 5, "contexte": "Liberté religieuse. Catholicisme très majoritaire (~25%). Pays très divers ethniquement.", "defis": ["Pauvreté rurale", "Violences tribales", "Développement des infrastructures"]},

    # Amérique centrale et Caraïbes
    "Cuba": {"idh": 0.764, "pib": 9500, "urbanisation": 78, "liberte": 45, "persecution": 40, "contexte": "Liberté religieuse restreinte (régime communiste). Catholicisme historique mais affaibli. Ouverture limitée depuis 2015.", "defis": ["Contrôle étatique", "Pénuries économiques", "Exode des jeunes"]},
    "Haiti": {"idh": 0.552, "pib": 1800, "urbanisation": 59, "liberte": 80, "persecution": 15, "contexte": "Liberté religieuse. Catholicisme très majoritaire mais concurrence du vaudou. Effondrement de l'État.", "defis": ["Effondrement de l'État", "Gangs et insécurité", "Pauvreté extrême"]},
    "Dominican Republic": {"idh": 0.766, "pib": 11000, "urbanisation": 84, "liberte": 95, "persecution": 0, "contexte": "Liberté religieuse totale. Catholicisme très majoritaire. Pays stable en comparaison d'Haïti.", "defis": ["Déclin des pratiquants", "Immigration haïtienne", "Inégalités"]},
    "Guatemala": {"idh": 0.663, "pib": 5600, "urbanisation": 52, "liberte": 90, "persecution": 5, "contexte": "Liberté religieuse. Catholicisme historique mais évangéliques en forte croissance. Violence des gangs.", "defis": ["Croissance des évangéliques", "Violence des gangs", "Pauvreté et inégalités"]},
    "El Salvador": {"idh": 0.674, "pib": 5400, "urbanisation": 78, "liberte": 85, "persecution": 10, "contexte": "Liberté religieuse. Catholicisme historique. Réduction drastique de la violence sous Bukele.", "defis": ["Autoritarisme de Bukele", "Pauvreté rurale", "Déclin du catholicisme"]},
    "Honduras": {"idh": 0.624, "pib": 3100, "urbanisation": 59, "liberte": 85, "persecution": 10, "contexte": "Liberté religieuse. Catholicisme historique. Violence des gangs et pauvreté.", "defis": ["Violence des gangs", "Pauvreté", "Corruption"]},
    "Nicaragua": {"idh": 0.669, "pib": 2300, "urbanisation": 60, "liberte": 25, "persecution": 70, "contexte": "Liberté religieuse très menacée. Catholicisme persécuté par le régime d'Ortega. Église considérée comme ennemie.", "defis": ["Persécution du régime Ortega", "Fermeture d'ONG catholiques", "Exil de prêtres et évêques"]},
    "Costa Rica": {"idh": 0.806, "pib": 14000, "urbanisation": 83, "liberte": 95, "persecution": 0, "contexte": "Liberté religieuse totale. Catholicisme historique mais en déclin. Démocratie stable.", "defis": ["Déclin des pratiquants", "Sécularisation", "Développement durable"]},
    "Panama": {"idh": 0.820, "pib": 19000, "urbanisation": 69, "liberte": 95, "persecution": 0, "contexte": "Liberté religieuse totale. Catholicisme très majoritaire. Pays prospère et stable.", "defis": ["Déclin des pratiquants", "Inégalités", "Migration"]},
    "Puerto Rico": {"idh": 0.880, "pib": 35000, "urbanisation": 94, "liberte": 95, "persecution": 0, "contexte": "Liberté religieuse totale (territoire US). Catholicisme historique mais en déclin. Crise économique.", "defis": ["Déclin des pratiquants", "Crise économique", "Ouragans et catastrophes"]},
    "Jamaica": {"idh": 0.706, "pib": 6000, "urbanisation": 57, "liberte": 95, "persecution": 0, "contexte": "Liberté religieuse totale. Catholicisme minoritaire. Pays très religieux mais protestant majoritaire.", "defis": ["Catholicisme minoritaire", "Violence", "Développement économique"]},
    "Trinidad and Tobago": {"idh": 0.814, "pib": 18000, "urbanisation": 53, "liberte": 90, "persecution": 5, "contexte": "Liberté religieuse. Catholicisme minoritaire (~20%). Pays pétrolier multiculturel.", "defis": ["Catholicisme minoritaire", "Crime", "Diversité religieuse"]},

    # Europe de l'Est
    "Ukraine": {"idh": 0.773, "pib": 5000, "urbanisation": 70, "liberte": 70, "persecution": 25, "contexte": "Liberté religieuse menacée par la guerre. Catholicisme minoritaire (grec et latin). Guerre d'invasion russe depuis 2022.", "defis": ["Guerre d'invasion russe", "Destruction des églises", "Exode massif"]},
    "Russia": {"idh": 0.822, "pib": 13000, "urbanisation": 75, "liberte": 30, "persecution": 60, "contexte": "Liberté religieuse très restreinte. Catholicisme persécuté (minoritaire). Loi anti-missionnaire. Orthodoxe russe privilégiée.", "defis": ["Loi anti-missionnaire", "Persécution des catholiques", "Guerre en Ukraine"]},
    "Belarus": {"idh": 0.801, "pib": 8000, "urbanisation": 80, "liberte": 35, "persecution": 55, "contexte": "Liberté religieuse très restreinte. Catholicisme minoritaire (~10%). Dictature de Loukachenko. Église catholique persécutée.", "defis": ["Dictature et persécution", "Catholicisme minoritaire", "Répression des manifestations"]},
    "Romania": {"idh": 0.827, "pib": 16000, "urbanisation": 55, "liberte": 85, "persecution": 5, "contexte": "Liberté religieuse. Catholicisme minoritaire (hongrois, grecs-catholiques). Orthodoxe majoritaire.", "defis": ["Catholicisme minoritaire", "Corruption", "Déclin des pratiquants"]},
    "Hungary": {"idh": 0.851, "pib": 22000, "urbanisation": 72, "liberte": 85, "persecution": 5, "contexte": "Liberté religieuse. Catholicisme historique mais en déclin. Nationalisme croissant sous Orban.", "defis": ["Déclin des pratiquants", "Nationalisme", "Sécularisation"]},
    "Czech Republic": {"idh": 0.895, "pib": 31000, "urbanisation": 74, "liberte": 95, "persecution": 0, "contexte": "Liberté religieuse totale. Catholicisme minoritaire. Le pays le plus athée d'Europe.", "defis": ["Athéisme majoritaire", "Catholicisme marginal", "Nouvelle évangélisation"]},
    "Slovakia": {"idh": 0.855, "pib": 23000, "urbanisation": 54, "liberte": 90, "persecution": 0, "contexte": "Liberté religieuse. Catholicisme majoritaire mais en déclin. Pays très conservateur sur les valeurs.", "defis": ["Déclin des pratiquants", "Nationalisme", "Sécularisation urbaine"]},
    "Croatia": {"idh": 0.878, "pib": 21000, "urbanisation": 58, "liberte": 92, "persecution": 0, "contexte": "Liberté religieuse. Catholicisme très majoritaire (~85%). Forte identité catholique post-guerre.", "defis": ["Déclin des pratiquants", "Émigration des jeunes", "Sécularisation"]},
    "Serbia": {"idh": 0.805, "pib": 12000, "urbanisation": 56, "liberte": 80, "persecution": 10, "contexte": "Liberté religieuse relative. Catholicisme minoritaire (hongrois, croates). Orthodoxe majoritaire.", "defis": ["Catholicisme minoritaire", "Tensions ethniques", "Déclin démographique"]},
    "Bosnia and Herzegovina": {"idh": 0.779, "pib": 8000, "urbanisation": 49, "liberte": 75, "persecution": 15, "contexte": "Liberté religieuse relative. Catholicisme minoritaire (~15%). Héritage de la guerre de 1992-1995.", "defis": ["Divisions ethniques", "Catholicisme minoritaire", "Instabilité politique"]},
    "Bulgaria": {"idh": 0.799, "pib": 15000, "urbanisation": 76, "liberte": 85, "persecution": 5, "contexte": "Liberté religieuse. Catholicisme très minoritaire (<1%). Orthodoxe majoritaire. Pays le plus pauvre de l'UE.", "defis": ["Catholicisme quasi invisible", "Corruption", "Déclin démographique"]},
    "Albania": {"idh": 0.789, "pib": 8000, "urbanisation": 63, "liberte": 85, "persecution": 5, "contexte": "Liberté religieuse. Catholicisme minoritaire (~10%). Pays majoritairement musulman laïc.", "defis": ["Catholicisme minoritaire", "Corruption", "Émigration massive"]},
    "Lithuania": {"idh": 0.879, "pib": 28000, "urbanisation": 68, "liberte": 90, "persecution": 0, "contexte": "Liberté religieuse. Catholicisme très majoritaire (~75%). Forte identité catholique résistante au communisme.", "defis": ["Déclin des pratiquants", "Sécularisation", "Déclin démographique"]},
    "Latvia": {"idh": 0.863, "pib": 24000, "urbanisation": 68, "liberte": 90, "persecution": 0, "contexte": "Liberté religieuse. Catholicisme minoritaire (~20%). Protestantisme et orthodoxie majoritaires.", "defis": ["Catholicisme minoritaire", "Déclin démographique", "Russophonie"]},
    "Estonia": {"idh": 0.899, "pib": 32000, "urbanisation": 70, "liberte": 95, "persecution": 0, "contexte": "Liberté religieuse totale. Catholicisme très minoritaire. Le pays le plus athée du monde.", "defis": ["Athéisme majoritaire", "Catholicisme marginal", "Nouvelle évangélisation"]},
    "Moldova": {"idh": 0.763, "pib": 6500, "urbanisation": 43, "liberte": 75, "persecution": 10, "contexte": "Liberté religieuse relative. Catholicisme minoritaire. Pays très pauvre. Tensions avec la Transnistrie.", "defis": ["Pauvreté extrême", "Catholicisme minoritaire", "Instabilité politique"]},
    "Georgia": {"idh": 0.802, "pib": 8000, "urbanisation": 60, "liberte": 80, "persecution": 10, "contexte": "Liberté religieuse relative. Catholicisme minoritaire (<1%). Orthodoxe majoritaire. Pays en transition.", "defis": ["Catholicisme quasi invisible", "Tensions avec la Russie", "Développement économique"]},
    "Armenia": {"idh": 0.786, "pib": 7000, "urbanisation": 63, "liberte": 70, "persecution": 15, "contexte": "Liberté religieuse relative. Catholicisme minoritaire (arméniens-catholiques). Orthodoxe arménienne majoritaire.", "defis": ["Conflit avec l'Azerbaïdjan", "Catholicisme minoritaire", "Crise économique"]},
    "Azerbaijan": {"idh": 0.760, "pib": 7000, "urbanisation": 57, "liberte": 40, "persecution": 45, "contexte": "Liberté religieuse restreinte. Catholicisme minoritaire. Régime autoritaire. Shiite majoritaire.", "defis": ["Autoritarisme", "Catholicisme minoritaire", "Conflit avec l'Arménie"]},
}

# Données par continent pour fallback
CONTINENT_DEFAULTS = {
    "Europe": {"idh": 0.85, "pib": 35000, "urbanisation": 70, "liberte": 90, "persecution": 5, "contexte": "Liberté religieuse généralement garantie. Catholicisme historique en déclin progressif face à la sécularisation.", "defis": ["Sécularisation croissante", "Déclin des vocations", "Nouvelle évangélisation"]},
    "North America": {"idh": 0.90, "pib": 55000, "urbanisation": 80, "liberte": 90, "persecution": 5, "contexte": "Liberté religieuse constitutionnelle. Catholicisme minoritaire mais diversifié. Sociétés très développées.", "defis": ["Sécularisation urbaine", "Polarisation politique", "Immigration et diversité"]},
    "South America": {"idh": 0.78, "pib": 12000, "urbanisation": 80, "liberte": 85, "persecution": 10, "contexte": "Liberté religieuse globale. Catholicisme historiquement dominant mais en déclin face aux évangéliques. Inégalités sociales importantes.", "defis": ["Perte de fidèles vers les évangéliques", "Inégalités sociales", "Pénuries de prêtres ruraux"]},
    "Africa": {"idh": 0.55, "pib": 2500, "urbanisation": 45, "liberte": 65, "persecution": 35, "contexte": "Liberté religieuse très variable selon les régions. Catholicisme très dynamique dans de nombreux pays. Pauvreté, conflits et persécution dans certaines zones.", "defis": ["Conflits armés et insécurité", "Pauvreté et sous-développement", "Persécution dans certaines régions"]},
    "Asia": {"idh": 0.70, "pib": 12000, "urbanisation": 55, "liberte": 55, "persecution": 45, "contexte": "Liberté religieuse très variable. Catholicisme minoritaire et souvent persécuté dans les pays musulmans et communistes. Très dynamique en Asie du Sud-Est.", "defis": ["Persécution dans les régimes autoritaires", "Catholicisme minoritaire", "Développement économique inégal"]},
    "Oceania": {"idh": 0.90, "pib": 45000, "urbanisation": 70, "liberte": 95, "persecution": 0, "contexte": "Liberté religieuse totale. Catholicisme minoritaire mais actif. Pays très développés avec multiculturalisme affirmé.", "defis": ["Sécularisation croissante", "Catholicisme minoritaire", "Questions environnementales"]},
    "Middle East": {"idh": 0.75, "pib": 25000, "urbanisation": 70, "liberte": 40, "persecution": 60, "contexte": "Liberté religieuse très menacée. Catholicisme minoritaire et souvent persécuté. Berceau du christianisme en déclin dramatique.", "defis": ["Persécution systémique", "Exode des chrétiens", "Conflits et instabilité"]},
    "Central America": {"idh": 0.70, "pib": 8000, "urbanisation": 65, "liberte": 85, "persecution": 15, "contexte": "Liberté religieuse générale. Catholicisme historique mais évangéliques en forte croissance. Violence des gangs et pauvreté.", "defis": ["Croissance des évangéliques", "Violence des gangs", "Pauvreté et inégalités"]},
    "Caribbean": {"idh": 0.75, "pib": 15000, "urbanisation": 60, "liberte": 90, "persecution": 5, "contexte": "Liberté religieuse générale. Catholicisme historique dominant. Pays très divers économiquement.", "defis": ["Déclin des pratiquants", "Dépendance économique", "Ouragans et catastrophes"]},
}


COUNTRY_CODE_MAP: Dict[str, str] = {
    "ae": "United Arab Emirates",
    "al": "Albania",
    "am": "Armenia",
    "ao": "Angola",
    "ar": "Argentina",
    "at": "Austria",
    "au": "Australia",
    "az": "Azerbaijan",
    "ba": "Bosnia and Herzegovina",
    "bd": "Bangladesh",
    "be": "Belgium",
    "bg": "Bulgaria",
    "bh": "Bahrain",
    "bi": "Burundi",
    "bo": "Bolivia",
    "br": "Brazil",
    "by": "Belarus",
    "ca": "Canada",
    "cd": "Democratic Republic of the Congo",
    "cf": "Central African Republic",
    "ch": "Switzerland",
    "ci": "Ivory Coast",
    "cl": "Chile",
    "cm": "Cameroon",
    "cn": "China",
    "co": "Colombia",
    "cr": "Costa Rica",
    "cu": "Cuba",
    "cz": "Czech Republic",
    "de": "Germany",
    "do": "Dominican Republic",
    "ec": "Ecuador",
    "ee": "Estonia",
    "eg": "Egypt",
    "es": "Spain",
    "et": "Ethiopia",
    "fr": "France",
    "gb": "United Kingdom",
    "ge": "Georgia",
    "gh": "Ghana",
    "gt": "Guatemala",
    "hn": "Honduras",
    "hr": "Croatia",
    "ht": "Haiti",
    "hu": "Hungary",
    "id": "Indonesia",
    "ie": "Ireland",
    "il": "Israel",
    "in": "India",
    "iq": "Iraq",
    "ir": "Iran",
    "it": "Italy",
    "jm": "Jamaica",
    "jo": "Jordan",
    "jp": "Japan",
    "ke": "Kenya",
    "kh": "Cambodia",
    "kr": "South Korea",
    "kw": "Kuwait",
    "la": "Laos",
    "lb": "Lebanon",
    "lk": "Sri Lanka",
    "lt": "Lithuania",
    "lv": "Latvia",
    "md": "Moldova",
    "mg": "Madagascar",
    "mm": "Myanmar",
    "mw": "Malawi",
    "mx": "Mexico",
    "my": "Malaysia",
    "mz": "Mozambique",
    "ng": "Nigeria",
    "ni": "Nicaragua",
    "nl": "Netherlands",
    "np": "Nepal",
    "nz": "New Zealand",
    "om": "Oman",
    "pa": "Panama",
    "pe": "Peru",
    "pg": "Papua New Guinea",
    "ph": "Philippines",
    "pk": "Pakistan",
    "pl": "Poland",
    "pr": "Puerto Rico",
    "ps": "Palestine",
    "pt": "Portugal",
    "py": "Paraguay",
    "qa": "Qatar",
    "ro": "Romania",
    "rs": "Serbia",
    "ru": "Russia",
    "rw": "Rwanda",
    "sa": "Saudi Arabia",
    "sd": "Sudan",
    "sk": "Slovakia",
    "ss": "South Sudan",
    "sv": "El Salvador",
    "sy": "Syria",
    "th": "Thailand",
    "tl": "East Timor",
    "tr": "Turkey",
    "tt": "Trinidad and Tobago",
    "tz": "Tanzania",
    "ua": "Ukraine",
    "ug": "Uganda",
    "uk": "United Kingdom",
    "us": "United States",
    "uy": "Uruguay",
    "ve": "Venezuela",
    "vn": "Vietnam",
    "ye": "Yemen",
    "za": "South Africa",
    "zm": "Zambia",
    "zw": "Zimbabwe",
}

def get_socioeco_data(pays: str, continent: str = "") -> Dict[str, Any]:
    """Récupère les données socio-économiques pour un pays. Fallback par continent si inconnu."""
    # Normaliser le pays (enlever espaces, titre)
    pays_clean = pays.strip().title() if pays else ""

    # Essayer directement
    if pays_clean in SOCIO_ECO_DATA:
        return SOCIO_ECO_DATA[pays_clean]

    # Mapping des codes pays vers les noms
    if pays.lower() in COUNTRY_CODE_MAP:
        pays_nom = COUNTRY_CODE_MAP[pays.lower()]
        if pays_nom in SOCIO_ECO_DATA:
            return SOCIO_ECO_DATA[pays_nom]

    # Mapping des noms de pays alternatifs
    aliases = {
        "USA": "United States", "U.S.A.": "United States", "America": "United States",
        "UK": "United Kingdom", "Great Britain": "United Kingdom", "England": "United Kingdom",
        "DRC": "Democratic Republic of the Congo", "Congo-Kinshasa": "Democratic Republic of the Congo",
        "Congo": "Democratic Republic of the Congo", "CAR": "Central African Republic",
        "UAE": "United Arab Emirates", "KSA": "Saudi Arabia", "South Korea": "South Korea",
        "North Korea": "North Korea", "Czechia": "Czech Republic", "Macedonia": "North Macedonia",
        "Swaziland": "Eswatini", "Burma": "Myanmar", "East Timor": "East Timor",
        "Ivory Coast": "Ivory Coast", "Cabo Verde": "Cape Verde", "Czech Republic": "Czech Republic",
        "Vatican": "Italy", "Holy See": "Italy",
    }
    if pays in aliases and aliases[pays] in SOCIO_ECO_DATA:
        return SOCIO_ECO_DATA[aliases[pays]]

    # Fallback par continent
    if continent in CONTINENT_DEFAULTS:
        data = CONTINENT_DEFAULTS[continent].copy()
        data["contexte"] = f"Données spécifiques non disponibles pour {pays}. " + data["contexte"]
        return data

    # Valeurs par défaut globales
    return {
        "idh": 0.70, "pib": 10000, "urbanisation": 50,
        "liberte": 70, "persecution": 20,
        "contexte": f"Données détaillées non disponibles pour {pays}. Liberté religieuse et contexte socio-économique à vérifier localement.",
        "defis": ["Données locales à compléter", "Contexte socio-économique à analyser"]
    }