# 🤖 HOMER OpenAI Module

The `openai` module provides OpenAI integration for HOMER, enabling text summarization, embeddings generation, content tagging, and sentiment analysis through both CLI and API interfaces.

---

## 📦 Module Contents

```text
openai/
├── api.py             # FastAPI routes for OpenAI operations
├── cli.py             # CLI commands for OpenAI integration
├── client.py          # OpenAI SDK wrapper and utilities
├── config.py          # Environment configuration schema
├── requirements.txt   # Python dependencies
├── Dockerfile         # Build script for containerization
├── Makefile           # Build and deployment targets
└── README.md          # This file
```

---

## 🧠 Module Capabilities

This module provides:

* ✅ Text summarization with customizable length
* ✅ Embedding generation for vector operations
* ✅ Automatic tag generation for content
* ✅ Sentiment analysis with confidence scores
* ✅ Batch processing for multiple operations
* ✅ CLI commands for all AI operations
* ✅ FastAPI routes for programmatic access

---

## 💻 CLI Usage

```bash
# Summarize text
./homer openai summarize --text "Long text to summarize..."
./homer openai summarize --file document.txt --max-length 200

# Generate embeddings
./homer openai embed --text "Text to embed" --output embeddings.json

# Generate tags
./homer openai tags --text "Content to tag" --num-tags 10

# Analyze sentiment
./homer openai sentiment --text "I love this product!"

# Check module configuration
./homer openai ping
```

Or with Docker:

```bash
docker run --rm -e OPENAI_API_KEY=your_key \
  mscrnt/homer:openai openai summarize --text "Text to summarize"
```

---

## 🌐 API Routes

The `openai` module exposes the following API routes:

```http
GET  /openai/ping              # Health check
POST /openai/summarize         # Generate text summary
POST /openai/embed             # Generate embeddings
POST /openai/tags              # Generate content tags
POST /openai/sentiment         # Analyze sentiment
POST /openai/batch             # Batch processing
```

Example API usage:

```bash
# Summarize text
curl -X POST http://localhost:4242/openai/summarize \
  -H "Content-Type: application/json" \
  -d '{"text": "Long text to summarize...", "max_length": 100}'

# Generate embeddings
curl -X POST http://localhost:4242/openai/embed \
  -H "Content-Type: application/json" \
  -d '{"text": "Text to embed"}'

# Batch processing
curl -X POST http://localhost:4242/openai/batch \
  -H "Content-Type: application/json" \
  -d '{"text": "Sample text", "operations": ["summarize", "tags", "sentiment"]}'
```

---

## 🔧 Environment Variables

This module requires the following environment variables:

| Variable                 | Description                    | Default           |
| ------------------------ | ------------------------------ | ----------------- |
| `OPENAI_API_KEY`         | OpenAI API key                 | Required          |
| `OPENAI_MODEL`           | GPT model to use               | `gpt-3.5-turbo`   |
| `OPENAI_EMBEDDING_MODEL` | Embedding model to use         | `text-embedding-ada-002` |
| `OPENAI_MAX_TOKENS`      | Maximum tokens for responses   | `1000`            |
| `OPENAI_TEMPERATURE`     | Response randomness (0-1)      | `0.7`             |

---

## 🔑 OpenAI API Setup

To use this module, you need an OpenAI API key:

1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Set the `OPENAI_API_KEY` environment variable
4. Ensure you have sufficient API credits

---

## 🚀 Integration Examples

### Cross-Module Workflow
Combine with Slack for AI-powered notifications:

```bash
# Generate summary and send to Slack
TEXT=$(cat changelog.txt)
SUMMARY=$(./homer openai summarize --text "$TEXT")
./homer slack send --channel "#updates" --message "📋 Changelog Summary: $SUMMARY"
```

### Perforce Integration
Analyze code changes with AI:

```bash
# Get changelist description and analyze
CHANGELIST=$(./homer perforce describe 12345)
./homer openai sentiment --text "$CHANGELIST"
./homer openai tags --text "$CHANGELIST"
```

---

## 🧪 Development and Testing

```bash
# Validate module structure
make validate-module MODULE=openai

# Test locally
python -m homer.modules.openai.cli ping

# Build and test
make build-module MODULE=openai
```

## 🐳 Docker Build

```bash
# Validate before building (recommended)
make validate-module MODULE=openai

# Build the module image
make build-module MODULE=openai

# Or manually
cd modules/openai
make build

# Push to registry
make push
```

---

## 🧱 Stack Integration

To include this module in a stack, add to your stack Dockerfile:

```dockerfile
COPY modules/openai/ /homer/modules/openai/
RUN pip install -r /homer/modules/openai/requirements.txt
```

---

## 🎯 Use Cases

* **Code Review**: Summarize pull request changes
* **Documentation**: Generate tags for content organization  
* **Support**: Analyze customer feedback sentiment
* **Content**: Create embeddings for semantic search
* **Automation**: AI-powered content classification

---

© Mscrnt, LLC – 2025