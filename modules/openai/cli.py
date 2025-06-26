#!/usr/bin/env python3

import click
import asyncio
import json
from homer.cli_registry import register_cli
from homer.utils.logger import get_module_logger
from modules.openai.client import get_openai_client
from pathlib import Path
import os

log = get_module_logger("openai")

@register_cli("openai")
@click.group(
    help="🤖 OpenAI CLI — Commands for OpenAI integration",
    context_settings=dict(help_option_names=["-h", "--help"])
)
def cli():
    pass

@cli.command("summarize", help="Generate a summary of text")
@click.option("--text", "-t", help="Text to summarize")
@click.option("--file", "-f", type=click.Path(exists=True), help="File containing text to summarize")
@click.option("--max-length", type=int, help="Maximum length of summary")
@click.option("--api-key", help="OpenAI API key (overrides env var)")
def summarize(text: str, file: str, max_length: int, api_key: str):
    """Generate a summary of the provided text."""
    try:
        # Load environment config
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            from dotenv import load_dotenv
            load_dotenv(env_path)
        
        # Get text input
        if file:
            with open(file, 'r') as f:
                text = f.read()
        elif not text:
            click.echo("❌ Please provide text with --text or --file")
            return
        
        client = get_openai_client(api_key)
        summary = asyncio.run(client.generate_summary(text, max_length))
        
        click.echo("📝 Summary:")
        click.echo(summary)
        
    except Exception as e:
        click.echo(f"❌ Failed to generate summary: {e}")
        log.exception("Summarize error")

@cli.command("embed", help="Generate embeddings for text")
@click.option("--text", "-t", required=True, help="Text to embed")
@click.option("--output", "-o", type=click.Path(), help="Output file for embeddings (JSON)")
@click.option("--api-key", help="OpenAI API key (overrides env var)")
def embed(text: str, output: str, api_key: str):
    """Generate embeddings for the provided text."""
    try:
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            from dotenv import load_dotenv
            load_dotenv(env_path)
        
        client = get_openai_client(api_key)
        embedding = asyncio.run(client.generate_embedding(text))
        
        result = {
            "text": text,
            "embedding": embedding,
            "dimensions": len(embedding)
        }
        
        if output:
            with open(output, 'w') as f:
                json.dump(result, f, indent=2)
            click.echo(f"✅ Embeddings saved to {output}")
        else:
            click.echo(f"🧮 Generated {len(embedding)}-dimensional embedding")
            click.echo(f"📊 First 10 values: {embedding[:10]}")
        
    except Exception as e:
        click.echo(f"❌ Failed to generate embeddings: {e}")
        log.exception("Embed error")

@cli.command("tags", help="Generate tags for text")
@click.option("--text", "-t", help="Text to tag")
@click.option("--file", "-f", type=click.Path(exists=True), help="File containing text to tag")
@click.option("--num-tags", type=int, default=5, help="Number of tags to generate")
@click.option("--api-key", help="OpenAI API key (overrides env var)")
def generate_tags(text: str, file: str, num_tags: int, api_key: str):
    """Generate relevant tags for the provided text."""
    try:
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            from dotenv import load_dotenv
            load_dotenv(env_path)
        
        # Get text input
        if file:
            with open(file, 'r') as f:
                text = f.read()
        elif not text:
            click.echo("❌ Please provide text with --text or --file")
            return
        
        client = get_openai_client(api_key)
        tags = asyncio.run(client.generate_tags(text, num_tags))
        
        click.echo("🏷️  Generated tags:")
        for i, tag in enumerate(tags, 1):
            click.echo(f"  {i}. {tag}")
        
    except Exception as e:
        click.echo(f"❌ Failed to generate tags: {e}")
        log.exception("Tags error")

@cli.command("sentiment", help="Analyze sentiment of text")
@click.option("--text", "-t", help="Text to analyze")
@click.option("--file", "-f", type=click.Path(exists=True), help="File containing text to analyze")
@click.option("--api-key", help="OpenAI API key (overrides env var)")
def analyze_sentiment(text: str, file: str, api_key: str):
    """Analyze the sentiment of the provided text."""
    try:
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            from dotenv import load_dotenv
            load_dotenv(env_path)
        
        # Get text input
        if file:
            with open(file, 'r') as f:
                text = f.read()
        elif not text:
            click.echo("❌ Please provide text with --text or --file")
            return
        
        client = get_openai_client(api_key)
        result = asyncio.run(client.analyze_sentiment(text))
        
        sentiment = result.get('sentiment', 'unknown')
        confidence = result.get('confidence', 0.0)
        
        # Add emoji based on sentiment
        emoji = {"positive": "😊", "negative": "😞", "neutral": "😐"}.get(sentiment, "❓")
        
        click.echo(f"{emoji} Sentiment: {sentiment}")
        click.echo(f"📊 Confidence: {confidence:.2f}")
        
    except Exception as e:
        click.echo(f"❌ Failed to analyze sentiment: {e}")
        log.exception("Sentiment error")

@cli.command("ping", help="Check OpenAI module configuration")
def cli_ping():
    """Ping command to check OpenAI module status."""
    try:
        env_path = Path(__file__).parent / ".env"
        if env_path.exists():
            click.echo("✅ OpenAI module configuration found")
            click.echo(f"📁 Config path: {env_path}")
        else:
            click.echo("⚠️  No .env file found in OpenAI module")
            click.echo(f"📁 Expected path: {env_path}")
        
        # Check if API key is available
        if os.getenv("OPENAI_API_KEY"):
            click.echo("🔑 OpenAI API key configured")
            click.echo(f"🤖 Model: {os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')}")
        else:
            click.echo("❌ No OPENAI_API_KEY found in environment")
            
    except Exception as e:
        click.echo(f"❌ Ping failed: {e}")
        log.exception("Ping error")