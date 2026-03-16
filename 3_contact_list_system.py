import json
import os
import re

CONTACTS_FILE = "contacts.json"


def load_contacts() -> dict:
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, "r") as f:
            return json.load(f)
    return {}


def save_contacts(contacts: dict):
    with open(CONTACTS_FILE, "w") as f:
        json.dump(contacts, f, indent=4)


def is_valid_phone(phone: str) -> bool:
    return bool(re.fullmatch(r"[\d\s\-\+\(\)]{7,15}", phone))


def is_valid_email(email: str) -> bool:
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email))


def add_contact(contacts: dict):
    print("\n  ➕ ADD CONTACT")
    name = input("  Name: ").strip().title()
    if not name:
        print("  ⚠️  Name cannot be empty.")
        return
    if name in contacts:
        print(f"  ⚠️  Contact '{name}' already exists. Use Update instead.")
        return

    phone = input("  Phone: ").strip()
    if phone and not is_valid_phone(phone):
        print("  ⚠️  Invalid phone format.")
        return

    email = input("  Email: ").strip()
    if email and not is_valid_email(email):
        print("  ⚠️  Invalid email format.")
        return

    address = input("  Address (optional): ").strip()

    contacts[name] = {"phone": phone, "email": email, "address": address}
    save_contacts(contacts)
    print(f"  ✅ Contact '{name}' added successfully.")


def view_all_contacts(contacts: dict):
    print("\n  📋 ALL CONTACTS")
    if not contacts:
        print("  (No contacts found)")
        return
    print(f"  {'#':<4} {'Name':<22} {'Phone':<18} {'Email'}")
    print("  " + "-" * 68)
    for i, (name, info) in enumerate(sorted(contacts.items()), start=1):
        print(f"  {i:<4} {name:<22} {info['phone']:<18} {info['email']}")


def search_contact(contacts: dict):
    print("\n  🔍 SEARCH CONTACT")
    query = input("  Enter name to search: ").strip().title()
    results = {k: v for k, v in contacts.items() if query in k}
    if not results:
        print(f"  ❌ No contact found for '{query}'.")
        return
    for name, info in results.items():
        print(f"\n  👤 {name}")
        print(f"     Phone  : {info['phone'] or 'N/A'}")
        print(f"     Email  : {info['email'] or 'N/A'}")
        print(f"     Address: {info['address'] or 'N/A'}")


def update_contact(contacts: dict):
    print("\n  ✏️  UPDATE CONTACT")
    name = input("  Enter contact name to update: ").strip().title()
    if name not in contacts:
        print(f"  ❌ Contact '{name}' not found.")
        return

    info = contacts[name]
    print(f"  Updating: {name} | Leave blank to keep current value.")

    new_phone = input(f"  Phone [{info['phone']}]: ").strip()
    new_email = input(f"  Email [{info['email']}]: ").strip()
    new_address = input(f"  Address [{info['address']}]: ").strip()

    if new_phone:
        if not is_valid_phone(new_phone):
            print("  ⚠️  Invalid phone. Update cancelled.")
            return
        contacts[name]["phone"] = new_phone
    if new_email:
        if not is_valid_email(new_email):
            print("  ⚠️  Invalid email. Update cancelled.")
            return
        contacts[name]["email"] = new_email
    if new_address:
        contacts[name]["address"] = new_address

    save_contacts(contacts)
    print(f"  ✅ Contact '{name}' updated.")


def delete_contact(contacts: dict):
    print("\n  🗑️  DELETE CONTACT")
    name = input("  Enter contact name to delete: ").strip().title()
    if name not in contacts:
        print(f"  ❌ Contact '{name}' not found.")
        return
    confirm = input(f"  Are you sure you want to delete '{name}'? (y/n): ").lower()
    if confirm == "y":
        del contacts[name]
        save_contacts(contacts)
        print(f"  ✅ Contact '{name}' deleted.")
    else:
        print("  ↩️  Deletion cancelled.")


def main():
    contacts = load_contacts()

    menu = {
        "1": ("Add Contact", add_contact),
        "2": ("View All Contacts", view_all_contacts),
        "3": ("Search Contact", search_contact),
        "4": ("Update Contact", update_contact),
        "5": ("Delete Contact", delete_contact),
        "6": ("Exit", None),
    }

    while True:
        print("\n" + "=" * 40)
        print("       CONTACT LIST SYSTEM")
        print("=" * 40)
        for key, (label, _) in menu.items():
            print(f"  {key}. {label}")
        print()

        choice = input("  Enter choice: ").strip()
        if choice == "6":
            print("\n  Goodbye! 👋\n")
            break
        elif choice in menu:
            _, func = menu[choice]
            func(contacts)
        else:
            print("  ⚠️  Invalid choice. Try again.")


if __name__ == "__main__":
    main()
