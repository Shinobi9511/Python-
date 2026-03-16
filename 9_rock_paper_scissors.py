import random

CHOICES = ["rock", "paper", "scissors"]

ART = {
    "rock":     ["    _______", "---'   ____)","      (_____)","      (_____)","      (____)","---.__(___)"],
    "paper":    ["    _______", "---'   ____)____","          ______)","          _______)","         _______)","---.__________)"],
    "scissors": ["    _______", "---'   ____)____","          ______)","       __________)","      (____)","---.__(___)"],
}

OUTCOMES = {
    ("rock", "scissors"): "Rock smashes Scissors!",
    ("scissors", "paper"): "Scissors cuts Paper!",
    ("paper", "rock"): "Paper covers Rock!",
}


def get_winner(player: str, computer: str) -> str:
    """Returns 'player', 'computer', or 'tie'."""
    if player == computer:
        return "tie"
    elif (player, computer) in OUTCOMES:
        return "player"
    else:
        return "computer"


def display_choices(player: str, computer: str):
    """Side-by-side ASCII art."""
    player_art = ART[player]
    computer_art = ART[computer]

    print(f"\n  {'YOU':<30}  COMPUTER")
    print(f"  {player.upper():<30}  {computer.upper()}")
    for p_line, c_line in zip(player_art, computer_art):
        print(f"  {p_line:<30}  {c_line}")


def play_round(score: dict) -> bool:
    """Play one round. Returns True if game should continue."""
    print("\n  Choose: rock / paper / scissors / quit")
    choice = input("  Your move: ").strip().lower()

    if choice == "quit":
        return False
    if choice not in CHOICES:
        print("  ⚠️  Invalid choice. Try again.")
        return True

    computer_choice = random.choice(CHOICES)
    display_choices(choice, computer_choice)

    result = get_winner(choice, computer_choice)

    if result == "tie":
        print("\n  🤝 It's a tie!")
        score["ties"] += 1
    elif result == "player":
        msg = OUTCOMES[(choice, computer_choice)]
        print(f"\n  🎉 You win! {msg}")
        score["player"] += 1
    else:
        msg = OUTCOMES[(computer_choice, choice)]
        print(f"\n  💻 Computer wins! {msg}")
        score["computer"] += 1

    print(f"\n  Score → You: {score['player']}  |  Computer: {score['computer']}  |  Ties: {score['ties']}")
    return True


def best_of_mode(n: int):
    """Play a Best-of-N series."""
    target = (n // 2) + 1
    score = {"player": 0, "computer": 0, "ties": 0}

    print(f"\n  🏆 Best of {n} — First to {target} wins!\n")

    while score["player"] < target and score["computer"] < target:
        if not play_round(score):
            break

    print("\n  === SERIES RESULT ===")
    if score["player"] >= target:
        print(f"  🎉 YOU WIN THE SERIES! ({score['player']} – {score['computer']})")
    elif score["computer"] >= target:
        print(f"  💻 COMPUTER WINS THE SERIES! ({score['computer']} – {score['player']})")
    else:
        print("  Series ended early.")


def free_play_mode():
    """Free play until user quits."""
    score = {"player": 0, "computer": 0, "ties": 0}
    while play_round(score):
        pass
    total = score["player"] + score["computer"] + score["ties"]
    print(f"\n  Played {total} rounds.")


def main():
    print("=" * 45)
    print("      ROCK, PAPER, SCISSORS ✊📄✂️")
    print("=" * 45)

    while True:
        print("\n  1. Free Play")
        print("  2. Best of 3")
        print("  3. Best of 5")
        print("  4. Best of 7")
        print("  5. Exit")

        choice = input("\n  Select mode: ").strip()

        if choice == "1":
            free_play_mode()
        elif choice == "2":
            best_of_mode(3)
        elif choice == "3":
            best_of_mode(5)
        elif choice == "4":
            best_of_mode(7)
        elif choice == "5":
            print("\n  GG! 👋\n")
            break
        else:
            print("  ⚠️  Invalid choice.")


if __name__ == "__main__":
    main()
