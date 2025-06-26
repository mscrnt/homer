#!/bin/bash
# pre-build-check.sh - Comprehensive pre-build validation and fixes
set -euo pipefail

SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")
PROJECT_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 HOMER Pre-Build Validation${NC}"
echo "================================="

# Make all scripts executable
chmod +x "$SCRIPT_DIR"/*.sh

# Command line arguments
FIX_ISSUES=false
SPECIFIC_MODULE=""
SPECIFIC_STACK=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --fix)
            FIX_ISSUES=true
            shift
            ;;
        --module)
            SPECIFIC_MODULE="$2"
            shift 2
            ;;
        --stack)
            SPECIFIC_STACK="$2"
            shift 2
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo "Options:"
            echo "  --fix           Automatically fix common issues"
            echo "  --module NAME   Validate only specific module"
            echo "  --stack NAME    Validate only specific stack"
            echo "  --help          Show this help message"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Function to run validation and optionally fix issues
validate_and_fix() {
    local type="$1"
    local name="$2"
    local path="$3"
    
    echo
    echo -e "${BLUE}--- $type: $name ---${NC}"
    
    if [[ "$type" == "Module" ]]; then
        if "$SCRIPT_DIR/validate-module.sh" "$path" 2>/dev/null; then
            echo -e "${GREEN}✅ $name: PASSED${NC}"
            return 0
        else
            echo -e "${RED}❌ $name: FAILED${NC}"
            if [[ "$FIX_ISSUES" == true ]]; then
                echo -e "${YELLOW}🔧 Attempting to fix issues...${NC}"
                "$SCRIPT_DIR/fix-module-structure.sh" "$path"
                
                # Re-validate after fix
                if "$SCRIPT_DIR/validate-module.sh" "$path" 2>/dev/null; then
                    echo -e "${GREEN}✅ $name: FIXED and PASSED${NC}"
                    return 0
                else
                    echo -e "${RED}❌ $name: Still has issues after fix${NC}"
                    return 1
                fi
            else
                echo -e "${YELLOW}💡 Run with --fix to automatically fix common issues${NC}"
                return 1
            fi
        fi
    else
        # Stack validation
        if "$SCRIPT_DIR/validate-stack.sh" "$path" 2>/dev/null; then
            echo -e "${GREEN}✅ $name: PASSED${NC}"
            return 0
        else
            echo -e "${RED}❌ $name: FAILED${NC}"
            return 1
        fi
    fi
}

# Track results
FAILED_ITEMS=()
TOTAL_ITEMS=0

# Validate specific module if requested
if [[ -n "$SPECIFIC_MODULE" ]]; then
    echo -e "${BLUE}🧩 VALIDATING MODULE: $SPECIFIC_MODULE${NC}"
    TOTAL_ITEMS=1
    if ! validate_and_fix "Module" "$SPECIFIC_MODULE" "modules/$SPECIFIC_MODULE"; then
        FAILED_ITEMS+=("Module:$SPECIFIC_MODULE")
    fi
fi

# Validate specific stack if requested
if [[ -n "$SPECIFIC_STACK" ]]; then
    echo -e "${BLUE}🧱 VALIDATING STACK: $SPECIFIC_STACK${NC}"
    TOTAL_ITEMS=1
    if ! validate_and_fix "Stack" "$SPECIFIC_STACK" "stacks/$SPECIFIC_STACK"; then
        FAILED_ITEMS+=("Stack:$SPECIFIC_STACK")
    fi
fi

# If no specific module/stack requested, validate all
if [[ -z "$SPECIFIC_MODULE" && -z "$SPECIFIC_STACK" ]]; then
    echo -e "${BLUE}🧩 VALIDATING ALL MODULES${NC}"
    echo "======================="
    
    if [[ -d "$PROJECT_ROOT/modules" ]]; then
        for module_dir in "$PROJECT_ROOT/modules"/*; do
            if [[ -d "$module_dir" ]]; then
                module_name=$(basename "$module_dir")
                TOTAL_ITEMS=$((TOTAL_ITEMS + 1))
                
                if ! validate_and_fix "Module" "$module_name" "modules/$module_name"; then
                    FAILED_ITEMS+=("Module:$module_name")
                fi
            fi
        done
    fi

    echo
    echo -e "${BLUE}🧱 VALIDATING ALL STACKS${NC}"
    echo "======================"
    
    if [[ -d "$PROJECT_ROOT/stacks" ]]; then
        for stack_dir in "$PROJECT_ROOT/stacks"/*; do
            if [[ -d "$stack_dir" ]]; then
                stack_name=$(basename "$stack_dir")
                # Skip homer-latest as it's auto-generated
                if [[ "$stack_name" == "homer-latest" ]]; then
                    echo -e "${YELLOW}⏭️  Skipping auto-generated stack: $stack_name${NC}"
                    continue
                fi
                
                TOTAL_ITEMS=$((TOTAL_ITEMS + 1))
                
                if ! validate_and_fix "Stack" "$stack_name" "stacks/$stack_name"; then
                    FAILED_ITEMS+=("Stack:$stack_name")
                fi
            fi
        done
    fi
fi

# Final summary
echo
echo -e "${BLUE}📊 FINAL SUMMARY${NC}"
echo "================"
echo "Total validated: $TOTAL_ITEMS"
echo "Passed: $((TOTAL_ITEMS - ${#FAILED_ITEMS[@]}))"
echo "Failed: ${#FAILED_ITEMS[@]}"

if [[ ${#FAILED_ITEMS[@]} -gt 0 ]]; then
    echo
    echo -e "${RED}❌ FAILED ITEMS:${NC}"
    for item in "${FAILED_ITEMS[@]}"; do
        echo "   - $item"
    done
    echo
    if [[ "$FIX_ISSUES" == false ]]; then
        echo -e "${YELLOW}💡 Run with --fix to automatically fix common issues${NC}"
    fi
    echo -e "${RED}🚨 VALIDATION FAILED - Fix issues before building${NC}"
    exit 1
else
    echo
    echo -e "${GREEN}🎉 ALL VALIDATIONS PASSED - Ready to build!${NC}"
    
    # Show next steps
    echo
    echo -e "${BLUE}📋 NEXT STEPS:${NC}"
    echo "1. Run builds:"
    echo "   ./build_and_push_all.sh"
    echo "2. Or build specific module:"
    echo "   cd modules/<module> && make build"
    echo "3. Or build specific stack:"
    echo "   cd stacks/<stack> && make build"
    
    exit 0
fi