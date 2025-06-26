# HOMER Validation Scripts

This directory contains automation scripts to validate and fix HOMER modules and stacks before building, preventing build failures like missing `requirements.txt` files.

## Scripts Overview

### 🔍 `validate-module.sh`
Validates individual module structure and dependencies.

```bash
./scripts/validate-module.sh modules/openai
```

**Checks:**
- Required files: `__init__.py`, `api.py`, `cli.py`, `client.py`, etc.
- Required directories: `cli_functions/`, `logic/`, `routes/`
- `requirements.txt` content validation
- Dockerfile best practices
- Python decorator usage (`@register_cli`, `@register_api`)
- `__init__.py` files in subdirectories

### 🧱 `validate-stack.sh`
Validates stack configuration and module dependencies.

```bash
./scripts/validate-stack.sh stacks/github-atlassian
```

**Checks:**
- Required stack files
- Dockerfile base image usage
- Module dependency validation
- Referenced modules exist and are valid

### 🔧 `fix-module-structure.sh`
Automatically fixes common module structure issues.

```bash
./scripts/fix-module-structure.sh modules/openai
```

**Fixes:**
- Creates missing directories and `__init__.py` files
- Updates Dockerfile to use better caching patterns
- Creates basic `Makefile` if missing
- Provides guidance for remaining manual fixes

### 🚀 `pre-build-check.sh`
Comprehensive validation with optional auto-fixes.

```bash
# Basic validation
./scripts/pre-build-check.sh

# With auto-fixes
./scripts/pre-build-check.sh --fix

# Validate specific module/stack
./scripts/pre-build-check.sh --module openai
./scripts/pre-build-check.sh --stack github-atlassian
```

### ✅ `validate-all.sh`
Validates all modules and stacks (legacy, use `pre-build-check.sh` instead).

## Integration

### Makefile Integration
Use the project Makefile for common tasks:

```bash
# Validate everything
make validate

# Validate with fixes
make validate-fix

# Validate specific module
make validate-module MODULE=openai

# Build with validation
make build
```

### GitHub Actions
The `.github/workflows/validate-and-build.yml` workflow automatically:
1. Validates all modules and stacks
2. Attempts auto-fixes if validation fails
3. Builds base image, modules, and stacks in parallel
4. Only pushes on main branch (not PRs)

### Build Script Integration
The main `build_and_push_all.sh` script now includes pre-build validation:
- Runs validation before building
- Attempts auto-fixes if validation fails
- Stops build if issues can't be resolved

## Common Issues and Fixes

### Missing `requirements.txt`
**Error:** `ERROR: Could not open requirements file: [Errno 2] No such file or directory`

**Fix:** The validation scripts check for and create missing `requirements.txt` files.

### Docker Layer Caching Issues
**Problem:** Inefficient Dockerfile patterns like `COPY . /homer/modules/module/`

**Fix:** Auto-converts to better pattern:
```dockerfile
COPY modules/module/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY modules/module/ /homer/modules/module/
```

### Missing Decorators
**Problem:** Modules missing `@register_cli` or `@register_api` decorators

**Detection:** Scripts validate Python files for required decorators
**Fix:** Manual fix required - add decorators to `cli.py` and `api.py`

### Missing Directory Structure
**Problem:** Modules missing required directories (`cli_functions/`, `logic/`, `routes/`)

**Fix:** Auto-creates missing directories and `__init__.py` files

## Usage Examples

### Before Building
```bash
# Quick validation
make validate

# Fix issues automatically
make validate-fix

# Build everything
make build
```

### Development Workflow
```bash
# Setup new module
cp -r examples/modules modules/my-module

# Fix structure
./scripts/fix-module-structure.sh modules/my-module

# Validate
make validate-module MODULE=my-module

# Build when ready
make build-module MODULE=my-module
```

### CI/CD Integration
The scripts return proper exit codes:
- `0` = validation passed
- `1` = validation failed

Perfect for CI/CD pipelines and pre-commit hooks.

## Error Output Examples

### Successful Validation
```
🔍 Validating module: openai
✅ All required files and directories present
```

### Failed Validation
```
❌ Validation failed
Missing files: client.py
Missing directories: cli_functions logic routes
```

### Auto-Fix Success
```
🔧 Attempting to fix issues...
✅ Created cli_functions/__init__.py
✅ Updated Dockerfile (backup saved as Dockerfile.backup)
✅ openai: FIXED and PASSED
```

This validation system prevents build failures and ensures consistent module/stack structure across the HOMER project.