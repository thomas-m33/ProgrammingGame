from levels.base import BaseLevelPage

class Level1Page(BaseLevelPage):
    def __init__(self, back_method):
        level_info = (
            "Dave is having trouble saying hello to his kids.\n\n"
            "Could you please help Dave out by returning 'Hi!' from this function?"
        )
        func_name = "say_hi"
        parameters = ""
        io_dict = {"": "Hi!"}
        super().__init__(back_method, level_info, func_name, parameters, io_dict)