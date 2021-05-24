"""
Hang-a-man game 
"""
import functools
import re
import os
import string
import json

from random_word import RandomWords

import hangman.resources


from random import randrange
from datetime import timedelta, datetime

def random_date():
    fmt =  r"%Y-%m-%d"
    start = datetime.strptime("2018-01-01", fmt)
    delta = datetime.now() - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    time = start + timedelta(seconds=random_second)
    return time.strftime(fmt)


def game() -> None:
    # Get random name from database
    # TODO: Pass name/word as argument instead
    name, definitions = json.loads(RandomWords().word_of_the_day(date=str(random_date()))).values()
    

    assert set(name).issubset(string.ascii_lowercase), NameError(
        "Name contained illegal characters"
    )

    # User guidense data
    # Holds possitions of known letters in the word and its length
    progress = ["_"] * len(name)
    previous_guesses = set()
    # TODO: Take a deep copy of gallow to allow for repeated games
    #       This would also make the program to not act on any data outside the current scope
    #       OBS! all instances need to be refactored 
    scene = hangman.resources.gallow.popleft()  # Current Hangman status "Picture"

    def _get_user_input() -> str:
        """
        Infinity generator to get user input (character by character)

        Yields:
            [str]: yields character for user input
        """
        while True:
            for character in input("Input guess: ").lower():
                # NOTE: previous_guesses is form the outer scope, is this okay?
                #       or is there a better way?
                if character not in previous_guesses:
                    previous_guesses.add(character)
                    yield character
                else:
                    print(f"Ignoring Repeated character {character}")

    def _stats() -> None:
        """
        Clear Screen and print current game data
        """
        # Clear screen command (platform dependent)
        # NOTE: the if case could probably be lru cashed for a little extra performance
        os.system(            
            functools.lru_cache(maxsize=1)(  # NOTE: Store and reuse
                lambda: "cls" if os.name == "nt" else "clear"
            )())
        print(
            scene,
            "\n",
            *progress,
            f"\nPrevious guesses: {previous_guesses}",
        )

    # User input character generator
    guess = _get_user_input()
    while hangman.resources.gallow:
        _stats()

        # Win check
        if "_" not in progress:
            break  # NOTE: is there a better way?

        # Check guess
        match = None
        for match in re.finditer(next(guess), name):
            progress[match.start()] = match.group()

        # Wrong guess
        if match is None:
            scene = hangman.resources.gallow.popleft()

    else:  # No break clause (if we reached last gallow image we lost)
        _stats()
        print(
            f"You lost, how could you not have guessed {name}?\n",
        json.dumps(definitions, indent=4)
        )
        return 1

    # If while is broken we have avoided the death for now
    print(
        "You made it through\n",
        json.dumps(definitions, indent=4)
    )
    return 0

if __name__ == "__main__":
    game()