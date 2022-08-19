import re
from file_writer import FileWriter
from thefuzz import fuzz

SHAREBB_DIR = 'sharebb/2022-08-18/'
MOVIE_NERDS_DIR = 'movie-nerds/2022-08-18/'


TIME_REGEX = re.compile(r'[0-9]:[0-9]+ PM')
curr_users = {}
curr_words = {}

file = open(FILE_NAME, 'r')
lines = file.readlines()

# Get all the stats for current file
for index, line in enumerate(lines):
    if not line:
        continue
    curr_line = line.strip()
    next_index = 0
    if index + 1 != len(lines):
        if not TIME_REGEX.fullmatch(curr_line):
            # current line is not time so it's either a person's name or a message line
            # otherwise continue
            next_index = index + 1
            next_line = lines[next_index].strip()
            if TIME_REGEX.fullmatch(next_line):
                # next line is time so current line is person name
                if curr_line in curr_users:
                    curr_users[curr_line] += 1
                else:
                    curr_users[curr_line] = 1
            else:
                # next line isn't time so it's a message
                add_to_words(curr_line, curr_words)
    else:
        add_to_words(curr_line, curr_words)

# Write them to the db/
FileWriter.sort_and_write(curr_users, curr_words, to_master=False)

# Add everything in curr file to master tracking
for key, value in curr_users.items():
    if key in USERS:
        USERS[key] += value
    else:
        USERS[key] = value

for key, value in curr_words.items():
    if key in WORDS:
        WORDS[key] += value
    else:
        WORDS[key] = value

FileWriter.sort_and_write(USERS, WORDS, to_master=True)