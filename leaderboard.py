import gspread
from colorama import Fore, Style, init
from google.oauth2.service_account import Credentials

init()


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

    # Print success message with position
    for index, (player_name, player_score) in enumerate(leaderboard, start=1):
        if player_name == name and player_score == score:
            print(
                f"{Fore.GREEN}🎉 Well done {name}!"
                "You are on the leaderboard!\n"
                f"Position: #{index}{Style.RESET_ALL}"
            )
            break
    else:
        print(
            f"{Fore.YELLOW}\nSorry {name}.\n"
            f"That score didn't make the leaderboard.{Style.RESET_ALL}"
        )

    return


def view_leaderboard(difficulty):
    """ Prints the leaderboard to the screen """
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
