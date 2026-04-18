from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QSizePolicy
from PyQt6.QtGui import QPixmap

def create_main_menu(stack, quit_method):
    page = QWidget()
    main_layout = QHBoxLayout()
    left_layout = QVBoxLayout()
    right_layout = QVBoxLayout()
    main_layout.addLayout(left_layout, stretch = 1)
    main_layout.addSpacing(50)  # Puts 50 pixels of empty space between left and right side
    main_layout.addLayout(right_layout, stretch = 1)
    main_layout.setContentsMargins(50, 50, 50, 50)

    title = QLabel("Dave's Algorithm Adventures")  # QLabel is an object type which displays non-editable text
    title.setStyleSheet("font-size: 28px; font-weight: bold;")  # Sets the style for the title's QLabel object
    # Will add more styling to everything later.

    button1 = QPushButton("Play") # QPushButton is an object type which creates a pushable button
    button2 = QPushButton("Settings")
    button3 = QPushButton("Quit")
    button1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    button2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    button3.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    button1.clicked.connect(lambda: stack.setCurrentIndex(1)) # 0 = main menu, 1 = level select
    button2.clicked.connect(lambda: print("Settings clicked")) # Will add settings later
    button3.clicked.connect(quit_method)
    # Connects the button objects to a function that will run when they are clicked

    dave_pic = QLabel()
    pixmap = QPixmap("dave.png")
    scaled_pixmap = pixmap.scaled(200, 200)
    dave_pic.setPixmap(scaled_pixmap)

    left_layout.addWidget(title)
    left_layout.addWidget(dave_pic)
    right_layout.addWidget(button1)
    right_layout.addWidget(button2)
    right_layout.addWidget(button3)
    # Adds all the objects defined above to the layout

    page.setLayout(main_layout)
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
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        button.clicked.connect(lambda _, n=i: stack.setCurrentIndex(n + 2)) # Levels start at index 2
        # The clicked method also passes True or False to the first argument of lambda so it needs to be a throwaway

    back1 = QPushButton("Back")
    back1.clicked.connect(lambda: stack.setCurrentIndex(0))
    grid_layout.addWidget(back1, 2, 0, 1, 5)

    layout.addLayout(grid_layout)
    page.setLayout(layout)
    return page