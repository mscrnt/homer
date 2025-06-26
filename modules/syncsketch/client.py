import os
import requests
import aiohttp
import asyncio
from pathlib import Path
from typing import Dict, Any, List, Optional
from homer.utils.logger import get_module_logger

log = get_module_logger("syncsketch.client")

class SyncSketchClient:
    def __init__(self, api_key: str = None, workspace: str = None, base_url: str = None):
        self.api_key = api_key or os.getenv("SYNCSKETCH_API_KEY")
        self.workspace = workspace or os.getenv("SYNCSKETCH_WORKSPACE")
        self.base_url = base_url or os.getenv("SYNCSKETCH_BASE_URL", "https://www.syncsketch.com/api/v1")
        
        if not self.api_key:
            raise ValueError("SYNCSKETCH_API_KEY is required")
        
        self.headers = {
            "Authorization": f"apikey {self.api_key}",
        }
        self.session = None
    
    async def _get_session(self):
        """Get or create aiohttp session"""
        if not self.session:
            self.session = aiohttp.ClientSession(headers=self.headers)
        return self.session
    
    async def close(self):
        """Close the session"""
        if self.session:
            await self.session.close()
            self.session = None

    async def upload_media(self, file_path: str, project_id: int, name: str = None, noConvertFlag: bool = False) -> Dict[str, Any]:
        """Upload media file to SyncSketch project."""
        session = await self._get_session()
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        try:
            url = f"{self.base_url}/person/upload/{project_id}/"
            
            # Prepare multipart form data
            data = aiohttp.FormData()
            data.add_field('name', name or file_path.stem)
            data.add_field('noConvertFlag', str(noConvertFlag).lower())
            data.add_field('file', 
                          file_path.open('rb'), 
                          filename=file_path.name, 
                          content_type='application/octet-stream')
            
            log.info(f"Uploading {file_path.name} to project {project_id}")
            
            async with session.post(url, data=data) as response:
                if response.status == 200:
                    result = await response.json()
                    log.info(f"Successfully uploaded media: {result.get('id')}")
                    return result
                else:
                    error_text = await response.text()
                    raise Exception(f"Upload failed with status {response.status}: {error_text}")
                    
        except Exception as e:
            log.error(f"Failed to upload media: {e}")
            raise

    async def get_projects(self) -> List[Dict[str, Any]]:
        """Get list of projects accessible to the user."""
        session = await self._get_session()
        
        try:
            url = f"{self.base_url}/person/projects/"
            
            async with session.get(url) as response:
                if response.status == 200:
                    projects = await response.json()
                    log.info(f"Retrieved {len(projects.get('objects', []))} projects")
                    return projects.get('objects', [])
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to get projects: {response.status} - {error_text}")
                    
        except Exception as e:
            log.error(f"Failed to get projects: {e}")
            raise

    async def get_project(self, project_id: int) -> Dict[str, Any]:
        """Get specific project details."""
        session = await self._get_session()
        
        try:
            url = f"{self.base_url}/person/projects/{project_id}/"
            
            async with session.get(url) as response:
                if response.status == 200:
                    project = await response.json()
                    log.info(f"Retrieved project: {project.get('name', project_id)}")
                    return project
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to get project {project_id}: {response.status} - {error_text}")
                    
        except Exception as e:
            log.error(f"Failed to get project {project_id}: {e}")
            raise

    async def get_reviews(self, project_id: int) -> List[Dict[str, Any]]:
        """Get reviews for a project."""
        session = await self._get_session()
        
        try:
            url = f"{self.base_url}/person/projects/{project_id}/reviews/"
            
            async with session.get(url) as response:
                if response.status == 200:
                    reviews = await response.json()
                    log.info(f"Retrieved {len(reviews.get('objects', []))} reviews for project {project_id}")
                    return reviews.get('objects', [])
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to get reviews: {response.status} - {error_text}")
                    
        except Exception as e:
            log.error(f"Failed to get reviews for project {project_id}: {e}")
            raise

    async def create_review(self, project_id: int, name: str, description: str = "") -> Dict[str, Any]:
        """Create a new review in a project."""
        session = await self._get_session()
        
        try:
            url = f"{self.base_url}/person/projects/{project_id}/reviews/"
            
            payload = {
                "name": name,
                "description": description
            }
            
            async with session.post(url, json=payload) as response:
                if response.status == 201:
                    review = await response.json()
                    log.info(f"Created review '{name}' with ID: {review.get('id')}")
                    return review
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to create review: {response.status} - {error_text}")
                    
        except Exception as e:
            log.error(f"Failed to create review '{name}': {e}")
            raise

    async def get_items(self, project_id: int, review_id: int = None) -> List[Dict[str, Any]]:
        """Get items (media) from a project or review."""
        session = await self._get_session()
        
        try:
            if review_id:
                url = f"{self.base_url}/person/projects/{project_id}/reviews/{review_id}/items/"
            else:
                url = f"{self.base_url}/person/projects/{project_id}/items/"
            
            async with session.get(url) as response:
                if response.status == 200:
                    items = await response.json()
                    log.info(f"Retrieved {len(items.get('objects', []))} items")
                    return items.get('objects', [])
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to get items: {response.status} - {error_text}")
                    
        except Exception as e:
            log.error(f"Failed to get items: {e}")
            raise

    async def add_note(self, item_id: int, text: str, frame: int = 0) -> Dict[str, Any]:
        """Add a note/comment to a media item."""
        session = await self._get_session()
        
        try:
            url = f"{self.base_url}/person/greasepencil/"
            
            payload = {
                "item": item_id,
                "text": text,
                "frame": frame
            }
            
            async with session.post(url, json=payload) as response:
                if response.status == 201:
                    note = await response.json()
                    log.info(f"Added note to item {item_id}")
                    return note
                else:
                    error_text = await response.text()
                    raise Exception(f"Failed to add note: {response.status} - {error_text}")
                    
        except Exception as e:
            log.error(f"Failed to add note to item {item_id}: {e}")
            raise

    async def health_check(self) -> Dict[str, Any]:
        """Check API connectivity and authentication."""
        try:
            projects = await self.get_projects()
            return {
                "status": "ok",
                "authenticated": True,
                "projects_count": len(projects)
            }
        except Exception as e:
            return {
                "status": "error", 
                "authenticated": False,
                "error": str(e)
            }

def get_syncsketch_client(api_key: str = None, workspace: str = None, base_url: str = None) -> SyncSketchClient:
    """Get a configured SyncSketch client instance."""
    return SyncSketchClient(api_key, workspace, base_url)