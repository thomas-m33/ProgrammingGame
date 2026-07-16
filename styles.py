import os
from PyQt6.QtWidgets import QPushButton, QLabel, QGraphicsDropShadowEffect, QVBoxLayout, QWidget, QHBoxLayout, QStyle
from PyQt6.QtGui import QColor, QFont, QFontDatabase
from PyQt6.QtCore import Qt, QSize


class MainMenuButton(QPushButton):
    def __init__(self, text,
                 font_path=os.path.abspath("assets/fonts/BigShoulders-Bold.ttf"),
                 default_img=os.path.abspath("assets/buttons/default.png"),
                 pressed_img=os.path.abspath("assets/buttons/pressed.png"),
                 parent=None):

        super().__init__(parent)

        # Handle Font Loading
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            self.font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            self.font_family = "Arial"  # Fallback if font file missing

        # Base Styling
        # This part is for compatibility. Eventually I will have to add compatibility to all the file paths
        d_url = default_img.replace('\\', '/')
        p_url = pressed_img.replace('\\', '/')

        self.setStyleSheet(f"""
            QPushButton {{
                border-image: url("{d_url}");
                background-color: transparent; 
                border: none;                  
            }}
            QPushButton:pressed {{
                border-image: url("{p_url}");
            }}
        """)

        self.setMinimumSize(180, 75)

        # Layout & Text
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)

        self.text_label = QLabel(text)

        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.text_label.setStyleSheet("""
                    color: #FFFFFF; 
                    background-color: transparent;
                    padding: 38px; 
                """)

        # Glow Effect
        self.glow = QGraphicsDropShadowEffect(self)
        self.glow.setBlurRadius(30)
        self.glow.setColor(QColor("#FFFFFF"))
        self.glow.setOffset(0, 0)
        self.text_label.setGraphicsEffect(self.glow)

        layout.addWidget(self.text_label)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        # Safely scale based on the smaller bounding dimension
        safe_width_scale = self.width() * 0.10
        safe_height_scale = self.height() * 0.30
        dynamic_font_size = max(12, int(min(safe_width_scale, safe_height_scale)))

        font = QFont(self.font_family, dynamic_font_size, QFont.Weight.Bold)
        font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 105)
        self.text_label.setFont(font)
        self.glow.setBlurRadius(max(4, int(dynamic_font_size * 0.12)))

    def mousePressEvent(self, event):
        self.glow.setColor(QColor("#8B8B8B"))
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.glow.setColor(QColor("#FFFFFF"))
        super().mouseReleaseEvent(event)


class ProgressButton(QPushButton):
    def __init__(self,
                 text="",
                 completed=False,
                 default_img=os.path.abspath("assets/buttons/uncompleted default.png"),
                 pressed_img=os.path.abspath("assets/buttons/uncompleted pressed.png"),
                 parent=None):

        super().__init__(parent)

        self.default_img = default_img
        self.pressed_img = pressed_img
        self.completed = completed

        self.setStyleSheet("border: none; background-color: transparent;")
        self.setMinimumSize(180, 75)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)

        self.text_label = QLabel(text)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.text_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.text_label.setStyleSheet("""
            color: #FFFFFF;
            background-color: transparent;
            padding: 38px;
        """)

        layout.addWidget(self.text_label)
        self._apply_state_images()

    def _apply_state_images(self):
        if self.completed:
            d_url = self.default_img.replace("uncompleted", "completed").replace("\\", "/")
            p_url = self.pressed_img.replace("uncompleted", "completed").replace("\\", "/")
        else:
            d_url = self.default_img.replace("\\", "/")
            p_url = self.pressed_img.replace("\\", "/")

        self.setStyleSheet(f"""
            QPushButton {{
                border-image: url("{d_url}");
                background-color: transparent;
                border: none;
            }}
            QPushButton:pressed {{
                border-image: url("{p_url}");
            }}
        """)

    def set_completed(self, completed=True):
        self.completed = completed
        self._apply_state_images()

class CustomTitleBar(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setFixedHeight(25)

        # Unified Application Theme
        self.setStyleSheet("""
            QWidget { 
                background-color: #1e1e24; 
                color: #ffffff; 
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QPushButton { 
                background-color: transparent; 
                border: none; 
                font-size: 14px;
                color: #cccccc;
            }
            QPushButton:hover { 
                background-color: #2d2d35; 
                color: #ffffff;
            }
            QPushButton#close_btn:hover { 
                background-color: #e81123; 
                color: #ffffff;
            }
        """)

        layout = QHBoxLayout()
        layout.setContentsMargins(12, 0, 0, 0)
        layout.setSpacing(0)

        # Window Title Label
        self.title = QLabel("Dave's Algorithm Adventures")
        self.title.setStyleSheet("font-size: 12px; font-weight: 500;")
        layout.addWidget(self.title)

        layout.addStretch()

        # Minimize Interface Option Button
        self.min_btn = QPushButton("—")
        self.min_btn.setFixedSize(46, 32)
        self.min_btn.clicked.connect(self.parent_window.showMinimized)
        layout.addWidget(self.min_btn)

        # Maximize / Restore Desktop Layout Square Button
        self.max_btn = QPushButton()
        self.max_btn.setFixedSize(46, 32)
        self.max_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.max_btn.setFlat(True)
        self.max_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarMaxButton))
        self.max_btn.setIconSize(QSize(12, 12))
        self.max_btn.clicked.connect(self.toggle_maximize_state)
        layout.addWidget(self.max_btn)

        # Application Execution Termination Option Button
        self.close_btn = QPushButton("✕")
        self.close_btn.setObjectName("close_btn")
        self.close_btn.setFixedSize(46, 32)
        self.close_btn.clicked.connect(self.parent_window.close)
        layout.addWidget(self.close_btn)

        self.setLayout(layout)

    def toggle_maximize_state(self):
        if self.parent_window.isMaximized():
            self.parent_window.showNormal()
            self.max_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarMaxButton))
        else:
            self.parent_window.showMaximized()
            self.max_btn.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarNormalButton))
            self.max_btn.setToolTip("Restore")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Only allow dragging if the window isn't currently stretched out fully maximized
            if not self.parent_window.isMaximized():
                self.drag_pos = event.globalPosition().toPoint() - self.parent_window.frameGeometry().topLeft()
                event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and hasattr(self, 'drag_pos'):
            if not self.parent_window.isMaximized():
                self.parent_window.move(event.globalPosition().toPoint() - self.drag_pos)
                event.accept()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.toggle_maximize_state()