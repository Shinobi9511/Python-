import random
import string
import os
import base64

try:
    import pyperclip
    CLIPBOARD = True
except ImportError:
    CLIPBOARD = False

SAVE_FILE = "passwords.txt"


def generate_password(
    length: int,
    use_upper: bool,
    use_lower: bool,
    use_digits: bool,
    use_symbols: bool,
    exclude_ambiguous: bool,
) -> str:
    pool = ""
    required = []

    upper_chars = string.ascii_uppercase
    lower_chars = string.ascii_lowercase
    digit_chars = string.digits
    symbol_chars = "!@#$%^&*()-_=+[]{}|;:,.<>?"

    if exclude_ambiguous:
        upper_chars = upper_chars.replace("O", "").replace("I", "")
        lower_chars = lower_chars.replace("l", "")
        digit_chars = digit_chars.replace("0", "").replace("1", "")

    if use_upper:
        pool += upper_chars
        required.append(random.choice(upper_chars))
    if use_lower:
        pool += lower_chars
        required.append(random.choice(lower_chars))
    if use_digits:
        pool += digit_chars
        required.append(random.choice(digit_chars))
    if use_symbols:
        pool += symbol_chars
        required.append(random.choice(symbol_chars))

    if not pool:
        raise ValueError("At least one character type must be selected.")

    remaining_length = length - len(required)
    password_chars = required + random.choices(pool, k=remaining_length)
    random.shuffle(password_chars)
    return "".join(password_chars)


def check_strength(password: str) -> tuple:
    score = 0
    feedback = []

    if len(password) >= 12:
        score += 1
    else:
        feedback.append("Use at least 12 characters")

    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("Add uppercase letters")

    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("Add lowercase letters")

    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("Add numbers")

    if any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?" for c in password):
        score += 1
    else:
        feedback.append("Add special characters")

    levels = {5: "💪 Very Strong", 4: "✅ Strong", 3: "⚠️  Moderate", 2: "❌ Weak", 1: "🔴 Very Weak"}
    strength = levels.get(score, "🔴 Very Weak")
    return strength, feedback


def save_password(label: str, password: str):
    """Save password to file with basic obfuscation."""
    encoded = base64.b64encode(password.encode()).decode()
    with open(SAVE_FILE, "a") as f:
        f.write(f"{label} | {encoded}\n")
    print(f"  💾 Saved to {SAVE_FILE}")


def view_saved():
    if not os.path.exists(SAVE_FILE):
        print("  (No saved passwords)")
        return
    print("\n  📂 Saved Passwords (decoded):\n")
    with open(SAVE_FILE, "r") as f:
        for i, line in enumerate(f, 1):
            parts = line.strip().split(" | ", 1)
            if len(parts) == 2:
                label, encoded = parts
                decoded = base64.b64decode(encoded.encode()).decode()
                print(f"  {i:>3}. {label:<25} → {decoded}")


def main():
    print("=" * 50)
    print("          PASSWORD GENERATOR 🔐")
    print("=" * 50)

    while True:
        print("\n  1. Generate password")
        print("  2. Check password strength")
        print("  3. View saved passwords")
        print("  4. Exit")

        choice = input("\n  Choice: ").strip()

        if choice == "1":
            try:
                length = int(input("  Password length [default: 16]: ").strip() or 16)
                if length < 4 or length > 128:
                    print("  ⚠️  Length must be between 4 and 128.")
                    continue
            except ValueError:
                print("  ⚠️  Invalid length.")
                continue

            use_upper   = input("  Include UPPERCASE? (y/n) [y]: ").strip().lower() != "n"
            use_lower   = input("  Include lowercase? (y/n) [y]: ").strip().lower() != "n"
            use_digits  = input("  Include digits?    (y/n) [y]: ").strip().lower() != "n"
            use_symbols = input("  Include symbols?   (y/n) [y]: ").strip().lower() != "n"
            excl_ambig  = input("  Exclude ambiguous chars (0,O,l,1)? (y/n) [n]: ").strip().lower() == "y"

            try:
                try:
                    count = int(input("  How many passwords? [default: 1]: ").strip() or 1)
                except ValueError:
                    count = 1

                for i in range(count):
                    pwd = generate_password(length, use_upper, use_lower, use_digits, use_symbols, excl_ambig)
                    strength, _ = check_strength(pwd)
                    print(f"\n  {'Password':>12}: {pwd}")
                    print(f"  {'Strength':>12}: {strength}")

                    if CLIPBOARD and count == 1:
                        copy = input("\n  Copy to clipboard? (y/n): ").strip().lower()
                        if copy == "y":
                            pyperclip.copy(pwd)
                            print("  ✅ Copied!")

                    save = input("  Save this password? (y/n): ").strip().lower()
                    if save == "y":
                        label = input("  Label (e.g., 'Gmail'): ").strip() or "Unlabeled"
                        save_password(label, pwd)

            except ValueError as e:
                print(f"  ❌ {e}")

        elif choice == "2":
            pwd = input("  Enter password to check: ").strip()
            if not pwd:
                continue
            strength, tips = check_strength(pwd)
            print(f"\n  Strength: {strength}")
            if tips:
                print("  Tips to improve:")
                for tip in tips:
                    print(f"    • {tip}")

        elif choice == "3":
            view_saved()

        elif choice == "4":
            print("\n  Stay secure! 🔒\n")
            break
        else:
            print("  ⚠️  Invalid choice.")


if __name__ == "__main__":
    main()
