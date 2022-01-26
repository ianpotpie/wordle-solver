# wordle-solver

This program provides suggestions for guessing words in the online game [Wordle](https://www.powerlanguage.co.uk/wordle/). It is meant to be run alongside an in-progress wordle game. Feed your guesses and hints to the program, and it will return the optimal next guesses. 

## Running the Solver:

1. Ensure that you have python installed on your system.
2. Clone the repository onto your local machine.
3. Open the terminal in the project directory.
4. Run "sh main.sh" or equivalently "python main.py".

## Project Details

### Dictionaries

This project draws from three possible word banks:

1. all english words (from https://github.com/dwyl/english-words)
2. all viable wordle guesses
3. all possible wordle answers

The lists of wordle guesses and answers can be found in the website source code. Note! The answers on the site appear in the same order as they are given in the daily challenges, so watch out for spoilers! (The dictionary in this project alphabetizes the answers).

If the list of all english words is chosen, then the user is also given the option to choose their own goal-word length. This allows the program to handle future instances of wordle, which may expand beyond 5-letter words.

### Word Scoring

This program finds the optimal guess words based on a probabilistic scoring system. The words are ranked based on the probability that they will either match an unknown letter with the goal word or match the position of a known letter with the goal word. Thus, the initial word suggestion will be solely based on common letters, but as letters are discovered the algorithm will also try to match the positions of those letters.

Within the code you can also find functions that implement scoring systems solely based on letter frequency or solely based on positional-letter frequency, but I settled a scoring heuristic the uses the probability of both. Scoring solely based on the letter frequency works fairly well, but scoring based on positional-letter frequency alone does not work well until late-game (since it often favors double-letter words and some infrequent letters).

