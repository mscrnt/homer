# 🔄 HOMER Cross-Module Workflows

This directory contains automation workflows that combine multiple HOMER modules to create intelligent, end-to-end processes.

## Available Workflows

### 🔧🤖💬 Perforce → OpenAI → Slack Pipeline

**File:** `perforce-ai-slack.sh`

Intelligent changelist analysis and team notification workflow:

1. **📋 Perforce** - Retrieves changelist details
2. **🤖 OpenAI** - Analyzes description with AI (summary, sentiment, tags)  
3. **💬 Slack** - Sends rich notification with insights

**Usage:**
```bash
# Analyze latest changelist and send to #dev-updates
./workflows/perforce-ai-slack.sh

# Analyze specific changelist
./workflows/perforce-ai-slack.sh 12345

# Send to specific channel
./workflows/perforce-ai-slack.sh 12345 "#code-review"
```

**Requirements:**
- `P4PORT` - Perforce server address
- `P4USER` - Perforce username
- `OPENAI_API_KEY` - OpenAI API key  
- `SLACK_BOT_TOKEN` - Slack bot token

## Running Workflows

### With Docker (homer:latest)
```bash
docker run --rm \
  -e P4PORT=ssl:perforce.company.com:1666 \
  -e P4USER=username \
  -e OPENAI_API_KEY=sk-your-key \
  -e SLACK_BOT_TOKEN=xoxb-your-token \
  mscrnt/homer:latest ./workflows/perforce-ai-slack.sh
```

### With Stack Images
```bash
# Use perforce-openai stack + separate Slack call
docker run --rm \
  -e P4PORT=ssl:perforce.company.com:1666 \
  -e P4USER=username \
  -e OPENAI_API_KEY=sk-your-key \
  mscrnt/homer:perforce-openai perforce changelist 12345

# Or use custom orchestration with docker-compose
```

## Creating New Workflows

Follow this pattern for new cross-module workflows:

1. **Environment Check** - Validate required environment variables
2. **Error Handling** - Use proper cleanup and error reporting
3. **Logging** - Provide clear progress indicators
4. **Documentation** - Include usage examples and requirements

Example workflow structure:
```bash
#!/bin/bash
set -e

# Configuration
PARAM1=${1:-"default"}
TEMP_DIR="/tmp/homer-workflow-$$"

# Functions
check_env() { ... }
cleanup() { ... }
main() { ... }

# Execution
trap cleanup EXIT
main "$@"
```

## Workflow Ideas

Consider creating workflows for:

- **Creative Pipeline**: SyncSketch upload → AI analysis → Slack notification
- **GitHub Integration**: PR analysis → AI summary → team notification  
- **Infrastructure Monitoring**: NetBox inventory → AI insights → alerting
- **Documentation**: Code changes → AI documentation → Confluence update

---

© Mscrnt, LLC – 2025