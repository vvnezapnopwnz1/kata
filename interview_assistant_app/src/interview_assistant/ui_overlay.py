import re
import html
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QScrollArea, QSizePolicy, QPushButton, QApplication
from PyQt6.QtCore import Qt, QPoint, QPropertyAnimation, QRect
from PyQt6.QtGui import QColor, QScreen
from PyQt6.QtWidgets import QGraphicsDropShadowEffect

def highlight_go_code(code: str) -> str:
    # Escape HTML first
    code = html.escape(code)
    
    # Token dictionary to store placeholders for strings and comments
    # to protect them from keyword highlighting.
    tokens = {}
    token_counter = 0
    
    def add_token(text, style):
        nonlocal token_counter
        placeholder = f"___TOKEN_PLACEHOLDER_{token_counter}___"
        tokens[placeholder] = f'<span style="{style}">{text}</span>'
        token_counter += 1
        return placeholder

    # 1. Capture and replace comments
    # Single-line comment
    def comment_repl(match):
        return add_token(match.group(1), "color: #6B7280; font-style: italic;")
    code = re.sub(r'(//.*)', comment_repl, code)
    
    # Multi-line comment
    def ml_comment_repl(match):
        return add_token(match.group(1), "color: #6B7280; font-style: italic;")
    code = re.sub(r'(/\*.*?\*/)', ml_comment_repl, code, flags=re.DOTALL)

    # 2. Capture and replace strings
    # Double quoted string
    def string_repl(match):
        return add_token(match.group(1), "color: #34D399;")
    code = re.sub(r'("[^"\\]*(?:\\.[^"\\]*)*")', string_repl, code)
    
    # Raw backtick string
    def raw_string_repl(match):
        return add_token(match.group(1), "color: #34D399;")
    code = re.sub(r'(`[^`]*`)', raw_string_repl, code)

    # 3. Highlight Keywords (only outside comments/strings)
    keywords = [
        r'\bpackage\b', r'\bimport\b', r'\bfunc\b', r'\bvar\b', r'\bconst\b',
        r'\btype\b', r'\bstruct\b', r'\binterface\b', r'\bmap\b', r'\bchan\b',
        r'\bgo\b', r'\bdefer\b', r'\breturn\b', r'\bif\b', r'\belse\b',
        r'\bfor\b', r'\brange\b', r'\bswitch\b', r'\bcase\b', r'\bdefault\b',
        r'\bselect\b', r'\bnil\b', r'\btrue\b', r'\bfalse\b'
    ]
    for kw in keywords:
        code = re.sub(kw, lambda m: f'<span style="color: #F87171; font-weight: bold;">{m.group(0)}</span>', code)
        
    # 4. Highlight Types & builtins
    types = [
        r'\bint\b', r'\bint64\b', r'\bstring\b', r'\bbool\b', r'\berror\b',
        r'\bfloat64\b', r'\bbyte\b', r'\bmake\b', r'\bappend\b', r'\blen\b', r'\bcap\b'
    ]
    for t in types:
        code = re.sub(t, lambda m: f'<span style="color: #60A5FA;">{m.group(0)}</span>', code)

    # 5. Restore comments and strings placeholders
    for placeholder, span in tokens.items():
        code = code.replace(placeholder, span)
        
    return code

