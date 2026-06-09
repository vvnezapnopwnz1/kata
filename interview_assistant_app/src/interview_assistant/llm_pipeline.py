import vertexai
from vertexai.generative_models import GenerativeModel

# Initialize vertex ai with default credentials
# vertexai.init() is expected to be called in main.py or uses ADC

SYSTEM_PROMPT = """You are an invisible teleprompter for an interviewee.
Given the transcription of the interview question, provide a two-part response.
Format your output EXACTLY as follows:

**TL;DR:** [One concise sentence summarizing the core answer]

**Script:** [A conversational, first-person response ("I would approach this by...", "The main difference is...") designed to be read aloud naturally.]
"""

def generate_interview_response(question_text: str, project_id: str = None, location: str = "global") -> tuple[str, str]:
    if project_id:
        vertexai.init(project=project_id, location=location)
        
    model = GenerativeModel("gemini-2.5-flash", system_instruction=SYSTEM_PROMPT)
    
    response = model.generate_content(question_text)
    text = response.text.strip()
    
    # Parse the response
    tldr = ""
    script = ""
    
    if "**TL;DR:**" in text and "**Script:**" in text:
        parts = text.split("**Script:**")
        tldr = parts[0].strip()
        script = "**Script:**\n" + parts[1].strip()
    else:
        # Fallback if format isn't strictly followed
        tldr = "**TL;DR:** Could not parse strictly."
        script = f"**Script:**\n{text}"
        
    return tldr, script
