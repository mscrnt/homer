"""
Creative workflow automation that combines Slack notifications with SyncSketch operations.
"""
import asyncio
from typing import Dict, Any, List, Optional
from homer.utils.logger import get_module_logger
from homer.modules.slack.client import SlackClient
from homer.modules.syncsketch.client import SyncSketchClient

log = get_module_logger("stack.slack_syncsketch.creative_workflow")

class CreativeWorkflowAutomation:
    """Automates creative review workflows between SyncSketch and Slack."""
    
    def __init__(self):
        self.slack_client = SlackClient()
        self.syncsketch_client = SyncSketchClient()
    
    async def close(self):
        """Close all client connections."""
        await self.syncsketch_client.close()
    
    async def notify_new_upload(self, project_id: int, media_path: str, 
                               channel: str = "#creative", custom_message: str = None) -> Dict[str, Any]:
        """Upload media to SyncSketch and notify team via Slack."""
        try:
            # Upload to SyncSketch
            log.info(f"Uploading {media_path} to SyncSketch project {project_id}")
            upload_result = await self.syncsketch_client.upload_media(
                file_path=media_path,
                project_id=project_id
            )
            
            # Get project details for better messaging
            project = await self.syncsketch_client.get_project(project_id)
            project_name = project.get('name', f'Project {project_id}')
            
            # Create notification message
            if custom_message:
                message = custom_message
            else:
                media_name = upload_result.get('name', 'New Media')
                message = f"🎬 New upload to *{project_name}*: {media_name}\n"
                message += f"📁 Ready for review in SyncSketch"
                
                if 'url' in upload_result:
                    message += f" - <{upload_result['url']}|View>"
            
            # Send Slack notification
            slack_result = await self.slack_client.send_message(
                channel=channel,
                text=message
            )
            
            log.info(f"Successfully uploaded and notified team")
            
            return {
                "status": "success",
                "upload": upload_result,
                "notification": slack_result,
                "project_name": project_name
            }
            
        except Exception as e:
            log.error(f"Failed to upload and notify: {e}")
            raise

    async def notify_review_created(self, project_id: int, review_name: str, 
                                   description: str = "", channel: str = "#creative") -> Dict[str, Any]:
        """Create a SyncSketch review and notify team via Slack."""
        try:
            # Create review in SyncSketch
            log.info(f"Creating review '{review_name}' in project {project_id}")
            review = await self.syncsketch_client.create_review(
                project_id=project_id,
                name=review_name,
                description=description
            )
            
            # Get project details
            project = await self.syncsketch_client.get_project(project_id)
            project_name = project.get('name', f'Project {project_id}')
            
            # Create notification message
            message = f"📋 New review created in *{project_name}*: *{review_name}*\n"
            if description:
                message += f"📝 {description}\n"
            message += f"👥 Please check SyncSketch for review tasks"
            
            if 'url' in review:
                message += f" - <{review['url']}|Open Review>"
            
            # Send Slack notification
            slack_result = await self.slack_client.send_message(
                channel=channel,
                text=message
            )
            
            log.info(f"Successfully created review and notified team")
            
            return {
                "status": "success",
                "review": review,
                "notification": slack_result,
                "project_name": project_name
            }
            
        except Exception as e:
            log.error(f"Failed to create review and notify: {e}")
            raise

    async def daily_project_summary(self, project_ids: List[int], 
                                   channel: str = "#daily-updates") -> Dict[str, Any]:
        """Generate and send daily project summary to Slack."""
        try:
            summaries = []
            
            for project_id in project_ids:
                # Get project details
                project = await self.syncsketch_client.get_project(project_id)
                project_name = project.get('name', f'Project {project_id}')
                
                # Get recent items and reviews
                items = await self.syncsketch_client.get_items(project_id)
                reviews = await self.syncsketch_client.get_reviews(project_id)
                
                # Build summary
                summary = f"*{project_name}*:\n"
                summary += f"   • {len(items)} media items\n"
                summary += f"   • {len(reviews)} active reviews\n"
                
                summaries.append(summary)
            
            # Create full message
            message = "📊 *Daily Creative Summary*\n\n"
            message += "\n".join(summaries)
            message += f"\n🎨 Keep up the great work team!"
            
            # Send to Slack
            slack_result = await self.slack_client.send_message(
                channel=channel,
                text=message
            )
            
            log.info(f"Sent daily summary for {len(project_ids)} projects")
            
            return {
                "status": "success",
                "projects_summarized": len(project_ids),
                "notification": slack_result
            }
            
        except Exception as e:
            log.error(f"Failed to generate daily summary: {e}")
            raise

    async def review_completion_workflow(self, project_id: int, review_id: int, 
                                       channel: str = "#creative") -> Dict[str, Any]:
        """Handle review completion notifications and next steps."""
        try:
            # Get project and review details
            project = await self.syncsketch_client.get_project(project_id)
            reviews = await self.syncsketch_client.get_reviews(project_id)
            
            # Find the specific review
            review = None
            for r in reviews:
                if r.get('id') == review_id:
                    review = r
                    break
            
            if not review:
                raise ValueError(f"Review {review_id} not found in project {project_id}")
            
            project_name = project.get('name', f'Project {project_id}')
            review_name = review.get('name', f'Review {review_id}')
            
            # Get review items for final count
            items = await self.syncsketch_client.get_items(project_id, review_id)
            
            # Create completion message
            message = f"✅ *Review Completed*: {review_name}\n"
            message += f"📁 Project: {project_name}\n"
            message += f"🎬 {len(items)} items reviewed\n"
            message += f"🎉 Great work team! Ready for next phase."
            
            # Send notification
            slack_result = await self.slack_client.send_message(
                channel=channel,
                text=message
            )
            
            log.info(f"Notified review completion for {review_name}")
            
            return {
                "status": "success",
                "review": review,
                "items_count": len(items),
                "notification": slack_result
            }
            
        except Exception as e:
            log.error(f"Failed to handle review completion: {e}")
            raise

    async def health_check(self) -> Dict[str, Any]:
        """Check connectivity to both Slack and SyncSketch."""
        results = {}
        
        try:
            slack_health = await self.slack_client.test_connection()
            results["slack"] = slack_health
        except Exception as e:
            results["slack"] = {"status": "error", "error": str(e)}
        
        try:
            syncsketch_health = await self.syncsketch_client.health_check()
            results["syncsketch"] = syncsketch_health
        except Exception as e:
            results["syncsketch"] = {"status": "error", "error": str(e)}
        
        # Overall status
        all_ok = all(r.get("status") == "ok" for r in results.values())
        results["overall"] = "ok" if all_ok else "degraded"
        
        return results


# Convenience functions for common workflows
async def upload_and_notify(media_path: str, project_id: int, channel: str = "#creative") -> Dict[str, Any]:
    """Quick function to upload media and notify team."""
    workflow = CreativeWorkflowAutomation()
    try:
        return await workflow.notify_new_upload(project_id, media_path, channel)
    finally:
        await workflow.close()

async def create_review_and_notify(project_id: int, review_name: str, 
                                 description: str = "", channel: str = "#creative") -> Dict[str, Any]:
    """Quick function to create review and notify team."""
    workflow = CreativeWorkflowAutomation()
    try:
        return await workflow.notify_review_created(project_id, review_name, description, channel)
    finally:
        await workflow.close()