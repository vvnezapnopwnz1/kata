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
