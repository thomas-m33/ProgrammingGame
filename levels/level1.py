import io
from contextlib import redirect_stdout, redirect_stderr
from base import BaseLevelPage


class Level1Page(BaseLevelPage):
    def __init__(self, back_method):
        level_info = ("Dave loves to play hide and seek with his kids, but they've gotten too good at hiding recently! "
                      "He needs you to make an algorithm that will help him find them.\n\n"
                      "Each index in the list 'rooms' represents a different room of Dave's house where his kids could "
                      "be hiding. If rooms[index] == True, then at least one of his kids is at that position.\n\n"
                      "Dave needs you to program the function search_house so that it returns a list with every index "
                      "that his kids can be found at.\n\n"
                      "Example:\nrooms = [True, False, True, False]\nreturn [0, 2]"
                      )

        func_name = "search_house"
        parameters = "rooms"

        io_dict = {'[True, False, True, True, False, False]': [0, 2, 3],
                   '[False, True]': [1],
                   '[True, True, True, True]': [0, 1, 2, 3],
                   '[False]': [],
                   '[True]': [0]
                   }
        # Keys are inputs, values are the expected output of the function

        super().__init__(back_method, level_info, func_name, parameters, io_dict)

    # The user might return a list which is correct but has elements in a different order to the expected output list
    # This would return True for list1 != list2 and test_code() would think they are returning the wrong thing
    # The method is changed here so that it sorts the lists before it compares them, that way order doesn't matter
    @staticmethod
    def test_code(code, func_name, io_dict, stdout_queue):
        buffer = io.StringIO()
        with redirect_stdout(buffer), redirect_stderr(buffer):
            try:
                for args, expected_output in io_dict.items():
                    namespace = {}
                    exec(code + f"\noutput = {func_name}({args})", namespace)

                    output = namespace["output"]
                    # output was created inside exec's namespace, so must it be fetched from there

                    if sorted(output) != sorted(expected_output): # sorts the outputs (update to original function)
                        print(f"Your code failed with an input of ({args})")
                        print(f"Expected output: {expected_output}")
                        print(f"Actual output: {output}")
                        break  # Skips the else block attached to the for loop
                else:
                    print("Your code was successful! Great job on helping Dave.")
            except Exception as e:
                print("error", e)
        stdout_queue.put(buffer.getvalue())


"""
Solution:

def search_house(rooms):
	positions = []
	for i in range(len(rooms)):
		if rooms[i]:
			positions.append(i)
	return positions
	
"""
