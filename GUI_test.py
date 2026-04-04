import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App") # Text that appears at the top of the window.

        title = QLabel("Main Menu") #QLabel is an object type which displays non-editable text.
        title.setStyleSheet("font-size: 28px; font-weight: bold;")  # Sets the style for the title's QLabel object.
        # Will add more styling to everything later.

        button1 = QPushButton("Play") #QPushButton is an object type which creates a pushable button.
        button2 = QPushButton("Settings")
        button3 = QPushButton("Quit")

        button1.clicked.connect(self.play_clicked)
        button2.clicked.connect(self.settings_clicked)
        button3.clicked.connect(self.close) # runs the close method which makes app.exec() return
        # On the signal from a QPushButton being clicked, it will run a method of the MainWindow class.
        # .connect(method) ties the signal to the method.

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)
        # Adds all the objects defined above to the layout (screen).
        # This is done by running the addWidget() method from QVBoxLayout on the layout object.

        self.setLayout(layout)
        # Sets the layout for MainWindow to the object defined above.

    def play_clicked(self):
        print("Play clicked")

    def settings_clicked(self):
        print("Settings clicked")

    # Methods to be run on the buttons being clicked

app = QApplication(sys.argv) # Creates the application object and passes any command line arguments into it.
window = MainWindow()
window.show() # Makes the window visible.

sys.exit(app.exec())
# Starts the Qt event loop.
# app.exec() does not return until user does something like press the quit button or close the window.
# When it does return, it tells Python to exit the app with a code of the return value