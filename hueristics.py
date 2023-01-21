from itertools import product
from wordle_game import restrict_word_bank, evaluate_guess
from math import log2


def word_entropy(word: str, word_bank: set[str]) -> float:
    """
    Returns the entropy of a word with respect to the word bank.
    :param word: a guess word
    :param word_bank:
    :return: the entropy of the word
    """

    bank_size = len(word_bank)

    next_bank_size = {}
    for goal in word_bank:
        evaluation = evaluate_guess(word, goal)
        if evaluation not in next_bank_size:
            next_bank_size[evaluation] = 0
        next_bank_size[evaluation] += 1

    entropy = 0
    for next_size in next_bank_size.values():
        p = next_size / bank_size
        entropy -= p * log2(p)

    return entropy


def calc_positional_freqs(word_size: int, word_set: set[str]) -> list[dict[str, float]]:
    """
    Iterates through a set of (fixed size) words and creates a list of dictionaries. The dictionary in index "i" of the
    list maps letters to their frequencies in position "i" of all the words in the set.
    :param word_size: the size of each word in the set
    :param word_set: the set of words
    :return: the list of letter dictionary frequencies
    """
    positional_freqs = [{} for _ in range(word_size)]
    for word in word_set:
        for i, char in enumerate(word):
            if char in positional_freqs[i]:
                positional_freqs[i][char] += 1
            else:
                positional_freqs[i][char] = 1

    for i in range(word_size):
        for char in positional_freqs[i]:
            positional_freqs[i][char] /= len(word_set)

    return positional_freqs


def calc_letter_freqs(word_set: set[str]) -> dict[str, float]:
    """
    Iterates through a set of words and creates a dictionary of each letter to it's frequency in the set. The frequency
    is based on the number of words in the set that contain the letter, thus words containing multiple instances of a
    letter will affect the frequency the same as if they contained a single instance of the letter.
    :param word_set: the set of words
    :return: a dictionary of letters to their frequencies in the the set
    """
    letter_freqs = {}
    for word in word_set:
        seen = set()
        for char in word:
            if char not in seen:
                seen.add(char)
                if char in letter_freqs:
                    letter_freqs[char] += 1
                else:
                    letter_freqs[char] = 1

    for char in letter_freqs:
        letter_freqs[char] /= len(word_set)

    return letter_freqs


def prob_letter_match(word: str, letter_freqs: dict[str, float]) -> float:
    """
    Returns the probability that the word shares at least one letter with the goal word.
    :param word: the word to be checked
    :param letter_freqs: a dictionary mapping letters to their frequencies
    :return: a probability
    """
    seen = []
    p = 1
    for i, char in enumerate(word):
        if char not in seen:
            if letter_freqs[char] != 1:
                p *= 1 - letter_freqs[char]
                seen.append(char)
    return 1 - p


def prob_position_match(word: str, positional_freqs: list[dict[str, float]]) -> float:
    """
    Returns the probability that the word has at least one matching position with the goal word.
    :param word: the word to be checked
    :param positional_freqs: a list of dictionaries mapping letters to their frequencies
    :return: a probability
    """
    p = 1
    for i, char in enumerate(word):
        p *= 1 - positional_freqs[i][char]

    return 1 - p


def score_word(word: str, letter_freqs: dict[str, float], positional_freqs: list[dict[str, float]]) -> float:
    """
    Calculates the probability that the word will either match a find a new letter put a known letter in the correct
    position.
    :param word: the word to be checked
    :param letter_freqs: a dictionary mapping letters to their frequencies
    :param positional_freqs: a list of dictionaries mapping letters to their frequencies
    :return: a probability
    """
    seen = []
    p = 1
    for i, char in enumerate(word):
        if letter_freqs[char] == 1.0:
            if positional_freqs[i][char] < 1.0:
                p *= 1 - positional_freqs[i][char]
        elif char not in seen:
            p *= 1 - letter_freqs[char]
            seen.append(char)
    return 1 - p
