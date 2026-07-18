import multiprocessing
import sys
import os
os.environ["QT_LOGGING_RULES"] = "qt.multimedia.*=false" # Stops media player data from being dumped into the terminal
import random
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QStackedWidget, QGridLayout
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl, Qt
from menus import LevelSelectPage, SettingsPage, MainMenuPage, BackgroundVideoView
from levels import (Level1Page, Level2Page, Level3Page, Level4Page, Level5Page,
                    Level6Page, Level7Page, Level8Page, Level9Page, Level10Page)
from styles import CustomTitleBar, standard_styles
from utils import path, SaveManager, load_save_data


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(standard_styles)

        # Initialise window
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.CustomizeWindowHint)
        self.setWindowTitle("Dave's Algorithm Adventures")
        self.stack = QStackedWidget() # Holds multiple pages
        self.setMinimumSize(920, 640)
        self.title_bar = CustomTitleBar(self)

        # Initialise audio
        # Since QMediaPlayer can only handle one audio stream at a time, we need to make separate ones for music and sfx
        self.music_player = QMediaPlayer()
        self.music_output = QAudioOutput()
        self.music_player.setAudioOutput(self.music_output)

        self.sfx_player = QMediaPlayer()
        self.sfx_output = QAudioOutput()
        self.sfx_player.setAudioOutput(self.sfx_output)

        self.songs = [
            "Above All.mp3",
            "Before the Night.mp3",
            "New Machines.mp3",
            "Resonance.mp3",
            "Sunshower.mp3",
            "Synchronize.mp3"
        ]
        # All music by Home

        random.shuffle(self.songs)
        self.song_index = 0
        self.music_player.mediaStatusChanged.connect(self.on_media_status_changed)
        self.play_current_song()

        # Build GUI
        self.main_menu = MainMenuPage(self.stack, self.close, self.sfx_player)
        self.level_select = LevelSelectPage(self.stack, self.sfx_player)
        self.settings_menu = SettingsPage(self.stack, self.music_output, self.sfx_output, self.sfx_player,
                                     self.toggle_fullscreen)
        self.stack.addWidget(self.main_menu) # Stack index 0 because it was added first
        self.stack.addWidget(self.level_select) # Index 1
        self.stack.addWidget(self.settings_menu) # Index 2...

        self.save_manager = SaveManager(self.level_select, self.settings_menu)
        self.background = BackgroundVideoView()
        self.background.start()

        level_classes = [
            Level1Page, Level2Page, Level3Page, Level4Page, Level5Page,
            Level6Page, Level7Page, Level8Page, Level9Page, Level10Page
        ]

        self.level_pages = []

        for LevelClass in level_classes:
            level_page = LevelClass(self.sfx_player,
                                    back_method=lambda: self.stack.setCurrentIndex(1),
                                    save_data_update_method= self.save_manager.update_save_data
                                    )
            self.stack.addWidget(level_page)
            self.level_pages.append(level_page)

        self.stack.currentChanged.connect(self.on_page_stack_changed)

        content_host = QWidget()
        content_host.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        content_layout = QGridLayout(content_host)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        self.background.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.stack.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.stack.setStyleSheet("QStackedWidget { background: transparent; border: none; }")

        content_layout.addWidget(self.background, 0, 0)
        content_layout.addWidget(self.stack, 0, 0)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.title_bar)
        main_layout.addWidget(content_host)
        self.setLayout(main_layout)

        # Preload the level videos so the transition from the menu video doesn't leave the screen empty for a bit
        self.background.preload_level_videos()

    def toggle_fullscreen(self, toggle: bool):
        if toggle:
            self.title_bar.hide()  # Remove custom title bar layout
            self.showFullScreen()
        else:
            self.title_bar.show()  # Bring back title bar in windowed view modes
            self.showNormal()

    def play_current_song(self):
        music_file_path = path(f"assets/music/{self.songs[self.song_index]}")
        self.music_player.setSource(QUrl.fromLocalFile(music_file_path))
        self.music_player.play()

    def on_media_status_changed(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.song_index += 1
            if self.song_index >= len(self.songs):
                self.song_index = 0
            self.play_current_song()

    def on_page_stack_changed(self):
        if self.stack.currentIndex() == 9: # Checks if the page is level 7
            self.level_pages[6].activate_mechanic()
        else:
            self.level_pages[6].deactivate_mechanic()

        # Set overlays and backgrounds
        match self.stack.currentIndex():
            case 0:
                self.background.overlay.setVisible(False)
                self.background.show_video("menu")
            case 1 | 2:
                self.background.set_overlay_for_menus()
                self.background.show_video("menu")
            case 3 | 4 | 5 | 6:
                self.background.set_overlay_for_levels()
                self.background.show_video("purple stars")
            case 7 | 9:
                self.background.set_overlay_for_levels()
                self.background.show_video("red stars")
            case 8 | 10 | 11 | 12:
                self.background.set_overlay_for_levels()
                self.background.show_video("pink stars")

    def closeEvent(self, event):
        # Detach sources so audio/video is fully released
        # Fixes a bug where the app would remain running in the background even after you closed it
        self.background.stop()
        self.music_player.stop()
        self.sfx_player.stop()
        self.music_player.setSource(QUrl())
        self.sfx_player.setSource(QUrl())

        self.save_manager.update_save_data("fullscreen", value=self.isFullScreen())
        self.save_manager.update_save_data("music_slider_value", value=(self.music_output.volume()*200))
        self.save_manager.update_save_data("sfx_slider_value", value=(self.sfx_output.volume()*200))

        # Close the app
        event.accept()


if __name__ == "__main__":
    multiprocessing.freeze_support() # Do not allow multiprocessing children past this point
    app = QApplication(sys.argv) # Creates the application object and passes any command line arguments into it.

    window = MainWindow()
    window.show() # Makes the window visible.

    sys.exit(app.exec())
    # Starts the Qt event loop.
    # app.exec() does not return until user does something like press the quit button or close the window.
    # When it does return, it tells Python to exit the app with a code of the return value.
