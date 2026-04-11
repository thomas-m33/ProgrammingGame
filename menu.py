import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout, QStackedWidget

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dave's Algorithm Adventures") # Text that appears at the top of the window
        self.stack = QStackedWidget() # Holds multiple pages and you switch between them

        # Main Menu
        # ----------
        page1 = QWidget()
        layout1 = QVBoxLayout()

        title = QLabel("Dave's Algorithm Adventures") # QLabel is an object type which displays non-editable text
        title.setStyleSheet("font-size: 28px; font-weight: bold;")  # Sets the style for the title's QLabel object
        # Will add more styling to everything later.

        button1 = QPushButton("Play") # QPushButton is an object type which creates a pushable button
        button2 = QPushButton("Settings")
        button3 = QPushButton("Quit")

        button1.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        button2.clicked.connect(self.settings_clicked)
        button3.clicked.connect(self.close) # Runs the close method which makes app.exec() return
        # On the signal from a QPushButton being clicked, it will run a method of the MainWindow class
        # .connect(method) ties the signal to the method

        layout1.addWidget(title)
        layout1.addWidget(button1)
        layout1.addWidget(button2)
        layout1.addWidget(button3)
        # Adds all the objects defined above to the layout
        # This is done by running the addWidget() method from QVBoxLayout on the layout object
        page1.setLayout(layout1)
        # ----------

        # Level Select
        # ----------
        page2 = QWidget()
        layout2 = QVBoxLayout()
        layout2.addWidget(QLabel("Level Select"))
        page2.setLayout(layout2)

        grid_layout = QGridLayout()

        for i in range(10):
            button = QPushButton(str(i+1))
            row = i // 5   # 5 buttons per row
            col = i % 5
            grid_layout.addWidget(button, row, col)

        back1 = QPushButton("Back")
        grid_layout.addWidget(back1)
        back1.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        layout2.addLayout(grid_layout)
        # ----------

        # Add pages to the stack
        self.stack.addWidget(page1)
        self.stack.addWidget(page2)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)

    def settings_clicked(self):
        print("Settings clicked")

    # Methods to be run on the buttons being clicked

app = QApplication(sys.argv) # Creates the application object and passes any command line arguments into it.
window = MainWindow()
window.show() # Makes the window visible.

sys.exit(app.exec())
# Starts the Qt event loop.
# app.exec() does not return until user does something like press the quit button or close the window.
# When it does return, it tells Python to exit the app with a code of the return value.