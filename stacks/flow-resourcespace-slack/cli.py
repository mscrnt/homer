"""
Flow-ResourceSpace-Slack Stack CLI

Robust CLI for seamless asset sharing between Flow, ResourceSpace, and Slack.
"""
import click
import asyncio
import json
from homer.modules.flow.cli import cli as flow_cli
from homer.modules.resourcespace.cli import cli as resourcespace_cli
from homer.modules.slack.cli import cli as slack_cli
from homer.utils.logger import get_module_logger
from .logic.asset_bridge import AssetBridge, push_flow_asset_to_resourcespace, share_resourcespace_asset_to_slack, complete_flow_to_slack_workflow

log = get_module_logger("flow_resourcespace_slack.cli")


@click.group()
def cli():
    """Flow-ResourceSpace-Slack asset sharing integration"""
    pass


# Add module CLIs as subcommands
cli.add_command(flow_cli, name="flow")
cli.add_command(resourcespace_cli, name="resourcespace")
cli.add_command(slack_cli, name="slack")


@cli.command()
def status():
    """Show stack status and health"""
    click.echo("🔗 Flow-ResourceSpace-Slack Asset Bridge")
    click.echo("=" * 42)
    
    async def check_status():
        bridge = AssetBridge()
        try:
            health = await bridge.health_check()
            
            click.echo(f"Overall Status: {health['overall']}")
            click.echo()
            
            for service, status in health.items():
                if service != 'overall':
                    status_icon = "✅" if status.get('status') == 'ok' else "❌"
                    click.echo(f"{status_icon} {service.title()}: {status.get('status', 'unknown')}")
                    if 'error' in status:
                        click.echo(f"   Error: {status['error']}")
            
            click.echo()
            click.echo("Available workflows:")
            click.echo("  • flow-to-resourcespace: Push Flow assets to ResourceSpace")
            click.echo("  • resourcespace-to-slack: Share ResourceSpace assets in Slack")
            click.echo("  • complete-workflow: Flow → ResourceSpace → Slack")
            click.echo("  • project-sync: Sync entire Flow project")
            click.echo("  • search-and-share: Search ResourceSpace and share results")
            
        finally:
            await bridge.close()
    
    asyncio.run(check_status())


@cli.group()
def push():
    """Push assets between systems"""
    pass


@push.command()
@click.argument('flow_asset_id', type=int)
@click.option('--title', help='Override asset title')
@click.option('--description', help='Override asset description')
@click.option('--project-name', help='Override project name')
@click.option('--tags', help='Comma-separated tags')
@click.option('--output', type=click.File('w'), help='Save result to JSON file')
def flow_to_resourcespace(flow_asset_id, title, description, project_name, tags, output):
    """Push Flow asset to ResourceSpace with metadata"""
    
    # Prepare metadata overrides
    metadata_overrides = {}
    if title:
        metadata_overrides['title'] = title
    if description:
        metadata_overrides['description'] = description
    if project_name:
        metadata_overrides['project_name'] = project_name
    if tags:
        metadata_overrides['keywords'] = tags
    
    async def run_push():
        result = await push_flow_asset_to_resourcespace(flow_asset_id, metadata_overrides if metadata_overrides else None)
        
        if result['status'] == 'success':
            rs_result = result['resourcespace_result']
            click.echo(f"✅ Flow asset {flow_asset_id} pushed to ResourceSpace")
            click.echo(f"📁 ResourceSpace ID: {rs_result['resource_id']}")
            click.echo(f"📋 Title: {rs_result['title']}")
            click.echo(f"🔗 URL: {rs_result['url']}")
            
            if metadata_overrides:
                click.echo(f"🏷️  Metadata overrides applied: {len(metadata_overrides)} fields")
        else:
            click.echo(f"❌ Push failed: {result.get('error', 'Unknown error')}")
        
        if output:
            json.dump(result, output, indent=2)
            click.echo(f"💾 Full result saved to {output.name}")
        
        return result
    
    try:
        asyncio.run(run_push())
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@cli.group()
def share():
    """Share assets in Slack channels"""
    pass


