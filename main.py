import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QStackedWidget
from menus import create_main_menu, create_level_select
from levels.level1 import Level1Page

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dave's Algorithm Adventures")
        self.stack = QStackedWidget() # Holds multiple pages

        main_menu = create_main_menu(self.stack, self.close)
        level_select = create_level_select(self.stack)
        level1 = Level1Page(on_back = lambda: self.stack.setCurrentIndex(1))

        self.stack.addWidget(main_menu) # Stack index 0 because it was added first
        self.stack.addWidget(level_select) # Index 1
        self.stack.addWidget(level1) # Index 2

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)


if __name__ == "__main__":
# Only initialise the app if this is the main instance of it (not a multiprocess child)
# When the child imports this file it will set __name__ to "__main.py__" and not "__main__"

    app = QApplication(sys.argv) # Creates the application object and passes any command line arguments into it.

    window = MainWindow()
    window.show() # Makes the window visible.

    sys.exit(app.exec())
    # Starts the Qt event loop.
    # app.exec() does not return until user does something like press the quit button or close the window.
    # When it does return, it tells Python to exit the app with a code of the return value.