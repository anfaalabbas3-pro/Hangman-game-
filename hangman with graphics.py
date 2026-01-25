import tkinter as tk
import random
import os

# ---------------- FILES ----------------
WORD_FILE = "words.txt"
LEADERBOARD_FILE = "leaderboard.txt"

# ---------------- COLORS ----------------
MENU_COLOR = "#1D546D"
GAME_COLOR = "#5F9598"
TEXT_COLOR = "black"
HANGMAN_COLOR = "#93BD57"
BUTTON_COLOR = "#FEB05D"

# ---------------- WORD FILE ----------------
def create_word_file():
    if not os.path.exists(WORD_FILE):
        with open(WORD_FILE, "w") as f:
            f.write(
                "cat\ndog\ntree\nbook\npen\n"
                "python\nhangman\nscience\ncollege\n"
                "algorithm\nengineering\ncomplexity\nframework"
            )

def load_words():
    create_word_file()
    with open(WORD_FILE) as f:
        return [w.strip() for w in f]

# ---------------- LEADERBOARD ----------------
def save_score(name, score):
    with open(LEADERBOARD_FILE, "a") as f:
        f.write(f"{name},{score}\n")

def load_scores():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE) as f:
        return [line.strip().split(",") for line in f]

# ---------------- GAME DATA ----------------
all_words = load_words()

DIFFICULTY_WORDS = {
    "Easy": [w for w in all_words if len(w) <= 4],
    "Medium": [w for w in all_words if 5 <= len(w) <= 7],
    "Hard": [w for w in all_words if len(w) >= 8]
}

MAX_WRONG = 6
player_name = ""
score = 0
wrong = 0
word_list = []
current_word = ""
guessed = []
guessed_letters = []
word_index = 0

# ---------------- WINDOW ----------------
root = tk.Tk()
root.title("Hangman Game")
root.geometry("900x600")

# ---------------- FRAME CONTROL ----------------
def clear_frames():
    for f in (name_frame, menu_frame, game_frame, leaderboard_frame, game_over_frame):
        f.pack_forget()

# ---------------- GAME FLOW ----------------
def start_menu():
    clear_frames()
    menu_frame.pack(fill="both", expand=True)

def start_game(diff):
    global score, word_index, word_list
    score = 0
    word_index = 0
    word_list = random.sample(DIFFICULTY_WORDS[diff], 3)
    load_next_word()
    clear_frames()
    game_frame.pack(fill="both", expand=True)

def load_next_word():
    global current_word, guessed, guessed_letters, wrong, word_index

    if word_index >= len(word_list):
        save_score(player_name, score)
        show_game_over()
        return

    current_word = word_list[word_index]
    word_index += 1
    guessed = ["_"] * len(current_word)
    guessed_letters = []
    wrong = 0
    update_ui()

def guess_letter(letter):
    global wrong, score

    if letter in guessed_letters:
        return

    guessed_letters.append(letter)

    if letter in current_word:
        score += 5
        for i in range(len(current_word)):
            if current_word[i] == letter:
                guessed[i] = letter
    else:
        wrong += 1
        score -= 2

    update_ui()

    if "_" not in guessed or wrong >= MAX_WRONG:
        root.after(800, load_next_word)

def update_ui():
    word_label.config(text=" ".join(guessed))
    score_label.config(text=f"Score: {score}")
    guessed_label.config(text="Guessed: " + " ".join(guessed_letters))
    draw_hangman(wrong)

# ---------------- EXIT GAME (PRESS 1) ----------------
def exit_game(event=None):
    save_score(player_name, score)
    show_game_over()

root.bind("1", exit_game)

# ---------------- HANGMAN DRAW ----------------
def draw_hangman(w):
    canvas.delete("all")
    canvas.create_line(150, 30, 150, 300, width=5, fill=HANGMAN_COLOR)
    canvas.create_line(100, 30, 220, 30, width=5, fill=HANGMAN_COLOR)
    canvas.create_line(220, 30, 220, 70, width=5, fill=HANGMAN_COLOR)

    if w >= 1:
        canvas.create_oval(195, 70, 245, 120, width=4, outline=HANGMAN_COLOR)
    if w >= 2:
        canvas.create_line(220, 120, 220, 210, width=4, fill=HANGMAN_COLOR)
    if w >= 3:
        canvas.create_line(220, 140, 190, 180, width=4, fill=HANGMAN_COLOR)
    if w >= 4:
        canvas.create_line(220, 140, 250, 180, width=4, fill=HANGMAN_COLOR)
    if w >= 5:
        canvas.create_line(220, 210, 200, 260, width=4, fill=HANGMAN_COLOR)
    if w >= 6:
        canvas.create_line(220, 210, 240, 260, width=4, fill=HANGMAN_COLOR)

# ---------------- NAME FRAME ----------------
name_frame = tk.Frame(root, bg=GAME_COLOR)

