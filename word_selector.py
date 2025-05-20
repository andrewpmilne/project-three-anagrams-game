import string
import random


class WordSelector:
    """
    Selects a word from words.txt.
    Ensures correct length for the difficulty setting.
    Jumbles up the letters in the word.
    """
    def __init__(self, filepath="words.txt"):
        with open(filepath, "r") as file:
            raw_words = [word.strip().lower() for word in file]
            self.words = [
                word for word in raw_words
                if all(char not in string.punctuation for char in word)
            ]

    def get_word_by_difficulty(self, difficulty):
        if difficulty == "e":
            valid_words = [w for w in self.words if len(w) == 6]
        elif difficulty == "m":
            valid_words = [w for w in self.words if len(w) in (7, 8)]
        elif difficulty == "h":
            valid_words = [w for w in self.words if len(w) in (9, 10)]
        else:
            valid_words = []

        return random.choice(valid_words) if valid_words else None

    def jumble_word(self, word):
        letters = list(word)
        random.shuffle(letters)
        return ''.join(letters)
