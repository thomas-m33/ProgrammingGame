import multiprocessing
import sys
import os
os.environ["QT_LOGGING_RULES"] = "qt.multimedia.*=false" # Stops media player data from being dumped into the terminal
import random
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QStackedWidget, QGridLayout
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl, Qt
from menus import create_level_select, SettingsMenu, MainMenuPage, BackgroundVideoView
from levels import (Level1Page, Level2Page, Level3Page, Level4Page, Level5Page,
                    Level6Page, Level7Page, Level8Page, Level9Page, Level10Page)
from styles import CustomTitleBar


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # This should be moved into styles.py
        self.setStyleSheet("""
            QPushButton {
                background-color: #2D2D2D;
                border: 1px solid #3C3C3C;
                border-bottom: 1px solid #222222;
                border-radius: 4px;
                color: #FFFFFF;
                font-family: "Segoe UI Variable", "Segoe UI", sans-serif;
                font-size: 14px;
                padding: 6px 16px;
            }
            
            QPushButton:hover {
                background-color: #383838;
                border: 1px solid #404040;
                border-bottom: 1px solid #222222;
            }
            
            QPushButton:pressed {
                background-color: #282828;
                border: 1px solid #3C3C3C;
                border-top: 1px solid #222222;
                color: rgba(255, 255, 255, 0.78);
            }
            
            QPushButton:disabled {
                background-color: #1E1E1E;
                border: 1px solid #2B2B2B;
                color: #636363;
            }
            
            QPushButton:focus {
                border: 1px solid #757575; 
                }
                

            QSlider {
                min-height: 20px;
            }

            QSlider::groove:horizontal {
                height: 6px;
                background: #E0E0E0;
            }

            QSlider::sub-page:horizontal {
                background: #FF66C4;
            }

            QSlider::add-page:horizontal {
                background: #E0E0E0;
            }

            QSlider::handle:horizontal {
                background: #424242;
                width: 16px;
                height: 16px;
                margin-top: -5px;
                margin-bottom: -5px;
                border-radius: 8px;
            }
            
            
            QCheckBox {
                padding-top: 8px;
                padding-bottom: 8px;
                color: #F0F0F0;
                spacing: 12px;
                font-weight: 500;
            }

            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #FFFFFF;
                border-radius: 5px;
                background-color: rgba(45, 45, 45, 0.3);
            }

            QCheckBox::indicator:hover {
                border: 2px solid #FF99D8;
                background-color: rgba(255, 102, 196, 0.1);
            }
            
            QCheckBox::indicator:checked {
                background-color: #FF66C4;
                border: 2px solid #2D2D2F;
            }
            
            QCheckBox::indicator:checked:hover {
                background-color: #FF99D8; /* Lighter pink when hovering while checked */
                border: 2px solid #3D3D3D; /* Subtly lighter border on hover */
            }

            QCheckBox:disabled {
                color: #555555;
            }
            
            QCheckBox::indicator:disabled {
                border: 2px solid #2D2D2D;
                background-color: transparent;
            }
        """)

        # Initialise window
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.CustomizeWindowHint)
        self.setWindowTitle("Dave's Algorithm Adventures")
        self.stack = QStackedWidget() # Holds multiple pages
        self.setMinimumSize(920, 640)

        # Initialise audio
        # Since QMediaPlayer can only handle one audio stream at a time, we need to make separate ones for music and sfx
        self.music_player = QMediaPlayer()
        self.music_output = QAudioOutput()
        self.music_player.setAudioOutput(self.music_output)

        self.sfx_player = QMediaPlayer()
        self.sfx_output = QAudioOutput()
        self.sfx_player.setAudioOutput(self.sfx_output)

        self.music_output.setVolume(0.25)
        self.sfx_output.setVolume(0.25)

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
        main_menu = MainMenuPage(self.stack, self.close, self.sfx_player)
        level_select = create_level_select(self.stack, self.sfx_player)
        settings_menu = SettingsMenu(self.stack, self.music_output, self.sfx_output, self.sfx_player,
                                     self.toggle_fullscreen)
        self.stack.addWidget(main_menu) # Stack index 0 because it was added first
        self.stack.addWidget(level_select) # Index 1
        self.stack.addWidget(settings_menu) # Index 2...

        self.background = BackgroundVideoView()
        self.background.start()

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
        self.title_bar = CustomTitleBar(self)
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
        music_file_path = os.path.abspath(f"assets/music/{self.songs[self.song_index]}")
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

    # Fixing a bug where the app wouldn't close properly
    def closeEvent(self, event):
        self.background.stop()
        self.music_player.stop()
        self.sfx_player.stop()

        # Detach sources so audio/video is fully released
        self.music_player.setSource(QUrl())
        self.sfx_player.setSource(QUrl())

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
