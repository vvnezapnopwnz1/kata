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
