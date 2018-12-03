from cozmo_taste_game import RealTasterBot


class TasteGameEngine:

    def __init__(self, items, bot: RealTasterBot):
        self.bot = bot
        self.items = items

