# This is a template for the levels

from PyQt6.QtWidgets import QWidget, QPlainTextEdit, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PyQt6.QtGui import QPainter, QColor, QFont, QFontMetrics
from PyQt6.QtCore import QRect, QSize, Qt
import re
import multiprocessing
import io
from contextlib import redirect_stdout, redirect_stderr

class BaseLevelPage(QWidget):
    success_text = "Your code was successful! Great job on helping Dave."

    def __init__(self, back_method, level_info: str, func_name: str, parameters: str, io_checks):
        # level info will probably be updated so it can include images
        super().__init__()
        self.back_method = back_method # Method of MainWindow, goes back to the page stack index for level select screen
        self.level_info = level_info # Instructions/info displayed on the right panel
        self.func_name = func_name # Name of the function that using is writing their algorithm inside
        self.parameters = parameters # Parameters that the function is declared with.
        self.io_checks = io_checks # A dictionary of inputs and expected outputs, used for testing the user algorithm
        self.build_ui()

    def build_ui(self):
        main_layout = QHBoxLayout(self) #QHBoxLayout organises widgets horizontally from left to right

        self.editor = CodeEditor()
        self.console = ConsoleDisplay()
        font = QFont("Consolas", 12)
        self.editor.setFont(font)
        self.console.setFont(font)

        font_metrics = QFontMetrics(self.editor.font())
        space_width = font_metrics.horizontalAdvance(' ')
        self.editor.setTabStopDistance(4 * space_width)

        cursor = self.editor.textCursor()
        cursor.insertText(self.get_starting_text())
        cursor.insertBlock()
        cursor.insertText("\t")
        self.editor.setTextCursor(cursor)
        self.editor.setPlaceholderText("Type your code here...")
        self.editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap) # Disable line wrapping

        # Left half: code editor
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(self.editor, stretch=3)
        left_layout.addWidget(self.console, stretch=1)

        # Right half: displaying info and buttons
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        info = QLabel(self.level_info)
        right_layout.addWidget(info)
        info.setWordWrap(True)

        run_button = QPushButton("Run Code")
        run_button.clicked.connect(self.safe_exec) # Temporary
        right_layout.addWidget(run_button)

        submit_button = QPushButton("Submit Solution")
        submit_button.clicked.connect(lambda: self.safe_exec(test=True))
        right_layout.addWidget(submit_button)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.back_method)
        right_layout.addWidget(back_button)

        main_layout.addWidget(left_panel, stretch=3)
        main_layout.addWidget(right_panel, stretch=2)

        self.editor.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        right_panel.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding
        )

    # This needs to be a static method because otherwise Python will throw a pickling error
    # Also makes sure you can't mess with the class methods or buttons
    @staticmethod
    def try_code(code, stdout_queue):
        buffer = io.StringIO()
        with redirect_stdout(buffer), redirect_stderr(buffer):  # Errors and print statements redirected to buffer
            try:
                exec(code, {}) # The {} gives exec an empty namespace to use
            except Exception as e:
                print("error:", e)
        stdout_queue.put(buffer.getvalue())

    @staticmethod
    def run_tests(code, func_name, io_dict, success_text):
        def fail_msg(args, expected_output, output):
            if "\n" in expected_output:
                print(f"Your code failed with an input of ({args})")
                print(f"Expected output:\n{expected_output}")
                print(f"Actual output:\n{output}")
            else:
                print(f"Your code failed with an input of ({args})")
                print(f"Expected output: {expected_output}")
                print(f"Actual output: {output}")

        if func_name not in code:
            print(f"Your code is missing the function {func_name}")
            return

        for args, expected_output in io_dict.items():
            namespace = {}
            exec(code + f"\noutput = {func_name}({args})", namespace)
            output = namespace["output"]
            # output was created inside exec's namespace, so must it be fetched from there

            if type(output) is list:
                if sorted(output) != expected_output:
                    fail_msg(args, expected_output, output)
                    return
            elif type(output) is str:
                if output.strip() != expected_output:
                    fail_msg(args, expected_output, output)
                    return
            else:
                if output != expected_output:
                    fail_msg(args, expected_output, output)
                    return

        # If the user passed all the tests, then a success message is displayed in the console
        print(success_text)

    @staticmethod
    def test_code(Class, code, func_name, io_dict, stdout_queue):
        buffer = io.StringIO()
        if func_name in code:
            with redirect_stdout(buffer), redirect_stderr(buffer):
                try:
                    Class.run_tests(code, func_name, io_dict, Class.success_text)
                except Exception as e:
                    print("error:", e)
        else:
            buffer.write(f"error: the function {func_name} is not in your code.")
        stdout_queue.put(buffer.getvalue())

    def safe_exec(self, test=False):
        stdout_queue = multiprocessing.Queue()
        if test:
            p = multiprocessing.Process(
                target=self.test_code,
                args=(self.__class__, self.editor.toPlainText(), self.func_name, self.io_checks, stdout_queue))
            p.start()
            p.join(3) # Wait up to 3 seconds
        else:
            p = multiprocessing.Process(target=self.try_code, args=(self.editor.toPlainText(), stdout_queue))
            p.start()
            p.join(2)

        if p.is_alive():
            p.terminate()
            self.console.appendPlainText("Your code took too long to execute. It may have gotten stuck.")
            p.join() # Triggers OS to remove the multiprocess child's PID

        if not stdout_queue.empty():
            text = stdout_queue.get().rstrip("\n")
            self.console.appendPlainText(text)

    def get_starting_text(self):
        return f"def {self.func_name}({self.parameters}):"


class CodeEditor(QPlainTextEdit):

    KEY_PAIRS = {
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

        space = 10 + self.fontMetrics().horizontalAdvance("9") * digits # space = 10 + width of '9' * digits
        # Calculates the width needed for the line number margin
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

        elif event.text() in CodeEditor.KEY_PAIRS:
            cursor = self.textCursor()
            cursor.insertText(event.text() + CodeEditor.KEY_PAIRS[event.text()])
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


class ConsoleDisplay(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.appendPlainText('# Output Console')
        self.setReadOnly(True)


