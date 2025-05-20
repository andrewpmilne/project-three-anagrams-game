# Anagrams Game!

The Anagrams Game is a Python terminal game, which runs in the Code Institute mock terminal in Heroku.

Users can try to solve five anagrams set at easy, medium or hard level of difficulty. After completing the game, users will see if they have achieved a place on the leaderboard and have an option to view the leaderboard before playing again or exiting.

[Here is the live version of the project](https://project-three-anagrams-e926f3ae0dcd.herokuapp.com/)

## How to play

This is the text the user will read if they select 'rules' as the first option in the game:

- You will be given five randomly generated words in the English language (with American spelling).
- The only problem is the letters have been jumbled up!
- You will need to try and work out what the word is.
- You have twenty seconds to solve each anagram.
- The quicker you solve the anagram the more points you will receive.
- For example, if you solve it with 12 seconds remaining you will score 12 points.
- If you score enough points your name will appear on the leaderboard.

## Features
The website has a number of features to aid the user experience:

### Rules
At the start, the user will be given the option of reading the rules. If they already know how to play they will be able to go straight to the game.

![rules text](readme-resources/rules.png)

### Opportunity to enter your name
The user will have an opportunity to enter a username. This will later be used for the leaderboard. Characters are set to a maximum of 20 to avoid issues when presenting the leaderboard at a later stage.

![input username text](readme-resources/username.png)

### A difficulty selector
Next, the user is able to select a difficulty level. This will determine the number of letters in the anagram.

![Difficulty selection text](readme-resources/difficulty-selector.png)

### Random word generation
A random word is generated from a list of words in a txt file, in a length inkeeping with the difficulty set. The letters are jumbled to create an anagram. Users have a time limit to correctly solve the anagram.

### Timer
The user has 20 seconds to solve the anagram before running out of time.

![Time is up](readme-resources/time-up.png)

### A Solution Check
If an attempt is inputted as a solution, the program will check if it matches the original word and feedback appropriately. Correct answers will score points based on how many seconds are remaining.

![Incorrect answer](readme-resources/incorrect-answer.png)

![Correct answer](readme-resources/correct-answer.png)

On rare occasions, the user may input a word that is in the txt file and a correct word in the English language but not the answer the program was expecting. In these occurences the program does check and feedback that the answer is correct.

![Different correct answer](readme-resources/valid-anagram-screenshot.png)


### A Score
After five anagrams, the program totals the score and checks to see if it has made the Google sheet used to store the leadboard data. It rearranges the data as necessary.

![end game score](readme-resources/game-end.png)

### A Leaderboard

The user is then given the opportunity to view a leaderboard, play again or exit. If the leaderboard has already been viewed this option is removed for the question after viewing it.

![leaderboard](readme-resources/leaderboard.png)

### Error Messages
Red coloured Validation Error messages are a feature that can be seen at various points in the game. They avoid errors that would have consequences at a later point in the program (such as a username with more than 20 characters) and give a clear message to the user about what they need to type for the game to continue. Colorama was implemented so that they could be written in red and stand out to the user.

![example of validation error](readme-resources/validation-one.png)

![another example of validation error](readme-resources/validation-two.png)

## Flowchart
This flowchart represents the logical flow of the program.

![Flowchart to showthe logical flow of the program](readme-resources/flowchart.png)

## Data Model
To improve readability and maintainability, I split my code into three separate .py files. I created a class (WordSelector) to handle reading and storing the word data from words.txt, which avoids the need to re-read the file every time a word is needed. This class also contains methods for selecting a word based on the chosen difficulty and jumbling the letters to create an anagram.

Using a class in this way helps separate word-handling logic from the main gameplay and leaderboard functionality, which are handled in their own modules. This structure not only keeps the code organised but also makes it easier to extend or modify the game in the future without major rewrites.

## Testing
A number of people have played the game to test for errors, including the designer and a Code Institute mentor. Attemps to 'break' the code were made to ensure all error messages appeared as expected. The program has been tested in the local terminal and the Code Institue Heroku terminal.

### Validation
All three .py modules have been passed through the Code Institute linter and confirmed no problems.

run.py

![screenshot of run.py linter](readme-resources/run-linter.png)

word_selector.py

![screenshot of word_selector.py linter](readme-resources/word-selector-linter.png)

leaderboard.py

![screenshot of leaderboard.py linter](readme-resources/leaderboard-linter.png)

## Bugs
A number of bugs were found during the testing process at various occurences.

### Solved Bugs
After implementing the countdown timer and linking this with scoring, it was revealed that on occasions players were scoring one fewer point than they should have done when correctly solving an anagram. One particular test resulted in an anagram being solved in 19 seconds (1 second remaining) but scoring 0 points. This was due to the rounding method used to calculate the time remaining occasionally rounding down. Using math.ceil ensured that the time remaining is always rounded up, correcting the scoring.

Playtesting revealed that if a user attempted to type an answer just as the time was running out, then pressed enter once it had run out, this resulted in an answer being submitted for the next question which was inevitably incorrect. To fix this, a 'pause' was coded in to the program between the first four questions to ensure the user was ready to move on. 

### Remaining Bugs
There is still a bug relating to the words.txt file used. Currently, there are still occurences where a user will type in a correct answers that uses the right letters and is a word in the English language but is not in the words.txt file. On this occasion the program will check the txt file for other suitable answers but will not be able to find one. To completely aleviate this issue a much larger dictionary would need to be used to check answers. This dictionary could not be used for the generation of the words at it would regularly find obscure and unusual English words, which would be frustrating for the user.

## Future Features
- Implement a larger dictionary to fix the bug described above of anagrams of the correct word being considered incorrect.
- Implement a two player game.
- Create a visual countdown so players can see how many seconds are remaining as they solve an anagram.

## Deployment

## Technologies Used

## Credits
List of 3000 common English words found through [université paris cité](https://python.sdv.u-paris.fr/data-files/english-common-words.txt)


## Acknowledgements
Thanks, once again, to Juliia Konovalova for Slack calls and advice whilst nine months pregnant!
My friend, John Holland, for playtesting the game and occasionally getting on the leaderboard!
