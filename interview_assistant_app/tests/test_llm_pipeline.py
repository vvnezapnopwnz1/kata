import pytest
import argparse
from unittest.mock import MagicMock, patch
from src.interview_assistant.llm_pipeline import LLMPipeline

@pytest.fixture
def base_args():
    return argparse.Namespace(
        backend="direct",
        project_id="test-project",
        location="global",
        data_store_id="test-ds",
        agent_id="test-agent",
        app_id="test-app",
        version_id="test-version",
        deployment_id="test-deploy",
        session_id="test-session"
    )

def test_llm_pipeline_direct(base_args, mocker):
    base_args.backend = "direct"
    pipeline = LLMPipeline(base_args)
    
    # Mock litellm.completion
    mock_chunk = mocker.Mock()
    mock_chunk.choices = [mocker.Mock()]
    mock_chunk.choices[0].delta.content = "Streaming chunk"
    
    mocker.patch("litellm.completion", return_value=[mock_chunk])
    
    generator = pipeline.generate_response("hello")
    chunks = list(generator)
    
    assert len(chunks) == 1
    assert chunks[0] == "Streaming chunk"

def test_llm_pipeline_search(base_args, mocker):
    base_args.backend = "search"
    pipeline = LLMPipeline(base_args)
    
    # Mock SearchServiceClient
    mock_client_class = mocker.patch("src.interview_assistant.pipelines.search_rag_pipeline.discoveryengine.SearchServiceClient")
    mock_client = mock_client_class.return_value
    
    # Setup mock results
    mock_result = mocker.Mock()
    mock_result.document.derived_struct_data = {
        "extractive_segments": [{"content": "Extracted context snippet"}]
    }
    
    mock_response = mocker.Mock()
    mock_response.results = [mock_result]
    mock_client.search.return_value = mock_response
    mock_client.serving_config_path.return_value = "serving-config-path"
    
    # Mock litellm.completion
    mock_chunk = mocker.Mock()
    mock_chunk.choices = [mocker.Mock()]
    mock_chunk.choices[0].delta.content = "Answer with context"
    mocker.patch("litellm.completion", return_value=[mock_chunk])
    
    generator = pipeline.generate_response("what is go?")
    chunks = list(generator)
    
    assert len(chunks) == 1
    assert chunks[0] == "Answer with context"
    mock_client.search.assert_called_once()

def test_llm_pipeline_agent_builder(base_args, mocker):
    base_args.backend = "agent-builder"
    pipeline = LLMPipeline(base_args)
    
    # Mock token retrieval on the sub-pipeline
    mocker.patch.object(pipeline.pipeline, "get_google_access_token", return_value="mock-token")
    
    # Mock requests.post with stream response
    mock_response = mocker.Mock()
    mock_response.iter_content.return_value = [
        b'[\n',
        b'  {\n    "outputs": [\n      {\n        "text": "Agent response turn 1"\n      }\n    ]\n  }\n',
        b']'
    ]
    mocker.patch("requests.post", return_value=mock_response)
    
    generator = pipeline.generate_response("hi")
    chunks = list(generator)
    
    assert len(chunks) == 1
    assert chunks[0] == "Agent response turn 1"

def test_llm_pipeline_dialogflow(base_args, mocker):
    base_args.backend = "dialogflow"
    base_args.agent_id = "test-agent-id"
    pipeline = LLMPipeline(base_args)
    
    # Mock token retrieval on the sub-pipeline
    mocker.patch.object(pipeline.pipeline, "get_google_access_token", return_value="mock-token")
    
    # Mock requests.post
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "queryResult": {
            "responseMessages": [
                {"text": {"text": ["Dialogflow CX response text"]}}
            ]
        }
    }
    mocker.patch("requests.post", return_value=mock_response)
    
    generator = pipeline.generate_response("hello")
    chunks = list(generator)
    
    assert len(chunks) == 1
    assert chunks[0] == "Dialogflow CX response text"
