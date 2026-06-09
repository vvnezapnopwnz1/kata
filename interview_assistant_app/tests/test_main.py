from unittest.mock import MagicMock
import numpy as np
from src.interview_assistant.main import Controller

def test_controller_initialization(mocker):
    # Mock WhisperModel to prevent loading real model
    mocker.patch("src.interview_assistant.main.WhisperModel")
    
    controller = Controller()
    assert controller.is_recording_context == False
    assert controller.current_transcript == ""

def test_parse_incremental(mocker):
    # Mock WhisperModel to prevent loading real model
    mocker.patch("src.interview_assistant.main.WhisperModel")
    controller = Controller()
    
    # Test case 1: Empty text
    tldr, script = controller._parse_incremental("")
    assert tldr == "**TL;DR:**"
    assert script == "Waiting for script..."
    
    # Test case 2: Incomplete TL;DR tag
    tldr, script = controller._parse_incremental("**TL;D")
    assert tldr == "**TL;DR:**"
    assert script == "Waiting for script..."
    
    # Test case 3: TL;DR tag with content
    tldr, script = controller._parse_incremental("**TL;DR:** Hello world")
    assert tldr == "**TL;DR:** Hello world"
    assert script == "Waiting for script..."
    
    # Test case 4: Transition to script
    tldr, script = controller._parse_incremental("**TL;DR:** Hello world\n\n**Script:**")
    assert tldr == "**TL;DR:** Hello world"
    assert script == "**Script:**\n"
    
    # Test case 5: Full script streaming
    tldr, script = controller._parse_incremental("**TL;DR:** Hello world\n\n**Script:** I would approach this")
    assert tldr == "**TL;DR:** Hello world"
    assert script == "**Script:**\nI would approach this"

def test_diarize_and_merge(mocker):
    class MockSegment:
        def __init__(self, start, text):
            self.start = start
            self.text = text

    # Mock WhisperModel
    mocker.patch("src.interview_assistant.main.WhisperModel")
    
    controller = Controller()
    
    candidate_segs = [
        MockSegment(5.0, " I am the candidate. "),
        MockSegment(15.0, " That makes sense. ")
    ]
    interviewer_segs = [
        MockSegment(1.0, " What is Go? "),
        MockSegment(10.0, " Right. And what about concurrency? ")
    ]
    
    # Mock transcribe call
    controller.model.transcribe = MagicMock(side_effect=[
        (candidate_segs, None),
        (interviewer_segs, None)
    ])
    
    dummy_mic = np.zeros(16000)
    dummy_sys = np.zeros(16000)
    
    transcript = controller._diarize_and_merge(dummy_mic, dummy_sys)
    
    expected = (
        "[Interviewer]: What is Go?\n"
        "[Candidate]: I am the candidate.\n"
        "[Interviewer]: Right. And what about concurrency?\n"
        "[Candidate]: That makes sense."
    )
    
    assert transcript == expected

