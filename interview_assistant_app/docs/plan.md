# Real-time AI Interview Assistant Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a real-time AI assistant that acts as an invisible teleprompter during online interviews by capturing dual-stream audio, transcribing it, and displaying LLM-generated conversational answers in a transparent PyQt6 overlay triggered by hotkeys.

**Architecture:** The system runs three concurrent systems: a background audio ring buffer capturing from virtual cable and mic, a hotkey listener to slice the buffer and trigger the LLM pipeline, and a PyQt6 GUI running in the main thread with a transparent, frameless window to display the AI's response asynchronously.

**Tech Stack:** Python 3.11+, PyQt6, PyAudio, pynput, vertexai (Google Cloud), pytest.

---

### Task 1: Setup Project Structure and Dependencies

**Files:**
- Create: `requirements.txt`
- Create: `src/interview_assistant/__init__.py`
- Create: `tests/__init__.py`

- [ ] **Step 1: Create requirements.txt**

```text
PyQt6==6.7.0
PyAudio==0.2.14
pynput==1.7.6
vertexai==1.50.0
pytest==8.2.1
pytest-qt==4.4.0
pytest-mock==3.14.0
numpy==1.26.4
```

- [ ] **Step 2: Create project directories and init files**

```bash
mkdir -p src/interview_assistant
mkdir -p tests
touch src/interview_assistant/__init__.py
touch tests/__init__.py
```

- [ ] **Step 3: Commit**

```bash
git add requirements.txt src/ tests/
git commit -m "chore: setup project structure and dependencies"
```

### Task 2: Implement Audio Ring Buffer

**Files:**
- Create: `src/interview_assistant/audio_buffer.py`
- Create: `tests/test_audio_buffer.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_audio_buffer.py
import pytest
import numpy as np
from src.interview_assistant.audio_buffer import AudioRingBuffer

def test_audio_ring_buffer():
    buffer = AudioRingBuffer(max_seconds=5, sample_rate=16000, channels=2)
    # 1 second of data
    data1 = np.ones((16000, 2), dtype=np.float32)
    buffer.append(data1)
    
    assert buffer.get_length_seconds() == 1.0
    
    # Add 5 more seconds (total 6, should truncate to 5)
    data2 = np.zeros((16000 * 5, 2), dtype=np.float32)
    buffer.append(data2)
    
    assert buffer.get_length_seconds() == 5.0
    
    # Get last 2 seconds
    slice_data = buffer.get_last_seconds(2)
    assert slice_data.shape == (32000, 2)
    assert np.all(slice_data == 0) # Should be all zeros from data2
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_audio_buffer.py -v`
Expected: FAIL (ModuleNotFoundError)

- [ ] **Step 3: Write minimal implementation**

```python
# src/interview_assistant/audio_buffer.py
import numpy as np

class AudioRingBuffer:
    def __init__(self, max_seconds: int = 120, sample_rate: int = 16000, channels: int = 2):
        self.max_seconds = max_seconds
        self.sample_rate = sample_rate
        self.channels = channels
        self.max_samples = max_seconds * sample_rate
        self.buffer = np.zeros((0, channels), dtype=np.float32)

    def append(self, data: np.ndarray):
        if data.shape[1] != self.channels:
            raise ValueError(f"Expected {self.channels} channels, got {data.shape[1]}")
        
        self.buffer = np.vstack((self.buffer, data))
        
        if len(self.buffer) > self.max_samples:
            self.buffer = self.buffer[-self.max_samples:]

    def get_length_seconds(self) -> float:
        return len(self.buffer) / self.sample_rate

    def get_last_seconds(self, seconds: float) -> np.ndarray:
        samples_needed = int(seconds * self.sample_rate)
        return self.buffer[-samples_needed:]

    def clear(self):
        self.buffer = np.zeros((0, self.channels), dtype=np.float32)
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_audio_buffer.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/interview_assistant/audio_buffer.py tests/test_audio_buffer.py
git commit -m "feat: implement audio ring buffer using numpy"
```

### Task 3: Implement LLM Pipeline Interface (Vertex AI)

**Files:**
- Create: `src/interview_assistant/llm_pipeline.py`
- Create: `tests/test_llm_pipeline.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_llm_pipeline.py
import pytest
from src.interview_assistant.llm_pipeline import generate_interview_response

def test_generate_interview_response_format(mocker):
    # Mock the Vertex AI response
    mock_model = mocker.patch("vertexai.generative_models.GenerativeModel")
    mock_response = mocker.Mock()
    mock_response.text = "**TL;DR:** This is a summary.\n\n**Script:** I would say this is the script."
    mock_model.return_value.generate_content.return_value = mock_response

    tldr, script = generate_interview_response("Tell me about closures in JavaScript.")
    
    assert tldr == "**TL;DR:** This is a summary."
    assert script == "**Script:** I would say this is the script."
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_llm_pipeline.py -v`
Expected: FAIL

