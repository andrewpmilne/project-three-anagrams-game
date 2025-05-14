import random
import threading
import time
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('project_three_leaderboard')

easy = SHEET.worksheet('easy')
medium = SHEET.worksheet('medium')
hard = SHEET.worksheet('hard')

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
    Selects a word from words.txt. Ensures correct length for the difficulty setting. Jumbles up the letters in the word.
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


def timed_input(prompt, timeout=20):
    """
    Prompts the user for input, giving them a set number of seconds to respond.
    """
    user_input = [None]
    start_time = time.time()

    def get_input():
        user_input[0] = input(prompt)

    thread = threading.Thread(target=get_input)
    thread.daemon = True
    thread.start()
    thread.join(timeout)

    end_time = time.time()
    time_taken = end_time - start_time

    if thread.is_alive():
        return None, timeout
    else:
        return user_input[0], time_taken


def play_game(name):
    """
    Initiates 5 rounds of gameplay and asks the player if they want to play again.
    """
    while True:
        difficulty = select_difficulty(name)
        score = 0
        word_selector = WordSelector()

        for round_num in range(1, 6):
            print(f"\nRound {round_num}")
            word = word_selector.get_word_by_difficulty(difficulty)
            if not word:
                print("No valid word found for the selected difficulty.")
                break
            anagram = word_selector.jumble_word(word)
            print(f"Unscramble this word (you have 20 seconds): {anagram}")
            guess, time_taken = timed_input("Your guess: ", timeout=20)
            time_remaining = max(0, int(20 - time_taken))

            if guess is None:
                print(f"Sorry, time is up! The correct answer was: {word}")
            elif guess.strip().lower() == word:
                print(f"Correct! You answered in {int(time_taken)} seconds. You earn {time_remaining} points.")
                score += time_remaining
            elif sorted(guess.strip().lower()) == sorted(word) and guess.strip().lower() in word_selector.words:
                print(f"Nice! '{guess}' is a valid anagram of the correct word '{word}'. You earn {time_remaining} points.")
                score += time_remaining
            else:
                print(f"Incorrect. The correct word was: {word}")

        print(f"\nGame over, {name}! Your final score is: {score}")

        leaderboard_check(name, difficulty, score)

        # Ask if they want to play again
        while True:
            replay = input("\nWould you like to play again? (y/n): ").strip().lower()
            if replay == 'y':
                break  # Goes back to select_difficulty
            elif replay == 'n':
                print("Thanks for playing! Goodbye!")
                exit()
            else:
                print("Invalid input. Please type 'y' for yes or 'n' for no.")

def leaderboard_check(name, difficulty, score):
    sheet_map = {'e': easy, 'm': medium, 'h': hard}
    sheet = sheet_map[difficulty]

    # Get existing scores (skip header)
    data = sheet.get_all_values()[1:]

    # Build current leaderboard
    leaderboard = [(row[0], int(row[1])) for row in data if row[0] and row[1].isdigit()]

    # Add new score
    leaderboard.append((name, score))

    # Sort and trim to top 10
    leaderboard = sorted(leaderboard, key=lambda x: x[1], reverse=True)[:10]

    # Write leaderboard rows from A2 downward
    for i in range(10):
        cell_row = i + 2
        if i < len(leaderboard):
            player_name, player_score = leaderboard[i]
            sheet.update(range_name=f"A{cell_row}", values=[[player_name]])
            sheet.update(range_name=f"B{cell_row}", values=[[str(player_score)]])
        else:
            # Clear any remaining old rows beyond current top scores
            sheet.update(range_name=f"A{cell_row}", values=[[""]])
            sheet.update(range_name=f"B{cell_row}", values=[[""]])

    # Print success message
    if any(player_name == name and player_score == score for player_name, player_score in leaderboard):
        print(f"\n🎉 Well done {name}, you are on the leaderboard!")
    return




answer = welcome_message()
if answer == 'rules':
    print(
        "\nYou will be given five randomly generated words in the English language (with UK spelling)."
        "\nThe only problem is the letters have been jumbled up!"
        "\nYou will need to try and work out what the word is."
        "\nFor each one you answer correctly, you will receive a point.\n"
    )
name = player_name()
play_game(name)
