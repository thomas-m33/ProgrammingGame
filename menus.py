import os
from PyQt6.QtCore import Qt, QUrl, QTimer, QSizeF
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout,
    QSizePolicy, QCheckBox, QSlider, QGraphicsView, QGraphicsScene
)
from PyQt6.QtGui import QPixmap, QBrush, QColor, QFont, QFontDatabase
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimediaWidgets import QGraphicsVideoItem
from styles import MainMenuButton, ProgressButton, RegularText
from utils import *

class BackgroundVideoView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFrameShape(QGraphicsView.Shape.NoFrame)
        self.setBackgroundBrush(QBrush(QColor("black")))

        self.media_players = {}
        self.video_items = {}

        menu_video_item = QGraphicsVideoItem()
        self.video_items["menu"] = menu_video_item
        self.scene.addItem(menu_video_item)
        self.current_video_item = menu_video_item

        menu_media_player = QMediaPlayer(self)
        self.media_players["menu"] = menu_media_player
        menu_media_player.setVideoOutput(menu_video_item)
        self.current_media_player = menu_media_player

        self.overlay = QWidget(self.viewport())
        self.overlay.hide()
        self.overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        video_path = path("assets/backgrounds/menu bg.mp4")
        self.current_media_player.setSource(QUrl.fromLocalFile(video_path))
        self.current_media_player.setLoops(-1)

        self.current_video_item.nativeSizeChanged.connect(self.update_video_geometry)
        QTimer.singleShot(50, self.update_video_geometry)

    def start(self):
        self.current_media_player.play()

    def stop(self):
        self.current_media_player.stop()
        self.current_media_player.setSource(QUrl())
        self.current_media_player.setVideoOutput(None)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.overlay.resize(self.viewport().size())
        self.update_video_geometry()

    def set_overlay_for_menus(self):
        self.overlay.setStyleSheet("background-color: rgba(20, 20, 20, 0.7);")
        self.overlay.setVisible(True)

    def set_overlay_for_levels(self):
        self.overlay.setStyleSheet("background-color: rgba(10, 10, 10, 0.9);")
        self.overlay.setVisible(True)

    def update_video_geometry(self):
        w = float(self.width())
        h = float(self.height())
        if w <= 0 or h <= 0:
            return

        self.scene.setSceneRect(0, 0, w, h)

        native_size = self.current_video_item.nativeSize()
        if native_size.width() <= 0 or native_size.height() <= 0:
            self.current_video_item.setSize(QSizeF(w, h))
        else:
            self.current_video_item.setSize(
                native_size.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatioByExpanding)
            )

        vx = (w - self.current_video_item.size().width()) / 2
        vy = (h - self.current_video_item.size().height()) / 2
        self.current_video_item.setPos(vx, vy)

    def set_background_video(self, file_path):
        self.current_media_player.stop()
        self.current_media_player.setSource(QUrl.fromLocalFile(file_path))
        self.current_media_player.play()

    def preload_level_videos(self):
        for name in ("red stars", "purple stars", "pink stars"):
            player = QMediaPlayer(self)
            player.setLoops(-1)
            item = QGraphicsVideoItem()
            self.scene.addItem(item)
            player.setVideoOutput(item)

            video_path = path(f"assets/backgrounds/{name}.mp4")
            player.setSource(QUrl.fromLocalFile(video_path))

            item.hide()
            self.media_players[name] = player
            self.video_items[name] = item

    def show_video(self, name):
        if name not in self.media_players or name not in self.video_items:
            return

        self.current_video_item.hide()

        self.current_video_item = self.video_items[name]
        self.current_media_player = self.media_players[name]

        self.current_video_item.show()
        self.current_video_item.nativeSizeChanged.connect(self.update_video_geometry)
        self.update_video_geometry()
        self.current_media_player.play()


class MainMenuPage(QWidget):
    def __init__(self, stack, quit_method, sfx_player):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        main_layout.addLayout(left_layout, stretch=1)
        main_layout.addSpacing(50)
        main_layout.addLayout(right_layout, stretch=1)
        main_layout.setContentsMargins(50, 50, 50, 50)

        button1 = MainMenuButton("Play")
        button2 = MainMenuButton("Settings")
        button3 = MainMenuButton("Quit")
        button1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        button2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        button3.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        button1.clicked.connect(lambda: stack.setCurrentIndex(1))
        button2.clicked.connect(lambda: stack.setCurrentIndex(2))
        button3.clicked.connect(quit_method)
        set_button_sfx(button1, sfx_player, "select.mp3")
        set_button_sfx(button2, sfx_player, "select.mp3")

        title = QLabel()
        title_pixmap = QPixmap(path("assets/images/title.png"))
        title.setPixmap(title_pixmap)
        title.setMinimumSize(320, 180)
        title.setScaledContents(True)
        dave = QLabel()
        dave_pixmap = QPixmap(path("assets/images/dave.png"))
        dave.setPixmap(dave_pixmap)
        dave.setMinimumSize(250, 250)
        dave.setScaledContents(True)

        left_layout.addWidget(title, stretch=7)
        left_layout.addWidget(dave, stretch=8)
        right_layout.addWidget(button1)
        right_layout.addWidget(button2)
        right_layout.addWidget(button3)

        self.setLayout(main_layout)


