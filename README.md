# sb-culture
Keep track of scoring system used in thurs all hands

Scores for Sharebite Baby is [here](sharebb/scores.csv)

Scores for Guessing Movie is [here](movie-nerds/scores.csv)

# The Parser
The parser goes through the chat messages and will mark the first message sent by the user as a guess. Any subsequent messages by the same user within the same guessing round will be discarded. So please don't send any unnecessary messages while the guessing period is open!

# Scoring System
The scoring system is implemented as following:
* +5 points per correct guess
* +5 points if you’re the first close enough ***
* +5 points for the first perfect spelling guess ***
* -2 points if your guess is correct but has typos or doesn’t match the full spelling (eg missing or having extra ‘the’ in the title)

> ***A guess is considered "close enough" if the `parital_ratio` algorithm of [thefuzz](https://pypi.org/project/thefuzz/) returns a score of `85` or higher
> 
> ***If no one has qualified for the "first close enough" guess and you're the first to provide a perfect guess, you'll be automatically awarded +5 points for the "first close enough" guess as well
> 
> In any game, the maximum possible points you can receive is 15 points and the minimum possible points (if you guessed correctly) is 1 point

## Sharebite Baby Specific Scoring/Rules
* +3 points instead of +5 for the correct guess if you guessed after the team is revealed