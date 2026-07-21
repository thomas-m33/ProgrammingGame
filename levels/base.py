# This is a template for the levels
import random
from PyQt6.QtWidgets import (QWidget, QPlainTextEdit, QHBoxLayout, QVBoxLayout, QPushButton, QSizePolicy,
                            QTextEdit)
from PyQt6.QtGui import QPainter, QColor, QTextCursor, QTextFormat
from PyQt6.QtCore import QRect, QSize, Qt, QTimer, QUrl
import re
import multiprocessing
import io
from contextlib import redirect_stdout, redirect_stderr
from styles import RegularText, StyledCodeEditor, ConsoleDisplay
from utils import *

class BaseLevelPage(QWidget):
    success_text = "Your code was successful! Great job on helping Dave."
    level_num = None

    def __init__(self, level_info: str, func_name: str, parameters: str, io_checks, sfx_player, back_method,
                 save_data_update_method):
        super().__init__()
        self.level_info = level_info # Instructions/info displayed on the right panel
        self.func_name = func_name # Name of the function that using is writing their algorithm inside
        self.parameters = parameters # Parameters that the function is declared with.
        self.io_checks = io_checks # A dictionary of inputs and expected outputs, used for testing the user algorithm
        self.sfx_player = sfx_player # A QMediaPlayer object for sound effects
        self.back_method = back_method # Method of MainWindow, goes back to the page stack index for level select screen
        self.save_data_update_method = save_data_update_method # Lets the page write to "save data.json"
        self.build_ui()

    def build_ui(self):
        main_layout = QHBoxLayout(self) #QHBoxLayout organises widgets horizontally from left to right

        self.editor = CodeEditor(self.sfx_player)
        self.console = ConsoleDisplay()

        cursor = self.editor.textCursor()
        cursor.insertText(self.get_starting_text())
        cursor.insertBlock()
        if self.func_name:
            cursor.insertText("\t") # Gives you an indent if you need to write a function
        self.editor.setTextCursor(cursor)
        self.editor.setPlaceholderText("Type your code here...")
        self.editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap) # Disable line wrapping

        # Left half: code editor
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.addWidget(self.editor, stretch=5)
        left_layout.addWidget(self.console, stretch=2)

        # Right half: displaying info and buttons
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        info = RegularText(self.level_info)
        right_layout.addWidget(info)
        info.setWordWrap(True)

        run_button = QPushButton("Run Code")
        run_button.clicked.connect(self.safe_exec)
        right_layout.addWidget(run_button)

        submit_button = QPushButton("Submit Solution")
        submit_button.clicked.connect(lambda: self.safe_exec(test=True))
        right_layout.addWidget(submit_button)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.back_method)
        set_button_sfx(back_button, self.sfx_player, "back.mp3")
        right_layout.addWidget(back_button)

        main_layout.addWidget(left_panel, stretch=3)
        main_layout.addWidget(right_panel, stretch=2)
        # 3:2 size ratio between the left and right panels

        self.editor.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        right_panel.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Expanding
        )


    # This needs to be a static method because otherwise multiprocessing will throw a pickling error
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
            if type(expected_output) is str and "\n" in expected_output: # Cleaner display for multi-line text
                print(f"Your code failed with an input of ({args})")
                print(f"Expected return value:\n{expected_output}")
                print(f"Actual return value:\n{output}")
            else:
                print(f"Your code failed with an input of ({args})")
                print(f"Expected return value: {expected_output}")
                print(f"Actual return value: {output}")

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
                # Strip out whitespace and invisible Unicode variation selectors (Emoji modifiers)
                clean_output = output.strip().replace("\ufe0f", "")
                clean_expected = expected_output.replace("\ufe0f", "")
                # Removing emoji modifiers prevents a bug from happening in level 9 where your solution looks identical
                # to the expected solution but still gets marked wrong because it has different Unicode

                if clean_output != clean_expected:
                    fail_msg(args, expected_output, output)
                    return
            else:
                if output != expected_output:
                    fail_msg(args, expected_output, output)
                    return

        # If the user passed all the tests, then a success message is displayed in the console
        print(success_text)
        return True

    @staticmethod
    def test_code(level_class, code, func_name, io_dict, stdout_queue, result_queue):
        buffer = io.StringIO()
        result = None
        if func_name in code:
            with redirect_stdout(buffer), redirect_stderr(buffer):
                try:
                    result = level_class.run_tests(code, func_name, io_dict, level_class.success_text)
                    # The level class is passed in here because when I try to just pass self.run_tests, multiprocessing
                    # throws a pickling error.
                except Exception as e:
                    print("error:", e)
        else:
            buffer.write(f"error: the function {func_name} is not in your code.")
        stdout_queue.put(buffer.getvalue())
        result_queue.put(result)

    def safe_exec(self, test=False):
        stdout_queue = multiprocessing.Queue()
        if test:
            result_queue = multiprocessing.Queue()
            max_lines = self.editor.max_lines
            if max_lines is not None and self.editor.blockCount() > max_lines:
                self.console.appendPlainText(f"Your solution must be {max_lines} lines or less.")
                return
            self.console.appendPlainText("\nTesting algorithm...")
            process = multiprocessing.Process(
                target=self.test_code,
                args=(self.__class__, self.editor.toPlainText(), self.func_name, self.io_checks, stdout_queue,
                      result_queue)
            )
            process.start()
            process.join(2) # Wait up to 2 seconds
        else:
            process = multiprocessing.Process(target=self.try_code, args=(self.editor.toPlainText(), stdout_queue))
            process.start()
            process.join(2)

        if process.is_alive():
            process.terminate()
            self.console.appendPlainText("Your code took too long to execute. It may have gotten stuck.")
            process.join() # Triggers OS to remove the multiprocess child's PID
            return

        if not stdout_queue.empty():
            text = stdout_queue.get().rstrip("\n")
            self.console.appendPlainText(text)

        if test and not result_queue.empty():
            result = result_queue.get()
            if result:
                self.save_data_update_method("levels_completed", str(self.__class__.level_num), value=True)

    def get_starting_text(self):
        return f"def {self.func_name}({self.parameters}):"