@share.command()
@click.argument('resource_id')
@click.argument('channel')
@click.option('--message', help='Custom message to include')
@click.option('--include-preview', is_flag=True, help='Include asset preview in message')
def resourcespace_to_slack(resource_id, channel, message, include_preview):
    """Share ResourceSpace asset in Slack channel"""
    
    async def run_share():
        result = await share_resourcespace_asset_to_slack(resource_id, channel, message)
        
        if result['status'] == 'success':
            slack_result = result['slack_result']
            click.echo(f"✅ ResourceSpace asset {resource_id} shared in {channel}")
            click.echo(f"💬 Message ID: {slack_result['message_id']}")
            click.echo(f"⏰ Sent at: {slack_result['timestamp']}")
            
            if include_preview:
                click.echo(f"🖼️  Preview included: Yes")
        else:
            click.echo(f"❌ Share failed: {result.get('error', 'Unknown error')}")
        
        return result
    
    try:
        asyncio.run(run_share())
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@cli.group()
def workflow():
    """Complete asset workflows"""
    pass


@workflow.command()
@click.argument('flow_asset_id', type=int)
@click.argument('channel')
@click.option('--include-metadata', is_flag=True, default=True, help='Include Flow metadata in Slack message')
@click.option('--title', help='Override asset title')
@click.option('--tags', help='Comma-separated tags for ResourceSpace')
def complete(flow_asset_id, channel, include_metadata, title, tags):
    """Complete workflow: Flow → ResourceSpace → Slack"""
    
    async def run_workflow():
        click.echo(f"🚀 Starting complete workflow for Flow asset {flow_asset_id}")
        click.echo(f"   Flow → ResourceSpace → Slack ({channel})")
        click.echo()
        
        # Prepare metadata if provided
        metadata_overrides = {}
        if title:
            metadata_overrides['title'] = title
        if tags:
            metadata_overrides['keywords'] = tags
        
        # If we have overrides, need to do step-by-step
        if metadata_overrides:
            click.echo("📝 Step 1: Pushing to ResourceSpace with custom metadata...")
            rs_result = await push_flow_asset_to_resourcespace(flow_asset_id, metadata_overrides)
            
            if rs_result['status'] != 'success':
                click.echo(f"❌ Step 1 failed: {rs_result.get('error')}")
                return
            
            click.echo(f"✅ Step 1 complete: {rs_result['resourcespace_result']['resource_id']}")
            click.echo()
            
            click.echo("💬 Step 2: Sharing in Slack...")
            resource_id = rs_result['resourcespace_result']['resource_id']
            custom_message = f"🎬 Flow asset {flow_asset_id} uploaded to ResourceSpace"
            if include_metadata:
                custom_message += f"\n*Title:* {rs_result['resourcespace_result']['title']}"
            
            slack_result = await share_resourcespace_asset_to_slack(resource_id, channel, custom_message)
            
            if slack_result['status'] == 'success':
                click.echo(f"✅ Step 2 complete: Shared in {channel}")
                click.echo()
                click.echo("🎉 Complete workflow successful!")
                click.echo(f"📁 ResourceSpace: {resource_id}")
                click.echo(f"💬 Slack: {slack_result['slack_result']['message_id']}")
            else:
                click.echo(f"❌ Step 2 failed: {slack_result.get('error')}")
        else:
            # Use the optimized complete workflow
            result = await complete_flow_to_slack_workflow(flow_asset_id, channel)
            
            if result['status'] == 'success':
                click.echo("✅ Complete workflow successful!")
                click.echo(f"📁 ResourceSpace: {result['resourcespace_result']['resource_id']}")
                click.echo(f"💬 Slack: {result['slack_result']['message_id']}")
                click.echo()
                click.echo("Workflow steps completed:")
                for step in result['workflow_steps']:
                    click.echo(f"   ✅ {step.replace('_', ' ').title()}")
            elif result['status'] == 'partial_success':
                click.echo("⚠️  Partial success:")
                click.echo(f"✅ ResourceSpace: {result['resourcespace_result']['resource_id']}")
                click.echo(f"❌ Slack notification failed: {result['slack_error'].get('error')}")
            else:
                click.echo(f"❌ Workflow failed: {result.get('error', 'Unknown error')}")
    
    try:
        asyncio.run(run_workflow())
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@workflow.command()
@click.argument('project_id', type=int)
@click.argument('channel')
@click.option('--batch-size', default=5, help='Number of assets to process in each batch')
def sync_project(project_id, channel, batch_size):
    """Sync all assets from Flow project to ResourceSpace"""
    
    async def run_sync():
        click.echo(f"📊 Starting project sync for Flow project {project_id}")
        click.echo(f"   Target channel: {channel}")
        click.echo(f"   Batch size: {batch_size}")
        click.echo()
        
        bridge = AssetBridge()
        try:
            result = await bridge.sync_project_assets(project_id, channel)
            
            if result['status'] == 'success':
                click.echo("✅ Project sync completed!")
                click.echo(f"📁 Project: {result['project']['name']}")
                click.echo(f"📊 Total assets: {result['total_assets']}")
                click.echo(f"✅ Successful: {result['successful_syncs']}")
                click.echo(f"❌ Failed: {result['failed_syncs']}")
                click.echo()
                
                if result['successful_syncs'] > 0:
                    click.echo("✅ Successfully synced assets:")
                    for sync_result in result['sync_results']:
                        if sync_result['status'] == 'success':
                            click.echo(f"   • {sync_result['asset_name']} → {sync_result['resourcespace_id']}")
                
                if result['failed_syncs'] > 0:
                    click.echo()
                    click.echo("❌ Failed assets:")
                    for sync_result in result['sync_results']:
                        if sync_result['status'] == 'error':
                            click.echo(f"   • {sync_result['asset_name']}: {sync_result['error']}")
                
                click.echo(f"\n💬 Summary sent to {channel}")
            else:
                click.echo(f"❌ Project sync failed: {result.get('error', 'Unknown error')}")
        finally:
            await bridge.close()
    
    try:
        asyncio.run(run_sync())
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@cli.group()
def search():
    """Search and discovery tools"""
    pass


