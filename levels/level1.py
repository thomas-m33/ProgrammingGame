from levels.base import BaseLevelPage

class Level1Page(BaseLevelPage):
    def __init__(self, back_method):
        info = (
            "Dave is having trouble saying hello to his kids.\n\n"
            "Could you please help Dave out by printing 'Hi!' in the terminal?"
        )
        super().__init__(back_method, info)