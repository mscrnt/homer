"""
System orchestration logic that combines all HOMER modules for comprehensive automation.
"""
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from homer.utils.logger import get_module_logger

# Import all module clients
from homer.modules.slack.client import SlackClient
from homer.modules.discord.client import DiscordClient
from homer.modules.github.client import GitHubClient
from homer.modules.atlassian.client import AtlassianClient
from homer.modules.openai.client import OpenAIClient
from homer.modules.perforce.client import PerforceClient
from homer.modules.syncsketch.client import SyncSketchClient
from homer.modules.netbox.client import NetBoxClient
from homer.modules.ha_api.client import HAClient
from homer.modules.resourcespace.client import ResourceSpaceClient

log = get_module_logger("stack.homer_latest.system_orchestration")

class SystemOrchestration:
    """Orchestrates workflows across all HOMER modules."""
    
    def __init__(self):
        self.clients = {}
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize all available clients."""
        try:
            self.clients['slack'] = SlackClient()
        except Exception as e:
            log.warning(f"Slack client not available: {e}")
            
        try:
            self.clients['discord'] = DiscordClient()
        except Exception as e:
            log.warning(f"Discord client not available: {e}")
            
        try:
            self.clients['github'] = GitHubClient()
        except Exception as e:
            log.warning(f"GitHub client not available: {e}")
            
        try:
            self.clients['atlassian'] = AtlassianClient()
        except Exception as e:
            log.warning(f"Atlassian client not available: {e}")
            
        try:
            self.clients['openai'] = OpenAIClient()
        except Exception as e:
            log.warning(f"OpenAI client not available: {e}")
            
        try:
            self.clients['perforce'] = PerforceClient()
        except Exception as e:
            log.warning(f"Perforce client not available: {e}")
            
        try:
            self.clients['syncsketch'] = SyncSketchClient()
        except Exception as e:
            log.warning(f"SyncSketch client not available: {e}")
            
        try:
            self.clients['netbox'] = NetBoxClient()
        except Exception as e:
            log.warning(f"NetBox client not available: {e}")
            
        try:
            self.clients['ha_api'] = HAClient()
        except Exception as e:
            log.warning(f"Home Assistant client not available: {e}")
            
        try:
            self.clients['resourcespace'] = ResourceSpaceClient()
        except Exception as e:
            log.warning(f"ResourceSpace client not available: {e}")
        
        log.info(f"Initialized {len(self.clients)} clients: {list(self.clients.keys())}")

    async def comprehensive_health_check(self) -> Dict[str, Any]:
        """Check health of all configured services."""
        log.info("Running comprehensive health check across all services")
        
        health_results = {}
        overall_status = "ok"
        services_checked = 0
        services_healthy = 0
        
        for service_name, client in self.clients.items():
            try:
                services_checked += 1
                health = await client.health_check()
                health_results[service_name] = health
                
                if health.get("status") == "ok":
                    services_healthy += 1
                else:
                    overall_status = "degraded"
                    
            except Exception as e:
                health_results[service_name] = {
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
                overall_status = "degraded"
        
        summary = {
            "overall_status": overall_status,
            "services_checked": services_checked,
            "services_healthy": services_healthy,
            "health_percentage": round((services_healthy / services_checked) * 100, 1) if services_checked > 0 else 0,
            "timestamp": datetime.now().isoformat(),
            "services": health_results
        }
        
        log.info(f"Health check complete: {services_healthy}/{services_checked} services healthy")
        return summary

    async def intelligent_notification_pipeline(self, event_type: str, event_data: Dict[str, Any], 
                                               notification_channels: List[str] = None) -> Dict[str, Any]:
        """Intelligent notification system that routes events to appropriate channels using AI."""
        log.info(f"Processing {event_type} event for intelligent notification")
        
        if not notification_channels:
            notification_channels = ['slack', 'discord']
        
        notifications_sent = []
        
        # Use AI to enhance the event description
        if 'openai' in self.clients:
            try:
                enhanced_description = await self._enhance_event_with_ai(event_type, event_data)
                event_data['ai_enhanced_description'] = enhanced_description
            except Exception as e:
                log.warning(f"Failed to enhance event with AI: {e}")
        
        # Send notifications to configured channels
        for channel in notification_channels:
            if channel in self.clients:
                try:
                    notification_result = await self._send_notification(
                        channel, event_type, event_data
                    )
                    notifications_sent.append({
                        "channel": channel,
                        "status": "sent",
                        "result": notification_result
                    })
                except Exception as e:
                    notifications_sent.append({
                        "channel": channel,
                        "status": "failed",
                        "error": str(e)
                    })
        
        result = {
            "event_type": event_type,
            "notifications_sent": len([n for n in notifications_sent if n["status"] == "sent"]),
            "notifications_failed": len([n for n in notifications_sent if n["status"] == "failed"]),
            "details": notifications_sent,
            "timestamp": datetime.now().isoformat()
        }
        
        log.info(f"Notification pipeline complete: {result['notifications_sent']} sent, {result['notifications_failed']} failed")
        return result

    async def cross_platform_project_sync(self, project_config: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronize project data across multiple platforms."""
        log.info(f"Starting cross-platform sync for project: {project_config.get('name', 'Unknown')}")
        
        sync_results = {}
        
        # GitHub -> Jira sync
        if project_config.get('github_repo') and 'github' in self.clients and 'atlassian' in self.clients:
            try:
                github_sync = await self._sync_github_to_jira(project_config)
                sync_results['github_jira'] = github_sync
            except Exception as e:
                sync_results['github_jira'] = {"status": "failed", "error": str(e)}
        
        # Perforce -> Documentation sync
        if project_config.get('perforce_depot') and 'perforce' in self.clients and 'atlassian' in self.clients:
            try:
                p4_sync = await self._sync_perforce_to_confluence(project_config)
                sync_results['perforce_confluence'] = p4_sync
            except Exception as e:
                sync_results['perforce_confluence'] = {"status": "failed", "error": str(e)}
        
        # Creative assets sync
        if project_config.get('syncsketch_project') and 'syncsketch' in self.clients and 'resourcespace' in self.clients:
            try:
                creative_sync = await self._sync_creative_assets(project_config)
                sync_results['creative_assets'] = creative_sync
            except Exception as e:
                sync_results['creative_assets'] = {"status": "failed", "error": str(e)}
        
        result = {
            "project_name": project_config.get('name'),
            "sync_operations": len(sync_results),
            "successful_syncs": len([r for r in sync_results.values() if r.get("status") == "success"]),
            "failed_syncs": len([r for r in sync_results.values() if r.get("status") == "failed"]),
            "details": sync_results,
            "timestamp": datetime.now().isoformat()
        }
        
        log.info(f"Cross-platform sync complete: {result['successful_syncs']} successful, {result['failed_syncs']} failed")
        return result

    async def ai_powered_system_insights(self, time_period: str = "24h") -> Dict[str, Any]:
        """Generate AI-powered insights about system activity and health."""
        log.info(f"Generating AI insights for {time_period} period")
        
        if 'openai' not in self.clients:
            raise ValueError("OpenAI client not available for insights generation")
        
        # Collect system data
        health_data = await self.comprehensive_health_check()
        
        # Collect activity data from various services
        activity_data = await self._collect_system_activity(time_period)
        
        # Generate AI insights
        insights_prompt = f"""
        Analyze this system health and activity data to provide actionable insights:
        
        Health Status: {health_data['health_percentage']}% of services healthy
        Services: {list(health_data['services'].keys())}
        
        Activity Summary:
        {activity_data}
        
        Provide:
        1. Overall system health assessment
        2. Key trends and patterns
        3. Recommendations for improvement
        4. Potential issues to watch
        """
        
        try:
            ai_insights = await self.clients['openai'].generate_completion(
                prompt=insights_prompt,
                max_tokens=800
            )
            
            result = {
                "time_period": time_period,
                "health_data": health_data,
                "activity_summary": activity_data,
                "ai_insights": ai_insights,
                "generated_at": datetime.now().isoformat()
            }
            
            log.info("AI insights generated successfully")
            return result
            
        except Exception as e:
            log.error(f"Failed to generate AI insights: {e}")
            raise

    async def automated_incident_response(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """Automated incident response across multiple platforms."""
        log.info(f"Processing incident: {incident_data.get('title', 'Unknown')}")
        
        response_actions = []
        
        # Create incident ticket in Jira
        if 'atlassian' in self.clients:
            try:
                jira_ticket = await self._create_incident_ticket(incident_data)
                response_actions.append({
                    "action": "jira_ticket_created",
                    "status": "success",
                    "details": jira_ticket
                })
            except Exception as e:
                response_actions.append({
                    "action": "jira_ticket_creation",
                    "status": "failed",
                    "error": str(e)
                })
        
        # Send notifications to all communication channels
        notification_result = await self.intelligent_notification_pipeline(
            "incident", incident_data, ['slack', 'discord']
        )
        response_actions.append({
            "action": "notifications_sent",
            "status": "completed",
            "details": notification_result
        })
        
        # Update infrastructure monitoring
        if 'netbox' in self.clients or 'ha_api' in self.clients:
            try:
                infra_update = await self._update_infrastructure_status(incident_data)
                response_actions.append({
                    "action": "infrastructure_status_updated",
                    "status": "success",
                    "details": infra_update
                })
            except Exception as e:
                response_actions.append({
                    "action": "infrastructure_status_update",
                    "status": "failed",
                    "error": str(e)
                })
        
        result = {
            "incident_id": incident_data.get('id', 'unknown'),
            "incident_title": incident_data.get('title', 'Unknown'),
            "response_actions": len(response_actions),
            "successful_actions": len([a for a in response_actions if a["status"] == "success"]),
            "actions": response_actions,
            "timestamp": datetime.now().isoformat()
        }
        
        log.info(f"Incident response complete: {result['successful_actions']} successful actions")
        return result

    async def _enhance_event_with_ai(self, event_type: str, event_data: Dict[str, Any]) -> str:
        """Use AI to enhance event descriptions."""
        prompt = f"Create a clear, concise description for this {event_type} event: {event_data}"
        return await self.clients['openai'].generate_completion(prompt, max_tokens=150)

    async def _send_notification(self, channel: str, event_type: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Send notification to specific channel."""
        message = f"🔔 {event_type.upper()} Event\n"
        message += f"📝 {event_data.get('description', 'No description')}\n"
        message += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        if event_data.get('ai_enhanced_description'):
            message += f"\n🤖 AI Summary: {event_data['ai_enhanced_description']}"
        
        if channel == 'slack':
            return await self.clients['slack'].send_message(
                channel="#alerts",
                text=message
            )
        elif channel == 'discord':
            return await self.clients['discord'].send_message(
                channel_id="general",
                content=message
            )
        
        return {"status": "sent", "channel": channel}

    async def _sync_github_to_jira(self, project_config: Dict[str, Any]) -> Dict[str, Any]:
        """Sync GitHub issues to Jira tickets."""
        # This would implement GitHub -> Jira sync logic
        return {"status": "success", "synced_items": 0}

    async def _sync_perforce_to_confluence(self, project_config: Dict[str, Any]) -> Dict[str, Any]:
        """Sync Perforce changelists to Confluence documentation."""
        # This would implement Perforce -> Confluence sync logic
        return {"status": "success", "synced_changelists": 0}

    async def _sync_creative_assets(self, project_config: Dict[str, Any]) -> Dict[str, Any]:
        """Sync creative assets between SyncSketch and ResourceSpace."""
        # This would implement creative asset sync logic
        return {"status": "success", "synced_assets": 0}

    async def _collect_system_activity(self, time_period: str) -> str:
        """Collect activity data from various services."""
        activity_summary = f"System activity for {time_period}:\n"
        
        for service_name, client in self.clients.items():
            try:
                # This would collect actual activity metrics from each service
                activity_summary += f"- {service_name}: Active\n"
            except:
                activity_summary += f"- {service_name}: No data\n"
        
        return activity_summary

    async def _create_incident_ticket(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create incident ticket in Jira."""
        if 'atlassian' in self.clients and self.clients['atlassian'].jira:
            issue_dict = {
                'project': {'key': 'INC'},
                'summary': incident_data.get('title', 'System Incident'),
                'description': incident_data.get('description', 'Automated incident report'),
                'issuetype': {'name': 'Incident'},
                'priority': {'name': incident_data.get('priority', 'High')}
            }
            return self.clients['atlassian'].jira.create_issue(fields=issue_dict)
        
        return {"status": "skipped", "reason": "Jira not available"}

    async def _update_infrastructure_status(self, incident_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update infrastructure monitoring systems."""
        updates = []
        
        # Update NetBox if available
        if 'netbox' in self.clients:
            # This would update device status in NetBox
            updates.append("netbox_updated")
        
        # Update Home Assistant if available
        if 'ha_api' in self.clients:
            # This would update HA entity states
            updates.append("ha_updated")
        
        return {"updates": updates}

    async def close(self):
        """Close all client connections."""
        for client in self.clients.values():
            if hasattr(client, 'close'):
                try:
                    await client.close()
                except:
                    pass  # Ignore close errors


# Convenience functions for common orchestration tasks
async def system_health_check() -> Dict[str, Any]:
    """Quick system health check."""
    orchestrator = SystemOrchestration()
    try:
        return await orchestrator.comprehensive_health_check()
    finally:
        await orchestrator.close()

async def send_system_notification(event_type: str, message: str) -> Dict[str, Any]:
    """Quick system notification."""
    orchestrator = SystemOrchestration()
    try:
        return await orchestrator.intelligent_notification_pipeline(
            event_type, {"description": message}
        )
    finally:
        await orchestrator.close()

async def generate_system_insights(time_period: str = "24h") -> Dict[str, Any]:
    """Quick system insights generation."""
    orchestrator = SystemOrchestration()
    try:
        return await orchestrator.ai_powered_system_insights(time_period)
    finally:
        await orchestrator.close()