#!/usr/bin/env bash
set -e

# ═══════════════════════════════════════════════════════════════════
# Carta Pastorale — Script de déploiement automatique sur Render
# ═══════════════════════════════════════════════════════════════════

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration (modifiable)
RENDER_SERVICE_NAME="carta-pastorale"
DATA_RAW_DIR="data/raw"
FRONTEND_DIR="frontend"
BACKEND_DIR="backend"
DATA_DIR="data"

# ─── Fonctions utilitaires ─────────────────────────────────────────

log_info() {
    echo -e "${BLUE}ℹ${NC}  $1"
}

log_success() {
    echo -e "${GREEN}✅${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}⚠️${NC}  $1"
}

log_error() {
    echo -e "${RED}❌${NC} $1"
}

# ─── Vérification des prérequis ────────────────────────────────────

check_prerequisites() {
    log_info "Vérification des prérequis..."

    command -v git >/dev/null 2>&1 || { log_error "git est requis mais n'est pas installé."; exit 1; }
    command -v node >/dev/null 2>&1 || { log_error "node est requis mais n'est pas installé."; exit 1; }
    command -v npm >/dev/null 2>&1 || { log_error "npm est requis mais n'est pas installé."; exit 1; }
    command -v python3 >/dev/null 2>&1 || { log_error "python3 est requis mais n'est pas installé."; exit 1; }

    log_success "Tous les prérequis sont satisfaits"
}

# ─── Étape 1 : Pipeline de données ─────────────────────────────────

run_pipeline() {
    log_info "Étape 1/5 : Pipeline de données"

    if [ ! -d "$DATA_RAW_DIR" ]; then
        log_warn "Dossier $DATA_RAW_DIR introuvable — saut de l'étape pipeline"
        return 0
    fi

    local json_count=$(find "$DATA_RAW_DIR" -name "*.json" | wc -l)

    if [ "$json_count" -eq 0 ]; then
        log_warn "Aucun fichier JSON dans $DATA_RAW_DIR — saut de l'étape pipeline"
        return 0
    fi

    log_info "$json_count fichiers JSON trouvés dans $DATA_RAW_DIR"

    cd "$BACKEND_DIR"

    # Créer le venv s'il n'existe pas
    if [ ! -d "venv" ]; then
        log_info "Création de l'environnement virtuel Python..."
        python3 -m venv venv
    fi

    source venv/bin/activate

    # Installer les dépendances
    log_info "Installation des dépendances Python..."
    pip install -q -r requirements.txt

    # Lancer le pipeline
    log_info "Exécution du pipeline..."
    python run_all.py --raw "../$DATA_RAW_DIR"

    deactivate
    cd ..

    log_success "Pipeline terminé — données régénérées"
}

# ─── Étape 2 : Build du frontend ───────────────────────────────────

build_frontend() {
    log_info "Étape 2/5 : Build du frontend Next.js"

    cd "$FRONTEND_DIR"

    # Installer les dépendances si node_modules manquant
    if [ ! -d "node_modules" ]; then
        log_info "Installation des dépendances npm..."
        npm ci
    fi

    # Build statique
    log_info "Build Next.js (output: export)..."
    npm run build

    cd ..

    if [ ! -d "$FRONTEND_DIR/dist" ]; then
        log_error "Le build a échoué — dossier dist/ introuvable"
        exit 1
    fi

    log_success "Frontend buildé dans $FRONTEND_DIR/dist/"
}

# ─── Étape 3 : Git commit ──────────────────────────────────────────

git_commit() {
    log_info "Étape 3/5 : Commit des changements"

    # Vérifier si on est dans un repo git
    if [ ! -d ".git" ]; then
        log_error "Pas de repo git détecté. Initialisez avec : git init"
        exit 1
    fi

    # Ajouter les fichiers générés
    git add "$DATA_DIR/" "$FRONTEND_DIR/dist/" "$BACKEND_DIR/" 2>/dev/null || true

    # Vérifier s'il y a des changements
    if git diff --cached --quiet; then
        log_warn "Aucun changement à committer"
        return 0
    fi

    # Commit avec timestamp
    local timestamp=$(date +"%Y-%m-%d %H:%M")
    git commit -m "🚀 Déploiement Carta Pastorale — $timestamp

- Données mises à jour
- Frontend rebuildé
- Prêt pour Render"

    log_success "Changements commités"
}

# ─── Étape 4 : Push sur GitHub ─────────────────────────────────────

git_push() {
    log_info "Étape 4/5 : Push sur le remote"

    local current_branch=$(git rev-parse --abbrev-ref HEAD)

    log_info "Push sur la branche $current_branch..."
    git push origin "$current_branch"

    log_success "Push effectué — Render va auto-déployer"
}

# ─── Étape 5 : Vérification du déploiement ─────────────────────────

verify_deploy() {
    log_info "Étape 5/5 : Vérification du déploiement"

    log_info "Attente du déploiement Render (auto-deploy depuis GitHub)..."
    log_info "Vous pouvez suivre le déploiement sur :"
    log_info "  https://dashboard.render.com"

    # Optionnel : ping Render pour forcer le réveil
    if [ -n "$RENDER_URL" ]; then
        log_info "Ping de l'API pour vérification..."
        sleep 5
        curl -s "$RENDER_URL" > /dev/null && log_success "API répond !" || log_warn "API en cours de démarrage..."
    fi
}

# ─── Menu interactif ───────────────────────────────────────────────

show_menu() {
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  🗺️  Carta Pastorale — Déploiement automatique${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "  1) Déploiement complet (pipeline + build + push)"
    echo "  2) Build frontend uniquement"
    echo "  3) Pipeline données uniquement"
    echo "  4) Push git uniquement"
    echo "  5) Vérifier l'état du déploiement"
    echo "  q) Quitter"
    echo ""
}

# ─── Déploiement complet ───────────────────────────────────────────

full_deploy() {
    echo ""
    log_info "🚀 Démarrage du déploiement complet..."
    echo ""

    check_prerequisites
    run_pipeline
    build_frontend
    git_commit
    git_push
    verify_deploy

    echo ""
    log_success "Déploiement terminé !"
    echo ""
    echo -e "${BLUE}URLs :${NC}"
    echo "  Frontend : https://$RENDER_SERVICE_NAME.onrender.com"
    echo "  API      : https://$RENDER_SERVICE_NAME.onrender.com/dioceses"
    echo ""
}

# ─── Main ──────────────────────────────────────────────────────────

main() {
    # Si appelé avec un argument
    case "${1:-}" in
        --full|-f)
            full_deploy
            exit 0
            ;;
        --pipeline|-p)
            check_prerequisites
            run_pipeline
            exit 0
            ;;
        --build|-b)
            check_prerequisites
            build_frontend
            exit 0
            ;;
        --push)
            check_prerequisites
            git_commit
            git_push
            exit 0
            ;;
        --help|-h|*)
            show_menu
            read -p "Choix : " choice

            case "$choice" in
                1) full_deploy ;;
                2) check_prerequisites; build_frontend ;;
                3) check_prerequisites; run_pipeline ;;
                4) check_prerequisites; git_commit; git_push ;;
                5) verify_deploy ;;
                q|Q) exit 0 ;;
                *) log_error "Choix invalide"; exit 1 ;;
            esac
            ;;
    esac
}

main "$@"