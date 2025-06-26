"""
Slack-SyncSketch Stack CLI
"""
import click
import asyncio
from pathlib import Path
from homer.modules.slack.cli import cli as slack_cli
from homer.modules.syncsketch.cli import cli as syncsketch_cli
from homer.utils.logger import get_module_logger
from .logic.creative_workflow import CreativeWorkflowAutomation, upload_and_notify, create_review_and_notify

log = get_module_logger("slack_syncsketch.cli")


@click.group()
def cli():
    """Slack-SyncSketch integrated creative workflow stack"""
    pass


# Add module CLIs as subcommands
cli.add_command(slack_cli, name="slack")
cli.add_command(syncsketch_cli, name="syncsketch")


@cli.command()
def status():
    """Show stack status and health"""
    click.echo("🎨 Slack-SyncSketch Creative Workflow Stack")
    click.echo("=" * 40)
    
    async def check_status():
        workflow = CreativeWorkflowAutomation()
        try:
            health = await workflow.health_check()
            
            click.echo(f"Overall Status: {health['overall']}")
            click.echo()
            
            for service, status in health.items():
                if service != 'overall':
                    status_icon = "✅" if status.get('status') == 'ok' else "❌"
                    click.echo(f"{status_icon} {service.title()}: {status.get('status', 'unknown')}")
                    if 'error' in status:
                        click.echo(f"   Error: {status['error']}")
        finally:
            await workflow.close()
    
    asyncio.run(check_status())


@cli.group()
def workflow():
    """Creative workflow automation commands"""
    pass


@workflow.command()
@click.argument('media_path', type=click.Path(exists=True))
@click.argument('project_id', type=int)
@click.option('--channel', default='#creative', help='Slack channel for notification')
@click.option('--message', help='Custom notification message')
def upload_notify(media_path, project_id, channel, message):
    """Upload media to SyncSketch and notify team via Slack"""
    
    async def run_upload():
        result = await upload_and_notify(media_path, project_id, channel)
        
        if result['status'] == 'success':
            click.echo(f"✅ Successfully uploaded {Path(media_path).name}")
            click.echo(f"📁 Project: {result['project_name']}")
            click.echo(f"💬 Notified: {channel}")
            
            if 'url' in result['upload']:
                click.echo(f"🔗 View: {result['upload']['url']}")
        else:
            click.echo(f"❌ Upload failed: {result.get('error', 'Unknown error')}")
    
    try:
        asyncio.run(run_upload())
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@workflow.command()
@click.argument('project_id', type=int)
@click.argument('review_name')
@click.option('--description', default='', help='Review description')
@click.option('--channel', default='#creative', help='Slack channel for notification')
def create_review(project_id, review_name, description, channel):
    """Create SyncSketch review and notify team via Slack"""
    
    async def run_create():
        result = await create_review_and_notify(project_id, review_name, description, channel)
        
        if result['status'] == 'success':
            click.echo(f"✅ Successfully created review: {review_name}")
            click.echo(f"📁 Project: {result['project_name']}")
            click.echo(f"💬 Notified: {channel}")
            
            if 'url' in result['review']:
                click.echo(f"🔗 View: {result['review']['url']}")
        else:
            click.echo(f"❌ Review creation failed: {result.get('error', 'Unknown error')}")
    
    try:
        asyncio.run(run_create())
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@workflow.command()
@click.argument('project_ids', nargs=-1, type=int, required=True)
@click.option('--channel', default='#daily-updates', help='Slack channel for summary')
def daily_summary(project_ids, channel):
    """Generate and send daily project summary to Slack"""
    
    async def run_summary():
        workflow = CreativeWorkflowAutomation()
        try:
            result = await workflow.daily_project_summary(list(project_ids), channel)
            
            if result['status'] == 'success':
                click.echo(f"✅ Daily summary sent for {result['projects_summarized']} projects")
                click.echo(f"💬 Sent to: {channel}")
            else:
                click.echo(f"❌ Summary failed: {result.get('error', 'Unknown error')}")
        finally:
            await workflow.close()
    
    try:
        asyncio.run(run_summary())
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@workflow.command()
@click.argument('project_id', type=int)
@click.argument('review_id', type=int)
@click.option('--channel', default='#creative', help='Slack channel for notification')
def review_complete(project_id, review_id, channel):
    """Handle review completion workflow"""
    
    async def run_completion():
        workflow = CreativeWorkflowAutomation()
        try:
            result = await workflow.review_completion_workflow(project_id, review_id, channel)
            
            if result['status'] == 'success':
                click.echo(f"✅ Review completion processed")
                click.echo(f"📁 Review: {result['review']['name']}")
                click.echo(f"🎬 Items reviewed: {result['items_count']}")
                click.echo(f"💬 Notified: {channel}")
            else:
                click.echo(f"❌ Completion workflow failed: {result.get('error', 'Unknown error')}")
        finally:
            await workflow.close()
    
    try:
        asyncio.run(run_completion())
    except Exception as e:
        click.echo(f"❌ Error: {e}")


if __name__ == "__main__":
    cli()