# HOMER Project Makefile
# ======================

.PHONY: validate validate-fix build clean help

# Default target
all: validate build

# Validation targets
validate:
	@echo "🔍 Running validation..."
	./scripts/pre-build-check.sh

validate-fix:
	@echo "🔧 Running validation with auto-fix..."
	./scripts/pre-build-check.sh --fix

validate-module:
	@if [ -z "$(MODULE)" ]; then \
		echo "❌ Usage: make validate-module MODULE=<module_name>"; \
		exit 1; \
	fi
	./scripts/validate-module.sh modules/$(MODULE)

validate-stack:
	@if [ -z "$(STACK)" ]; then \
		echo "❌ Usage: make validate-stack STACK=<stack_name>"; \
		exit 1; \
	fi
	./scripts/validate-stack.sh stacks/$(STACK)

# Build targets
build: validate
	@echo "🚀 Building all images..."
	./build_and_push_all.sh

build-force:
	@echo "🚀 Building all images (skipping validation)..."
	./build_and_push_all.sh

# Individual module/stack builds
build-module:
	@if [ -z "$(MODULE)" ]; then \
		echo "❌ Usage: make build-module MODULE=<module_name>"; \
		exit 1; \
	fi
	@echo "🔧 Building module: $(MODULE)"
	cd modules/$(MODULE) && make build

build-stack:
	@if [ -z "$(STACK)" ]; then \
		echo "❌ Usage: make build-stack STACK=<stack_name>"; \
		exit 1; \
	fi
	@echo "🧱 Building stack: $(STACK)"
	cd stacks/$(STACK) && make build

# Cleanup
clean:
	@echo "🧹 Cleaning up..."
	docker system prune -f
	docker image prune -f

# Development helpers
dev-setup:
	@echo "🛠️  Setting up development environment..."
	chmod +x scripts/*.sh
	chmod +x build_and_push_all.sh

fix-all:
	@echo "🔧 Fixing all module structures..."
	@for module in modules/*/; do \
		if [ -d "$$module" ]; then \
			module_name=$$(basename "$$module"); \
			echo "Fixing $$module_name..."; \
			./scripts/fix-module-structure.sh "modules/$$module_name" || true; \
		fi \
	done

# Help
help:
	@echo "HOMER Project Build System"
	@echo "========================="
	@echo ""
	@echo "Main targets:"
	@echo "  validate       - Run full validation"
	@echo "  validate-fix   - Run validation with auto-fixes"
	@echo "  build         - Validate and build all images"
	@echo "  build-force   - Build without validation"
	@echo ""
	@echo "Individual targets:"
	@echo "  validate-module MODULE=<name>  - Validate specific module"
	@echo "  validate-stack STACK=<name>    - Validate specific stack"
	@echo "  build-module MODULE=<name>     - Build specific module"
	@echo "  build-stack STACK=<name>       - Build specific stack"
	@echo ""
	@echo "Development:"
	@echo "  dev-setup     - Setup development environment"
	@echo "  fix-all       - Fix all module structures"
	@echo "  clean         - Clean up Docker resources"
	@echo ""
	@echo "Examples:"
	@echo "  make validate-module MODULE=openai"
	@echo "  make build-module MODULE=discord"
	@echo "  make validate-stack STACK=github-atlassian"