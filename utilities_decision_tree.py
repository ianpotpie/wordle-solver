from wordle_game import evaluate_guess, restrict_word_bank


def worstcase_guess_number(goal: str, word_bank: set[str]) -> int:
    """
    Given a fixed goal word and a word_bank of possible guesses, returns the maximum number of possible guesses before
    reaching the goal word.
    :param goal: the fixed goal word
    :param word_bank: the word bank of possible guesses
    :return: the most possible guesses before reaching the goal word
    """
    n_words = len(word_bank)

    if n_words <= 1:
        return 1
    else:
        max_guesses = 1
        for guess in word_bank:
            if guess != goal:
                evaluation = evaluate_guess(guess, goal)
                next_word_bank = restrict_word_bank(word_bank, evaluation, guess)
                n_guesses = 1 + worstcase_guess_number(goal, next_word_bank)
                max_guesses = min(max_guesses, n_guesses)
        return max_guesses


def optimal_worstcase(word_bank: set[str]) -> int:
    """
    Given a word bank, find the best-possible number of guesses assuming the worst-case goal word.
    :param word_bank: a set of strings
    :return: an integer indicating the worst-case number of guesses in an optimally-chosen game
    """
    n_words = len(word_bank)
    if n_words <= 1:
        return 1  # if there is only one element in the bank, then we can always win the game with one guess
    else:
        minmax_guesses = n_words
        for guess in word_bank:  # loop finds the guess which will give us the best worst-case goal
            max_guesses = 1  # the worst-case number of optimally-chosen guesses (out of all possible goals)
            for goal in word_bank:
                if guess != goal:
                    evaluation = evaluate_guess(guess, goal)
                    next_word_bank = restrict_word_bank(word_bank, evaluation, guess)
                    max_guesses = max(max_guesses, 1 + optimal_worstcase(next_word_bank))
            minmax_guesses = min(max_guesses, minmax_guesses)

        return minmax_guesses


def guess_optimal_worstcase(guess: str, word_bank: set[str]) -> int:
    """
    Given an initial guess and a word bank, find the expected number guesses that it would take for an agent to guess a
    goal word. Assume that an adversarial agent can change the goal word to maximize the number of guesses we must make
    and our agent makes the optimal decision at every point.
    :param guess: an initial guess
    :param word_bank: a set of strings
    :return: an integer indicating the worst-case number of guesses in an optimally-chosen game
    """

    max_guesses = 1
    for goal in word_bank:
        evaluation = evaluate_guess(guess, goal)
        next_word_bank = restrict_word_bank(word_bank, evaluation, guess)
        max_guesses = max(max_guesses, 1 + guess_optimal_worstcase(next_word_bank))

    return max_guesses


def get_optimal_expected(word_bank: set[str], depth=0) -> float:
    """
    Given a word bank, find the expected number of guesses that it would take for an agent to guess a goal word. Assume
    that all words are on a uniform distribution and our agent makes the optimal choice at each step (picks the word
    with the minimum "optimal expected guesses" at each step).
    :param word_bank: a set of strings
    :return: a tuple of number of guesses, and a number of
    """

    print(depth)
    print(word_bank)

    n_words = len(word_bank)

    if n_words <= 1:
        return 1  # if there is one word, then we can win in one guess

    else:
        min_expected_guesses = n_words  # the worst-case max is guessing all words in the word bank
        for guess in word_bank:
            expected_guesses = 0
            for goal in word_bank:
                evaluation = evaluate_guess(guess, goal)
                next_word_bank = restrict_word_bank(word_bank, evaluation, guess)
                expected_guesses += get_optimal_expected(next_word_bank, depth + 1) / n_words
                if expected_guesses >= min_expected_guesses:  # no need to calculate more if it surpasses the minimum
                    break
            min_expected_guesses = min(min_expected_guesses, expected_guesses)

        return 1 + min_expected_guesses


def get_optimal_expected_word(guess: str, word_bank: set[str]):
    """
    Given an initial guess and a word bank, find the expected number of guesses that it would take for an agent to guess
    a goal word. Assume that all words are on a uniform distribution and our agent makes the optimal choice at each step
    (picks the word with the minimum "optimal expected guesses" at each step).
    :param guess: a fixed initial guess
    :param word_bank: a set of strings
    :return: an expected number of guesses (a real number)
    """

    n_words = len(word_bank)

    expected_guesses = 0
    for goal in word_bank:
        evaluation = evaluate_guess(guess, goal)
        next_word_bank = restrict_word_bank(word_bank, evaluation, guess)
        expected_guesses += get_optimal_expected(next_word_bank) / n_words

    return expected_guesses
