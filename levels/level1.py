from levels.base import BaseLevelPage

class Level1Page(BaseLevelPage):
    def __init__(self, on_back):
        info = (
            "Dave is having trouble saying hello to his kids.\n\n"
            "Could you please help Dave out by printing 'Hi!' in the terminal?"
        )
        super().__init__(on_back, info)