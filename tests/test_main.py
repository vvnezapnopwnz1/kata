import pytest
from src.interview_assistant.main import Controller

def test_controller_initialization():
    controller = Controller()
    assert controller.is_recording_context == False
    assert controller.context_start_time == 0.0
