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
                "algorithm\nengineering\ncomplexity\nframework\n"
                "development\nintelligence\nprogramming"
            )

def load_words():
    create_word_file()
    with open(WORD_FILE) as f:
        return [w.strip() for w in f]

# ---------------- ENCRYPTION ----------------
def encrypt(text, shift=2):
    res = ""
    for ch in text:
        if ch.isalpha():
            res += chr((ord(ch) - 97 + shift) % 26 + 97)
        else:
            res += ch
    return res

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

HARD_WORDS_WITH_HINTS = {
    "algorithm": "step by step",
    "engineering": "problem solving",
    "complexity": "time space",
    "framework": "software structure",
    "development": "making software",
    "intelligence": "ability to learn",
    "programming": "writing code"
}

DIFFICULTY_WORDS = {
    "Easy": [w for w in all_words if len(w) <= 4],
    "Medium": [w for w in all_words if 5 <= len(w) <= 7],
    "Hard": list(HARD_WORDS_WITH_HINTS.keys())
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
current_hint = ""
encrypted_hint = ""
current_difficulty = ""

# ---------------- WINDOW ----------------
root = tk.Tk()
root.title("Hangman Game")
root.geometry("900x600")

# ---------------- EXIT GAME ----------------
def exit_game(event=None):
    global score
    save_score(player_name, score)
    show_game_over()

root.bind("1", exit_game)

# ---------------- FRAMES ----------------
name_frame = tk.Frame(root, bg=GAME_COLOR)
menu_frame = tk.Frame(root, bg=MENU_COLOR)
game_frame = tk.Frame(root, bg=GAME_COLOR)
leaderboard_frame = tk.Frame(root, bg=MENU_COLOR)
game_over_frame = tk.Frame(root, bg=MENU_COLOR)

def clear_frames():
    for f in (name_frame, menu_frame, game_frame, leaderboard_frame, game_over_frame):
        f.pack_forget()

# ---------------- NAME FRAME ----------------
tk.Label(name_frame, text="Enter Your Name",
         font=("Times New Roman", 28, "bold"),
         bg=GAME_COLOR).pack(pady=40)

name_entry = tk.Entry(name_frame, font=("Times New Roman", 18))
name_entry.pack(pady=10)

def submit_name():
    global player_name
    if name_entry.get().strip():
        player_name = name_entry.get().strip()
        clear_frames()
        start_menu()

tk.Button(name_frame, text="Continue",
          font=("Times New Roman", 16),
          bg=BUTTON_COLOR,
          command=submit_name).pack(pady=20)

# ---------------- MENU ----------------
def start_menu():
    clear_frames()
    menu_frame.pack(fill="both", expand=True)

tk.Label(menu_frame, text="Select Difficulty",
         font=("Times New Roman", 32, "bold"),
         bg=MENU_COLOR).pack(pady=30)

def start_game(diff):
    global score, word_index, word_list, current_difficulty
    current_difficulty = diff
    score = 0
    word_index = 0
    word_list = random.sample(DIFFICULTY_WORDS[diff], 3)
    load_next_word()
    clear_frames()
    game_frame.pack(fill="both", expand=True)

for d in ["Easy", "Medium", "Hard"]:
    tk.Button(menu_frame, text=d,
              width=15,
              font=("Times New Roman", 18),
              bg=BUTTON_COLOR,
              command=lambda x=d: start_game(x)).pack(pady=8)

tk.Button(menu_frame, text="Leaderboard",
          font=("Times New Roman", 16),
          bg=BUTTON_COLOR,
          command=lambda: show_leaderboard()).pack(pady=15)

# ---------------- GAME UI ----------------
canvas = tk.Canvas(game_frame, width=400, height=350, bg=GAME_COLOR, bd=0, highlightthickness=0)
canvas.place(x=480, y=120)

score_label = tk.Label(game_frame, font=("Times New Roman", 16), bg=GAME_COLOR)
score_label.place(x=50, y=70)

word_label = tk.Label(game_frame, font=("Times New Roman", 32), bg=GAME_COLOR)
word_label.place(x=50, y=130)

hint_label = tk.Label(game_frame, font=("Times New Roman", 16, "italic"),
                      fg="darkred", bg=GAME_COLOR)
hint_label.place(x=50, y=190)

guessed_label = tk.Label(game_frame, font=("Times New Roman", 14), bg=GAME_COLOR)
guessed_label.place(x=50, y=240)

letters_frame = tk.Frame(game_frame, bg=GAME_COLOR)
letters_frame.place(x=50, y=300)

# ---------------- ANIMATED HANGMAN ----------------
SCAFFOLD_X = 150
SCAFFOLD_Y = 40
ROPE_Y = 90

def draw_scaffold():
    canvas.create_line(SCAFFOLD_X, SCAFFOLD_Y, SCAFFOLD_X, 300, fill=HANGMAN_COLOR, width=4)  # vertical pole
    canvas.create_line(SCAFFOLD_X, SCAFFOLD_Y, 300, SCAFFOLD_Y, fill=HANGMAN_COLOR, width=4)  # top horizontal
    canvas.create_line(300, SCAFFOLD_Y, 300, ROPE_Y, fill=HANGMAN_COLOR, width=4)  # rope

# Body parts
def draw_head(): canvas.create_oval(275, ROPE_Y, 325, ROPE_Y+60, outline=HANGMAN_COLOR, width=3)
def draw_body(): canvas.create_line(300, ROPE_Y+60, 300, ROPE_Y+150, fill=HANGMAN_COLOR, width=3)
def draw_left_arm(): canvas.create_line(300, ROPE_Y+80, 250, ROPE_Y+120, fill=HANGMAN_COLOR, width=3)
def draw_right_arm(): canvas.create_line(300, ROPE_Y+80, 350, ROPE_Y+120, fill=HANGMAN_COLOR, width=3)
def draw_left_leg(): canvas.create_line(300, ROPE_Y+150, 250, ROPE_Y+200, fill=HANGMAN_COLOR, width=3)
def draw_right_leg(): canvas.create_line(300, ROPE_Y+150, 350, ROPE_Y+200, fill=HANGMAN_COLOR, width=3)

body_parts = [draw_head, draw_body, draw_left_arm, draw_right_arm, draw_left_leg, draw_right_leg]

def animate_hangman(index):
    if index < len(body_parts):
        # simple animation: each part drawn after short delay
        steps = 5
        for i in range(steps):
            root.after(i*30, body_parts[index])

# ---------------- GAME LOGIC ----------------
def load_next_word():
    global current_word, guessed, guessed_letters, wrong
    global current_hint, encrypted_hint, word_index

    if word_index >= len(word_list):
        save_score(player_name, score)
        show_game_over()
        return

    current_word = word_list[word_index]
    word_index += 1
    guessed = ["_"] * len(current_word)
    guessed_letters = []
    wrong = 0
    canvas.delete("all")
    draw_scaffold()

    if current_difficulty == "Hard":
        current_hint = HARD_WORDS_WITH_HINTS[current_word]
        encrypted_hint = encrypt(current_hint)
        hint_label.config(text=f"Encrypted Hint: {encrypted_hint}")
    else:
        hint_label.config(text="")

    update_ui()

def update_ui():
    word_label.config(text=" ".join(guessed))
    score_label.config(text=f"Score: {score}")
    guessed_label.config(text="Guessed: " + " ".join(guessed_letters))

def guess_letter(letter):
    global wrong, score

    if letter in guessed_letters:
        return
    guessed_letters.append(letter)

    if letter in current_word:
        score += 5
        for i, ch in enumerate(current_word):
            if ch == letter:
                guessed[i] = letter
    else:
        wrong += 1
        score -= 2
        root.after(100, lambda w=wrong-1: animate_hangman(w))

    if current_difficulty == "Hard":
        if wrong >= 2:
            hint_label.config(text=f"Hint: {current_hint}")
        else:
            hint_label.config(text=f"Encrypted Hint: {encrypted_hint}")

    update_ui()

    if "_" not in guessed or wrong >= MAX_WRONG:
        root.after(800, load_next_word)

# ---------------- LETTER BUTTONS ----------------
for i, ch in enumerate("abcdefghijklmnopqrstuvwxyz"):
    tk.Button(letters_frame, text=ch.upper(), width=4, height=2,
              bg=BUTTON_COLOR,
              command=lambda c=ch: guess_letter(c)
              ).grid(row=i // 9, column=i % 9, padx=2, pady=2)

# ---------------- LEADERBOARD ----------------
def show_leaderboard():
    clear_frames()
    leaderboard_frame.pack(fill="both", expand=True)

    for w in leaderboard_frame.winfo_children():
        w.destroy()

    tk.Label(leaderboard_frame, text="Leaderboard",
             font=("Times New Roman", 32, "bold"),
             bg=MENU_COLOR).pack(pady=30)

    scores = load_scores()
    scores.sort(key=lambda x: int(x[1]), reverse=True)

    for name, sc in scores[:10]:
        tk.Label(leaderboard_frame, text=f"{name} - {sc}",
                 font=("Times New Roman", 16),
                 bg=MENU_COLOR).pack()

    tk.Button(leaderboard_frame, text="Back",
              font=("Times New Roman", 16),
              bg=BUTTON_COLOR,
              command=start_menu).pack(pady=30)

# ---------------- GAME OVER ----------------
def show_game_over():
    clear_frames()
    game_over_frame.pack(fill="both", expand=True)

    tk.Label(game_over_frame, text="GAME OVER",
             font=("Times New Roman", 36, "bold"),
             bg=MENU_COLOR).pack(pady=40)

    tk.Label(game_over_frame, text=f"Player: {player_name}",
             font=("Times New Roman", 20),
             bg=MENU_COLOR).pack()

    tk.Label(game_over_frame, text=f"Score: {score}",
             font=("Times New Roman", 24, "bold"),
             bg=MENU_COLOR).pack(pady=20)

    tk.Button(game_over_frame, text="Back to Menu",
              font=("Times New Roman", 16),
              bg=BUTTON_COLOR,
              command=start_menu).pack(pady=30)

# ---------------- START ----------------
name_frame.pack(fill="both", expand=True)
root.mainloop()


