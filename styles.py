import os
from PyQt6.QtWidgets import (QPushButton, QLabel, QGraphicsDropShadowEffect,
                             QVBoxLayout, QWidget, QHBoxLayout, QStyle, QPlainTextEdit)
from PyQt6.QtGui import QColor, QFont, QFontDatabase, QFontMetrics
from PyQt6.QtCore import Qt, QSize
from utils import path

standard_styles = """
            QPushButton {
                background-color: #2D2D2D;
                border: 1px solid #3C3C3C;
                border-bottom: 1px solid #222222;
                border-radius: 4px;
                color: #FFFFFF;
                font-family: "Segoe UI Variable", "Segoe UI", sans-serif;
                font-size: 14px;
                padding: 6px 16px;
            }
            
            QPushButton:hover {
                background-color: #383838;
                border: 1px solid #404040;
                border-bottom: 1px solid #222222;
            }
            
            QPushButton:pressed {
                background-color: #282828;
                border: 1px solid #3C3C3C;
                border-top: 1px solid #222222;
                color: rgba(255, 255, 255, 0.78);
            }
            
            QPushButton:disabled {
                background-color: #1E1E1E;
                border: 1px solid #2B2B2B;
                color: #636363;
            }
            
            QPushButton:focus {
                border: 1px solid #757575; 
                }
                

            QSlider {
                min-height: 20px;
            }

            QSlider::groove:horizontal {
                height: 6px;
                background: #E0E0E0;
            }

            QSlider::sub-page:horizontal {
                background: #FF66C4;
            }

            QSlider::add-page:horizontal {
                background: #E0E0E0;
            }

            QSlider::handle:horizontal {
                background: #424242;
                width: 16px;
                height: 16px;
                margin-top: -5px;
                margin-bottom: -5px;
                border-radius: 8px;
            }
            
            
            QCheckBox {
                padding-top: 8px;
                padding-bottom: 8px;
                color: #F0F0F0;
                spacing: 12px;
                font-weight: 500;
            }

            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #FFFFFF;
                border-radius: 5px;
                background-color: rgba(45, 45, 45, 0.3);
            }

            QCheckBox::indicator:hover {
                border: 2px solid #FF99D8;
                background-color: rgba(255, 102, 196, 0.1);
            }
            
            QCheckBox::indicator:checked {
                background-color: #FF66C4;
                border: 2px solid #2D2D2F;
            }
            
            QCheckBox::indicator:checked:hover {
                background-color: #FF99D8; /* Lighter pink when hovering while checked */
                border: 2px solid #3D3D3D; /* Subtly lighter border on hover */
            }

            QCheckBox:disabled {
                color: #555555;
            }
            
            QCheckBox::indicator:disabled {
                border: 2px solid #2D2D2D;
                background-color: transparent;
            }
        """

class MainMenuButton(QPushButton):
    def __init__(self, text, parent=None):

        super().__init__(parent)

        font_path = path("assets/fonts/BigShoulders-Bold.ttf")
        default_img = path("assets/buttons/default.png")
        pressed_img = path("assets/buttons/pressed.png")

        # Handle font loading
        font_id = QFontDatabase.addApplicationFont(font_path)
        self.font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

        # On windows, file paths contain the character \ which messes with Python strings
        # Replacing \ with / still lets Qt read the paths properly but avoids this issue
        d_url = default_img.replace('\\', '/')
        p_url = pressed_img.replace('\\', '/')
        # For some reason, I only got problems with the \ character when trying to put a path into a stylesheet

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

        # Scale based on the smaller bounding dimension
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
    def __init__(self, text, completed=False, parent=None):

        super().__init__(parent)
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
        self.apply_state_images()
        font_id = QFontDatabase.addApplicationFont(path("assets/fonts/BigShoulders-Bold.ttf"))
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        self.text_label.setFont(QFont(font_family, 18))

    def apply_state_images(self):
        if self.completed:
            self.default_img = path("assets/buttons/completed default.png")
            self.pressed_img = path("assets/buttons/completed pressed.png")
        else:
            self.default_img = path("assets/buttons/uncompleted default.png")
            self.pressed_img = path("assets/buttons/uncompleted pressed.png")

        d_url = self.default_img.replace('\\', '/')
        p_url = self.pressed_img.replace('\\', '/')

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
        self.apply_state_images()


