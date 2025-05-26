import math
import time
from inputimeout import inputimeout, TimeoutOccurred
from colorama import init, Fore, Style
from word_selector import WordSelector
from leaderboard import leaderboard_check, view_leaderboard


# Initialise colorama
init()

# The Rules
RULES = """
• You will be given five randomly generated words in the English language
  (with American spelling).
• The only problem is the letters have been jumbled up!
• You will need to try and work out what the word is.
• You have twenty seconds to solve each anagram.
• The quicker you solve the anagram the more points you will receive.
• Eg, if you solve it with 12 seconds remaining you will score 12 points.
• If you score enough points your name will appear on the leaderboard.
"""


def welcome_message():
    """
    Introduces the player to the game.
    Asks if they want to read the rules.
    """
    print("\nWelcome to the Anagrams game! \n")
    while True:
        answer = input(
            "Type 'rules' to learn how to play or 'play' to start the game: \n"
        ).lower().strip()
        if answer == "rules" or answer == "play":
            return answer
        else:
            print(Fore.RED +
                  "Invalid input. Please type 'rules' or 'play'.\n"
                  + Style.RESET_ALL)


def player_name():
    """
    Gets the player to input their name (max 20 characters).
    Converts to capital letters.
    """
    while True:
        name_input = input(
            "\nWhat is your username (max 20 characters)? \n"
        ).strip().upper()

        if len(name_input) == 0:
            print(Fore.RED + "\nPlease enter a username." + Style.RESET_ALL)
        elif len(name_input) > 20:
            print(
                Fore.RED +
                """\nUsername too long. Please enter a username with at most
                20 characters."""
                + Style.RESET_ALL)
        else:
            print(f"\nHello {name_input}! Hope you enjoy the game.")
            return name_input


def select_difficulty(name):
    """ Gets the player to select a difficulty level """

    print("\nWhat difficulty would you like?")
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
            print(
                Fore.RED +
                "Invalid input. Please type 'e', 'm', or 'h'.\n"
                + Style.RESET_ALL
                )


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

        # Creates a jumbled word and sets the time at 20.
        for round_num in range(1, 6):
            print(f"\nRound {round_num}")
            word = word_selector.get_word_by_difficulty(difficulty)
            anagram = ' '.join(word_selector.jumble_word(word))
            print(
                f"Unscramble this word (you have 20 seconds): {anagram}\n"
                "To skip hit enter"
            )
            guess, time_taken = timed_input("Your guess: ", timeout=20)
            time_remaining = max(0, math.ceil(20 - time_taken))

            # Prints message for correct/ incorrect answer, updates points
            if guess is None:
                print(
                    f"Sorry, time is up! The correct answer was: "
                    f"{Fore.YELLOW}{word}{Style.RESET_ALL}"
                    )
            elif guess.strip().lower() == word:
                print(f"{Fore.GREEN}Correct!{Style.RESET_ALL}"
                      f"\nYou answered in {int(time_taken)} seconds."
                      f"\nYou earn {time_remaining} points."
                      )
                score += time_remaining
            elif (sorted(guess.strip().lower()) == sorted(word)
                  and guess.strip().lower() in word_selector.words):
                print(f"Nice! '{guess}' is a valid anagram"
                      "of the correct word:"
                      f"'{Fore.YELLOW}{word}{Style.RESET_ALL}'."
                      f"You earn {time_remaining} points."
                      )
                score += time_remaining
            else:
                print(
                    "Incorrect. The correct word was: "
                    f"{Fore.YELLOW}{word}{Style.RESET_ALL}"
                    )

            # checks user is ready to continue
            if round_num < 5:
                while True:
                    user_input = input("\nPress ENTER to continue...").strip()
                    if user_input == "":
                        break
                    else:
                        print(
                            Fore.RED +
                            "Please press ENTER without typing anything."
                            + Style.RESET_ALL
                            )

        print(
            f"\nYou scored {score} points!"
            "\nChecking the leaderboard. Please wait...")

        viewed_leaderboard = False

        leaderboard_check(name, difficulty, score)

        # Asks end game question
        while True:
            if viewed_leaderboard:
                replay = input(
                    "\nWould you like to:\n"
                    "- Play again (p)\n"
                    "- Exit (e)?\n"
                ).strip().lower()
            else:
                difficulty_name = ({"e": "Easy", "m": "Medium",
                                    "h": "Hard"}[difficulty])
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
                    Fore.RED +
                    "Invalid input. Please type 'p' to play again"
                    + (", 'l' to view the leaderboard"
                        if not viewed_leaderboard else "")
                    + ", or 'e' to exit."
                    + Style.RESET_ALL
                    )


def main():
    answer = welcome_message()
    if answer == 'rules':
        print(RULES)
    name = player_name()
    play_game(name)


if __name__ == "__main__":
    main()
