import random
import math
import string
import time
from inputimeout import inputimeout, TimeoutOccurred
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("project_three_leaderboard")

easy = SHEET.worksheet("easy")
medium = SHEET.worksheet("medium")
hard = SHEET.worksheet("hard")


def welcome_message():
    """
    Introduces the player to the game and asks if they want to read the rules.
    """
    print("\nWelcome to the Anagrams game! \n")
    while True:
        answer = input(
            "Type 'rules' to learn how to play or 'play' to start the game: \n"
        ).lower().strip()
        if answer == "rules" or answer == "play":
            return answer
        else:
            print("Invalid input. Please type 'rules' or 'play'.\n")


def player_name():
    """
    Gets the player to input their name (max 20 characters), always in caps.
    """
    while True:
        name_input = input(
            "\nWhat is your username (max 20 characters)? \n"
        ).strip().upper()

        if len(name_input) == 0:
            print("\nPlease enter a username.")
        elif len(name_input) > 20:
            print(
                """\nUsername too long. Please enter a username with at most
                20 characters."""
            )
        else:
            print(f"\nHello {name_input}! Hope you enjoy the game.")
            return name_input


def select_difficulty(name):
    """ Gets the player to select a difficulty level """

    print(f"\nWhat difficulty would you like, {name}?")
    while True:
        choice = input(
            "\nType:\n"
            "'e' for easy (6-letter words)\n"
            "'m' for medium (7 or 8-letter words)\n"
            "'h' for hard (9 or 10-letter words): \n"
        ).lower().strip()

        if choice in {"e", "m", "h"}:
            return choice
        else:
            print("Invalid input. Please type 'e', 'm', or 'h'.\n")


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


def timed_input(prompt, timeout=20):
    """
    Prompts the user for input with a time limit.
    Returns the input (if any) and the time taken.
    """
    start_time = time.time()
    try:
        user_input = inputimeout(prompt=prompt, timeout=timeout)
        time_taken = time.time() - start_time
        return user_input.strip(), time_taken
    except TimeoutOccurred:
        print("\n⏰ Time's up!")
        return None, timeout


def play_game(name):
    """
    Initiates 5 rounds of gameplay.
    Asks the player if they want to play again.
    """
    while True:
        difficulty = select_difficulty(name)
        score = 0
        word_selector = WordSelector()

        for round_num in range(1, 6):
            print(f"\nRound {round_num}")
            word = word_selector.get_word_by_difficulty(difficulty)
            anagram = word_selector.jumble_word(word)
            print(f"Unscramble this word (you have 20 seconds): {anagram}")
            guess, time_taken = timed_input("Your guess: ", timeout=20)
            time_remaining = max(0, math.ceil(20 - time_taken))

            if guess is None:
                print(f"Sorry, time is up! The correct answer was: "
                      f"{word}"
                      )
            elif guess.strip().lower() == word:
                print(f"Correct! You answered in {int(time_taken)} seconds."
                      f"You earn {time_remaining} points."
                      )
                score += time_remaining
            elif (sorted(guess.strip().lower()) == sorted(word)
                  and guess.strip().lower() in word_selector.words):
                print(f"Nice! '{guess}' is a valid anagram"
                      f"of the correct word '{word}'."
                      f"You earn {time_remaining} points."
                      )
                score += time_remaining
            else:
                print(f"Incorrect. The correct word was: {word}")

        print(
            f"\nGame over, {name}! Your final score is: {score}\n"
            "Checking the leaderboard. Please wait...."
        )

        leaderboard_check(name, difficulty, score)

        viewed_leaderboard = False

        while True:
            if viewed_leaderboard:
                replay = input(
                    "\nWould you like to:\n"
                    "- Play again (p)\n"
                    "- Exit (e)?\n"
                ).strip().lower()
            else:
                difficulty_name = {"e": "Easy", "m": "Medium", "h": "Hard"}[difficulty]
                replay = input(
                    "\nWould you like to:\n"
                    "- Play again (p)\n"
                    f"- View the {difficulty_name} Level Leaderboard (l)\n"
                    "- Exit (e)?\n"
                ).strip().lower()

            if replay == 'p':
                break
            elif replay == 'l' and not viewed_leaderboard:
                view_leaderboard(difficulty)
                viewed_leaderboard = True
            elif replay == 'e':
                print("Thanks for playing! Goodbye!")
                exit()
            else:
                print(
                    "Invalid input. Please type 'p' to play again"
                    + (", 'l' to view the leaderboard"
                        if not viewed_leaderboard else "")
                    + ", or 'e' to exit."
                )


def leaderboard_check(name, difficulty, score):
    """
    Checks to see if the score obtained makes the top ten leaderboard.
    Informs the player if it has.
    Updates the leaderboard.
    """
    sheet_map = {'e': easy, 'm': medium, 'h': hard}
    sheet = sheet_map[difficulty]

    # Get existing scores (skip header)
    data = sheet.get_all_values()[1:]

    # Build current leaderboard
    leaderboard = [
        (row[0], int(row[1]))
        for row in data if row[0]
        and row[1].isdigit()
        ]

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
            sheet.update(
                range_name=f"B{cell_row}",
                values=[[str(player_score)]]
            )
        else:
            # Clear any remaining old rows beyond current top scores
            sheet.update(range_name=f"A{cell_row}", values=[[""]])
            sheet.update(range_name=f"B{cell_row}", values=[[""]])

    # Print success message
    if any(
        player_name == name and player_score == score
        for player_name, player_score in leaderboard
    ):
        print(f"\n🎉 Well done {name}, you are on the leaderboard!")
    else:
        print(f"\n Sorry {name}, that score didn't make the leaderboard.")
    return


def view_leaderboard(difficulty):
    """
    Prints the leaderboard to the screen
    """
    sheet_map = {"e": easy, "m": medium, "h": hard}
    sheet = sheet_map[difficulty]

    print("\n🏆 Leaderboard 🏆")
    difficulty_name = {"e": "Easy", "m": "Medium", "h": "Hard"}[difficulty]
    print(f"Difficulty: {difficulty_name}\n")

    data = sheet.get_all_values()

    for i, row in enumerate(data):
        if len(row) < 2:
            continue
        name, score = row[0], row[1]
        if i == 0:
            print(f"{name:<20}{score}")
        else:
            print(f"{i}. {name:<18}{score}")
    return


answer = welcome_message()
if answer == 'rules':
    print(
        """
• You will be given five randomly generated words in the English language
  (with American spelling).
• The only problem is the letters have been jumbled up!
• You will need to try and work out what the word is.
• You have twenty seconds to solve each anagram.
• The quicker you solve the anagram the more points you will receive.
• For example, if you solve it with 12 seconds remaining you will score 12
  points.
• If you score enough points your name will appear on the leaderboard.
"""
    )
name = player_name()
play_game(name)
