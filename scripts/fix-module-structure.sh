#!/bin/bash
# fix-module-structure.sh - Fixes common module structure issues
set -euo pipefail

MODULE_PATH="${1:-}"
if [[ -z "$MODULE_PATH" ]]; then
    echo "Usage: $0 <module_path>"
    echo "Example: $0 modules/openai"
    exit 1
fi

MODULE_NAME=$(basename "$MODULE_PATH")
SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")
PROJECT_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)
FULL_MODULE_PATH="$PROJECT_ROOT/$MODULE_PATH"

echo "🔧 Fixing module structure: $MODULE_NAME"
echo "📁 Path: $FULL_MODULE_PATH"

# Check if module directory exists
if [[ ! -d "$FULL_MODULE_PATH" ]]; then
    echo "❌ Module directory does not exist: $FULL_MODULE_PATH"
    exit 1
fi

cd "$FULL_MODULE_PATH"

# Create missing directories
REQUIRED_DIRS=(
    "cli_functions"
    "logic"
    "routes"
)

echo
echo "📂 Creating missing directories..."
for dir in "${REQUIRED_DIRS[@]}"; do
    if [[ ! -d "$dir" ]]; then
        mkdir -p "$dir"
        echo "✅ Created $dir/"
    else
        echo "⏭️  $dir/ already exists"
    fi
done

# Create missing __init__.py files
echo
echo "📝 Creating missing __init__.py files..."
for dir in . cli_functions logic routes; do
    if [[ -d "$dir" && ! -f "$dir/__init__.py" ]]; then
        touch "$dir/__init__.py"
        echo "✅ Created $dir/__init__.py"
    else
        echo "⏭️  $dir/__init__.py already exists"
    fi
done

# Fix Dockerfile if it exists and has issues
echo
echo "🐳 Checking Dockerfile..."
if [[ -f "Dockerfile" ]]; then
    # Check if it uses the old pattern
    if grep -q "COPY . /homer/modules/$MODULE_NAME/" Dockerfile && ! grep -q "COPY.*requirements.txt /tmp/requirements.txt" Dockerfile; then
        echo "🔄 Updating Dockerfile to use better caching pattern..."
        
        # Create backup
        cp Dockerfile Dockerfile.backup
        
        # Generate new Dockerfile based on the discord/example pattern
        cat > Dockerfile << EOF
FROM mscrnt/homer:base

USER root

# Install git and ssh client if they need to clone a private repository
RUN apt-get update && apt-get install -y --no-install-recommends \\
    git \\
 && rm -rf /var/lib/apt/lists/*

# Install $MODULE_NAME python dependencies
COPY modules/$MODULE_NAME/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy module code
COPY modules/$MODULE_NAME/ /homer/modules/$MODULE_NAME/

USER homer
EOF
        echo "✅ Updated Dockerfile (backup saved as Dockerfile.backup)"
    else
        echo "⏭️  Dockerfile already uses good pattern"
    fi
else
    echo "❌ Dockerfile missing - creating from template..."
    cat > Dockerfile << EOF
FROM mscrnt/homer:base

USER root

# Install git and ssh client if they need to clone a private repository
RUN apt-get update && apt-get install -y --no-install-recommends \\
    git \\
 && rm -rf /var/lib/apt/lists/*

# Install $MODULE_NAME python dependencies
COPY modules/$MODULE_NAME/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy module code
COPY modules/$MODULE_NAME/ /homer/modules/$MODULE_NAME/

USER homer
EOF
    echo "✅ Created Dockerfile from template"
fi

# Create basic Makefile if missing
if [[ ! -f "Makefile" ]]; then
    echo "🔧 Creating Makefile..."
    cat > Makefile << EOF
# Makefile for $MODULE_NAME module

build:
	cd ../.. && docker build -f modules/$MODULE_NAME/Dockerfile -t mscrnt/homer:$MODULE_NAME .

push:
	docker push mscrnt/homer:$MODULE_NAME

.PHONY: build push
EOF
    echo "✅ Created Makefile"
else
    echo "⏭️  Makefile already exists"
fi

# Check requirements.txt and provide guidance
echo
echo "📦 Checking requirements.txt..."
if [[ -f "requirements.txt" ]]; then
    if [[ ! -s "requirements.txt" ]] || grep -q "^#.*Example:" requirements.txt; then
        echo "⚠️  requirements.txt appears to be empty or contains only examples"
        echo "   Please add actual Python dependencies for this module"
    else
        echo "✅ requirements.txt has content"
    fi
else
    echo "❌ Creating empty requirements.txt..."
    cat > requirements.txt << EOF
# Add Python dependencies for $MODULE_NAME module here
# Example:
# requests>=2.25.0
# python-dotenv>=0.19.0
EOF
    echo "✅ Created requirements.txt template"
fi

echo
echo "🎉 Module structure fixes completed for $MODULE_NAME"
echo "   Next steps:"
echo "   1. Add actual dependencies to requirements.txt"
echo "   2. Implement proper @register_cli decorator in cli.py"
echo "   3. Implement proper @register_api decorator in api.py"
echo "   4. Run validation: ./scripts/validate-module.sh $MODULE_PATH"