class LevelSelectPage(QWidget):
    def __init__(self, stack, sfx_player):
        super().__init__()
        layout = QVBoxLayout(self)
        grid_layout = QGridLayout()
        self.sfx_player = sfx_player

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        layout.addWidget(QLabel())
        level_select_text = QLabel("Level Select")
        level_select_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font_id = QFontDatabase.addApplicationFont(path("assets/fonts/BigShoulders-Bold.ttf"))
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        level_select_text.setFont(QFont(font_family, 32))
        layout.addWidget(level_select_text)

        self.buttons = []
        save_data = load_save_data()

        for i in range(10):
            completed_status = save_data["levels_completed"][str(i + 1)]
            button = ProgressButton(str(i + 1), completed=completed_status)
            self.buttons.append(button)
            row = i // 5
            col = i % 5
            grid_layout.addWidget(button, row, col)
            button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            button.clicked.connect(lambda _, n=i: stack.setCurrentIndex(n + 3))
            set_button_sfx(button, self.sfx_player, "select.mp3")

        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: stack.setCurrentIndex(0))
        set_button_sfx(back_button, sfx_player, "back.mp3")
        grid_layout.addWidget(back_button, 2, 0, 1, 5)

        layout.addLayout(grid_layout)

    def set_level_as_complete(self, num):
        button = self.buttons[num - 1]
        button.completed = True
        button.apply_state_images()
        success_sound = path(f"assets/sfx/success.mp3")
        self.sfx_player.setSource(QUrl.fromLocalFile(success_sound))
        self.sfx_player.play()


class SettingsPage(QWidget):
    def __init__(self, stack, music_output, sfx_output, sfx_player, toggle_fullscreen):
        super().__init__()
        self.music_output = music_output
        self.sfx_output = sfx_output

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        right_layout = QVBoxLayout()
        main_layout.addLayout(left_layout, stretch=1)
        main_layout.addLayout(right_layout, stretch=1)

        save_data = load_save_data()

        fullscreen_checkbox = QCheckBox("Fullscreen Mode")
        if save_data["fullscreen"]:
            toggle_fullscreen(True)
            fullscreen_checkbox.setChecked(True)

        music_volume_text = RegularText("Music")
        music_volume_slider = QSlider(Qt.Orientation.Horizontal)
        music_volume = round(save_data["music_slider_value"])
        music_volume_slider.setRange(0, 100)
        # The range needs to go up to a high value so the slider actually moves smoothly
        # I would make the range 0 - 0.5 if I could (0.5+ was too loud)
        music_volume_slider.setValue(music_volume)
        self.change_music_volume(music_volume)

        sfx_volume_text = RegularText("Sound Effects")
        sfx_volume_slider = QSlider(Qt.Orientation.Horizontal)
        sfx_volume_slider.setRange(0, 100)
        sfx_volume = round(save_data["sfx_slider_value"])
        sfx_volume_slider.setValue(sfx_volume)
        self.change_sfx_volume(sfx_volume)

        back_button = QPushButton("Back")

        back_button.clicked.connect(lambda: stack.setCurrentIndex(0))
        set_button_sfx(back_button, sfx_player, "back.mp3")
        fullscreen_checkbox.toggled.connect(toggle_fullscreen)

        music_volume_slider.valueChanged.connect(self.change_music_volume)
        sfx_volume_slider.valueChanged.connect(self.change_sfx_volume)

        left_layout.addWidget(QLabel("Settings"))
        left_layout.addWidget(fullscreen_checkbox)
        left_layout.addWidget(music_volume_text)
        left_layout.addWidget(music_volume_slider)
        left_layout.addWidget(sfx_volume_text)
        left_layout.addWidget(sfx_volume_slider)
        left_layout.addWidget(back_button)

        self.setLayout(main_layout)

    def change_music_volume(self, value):
        volume = value / 200
        self.music_output.setVolume(volume)

    def change_sfx_volume(self, value):
        volume = value / 200
        self.sfx_output.setVolume(volume)