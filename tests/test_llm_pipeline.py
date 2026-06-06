import pytest
from src.interview_assistant.llm_pipeline import generate_interview_response

def test_generate_interview_response_format(mocker):
    # Mock the Vertex AI response
    mock_model = mocker.patch("src.interview_assistant.llm_pipeline.GenerativeModel")
    mock_response = mocker.Mock()
    mock_response.text = "**TL;DR:** This is a summary.\n\n**Script:** I would say this is the script."
    mock_model.return_value.generate_content.return_value = mock_response

    tldr, script = generate_interview_response("Tell me about closures in JavaScript.")
    
    assert tldr == "**TL;DR:** This is a summary."
    assert script == "**Script:**\nI would say this is the script."
