"""
Website Blocker in Python
- Block/unblock websites by editing the system hosts file
- Requires admin/sudo privileges to run
- Works on Windows, macOS, and Linux

⚠️  Run with: sudo python 6_website_blocker.py  (Linux/Mac)
              Run as Administrator              (Windows)
"""

import os
import sys
import platform

# Hosts file location per OS
if platform.system() == "Windows":
    HOSTS_FILE = r"C:\Windows\System32\drivers\etc\hosts"
else:
    HOSTS_FILE = "/etc/hosts"

REDIRECT = "127.0.0.1"
MARKER = "# WebBlocker"


def is_admin() -> bool:
    """Check for admin/root privileges."""
    try:
        return os.getuid() == 0
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0


def load_blocked_sites() -> list:
    """Read currently blocked sites from hosts file."""
    blocked = []
    if not os.path.exists(HOSTS_FILE):
        return blocked
    with open(HOSTS_FILE, "r") as f:
        for line in f:
            if MARKER in line:
                parts = line.strip().split()
                if len(parts) >= 2:
                    blocked.append(parts[1])
    return blocked


def block_sites(sites: list):
    """Add sites to the hosts file."""
    already_blocked = load_blocked_sites()
    added = []

    with open(HOSTS_FILE, "a") as f:
        for site in sites:
            site = site.strip().lower().replace("https://", "").replace("http://", "").rstrip("/")
            if site in already_blocked:
                print(f"  ⚠️  Already blocked: {site}")
            else:
                f.write(f"\n{REDIRECT} {site} {MARKER}\n")
                f.write(f"{REDIRECT} www.{site} {MARKER}\n")
                added.append(site)
                print(f"  🔒 Blocked: {site}")

    if added:
        print(f"\n  ✅ {len(added)} site(s) blocked successfully.")


def unblock_sites(sites: list):
    """Remove sites from the hosts file."""
    sites = [s.strip().lower().replace("https://", "").replace("http://", "").rstrip("/")
             for s in sites]

    with open(HOSTS_FILE, "r") as f:
        lines = f.readlines()

    new_lines = []
    removed = set()

    for line in lines:
        parts = line.strip().split()
        skip = False
        if MARKER in line and len(parts) >= 2:
            site = parts[1].replace("www.", "")
            if site in sites:
                removed.add(site)
                skip = True
        if not skip:
            new_lines.append(line)

    with open(HOSTS_FILE, "w") as f:
        f.writelines(new_lines)

    for site in sites:
        if site in removed:
            print(f"  🔓 Unblocked: {site}")
        else:
            print(f"  ❌ Not found in block list: {site}")

    if removed:
        print(f"\n  ✅ {len(removed)} site(s) unblocked.")


def view_blocked():
    """Display all currently blocked sites."""
    blocked = load_blocked_sites()
    unique = sorted(set(s.replace("www.", "") for s in blocked))
    print("\n  🔒 Currently Blocked Sites:")
    if not unique:
        print("  (None)")
    else:
        for i, site in enumerate(unique, 1):
            print(f"  {i:>3}. {site}")


def unblock_all():
    """Remove all WebBlocker entries from hosts file."""
    with open(HOSTS_FILE, "r") as f:
        lines = f.readlines()
    new_lines = [l for l in lines if MARKER not in l]
    with open(HOSTS_FILE, "w") as f:
        f.writelines(new_lines)
    print("  ✅ All blocked sites have been removed.")


def main():
    if not is_admin():
        print("\n  ❌ This script requires administrator/root privileges.")
        print("     Linux/Mac: sudo python 6_website_blocker.py")
        print("     Windows  : Run as Administrator\n")
        sys.exit(1)

    while True:
        print("\n" + "=" * 45)
        print("         WEBSITE BLOCKER")
        print("=" * 45)
        print("  1. Block website(s)")
        print("  2. Unblock website(s)")
        print("  3. View blocked sites")
        print("  4. Unblock ALL sites")
        print("  5. Exit")

        choice = input("\n  Choice: ").strip()

        if choice == "1":
            raw = input("  Enter sites to block (comma-separated): ")
            block_sites([s.strip() for s in raw.split(",") if s.strip()])
        elif choice == "2":
            raw = input("  Enter sites to unblock (comma-separated): ")
            unblock_sites([s.strip() for s in raw.split(",") if s.strip()])
        elif choice == "3":
            view_blocked()
        elif choice == "4":
            confirm = input("  Unblock ALL sites? (y/n): ").lower()
            if confirm == "y":
                unblock_all()
        elif choice == "5":
            print("\n  Goodbye! 👋\n")
            break
        else:
            print("  ⚠️  Invalid choice.")


if __name__ == "__main__":
    main()
