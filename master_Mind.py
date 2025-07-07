#!/bin/python3
# MasterMind
# by ICTROCN
# v1.02
# 15-8-2024
# lastmod by DevBart : admin check. color mode added. login for admins
# Username: admin Password: letmein
# push 9

import random

print("MasterMind")

# Define available colors
COLOR_LIST = ["Red", "Green", "Blue", "Yellow", "Orange", "Purple"]
# for case-insensitive matching
COLOR_SET = {color.lower() for color in COLOR_LIST}


def generate_Code(length=4, mode="numbers"):
    if mode == "colors":
        return [random.choice(COLOR_LIST) for _ in range(length)]
    else:
        return [str(random.randint(1, 6)) for _ in range(length)]


def get_Feedback(secret, guess):
    black_Pegs = sum(s.lower() == g.lower() for s, g in zip(secret, guess))

    secret_Counts = {}
    guess_Counts = {}

    for s, g in zip(secret, guess):
        if s.lower() != g.lower():
            s_key = s.lower()
            g_key = g.lower()
            secret_Counts[s_key] = secret_Counts.get(s_key, 0) + 1
            guess_Counts[g_key] = guess_Counts.get(g_key, 0) + 1

    white_Pegs = sum(
        min(secret_Counts.get(k, 0), guess_Counts.get(k, 0)) for k in guess_Counts
    )

    return black_Pegs, white_Pegs


def show_Secret(mystery):
    print("SECRET:", ' '.join(mystery))


def admin_login():
    print("Admin Login")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    # Hardcoded credentials
    if username == "admin" and password == "letmein":
        print("✅ Admin login successful.")
        return True
    else:
        print("❌ Invalid credentials.")
        return False


def play_Mastermind(is_admin=False):
    print("Welcome to Mastermind!")
    mode = ""
    while mode not in ["1", "2"]:
        print("Choose a mode:")
        print("1. Numbers (1-6)")
        print("2. Colors (Red, Green, Blue, Yellow, Orange, Purple)")
        mode = input("Enter 1 or 2: ").strip()

    mode = "numbers" if mode == "1" else "colors"
    secret_Code = generate_Code(mode=mode)
    attempts = 10

    if mode == "numbers":
        print(
            "Guess the 4-digit code. Each digit is from 1 to 6. "
            "You have 10 attempts."
        )
    else:
        print(
            "Guess the 4-color code. Use full color names "
            "(e.g., Red Green Blue Yellow)."
        )
        print("Available colors:", ', '.join(COLOR_LIST))
        print("You have 10 attempts. Input example: Red Blue Yellow Green")

    for attempt in range(1, attempts + 1):
        guess = []
        valid_Guess = False
        while not valid_Guess:
            raw = input(f"Attempt {attempt}: ").strip()
            if raw.lower() == "cheat":
                if is_admin:
                    show_Secret(secret_Code)
                else:
                    print("❌ Cheat code only available to admin.")
                continue

            if mode == "numbers":
                valid_Guess = len(raw) == 4 and all(c in "123456" for c in raw)
                guess = list(raw)
                if not valid_Guess:
                    print("Invalid input. Enter 4 digits from 1 to 6.")
            else:
                guess = raw.split()
                valid_Guess = len(guess) == 4 and all(
                    word.lower() in COLOR_SET for word in guess
                )
                if not valid_Guess:
                    print(
                        "Invalid input. Enter 4 valid color names separated "
                        "by spaces."
                    )
                    print("Example: Red Blue Green Yellow")

        black, white = get_Feedback(secret_Code, guess)
        print(
            f"Black pegs (correct position): {black}, "
            f"White pegs (wrong position): {white}"
        )

        if black == 4:
            print(
                f"🎉 Congratulations! You guessed the code: "
                f"{' '.join(secret_Code)}"
            )
            return

    print(
        f"❌ Sorry, you've used all attempts. "
        f"The correct code was: {' '.join(secret_Code)}"
    )


if __name__ == "__main__":
    is_admin = False
    while True:
        print("\nMain Menu:")
        print("1. Play Mastermind")
        print("2. Login as Admin")
        print("3. Quit")
        print(
            "Note: Admins can use 'cheat' during a game "
            "to reveal the secret code."
        )
        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            play_Mastermind(is_admin)
        elif choice == "2":
            is_admin = admin_login()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")
