#!/bin/bash
# Cross-module workflow: Perforce → OpenAI → Slack
# Analyzes Perforce changelists with AI and sends summaries to Slack

set -e

# Configuration
CHANGELIST_ID=${1:-"latest"}
SLACK_CHANNEL=${2:-"#dev-updates"}
TEMP_DIR="/tmp/homer-workflow-$$"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}" >&2
}

success() {
    echo -e "${GREEN}[SUCCESS] $1${NC}"
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

# Check required environment variables
check_env() {
    local missing=()
    
    [ -z "$P4PORT" ] && missing+=("P4PORT")
    [ -z "$P4USER" ] && missing+=("P4USER")
    [ -z "$OPENAI_API_KEY" ] && missing+=("OPENAI_API_KEY")
    [ -z "$SLACK_BOT_TOKEN" ] && missing+=("SLACK_BOT_TOKEN")
    
    if [ ${#missing[@]} -ne 0 ]; then
        error "Missing required environment variables: ${missing[*]}"
        echo "Required:"
        echo "  P4PORT - Perforce server address"
        echo "  P4USER - Perforce username"
        echo "  OPENAI_API_KEY - OpenAI API key"
        echo "  SLACK_BOT_TOKEN - Slack bot token"
        exit 1
    fi
}

# Cleanup function
cleanup() {
    if [ -d "$TEMP_DIR" ]; then
        rm -rf "$TEMP_DIR"
    fi
}

# Set up cleanup trap
trap cleanup EXIT

# Main workflow
main() {
    log "🚀 Starting Perforce → OpenAI → Slack workflow"
    
    # Check environment
    check_env
    
    # Create temp directory
    mkdir -p "$TEMP_DIR"
    
    # Step 1: Get changelist from Perforce
    log "📋 Getting changelist from Perforce..."
    
    if [ "$CHANGELIST_ID" = "latest" ]; then
        # Get the latest changelist
        CHANGELIST_ID=$(./homer perforce changes --max 1 | head -1 | cut -d' ' -f2)
        log "🔍 Found latest changelist: $CHANGELIST_ID"
    fi
    
    if ! ./homer perforce changelist "$CHANGELIST_ID" --output "$TEMP_DIR/changelist.json"; then
        error "Failed to get changelist $CHANGELIST_ID from Perforce"
        exit 1
    fi
    
    success "✅ Retrieved changelist $CHANGELIST_ID"
    
    # Extract changelist data
    DESCRIPTION=$(cat "$TEMP_DIR/changelist.json" | jq -r '.description' 2>/dev/null || echo "No description")
    USER=$(cat "$TEMP_DIR/changelist.json" | jq -r '.user' 2>/dev/null || echo "Unknown")
    DATE=$(cat "$TEMP_DIR/changelist.json" | jq -r '.date' 2>/dev/null || echo "Unknown date")
    FILE_COUNT=$(cat "$TEMP_DIR/changelist.json" | jq -r '.files | length' 2>/dev/null || echo "0")
    
    log "👤 User: $USER"
    log "📅 Date: $DATE"
    log "📁 Files: $FILE_COUNT"
    log "📝 Description: ${DESCRIPTION:0:100}..."
    
    # Step 2: Analyze with OpenAI
    log "🤖 Analyzing changelist with OpenAI..."
    
    # Generate summary
    if ! SUMMARY=$(./homer openai summarize --text "$DESCRIPTION" --max-length 150); then
        warning "Failed to generate summary, using description"
        SUMMARY="$DESCRIPTION"
    else
        success "✅ Generated summary"
    fi
    
    # Analyze sentiment
    if SENTIMENT_OUTPUT=$(./homer openai sentiment --text "$DESCRIPTION" 2>/dev/null); then
        SENTIMENT=$(echo "$SENTIMENT_OUTPUT" | grep "Sentiment:" | cut -d: -f2 | xargs)
        success "✅ Analyzed sentiment: $SENTIMENT"
    else
        warning "Failed to analyze sentiment"
        SENTIMENT="neutral"
    fi
    
    # Generate tags
    if TAGS_OUTPUT=$(./homer openai tags --text "$DESCRIPTION" --num-tags 3 2>/dev/null); then
        TAGS=$(echo "$TAGS_OUTPUT" | tail -n +2 | sed 's/^[[:space:]]*[0-9]*\.[[:space:]]*//' | paste -sd ',' -)
        success "✅ Generated tags: $TAGS"
    else
        warning "Failed to generate tags"
        TAGS="development"
    fi
    
    # Step 3: Send to Slack
    log "💬 Sending notification to Slack..."
    
    # Determine emoji based on sentiment
    case "$SENTIMENT" in
        *positive*) SENTIMENT_EMOJI="😊" ;;
        *negative*) SENTIMENT_EMOJI="😞" ;;
        *neutral*) SENTIMENT_EMOJI="😐" ;;
        *) SENTIMENT_EMOJI="📊" ;;
    esac
    
    # Create rich message
    MESSAGE="🔧 *Changelist $CHANGELIST_ID* by $USER
📅 $DATE | 📁 $FILE_COUNT files | $SENTIMENT_EMOJI $SENTIMENT

📋 *Summary:*
$SUMMARY

🏷️ *Tags:* $TAGS

🔗 P4 Changelist: $CHANGELIST_ID"
    
    if ./homer slack send --channel "$SLACK_CHANNEL" --message "$MESSAGE"; then
        success "✅ Sent notification to $SLACK_CHANNEL"
    else
        error "Failed to send Slack notification"
        exit 1
    fi
    
    # Step 4: Save workflow report
    REPORT_FILE="$TEMP_DIR/workflow_report.json"
    cat > "$REPORT_FILE" << EOF
{
  "workflow": "perforce-ai-slack",
  "timestamp": "$(date -Iseconds)",
  "changelist": {
    "id": "$CHANGELIST_ID",
    "user": "$USER",
    "date": "$DATE",
    "file_count": $FILE_COUNT,
    "description": "$DESCRIPTION"
  },
  "ai_analysis": {
    "summary": "$SUMMARY",
    "sentiment": "$SENTIMENT",
    "tags": "$TAGS"
  },
  "notification": {
    "channel": "$SLACK_CHANNEL",
    "status": "sent"
  }
}
EOF
    
    log "📊 Workflow report saved to: $REPORT_FILE"
    success "🎉 Workflow completed successfully!"
    
    echo ""
    echo "Summary:"
    echo "  📋 Changelist: $CHANGELIST_ID"
    echo "  🤖 AI Summary: ${SUMMARY:0:80}..."
    echo "  😊 Sentiment: $SENTIMENT"
    echo "  💬 Notified: $SLACK_CHANNEL"
}

# Help function
show_help() {
    cat << EOF
Perforce → OpenAI → Slack Workflow

USAGE:
    $0 [CHANGELIST_ID] [SLACK_CHANNEL]

ARGUMENTS:
    CHANGELIST_ID    Perforce changelist ID (default: latest)
    SLACK_CHANNEL    Slack channel to notify (default: #dev-updates)

ENVIRONMENT VARIABLES:
    P4PORT           Perforce server address
    P4USER           Perforce username  
    P4CLIENT         Perforce workspace (optional)
    OPENAI_API_KEY   OpenAI API key
    SLACK_BOT_TOKEN  Slack bot token

EXAMPLES:
    # Analyze latest changelist
    $0
    
    # Analyze specific changelist
    $0 12345
    
    # Send to specific channel
    $0 12345 "#code-review"

EOF
}

# Parse command line arguments
case "${1:-}" in
    -h|--help)
        show_help
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac