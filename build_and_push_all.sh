#!/bin/bash
set -euo pipefail

# Optional version override for base only
BASE_TAG=${1:-base}

echo "🔨 Building and pushing homer:base (tag: $BASE_TAG)"
make -f homer/Makefile build_and_push VERSION=$BASE_TAG

# --- Modules ---
for module in github atlassian resourcespace; do
    echo "🔧 Building and pushing homer:$module"
    make -f modules/$module/Makefile build_and_push VERSION=$module
done

# --- Stacks ---
echo "🧱 Building and pushing homer:github-atlassian"
make -f stacks/homer-github-atlassian/Makefile build_and_push VERSION=github-atlassian

echo "✅ All images built and pushed under mscrnt/homer with appropriate tags."
