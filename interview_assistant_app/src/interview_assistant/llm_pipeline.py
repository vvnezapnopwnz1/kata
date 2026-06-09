import logging

logger = logging.getLogger(__name__)

# System Prompt for Gemini completions
SYSTEM_PROMPT = """You are an invisible teleprompter for an interviewee (referred to as [Candidate]) interviewing for a Golang Developer (Middle/Middle+) position.
All questions must be answered strictly according to the specifications, runtime, and specifications of the Go (Golang) programming language.
Analyze the transcription of the technical interview conversation containing [Interviewer] and [Candidate] speaker tags.
Identify the last unanswered technical question asked by [Interviewer]. Ignore questions that [Candidate] has already answered correctly, unless the interviewer asked a follow-up.
Provide a two-part response. Format your output EXACTLY as follows:

**TL;DR:** [One concise sentence summarizing the core Go-specific answer to the last active question]

**Script:** [A conversational, first-person response ("I would approach this by...", "The main difference is...") designed to be read aloud naturally by the Candidate, using Go-specific terms.]
"""

class LLMPipeline:
    def __init__(self, args):
        self.backend = getattr(args, "backend", "direct")
        self.args = args
        self.pipeline = None
        
        logger.info(f"LLMPipeline routing initialized with backend: {self.backend}")
        
        if self.backend == "direct":
            from src.interview_assistant.pipelines.direct_pipeline import DirectPipeline
            self.pipeline = DirectPipeline(self.args, SYSTEM_PROMPT)
        elif self.backend == "dialogflow":
            from src.interview_assistant.pipelines.dialogflow_pipeline import DialogflowPipeline
            self.pipeline = DialogflowPipeline(self.args, SYSTEM_PROMPT)
        elif self.backend == "agent-builder":
            from src.interview_assistant.pipelines.playbook_agent_pipeline import PlaybookAgentPipeline
            self.pipeline = PlaybookAgentPipeline(self.args, SYSTEM_PROMPT)
        elif self.backend == "search":
            from src.interview_assistant.pipelines.search_rag_pipeline import SearchRAGPipeline
            self.pipeline = SearchRAGPipeline(self.args, SYSTEM_PROMPT)
        else:
            raise ValueError(f"Unknown LLM pipeline backend: {self.backend}")

    def generate_response(self, transcript: str):
        """Routes response generation to the active pipeline instance."""
        return self.pipeline.generate_response(transcript)
