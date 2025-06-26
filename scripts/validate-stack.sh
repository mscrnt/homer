#!/bin/bash
# validate-stack.sh - Validates stack structure and dependencies before building
set -euo pipefail

STACK_PATH="${1:-}"
if [[ -z "$STACK_PATH" ]]; then
    echo "Usage: $0 <stack_path>"
    echo "Example: $0 stacks/github-atlassian"
    exit 1
fi

STACK_NAME=$(basename "$STACK_PATH")
SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")
PROJECT_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)
FULL_STACK_PATH="$PROJECT_ROOT/$STACK_PATH"

echo "🔍 Validating stack: $STACK_NAME"
echo "📁 Path: $FULL_STACK_PATH"

# Check if stack directory exists
if [[ ! -d "$FULL_STACK_PATH" ]]; then
    echo "❌ Stack directory does not exist: $FULL_STACK_PATH"
    exit 1
fi

cd "$FULL_STACK_PATH"

# Required files check for stacks
REQUIRED_FILES=(
    "__init__.py"
    "cli.py"
    "config.py"
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

# Validate Dockerfile for stacks
echo
echo "🐳 Validating Dockerfile..."
if [[ -f "Dockerfile" ]]; then
    # Check for proper base image
    if grep -q "FROM mscrnt/homer:base" Dockerfile; then
        echo "✅ Uses correct base image"
    else
        echo "❌ Does not use 'mscrnt/homer:base' as base image"
    fi
    
    # Extract module dependencies from Dockerfile
    REFERENCED_MODULES=()
    while IFS= read -r line; do
        if [[ "$line" =~ COPY.*modules/([^/]+)/ ]]; then
            module_name="${BASH_REMATCH[1]}"
            REFERENCED_MODULES+=("$module_name")
        fi
    done < Dockerfile
    
    if [[ ${#REFERENCED_MODULES[@]} -gt 0 ]]; then
        echo "📦 Referenced modules: ${REFERENCED_MODULES[*]}"
        
        # Check if referenced modules exist
        echo "🔍 Checking module dependencies..."
        for module in "${REFERENCED_MODULES[@]}"; do
            if [[ -d "$PROJECT_ROOT/modules/$module" ]]; then
                echo "✅ modules/$module exists"
                
                # Validate the referenced module
                if [[ -f "$PROJECT_ROOT/scripts/validate-module.sh" ]]; then
                    echo "   🔄 Running validation for $module..."
                    if "$PROJECT_ROOT/scripts/validate-module.sh" "modules/$module" > /dev/null 2>&1; then
                        echo "   ✅ $module validation passed"
                    else
                        echo "   ❌ $module validation failed"
                        MISSING_FILES+=("valid-modules/$module")
                    fi
                fi
            else
                echo "❌ modules/$module does not exist"
                MISSING_FILES+=("modules/$module")
            fi
        done
    else
        echo "⚠️  No module dependencies found in Dockerfile"
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

# Check cli.py for stack-specific patterns
echo
echo "🐍 Validating Python files..."
if [[ -f "cli.py" ]]; then
    if grep -q "import.*modules" cli.py || grep -q "from.*modules" cli.py; then
        echo "✅ cli.py imports modules"
    else
        echo "⚠️  cli.py may not be importing required modules"
    fi
else
    echo "❌ cli.py missing"
fi

# Check Makefile for proper targets
echo
echo "🔧 Validating Makefile..."
if [[ -f "Makefile" ]]; then
    if grep -q "build:" Makefile; then
        echo "✅ Has build target"
    else
        echo "❌ Missing build target in Makefile"
    fi
    
    if grep -q "push:" Makefile; then
        echo "✅ Has push target"
    else
        echo "⚠️  Missing push target in Makefile"
    fi
else
    echo "❌ Makefile missing"
fi

# Summary
echo
echo "📊 Validation Summary for $STACK_NAME:"
if [[ ${#MISSING_FILES[@]} -eq 0 ]]; then
    echo "✅ Stack validation passed"
    exit 0
else
    echo "❌ Stack validation failed"
    echo "Issues: ${MISSING_FILES[*]}"
    exit 1
fi