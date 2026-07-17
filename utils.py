from PyQt6.QtCore import QUrl
import os


def true_path(relative_path):
    pass


def set_button_sfx(button, sfx_player, file_name):
    file_path = os.path.abspath(f"assets/sfx/{file_name}")

    def play_sfx():
        sfx_player.setSource(QUrl.fromLocalFile(file_path))
        sfx_player.play()

    button.clicked.connect(play_sfx)