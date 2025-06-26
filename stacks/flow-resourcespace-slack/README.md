# Flow-ResourceSpace-Slack Stack

A focused integration stack that enables seamless asset sharing between Flow production management, ResourceSpace digital asset management, and Slack team communication.

## Overview

This stack provides robust workflows for:
- **Flow → ResourceSpace**: Push assets from Flow to ResourceSpace with proper metadata
- **ResourceSpace → Slack**: Share ResourceSpace assets in Slack channels with rich context
- **Complete Workflow**: Streamlined Flow → ResourceSpace → Slack automation
- **Project Synchronization**: Bulk sync entire Flow projects
- **Search & Discovery**: Search ResourceSpace and share results in Slack

## Features

### 🔄 Asset Workflows
- **Push Assets**: Transfer Flow assets to ResourceSpace with metadata preservation
- **Share Assets**: Share ResourceSpace assets in Slack with rich formatting
- **Complete Pipeline**: End-to-end Flow → ResourceSpace → Slack automation
- **Bulk Operations**: Process multiple assets efficiently

### 📊 Project Management
- **Project Sync**: Synchronize entire Flow projects to ResourceSpace
- **Status Reporting**: Real-time project status updates in Slack
- **Asset Tracking**: Track asset movement across systems

### 🔍 Search & Discovery
- **Cross-platform Search**: Find assets across Flow and ResourceSpace
- **Smart Sharing**: Share search results directly in Slack channels
- **Context Preservation**: Maintain asset context and metadata

### 🏷️ Metadata Management
- **Automatic Tagging**: Intelligent metadata extraction from Flow
- **Custom Metadata**: Override and enhance asset metadata
- **Bidirectional Linking**: Link assets across all three platforms

## Quick Start

### Prerequisites
- Flow/ShotGrid API access
- ResourceSpace instance with API enabled
- Slack workspace with bot permissions

### Basic Usage

#### 1. Check System Status
```bash
homer flow-resourcespace-slack status
```

#### 2. Push Flow Asset to ResourceSpace
```bash
# Basic push
homer flow-resourcespace-slack push flow-to-resourcespace 12345

# With custom metadata
homer flow-resourcespace-slack push flow-to-resourcespace 12345 \
    --title "Hero Shot Final" \
    --description "Final approved hero shot" \
    --tags "final,approved,hero"
```

#### 3. Share ResourceSpace Asset in Slack
```bash
# Basic share
homer flow-resourcespace-slack share resourcespace-to-slack RS_12345_20231201 "#assets"

# With custom message
homer flow-resourcespace-slack share resourcespace-to-slack RS_12345_20231201 "#team" \
    --message "New asset ready for review!"
```

#### 4. Complete Workflow (Flow → ResourceSpace → Slack)
```bash
# Standard workflow
homer flow-resourcespace-slack workflow complete 12345 "#assets"

# With customization
homer flow-resourcespace-slack workflow complete 12345 "#team" \
    --title "Final Cut" \
    --tags "approved,final" \
    --include-metadata
```

#### 5. Sync Entire Project
```bash
homer flow-resourcespace-slack workflow sync-project 789 "#project-updates"
```

#### 6. Search and Share
```bash
homer flow-resourcespace-slack search and-share "hero shot" "#assets" --max-results 5
```

## Advanced Usage

### Bulk Operations
Process multiple assets at once:
```bash
# Push multiple Flow assets
homer flow-resourcespace-slack bulk push-multiple 001 002 003 004 "#assets"

# With delay between operations
homer flow-resourcespace-slack bulk push-multiple 001 002 003 "#assets" --delay 2.0
```

### API Usage

#### Health Check
```bash
curl http://localhost:8000/flow-resourcespace-slack/health
```

#### Push Asset via API
```bash
curl -X POST http://localhost:8000/flow-resourcespace-slack/push/flow-to-resourcespace \
  -H "Content-Type: application/json" \
  -d '{
    "flow_asset_id": 12345,
    "metadata_overrides": {
      "title": "Hero Shot Final",
      "tags": "final,approved"
    }
  }'
```

#### Complete Workflow via API
```bash
curl -X POST http://localhost:8000/flow-resourcespace-slack/workflow/complete \
  -H "Content-Type: application/json" \
  -d '{
    "flow_asset_id": 12345,
    "channel": "#assets",
    "include_metadata": true
  }'
```

## Configuration

### Environment Variables
```bash
# Flow/ShotGrid Configuration
FLOW_SERVER_URL=https://your-studio.shotgunstudio.com
FLOW_API_KEY=your_flow_api_key
FLOW_SCRIPT_NAME=your_script_name

# ResourceSpace Configuration
RESOURCESPACE_BASE_URL=https://your-resourcespace.com
RESOURCESPACE_API_KEY=your_rs_api_key
RESOURCESPACE_USER=your_rs_user

# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
SLACK_SIGNING_SECRET=your_slack_signing_secret

# Stack Configuration
FLOW_RESOURCESPACE_SLACK_DEFAULT_CHANNEL=#assets
FLOW_RESOURCESPACE_SLACK_AUTO_TAG=true
FLOW_RESOURCESPACE_SLACK_SYNC_UPDATES=true
```

