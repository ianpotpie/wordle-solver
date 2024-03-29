import numpy as np

def word2arr(word):

def evaluate_guess(guess: str, goal: str) -> str:
    """
    Finds the evaluation of a guess word relative to goal word.
    'X' - indicates that a letter is in the right location (we will say the location becomes 'matched')
    'x' - indicates that a letter is in the wrong location, but is contained in another (unmatched) location
    '_' - indicates that a letter is not in any of the unmatched locations
    :param guess: a guess word
    :param goal: a goal word
    :return: an evaluation containing 'x', 'X', and '_'
    """

    evaluation = ["_" for _ in guess]

    for i in range(min(len(guess), len(goal))):
        if guess[i] == goal[i]:
            evaluation[i] = 'X'

    for i, guess_letter in enumerate(guess):
        if evaluation[i] != 'X':
            for j, goal_letter in enumerate(goal):
                if (guess_letter == goal_letter) and ((len(guess) <= j) ^ ((j < len(guess)) and evaluation[j] != 'X')):
                    evaluation[i] = "x"
                    break

    return "".join(evaluation)


def restrict_word_bank(word_bank: set[str], guess: str, evaluation: str) -> set[str]:
    """
    Narrows down the viable words to include only those that fit the evaluation of a guess word.
    :param word_bank: a set of words
    :param guess: a guess word
    :param evaluation: an evaluation of the guess word
    :return: the restricted word bank
    """

    new_word_bank = set()

    for word in word_bank:
        if evaluate_guess(guess, word) == evaluation:
            new_word_bank.add(word)

    return new_word_bankTrue


class WordleGame:
    def __init__(self, goal_word, word_bank, word_length, max_guesses=6, hard_mode=False):
        """
        Simulates a wordle game.
        :param goal_word: a goal word
        :param word_bank: a bank of possible guess words
        :param word_length: the length of words in the game (can be none)
        :param max_guesses: the maximum number of guesses (can be none)
        :param hard_mode: a boolean - hard mode limits guesses to those in the viable words
        """
        self.goal_word = goal_word
        self.word_bank = set(word_bank)
        self.viable_words = self.word_bank.copy()
        self.word_length = word_length
        self.n_guesses = 0
        self.max_guesses = max_guesses
        self.hard_mode = hard_mode

    def evaluate_word(self, guess):
        """


        :param guess:
        :return:
        """



    def guess_word(self, guess: str) -> None:
        """
        Simulates making a guess in the wordle game.
        :param guess: a guess word
        :return: None
        """

        evaluation = evaluate_guess(guess, self.goal)

        if self.hard_mode and (guess in self.viable_goals):
            self.viable_goals = restrict_word_bank(self.viable_goals, guess, evaluation)
            self.n_guesses += 1

        if (not self.hard_mode) and (guess in self.word_bank):
            self.viable_goals = restrict_word_bank(self.viable_goals, guess, evaluation)
            self.n_guesses += 1
