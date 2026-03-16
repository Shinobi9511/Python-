# 🐍 Python Projects — 10 Complete Projects

---

## 📦 Installation (Run Once)

```bash
pip install requests beautifulsoup4 Pillow pygame pyperclip
```

---

## 🗂️ Projects Overview

| # | File | Description | Run Command |
|---|------|-------------|-------------|
| 1 | `1_number_guessing_game.py`  | Guess the secret number with hints         | `python 1_number_guessing_game.py`  |
| 2 | `2_google_image_downloader.py` | Download images by search query          | `python 2_google_image_downloader.py` |
| 3 | `3_contact_list_system.py`  | Add/search/update/delete contacts (JSON)  | `python 3_contact_list_system.py`   |
| 4 | `4_snake_game.py`           | Classic snake game with Pygame            | `python 4_snake_game.py`            |
| 5 | `5_gif_creator.py`          | Combine images into an animated GIF       | `python 5_gif_creator.py`           |
| 6 | `6_website_blocker.py`      | Block/unblock websites via hosts file     | `sudo python 6_website_blocker.py`  |
| 7 | `7_dice_rolling_simulator.py` | Roll dice (d4–d100) with ASCII art      | `python 7_dice_rolling_simulator.py` |
| 8 | `8_password_generator.py`   | Generate strong passwords + check strength| `python 8_password_generator.py`    |
| 9 | `9_rock_paper_scissors.py`  | RPS with ASCII art + Best-of-N mode       | `python 9_rock_paper_scissors.py`   |
|10 | `10_currency_converter.py`  | Live currency conversion (160+ currencies)| `python 10_currency_converter.py`   |

---

## 📋 Per-Project Notes

### 1️⃣  Number Guessing Game
- No dependencies needed — uses only built-in `random`
- Three difficulty levels: Easy / Medium / Hard

### 2️⃣  Google Image Downloader
- Uses DuckDuckGo (no API key required)
- Requires: `pip install requests beautifulsoup4`
- Downloads images to a folder you specify

### 3️⃣  Contact List System
- No dependencies — uses only built-in `json`
- Saves contacts to `contacts.json` in same folder
- Validates phone and email formats

### 4️⃣  Snake Game
- Requires: `pip install pygame`
- Controls: Arrow keys to move
- Press R to restart, Q to quit after Game Over

### 5️⃣  GIF Creator
- Requires: `pip install Pillow`
- Put your images in a folder, then run the script
- Supports PNG, JPG, BMP, WEBP

### 6️⃣  Website Blocker
- ⚠️  MUST run as administrator/root
  - Linux/macOS: `sudo python 6_website_blocker.py`
  - Windows: Right-click → "Run as Administrator"
- Edits your system hosts file to block sites

### 7️⃣  Dice Rolling Simulator
- No dependencies — uses only built-in `random`
- Supports d4, d6, d8, d10, d12, d20, d100
- Shows ASCII art for d6 dice

### 8️⃣  Password Generator
- Optional: `pip install pyperclip` (for clipboard copy)
- Saves passwords to `passwords.txt` (base64 encoded)
- Built-in password strength checker

### 9️⃣  Rock, Paper, Scissors
- No dependencies needed
- Free Play mode + Best-of-3/5/7 series
- Shows ASCII hand art for each move

### 🔟  Currency Converter
- Requires: `pip install requests`
- Uses live ExchangeRate-API (no key needed)
- Falls back to offline rates if no internet

---

## 🖥️ Python Version
Requires **Python 3.8+**

Check your version:
```bash
python --version
```
