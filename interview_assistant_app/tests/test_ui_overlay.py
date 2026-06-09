import pytest
from PyQt6.QtCore import Qt
from src.interview_assistant.ui_overlay import OverlayWindow, md_to_html, highlight_go_code

def test_overlay_window_initial_state(qtbot):
    window = OverlayWindow()
    qtbot.addWidget(window)
    
    # Check flags for frameless and always on top
    assert window.windowFlags() & Qt.WindowType.FramelessWindowHint
    assert window.windowFlags() & Qt.WindowType.WindowStaysOnTopHint
    
    # Check initial text
    assert window.tldr_label.text() == ""
    assert window.script_label.text() == "Waiting for interview question..."

def test_md_to_html_formatting():
    # Test bold tag
    html_text = md_to_html("**Hello**")
    assert "<b>Hello</b>" in html_text

    # Test headers
    html_text = md_to_html("### Header 3")
    assert "color: #A7F3D0" in html_text
    assert "Header 3" in html_text

    # Test Go code block highlight
    code_md = "```go\nvar m map[string]int\n```"
    html_text = md_to_html(code_md)
    assert "<pre" in html_text
    # Check keyword color wrapper (#F87171)
    assert "#F87171" in html_text
    # Check type color wrapper (#60A5FA)
    assert "#60A5FA" in html_text
