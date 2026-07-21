import json
from PyQt6.QtCore import QUrl, QObject
import os
import sys

def path(relative_path: str):
    # Get absolute path to internal game files (read only)

    if getattr(sys, 'frozen', False): # Checks if the program is running as an executable
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def get_save_path():
    # The save data needs to be written in APPDATA because the _MEIPASS folder will be deleted when the game closes
    save_file_name = "save data.json"

    if getattr(sys, 'frozen', False):
        game_name = "Dave's Algorithm Adventures"
        base_dir = os.environ.get('APPDATA')
        save_dir = os.path.join(base_dir, game_name)
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, save_file_name)

        if not os.path.exists(save_path):
            default_data = {
                "fullscreen": False,
                "music_slider_value": 50,
                "sfx_slider_value": 50,
                "levels_completed": {
                    "1": False,
                    "2": False,
                    "3": False,
                    "4": False,
                    "5": False,
                    "6": False,
                    "7": False,
                    "8": False,
                    "9": False,
                    "10": False
                }
            }

            with open(save_path, "w") as file:
                json.dump(default_data, file, indent=2)
        return save_path

    else:
        # For testing in IDE
        return save_file_name

def load_save_data():
    save_path = get_save_path()
    with open(save_path, "r") as file:
        data = json.load(file)
    return data

class SaveManager(QObject):
    def __init__(self, level_select_page, settings_page):
        super().__init__()
        self.save_path = get_save_path()
        self.level_select_page = level_select_page
        self.settings_page = settings_page

    def update_save_data(self, *keys, value):
        save_path = get_save_path()
        with open(save_path, "r") as file:
            data = json.load(file)

        current = data
        for key in keys[:-1]:
            current = current[key]
        current[keys[-1]] = value

        with open(save_path, "w") as file:
            json.dump(data, file, indent=2)


        if "levels_completed" in keys:
            # keys[-1] contains the level number as a string (e.g., "3")
            level_num = int(keys[-1])
            self.level_select_page.set_level_as_complete(level_num)


def set_button_sfx(button, sfx_player, file_name):
    file_path = path(f"assets/sfx/{file_name}")

    def play_sfx():
        sfx_player.setSource(QUrl.fromLocalFile(file_path))
        sfx_player.play()

    button.clicked.connect(play_sfx)
