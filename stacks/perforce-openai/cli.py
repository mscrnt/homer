"""
Perforce-OpenAI Stack CLI
"""
import click
import asyncio
from homer.modules.perforce.cli import cli as perforce_cli
from homer.modules.openai.cli import cli as openai_cli
from homer.utils.logger import get_module_logger
from .logic.ai_code_analysis import AICodeAnalysis, analyze_changelist_quick, generate_smart_commit_message

log = get_module_logger("perforce_openai.cli")


@click.group()
def cli():
    """Perforce-OpenAI AI-powered code analysis stack"""
    pass


# Add module CLIs as subcommands
cli.add_command(perforce_cli, name="perforce")
cli.add_command(openai_cli, name="openai")


@cli.command()
def status():
    """Show stack status and health"""
    click.echo("🤖 Perforce-OpenAI AI Code Analysis Stack")
    click.echo("=" * 42)
    
    async def check_status():
        analyzer = AICodeAnalysis()
        health = await analyzer.health_check()
        
        click.echo(f"Overall Status: {health['overall']}")
        click.echo()
        
        for service, status in health.items():
            if service != 'overall':
                status_icon = "✅" if status.get('status') == 'ok' else "❌"
                click.echo(f"{status_icon} {service.title()}: {status.get('status', 'unknown')}")
                if 'error' in status:
                    click.echo(f"   Error: {status['error']}")
    
    asyncio.run(check_status())


@cli.group()
def analyze():
    """AI-powered code analysis commands"""
    pass


@analyze.command()
@click.argument('changelist_id')
@click.option('--include-files', is_flag=True, help='Include file list in analysis')
@click.option('--output', type=click.File('w'), help='Save analysis to file')
def changelist(changelist_id, include_files, output):
    """Analyze a Perforce changelist using AI"""
    
    async def run_analysis():
        result = await analyze_changelist_quick(changelist_id)
        
        click.echo(f"🔍 AI Analysis for Changelist {changelist_id}")
        click.echo("=" * 50)
        click.echo(f"📝 Original: {result['original_description'][:100]}...")
        click.echo(f"📊 Files: {result['files_count']}")
        click.echo()
        
        ai_analysis = result['ai_analysis']
        click.echo(f"🤖 AI Summary: {ai_analysis['summary']}")
        click.echo(f"🏷️  Tags: {', '.join(ai_analysis['tags'])}")
        click.echo(f"😊 Sentiment: {ai_analysis['sentiment']}")
        click.echo(f"🔧 Type: {ai_analysis['change_type']}")
        click.echo(f"📈 Confidence: {ai_analysis['confidence']}")
        
        if result.get('recommendations'):
            click.echo("\n💡 Recommendations:")
            for rec in result['recommendations']:
                click.echo(f"   • {rec}")
        
        if output:
            import json
            json.dump(result, output, indent=2)
            click.echo(f"\n💾 Full analysis saved to {output.name}")
    
    try:
        asyncio.run(run_analysis())
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@analyze.command()
@click.argument('changelists', nargs=-1, required=True)
@click.option('--audience', default='technical', help='Target audience (technical/business)')
@click.option('--output', type=click.File('w'), help='Save release notes to file')
def release_notes(changelists, audience, output):
    """Generate AI-powered release notes from changelists"""
    
    async def run_generation():
        analyzer = AICodeAnalysis()
        result = await analyzer.generate_release_notes(list(changelists), audience)
        
        click.echo(f"📋 AI-Generated Release Notes")
        click.echo("=" * 35)
        click.echo(f"📊 Analyzed: {result['changelists_analyzed']} changelists")
        click.echo(f"🎯 Audience: {result['target_audience']}")
        click.echo()
        
        categorization = result['categorization']
        click.echo(f"📈 Categories:")
        click.echo(f"   • Features: {categorization['features']}")
        click.echo(f"   • Bug Fixes: {categorization['bugfixes']}")
        click.echo(f"   • Other: {categorization['other']}")
        click.echo()
        
        click.echo("📝 Release Notes:")
        click.echo("-" * 20)
        click.echo(result['release_notes'])
        click.echo()
        
        click.echo(f"🔖 Version Suggestion: {result['version_suggestion']}")
        
        if output:
            output.write(result['release_notes'])
            click.echo(f"\n💾 Release notes saved to {output.name}")
    
    try:
        asyncio.run(run_generation())
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@analyze.command()
@click.argument('changelist_id')
@click.option('--focus', multiple=True, help='Focus areas for review (security, performance, etc.)')
def code_review(changelist_id, focus):
    """AI-powered code review assistant"""
    
    async def run_review():
        analyzer = AICodeAnalysis()
        result = await analyzer.code_review_assistant(changelist_id, list(focus) if focus else None)
        
        click.echo(f"🔍 AI Code Review for Changelist {changelist_id}")
        click.echo("=" * 45)
        click.echo(f"📁 Files: {result['files_count']}")
        click.echo(f"🎯 Focus: {', '.join(result['focus_areas'])}")
        click.echo()
        
        click.echo("🤖 AI Review Analysis:")
        click.echo("-" * 25)
        click.echo(result['review_analysis'])
        click.echo()
        
        click.echo(f"⚠️  Risk Assessment: {result['risk_assessment']}")
        click.echo()
        
        security = result['security_check']
        if security['has_security_concerns']:
            click.echo("🔒 Security Check:")
            click.echo(f"   {security['recommendation']}")
            click.echo()
        
        recommendations = result['recommendations']
        click.echo("📋 Recommendations:")
        for key, value in recommendations.items():
            status = "✅" if value else "⏭️"
            click.echo(f"   {status} {key.replace('_', ' ').title()}: {value}")
    
    try:
        asyncio.run(run_review())
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@cli.group()
def commit():
    """Smart commit message generation"""
    pass


@commit.command()
@click.argument('files', nargs=-1, required=True)
@click.option('--summary', help='Brief summary of changes')
def message(files, summary):
    """Generate AI-powered commit message from file changes"""
    
    async def run_generation():
        result = await generate_smart_commit_message(list(files), summary or "")
        
        click.echo("🤖 AI-Generated Commit Message")
        click.echo("=" * 35)
        click.echo(f"📁 Files: {result['files_analyzed']}")
        click.echo(f"📊 Types: {', '.join([f'{k}({v})' for k, v in result['file_types'].items()])}")
        click.echo(f"📈 Confidence: {result['confidence']}")
        click.echo()
        
        click.echo("📝 Commit Message:")
        click.echo("-" * 20)
        click.echo(result['commit_message'])
        click.echo()
        
        click.echo("📄 Extended Description:")
        click.echo("-" * 25)
        click.echo(result['extended_description'])
    
    try:
        asyncio.run(run_generation())
    except Exception as e:
        click.echo(f"❌ Error: {e}")


if __name__ == "__main__":
    cli()