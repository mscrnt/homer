#!/bin/bash
# validate-all.sh - Validates all modules and stacks before building
set -euo pipefail

SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")
PROJECT_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)

echo "🚀 HOMER Project Validation"
echo "=========================="
echo

# Make validation scripts executable
chmod +x "$SCRIPT_DIR/validate-module.sh"
chmod +x "$SCRIPT_DIR/validate-stack.sh"

# Track results
FAILED_MODULES=()
FAILED_STACKS=()
TOTAL_MODULES=0
TOTAL_STACKS=0

# Validate all modules
echo "🧩 VALIDATING MODULES"
echo "===================="
if [[ -d "$PROJECT_ROOT/modules" ]]; then
    for module_dir in "$PROJECT_ROOT/modules"/*; do
        if [[ -d "$module_dir" ]]; then
            module_name=$(basename "$module_dir")
            TOTAL_MODULES=$((TOTAL_MODULES + 1))
            
            echo
            echo "--- Module: $module_name ---"
            if "$SCRIPT_DIR/validate-module.sh" "modules/$module_name"; then
                echo "✅ $module_name: PASSED"
            else
                echo "❌ $module_name: FAILED"
                FAILED_MODULES+=("$module_name")
            fi
        fi
    done
else
    echo "⚠️  No modules directory found"
fi

echo
echo "🧱 VALIDATING STACKS"
echo "==================="
if [[ -d "$PROJECT_ROOT/stacks" ]]; then
    for stack_dir in "$PROJECT_ROOT/stacks"/*; do
        if [[ -d "$stack_dir" ]]; then
            stack_name=$(basename "$stack_dir")
            # Skip homer-latest as it's auto-generated
            if [[ "$stack_name" == "homer-latest" ]]; then
                echo "⏭️  Skipping auto-generated stack: $stack_name"
                continue
            fi
            
            TOTAL_STACKS=$((TOTAL_STACKS + 1))
            
            echo
            echo "--- Stack: $stack_name ---"
            if "$SCRIPT_DIR/validate-stack.sh" "stacks/$stack_name"; then
                echo "✅ $stack_name: PASSED"
            else
                echo "❌ $stack_name: FAILED"
                FAILED_STACKS+=("$stack_name")
            fi
        fi
    done
else
    echo "⚠️  No stacks directory found"
fi

# Summary report
echo
echo "📊 VALIDATION SUMMARY"
echo "===================="
echo "Modules: $((TOTAL_MODULES - ${#FAILED_MODULES[@]}))/$TOTAL_MODULES passed"
echo "Stacks:  $((TOTAL_STACKS - ${#FAILED_STACKS[@]}))/$TOTAL_STACKS passed"

if [[ ${#FAILED_MODULES[@]} -gt 0 ]]; then
    echo
    echo "❌ FAILED MODULES:"
    for module in "${FAILED_MODULES[@]}"; do
        echo "   - $module"
    done
fi

if [[ ${#FAILED_STACKS[@]} -gt 0 ]]; then
    echo
    echo "❌ FAILED STACKS:"
    for stack in "${FAILED_STACKS[@]}"; do
        echo "   - $stack"
    done
fi

# Exit with error if any validations failed
if [[ ${#FAILED_MODULES[@]} -gt 0 || ${#FAILED_STACKS[@]} -gt 0 ]]; then
    echo
    echo "🚨 VALIDATION FAILED - Fix issues before building"
    exit 1
else
    echo
    echo "🎉 ALL VALIDATIONS PASSED - Ready to build!"
    exit 0
fi