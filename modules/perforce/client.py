import os
import subprocess
from typing import List, Dict, Any
from homer.utils.logger import get_module_logger

log = get_module_logger("perforce.client")

class PerforceClient:
    def __init__(self, port: str = None, user: str = None, client: str = None, password: str = None):
        self.port = port or os.getenv("P4PORT")
        self.user = user or os.getenv("P4USER")
        self.client = client or os.getenv("P4CLIENT")
        self.password = password or os.getenv("P4PASSWD")
        
        if not self.port or not self.user:
            raise ValueError("P4PORT and P4USER are required")
        
        self.env = os.environ.copy()
        self.env.update({
            "P4PORT": self.port,
            "P4USER": self.user,
        })
        
        if self.client:
            self.env["P4CLIENT"] = self.client
        if self.password:
            self.env["P4PASSWD"] = self.password

    def _run_command(self, args: List[str]) -> str:
        """Run a p4 command and return the output."""
        try:
            cmd = ["p4"] + args
            result = subprocess.run(
                cmd,
                env=self.env,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            log.error(f"Perforce command failed: {' '.join(cmd)}")
            log.error(f"Error: {e.stderr}")
            raise RuntimeError(f"P4 command failed: {e.stderr}")

    async def get_changelist(self, changelist_id: str) -> Dict[str, Any]:
        """Get details of a specific changelist."""
        try:
            # Get changelist description
            output = self._run_command(["describe", "-s", changelist_id])
            
            lines = output.split('\n')
            change_info = {}
            
            # Parse the changelist info
            for line in lines:
                if line.startswith("Change"):
                    parts = line.split()
                    change_info["id"] = parts[1]
                    change_info["user"] = parts[3]
                    change_info["date"] = " ".join(parts[5:8])
                elif line.startswith("\t") and "description" not in change_info:
                    change_info["description"] = line.strip()
            
            # Get affected files
            files_output = self._run_command(["describe", changelist_id])
            files = []
            in_files_section = False
            
            for line in files_output.split('\n'):
                if line.startswith("Affected files"):
                    in_files_section = True
                    continue
                elif in_files_section and line.startswith("..."):
                    file_info = line.split()
                    if len(file_info) >= 3:
                        files.append({
                            "path": file_info[1],
                            "action": file_info[2]
                        })
            
            change_info["files"] = files
            log.info(f"Retrieved changelist {changelist_id} with {len(files)} files")
            return change_info
            
        except Exception as e:
            log.error(f"Failed to get changelist {changelist_id}: {e}")
            raise

    async def list_changelists(self, user: str = None, max_results: int = 20) -> List[Dict[str, Any]]:
        """List recent changelists."""
        try:
            args = ["changes", "-m", str(max_results)]
            if user:
                args.extend(["-u", user])
            
            output = self._run_command(args)
            changelists = []
            
            for line in output.split('\n'):
                if line.startswith("Change"):
                    parts = line.split()
                    if len(parts) >= 7:
                        changelists.append({
                            "id": parts[1],
                            "user": parts[3],
                            "date": " ".join(parts[5:8]),
                            "description": " ".join(parts[8:]) if len(parts) > 8 else ""
                        })
            
            log.info(f"Listed {len(changelists)} changelists")
            return changelists
            
        except Exception as e:
            log.error(f"Failed to list changelists: {e}")
            raise

    async def get_streams(self) -> List[Dict[str, Any]]:
        """List available streams."""
        try:
            output = self._run_command(["streams"])
            streams = []
            
            for line in output.split('\n'):
                if line.startswith("Stream"):
                    parts = line.split()
                    if len(parts) >= 4:
                        streams.append({
                            "name": parts[1],
                            "type": parts[2],
                            "parent": parts[3] if len(parts) > 3 else None,
                            "description": " ".join(parts[4:]) if len(parts) > 4 else ""
                        })
            
            log.info(f"Found {len(streams)} streams")
            return streams
            
        except Exception as e:
            log.error(f"Failed to get streams: {e}")
            raise

    async def sync_files(self, file_spec: str = "...") -> str:
        """Sync files from the depot."""
        try:
            output = self._run_command(["sync", file_spec])
            log.info(f"Synced files: {file_spec}")
            return output
            
        except Exception as e:
            log.error(f"Failed to sync files {file_spec}: {e}")
            raise

    async def get_workspace_info(self) -> Dict[str, Any]:
        """Get information about the current workspace/client."""
        try:
            output = self._run_command(["info"])
            info = {}
            
            for line in output.split('\n'):
                if ": " in line:
                    key, value = line.split(": ", 1)
                    info[key.lower().replace(" ", "_")] = value
            
            log.info("Retrieved workspace info")
            return info
            
        except Exception as e:
            log.error(f"Failed to get workspace info: {e}")
            raise

def get_perforce_client(port: str = None, user: str = None, client: str = None, password: str = None) -> PerforceClient:
    """Get a configured Perforce client instance."""
    return PerforceClient(port, user, client, password)