### Stack Configuration
```python
from stacks.flow_resourcespace_slack.config import get_stack_config

config = get_stack_config()
# Returns:
# {
#   "stack_name": "flow-resourcespace-slack",
#   "default_channel": "#assets",
#   "auto_tag_assets": True,
#   "sync_project_updates": True
# }
```

## Workflows

### 1. Asset Publishing Workflow
```
Flow Asset → ResourceSpace (with metadata) → Slack Notification
```
1. Asset is marked as "Final" in Flow
2. Automatically pushed to ResourceSpace with Flow metadata
3. Team notified in Slack with asset preview and context

### 2. Review & Approval Workflow
```
ResourceSpace Search → Slack Share → Team Review → Flow Update
```
1. Search ResourceSpace for assets needing review
2. Share candidates in Slack review channel
3. Team reviews and approves in Slack
4. Status updated back in Flow

### 3. Project Delivery Workflow
```
Flow Project → Bulk ResourceSpace Upload → Slack Summary
```
1. Project marked as "Delivered" in Flow
2. All final assets bulk uploaded to ResourceSpace
3. Delivery summary shared in client Slack channel

## Metadata Mapping

### Flow → ResourceSpace
| Flow Field | ResourceSpace Field | Notes |
|------------|-------------------|-------|
| `code` | `title` | Asset name/code |
| `description` | `description` | Asset description |
| `sg_asset_type` | `keywords` | Added as tag |
| `project.name` | `project_name` | Custom field |
| `sg_status_list` | `status` | Custom field |
| `created_by` | `created_by` | Custom field |

### ResourceSpace → Slack
- **Rich Cards**: Asset previews with metadata
- **Action Buttons**: Direct links to view/download
- **Context**: Project and status information
- **Threading**: Group related assets in threads

## Error Handling

The stack includes robust error handling:
- **Partial Success**: ResourceSpace upload succeeds but Slack notification fails
- **Retry Logic**: Automatic retries for transient failures
- **Graceful Degradation**: Continue operation even if one service is down
- **Detailed Logging**: Comprehensive logs for troubleshooting

## Monitoring

### Health Checks
```bash
# Check all services
homer flow-resourcespace-slack status

# API health check
curl http://localhost:8000/flow-resourcespace-slack/health
```

### Logging
```bash
# View stack logs
docker logs homer-flow-resourcespace-slack

# Enable debug logging
export HOMER_LOG_LEVEL=DEBUG
```

## Troubleshooting

### Common Issues

#### 1. Flow Connection Failed
```bash
# Check Flow credentials
echo $FLOW_API_KEY
echo $FLOW_SERVER_URL

# Test Flow connection
homer flow-resourcespace-slack flow auth test
```

#### 2. ResourceSpace Upload Failed
```bash
# Check ResourceSpace API
curl https://your-resourcespace.com/api/

# Verify permissions
homer flow-resourcespace-slack resourcespace user info
```

#### 3. Slack Notifications Not Sent
```bash
# Check Slack token
echo $SLACK_BOT_TOKEN

# Test Slack connection
homer flow-resourcespace-slack slack auth test
```

#### 4. Metadata Not Preserved
```bash
# Check metadata mapping
homer flow-resourcespace-slack push flow-to-resourcespace 12345 --output result.json
cat result.json | jq '.metadata_applied'
```

### Debug Mode
```bash
# Enable verbose output
export HOMER_LOG_LEVEL=DEBUG
homer flow-resourcespace-slack workflow complete 12345 "#test"
```

## Examples

See comprehensive examples:
```bash
homer flow-resourcespace-slack examples
```

## API Reference

### Endpoints
- `GET /health` - Service health check
- `GET /status` - Stack status and capabilities
- `POST /push/flow-to-resourcespace` - Push Flow asset to ResourceSpace
- `POST /share/resourcespace-to-slack` - Share ResourceSpace asset in Slack
- `POST /workflow/complete` - Complete Flow → ResourceSpace → Slack workflow
- `POST /workflow/sync-project` - Sync Flow project to ResourceSpace
- `POST /search/and-share` - Search ResourceSpace and share in Slack

### Response Format
```json
{
  "status": "success|error|partial_success",
  "message": "Human readable message",
  "data": { ... },
  "error": "Error details (if applicable)"
}
```

## Contributing

This stack is part of the HOMER automation framework. For contributions:
1. Follow HOMER coding standards
2. Include comprehensive tests
3. Update documentation
4. Ensure backward compatibility

## License

Part of HOMER automation framework.