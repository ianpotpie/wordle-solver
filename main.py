ENGLISH_FILE = "dictionaries/english-words.txt"
GUESSES_FILE = "dictionaries/wordle-guesses.txt"
ANSWERS_FILE = "dictionaries/wordle-answers.txt"


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


def get_file_words(filepath: str) -> set[str]:
    """
    Takes in a file with text, where each line of the file is a single word. The function produces the set of all words
    in the file.
    :param filepath: a path to a file
    :return: a set of words in the file
    """
    word_set = set()
    with open(filepath, 'r') as f:
        word_set.update([word.strip() for word in f.readlines()])
        f.close()
    return word_set


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
                letter_freqs = calc_letter_freqs(possible_words)
                positional_freqs = calc_positional_freqs(word_size, possible_words)
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
                        score = score_word(word, letter_freqs, positional_freqs)
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