def md_to_html(text: str) -> str:
    if not text:
        return ""
        
    # Extract and highlight code blocks first
    code_blocks = []
    
    def replace_code_block(match):
        code_content = match.group(1)
        highlighted = highlight_go_code(code_content)
        code_blocks.append(highlighted)
        return f"<!--CODE_BLOCK_{len(code_blocks)-1}-->"
        
    # Match ```go ... ``` or ``` ... ```
    pattern = re.compile(r'```(?:go)?\n(.*?)\n```', re.DOTALL)
    processed_text = pattern.sub(replace_code_block, text)
    
    # Escape general HTML characters
    processed_text = html.escape(processed_text)
    
    # Convert bold **text** -> <b>text</b>
    processed_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', processed_text)
    
    # Convert headings
    processed_text = re.sub(r'^### (.*?)$', r'<h3 style="color: #A7F3D0; font-size: 18px; margin-top: 12px; margin-bottom: 6px;">\1</h3>', processed_text, flags=re.MULTILINE)
    processed_text = re.sub(r'^## (.*?)$', r'<h2 style="color: #A7F3D0; font-size: 20px; margin-top: 14px; margin-bottom: 8px;">\1</h2>', processed_text, flags=re.MULTILINE)
    processed_text = re.sub(r'^# (.*?)$', r'<h1 style="color: #A7F3D0; font-size: 24px; margin-top: 16px; margin-bottom: 10px;">\1</h1>', processed_text, flags=re.MULTILINE)
    
    # Restore code blocks wrap in <pre>
    for i, block in enumerate(code_blocks):
        placeholder = html.escape(f"<!--CODE_BLOCK_{i}-->")
        pre_html = f'<pre style="background-color: #0F0F12; padding: 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,10); font-family: \'JetBrains Mono\', \'Courier New\', monospace; font-size: 14px; color: #E2E8F0;"><code>{block}</code></pre>'
        processed_text = processed_text.replace(placeholder, pre_html)
        
    # Convert line breaks to <br> outside <pre> tags
    parts = processed_text.split('<pre')
    new_parts = [parts[0].replace('\n', '<br>')]
    for part in parts[1:]:
        subparts = part.split('</pre>')
        outside = subparts[1].replace('\n', '<br>')
        new_parts.append(f'<pre{subparts[0]}</pre>{outside}')
        
    return "".join(new_parts)

