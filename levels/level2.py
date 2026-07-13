from levels.base import BaseLevelPage

class Level2Page(BaseLevelPage):
    success_text = "Your code was successful! Dave's boss liked the algorithm, but he still had some bad news..."

    def __init__(self, back_method):
        level_info = ("Dave has a job at the bank. This bank has recently been working on a new way to verify "
                      "transactions by looking at the digits of their transaction ID. As part of this system, "
                      "they need an algorithm that finds the sum of the digits in a number.\n\n"
                      "Dave has been chosen as the employee to make this algorithm, but his boss is a very picky man! "
                      "He will not accept the algorithm if it is over six lines long (including the function "
                      "definition).\n\n"
                      "You will need to program the function sum_digits in six or less lines so that it returns the "
                      "sum of the digits in num. Note that num will be a positive integer.\n\n"
                      "Example:\n"
                      "num = 123\n"
                      "return 6\n\n"
                      )

        func_name = "sum_digits"
        parameters = "num"

        io_dict = {'310': 4,
                   '14744': 20,
                   '1': 1,
                   '4342959325': 46,
                   '235421187': 33
                   }
        # Keys are inputs, values are the expected output of the function

        super().__init__(back_method, level_info, func_name, parameters, io_dict)

"""
Solution:

def sum_digits(num):
  sum = 0
  while num > 0:
    sum += num % 10
    num = num // 10
  return sum
  
------------------------------

Alternatively:

def sum_digits(num):
  digits = [int(digit) for digit in str(num)]
  return sum(digits)

"""

# Solution must be 6 lines or less
# Extra lines that the user inserts are highlighted red in the editor
