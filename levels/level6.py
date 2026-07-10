from levels.base import BaseLevelPage

class Level6Page(BaseLevelPage):
    def __init__(self, back_method):
        level_info = ("Dave is back at home with his kids now who have challenged him to another game of hide and "
                      "seek. They seem to have gotten even better at hiding, so he will need to search his house much "
                      "more carefully to have any chance of finding them!\n\n"
                      "Dave now needs to use a 2D array to more accurately map out the areas of his house. Each entry "
                      "inside the array will either be True if one of his kids is in that spot or False otherwise.\n\n"
                      "Your job is to search the 2D array 'house_map' and return a list with all the index pairs where "
                      "Dave's kids can be found. Put the index pairs in a tuple as (row, column) before placing them "
                      "in your list.\n\n"
                      "Example:\n"
                      "house_map = [\n"
                      "             [False, False, False, True],\n"
                      "             [True, False, False],\n"
                      "             [False, True, False, False, False],\n"
                      "             [False, False, False]\n"
                      "             ]\n"
                      "return [(0, 3), (1, 0), (2, 1)]"
                      ""
                      )

        func_name = "search_house"
        parameters = "house_map"

        io_dict = {"[[True, False], [False, True]]": [(0, 0), (1, 1)],
                   "[[False, False], [False, False]]": [],
                   "[[True, False], [False, False, True], [False, False, False, False]]": [(0, 0), (1, 2),],
                   "[[False, False, False], [True, True, False], [False, True, False]]": [(1, 0), (1, 1), (2, 1)],
                   "[[False]]": [],
                   "[[True]]": [(0, 0)]
                   }
        # Keys are inputs, values are the expected output of the function

        super().__init__(back_method, level_info, func_name, parameters, io_dict)


"""
Solution:

def search_house(house_map):
  positions = []
  for i in range(len(house_map)):
    row = house_map[i]
    for j in range(len(row)):
      if house_map[i][j]:
        positions.append((i, j))
  return positions
  
"""
