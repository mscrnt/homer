import os
from openai import OpenAI
from homer.utils.logger import get_module_logger
from typing import List, Dict, Any

log = get_module_logger("openai.client")

class OpenAIClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.embedding_model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    
    async def generate_summary(self, text: str, max_length: int = None) -> str:
        """Generate a summary of the given text."""
        try:
            max_tokens = max_length or self.max_tokens
            
            prompt = f"Please provide a concise summary of the following text:\\n\\n{text}"
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates concise summaries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=self.temperature
            )
            
            summary = response.choices[0].message.content.strip()
            log.info(f"Generated summary of {len(text)} characters -> {len(summary)} characters")
            return summary
            
        except Exception as e:
            log.error(f"Failed to generate summary: {e}")
            raise
    
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate an embedding vector for the given text."""
        try:
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            
            embedding = response.data[0].embedding
            log.info(f"Generated embedding for text of {len(text)} characters -> {len(embedding)} dimensions")
            return embedding
            
        except Exception as e:
            log.error(f"Failed to generate embedding: {e}")
            raise
    
    async def generate_tags(self, text: str, num_tags: int = 5) -> List[str]:
        """Generate relevant tags for the given text."""
        try:
            prompt = f"Generate {num_tags} relevant tags for the following text. Return only the tags as a comma-separated list:\\n\\n{text}"
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates relevant tags for content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.5
            )
            
            tags_text = response.choices[0].message.content.strip()
            tags = [tag.strip() for tag in tags_text.split(',')]
            
            log.info(f"Generated {len(tags)} tags for text")
            return tags
            
        except Exception as e:
            log.error(f"Failed to generate tags: {e}")
            raise
    
    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze the sentiment of the given text."""
        try:
            prompt = f"Analyze the sentiment of the following text and return a JSON object with 'sentiment' (positive/negative/neutral) and 'confidence' (0-1):\\n\\n{text}"
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that analyzes sentiment. Always return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.3
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Try to parse as JSON, fallback to simple parsing
            try:
                import json
                result = json.loads(result_text)
            except:
                # Simple fallback parsing
                if "positive" in result_text.lower():
                    result = {"sentiment": "positive", "confidence": 0.8}
                elif "negative" in result_text.lower():
                    result = {"sentiment": "negative", "confidence": 0.8}
                else:
                    result = {"sentiment": "neutral", "confidence": 0.6}
            
            log.info(f"Analyzed sentiment: {result}")
            return result
            
        except Exception as e:
            log.error(f"Failed to analyze sentiment: {e}")
            raise

def get_openai_client(api_key: str = None) -> OpenAIClient:
    """Get a configured OpenAI client instance."""
    return OpenAIClient(api_key)