- [ ] **Step 3: Write minimal implementation**

```python
# src/interview_assistant/llm_pipeline.py
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

def generate_interview_response(question_text: str, project_id: str = None, location: str = "us-central1") -> tuple[str, str]:
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_llm_pipeline.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/interview_assistant/llm_pipeline.py tests/test_llm_pipeline.py
git commit -m "feat: implement vertex ai llm pipeline for response generation"
```

### Task 4: Implement the PyQt6 Transparent Overlay

**Files:**
- Create: `src/interview_assistant/ui_overlay.py`
- Create: `tests/test_ui_overlay.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_ui_overlay.py
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_ui_overlay.py -v`
Expected: FAIL

- [ ] **Step 3: Write minimal implementation**

```python
# src/interview_assistant/ui_overlay.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

class OverlayWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # Set window flags for overlay
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Layout
        self.layout = QVBoxLayout(self)
        
        # TL;DR Label (Highlighted)
        self.tldr_label = QLabel("Ready")
        self.tldr_label.setStyleSheet("color: #FFD700; font-size: 20px; font-weight: bold; background-color: rgba(0, 0, 0, 180); padding: 10px; border-radius: 5px;")
        self.tldr_label.setWordWrap(True)
        
        # Script Label
        self.script_label = QLabel("Waiting for hotkey...")
        self.script_label.setStyleSheet("color: #FFFFFF; font-size: 18px; background-color: rgba(0, 0, 0, 180); padding: 10px; border-radius: 5px;")
        self.script_label.setWordWrap(True)
        
        self.layout.addWidget(self.tldr_label)
        self.layout.addWidget(self.script_label)
        
        self.resize(800, 200)
        
    def update_text(self, tldr: str, script: str):
        self.tldr_label.setText(tldr)
        self.script_label.setText(script)

    def set_status(self, status: str):
        self.tldr_label.setText(f"Status: {status}")
        self.script_label.setText("")
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_ui_overlay.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/interview_assistant/ui_overlay.py tests/test_ui_overlay.py
git commit -m "feat: implement pyqt6 frameless transparent overlay"
```

### Task 5: Implement Hotkey Controller and Main Thread

**Files:**
- Create: `src/interview_assistant/main.py`
- Create: `tests/test_main.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/test_main.py
import pytest
from src.interview_assistant.main import Controller

def test_controller_initialization():
    controller = Controller()
    assert controller.is_recording_context == False
    assert controller.context_start_time == 0.0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_main.py -v`
Expected: FAIL

- [ ] **Step 3: Write minimal implementation**

```python
# src/interview_assistant/main.py
import sys
import time
import threading
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSignal, QObject
from pynput import keyboard
from src.interview_assistant.ui_overlay import OverlayWindow

class SignalEmitter(QObject):
    update_ui = pyqtSignal(str, str)
    update_status = pyqtSignal(str)

class Controller:
    def __init__(self):
        self.is_recording_context = False
        self.context_start_time = 0.0
        self.emitter = SignalEmitter()
        
    def on_press(self, key):
        try:
            if key == keyboard.Key.f8:
                self.handle_start_context()
            elif key == keyboard.Key.f9:
                self.handle_trigger_answer()
            elif key == keyboard.Key.f10:
                self.handle_clear()
        except AttributeError:
            pass

    def handle_start_context(self):
        self.is_recording_context = True
        self.context_start_time = time.time()
        self.emitter.update_status.emit("Recording Context (F9 to process, F10 to clear)")

    def handle_trigger_answer(self):
        if not self.is_recording_context:
            return
            
        self.is_recording_context = False
        self.emitter.update_status.emit("Processing via Gemini...")
        
        # In a real scenario, we slice the audio buffer here and pass to LLM pipeline.
        # For the controller structure, we simulate async processing.
        threading.Thread(target=self._mock_process, daemon=True).start()
        
    def handle_clear(self):
        self.is_recording_context = False
        self.emitter.update_status.emit("Ready (Press F8 to start)")

    def _mock_process(self):
        time.sleep(1) # simulate api call
        self.emitter.update_ui.emit("**TL;DR:** Dummy Response.", "**Script:** This is a dummy script.")

def main():
    app = QApplication(sys.argv)
    
    overlay = OverlayWindow()
    overlay.show()
    
    controller = Controller()
    controller.emitter.update_ui.connect(overlay.update_text)
    controller.emitter.update_status.connect(overlay.set_status)
    
    # Start keyboard listener
    listener = keyboard.Listener(on_press=controller.on_press)
    listener.start()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_main.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add src/interview_assistant/main.py tests/test_main.py
git commit -m "feat: implement main controller and hotkey listener"
```
