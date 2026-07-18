from levels.base import BaseLevelPage
from PyQt6.QtCore import pyqtSignal

class Level7Page(BaseLevelPage):
    success_text = ("Your code was successful! Dave figured out that the loan sharks were offering him a horrible deal "
                    "and he declined the loan.")
    level_num = 7

    def __init__(self, sfx_player, back_method, save_data_update_method):
        level_info = ("Some loan sharks have heard about Dave's poor finances and they've come to offer him a bit of "
                      "'help'. These are the details of the loan they offer to Dave:\n\n"
                      "• The loan begins on January 1st and Dave will be paid initial_amount. This amount also becomes "
                      "the balance of his loan which he needs to pay off.\n"
                      "• On the second day of each month, Dave must pay the loan sharks back $1000 to reduce his loan "
                      "balance. If there is less than $1000 left on the balance, then he will pay whatever is left.\n"
                      "• At the end of each month, compound interest is applied to his remaining balance at "
                      "monthly_rate. This rate will be low enough so that Dave's repayments of $1000 actually "
                      "reduce the balance of the loan.\n\n"
                      "Dave needs you to make the algorithm total_interest so he can figure out the total amount of "
                      "interest he'd need to pay to the loan sharks if he accepted their loan. Round this amount to "
                      "the nearest dollar.\n\n"
                      "Example:\n"
                      "initial_amount = 8000\n"
                      "monthly_rate = 0.10\n"
                      "return 5643\n\n"
                      "The loan sharks are really scaring Dave though so he might accidentally delete some lines of "
                      "your code!"
                      )

        func_name = "total_interest"
        parameters = "initial_amount, monthly_rate"

        io_dict = {
            "500, 0.10": 0,
            "1000, 0.0": 0,
            "1500, 0.0": 0,
            "1500, 0.10": 50,
            "50000, 0.01": 18672,
            "100000, 0.01": 363817,
            "200000, 0.005": 863311,
        }
        # Keys are inputs, values are the expected output of the function

        super().__init__(level_info, func_name, parameters, io_dict, sfx_player, back_method, save_data_update_method)

    def activate_mechanic(self):
        self.editor.sabotage_mode = True
        self.editor.start_sabotage() # This won't do anything if sabotage mode is deactivated later

    def deactivate_mechanic(self):
        self.editor.sabotage_mode = False

"""
Solution:

def total_interest(initial_amount, monthly_rate):
  balance = initial_amount
  total_paid = 0

  while balance > 0:
    if balance < 1000:
      total_paid += balance
    else:
      total_paid += 1000
    balance -= 1000
    balance += balance * monthly_rate

  interest_paid = total_paid - initial_amount
  return round(interest_paid)
  
------------------------------
  
If you didn't know about the round function, you could also round to the nearest integer like this

if int(interest_paid) + 0.5 > interest_paid:
    interest_paid = int(interest_paid)
else:
    interest_paid = int(interest_paid) + 1
  
"""
