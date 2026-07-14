import sys
import os
import random
os.environ["QT_LOGGING_RULES"] = "qt.multimedia.*=false" # Stops media player data from being dumped into the terminal
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QStackedWidget
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl, pyqtSignal
from menus import create_main_menu, create_level_select, SettingsMenu
from levels import (Level1Page, Level2Page, Level3Page, Level4Page, Level5Page,
                    Level6Page, Level7Page, Level8Page, Level9Page, Level10Page)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Initialise window
        self.setWindowTitle("Dave's Algorithm Adventures")
        self.stack = QStackedWidget() # Holds multiple pages
        self.setMinimumSize(852, 560)

        # Initialise audio
        # Since QMediaPlayer can only handle one audio stream at a time, we need to make separate ones for music and sfx
        self.music_player = QMediaPlayer()
        self.music_output = QAudioOutput()
        self.music_player.setAudioOutput(self.music_output)

        self.sfx_player = QMediaPlayer()
        self.sfx_output = QAudioOutput()
        self.sfx_player.setAudioOutput(self.sfx_output)

        self.songs = [
            "Before the Night.mp3",
            "New Machines.mp3",
            "Oort Cloud.mp3",
            "Resonance.mp3",
            "Synchronize.mp3"
        ]
        # All music by Home

        random.shuffle(self.songs)
        self.song_index = 0
        self.music_player.mediaStatusChanged.connect(self.on_media_status_changed)
        self.music_output.setVolume(0.25) # This will be a value decided by the user in future versions
        self.play_current_song()

        # Build GUI
        main_menu = create_main_menu(self.stack, self.close)
        level_select = create_level_select(self.stack)
        settings_menu = SettingsMenu(self.stack, self.music_output, self.sfx_output, self.toggle_fullscreen)
        self.stack.addWidget(main_menu) # Stack index 0 because it was added first
        self.stack.addWidget(level_select) # Index 1
        self.stack.addWidget(settings_menu) # Index 2...

        level_classes = [
            Level1Page, Level2Page, Level3Page, Level4Page, Level5Page,
            Level6Page, Level7Page, Level8Page, Level9Page, Level10Page
        ]

        self.level_pages = []

        for LevelClass in level_classes:
            level_page = LevelClass(self.sfx_player, back_method=lambda: self.stack.setCurrentIndex(1))
            self.stack.addWidget(level_page)
            self.level_pages.append(level_page)

        self.stack.currentChanged.connect(self.on_page_stack_changed)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)

    def toggle_fullscreen(self, toggle: bool):
        if toggle:
            self.showFullScreen()
        else:
            self.showNormal()

    def play_current_song(self):
        music_file_path = os.path.abspath(f"assets/music/{self.songs[self.song_index]}")
        self.music_player.setSource(QUrl.fromLocalFile(music_file_path))
        self.music_player.play()

    def on_media_status_changed(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.song_index += 1
            if self.song_index >= len(self.songs):
                self.song_index = 0
            self.play_current_song()

    # Only reason this function exists is to fix a bug with level 7. There might be a better way to do this
    def on_page_stack_changed(self):
        if self.stack.currentIndex() == 9: # Checks if the page is level 7
            self.level_pages[6].activate_mechanic()
        else:
            self.level_pages[6].deactivate_mechanic()


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
