from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QSizePolicy,
                             QCheckBox, QSlider)
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

    title = QLabel()
    pixmap1 = QPixmap("assets/title.png")
    scaled_pixmap1 = pixmap1.scaled(320, 180)
    title.setPixmap(scaled_pixmap1)
    title.setScaledContents(True)

    button1 = QPushButton("Play") # QPushButton is an object type which creates a pushable button
    button2 = QPushButton("Settings")
    button3 = QPushButton("Quit")
    button1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    button2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    button3.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    button1.clicked.connect(lambda: stack.setCurrentIndex(1)) # 0 = main menu, 1 = level select
    button2.clicked.connect(lambda: stack.setCurrentIndex(2)) # Will add settings later
    button3.clicked.connect(quit_method)
    # Connects the button objects to a function that will run when they are clicked

    dave_pic = QLabel()
    pixmap2 = QPixmap("assets/dave.png")
    scaled_pixmap2 = pixmap2.scaled(250, 250)
    dave_pic.setPixmap(scaled_pixmap2)

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
        button.clicked.connect(lambda _, n=i: stack.setCurrentIndex(n + 3)) # Levels start at index 2
        # The clicked method also passes True or False to the first argument of lambda so it needs to be a throwaway

    back_button = QPushButton("Back")
    back_button.clicked.connect(lambda: stack.setCurrentIndex(0))
    grid_layout.addWidget(back_button, 2, 0, 1, 5)

    layout.addLayout(grid_layout)
    page.setLayout(layout)
    return page

class SettingsMenu(QWidget):
    def __init__(self, stack, music_output, sfx_output, toggle_fullscreen):
        super().__init__()
        self.music_output = music_output
        self.sfx_output = sfx_output

        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        right_layout = QVBoxLayout()
        main_layout.addLayout(left_layout, stretch=1)
        main_layout.addLayout(right_layout, stretch=1)

        fullscreen_checkbox = QCheckBox("Fullscreen Mode")
        music_volume_text = QLabel("Music")
        music_volume_slider = QSlider(Qt.Orientation.Horizontal)
        music_volume_slider.setRange(0, 100)
        music_volume_slider.setValue(50)
        sfx_volume_text = QLabel("Sound Effects")
        sfx_volume_slider = QSlider(Qt.Orientation.Horizontal)
        sfx_volume_slider.setRange(0, 100)
        sfx_volume_slider.setValue(50)
        back_button = QPushButton("Back")

        back_button.clicked.connect(lambda: stack.setCurrentIndex(0))
        fullscreen_checkbox.toggled.connect(toggle_fullscreen)

        music_volume_slider.valueChanged.connect(self.handle_music_volume_change)
        sfx_volume_slider.valueChanged.connect(self.handle_sfx_volume_change)

        left_layout.addWidget(QLabel("Settings"))
        left_layout.addWidget(fullscreen_checkbox)
        left_layout.addWidget(music_volume_text)
        left_layout.addWidget(music_volume_slider)
        left_layout.addWidget(sfx_volume_text)
        left_layout.addWidget(sfx_volume_slider)
        left_layout.addWidget(back_button)

        self.setLayout(main_layout)

    def handle_music_volume_change(self, value):
        volume_float = value / 200
        self.music_output.setVolume(volume_float)

    def handle_sfx_volume_change(self, value):
        volume_float = value / 200
        self.sfx_output.setVolume(volume_float)
