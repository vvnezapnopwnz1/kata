import litellm
import logging

logger = logging.getLogger(__name__)

class DirectPipeline:
    def __init__(self, args, system_prompt: str):
        self.system_prompt = system_prompt
        if getattr(args, "project_id", None):
            litellm.vertex_project = args.project_id
        if getattr(args, "location", None):
            litellm.vertex_location = args.location
            
    def generate_response(self, transcript: str):
        try:
            response = litellm.completion(
                model="vertex_ai/gemini-2.5-flash",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Interview Transcript:\n{transcript}"}
                ],
                temperature=0.3,
                stream=True
            )
            for chunk in response:
                chunk_text = chunk.choices[0].delta.content
                if chunk_text:
                    yield chunk_text
        except Exception as e:
            logger.error(f"Gemini Direct completion failed: {e}")
            yield f"**TL;DR:** Gemini API Error.\n\n**Script:**\nFailed to complete request: {str(e)}"
