import os
from datetime import datetime
from decimal import Decimal
import string
from file_io import FileIO
from thefuzz import fuzz
from game import GameModes, GameState
from user import User
from constants import MOVIE_NERDS, SHAREBB, TIME_REGEX, SIMILARITY_THRESHOLD


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
    if perfect_match:
        if not state.perfect_guess_user:
            state.perfect_guess_user = user
            user.first_perfect_guess = True
    else:
        # Not perfect guess so close guesses
        if not state.close_guess_user:
            state.close_guess_user = user
            user.first_close_guess = True
        user.correct_guess_has_typos = True
    
    # For sharebite baby: Guess after team reveal
    if state.game_mode == GameModes.SHAREBB:
        user.post_team_reveal_guess = state.team_reveal
    
    user.calculate_score()

def parse_through_chat(lines: list[str], users_list: list[User], game_state: GameState):
    # Get all the stats for current file
    skip_guess = False
    curr_user = None
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
                curr_user = get_user(users_list, curr_line)

                if not curr_user:
                    curr_user = User(curr_line)
                    users_list.append(curr_user)
                    skip_guess = False
                if curr_user.guess:
                    skip_guess = True
                    curr_user = None
                else:
                    skip_guess = False
            else:
                # next line isn't time so it's a message
                # Team Reveal for Sharebite baby
                if game_state.game_mode == GameModes.SHAREBB:
                    if "team" in curr_line and "--" in curr_line:
                        game_state.team_reveal = True
                        continue
                if skip_guess:
                    continue
                unformatted_line = curr_line.lower()
                curr_user.guess = unformatted_line.translate(str.maketrans('', '', string.punctuation))
                calculate_score(curr_user, game_state)
        else:
            # last line is always a msg
            # check if last guess is by a user who guessed already
            if skip_guess:
                continue
            curr_user.guess = curr_line.lower()
            calculate_score(curr_user, game_state)


def reset_game(state: GameState, users: list[User]) -> None:
    state.reset()
    for user in users:
        user.reset()

def get_dir_name(game_state: GameState) -> list[str]:
    if game_state.game_mode == GameModes.SHAREBB:
        return SHAREBB
    if game_state.game_mode == GameModes.GUESS_MOVIES:
        return MOVIE_NERDS

def load_users(file_name: str) -> list[User]:
    users_list = []
    csv_file = open(file_name, 'r')
    csv_file.readline()
    lines = csv_file.readlines()
    for line in lines:
        user_info = line.split(',')
        user = User(user_info[0], int(user_info[1]), int(user_info[2]), int(user_info[3]))
        users_list.append(user)
    return users_list


game_modes = [GameModes.SHAREBB, GameModes.GUESS_MOVIES]

for game_mode in game_modes:
    game_state = GameState(game_mode)

    dir_name = get_dir_name(game_state)
    scores_file = f"{dir_name}scores.csv"
    all_dirs = os.listdir(dir_name)
    users_list = load_users(scores_file)
    all_dirs.sort()
    # after sorting, scores.csv will always be last so get the latest folder
    working_dir = all_dirs[-2]
    # get all the files in the working_dir
    files = os.listdir(f'{dir_name}{working_dir}')

    for file in files:
        reset_game(game_state, users_list)
        file_name = f'{dir_name}{working_dir}/{file}'
        o_file = open(file_name, 'r')
        lines = o_file.readlines()
        parse_through_chat(lines, users_list, game_state)
        o_file.close()

    sorted_users = sorted(users_list, key=lambda u: (u.name))
    FileIO.write_to_file(sorted_users, scores_file)