@search.command()
@click.argument('query')
@click.argument('channel')
@click.option('--max-results', default=5, type=int, help='Maximum results to share')
@click.option('--format', type=click.Choice(['summary', 'detailed']), default='summary', help='Message format')
def and_share(query, channel, max_results, format):
    """Search ResourceSpace and share results in Slack"""
    
    async def run_search():
        click.echo(f"🔍 Searching ResourceSpace for: '{query}'")
        click.echo(f"   Max results: {max_results}")
        click.echo(f"   Sharing in: {channel}")
        click.echo()
        
        bridge = AssetBridge()
        try:
            result = await bridge.search_and_share(query, channel, max_results)
            
            if result['status'] == 'success':
                click.echo("✅ Search and share completed!")
                click.echo(f"🔍 Query: '{result['search_query']}'")
                click.echo(f"📊 Total found: {result['total_found']}")
                click.echo(f"💬 Shared: {result['shared_count']} results in {channel}")
                
                if result['shared_count'] > 0:
                    click.echo()
                    click.echo("Shared assets:")
                    for i, asset in enumerate(result['slack_result']['results'], 1):
                        click.echo(f"   {i}. {asset['title']} ({asset['asset_type']})")
                else:
                    click.echo("No results found to share.")
            else:
                click.echo(f"❌ Search failed: {result.get('error', 'Unknown error')}")
        finally:
            await bridge.close()
    
    try:
        asyncio.run(run_search())
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@cli.group()
def bulk():
    """Bulk operations"""
    pass


