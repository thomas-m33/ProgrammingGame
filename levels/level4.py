from levels.base import BaseLevelPage
import io
from contextlib import redirect_stdout, redirect_stderr
import random

class Level4Page(BaseLevelPage):
    success_text = "Your code was successful! Dave unlocked the door and sneaked his way into the store..."

    def __init__(self, sfx_player, back_method):
        level_info = ("Dave can't afford a present for his son's birthday this week because he lost his job. He would "
                      "never let his kids down though, so he's going to get his son a present by stealing it from the "
                      "store. Dave plans to show up in the dead of night, pick the lock on the store's door and quickly "
                      "grab a toy before anyone notices!\n\n"
                      "The store's lock has five pins which can each either be raised (True) or lowered (False). The "
                      "pin arrangement needed to unlock the lock can be represented as a list (e.g. [True, False, True,"
                      " True, False], and the function pick_pin(index) returns the value of a pin at a given index of "
                      "this list. For example if the first pin was raised, then pick_pin(0) would return True.\n\n"
                      "Dave needs you to program the function pick_lock to help him pick this lock. It should get the "
                      "values of the pins using pick_pin and return them in a list like [False, False True...].\n\n"
                      "Also, since it is so dark outside, lines in your code will go dark once you press enter on "
                      "them!"
                      )

        func_name = "pick_lock"
        parameters = ""

        values_list = [
            [True, False, True, False, True],
            [False, False, True, True, False],
            [True, True, True, False, False],
            [False, True, False, True, False],
            [True, False, False, True, True],
            [True, True, True, True, True],
            [False, False, False, False, False]
        ]
        # These lists are used to both create the pick_pin function and test the user's algorithm

        super().__init__(level_info, func_name, parameters, values_list, sfx_player, back_method)

    def build_ui(self):
        super().build_ui()
        self.editor.obscure_mode = True

    @staticmethod
    def try_code(code, stdout_queue):
        buffer = io.StringIO()
        def pick_pin(index):
            arrangement = [random.choice([True, False]) for i in range(5)] # For the player to use during testing
            return arrangement[index]

        with redirect_stdout(buffer), redirect_stderr(buffer):  # Errors and print statements redirected to buffer
            try:
                exec(code, {"pick_pin": pick_pin})
            except Exception as e:
                print("error:", e)
        stdout_queue.put(buffer.getvalue())

    @staticmethod
    def run_tests(code, func_name, values_list, success_text):
        for arrangement in values_list:
            def pick_pin(index):
                return arrangement[index]

            namespace = {"pick_pin": pick_pin}
            exec(code + f"\noutput = {func_name}()", namespace)
            output = namespace["output"]
            # output was created inside exec's namespace, so must it be fetched from there

            if output != arrangement:
                print(f"Your code failed with pins 0 = {arrangement[0]}, 1 = {arrangement[1]}, "
                      f"2 = {arrangement[2]}, 3 = {arrangement[3]} and 4 = {arrangement[4]}.")
                print(f"Expected output: {arrangement}")
                print(f"Actual output: {output}")
                return

        print(success_text)

    def get_starting_text(self):
        return f"# pick_pin(index) is defined elsewhere\n\ndef {self.func_name}({self.parameters}):"

"""
Solution:

def pick_lock():
  arrangement = []
  for i in range(5):
    arrangement.append(pick_pin(i))
  return arrangement
  
"""