class CodeEditor(StyledCodeEditor):
    KEY_PAIRS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "'": "'",
    '"': '"'
    }
    # For turning inputs like ( into ()

    def __init__(self, sfx_player, parent=None):
        super().__init__(parent)
        self.sfx_player = sfx_player

        self.line_number_area = LineNumberArea(self)

        self.blockCountChanged.connect(self.update_line_number_area_width)
        # Whenever the number of lines changes, run the update method to see if more space is needed for the gutter
        # This is needed if the amount of lines gains another digit, like going from 9 to 10 lines

        self.updateRequest.connect(self.update_line_number_area)
        # When the update signal is triggered on the editor, also trigger an update on the line number area
        # (e.g. when user scrolls down)

        self.update_line_number_area_width(0)
        # Set the initial width of the line number area (it isn't 0)

        # For level 2 mechanic
        self.max_lines = None

        # For level 4 mechanic
        self.obscure_mode = False
        self._ignore_edits = False

        # For level 7 mechanic
        self.sabotage_mode = False
        self.is_flashing_red = False
        self.sabotage_timer = QTimer(self)
        self.sabotage_timer.timeout.connect(self.start_deletion_warning)
        self.flash_timer = QTimer(self)
        self.flash_timer.timeout.connect(self.toggle_flash)

        self.document().contentsChange.connect(self.on_contents_change)
        self.selectionChanged.connect(self.on_selection_changed)


    def line_number_area_width(self) -> int:
        digits = len(str(self.blockCount()))
        # Number of digits that the largest line number has

        space = 10 + self.fontMetrics().horizontalAdvance("9") * digits # space = 10 + width of '9' * digits
        # Calculates the width needed for the line number margin
        return space

    def update_line_number_area_width(self, _): # Has a throwaway parameter for the value passed in by blockCountChanged
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)
        # Reserve space on the left side of the editor for the line numbers

    def update_line_number_area(self, rect, y_change):
        # rect is the rectangle of area that needs updating
        # If the editor scrolls vertically, scroll the line-number area too
        if y_change:
            self.line_number_area.scroll(0, y_change)
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
        painter.fillRect(event.rect(), self.GUTTER_BG_COLOR)

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
                painter.setPen(self.GUTTER_TEXT_COLOR)
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
            self._ignore_edits = True
            # This is a flag to make sure on_contents_change and other methods don't detect changes here as being from
            # the player. It is mainly to fix bugs with level 4 where the highlighting would get cleared by this method.

            if self.obscure_mode:
                self.textCursor().block().setUserState(1)  # 1 = obscured

            cursor = self.textCursor()
            block_text = cursor.block().text()
            indent = re.match(r"[ \t]*", block_text).group(0)  # Match 0 or more spaces or tabs
            cursor.insertBlock()  # Go to next line
            if len(block_text) > 1 and block_text[-1] == ":":
                cursor.insertText("\t")

            if self.obscure_mode:
                cursor.block().setUserState(-1)

            cursor.insertText(indent)  # Insert the level of indenting detected by the regex matching
            self.setTextCursor(cursor)  # Move the cursor to the updated position

            self.update_dynamic_highlighting()
            return

        elif event.text() in CodeEditor.KEY_PAIRS:
            cursor = self.textCursor()
            cursor.insertText(event.text() + CodeEditor.KEY_PAIRS[event.text()])
            cursor.movePosition(cursor.MoveOperation.Left)  # Places text cursor in the middle of the characters
            self.setTextCursor(cursor)

            self._ignore_edits = False
            return

        super().keyPressEvent(event)

    def on_contents_change(self, position, chars_removed, chars_added):
        if not self.obscure_mode or self._ignore_edits:
            return

        # If text was typed or deleted, remove the 'obscured' state from affected blocks
        if chars_removed > 0 or chars_added > 0:
            block = self.document().findBlock(position)
            end_block = self.document().findBlock(position + chars_added)

            while block.isValid() and block.blockNumber() <= end_block.blockNumber():
                if block.userState() != 2:
                    block.setUserState(-1) # -1 is the default (un-obscured) state
                block = block.next()

            self.update_dynamic_highlighting()

    def on_selection_changed(self):
        if not self.obscure_mode:
            return

        cursor = self.textCursor()
        has_obscured_selection = False

        if cursor.hasSelection():
            start_block = self.document().findBlock(cursor.selectionStart())
            end_block = self.document().findBlock(cursor.selectionEnd())

            block = start_block
            while block.isValid() and block.blockNumber() <= end_block.blockNumber():
                # If the highlight touches an obscured line...
                if block.userState() == 1:
                    has_obscured_selection = True
                    break
                block = block.next()

        if has_obscured_selection:
            # Override the system highlight to be dark grey on dark grey
            self.set_obscure_selection_style(True)
        else:
            # Clear the stylesheet to return to normal OS selection colors
            self.set_obscure_selection_style(False)


    def update_dynamic_highlighting(self):
        extra_selections = []
        block = self.document().firstBlock()

        while block.isValid():
            selection = None

            # Level 2 mechanic (max lines)
            if self.max_lines is not None and block.blockNumber() >= self.max_lines:
                selection = QTextEdit.ExtraSelection()
                fmt = selection.format
                fmt.setBackground(QColor(40, 20, 20))  # dark red
                selection.format = fmt

            # Level 4 mechanic (obscured lines)
            elif self.obscure_mode and block.userState() == 1:
                selection = QTextEdit.ExtraSelection()
                fmt = selection.format
                # Pitch black text on pitch black background
                fmt.setBackground(QColor(0, 0, 0))
                fmt.setForeground(QColor(0, 0, 0))
                selection.format = fmt

            # Level 7 mechanic (line deletion)
            elif self.sabotage_mode and block.userState() == 2 and self.is_flashing_red:
                selection = QTextEdit.ExtraSelection()
                fmt = selection.format
                fmt.setBackground(QColor(255, 50, 50))  # Bright Red
                fmt.setForeground(QColor(255, 255, 255))  # White text
                fmt.setProperty(QTextFormat.Property.FullWidthSelection, True)
                selection.format = fmt

            # Apply the selection if a mechanic triggered it
            if selection:
                cursor = self.textCursor()
                cursor.setPosition(block.position())
                cursor.movePosition(
                    QTextCursor.MoveOperation.EndOfBlock,
                    QTextCursor.MoveMode.KeepAnchor
                )
                selection.cursor = cursor
                extra_selections.append(selection)

            block = block.next()

        self.setExtraSelections(extra_selections)

    def start_sabotage(self):
        if self.sabotage_mode:
            # Pick a random interval between 20s (20000ms) and 30s (30000ms)
            interval = random.randint(20000, 30000)
            self.sabotage_timer.start(interval)

    def play_sound(self, filename):
        sound_path = path(f"assets/sfx/{filename}")
        self.sfx_player.setSource(QUrl.fromLocalFile(sound_path))
        self.sfx_player.play()

    def start_deletion_warning(self):
        if self.sabotage_mode:
            self.sabotage_timer.stop()  # Pause the main countdown

            # Try to target a line that actually has text on it
            total_blocks = self.document().blockCount()
            valid_blocks = [i for i in range(1, total_blocks) if self.document().findBlockByNumber(i).text().strip()]

            # Fallback to any block if the editor is completely empty
            if not valid_blocks and total_blocks > 1:
                valid_blocks = list(range(1, total_blocks))

            # If the editor has no lines beneath the function definition, safety exit and reset timer
            if not valid_blocks:
                self.start_sabotage()
                return

            target_index = random.choice(valid_blocks)
            block = self.document().findBlockByNumber(target_index)

            # State 2 means the deletion mechanic is active
            block.setUserState(2)

            self.is_flashing_red = True
            self.flash_timer.start(250)  # Toggle flash every 250 milliseconds

            # Schedule the actual deletion in exactly 2 seconds (2000ms)
            QTimer.singleShot(2000, self.execute_deletion)


    def toggle_flash(self):
        self.is_flashing_red = not self.is_flashing_red
        if self.is_flashing_red:
            self.play_sound("deletion warning.mp3")
        self.update_dynamic_highlighting()

    def execute_deletion(self):
        self.flash_timer.stop()
        self.is_flashing_red = False
        deleted = False

        # Find the targeted block
        block = self.document().firstBlock()
        while block.isValid():
            if block.userState() == 2:
                self._ignore_edits = True

                cursor = QTextCursor(block)
                cursor.movePosition(QTextCursor.MoveOperation.StartOfBlock)
                cursor.movePosition(QTextCursor.MoveOperation.EndOfBlock, QTextCursor.MoveMode.KeepAnchor)
                cursor.removeSelectedText()
                cursor.deleteChar()

                self._ignore_edits = False
                deleted = True
                break
            block = block.next()

        self.update_dynamic_highlighting()

        if deleted:
            self.play_sound("deletion complete.mp3")

        # Restart the timer for the next sabotage event
        self.start_sabotage()


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor  # Reference to the CodeEditor that owns this gutter

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0) # Returns how wide the gutter should be

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event) # Delegate all painting to the editor
