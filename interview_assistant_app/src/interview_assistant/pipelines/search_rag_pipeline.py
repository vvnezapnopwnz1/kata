import logging
import litellm
from google.cloud import discoveryengine_v1 as discoveryengine

logger = logging.getLogger(__name__)

class SearchRAGPipeline:
    def __init__(self, args, system_prompt: str):
        self.system_prompt = system_prompt
        self.project_id = getattr(args, "project_id", "project-7d570aed-312f-4939-9a4")
        self.location = getattr(args, "location", "global")
        self.data_store_id = getattr(args, "data_store_id", "")
        
        if self.project_id:
            litellm.vertex_project = self.project_id
        if self.location:
            litellm.vertex_location = self.location

    def _get_search_context(self, query: str) -> str:
        """Queries Discovery Engine Search and builds context from extractive segments."""
        if not self.data_store_id:
            logger.warning("Search RAG selected, but data_store_id is empty!")
            return ""
            
        logger.info(f"Querying Search RAG for: '{query[:50]}...'")
        try:
            client = discoveryengine.SearchServiceClient()
            
            serving_config = client.serving_config_path(
                project=self.project_id,
                location="global",
                data_store=self.data_store_id,
                serving_config="default_search"
            )
            
            extractive_spec = discoveryengine.SearchRequest.ContentSearchSpec.ExtractiveContentSpec(
                max_extractive_segment_count=3,
                return_extractive_segment_score=True
            )
            content_search_spec = discoveryengine.SearchRequest.ContentSearchSpec(
                extractive_content_spec=extractive_spec
            )
            
            request = discoveryengine.SearchRequest(
                serving_config=serving_config,
                query=query,
                page_size=3,
                content_search_spec=content_search_spec
            )
            
            response = client.search(request)
            
            chunks = []
            for result in response.results:
                derived_data = result.document.derived_struct_data
                if "extractive_segments" in derived_data:
                    for segment in derived_data["extractive_segments"]:
                        content = segment.get("content")
                        if content:
                            chunks.append(content.strip())
                            
            if chunks:
                logger.info(f"Found {len(chunks)} relevant context segments.")
                return "\n\n---\n\n".join(chunks)
            else:
                logger.info("No relevant context segments found in Data Store.")
                return ""
                
        except Exception as e:
            logger.error(f"Search RAG query failed: {e}")
            return ""

    def generate_response(self, transcript: str):
        context = self._get_search_context(transcript)
        
        user_content = f"Interview Transcript:\n{transcript}"
        if context:
            user_content += f"\n\nUse this context from Candidate's cheat sheets to answer:\n{context}"
            logger.info("Injecting RAG context into prompt.")
        else:
            logger.info("No context injected, falling back to General Knowledge.")
            
        try:
            response = litellm.completion(
                model="vertex_ai/gemini-2.5-flash",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_content}
                ],
                temperature=0.3,
                stream=True
            )
            for chunk in response:
                chunk_text = chunk.choices[0].delta.content
                if chunk_text:
                    yield chunk_text
        except Exception as e:
            logger.error(f"Gemini Search RAG completion failed: {e}")
            yield f"**TL;DR:** Gemini API Error.\n\n**Script:**\nFailed to complete request: {str(e)}"
