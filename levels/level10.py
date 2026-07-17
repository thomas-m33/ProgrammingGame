from levels.base import BaseLevelPage

class Level10Page(BaseLevelPage):
    success_text = ("Your code was successful! Dave passed the interview and finally managed to land a job. His "
                    "days of buying the cheapest bread are over!")

    def __init__(self, sfx_player, back_method):
        level_info = ("Dave has made it to the final interview and he just needs to answer one more question to get "
                      "the job.\n\n"
                      "The algorithm that Dave needs to make is a random password generator. It needs to randomly "
                      "create a password that satisfies the following requirements:\n"
                      "• Longer than 8 characters\n"
                      "• Contains at least 1 special character\n"
                      "• Contains exactly 2 numerical characters\n"
                      "• Ends with a capital letter\n\n"
                      "Dave needs your help one last time!. You will need to program the function create_password so "
                      "that it returns a randomly generated password satisfying all these requirements.\n\n"
                      "Example:\n"
                      "return '4p%9aFSeW'"
                      )

        func_name = "create_password"
        parameters = ""

        io_dict = {
                   }
        # Keys are inputs, values are the expected output of the function

        super().__init__(level_info, func_name, parameters, io_dict, sfx_player, back_method)

    @staticmethod
    def run_tests(code, func_name, _, success_text):
        namespace = {}
        exec(code, namespace)

        create_password = namespace[func_name]
        output_collector = []
        feedback = None
        capital_letters = "QWERTYUIOPASDFGHJKLZXCVBNM"
        special_chars = """~!@#$%^&*()_+`-=[]\;',./{}|:"<>?"""

        for i in range(50):
            output = create_password()
            if type(output) is not str:
                feedback = f"Your algorithm returned something that isn't a string ({output})."
                break
            if len(output) <= 8:
                feedback = f"Your algorithm generated a password which didn't have more than 8 characters ({output})."
                break
            if set(output).isdisjoint(special_chars):
                feedback = f"Your algorithm generated a password with no special characters ({output})."
                break
            if sum(char.isdigit() for char in output) != 2:
                feedback = (f"Your algorithm generated a password which didn't have exactly 2 numeric characters "
                            f"({output}).")
                break
            if output[-1] not in capital_letters:
                feedback = (f"Your algorithm generated a password where the last character wasn't a capital letter "
                            f"({output}).")
                break
            output_collector.append(output)

        if feedback is None:
            # The algorithm will now check whether the user's passwords are actually being randomly generated

            same_indices_data = [(i, chars[0]) for i, chars in enumerate(zip(*output_collector)) if
                                 len(set(chars)) == 1]
            # Finds characters which are in the same index across every password (not being randomly placed)

            char_sets = [set(s) for s in output_collector]
            char_union = set.union(*char_sets)
            char_intersection = set.intersection(*char_sets)
            # Used for checking if all passwords are just rearrangements of the same few characters

            if same_indices_data:
                if len(same_indices_data) == 1:
                    index, char = same_indices_data[0]
                    feedback = f"All your passwords have the same character ('{char}') at index {index}."
                else:
                    # Build details like "index 0 ('A'), index 4 ('!') and index 8 ('X')"
                    details = [f"index {index} ('{char}')" for index, char in same_indices_data]
                    formatted_details = ", ".join(details[:-1]) + " and " + details[-1]
                    feedback = f"All your passwords have the same character at {formatted_details}."
            elif char_union == char_intersection:
                feedback = f"All your passwords have the same characters {tuple(char_union)}."
                # This converts char_union to a tuple so the characters will be in round brackets

        if feedback is not None:
            print("Tests failed:", feedback)
        else:
            print(success_text)

    def get_starting_text(self):
        return f"import random\n\ndef {self.func_name}({self.parameters}):"


"""
Solution:

import random

def create_password():
  letters = "qwertyuiopasdfghjklzxcvbnm"
  special_chars = "!@#$%^&*()"
  digits = "0123456789"
  included_chars = []

  included_chars.append(random.choice(special_chars))
  for i in range(2):
    included_chars.append(random.choice(digits))
  for i in range(5):
    included_chars.append(random.choice(letters + letters.upper() + special_chars))

  random.shuffle(included_chars) 
  password = "".join(included_chars)
  password += random.choice(letters.upper())
  return password

"""
