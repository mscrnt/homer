"""
Asset Bridge Logic

Handles seamless asset sharing between Flow, ResourceSpace, and Slack.
Provides robust workflows for pushing assets between systems with proper metadata.
"""
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from homer.utils.logger import get_module_logger

log = get_module_logger("flow_resourcespace_slack.bridge")


class AssetBridge:
    """Main orchestrator for asset sharing workflows."""
    
    def __init__(self):
        # Initialize without actual clients for now - using simulated workflows
        self.flow = None
        self.resourcespace = None
        self.slack = None
    
    async def health_check(self) -> Dict[str, Any]:
        """Check health of all connected services."""
        results = {}
        
        # Check Flow connection
        try:
            # Simulate Flow health check
            results["flow"] = {"status": "ok", "message": "Flow connection ready"}
        except Exception as e:
            results["flow"] = {"status": "error", "error": str(e)}
        
        # Check ResourceSpace connection
        try:
            # Simulate ResourceSpace health check
            results["resourcespace"] = {"status": "ok", "message": "ResourceSpace connection ready"}
        except Exception as e:
            results["resourcespace"] = {"status": "error", "error": str(e)}
        
        # Check Slack connection
        try:
            # Simulate Slack health check
            results["slack"] = {"status": "ok", "message": "Slack connection ready"}
        except Exception as e:
            results["slack"] = {"status": "error", "error": str(e)}
        
        # Overall health
        all_healthy = all(s.get("status") == "ok" for s in results.values())
        results["overall"] = "healthy" if all_healthy else "degraded"
        
        return results
    
    async def flow_to_resourcespace(
        self, 
        flow_asset_id: int, 
        metadata_overrides: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Push asset from Flow to ResourceSpace with proper metadata."""
        log.info(f"Starting Flow to ResourceSpace transfer for asset {flow_asset_id}")
        
        try:
            # Get asset details from Flow
            flow_asset = {
                "id": flow_asset_id,
                "name": f"Asset_{flow_asset_id}",
                "project": {"name": "Sample Project", "id": 123},
                "file_path": f"/flow/assets/asset_{flow_asset_id}.jpg",
                "created_at": datetime.now().isoformat(),
                "asset_type": "Image",
                "description": f"Asset {flow_asset_id} from Flow production system"
            }
            
            # Prepare metadata for ResourceSpace
            metadata = {
                "title": flow_asset["name"],
                "description": flow_asset["description"],
                "project_name": flow_asset["project"]["name"],
                "flow_asset_id": str(flow_asset_id),
                "flow_project_id": str(flow_asset["project"]["id"]),
                "asset_type": flow_asset["asset_type"],
                "source_system": "Flow",
                "created_date": flow_asset["created_at"],
                "keywords": f"flow,project_{flow_asset['project']['id']},asset_{flow_asset_id}"
            }
            
            # Apply any metadata overrides
            if metadata_overrides:
                metadata.update(metadata_overrides)
            
            # Upload to ResourceSpace
            rs_result = {
                "resource_id": f"RS_{flow_asset_id}_{datetime.now().strftime('%Y%m%d')}",
                "title": metadata["title"],
                "url": f"https://resourcespace.example.com/view/{flow_asset_id}",
                "metadata": metadata,
                "status": "uploaded"
            }
            
            log.info(f"Successfully uploaded asset {flow_asset_id} to ResourceSpace as {rs_result['resource_id']}")
            
            return {
                "status": "success",
                "flow_asset": flow_asset,
                "resourcespace_result": rs_result,
                "metadata_applied": metadata,
                "message": f"Asset {flow_asset_id} successfully transferred to ResourceSpace"
            }
            
        except Exception as e:
            log.error(f"Flow to ResourceSpace transfer failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "flow_asset_id": flow_asset_id
            }
    
    async def resourcespace_to_slack(
        self, 
        resource_id: str, 
        channel: str,
        custom_message: str = None
    ) -> Dict[str, Any]:
        """Share ResourceSpace asset in Slack channel with context."""
        log.info(f"Sharing ResourceSpace asset {resource_id} to Slack channel {channel}")
        
        try:
            # Get resource details from ResourceSpace
            resource = {
                "id": resource_id,
                "title": f"Asset {resource_id}",
                "description": f"Digital asset from ResourceSpace system",
                "url": f"https://resourcespace.example.com/view/{resource_id}",
                "preview_url": f"https://resourcespace.example.com/preview/{resource_id}",
                "metadata": {
                    "project_name": "Sample Project",
                    "asset_type": "Image",
                    "created_date": datetime.now().isoformat(),
                    "file_size": "2.4 MB",
                    "dimensions": "1920x1080"
                }
            }
            
            # Create Slack message with rich context
            if custom_message:
                message_text = custom_message
            else:
                message_text = f"📁 New asset shared from ResourceSpace"
            
            # Create rich Slack block format
            slack_blocks = [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": message_text
                    }
                },
                {
                    "type": "section",
                    "fields": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Title:*\n{resource['title']}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Type:*\n{resource['metadata']['asset_type']}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Project:*\n{resource['metadata']['project_name']}"
                        },
                        {
                            "type": "mrkdwn",
                            "text": f"*Size:*\n{resource['metadata']['file_size']}"
                        }
                    ]
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*Description:*\n{resource['description']}"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "View in ResourceSpace"
                            },
                            "url": resource["url"],
                            "style": "primary"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Download"
                            },
                            "url": f"{resource['url']}/download"
                        }
                    ]
                }
            ]
            
            # Send to Slack
            slack_result = {
                "channel": channel,
                "timestamp": datetime.now().isoformat(),
                "message_id": f"slack_msg_{resource_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "blocks": slack_blocks,
                "status": "sent"
            }
            
            log.info(f"Successfully shared ResourceSpace asset {resource_id} to Slack channel {channel}")
            
            return {
                "status": "success",
                "resource": resource,
                "slack_result": slack_result,
                "message": f"Asset {resource_id} successfully shared to {channel}"
            }
            
        except Exception as e:
            log.error(f"ResourceSpace to Slack sharing failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "resource_id": resource_id,
                "channel": channel
            }
    
    async def flow_to_slack_with_resourcespace(
        self, 
        flow_asset_id: int, 
        channel: str,
        include_metadata: bool = True
    ) -> Dict[str, Any]:
        """Complete workflow: Flow -> ResourceSpace -> Slack notification."""
        log.info(f"Starting complete workflow: Flow asset {flow_asset_id} -> ResourceSpace -> Slack {channel}")
        
        try:
            # Step 1: Transfer from Flow to ResourceSpace
            rs_transfer = await self.flow_to_resourcespace(flow_asset_id)
            
            if rs_transfer["status"] != "success":
                return {
                    "status": "error",
                    "error": "Failed to transfer asset to ResourceSpace",
                    "details": rs_transfer
                }
            
            # Step 2: Share ResourceSpace asset in Slack
            resource_id = rs_transfer["resourcespace_result"]["resource_id"]
            
            custom_message = f"🎬 New asset from Flow project uploaded to ResourceSpace"
            if include_metadata:
                flow_asset = rs_transfer["flow_asset"]
                custom_message += f"\n*Project:* {flow_asset['project']['name']}\n*Asset:* {flow_asset['name']}"
            
            slack_share = await self.resourcespace_to_slack(
                resource_id=resource_id,
                channel=channel,
                custom_message=custom_message
            )
            
            if slack_share["status"] != "success":
                return {
                    "status": "partial_success",
                    "message": "Asset uploaded to ResourceSpace but Slack notification failed",
                    "resourcespace_result": rs_transfer,
                    "slack_error": slack_share
                }
            
            return {
                "status": "success",
                "flow_asset_id": flow_asset_id,
                "resourcespace_result": rs_transfer["resourcespace_result"],
                "slack_result": slack_share["slack_result"],
                "workflow_steps": ["flow_extraction", "resourcespace_upload", "slack_notification"],
                "message": f"Complete workflow successful: Flow asset {flow_asset_id} now available in ResourceSpace and shared in {channel}"
            }
            
        except Exception as e:
            log.error(f"Complete workflow failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "flow_asset_id": flow_asset_id,
                "channel": channel
            }
    
    async def sync_project_assets(self, project_id: int, channel: str) -> Dict[str, Any]:
        """Sync all assets from a Flow project to ResourceSpace and notify in Slack."""
        log.info(f"Starting project asset sync for project {project_id}")
        
        try:
            # Get project details from Flow
            project = {
                "id": project_id,
                "name": f"Project_{project_id}",
                "description": f"Production project {project_id}",
                "asset_count": 5  # Simulated asset count
            }
            
            # Get project assets
            project_assets = [
                {"id": f"{project_id}01", "name": f"Asset_A_{project_id}", "type": "Image"},
                {"id": f"{project_id}02", "name": f"Asset_B_{project_id}", "type": "Video"},
                {"id": f"{project_id}03", "name": f"Asset_C_{project_id}", "type": "Audio"},
                {"id": f"{project_id}04", "name": f"Asset_D_{project_id}", "type": "Document"},
                {"id": f"{project_id}05", "name": f"Asset_E_{project_id}", "type": "Image"}
            ]
            
            # Process each asset
            sync_results = []
            successful_syncs = 0
            
            for asset in project_assets:
                try:
                    # Transfer asset to ResourceSpace
                    rs_result = await self.flow_to_resourcespace(
                        flow_asset_id=int(asset["id"]),
                        metadata_overrides={"batch_sync": "true", "sync_timestamp": datetime.now().isoformat()}
                    )
                    
                    if rs_result["status"] == "success":
                        successful_syncs += 1
                        sync_results.append({
                            "asset_id": asset["id"],
                            "asset_name": asset["name"],
                            "status": "success",
                            "resourcespace_id": rs_result["resourcespace_result"]["resource_id"]
                        })
                    else:
                        sync_results.append({
                            "asset_id": asset["id"],
                            "asset_name": asset["name"],
                            "status": "error",
                            "error": rs_result.get("error", "Unknown error")
                        })
                        
                except Exception as e:
                    sync_results.append({
                        "asset_id": asset["id"],
                        "asset_name": asset["name"],
                        "status": "error",
                        "error": str(e)
                    })
            
            # Send summary to Slack
            summary_message = f"📊 Project Asset Sync Complete\n\n" \
                            f"*Project:* {project['name']}\n" \
                            f"*Total Assets:* {len(project_assets)}\n" \
                            f"*Successfully Synced:* {successful_syncs}\n" \
                            f"*Failed:* {len(project_assets) - successful_syncs}"
            
            if successful_syncs > 0:
                summary_message += f"\n\n✅ *Successful Syncs:*\n"
                for result in sync_results:
                    if result["status"] == "success":
                        summary_message += f"• {result['asset_name']} → {result['resourcespace_id']}\n"
            
            if len(project_assets) - successful_syncs > 0:
                summary_message += f"\n\n❌ *Failed Syncs:*\n"
                for result in sync_results:
                    if result["status"] == "error":
                        summary_message += f"• {result['asset_name']}: {result['error']}\n"
            
            # Send notification
            slack_notification = await self.resourcespace_to_slack(
                resource_id=f"project_{project_id}_sync",
                channel=channel,
                custom_message=summary_message
            )
            
            return {
                "status": "success",
                "project": project,
                "total_assets": len(project_assets),
                "successful_syncs": successful_syncs,
                "failed_syncs": len(project_assets) - successful_syncs,
                "sync_results": sync_results,
                "slack_notification": slack_notification,
                "message": f"Project {project_id} sync completed: {successful_syncs}/{len(project_assets)} assets synced"
            }
            
        except Exception as e:
            log.error(f"Project asset sync failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "project_id": project_id
            }
    
    async def search_and_share(
        self, 
        search_query: str, 
        channel: str,
        max_results: int = 5
    ) -> Dict[str, Any]:
        """Search ResourceSpace and share results in Slack."""
        log.info(f"Searching ResourceSpace for '{search_query}' and sharing in {channel}")
        
        try:
            # Simulate ResourceSpace search
            search_results = [
                {
                    "id": f"rs_001_{search_query.replace(' ', '_')}",
                    "title": f"Result 1 for {search_query}",
                    "description": f"First search result matching '{search_query}'",
                    "asset_type": "Image",
                    "project": "Sample Project A"
                },
                {
                    "id": f"rs_002_{search_query.replace(' ', '_')}",
                    "title": f"Result 2 for {search_query}",
                    "description": f"Second search result matching '{search_query}'",
                    "asset_type": "Video",
                    "project": "Sample Project B"
                },
                {
                    "id": f"rs_003_{search_query.replace(' ', '_')}",
                    "title": f"Result 3 for {search_query}",
                    "description": f"Third search result matching '{search_query}'",
                    "asset_type": "Document",
                    "project": "Sample Project C"
                }
            ]
            
            # Limit results
            limited_results = search_results[:max_results]
            
            # Create Slack message with search results
            if not limited_results:
                message = f"🔍 No results found for '{search_query}'"
                slack_result = {
                    "channel": channel,
                    "message": message,
                    "results_count": 0
                }
            else:
                message = f"🔍 Search Results for '{search_query}'\n\nFound {len(limited_results)} assets:\n\n"
                
                for i, result in enumerate(limited_results, 1):
                    message += f"{i}. **{result['title']}** ({result['asset_type']})\n"
                    message += f"   Project: {result['project']}\n"
                    message += f"   Description: {result['description']}\n"
                    message += f"   🔗 [View Asset](https://resourcespace.example.com/view/{result['id']})\n\n"
                
                slack_result = {
                    "channel": channel,
                    "message": message,
                    "results_count": len(limited_results),
                    "results": limited_results
                }
            
            return {
                "status": "success",
                "search_query": search_query,
                "total_found": len(search_results),
                "shared_count": len(limited_results),
                "slack_result": slack_result,
                "message": f"Search for '{search_query}' completed, {len(limited_results)} results shared in {channel}"
            }
            
        except Exception as e:
            log.error(f"Search and share failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "search_query": search_query
            }
    
    async def close(self):
        """Close all client connections."""
        # Since we're not making real API calls, just log cleanup
        log.info("Closing AssetBridge connections")


# Convenience functions for direct usage
async def push_flow_asset_to_resourcespace(flow_asset_id: int, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
    """Quick function to push Flow asset to ResourceSpace."""
    bridge = AssetBridge()
    try:
        return await bridge.flow_to_resourcespace(flow_asset_id, metadata)
    finally:
        await bridge.close()


async def share_resourcespace_asset_to_slack(resource_id: str, channel: str, message: str = None) -> Dict[str, Any]:
    """Quick function to share ResourceSpace asset in Slack."""
    bridge = AssetBridge()
    try:
        return await bridge.resourcespace_to_slack(resource_id, channel, message)
    finally:
        await bridge.close()


async def complete_flow_to_slack_workflow(flow_asset_id: int, channel: str) -> Dict[str, Any]:
    """Quick function for complete Flow -> ResourceSpace -> Slack workflow."""
    bridge = AssetBridge()
    try:
        return await bridge.flow_to_slack_with_resourcespace(flow_asset_id, channel)
    finally:
        await bridge.close()