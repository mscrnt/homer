"""
GitHub API client for HOMER
"""
import os
from typing import Optional, Dict, Any, List
from github import Github
from homer.utils.logger import get_logger

logger = get_logger(__name__)


class GitHubClient:
    """GitHub API client wrapper"""
    
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.base_url = os.getenv("GITHUB_BASE_URL", "https://api.github.com")
        self._client = None
    
    @property
    def client(self) -> Optional[Github]:
        """Get GitHub client"""
        if not self._client and self.token:
            self._client = Github(
                login_or_token=self.token,
                base_url=self.base_url
            )
        return self._client
    
    def health_check(self) -> Dict[str, Any]:
        """Check connection health"""
        if not self.client:
            return {"status": "error", "error": "No token configured"}
        
        try:
            user = self.client.get_user()
            rate_limit = self.client.get_rate_limit()
            
            return {
                "status": "ok",
                "user": user.login,
                "rate_limit": {
                    "remaining": rate_limit.core.remaining,
                    "limit": rate_limit.core.limit,
                    "reset": rate_limit.core.reset.isoformat()
                }
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def get_repositories(self, org: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get repositories"""
        if not self.client:
            return []
        
        try:
            if org:
                repos = self.client.get_organization(org).get_repos()
            else:
                repos = self.client.get_user().get_repos()
            
            return [
                {
                    "name": repo.name,
                    "full_name": repo.full_name,
                    "description": repo.description,
                    "url": repo.html_url,
                    "private": repo.private,
                    "updated_at": repo.updated_at.isoformat() if repo.updated_at else None
                }
                for repo in repos
            ]
        except Exception as e:
            logger.error(f"Error fetching repositories: {e}")
            return []