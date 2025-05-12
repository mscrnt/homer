#!/bin/bash
set -euo pipefail

# Configurable version (default to "latest" if not provided)
VERSION=${1:-latest}

echo "🔨 Building and pushing homer-base:$VERSION"
make -f homer/Makefile build_and_push VERSION=$VERSION

# --- Modules ---
for module in github atlassian resourcespace; do
    echo "🔧 Building and pushing homer-$module:$VERSION"
    make -f modules/$module/Makefile build_and_push VERSION=$VERSION
done

# --- Stacks ---
echo "🧱 Building and pushing homer-github-atlassian:$VERSION"
make -f stacks/homer-github-atlassian/Makefile build_and_push VERSION=$VERSION

echo "✅ All images built and pushed with tag: $VERSION"
