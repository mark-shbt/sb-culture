import re

SHAREBB = "sharebb/"
SHAREBB_SCORE = f"{SHAREBB}scores.csv"

MOVIE_NERDS = "movie-nerds/"
MOVIE_NERDS_SCORE = f"{MOVIE_NERDS}scores.csv"

TIME_REGEX = re.compile(r"[0-9]:[0-9]+ PM")
SIMILARITY_THRESHOLD = 85
