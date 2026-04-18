from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout


def create_main_menu(stack, quit_method):
    page = QWidget()
    layout = QVBoxLayout()

    title = QLabel("Dave's Algorithm Adventures")  # QLabel is an object type which displays non-editable text
    title.setStyleSheet("font-size: 28px; font-weight: bold;")  # Sets the style for the title's QLabel object
    # Will add more styling to everything later.

    button1 = QPushButton("Play") # QPushButton is an object type which creates a pushable button
    button2 = QPushButton("Settings")
    button3 = QPushButton("Quit")

    button1.clicked.connect(lambda: stack.setCurrentIndex(1)) # 0 = main menu, 1 = level select
    button2.clicked.connect(lambda: print("Settings clicked")) # Will add settings later
    button3.clicked.connect(quit_method)
    # Connects the button objects to a function that will run when they are clicked

    layout.addWidget(title)
    layout.addWidget(button1)
    layout.addWidget(button2)
    layout.addWidget(button3)
    # Adds all the objects defined above to the layout

    page.setLayout(layout)
    return page


def create_level_select(stack):
    page = QWidget()
    layout = QVBoxLayout()

    layout.addWidget(QLabel("Level Select"))

    grid_layout = QGridLayout() # Buttons use QGridLayout

    for i in range(10):
        button = QPushButton(str(i + 1))
        row = i // 5 # 5 buttons per row
        col = i % 5
        grid_layout.addWidget(button, row, col)
        button.clicked.connect(lambda _, n=i: stack.setCurrentIndex(n + 2)) # Levels start at index 2
        # The clicked method also passes True or False to the first argument of lambda so it needs to be a throwaway

    back1 = QPushButton("Back")
    back1.clicked.connect(lambda: stack.setCurrentIndex(0))
    grid_layout.addWidget(back1, 2, 0, 1, 5)

    layout.addLayout(grid_layout)
    page.setLayout(layout)
    return page