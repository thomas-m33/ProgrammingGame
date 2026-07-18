from levels.base import BaseLevelPage

class Level1Page(BaseLevelPage):
    success_text = "Your code was successful! Dave finally won a game of hide and seek against his kids."
    level_num = 1

    def __init__(self, sfx_player, back_method, save_data_update_method):
        level_info = ("Dave loves to play hide and seek with his kids, but they've gotten too good at hiding recently! "
                      "He needs you to make an algorithm that will help him find them.\n\n"
                      "Each index in the list rooms represents a different room of Dave's house where his kids could "
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

        super().__init__(level_info, func_name, parameters, io_dict, sfx_player, back_method, save_data_update_method)


"""
Solution:

def search_house(rooms):
	positions = []
	for i in range(len(rooms)):
		if rooms[i]:
			positions.append(i)
	return positions
	
"""