class OverlayWindow(QWidget):
    # Resize edge constants
    EDGE_NONE = 0
    EDGE_LEFT = 1
    EDGE_TOP = 2
    EDGE_RIGHT = 4
    EDGE_BOTTOM = 8
    BORDER_WIDTH = 25

    def __init__(self):
        super().__init__()
        
        # Set window flags for overlay
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Root layout for window (gives space for shadow)
        self.root_layout = QVBoxLayout(self)
        self.root_layout.setContentsMargins(15, 15, 15, 15)
        self.root_layout.setSpacing(0)
        
        # 1. Main container frame to support rounded corners, border, and blur
        self.container = QFrame()
        self.container.setObjectName("container")
        self.container.setStyleSheet("""
            QFrame#container {
                background-color: rgba(18, 18, 22, 235);
                border: 1px solid rgba(16, 185, 129, 45);
                border-radius: 12px;
            }
        """)
        
        # 2. Add high-quality drop shadow to the container
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(25)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(6)
        self.shadow.setColor(QColor(0, 0, 0, 180))
        self.container.setGraphicsEffect(self.shadow)
        
        # Layout inside the container
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(0, 0, 0, 0) # Flush with edges
        self.container_layout.setSpacing(0)
        
        # 3. Custom Title Bar (Header for Dragging)
        self.title_bar = QWidget()
        self.title_bar.setObjectName("title_bar")
        self.title_bar.setStyleSheet("""
            QWidget#title_bar {
                background-color: rgba(25, 25, 30, 220);
                border-bottom: 1px solid rgba(255, 255, 255, 15);
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
            }
        """)
        self.title_bar_layout = QHBoxLayout(self.title_bar)
        self.title_bar_layout.setContentsMargins(12, 6, 12, 6)
        self.title_bar_layout.setSpacing(10)
        
        # Title Label
        self.title_label = QLabel("🐹 Go Interview Co-Pilot")
        self.title_label.setStyleSheet("color: #A7F3D0; font-size: 12px; font-weight: bold; background: transparent;")
        
        # Control Buttons
        self.min_btn = QPushButton("—")
        self.min_btn.setToolTip("Свернуть программу в док")
        self.min_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #94A3B8;
                border: none;
                font-size: 11px;
                font-weight: bold;
                border-radius: 4px;
                width: 22px;
                height: 22px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 30);
                color: #FFFFFF;
            }
        """)
        self.min_btn.clicked.connect(self.showMinimized)
        
        self.close_btn = QPushButton("✕")
        self.close_btn.setToolTip("Закрыть программу")
        self.close_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #94A3B8;
                border: none;
                font-size: 11px;
                font-weight: bold;
                border-radius: 4px;
                width: 22px;
                height: 22px;
            }
            QPushButton:hover {
                background-color: #EF4444;
                color: #FFFFFF;
            }
        """)
        self.close_btn.clicked.connect(QApplication.instance().quit)
        
        self.title_bar_layout.addWidget(self.title_label)
        self.title_bar_layout.addStretch()
        self.title_bar_layout.addWidget(self.min_btn)
        self.title_bar_layout.addWidget(self.close_btn)
        
        self.container_layout.addWidget(self.title_bar)
        
        # Content widget for elements below title bar
        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background: transparent;")
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(16, 12, 16, 16)
        self.content_layout.setSpacing(12)
        
        # 4. Header Row: Transcript and Status
        self.header_row_layout = QHBoxLayout()
        
        # Transcript Scroll Area (restricted height)
        self.transcript_scroll = QScrollArea()
        self.transcript_scroll.setWidgetResizable(True)
        self.transcript_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.transcript_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.transcript_scroll.setMaximumHeight(70)
        self.transcript_scroll.setStyleSheet("""
            QScrollArea {
                background-color: rgba(30, 30, 35, 180); 
                border-radius: 6px;
                border: 1px solid rgba(255, 255, 255, 15);
            }
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 4px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 30);
                min-height: 10px;
                border-radius: 2px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }
        """)
        
        # Transcript Label (Live STT)
        self.transcript_label = QLabel("Transcript: [Speech will appear here]")
        self.transcript_label.setStyleSheet("""
            color: #94A3B8; 
            font-size: 13px; 
            font-style: italic; 
            background: transparent;
            border: none;
            padding: 6px 10px; 
        """)
        self.transcript_label.setWordWrap(True)
        self.transcript_scroll.setWidget(self.transcript_label)
        
        # Status Label
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("""
            color: #10B981; 
            font-size: 12px; 
            font-weight: bold; 
            background-color: rgba(16, 185, 129, 15); 
            padding: 6px 12px; 
            border-radius: 6px;
            border: 1px solid #10B981;
        """)
        self.status_label.setFixedWidth(160)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.header_row_layout.addWidget(self.transcript_scroll, 3)
        self.header_row_layout.addWidget(self.status_label, 1, Qt.AlignmentFlag.AlignVCenter)
        self.content_layout.addLayout(self.header_row_layout)
        
        # 5. Scroll Area for TL;DR and Script
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.scroll_area.setMinimumHeight(100)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 6px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 45);
                min-height: 20px;
                border-radius: 3px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(255, 255, 255, 80);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
                height: 0px;
            }
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                border: none;
                background: none;
            }
        """)
        
        # Scroll area content widget
        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background: transparent;")
        self.scroll_content_layout = QVBoxLayout(self.scroll_content)
        self.scroll_content_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_content_layout.setSpacing(10)
        
        # TL;DR Label (Highlighted)
        self.tldr_label = QLabel("")
        self.tldr_label.setTextFormat(Qt.TextFormat.RichText)
        self.tldr_label.setStyleSheet("""
            color: #F59E0B; 
            font-size: 20px; 
            font-weight: 700; 
            background-color: rgba(245, 158, 11, 15); 
            padding: 12px 16px; 
            border-radius: 8px;
            border-left: 4px solid #F59E0B;
        """)
        self.tldr_label.setWordWrap(True)
        self.tldr_label.hide()
        
        # Script Label
        self.script_label = QLabel("Waiting for interview question...")
        self.script_label.setTextFormat(Qt.TextFormat.RichText)
        self.script_label.setStyleSheet("""
            color: #F8FAFC; 
            font-size: 17px; 
            line-height: 1.5;
            background-color: rgba(30, 30, 35, 120); 
            padding: 16px; 
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 15);
        """)
        self.script_label.setWordWrap(True)
        
        self.scroll_content_layout.addWidget(self.tldr_label)
        self.scroll_content_layout.addWidget(self.script_label)
        
        self.scroll_area.setWidget(self.scroll_content)
        self.content_layout.addWidget(self.scroll_area)
        
        self.container_layout.addWidget(self.content_widget)
        
        # Add container to root layout
        self.root_layout.addWidget(self.container)
        
        self.resize(1000, 240) # Slightly larger initial height for header
        self.center_on_top()
        self.anim = None
        
        self.user_resized = False
        self.resize_edge = self.EDGE_NONE
        
        self.setMouseTracking(True)
        self.install_event_filter_recursive(self.container)
        
    def center_on_top(self):
        screen = self.screen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = 50 # Small offset from top
        self.move(x, y)

    def install_event_filter_recursive(self, widget):
        widget.installEventFilter(self)
        widget.setMouseTracking(True)
        for child in widget.findChildren(QWidget):
            child.installEventFilter(self)
            child.setMouseTracking(True)

    def eventFilter(self, obj, event):
        if event.type() == event.Type.MouseMove:
            gp = event.globalPosition().toPoint()
            pos = self.mapFromGlobal(gp)
            self.handle_hover_pos(pos)
        return super().eventFilter(obj, event)

    def handle_hover_pos(self, pos: QPoint):
        if not (self.windowState() & Qt.WindowState.WindowMaximized) and not hasattr(self, 'drag_position') and self.resize_edge == self.EDGE_NONE:
            edge = self.get_resize_edge(pos)
            self.update_cursor_shape(edge)

    def get_resize_edge(self, pos: QPoint) -> int:
        edge = self.EDGE_NONE
        w = self.width()
        h = self.height()
        x = pos.x()
        y = pos.y()
        
        if x <= self.BORDER_WIDTH:
            edge |= self.EDGE_LEFT
        elif x >= w - self.BORDER_WIDTH:
            edge |= self.EDGE_RIGHT
            
        if y <= self.BORDER_WIDTH:
            edge |= self.EDGE_TOP
        elif y >= h - self.BORDER_WIDTH:
            edge |= self.EDGE_BOTTOM
            
        return edge

    def update_cursor_shape(self, edge: int):
        if edge == self.EDGE_NONE:
            self.setCursor(Qt.CursorShape.ArrowCursor)
        elif edge in (self.EDGE_LEFT, self.EDGE_RIGHT):
            self.setCursor(Qt.CursorShape.SizeHorCursor)
        elif edge in (self.EDGE_TOP, self.EDGE_BOTTOM):
            self.setCursor(Qt.CursorShape.SizeVerCursor)
        elif edge in (self.EDGE_LEFT | self.EDGE_TOP, self.EDGE_RIGHT | self.EDGE_BOTTOM):
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        elif edge in (self.EDGE_RIGHT | self.EDGE_TOP, self.EDGE_LEFT | self.EDGE_BOTTOM):
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position().toPoint()
            self.resize_edge = self.get_resize_edge(pos)
            
            if self.resize_edge != self.EDGE_NONE:
                self.drag_start_geometry = self.geometry()
                self.drag_start_pos = event.globalPosition().toPoint()
                event.accept()
            else:
                pos_in_title_bar = self.title_bar.mapFromParent(pos)
                if self.title_bar.rect().contains(pos_in_title_bar):
                    self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                    event.accept()

    def mouseMoveEvent(self, event):
        global_pos = event.globalPosition().toPoint()
        
        if hasattr(self, 'drag_position') and self.drag_position is not None:
            self.move(global_pos - self.drag_position)
            event.accept()
            return
            
        if self.resize_edge != self.EDGE_NONE:
            self.user_resized = True
            geom = self.drag_start_geometry
            delta = global_pos - self.drag_start_pos
            
            left = geom.left()
            top = geom.top()
            right = geom.right()
            bottom = geom.bottom()
            
            min_w = 400
            min_h = 440
            
            if self.resize_edge & self.EDGE_LEFT:
                new_left = left + delta.x()
                if right - new_left >= min_w:
                    left = new_left
            elif self.resize_edge & self.EDGE_RIGHT:
                new_right = right + delta.x()
                if new_right - left >= min_w:
                    right = new_right
                    
            if self.resize_edge & self.EDGE_TOP:
                new_top = top + delta.y()
                if bottom - new_top >= min_h:
                    top = new_top
            elif self.resize_edge & self.EDGE_BOTTOM:
                new_bottom = bottom + delta.y()
                if new_bottom - top >= min_h:
                    bottom = new_bottom
                    
            self.setGeometry(QRect(QPoint(left, top), QPoint(right, bottom)))
            event.accept()
            return
            
        if not event.buttons() & Qt.MouseButton.LeftButton:
            pos = event.position().toPoint()
            self.handle_hover_pos(pos)

    def mouseReleaseEvent(self, event):
        if hasattr(self, 'drag_position'):
            self.drag_position = None
        self.resize_edge = self.EDGE_NONE

    def resize_window_animated(self, target_height: int):
        # Prevent height shrinking below a reasonable threshold
        if target_height < 240:
            target_height = 240
            
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(150)
        geom = self.geometry()
        new_geom = QRect(geom.x(), geom.y(), geom.width(), target_height)
        self.anim.setEndValue(new_geom)
        self.anim.start()

    def update_text(self, tldr: str, script: str):
        # Auto-show if text arrives
        self.show()
        
        tldr_html = md_to_html(tldr)
        script_html = md_to_html(script)
        
        if tldr:
            self.tldr_label.setText(tldr_html)
            self.tldr_label.show()
        else:
            self.tldr_label.hide()
            
        self.script_label.setText(script_html)
        
        # Allow layouts to adjust to new content
        self.scroll_content.adjustSize()
        self.container.adjustSize()
        
        # Calculate target height based on new layout hints + padding
        if not self.user_resized:
            hint_height = self.container.sizeHint().height() + 30 # 30 is root layout margins
            target_h = max(240, min(hint_height, 600))
            self.resize_window_animated(target_h)

    def set_status(self, status: str):
        self.status_label.setText(status)
        
        # Visibility controls: hide on ready/idle
        if "Ready" in status:
            self.hide()
            self.user_resized = False
            self.resize(1000, 240)
            return
        else:
            self.show()
            
        # Color coding status and glowing frame border
        if "Recording" in status or "Listening" in status:
            self.status_label.setStyleSheet("""
                color: #EF4444; 
                font-size: 12px; 
                font-weight: bold; 
                background-color: rgba(239, 68, 68, 15); 
                padding: 6px 12px; 
                border-radius: 6px;
                border: 1px solid #EF4444;
            """)
            self.container.setStyleSheet("""
                QFrame#container {
                    background-color: rgba(18, 18, 22, 235);
                    border: 1px solid rgba(239, 68, 68, 80);
                    border-radius: 12px;
                }
            """)
        elif "Processing" in status or "Generating" in status or "Transcribing" in status:
            self.status_label.setStyleSheet("""
                color: #3B82F6; 
                font-size: 12px; 
                font-weight: bold; 
                background-color: rgba(59, 130, 246, 15); 
                padding: 6px 12px; 
                border-radius: 6px;
                border: 1px solid #3B82F6;
            """)
            self.container.setStyleSheet("""
                QFrame#container {
                    background-color: rgba(18, 18, 22, 235);
                    border: 1px solid rgba(59, 130, 246, 80);
                    border-radius: 12px;
                }
            """)
        else:
            # Green status for Done / Idle
            self.status_label.setStyleSheet("""
                color: #10B981; 
                font-size: 12px; 
                font-weight: bold; 
                background-color: rgba(16, 185, 129, 15); 
                padding: 6px 12px; 
                border-radius: 6px;
                border: 1px solid #10B981;
            """)
            self.container.setStyleSheet("""
                QFrame#container {
                    background-color: rgba(18, 18, 22, 235);
                    border: 1px solid rgba(16, 185, 129, 45);
                    border-radius: 12px;
                }
            """)

    def set_transcript(self, text: str):
        self.show()
        self.transcript_label.setText(f"Transcript: {text}")
        # Auto-scroll to the bottom of the transcript scroll area
        scrollbar = self.transcript_scroll.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
