# 🔧🤖 Perforce-OpenAI Stack

This stack combines Perforce version control with OpenAI's AI capabilities to create intelligent code analysis, automated summaries, and smart development workflows.

---

## 🧱 Included Modules

* **Perforce** - Version control and changelist management
* **OpenAI** - AI-powered text analysis, summarization, and tagging

---

## 🚀 Use Cases

### Intelligent Code Review
```bash
# Get changelist and analyze with AI
./homer perforce changelist 12345 --output /tmp/changelist.json
DESCRIPTION=$(cat /tmp/changelist.json | jq -r '.description')
./homer openai summarize --text "$DESCRIPTION" --max-length 100
./homer openai sentiment --text "$DESCRIPTION"
```

### Automated Changelist Analysis
```bash
# Analyze recent changes with AI insights
./homer perforce changes --max 10 --output /tmp/recent.json
cat /tmp/recent.json | jq -r '.[].description' | while read desc; do
  echo "Analyzing: $desc"
  ./homer openai tags --text "$desc" --num-tags 3
done
```

### Smart Release Notes
```bash
# Generate AI-powered release notes
CHANGES=$(./homer perforce changes --max 50 --output /tmp/changes.json)
DESCRIPTIONS=$(cat /tmp/changes.json | jq -r '.[].description' | paste -sd '\n')
./homer openai summarize --text "$DESCRIPTIONS" --max-length 500
```

---

## 🏗️ Building and Validation

```bash
# Validate stack structure
make validate-stack STACK=perforce-openai

# Build the stack
make build-stack STACK=perforce-openai

# Or use manual commands
cd stacks/perforce-openai
make build
```

## 🐳 Running the Stack

```bash
# Run with environment variables
docker run --rm \
  -e P4PORT=ssl:perforce.company.com:1666 \
  -e P4USER=your-username \
  -e P4CLIENT=your-workspace \
  -e OPENAI_API_KEY=your-openai-key \
  mscrnt/homer:perforce-openai <command>

# Example: Check stack status
docker run --rm \
  -e P4PORT=ssl:perforce.company.com:1666 \
  -e P4USER=your-username \
  -e OPENAI_API_KEY=your-openai-key \
  mscrnt/homer:perforce-openai status

# Example: Analyze latest changelist
docker run --rm \
  -e P4PORT=ssl:perforce.company.com:1666 \
  -e P4USER=your-username \
  -e OPENAI_API_KEY=your-openai-key \
  mscrnt/homer:perforce-openai perforce changelist 12345
```

---

## 🔧 Environment Variables

You need to configure environment variables for both modules:

### Perforce Configuration
- `P4PORT` - Perforce server address
- `P4USER` - Your Perforce username  
- `P4CLIENT` - Your workspace name (optional)
- `P4PASSWD` - Your Perforce password (optional)

### OpenAI Configuration
- `OPENAI_API_KEY` - Your OpenAI API key
- `OPENAI_MODEL` - GPT model to use (default: gpt-3.5-turbo)
- `OPENAI_MAX_TOKENS` - Max response length (default: 1000)

---

## 📊 API Endpoints

When running as an API service, this stack exposes:

```http
# Perforce endpoints
GET  /perforce/ping
GET  /perforce/changelist/{id}
GET  /perforce/changelists
GET  /perforce/streams
POST /perforce/sync

# OpenAI endpoints
GET  /openai/ping
POST /openai/summarize
POST /openai/embed
POST /openai/tags
POST /openai/sentiment
POST /openai/batch
```

---

## 🔄 Advanced Automation

Create intelligent workflows that combine both platforms:

```bash
#!/bin/bash
# Intelligent Perforce Analysis Pipeline

# Configuration
CHANGELIST_ID=$1
OUTPUT_DIR="/tmp/analysis"
mkdir -p "$OUTPUT_DIR"

echo "🔍 Analyzing changelist $CHANGELIST_ID..."

# 1. Get changelist details
./homer perforce changelist "$CHANGELIST_ID" --output "$OUTPUT_DIR/changelist.json"

# 2. Extract description
DESCRIPTION=$(cat "$OUTPUT_DIR/changelist.json" | jq -r '.description')
echo "📝 Description: $DESCRIPTION"

# 3. AI Analysis
echo "🤖 Running AI analysis..."

# Generate summary
SUMMARY=$(./homer openai summarize --text "$DESCRIPTION" --max-length 100)
echo "📋 Summary: $SUMMARY"

# Analyze sentiment
SENTIMENT=$(./homer openai sentiment --text "$DESCRIPTION")
echo "😊 Sentiment: $SENTIMENT"

# Generate tags
TAGS=$(./homer openai tags --text "$DESCRIPTION" --num-tags 5)
echo "🏷️  Tags: $TAGS"

# 4. Save analysis report
cat > "$OUTPUT_DIR/analysis_report.md" << EOF
# Changelist $CHANGELIST_ID Analysis Report

## Summary
$SUMMARY

## Sentiment Analysis
$SENTIMENT

## Generated Tags
$TAGS

## Full Description
$DESCRIPTION
EOF

echo "✅ Analysis complete! Report saved to $OUTPUT_DIR/analysis_report.md"
```

---

## 🎯 Advanced Use Cases

### Code Quality Insights
- Analyze changelist descriptions for sentiment trends
- Generate summaries of development activities
- Tag changes by feature, bugfix, or refactoring
- Create embeddings for semantic search of changes

### Development Intelligence
- Identify patterns in code changes over time
- Generate automated release notes with AI summaries
- Analyze developer communication in changelist descriptions
- Create intelligent dashboards with AI-powered insights

### Process Automation
- Auto-categorize changes based on content analysis
- Generate smart notifications with context summaries
- Create intelligent code review assignments
- Build AI-powered development metrics

---

© Mscrnt, LLC – 2025