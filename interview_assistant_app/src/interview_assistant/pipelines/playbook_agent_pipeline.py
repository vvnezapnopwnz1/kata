import logging
import requests
import subprocess
import google.auth
import google.auth.transport.requests

logger = logging.getLogger(__name__)

class PlaybookAgentPipeline:
    def __init__(self, args, system_prompt: str):
        self.system_prompt = system_prompt
        self.project_id = getattr(args, "project_id", "project-7d570aed-312f-4939-9a4")
        self.location = getattr(args, "location", "eu")
        self.app_id = getattr(args, "app_id", "289f0946-709f-4a80-b7ff-e863aace6bde")
        self.version_id = getattr(args, "version_id", "2abf9851-9b93-405d-8420-2f73931def9a")
        self.deployment_id = getattr(args, "deployment_id", "17540902-bba7-4693-b05d-52c77970c493")
        self.session_id = getattr(args, "session_id", "aAOXjF")

    def get_google_access_token(self) -> str:
        """Obtains Google Access Token using ADC, fallback to gcloud subprocess."""
        try:
            credentials, project = google.auth.default()
            auth_req = google.auth.transport.requests.Request()
            credentials.refresh(auth_req)
            if credentials.token:
                return credentials.token
        except Exception as e:
            logger.debug(f"google.auth.default() failed: {e}")
            
        # Fallback to gcloud print-access-token subprocess
        try:
            token = subprocess.check_output(["gcloud", "auth", "print-access-token"], text=True).strip()
            return token
        except Exception as e:
            logger.error(f"Failed to run gcloud command to fetch token: {e}")
            raise RuntimeError(f"Failed to obtain Google Access Token: {e}")

    def generate_response(self, transcript: str):
        logger.info(f"Calling Playbook Agent API for session: {self.session_id}")
        try:
            token = self.get_google_access_token()
            loc = self.location if self.location else "eu"
            url = f"https://ces.googleapis.com/v1beta/projects/{self.project_id}/locations/{loc}/apps/{self.app_id}/sessions/{self.session_id}:streamRunSession"
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "config": {
                    "session": f"projects/{self.project_id}/locations/{loc}/apps/{self.app_id}/sessions/{self.session_id}",
                    "app_version": f"projects/{self.project_id}/locations/{loc}/apps/{self.app_id}/versions/{self.version_id}",
                    "deployment": f"projects/{self.project_id}/locations/{loc}/apps/{self.app_id}/deployments/{self.deployment_id}"
                },
                "inputs": [
                    {
                        "text": transcript
                    }
                ],
                "enable_text_streaming": True
            }
            
            response = requests.post(url, headers=headers, json=payload, stream=True)
            response.raise_for_status()
            
            import json
            buffer = []
            brace_count = 0
            in_string = False
            escape = False
            
            for chunk in response.iter_content(chunk_size=1024):
                if not chunk:
                    continue
                chunk_str = chunk.decode('utf-8', errors='ignore')
                for char in chunk_str:
                    if brace_count > 0:
                        buffer.append(char)
                    elif char == '{':
                        brace_count = 1
                        buffer = ['{']
                        in_string = False
                        escape = False
                        continue
                        
                    if brace_count > 0:
                        if escape:
                            escape = False
                        elif char == '\\':
                            escape = True
                        elif char == '"':
                            in_string = not in_string
                        elif not in_string:
                            if char == '{':
                                brace_count += 1
                            elif char == '}':
                                brace_count -= 1
                                if brace_count == 0:
                                    # Complete JSON object detected
                                    obj_str = "".join(buffer)
                                    try:
                                        obj = json.loads(obj_str)
                                        if "outputs" in obj:
                                            for out in obj["outputs"]:
                                                if "text" in out:
                                                    yield out["text"]
                                    except Exception as je:
                                        logger.debug(f"Failed to parse accumulated JSON chunk: {je} for data: {obj_str}")
                                    buffer = []
            
        except Exception as e:
            logger.error(f"Agent Builder Playbook execution failed: {e}")
            yield f"**TL;DR:** Agent Builder API Error.\n\n**Script:**\nFailed to invoke Conversational Agent: {str(e)}"
