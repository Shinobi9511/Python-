import random

DICE_ART = {
    1: ["┌─────────┐", "│         │", "│    ●    │", "│         │", "└─────────┘"],
    2: ["┌─────────┐", "│  ●      │", "│         │", "│      ●  │", "└─────────┘"],
    3: ["┌─────────┐", "│  ●      │", "│    ●    │", "│      ●  │", "└─────────┘"],
    4: ["┌─────────┐", "│  ●   ●  │", "│         │", "│  ●   ●  │", "└─────────┘"],
    5: ["┌─────────┐", "│  ●   ●  │", "│    ●    │", "│  ●   ●  │", "└─────────┘"],
    6: ["┌─────────┐", "│  ●   ●  │", "│  ●   ●  │", "│  ●   ●  │", "└─────────┘"],
}

DICE_TYPES = [4, 6, 8, 10, 12, 20, 100]


def roll_dice(num_dice: int, sides: int) -> list:
    return [random.randint(1, sides) for _ in range(num_dice)]


def display_d6_art(results: list):
    chunk_size = 5
    for chunk_start in range(0, len(results), chunk_size):
        chunk = results[chunk_start:chunk_start + chunk_size]
        for row in range(5):
            line = "  ".join(DICE_ART[val][row] for val in chunk)
            print(f"  {line}")
        print()


def get_roll_stats(results: list) -> dict:
    return {
        "total": sum(results),
        "min": min(results),
        "max": max(results),
        "avg": round(sum(results) / len(results), 2),
    }


def main():
    history = []

    print("=" * 50)
    print("        DICE ROLLING SIMULATOR 🎲")
    print("=" * 50)

    while True:
        print("\n  Options:")
        print("  1. Roll dice")
        print("  2. View roll history")
        print("  3. Clear history")
        print("  4. Exit")

        choice = input("\n  Choice: ").strip()

        if choice == "1":
            # Select dice type
            print(f"\n  Dice types: {', '.join(f'd{d}' for d in DICE_TYPES)}")
            sides_input = input("  Sides (e.g. 6 or d20): ").strip().lower().replace("d", "")
            try:
                sides = int(sides_input)
                if sides < 2:
                    raise ValueError
            except ValueError:
                print("  ⚠️  Invalid dice type.")
                continue

            # Number of dice
            try:
                num_dice = int(input("  How many dice? [default: 1]: ").strip() or 1)
                if num_dice < 1 or num_dice > 20:
                    raise ValueError
            except ValueError:
                print("  ⚠️  Enter a number between 1 and 20.")
                continue

            results = roll_dice(num_dice, sides)
            stats = get_roll_stats(results)

            print(f"\n  🎲 Rolling {num_dice}d{sides}...\n")

            if sides == 6 and num_dice <= 10:
                display_d6_art(results)
            else:
                print(f"  Results: {results}\n")

            print(f"  Total : {stats['total']}")
            print(f"  Min   : {stats['min']}  |  Max: {stats['max']}  |  Avg: {stats['avg']}")

            entry = {"dice": f"{num_dice}d{sides}", "results": results, "total": stats["total"]}
            history.append(entry)

        elif choice == "2":
            print("\n  📜 ROLL HISTORY")
            if not history:
                print("  (No rolls yet)")
            else:
                for i, entry in enumerate(history[-10:], 1):
                    print(f"  {i:>2}. {entry['dice']:>7}  →  {entry['results']}  (Total: {entry['total']})")

        elif choice == "3":
            history.clear()
            print("  ✅ History cleared.")

        elif choice == "4":
            print("\n  Good luck! 🍀\n")
            break
        else:
            print("  ⚠️  Invalid choice.")


if __name__ == "__main__":
    main()
