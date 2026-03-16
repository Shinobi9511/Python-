import random

def get_difficulty():
    print("\n Select Difficulty:")
    print("  1. Easy   (1–50,  10 attempts)")
    print("  2. Medium (1–100, 7 attempts)")
    print("  3. Hard   (1–200, 5 attempts)")
    choice = input("Enter choice (1/2/3): ").strip()
    levels = {
        "1": (1, 50, 10),
        "2": (1, 100, 7),
        "3": (1, 200, 5),
    }
    return levels.get(choice, (1, 100, 7))

def play_game():
    print("=" * 40)
    print("       NUMBER GUESSING GAME")
    print("=" * 40)

    low, high, max_attempts = get_difficulty()
    secret = random.randint(low, high)
    attempts = 0

    print(f"\n Guess the number between {low} and {high}. You have {max_attempts} attempts.\n")

    while attempts < max_attempts:
        remaining = max_attempts - attempts
        try:
            guess = int(input(f"  [{remaining} left] Your guess: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        attempts += 1

        if guess < low or guess > high:
            print(f"Out of range! Guess between {low} and {high}.")
            attempts -= 1  # Don't penalize out-of-range
        elif guess < secret:
            print("Too low! Go higher.")
        elif guess > secret:
            print("Too high! Go lower.")
        else:
            print(f"\n Correct! The number was {secret}.")
            print(f" You got it in {attempts} attempt(s)!\n")
            return

    print(f"\n  Out of attempts! The number was {secret}.\n")

def main():
    while True:
        play_game()
        again = input("  Play again? (y/n): ").strip().lower()
        if again != "y":
            print("\n  Thanks for playing! Goodbye \n")
            break

if __name__ == "__main__":
    main()
