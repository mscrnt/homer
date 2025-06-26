from fastapi import HTTPException
from pydantic import BaseModel
from homer.api.core import HomerAPI, register_api
from homer.utils.logger import get_module_logger
from modules.openai.client import get_openai_client
from typing import List, Dict, Any
import os

log = get_module_logger("openai-api")

class SummarizeRequest(BaseModel):
    text: str
    max_length: int = None

class EmbeddingRequest(BaseModel):
    text: str

class TagsRequest(BaseModel):
    text: str
    num_tags: int = 5

class SentimentRequest(BaseModel):
    text: str

class SummarizeResponse(BaseModel):
    summary: str
    original_length: int
    summary_length: int

class EmbeddingResponse(BaseModel):
    embedding: List[float]
    dimensions: int

class TagsResponse(BaseModel):
    tags: List[str]
    count: int

class SentimentResponse(BaseModel):
    sentiment: str
    confidence: float

@register_api
class OpenAIAPI(HomerAPI):
    def __init__(self):
        super().__init__(prefix="/openai")

    def register_routes(self):
        # 🩺 Health check route
        @self.router.get("/ping")
        async def ping():
            """Simple health check for OpenAI service."""
            try:
                has_key = bool(os.getenv("OPENAI_API_KEY"))
                return {
                    "status": "ok", 
                    "module": "openai",
                    "api_key_configured": has_key,
                    "model": os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
                }
            except Exception as e:
                log.exception("❌ OpenAI ping failed")
                return {"status": "error", "message": str(e)}

        # 📝 Summarize text route
        @self.router.post("/summarize", response_model=SummarizeResponse)
        async def summarize_text(request: SummarizeRequest):
            """Generate a summary of the provided text."""
            try:
                client = get_openai_client()
                summary = await client.generate_summary(request.text, request.max_length)
                
                return SummarizeResponse(
                    summary=summary,
                    original_length=len(request.text),
                    summary_length=len(summary)
                )
            except Exception as e:
                log.exception("❌ Failed to summarize text")
                raise HTTPException(status_code=500, detail=str(e))

        # 🧮 Generate embeddings route
        @self.router.post("/embed", response_model=EmbeddingResponse)
        async def generate_embedding(request: EmbeddingRequest):
            """Generate embeddings for the provided text."""
            try:
                client = get_openai_client()
                embedding = await client.generate_embedding(request.text)
                
                return EmbeddingResponse(
                    embedding=embedding,
                    dimensions=len(embedding)
                )
            except Exception as e:
                log.exception("❌ Failed to generate embeddings")
                raise HTTPException(status_code=500, detail=str(e))

        # 🏷️ Generate tags route
        @self.router.post("/tags", response_model=TagsResponse)
        async def generate_tags(request: TagsRequest):
            """Generate relevant tags for the provided text."""
            try:
                client = get_openai_client()
                tags = await client.generate_tags(request.text, request.num_tags)
                
                return TagsResponse(
                    tags=tags,
                    count=len(tags)
                )
            except Exception as e:
                log.exception("❌ Failed to generate tags")
                raise HTTPException(status_code=500, detail=str(e))

        # 😊 Analyze sentiment route
        @self.router.post("/sentiment", response_model=SentimentResponse)
        async def analyze_sentiment(request: SentimentRequest):
            """Analyze the sentiment of the provided text."""
            try:
                client = get_openai_client()
                result = await client.analyze_sentiment(request.text)
                
                return SentimentResponse(
                    sentiment=result.get('sentiment', 'unknown'),
                    confidence=result.get('confidence', 0.0)
                )
            except Exception as e:
                log.exception("❌ Failed to analyze sentiment")
                raise HTTPException(status_code=500, detail=str(e))

        # 🔄 Batch processing route
        @self.router.post("/batch")
        async def batch_process(requests: Dict[str, Any]):
            """Process multiple AI operations in a single request."""
            try:
                client = get_openai_client()
                results = {}
                
                text = requests.get("text", "")
                if not text:
                    raise ValueError("Text is required for batch processing")
                
                operations = requests.get("operations", [])
                
                for operation in operations:
                    if operation == "summarize":
                        results["summary"] = await client.generate_summary(text)
                    elif operation == "embed":
                        results["embedding"] = await client.generate_embedding(text)
                    elif operation == "tags":
                        results["tags"] = await client.generate_tags(text)
                    elif operation == "sentiment":
                        results["sentiment"] = await client.analyze_sentiment(text)
                
                return {
                    "status": "success",
                    "text": text,
                    "results": results
                }
            except Exception as e:
                log.exception("❌ Failed to process batch request")
                raise HTTPException(status_code=500, detail=str(e))