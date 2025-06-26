#!/bin/bash
set -euo pipefail

# Optional override for base tag (defaults to 'base')
BASE_TAG=${1:-base}
LATEST_DOCKERFILE="stacks/homer-latest/Dockerfile"
LATEST_STACK_DIR="stacks/homer-latest"

# Get script directory
SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")
PROJECT_ROOT=$(cd "$SCRIPT_DIR" && pwd)

echo "🚀 HOMER Build and Push Pipeline"
echo "================================"

# Run pre-build validation
echo "🔍 Running pre-build validation..."
if [[ -f "$PROJECT_ROOT/scripts/pre-build-check.sh" ]]; then
    chmod +x "$PROJECT_ROOT/scripts/pre-build-check.sh"
    if ! "$PROJECT_ROOT/scripts/pre-build-check.sh"; then
        echo "❌ Validation failed. Attempting automatic fixes..."
        if ! "$PROJECT_ROOT/scripts/pre-build-check.sh" --fix; then
            echo "🚨 Could not fix all issues automatically. Please fix manually and try again."
            exit 1
        fi
        echo "✅ Issues fixed. Continuing with build..."
    fi
else
    echo "⚠️  Pre-build validation script not found. Continuing without validation..."
fi

echo

echo "🔨 Building and pushing homer:$BASE_TAG"
make -f homer/Makefile build_and_push VERSION=$BASE_TAG

# --- Modules ---
MODULES=()
for dir in modules/*/; do
    module=$(basename "$dir")
    MODULES+=("$module")
    echo "🔧 Building and pushing homer:$module"
    make -f "modules/$module/Makefile" build_and_push VERSION=$module
done

# --- Combined homer:latest from all modules ---
echo "🧱 Creating combined homer:latest from modules: ${MODULES[*]}"
mkdir -p "$LATEST_STACK_DIR"

# Collect unique pip requirements from all module requirements.txt files
REQUIREMENTS=$(for module in "${MODULES[@]}"; do
    grep -h '^[^#[:space:]]' "modules/$module/requirements.txt" 2>/dev/null || true
done | sort -u | xargs)

# Write Dockerfile for homer:latest
{
    echo "FROM mscrnt/homer:$BASE_TAG"
    for module in "${MODULES[@]}"; do
        echo "COPY modules/$module/ /homer/modules/$module/"
    done
    if [[ -n "$REQUIREMENTS" ]]; then
        echo "USER root"
        echo "RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*"
        echo "USER homer"
        echo "RUN pip install $REQUIREMENTS"
    fi
} > "$LATEST_DOCKERFILE"

# Build and push homer:latest
docker build -t mscrnt/homer:latest -f "$LATEST_DOCKERFILE" .
docker push mscrnt/homer:latest

# --- All Stacks ---
echo "📦 Building all other stacks..."
for dir in stacks/*/; do
    stack=$(basename "$dir")
    [[ "$stack" == "homer-latest" ]] && continue  # skip dynamically generated latest
    echo "🧱 Building and pushing homer:$stack"
    make -f "stacks/$stack/Makefile" build_and_push VERSION=$stack
done

echo "✅ All images built and pushed."
