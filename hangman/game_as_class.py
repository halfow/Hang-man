"""
Hang-a-man game 
"""
import re
import os
from random import choice
import string
import functools

import hangman.resources


class game(object):
    def __init__(self) -> None:
        """
        NOTE: Name/word could be passed as a init condition.

        NOTE: Runing a counter would be cheeper than a copy
              but this looks neat, an memory is not an issue for
              such a small application, readability should be priority.
              Also this lets me showcases some of the "be careful"
              features of python. If copy is removed, you will contine
              on the previous progress. This is as the standara model
              in python is to reference an object not copy it. Consider
              reading up on copy and deepcopy the functionality is needed.

        NOTE: Writing this as a class lets me have all the initial condition 
              placed together. This is not the case with the nested function
              version.
        """
        self.name = choice(hangman.resources.names).lower()
        assert set(self.name).issubset(string.ascii_lowercase), NameError(
            "Name contained illegal characters"
        )
        self.progress = ["_"] * len(self.name)  # Correct characters
        self.previous_guesses = set()
        self.gallow = hangman.resources.gallow.copy()
        self.scene = self.gallow.popleft()
        self.guess = self._get_user_input()  # NOTE: infinite generator

    def _get_user_input(self) -> str:
        """
        Infinity generator to get user input (character by character)

        Yields:
            [str]: yields character for user input
        """
        while True:
            for character in input("Input guess: ").lower():
                if character not in self.previous_guesses:
                    self.previous_guesses.add(character)
                    yield character
                else:
                    print(f"Ignoring Repeated character {character}")


    def _stats(self) -> None:
        """
        Clear Screen and print current game data
        """
        # Clear screen command (platform dependent)
        os.system(
            functools.lru_cache(maxsize=1)(  # NOTE: Store and reuse result
                lambda: "cls" if os.name == "nt" else "clear"
            )()
        )
        print(
            self.scene,
            "\n",
            *self.progress,
            f"\nPrevious guesses: {self.previous_guesses}",
        )

    def play(self):
        while self.gallow:
            self._stats()

            # Win check
            if "_" not in self.progress:
                break

            # Check guess
            match = None
            for match in re.finditer(next(self.guess), self.name):
                self.progress[match.start()] = match.group()

            # Wrong guess
            if match is None:
                self.scene = self.gallow.popleft()

        else:  # No break clause (if we reached last gallow image we lost)
            self._stats()
            print(f"You lost, how could you not have guessed {self.name}?")
            return 1

        # If while is broken we have avoided the death for now
        print("You made it through")
        return 0


if __name__ == "__main__":
    # Prof that multi run works
    game().play()
    game().play()