class CustomTitleBar(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.setFixedHeight(25)

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
            # Only allow dragging if the window isn't currently fully maximized
            if not self.parent_window.isMaximized():
                self.drag_pos = event.globalPosition().toPoint() - self.parent_window.frameGeometry().topLeft()
                event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and hasattr(self, "drag_pos"):
            if not self.parent_window.isMaximized():
                self.parent_window.move(event.globalPosition().toPoint() - self.drag_pos)
                event.accept()

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.toggle_maximize_state()


class RegularText(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("""
            QLabel {
                font-family: "Segoe UI";
                font-size: 9pt;
                color: #FFFFFF;
            }
        """)


class StyledCodeEditor(QPlainTextEdit):
    # Gutter colors for the QPainter in line_number_area_paint_event
    GUTTER_BG_COLOR = QColor(37, 37, 40)
    GUTTER_TEXT_COLOR = QColor(133, 133, 133)

    def __init__(self, parent=None):
        super().__init__(parent)

        font_metrics = QFontMetrics(QFont("Consolas", 12))
        space_width = font_metrics.horizontalAdvance(" ")
        self.setTabStopDistance(4 * space_width)

        # Base styling for the code editor
        self._base_style = """
            QPlainTextEdit {
                background-color: #2d2d2d;
                color: #d4d4d4;
                border: 1px solid #3e3e42;
                border-radius: 4px;
                padding: 4px;
                selection-background-color: #264f78;
                font-family: "Consolas";
                font-size: 12pt;
            }

            /* Minimalist Dark Scrollbars */
            QScrollBar:vertical {
                border: none;
                background: #2d2d2d;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #555555;
                min-height: 20px;
                border-radius: 6px;
                margin: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background: #777777;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
                background: none;
            }

            QScrollBar:horizontal {
                border: none;
                background: #2d2d2d;
                height: 12px;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background: #555555;
                min-width: 20px;
                border-radius: 6px;
                margin: 2px;
            }
            QScrollBar::handle:horizontal:hover {
                background: #777777;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
                background: none;
            }
        """

        # Swaps selection colors for the obscure mechanic
        self._obscured_style = self._base_style + """
            QPlainTextEdit {
                selection-background-color: #777777;
                selection-color: #777777;
            }
        """

        # Apply base style initially
        self.setStyleSheet(self._base_style)

    def set_obscure_selection_style(self, enable: bool):
        # Safely toggles the stylesheet for the obscure mechanic selection without resetting scrollbars
        if enable:
            self.setStyleSheet(self._obscured_style)
        else:
            self.setStyleSheet(self._base_style)


class ConsoleDisplay(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.appendPlainText('# Output Console')
        self.setReadOnly(True)

        self.setStyleSheet("""
            ConsoleDisplay {
                background-color: #262626;
                color: #FFFFFF;
                border: 1px solid #333333;
                border-radius: 4px;
                padding: 4px;
                font-family: "Consolas";
            }

            /* Minimalist Dark Scrollbars */
            ConsoleDisplay QScrollBar:vertical {
                border: none;
                background: #262626;
                width: 12px;
                margin: 0px;
            }
            ConsoleDisplay QScrollBar::handle:vertical {
                background: #555555;
                min-height: 20px;
                border-radius: 6px;
                margin: 2px;
            }
            ConsoleDisplay QScrollBar::handle:vertical:hover {
                background: #777777;
            }
            ConsoleDisplay QScrollBar::add-line:vertical, ConsoleDisplay QScrollBar::sub-line:vertical {
                height: 0px;
                background: none;
            }

            ConsoleDisplay QScrollBar:horizontal {
                border: none;
                background: #262626;
                height: 12px;
                margin: 0px;
            }
            ConsoleDisplay QScrollBar::handle:horizontal {
                background: #555555;
                min-width: 20px;
                border-radius: 6px;
                margin: 2px;
            }
            ConsoleDisplay QScrollBar::handle:horizontal:hover {
                background: #777777;
            }
            ConsoleDisplay QScrollBar::add-line:horizontal, ConsoleDisplay QScrollBar::sub-line:horizontal {
                width: 0px;
                background: none;
            }
        """)