class Scores:
    CORRECT_GUESS = 5
    FIRST_CLOSE_GUESS = 5
    FIRST_PERFECT_GUESS = 5
    CORRECT_GUESS_HAS_TYPOS = -2

    # for sharebite babies
    POST_TEAM_REVEAL_GUESS = 3


class GameModes:
    SHAREBB = "Sharebite Babies"
    GUESS_MOVIES = "Guess The Movie"


class GameState:
    def __init__(self, game_mode: str):
        self.team_reveal = False
        self.close_guess_user = None
        self.perfect_guess_user = None
        self.answer = []
        self.game_mode = game_mode

    def reset(self):
        self.team_reveal = False
        self.close_guess_user = None
        self.perfect_guess_user = None
        self.answer = []