tk.Label(
    name_frame, text="Enter Your Name",
    font=("Times New Roman", 28, "bold"),
    bg=GAME_COLOR, fg=TEXT_COLOR
).pack(pady=50)

name_entry = tk.Entry(name_frame, font=("Times New Roman", 18))
name_entry.pack(pady=20)

def submit_name():
    global player_name
    if name_entry.get().strip():
        player_name = name_entry.get()
        start_menu()

tk.Button(
    name_frame, text="Continue",
    font=("Times New Roman", 16),
    bg=BUTTON_COLOR,
    command=submit_name
).pack(pady=20)

# ---------------- MENU FRAME ----------------
menu_frame = tk.Frame(root, bg=MENU_COLOR)

tk.Label(
    menu_frame, text="Select Difficulty",
    font=("Times New Roman", 32, "bold"),
    bg=MENU_COLOR, fg=TEXT_COLOR
).pack(pady=40)

for d in ["Easy", "Medium", "Hard"]:
    tk.Button(
        menu_frame, text=d,
        font=("Times New Roman", 18),
        width=15,
        bg=BUTTON_COLOR,
        command=lambda x=d: start_game(x)
    ).pack(pady=10)

tk.Button(
    menu_frame, text="Leaderboard",
    font=("Times New Roman", 16),
    bg=BUTTON_COLOR,
    command=lambda: show_leaderboard()
).pack(pady=20)

# ---------------- GAME FRAME ----------------
game_frame = tk.Frame(root, bg=GAME_COLOR)

canvas = tk.Canvas(
    game_frame, width=300, height=350,
    bg=GAME_COLOR, highlightthickness=0
)
canvas.place(x=560, y=120)

score_label = tk.Label(
    game_frame, bg=GAME_COLOR,
    fg=TEXT_COLOR, font=("Times New Roman", 16)
)
score_label.place(x=50, y=80)

word_label = tk.Label(
    game_frame, bg=GAME_COLOR,
    fg=TEXT_COLOR, font=("Times New Roman", 32)
)
word_label.place(x=50, y=160)

guessed_label = tk.Label(
    game_frame, bg=GAME_COLOR,
    fg=TEXT_COLOR, font=("Times New Roman", 14)
)
guessed_label.place(x=50, y=240)

letters_frame = tk.Frame(game_frame, bg=GAME_COLOR)
letters_frame.place(x=50, y=300)

for i, ch in enumerate("abcdefghijklmnopqrstuvwxyz"):
    tk.Button(
        letters_frame, text=ch.upper(),
        width=4, height=2,
        bg=BUTTON_COLOR,
        command=lambda c=ch: guess_letter(c)
    ).grid(row=i // 9, column=i % 9, padx=2, pady=2)

# ---------------- LEADERBOARD FRAME ----------------
leaderboard_frame = tk.Frame(root, bg=MENU_COLOR)

def show_leaderboard():
    clear_frames()
    leaderboard_frame.pack(fill="both", expand=True)

    for w in leaderboard_frame.winfo_children():
        w.destroy()

    tk.Label(
        leaderboard_frame, text="Leaderboard",
        font=("Times New Roman", 32, "bold"),
        bg=MENU_COLOR, fg=TEXT_COLOR
    ).pack(pady=30)

    scores = load_scores()
    scores.sort(key=lambda x: int(x[1]), reverse=True)

    for name, sc in scores:
        tk.Label(
            leaderboard_frame,
            text=f"{name}  -  {sc}",
            font=("Times New Roman", 16),
            bg=MENU_COLOR, fg=TEXT_COLOR
        ).pack(pady=2)

    tk.Button(
        leaderboard_frame, text="Back",
        font=("Times New Roman", 16),
        bg=BUTTON_COLOR,
        command=start_menu
    ).pack(pady=30)

# ---------------- GAME OVER FRAME ----------------
game_over_frame = tk.Frame(root, bg=MENU_COLOR)

def show_game_over():
    clear_frames()
    game_over_frame.pack(fill="both", expand=True)

    for w in game_over_frame.winfo_children():
        w.destroy()

    tk.Label(
        game_over_frame, text=" YOU WIN ",
        font=("Times New Roman", 36, "bold"),
        bg=MENU_COLOR, fg=TEXT_COLOR
    ).pack(pady=40)

    tk.Label(
        game_over_frame, text=f"Player: {player_name}",
        font=("T", 20),
        bg=MENU_COLOR, fg=TEXT_COLOR
    ).pack(pady=10)

    tk.Label(
        game_over_frame, text=f"Total Score: {score}",
        font=("T", 24, "bold"),
        bg=MENU_COLOR, fg=TEXT_COLOR
    ).pack(pady=20)

    tk.Button(
        game_over_frame, text="Back to Menu",
        font=("Times New Roman", 16),
        bg=BUTTON_COLOR,
        command=start_menu
    ).pack(pady=30)

# ---------------- START ----------------
name_frame.pack(fill="both", expand=True)
root.mainloop()
