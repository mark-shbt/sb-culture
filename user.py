from game import Scores


class User:
    def __init__(
        self,
        name,
        points: int = 0,
        first_close_guess: int = 0,
        first_perfect_guess: int = 0,
    ):
        self.name = name
        self.points = points
        self.correct_guess = False
        self.first_close_guess = False
        self.first_perfect_guess = False
        self.correct_guess_has_typos = False
        self.post_team_reveal_guess = False
        self.guess = ""
        self.num_first_close_guess = first_close_guess
        self.num_first_perfect_guess = first_perfect_guess

    def __str__(self):
        return f"{self.name}, {self.points}"

    def reset(self):
        self.guess = ""
        self.correct_guess = False
        self.first_close_guess = False
        self.first_perfect_guess = False
        self.correct_guess_has_typos = False
        self.post_team_reveal_guess = False

    def calculate_score(self) -> int:
        """
        Scoring system:
        +5 points per correct guess (with or without typos)
        +5 points if you're the first close enough
        +5 points for the first spelling
        -2 points if your guess is correct but has typos or doesn't match the full spelling (eg missing or having extra 'the' in the title)
        And for guessing baby
        +5 points if you guessed before the team is revealed
        +3 points if you guessed after the team is revealed
        """
        if not self.correct_guess:
            return self.points

        gained_points = 0

        # For Sharebite Babies
        if self.post_team_reveal_guess:
            gained_points += Scores.POST_TEAM_REVEAL_GUESS
        else:
            gained_points += Scores.CORRECT_GUESS

        if self.correct_guess_has_typos:
            gained_points += Scores.CORRECT_GUESS_HAS_TYPOS

        if self.first_close_guess:
            gained_points += Scores.FIRST_CLOSE_GUESS
            self.num_first_close_guess += 1

        if self.first_perfect_guess:
            gained_points += Scores.FIRST_PERFECT_GUESS
            self.num_first_perfect_guess += 1

        # print(f'{self.name} guessed {self.guess} correctly. Gained: {gained_points}, total points: {self.points}, first close guess: {self.first_close_guess}, perfect guess: {self.first_perfect_guess}')

        self.points += gained_points

        return self.points
