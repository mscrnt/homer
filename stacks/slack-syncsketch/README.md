# 🎨💬 Slack-SyncSketch Stack

This stack combines the Slack and SyncSketch modules to create a powerful creative workflow automation system. Perfect for creative teams that need to coordinate reviews, uploads, and notifications.

---

## 🧱 Included Modules

* **Slack** - Team communication and notifications
* **SyncSketch** - Creative review and collaboration platform

---

## 🚀 Use Cases

### Creative Review Workflow
```bash
# Upload media to SyncSketch and notify team
./homer syncsketch upload video.mp4 --project-id 12345 --name "Scene 01 Draft"
./homer slack send --channel "#creative-review" --message "🎬 New upload: Scene 01 Draft ready for review!"
```

### Project Status Updates
```bash
# Create review and announce it
./homer syncsketch create-review --project-id 12345 --name "Weekly Review" --description "Assets for client approval"
./homer slack send --channel "#updates" --message "📋 Weekly Review created - please check SyncSketch for new assets"
```

### Automated Notifications
Set up webhooks or cron jobs to automatically notify teams of new uploads, completed reviews, or project milestones.

---

## 🏗️ Building and Validation

```bash
# Validate stack structure
make validate-stack STACK=slack-syncsketch

# Build the stack
make build-stack STACK=slack-syncsketch

# Or use manual commands
cd stacks/slack-syncsketch
make build
```

## 🐳 Running the Stack

```bash
# Run with environment variables
docker run --rm \
  -e SLACK_BOT_TOKEN=xoxb-your-token \
  -e SYNCSKETCH_API_KEY=your-key \
  -e SYNCSKETCH_WORKSPACE=your-workspace \
  mscrnt/homer:slack-syncsketch <command>

# Example: Check stack status
docker run --rm \
  -e SLACK_BOT_TOKEN=xoxb-your-token \
  -e SYNCSKETCH_API_KEY=your-key \
  -e SYNCSKETCH_WORKSPACE=your-workspace \
  mscrnt/homer:slack-syncsketch status

# Example: List SyncSketch projects and send summary to Slack
docker run --rm \
  -e SLACK_BOT_TOKEN=xoxb-your-token \
  -e SYNCSKETCH_API_KEY=your-key \
  -e SYNCSKETCH_WORKSPACE=your-workspace \
  mscrnt/homer:slack-syncsketch syncsketch projects
```

---

## 🔧 Environment Variables

You need to configure environment variables for both modules:

### Slack Configuration
- `SLACK_BOT_TOKEN` - Your Slack bot token
- `SLACK_DEFAULT_CHANNEL` - Default channel for notifications

### SyncSketch Configuration
- `SYNCSKETCH_API_KEY` - Your SyncSketch API key
- `SYNCSKETCH_WORKSPACE` - Your workspace identifier

---

## 📊 API Endpoints

When running as an API service, this stack exposes:

```http
# Slack endpoints
GET  /slack/ping
POST /slack/send
GET  /slack/channels

# SyncSketch endpoints  
GET  /syncsketch/ping
GET  /syncsketch/projects
POST /syncsketch/reviews
POST /syncsketch/upload
```

---

## 🔄 Automation Examples

Create scripts that combine both platforms:

```bash
#!/bin/bash
# Automated creative workflow

# Upload new assets
UPLOAD_RESULT=$(./homer syncsketch upload "$1" --project-id "$PROJECT_ID")
MEDIA_ID=$(echo "$UPLOAD_RESULT" | grep "ID:" | cut -d: -f2 | xargs)

# Notify creative team
./homer slack send \
  --channel "#creative" \
  --message "🎨 New asset uploaded! Media ID: $MEDIA_ID - Ready for review"

# Create review if needed
if [ "$CREATE_REVIEW" = "true" ]; then
  ./homer syncsketch create-review \
    --project-id "$PROJECT_ID" \
    --name "Review $(date +%Y-%m-%d)" \
    --description "Daily creative review"
fi
```

---

© Mscrnt, LLC – 2025