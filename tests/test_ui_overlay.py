import pytest
from PyQt6.QtCore import Qt
from src.interview_assistant.ui_overlay import OverlayWindow

def test_overlay_window_initial_state(qtbot):
    window = OverlayWindow()
    qtbot.addWidget(window)
    
    # Check flags for frameless and always on top
    assert window.windowFlags() & Qt.WindowType.FramelessWindowHint
    assert window.windowFlags() & Qt.WindowType.WindowStaysOnTopHint
    
    # Check initial text
    assert window.tldr_label.text() == "Ready"
    assert window.script_label.text() == "Waiting for hotkey..."