@bulk.command()
@click.argument('asset_ids', nargs=-1, required=True, type=int)
@click.argument('channel')
@click.option('--delay', default=1.0, type=float, help='Delay between operations (seconds)')
def push_multiple(asset_ids, channel, delay):
    """Push multiple Flow assets through complete workflow"""
    
    async def run_bulk():
        click.echo(f"📦 Bulk operation: {len(asset_ids)} Flow assets")
        click.echo(f"   Target channel: {channel}")
        click.echo(f"   Delay between operations: {delay}s")
        click.echo()
        
        successful = 0
        failed = 0
        
        for i, asset_id in enumerate(asset_ids, 1):
            click.echo(f"[{i}/{len(asset_ids)}] Processing Flow asset {asset_id}...")
            
            try:
                result = await complete_flow_to_slack_workflow(asset_id, channel)
                
                if result['status'] == 'success':
                    click.echo(f"   ✅ Success: {result['resourcespace_result']['resource_id']}")
                    successful += 1
                else:
                    click.echo(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
                    failed += 1
                
                # Add delay between operations
                if i < len(asset_ids) and delay > 0:
                    await asyncio.sleep(delay)
                    
            except Exception as e:
                click.echo(f"   ❌ Error: {e}")
                failed += 1
        
        click.echo()
        click.echo("📊 Bulk operation summary:")
        click.echo(f"   ✅ Successful: {successful}")
        click.echo(f"   ❌ Failed: {failed}")
        click.echo(f"   📊 Success rate: {(successful/(successful+failed)*100):.1f}%")
    
    try:
        asyncio.run(run_bulk())
    except Exception as e:
        click.echo(f"❌ Error: {e}")


@cli.command()
def examples():
    """Show usage examples"""
    click.echo("🔗 Flow-ResourceSpace-Slack Usage Examples")
    click.echo("=" * 45)
    click.echo()
    
    click.echo("📤 Push Flow asset to ResourceSpace:")
    click.echo("   homer flow-resourcespace-slack push flow-to-resourcespace 12345")
    click.echo("   homer flow-resourcespace-slack push flow-to-resourcespace 12345 --title 'Hero Shot' --tags 'final,approved'")
    click.echo()
    
    click.echo("💬 Share ResourceSpace asset in Slack:")
    click.echo("   homer flow-resourcespace-slack share resourcespace-to-slack RS_12345_20231201 '#assets'")
    click.echo("   homer flow-resourcespace-slack share resourcespace-to-slack RS_12345_20231201 '#team' --message 'Check this out!'")
    click.echo()
    
    click.echo("🚀 Complete workflow (Flow → ResourceSpace → Slack):")
    click.echo("   homer flow-resourcespace-slack workflow complete 12345 '#assets'")
    click.echo("   homer flow-resourcespace-slack workflow complete 12345 '#team' --title 'Final Cut' --tags 'approved,final'")
    click.echo()
    
    click.echo("📊 Sync entire Flow project:")
    click.echo("   homer flow-resourcespace-slack workflow sync-project 789 '#project-updates'")
    click.echo()
    
    click.echo("🔍 Search and share results:")
    click.echo("   homer flow-resourcespace-slack search and-share 'hero shot' '#assets'")
    click.echo("   homer flow-resourcespace-slack search and-share 'final render' '#team' --max-results 3")
    click.echo()
    
    click.echo("📦 Bulk operations:")
    click.echo("   homer flow-resourcespace-slack bulk push-multiple 001 002 003 '#assets'")
    click.echo("   homer flow-resourcespace-slack bulk push-multiple 001 002 003 '#assets' --delay 2.0")
    click.echo()
    
    click.echo("📊 Check system status:")
    click.echo("   homer flow-resourcespace-slack status")


if __name__ == "__main__":
    cli()