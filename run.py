import random

def welcome_message():
    """
    Introduces the player to the game and asks if they want to read the rules.
    """
    print("Welcome to the Anagrams game! \n")
    while True:
        answer = input("Type 'rules' to learn how to play or 'play' to start the game: \n").lower().strip()
        if answer == "rules" or answer == "play":
            return answer
        else:
            print("Invalid input. Please type 'rules' or 'play'.\n")

def player_name():
    """
    Gets the player to input their name.
    """
    name_input = input("What is your name? ").strip()
    print(f"Hello {name_input}! Hope you enjoy the game.")
    return name_input

def select_difficulty(name):
    """
    Gets the player to select a difficulty level
    """
    print(f"What difficulty would you like, {name}?")
    while True:
        choice = input("Type 'e' for easy (6-letter words), 'm' for medium (7 or 8-letter words), or 'h' for hard (9 or 10-letter words): ").lower().strip()
        if choice in {'e', 'm', 'h'}:
            return choice
        else:
            print("Invalid input. Please type 'e', 'm', or 'h'.\n")

class WordSelector:
    """
    Selects a word from words.txt. Ensures correct length for the difficulty setting. Jumbled up the letters in the word.
    """
    def __init__(self, filepath='words.txt'):
        with open(filepath, 'r') as file:
            self.words = [word.strip().lower() for word in file]

    def get_word_by_difficulty(self, difficulty):
        if difficulty == 'e':
            valid_words = [w for w in self.words if len(w) == 6]
        elif difficulty == 'm':
            valid_words = [w for w in self.words if len(w) in (7, 8)]
        elif difficulty == 'h':
            valid_words = [w for w in self.words if len(w) in (9, 10)]
        else:
            valid_words = []

        return random.choice(valid_words) if valid_words else None

    def jumble_word(self, word):
        letters = list(word)
        random.shuffle(letters)
        return ''.join(letters)

def play_game(name, difficulty):
    """
    Initiates 5 rounds of gameplay.
    """
    score = 0
    word_selector = WordSelector()

    for round_num in range(1, 6):  # Loop 5 times
        print(f"\nRound {round_num}")
        word = word_selector.get_word_by_difficulty(difficulty)
        if not word:
            print("No valid word found for the selected difficulty.")
            break
        anagram = word_selector.jumble_word(word)
        print(f"Unscramble this word: {anagram}")
        guess = input("Your guess: ").strip().lower()
        if guess == word:
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect. The correct word was: {word}")

    print(f"\nGame Over! Your final score is: {score}")

answer = welcome_message()
if answer == 'rules':
    print(
        "\nYou will be given five randomly generated words in the English language (with UK spelling)."
        "\nThe only problem is the letters have been jumbled up!"
        "\nYou will need to try and work out what the word is."
        "\nFor each one you answer correctly, you will receive a point.\n"
    )
name = player_name()
difficulty = select_difficulty(name)
play_game(name, difficulty)
