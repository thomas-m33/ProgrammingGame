from levels.base import BaseLevelPage
import os
import io
from contextlib import redirect_stdout, redirect_stderr
import tempfile


class Level8Page(BaseLevelPage):
    success_text = "Your code was successful! Dave found Gilbert's phone number and they had a great chat."
    level_num = 8

    def __init__(self, sfx_player, back_method, save_data_update_method):
        level_info = ("Dave hasn't been having much luck on Linkedin, so he's now resorting to the most reliable way "
                      "of finding a job... nepotism! One of his friends named Gilbert is a very successful man who "
                      "could surely get Dave an interview at his company.\n\n"
                      "The only problem is that Dave can't remember Gilbert's phone number. His contact info was saved "
                      "in Dave's old phone, but that phone's screen doesn't turn on anymore. Dave will instead have to "
                      "search the phone's files by plugging it into his computer.\n\n"
                      "The file on Dave's old phone that stored phone numbers was contacts.txt. Each line of this file "
                      "contains the name of a person followed by their phone number. Dave needs you to make an "
                      "algorithm that looks for the line in contacts.txt containing 'Gilbert', then have it print out "
                      "his phone number.\n\n"
                      "Example:\n"
                      "(inside contacts.txt)\n"
                      "Alice, 04915707760\n"
                      "Gilbert, 0435823049\n\n"
                      "print out '0435823049'"
                      ""
                      )

        func_name = ""
        parameters = ""

        io_dict = {
            (
                "Alice, 0491570760\n"
                "Bob, 0411111111\n"
                "Gilbert, 0435823049\n"
            ): "0435823049",

            (
                "Gilbert, 0412345678\n"
                "Bob, 0400000000\n"
            ): "0412345678",

            (
                "Alice, 0412345678\n"
                "Bob, 0423456789\n"
                "Charlie, 0434567890\n"
                "Gilbert, 0498765432\n"
            ): "0498765432",

            (
                "Tom, 0401010101\n"
                "Gilbert, 0455555555\n"
                "Emma, 0466666666\n"
                "Liam, 0477777777\n"
                "Olivia, 0488888888\n"
            ): "0455555555",

            (
                "Sarah, 0409876543\n"
                "James, 0412345678\n"
                "Gilbert, 0424681357\n"
                "Zoe, 0435792468\n"
                "Noah, 0446803579\n"
            ): "0424681357",

            (
                "Gilbert, 0400000001\n"
            ): "0400000001",
        }
        # Keys are inputs, values are the expected output of the algorithm

        super().__init__(level_info, func_name, parameters, io_dict, sfx_player, back_method, save_data_update_method)

    @staticmethod
    def run_tests(code, func_name, io_dict, success_text):
        # Change this child process's working directory to the OS temp folder
        # This guarantees the game will have write permissions, and lets the player
        # just write open("contacts.txt") in their code
        os.chdir(tempfile.gettempdir())

        for file_contents, expected_output in io_dict.items():
            with open("contacts.txt", "w") as file:  # Creates contacts.txt in the temp folder
                file.write(file_contents)
            buffer = io.StringIO()

            try:
                with redirect_stdout(buffer):
                    exec(code, {})
            except Exception as e:
                print("error:", e)
                if os.path.exists("contacts.txt"):
                    os.remove("contacts.txt")
                return

            output = buffer.getvalue().strip()

            if output != expected_output:
                print(f"Your code failed with contacts.txt as\n{file_contents}")
                print(f"Expected output: {expected_output}")
                print(f"Actual output: {output}")
                if os.path.exists("contacts.txt"):
                    os.remove("contacts.txt")
                return

            if os.path.exists("contacts.txt"):
                os.remove("contacts.txt")

        print(success_text)
        return True

    @staticmethod
    def try_code(code, stdout_queue):
        # Do the exact same thing for the testing environment
        os.chdir(tempfile.gettempdir())

        test_contacts = (
            "Alice, 0491570760\n"
            "Bob, 0411111111\n"
            "Gilbert, 0435823049\n"
            "Charlie, 0422222222\n"
        )
        buffer = io.StringIO()

        try:
            with open("contacts.txt", "w") as file:
                file.write(test_contacts)
            with redirect_stdout(buffer), redirect_stderr(buffer):
                try:
                    exec(code, {})
                except Exception as e:
                    print("error:", e)
        finally:
            if os.path.exists("contacts.txt"):
                os.remove("contacts.txt")

        stdout_queue.put(buffer.getvalue())

    def get_starting_text(self):
        return "# You don't need to write a function for this level\n"


"""
Solution:

phone_number = ""

with open("contacts.txt", "r") as file:
  for line in file:
    if "Gilbert" in line:
        for i in line:
            if i.isdigit():
                phone_number += i

print(phone_number)

"""
