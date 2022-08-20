import os
from datetime import datetime
from decimal import Decimal
import string
from file_writer import FileWriter
from thefuzz import fuzz
from game import GameModes, GameState, Scores
from user import User
from constants import SHAREBB_DIR, MOVIE_NERDS_DIR, TIME_REGEX, SIMILARITY_THRESHOLD


def set_game_answer(answer: str, state: GameState) -> None:
    if state.game_mode == GameModes.SHAREBB:
        state.answer = answer.split('Answer: ')[1:][0].lower().strip().split('/')
    elif state.game_mode == GameModes.GUESS_MOVIES:
        state.answer = [answer.split('Answer: ')[1:][0].lower().strip()]


def get_similarity_ratio(guess:str, game_answers: list[str]) -> Decimal:
    similarities = [fuzz.partial_ratio(guess, answer) for answer in game_answers]
    return max(similarities)

def is_perfect_match(guess: str, game_answers: list[str]) -> bool:
    matches = [fuzz.ratio(guess, answer) for answer in game_answers]
    return max(matches) == 100

def get_user(users: list[str], name: str) -> User:
    '''
    Get user from list of users, if it doesn't exist
    create new user and add to users list
    '''
    for user in users:
        if user.name == name:
            return user
    return None

def calculate_score(user: User, state: GameState):
    ratio = get_similarity_ratio(user.guess, state.answer)
    perfect_match = is_perfect_match(user.guess, state.answer)
    
    if ratio <= SIMILARITY_THRESHOLD:
        return
    
    user.correct_guess = True
    
    # Perfect guess
    if perfect_match and not state.perfect_guess_user:
        state.perfect_guess_user = user
        user.first_perfect_guess = True
    
    # Not perfect guess so close guesses
    if not state.close_guess_user:
        state.close_guess_user = user
        user.first_close_guess = True
    user.correct_guess_has_typos = True
    
    # For sharebite baby: Guess after team reveal
    if state.game_mode == GameModes.SHAREBB:
        user.post_team_reveal_guess = state.team_reveal
    
    user.calculate_score()

def parse_through_chat(lines: list[str], curr_user: User):
    # Get all the stats for current file
    skip_guess = False
    for index, line in enumerate(lines):
        if not line:
            continue
        
        if "Answer: " in line:
            set_game_answer(line, game_state)
            continue
        
        curr_line = line.strip()
        next_index = 0
        if index + 1 != len(lines):
            # we don't care about time
            if TIME_REGEX.fullmatch(curr_line):
                continue
            # current line is not time so it's either a person's name or a message line
            next_index = index + 1
            next_line = lines[next_index].strip()
            if TIME_REGEX.fullmatch(next_line):
                # next line is time so current line is person name
                # only care about users not in the list since only first guess counts
                if "You" == curr_line:
                    continue
                curr_user = get_user(guessed_users, curr_line)

                if not curr_user:
                    curr_user = User(curr_line)
                    guessed_users.append(curr_user)
                    skip_guess = False
                if curr_user.guess:
                    skip_guess = True
                    curr_user = None
                else:
                    skip_guess = False
            else:
                # next line isn't time so it's a message
                # Team Reveal for Sharebite baby
                if "team" in curr_line and "--" in curr_line:
                    game_state.team_reveal = True
                    continue
                if skip_guess:
                    continue
                unformatted_line = curr_line.lower()
                # if (curr_user.name == "Ben Neal"):
                #     import pdb; pdb.set_trace()
                if curr_user == None:
                    import pdb; pdb.set_trace()
                curr_user.guess = unformatted_line.translate(str.maketrans('', '', string.punctuation))
                calculate_score(curr_user, game_state)
        else:
            # last line is always a msg
            # last guess is by a user who guessed already
            if skip_guess:
                continue
            curr_user.guess = curr_line.lower()
            calculate_score(curr_user, game_state)


def reset_game(state: GameState, users: list[User], curr_user: User) -> None:
    state.reset()
    for user in users:
        user.reset()
    curr_user = None


guessed_users = list()
curr_user = None
game_state = GameState(GameModes.SHAREBB)

files = os.listdir(SHAREBB_DIR)
files.sort()
for file in files:
    reset_game(game_state, guessed_users, curr_user)
    file_name = f'{SHAREBB_DIR}{file}'
    print(f"Current file {file_name}")
    o_file = open(file_name, 'r')
    lines = o_file.readlines()
    parse_through_chat(lines, curr_user)
    o_file.close()


print('=================================')
print('name,total points,first close guess,first perfect guess')
for user in guessed_users:
    print(f'{user.name},{user.points},{user.num_first_close_guess},{user.num_first_perfect_guess}')
print('=================================')

# # Write them to the db/
# FileWriter.sort_and_write(

# # Add everything in curr file to master tracking
# for key, value in curr_users.items():
#     if key in USERS:
#         USERS[key] += value
#     else:
#         USERS[key] = value

# for key, value in curr_words.items():
#     if key in WORDS:
#         WORDS[key] += value
#     else:
#         WORDS[key] = value

# FileWriter.sort_and_write(USERS, WORDS, to_master=True)