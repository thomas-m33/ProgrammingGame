# This is a template for the levels

from PyQt6.QtWidgets import (
    QWidget, QPlainTextEdit, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
)
from PyQt6.QtGui import QPainter, QColor, QFont, QFontMetrics
from PyQt6.QtCore import QRect, QSize, Qt
import re
import multiprocessing as mp

class BaseLevelPage(QWidget):
    def __init__(self, back_method, level_info: str): # level info will probably be updated so it can include images
        super().__init__()
        self.back_method = back_method
        self.level_info = level_info
        self.build_ui()

    def build_ui(self):
        main_layout = QHBoxLayout(self) #QHBoxLayout organises widgets horizontally from left to right

        self.editor = CodeEditor()
        font = QFont("Consolas", 12)
        self.editor.setFont(font)

        font_metrics = QFontMetrics(self.editor.font())
        space_width = font_metrics.horizontalAdvance(' ')
        self.editor.setTabStopDistance(4 * space_width)

        # Inherited methods of QPlainTextEdit
        self.editor.setPlaceholderText("Type your code here...")
        self.editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap) # Disable line wrapping

        # Left half: code editor
        main_layout.addWidget(self.editor)

        # Right half: displaying info and buttons
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.addWidget(QLabel(self.level_info))

        run_button = QPushButton("Run Code")
        run_button.clicked.connect(self.safe_exec) # Temporary
        right_layout.addWidget(run_button)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.back_method)
        right_layout.addWidget(back_button)

        main_layout.addWidget(right_panel)

    @staticmethod
    def try_code(code):
        try:
            exec(code)
        except Exception as e:
            print("error:", e)

    def safe_exec(self):
        p = mp.Process(target=self.try_code, args=(self.editor.toPlainText(),))
        p.start()
        p.join(2)  # Wait up to 2 seconds

        if p.is_alive():
            p.terminate()
            print("your code got stuck")
            p.join() # Triggers OS to remove the multiprocess child's PID


class CodeEditor(QPlainTextEdit):

    character_pairs = {
    "(": ")",
    "[": "]",
    "{": "}",
    "'": "'",
    '"': '"'
    }
    # For turning inputs like ( into ()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.line_number_area = LineNumberArea(self)

        self.blockCountChanged.connect(self.update_line_number_area_width)
        # Whenever the number of lines changes, run the update method to see if more space is needed for the gutter
        # This is needed if the amount of lines gains another digit, like going from 9 to 10 lines

        self.updateRequest.connect(self.update_line_number_area)
        # When the update signal is triggered on the editor, also trigger an update on the line number area
        # (e.g. when user scrolls down)

        self.update_line_number_area_width(0)
        # Set the initial width of the line number area (it isn't 0)

    def line_number_area_width(self) -> int:
        digits = len(str(self.blockCount()))
        # Number of digits that the largest line number has

        # Calculate the width needed for the line number margin
        space = 10 + self.fontMetrics().horizontalAdvance("9") * digits # space = 10 + width of '9' * digits
        return space

    def update_line_number_area_width(self, _): # Has a throwaway parameter for the value passed in by blockCountChanged
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)
        # Reserve space on the left side of the editor for the line numbers

    def update_line_number_area(self, rect, dy): # rect is the area that needs updating
        # If the editor scrolls vertically, scroll the line-number area too
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            # Otherwise repaint the visible part of the line-number area
            self.line_number_area.update(
                0, rect.y(), self.line_number_area.width(), rect.height()
            )

        # If the visible area changed, update the margin width as well
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        # When the editor is resized, also resize the line-number gutter
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.line_number_area.setGeometry(
            QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height())
        )

    def line_number_area_paint_event(self, event):
        # Paint the background and numbers for the line-number gutter
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor(240, 240, 240))

        # Start from the first visible line in the editor
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()

        # Find the top and bottom position of the visible block
        top = round(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + round(self.blockBoundingRect(block).height())

        # Draw numbers for every visible line
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)

                # Draw the line number aligned to the right
                painter.setPen(Qt.GlobalColor.darkGray)
                painter.drawText(
                    0, top,
                    self.line_number_area.width() - 6,
                    self.fontMetrics().height(),
                    Qt.AlignmentFlag.AlignRight,
                    number
                )

            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
            block_number += 1

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            cursor = self.textCursor()
            block_text = cursor.block().text()
            indent = re.match(r"[ \t]*", block_text).group(0) # Match 0 or more spaces or tabs

            cursor.insertBlock() # Go to next line
            cursor.insertText(indent) # Insert the level of indenting detected by the regex matching
            self.setTextCursor(cursor) # Move the cursor to the updated position
            return

        elif event.text() in CodeEditor.character_pairs:
            cursor = self.textCursor()
            cursor.insertText(event.text() + CodeEditor.character_pairs[event.text()])
            cursor.movePosition(cursor.MoveOperation.Left) # Places text cursor in the middle of the characters
            self.setTextCursor(cursor)
            return

        super().keyPressEvent(event)


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor  # Reference to the CodeEditor that owns this gutter

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0) # Returns how wide the gutter should be

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event) # Delegate all painting to the editor
