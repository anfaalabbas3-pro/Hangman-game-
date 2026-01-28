Hangman Game
A Python-based Hangman Game with a graphical interface built using Tkinter. This game challenges players to guess words across multiple difficulty levels while enjoying an animated Hangman drawing, score tracking, and hints for harder words.

1. Features:
Multiple Difficulty Levels
Easy: Short words (≤4 letters)
Medium: Medium-length words (5–7 letters)
Hard: Long or complex words (≥8 letters) with hints

2. Animated Hangman:
Scaffold, rope, and body parts are drawn step-by-step on wrong guesses.

3. Score System:
+5 points for correct letters
-2 points for incorrect letters

4. Hints for Hard Words:
Hints are encrypted initially and revealed after 2 wrong guesses.

5. Leaderboard:
Tracks top scores across games and displays the top 10 players.

6. Keyboard Shortcut:
Press 1 at any time to exit the game and see the Game Over screen.

7. Installation
Clone or download the repository
Make sure you have Python 3.14.2 installed.
Tkinter is usually included with Python. If not, install it:
pip install tk

8. How to Play
Run the game:
python hangman_game.py
Enter your name and click Continue.
Select a difficulty level.
Guess the letters by clicking the buttons.
Watch the animated Hangman form on wrong guesses.
Hard words include hints, encrypted first and revealed after 2 wrong guesses.
Track your score and check the leaderboard.
Press 1 anytime to exit the game and see your final score.

9. Files:
hangman_game.py → Main game script
words.txt → Word list used by the game (auto-generated if missing)
leaderboard.txt → Saves player names and score

10. Future Improvements:
Smooth limb animation for more realistic Hangman drawing.
Add sound effects for correct/incorrect guesses.
Expand word database and hint system.
Add timer for each guess to increase difficulty.

11. License:

This project is open source and free to use for learning and personal purposes.
