from utilities_wordle import *
from utilities_decision_tree import *

ENGLISH_FILE = "dictionaries/english-words.txt"
GUESSES_FILE = "dictionaries/wordle-guesses.txt"
ANSWERS_FILE = "dictionaries/wordle-answers.txt"


def repl() -> None:
    """
    Runs the repl for the world solver.
    :return: Nothing
    """
    state: str = "select-dict"
    word_size: int = 0
    guess: str = ""
    n_guesses = 0
    possible_words: set[str] = set()

    try:
        while True:

            if state == "select-dict":
                print(f"Which set of words are you using? ")
                print("1. all english words")
                print("2. valid wordle guesses")
                print("3. possible wordle answers")
                _in = input("Enter 1, 2, or 3: ")
                try:
                    try:
                        dict_num = int(_in)
                    except ValueError:
                        raise ValueError(f"{_in} is not a valid integer")
                    if (dict_num < 1) or (3 < dict_num):
                        raise ValueError(f"{dict_num} is not 1, 2, or 3")
                except ValueError as e:
                    print(e)
                else:
                    if dict_num == 1:
                        possible_words = get_file_words(ENGLISH_FILE)
                        state = "get-word-size"
                    if dict_num == 2:
                        possible_words = get_file_words(GUESSES_FILE)
                        possible_words.update(get_file_words(ANSWERS_FILE))
                        word_size = 5
                        state = "suggest-words"
                    if dict_num == 3:
                        possible_words = get_file_words(ANSWERS_FILE)
                        word_size = 5
                        state = "suggest-words"

            # wordle words are all length 5, so we can skip this step with the wordle dicts
            if state == "get-word-size":
                _in = input("What is the size of your goal word? ")
                try:
                    try:
                        word_size = int(_in)
                    except ValueError:
                        raise ValueError(f"{_in} is not a valid integer")
                    if word_size < 1:
                        raise ValueError(f"size cannot be less than 1")
                except ValueError as e:
                    print(e)
                else:
                    for word in possible_words.copy():
                        if len(word) != word_size:
                            possible_words.remove(word)
                    state = "suggest-words"

            if state == "suggest-words":
                n_suggestions = 10
                if len(possible_words) == 0:
                    print("there are no viable words left to suggest")
                    state = "terminal"
                if len(possible_words) == 1:
                    print(f"the only word left is {possible_words.pop()}!")
                    state = "terminal"
                else:
                    best_words = []
                    for word in possible_words:
                        score = get_optimal_expected_word(word, possible_words)
                        best_words.append((score, word))
                        best_words.sort(reverse=True)
                        if len(best_words) > n_suggestions:
                            best_words.pop(-1)
                    print("Best words:")
                    for i, (score, word) in enumerate(best_words):
                        print(f"{i + 1}. {word} -> score: {score}")
                    state = "guess-word"

            if state == "guess-word":
                _in = input("Guess a word: ")
                guess = _in.strip()
                try:
                    if not guess.isalpha():
                        raise ValueError(f"{guess} contains non-alpha characters")
                    if len(guess) != word_size:
                        raise ValueError(f"{guess} does not have a length {word_size}")
                    if guess not in possible_words:
                        raise ValueError(f"{guess} is not one of the remaining possible words")
                except ValueError as e:
                    print(e)
                else:
                    n_guesses += 1
                    state = "evaluate-word"

            if state == "evaluate-word":
                print("type \"X\" if a letter was in the correct location")
                print("type \"x\" if a letter is in the word, but in the incorrect location")
                print("type \"_\" if a letter is not in the word")
                _in = input("Enter word evaluation: ")
                evaluation = _in.strip()
                try:
                    if len(evaluation) != word_size:
                        raise ValueError(f"evaluation string must have a length of {word_size}")
                    for char in evaluation:
                        if char not in ["X", "x", "_"]:
                            raise ValueError(f"{char} is not a valid evaluation character")
                except ValueError as e:
                    print(e)
                else:
                    if evaluation == (word_size * "X"):
                        print("Congrats! You found the goal word")
                        state = "terminal"
                    else:
                        for i, char in enumerate(evaluation):
                            if char == "X":
                                for word in possible_words.copy():
                                    if word[i] != guess[i]:
                                        possible_words.remove(word)
                            if char == "x":
                                for word in possible_words.copy():
                                    if (word[i] == guess[i]) or (guess[i] not in word):
                                        possible_words.remove(word)
                            if char == "_":
                                for word in possible_words.copy():
                                    if guess[i] in word:
                                        possible_words.remove(word)
                        state = "suggest-words"

            if state == "terminal":
                _in = input("press ctrl-c to quit or enter \"r\" to restart: ")
                if _in == "r":
                    state = "select-dict"
                    n_guesses = 0

    except KeyboardInterrupt:
        print("\nExiting...")


if __name__ == '__main__':
    print()
    print("Welcome to WORDLE solver")
    print("ctrl-c to quit")
    print()
    repl()
