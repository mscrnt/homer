#!/bin/bash
# validate-module.sh - Validates module structure and dependencies before building
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

echo "🔍 Validating module: $MODULE_NAME"
echo "📁 Path: $FULL_MODULE_PATH"

# Check if module directory exists
if [[ ! -d "$FULL_MODULE_PATH" ]]; then
    echo "❌ Module directory does not exist: $FULL_MODULE_PATH"
    exit 1
fi

cd "$FULL_MODULE_PATH"

# Required files check
REQUIRED_FILES=(
    "__init__.py"
    "api.py"
    "cli.py"
    "client.py"
    "config.py"
    "requirements.txt"
    "Dockerfile"
    "Makefile"
)

echo
echo "📋 Checking required files..."
MISSING_FILES=()
for file in "${REQUIRED_FILES[@]}"; do
    if [[ -f "$file" ]]; then
        echo "✅ $file"
    else
        echo "❌ $file (missing)"
        MISSING_FILES+=("$file")
    fi
done

# Required directories check
REQUIRED_DIRS=(
    "cli_functions"
    "logic"
    "routes"
)

echo
echo "📂 Checking required directories..."
MISSING_DIRS=()
for dir in "${REQUIRED_DIRS[@]}"; do
    if [[ -d "$dir" ]]; then
        echo "✅ $dir/"
    else
        echo "❌ $dir/ (missing)"
        MISSING_DIRS+=("$dir")
    fi
done

# Validate requirements.txt
echo
echo "📦 Validating requirements.txt..."
if [[ -f "requirements.txt" ]]; then
    if [[ -s "requirements.txt" ]]; then
        echo "✅ requirements.txt has content"
        # Check for common issues
        if grep -q "^#.*Example:" requirements.txt; then
            echo "⚠️  requirements.txt contains example comments - may need real dependencies"
        fi
        echo "📄 Contents:"
        cat requirements.txt | sed 's/^/   /'
    else
        echo "⚠️  requirements.txt is empty"
    fi
else
    echo "❌ requirements.txt missing"
fi

# Validate Dockerfile
echo
echo "🐳 Validating Dockerfile..."
if [[ -f "Dockerfile" ]]; then
    # Check for proper base image
    if grep -q "FROM mscrnt/homer:base" Dockerfile; then
        echo "✅ Uses correct base image"
    else
        echo "❌ Does not use 'mscrnt/homer:base' as base image"
    fi
    
    # Check for proper requirements.txt handling
    if grep -q "COPY.*requirements.txt /tmp/requirements.txt" Dockerfile; then
        echo "✅ Properly copies requirements.txt to /tmp first"
    elif grep -q "COPY . " Dockerfile && grep -q "pip install.*requirements.txt" Dockerfile; then
        echo "⚠️  Uses COPY . pattern - consider copying requirements.txt first for better caching"
    else
        echo "❌ No proper requirements.txt installation found"
    fi
    
    # Check for USER switching
    if grep -q "USER homer" Dockerfile; then
        echo "✅ Switches to homer user"
    else
        echo "⚠️  Consider adding 'USER homer' for security"
    fi
else
    echo "❌ Dockerfile missing"
fi

# Validate Python files for basic structure
echo
echo "🐍 Validating Python files..."

# Check cli.py for @register_cli decorator
if [[ -f "cli.py" ]]; then
    if grep -q "@register_cli" cli.py; then
        echo "✅ cli.py has @register_cli decorator"
    else
        echo "❌ cli.py missing @register_cli decorator"
    fi
else
    echo "❌ cli.py missing"
fi

# Check api.py for @register_api decorator
if [[ -f "api.py" ]]; then
    if grep -q "@register_api" api.py; then
        echo "✅ api.py has @register_api decorator"
    else
        echo "❌ api.py missing @register_api decorator"
    fi
else
    echo "❌ api.py missing"
fi

# Check for __init__.py files in subdirectories
echo
echo "📝 Checking __init__.py files in subdirectories..."
for dir in cli_functions logic routes; do
    if [[ -d "$dir" ]]; then
        if [[ -f "$dir/__init__.py" ]]; then
            echo "✅ $dir/__init__.py"
        else
            echo "❌ $dir/__init__.py (missing)"
            MISSING_FILES+=("$dir/__init__.py")
        fi
    fi
done

# Summary
echo
echo "📊 Validation Summary for $MODULE_NAME:"
if [[ ${#MISSING_FILES[@]} -eq 0 && ${#MISSING_DIRS[@]} -eq 0 ]]; then
    echo "✅ All required files and directories present"
    exit 0
else
    echo "❌ Validation failed"
    if [[ ${#MISSING_FILES[@]} -gt 0 ]]; then
        echo "Missing files: ${MISSING_FILES[*]}"
    fi
    if [[ ${#MISSING_DIRS[@]} -gt 0 ]]; then
        echo "Missing directories: ${MISSING_DIRS[*]}"
    fi
    exit 1
fi