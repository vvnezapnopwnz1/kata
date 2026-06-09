import logging
import requests
import subprocess
import google.auth
import google.auth.transport.requests

logger = logging.getLogger(__name__)

class DialogflowPipeline:
    def __init__(self, args, system_prompt: str):
        self.system_prompt = system_prompt
        self.project_id = getattr(args, "project_id", "project-7d570aed-312f-4939-9a4")
        self.location = getattr(args, "location", "eu")
        self.agent_id = getattr(args, "agent_id", "")
        self.session_id = getattr(args, "session_id", "YS-MSCoWgxO")

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
        if not self.agent_id:
            logger.warning("Dialogflow backend selected, but agent_id is empty!")
            yield "**TL;DR:** Dialogflow Configuration Error.\n\n**Script:**\nagent_id is required for Dialogflow backend. Pass --agent-id when starting."
            return
            
        logger.info(f"Calling Dialogflow CX DetectIntent for agent: {self.agent_id}")
        try:
            token = self.get_google_access_token()
            loc = self.location if self.location else "eu"
            url = f"https://{loc}-dialogflow.googleapis.com/v3/projects/{self.project_id}/locations/{loc}/agents/{self.agent_id}/sessions/{self.session_id}:detectIntent"
            
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "queryInput": {
                    "text": {
                        "text": transcript
                    },
                    "languageCode": "ru"
                }
            }
            
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            texts = []
            if "queryResult" in data and "responseMessages" in data["queryResult"]:
                for msg in data["queryResult"]["responseMessages"]:
                    if "text" in msg and "text" in msg["text"]:
                        texts.extend(msg["text"]["text"])
                        
            if not texts:
                yield "(No response text returned from Dialogflow CX)"
            else:
                yield "\n".join(texts)
                
        except Exception as e:
            logger.error(f"Dialogflow CX DetectIntent failed: {e}")
            yield f"**TL;DR:** Dialogflow CX API Error.\n\n**Script:**\nFailed to detect intent: {str(e)}"
