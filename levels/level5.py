from levels.base import BaseLevelPage

class Level5Page(BaseLevelPage):
    def __init__(self, back_method):
        level_info = ("Uh oh. Dave accidentally set off an alarm on his way out of the store and now the police are "
                      "coming to question him... Not to worry though. He is a very clever man and has thought up a "
                      "genius way to outsmart the cops.\n\n"
                      "If the police ask Dave a question which contains the word 'steal' in any way (including as part "
                      "of another word), then he will respond 'No'. Otherwise, he will respond 'Yes'.\n\n"
                      "Dave will respond to all the police's questions using the answer function. This function "
                      "will be passed a string (question) and should return either 'Yes' or 'No' "
                      "depending on if that string contains the word 'steal'. Dave needs you to program this function "
                      "according to his master plan so he can get back to his kids with the present.\n\n"
                      "Example:\n"
                      "question = 'Were you stealing something from here?'\n"
                      "return 'No'"
                      )

        func_name = "answer"
        parameters = "question"

        io_dict = {"Is your name Dave?": "Yes",
                   "Did you steal from here?": "No",
                   "How was your day?": "Yes",
                   "You're a thief aren't you.": "Yes",
                   "Did you know stealing is against the law?": "No",
                   "Stealing is what you spend your time doing?": "No"
                   }
        # Keys are inputs, values are the expected output of the function

        super().__init__(back_method, level_info, func_name, parameters, io_dict)


"""
Solution:

def answer(question):
  start_index = 0
  stop_index = 5

  while end_index <= len(question):
    if question[start_index : stop_index].lower() == "steal":
      return "Yes"
    start_index += 1
    stop_index += 1
  return "No"
  

This can be done much more efficiently if you know how to use the 'in' keyword on a string

def answer(question):
  if "steal" in question.lower():
    return "Yes"
  else:
    return "False"

"""
