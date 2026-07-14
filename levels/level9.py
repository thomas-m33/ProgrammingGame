from levels.base import BaseLevelPage

class Level9Page(BaseLevelPage):
    success_text = "Your code was successful! Now Dave will be moving on to the final stage of interviews."

    def __init__(self, sfx_player, back_method):
        level_info = ("Sure enough, Gilbert managed to land Dave an interview at his company! All Dave needs to do now "
                      "is answer some questions from the interviewer and he'll have a job in no time.\n\n"
                      "Unfortunately, this interviewer has some strange ways of testing candidates. He has given Dave "
                      "an algorithm to make, but he will not not tell Dave what the algorithm is supposed to do. "
                      "You will need to figure this out by analysing the feedback given to you when you press the "
                      "'Submit Solution' button.\n\n"
                      "Dave needs you to figure out what this algorithm does and then program mystery_func so that it "
                      "returns the right thing."
                      )

        func_name = "mystery_func"
        parameters = "binary_string"

        io_dict = {"'1010'": (
                        "⬜️⬛⬜️⬛"
                    ),
                   "'110110000011011'": (
                        "⬜️⬜️⬛⬜️⬜️\n"
                        "⬛⬛⬛⬛⬛\n"
                        "⬜️⬜⬛⬜⬜️"
                   ),
                   "'0111011111111110111000100'": (
                       "⬛⬜️⬜️⬜️⬛\n"
                       "⬜️⬜️⬜️⬜️⬜️\n"
                       "⬜️⬜️⬜️⬜️⬜️\n"
                       "⬛⬜️⬜️⬜️⬛\n"
                       "⬛⬛⬜️⬛⬛"
                   ),
                   "'0111010001101011000101110'": (
                       "⬛⬜️⬜️⬜️⬛\n"
                       "⬜️⬛⬛⬛⬜️\n"
                       "⬜️⬛⬜️⬛⬜️\n"
                       "⬜️⬛⬛⬛⬜️\n"
                       "⬛⬜️⬜️⬜️⬛"
                   ),
                   "'0010000100111110010000100'": (
                       "⬛⬛⬜️⬛⬛\n"
                       "⬛⬛⬜️⬛⬛\n"
                       "⬜️⬜️⬜️⬜️⬜️\n"
                       "⬛⬛⬜️⬛⬛\n"
                       "⬛⬛⬜️⬛⬛"
                   ),
                   "'0010001110111110111000100'": (
                       "⬛⬛⬜️⬛⬛\n"
                       "⬛⬜️⬜️⬜️⬛\n"
                       "⬜️⬜️⬜️⬜️⬜️\n"
                       "⬛⬜️⬜️⬜️⬛\n"
                       "⬛⬛⬜️⬛⬛"
                   ),
                   "'0101001010000001000101110'": (
                       "⬛⬜️⬛⬜️⬛\n"
                       "⬛⬜️⬛⬜️⬛\n"
                       "⬛⬛⬛⬛⬛\n"
                       "⬜️⬛⬛⬛⬜️\n"
                       "⬛⬜️⬜️⬜️⬛"
                  ),
        }
        # Keys are inputs, values are the expected output of the function

        super().__init__(level_info, func_name, parameters, io_dict, sfx_player, back_method)

    def get_starting_text(self):
        return ("# Hint: Try writing pass inside the function to make it do nothing\n# Then press 'Submit Solution' "
                f"to see an example\n\ndef {self.func_name}({self.parameters}):")


"""
Solution:

def mystery_func(binary_string):
  count = 0
  grid = ""
  for i in binary_string:
    count += 1
    if int(i):
      grid += "⬜️"
    else:
      grid += "⬛"
    if count % 5 == 0:
      grid += "\n"
  return grid
  
"""
