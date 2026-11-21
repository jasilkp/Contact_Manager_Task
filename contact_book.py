"""
Contact Book - A command-line app to manage contacts.
Contacts are saved to a text file (contacts.txt).
"""

import os
import re

# file where contacts are saved
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "contacts.txt")
SEPARATOR = " | "


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\n  Press Enter to return to the menu...")


def validate_phone(phone):
    """Check if phone number is valid (7-15 digits, allows +, -, spaces)."""
    digits = re.sub(r"\D", "", phone)
    if len(digits) < 7 or len(digits) > 15:
        return False
    return bool(re.fullmatch(r"[\d\s\-\(\)\+]+", phone))


def validate_email(email):
    """Check if email format is valid."""
    return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email))


def load_contacts():
    """Load all contacts from the text file."""
    contacts = []
    if not os.path.exists(DATA_FILE):
        return contacts

    with open(DATA_FILE, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            # split only first 3 so address can contain '|'
            parts = line.split(SEPARATOR, 3)
            if len(parts) == 4:
                contacts.append({
                    "name":    parts[0].strip(),
                    "phone":   parts[1].strip(),
                    "email":   parts[2].strip(),
                    "address": parts[3].strip(),
                })
    return contacts


def save_contacts(contacts):
    """Save all contacts back to the text file."""
    with open(DATA_FILE, "w", encoding="utf-8") as fh:
        for c in contacts:
            fh.write(SEPARATOR.join([
                c["name"], c["phone"], c["email"], c["address"]
            ]) + "\n")


def print_header():
    print()
    print("  ╔══════════════════════════════════════╗")
    print("  ║       📒 CONTACT BOOK MENU           ║")
    print("  ╠══════════════════════════════════════╣")
    print("  ║  1. Add New Contact                  ║")
    print("  ║  2. View All Contacts                ║")
    print("  ║  3. Search Contacts                  ║")
    print("  ║  4. Update a Contact                 ║")
    print("  ║  5. Delete a Contact                 ║")
    print("  ║  6. Exit                             ║")
    print("  ╚══════════════════════════════════════╝")
    print()


def print_contacts_table(contacts):
    """Print contacts in a nice table format."""
    if not contacts:
        print("\n  (No contacts to display.)\n")
        return

    headers = ["#", "Name", "Phone", "Email", "Address"]
    col_widths = [
        max(len(headers[0]), len(str(len(contacts)))),
        max(len(headers[1]), max(len(c["name"])    for c in contacts)),
        max(len(headers[2]), max(len(c["phone"])   for c in contacts)),
        max(len(headers[3]), max(len(c["email"])   for c in contacts)),
        max(len(headers[4]), max(len(c["address"]) for c in contacts)),
    ]

    divider = "  +-" + "-+-".join("-" * w for w in col_widths) + "-+"

    print()
    print(divider)
    header_row = "  | " + " | ".join(
        h.ljust(w) for h, w in zip(headers, col_widths)
    ) + " |"
    print(header_row)
    print(divider)

    for idx, c in enumerate(contacts, start=1):
        row = "  | " + " | ".join([
            str(idx).ljust(col_widths[0]),
            c["name"].ljust(col_widths[1]),
            c["phone"].ljust(col_widths[2]),
            c["email"].ljust(col_widths[3]),
            c["address"].ljust(col_widths[4]),
        ]) + " |"
        print(row)

    print(divider)
    print(f"  Total contacts: {len(contacts)}")
    print()


def add_contact(contacts):
    """Add a new contact to the list."""
    print("\n  ── Add New Contact ──────────────────────\n")

    name = input("  Name    : ").strip()
    if not name:
        print("  ⚠ Name cannot be empty.")
        return

    while True:
        phone = input("  Phone   : ").strip()
        if validate_phone(phone):
            break
        print("  ⚠ Invalid phone number. Use digits (7-15), may include +, -, spaces.")

    while True:
        email = input("  Email   : ").strip()
        if validate_email(email):
            break
        print("  ⚠ Invalid email format. Example: user@example.com")

    address = input("  Address : ").strip() or "N/A"

    contacts.append({
        "name": name,
        "phone": phone,
        "email": email,
        "address": address,
    })
    save_contacts(contacts)
    print(f"\n  ✅ Contact '{name}' added successfully!")


def view_contacts(contacts):
    """Show all contacts."""
    print("\n  ── All Contacts ────────────────────────")
    print_contacts_table(contacts)


def search_contacts(contacts):
    """Search for a contact by name, phone or email."""
    print("\n  ── Search Contacts ─────────────────────\n")
    query = input("  Enter search term (name / phone / email): ").strip().lower()
    if not query:
        print("  ⚠ Search term cannot be empty.")
        return

    results = [
        c for c in contacts
        if query in c["name"].lower()
        or query in c["phone"].lower()
        or query in c["email"].lower()
    ]

    if results:
        print(f"\n  Found {len(results)} result(s):")
        print_contacts_table(results)
    else:
        print("  🔍 No contacts matched your search.\n")


def update_contact(contacts):
    """Update an existing contact."""
    print("\n  ── Update a Contact ────────────────────")
    if not contacts:
        print("\n  (No contacts available to update.)\n")
        return

    print_contacts_table(contacts)

    try:
        idx = int(input("  Enter the contact number to update: ")) - 1
    except ValueError:
        print("  ⚠ Please enter a valid number.")
        return

    if idx < 0 or idx >= len(contacts):
        print("  ⚠ Invalid contact number.")
        return

    contact = contacts[idx]
    print(f"\n  Updating contact: {contact['name']}")
    print("  (Press Enter to keep the current value)\n")

    new_name = input(f"  Name    [{contact['name']}]: ").strip()
    if new_name:
        contact["name"] = new_name

    while True:
        new_phone = input(f"  Phone   [{contact['phone']}]: ").strip()
        if not new_phone:
            break
        if validate_phone(new_phone):
            contact["phone"] = new_phone
            break
        print("  ⚠ Invalid phone number.")

    while True:
        new_email = input(f"  Email   [{contact['email']}]: ").strip()
        if not new_email:
            break
        if validate_email(new_email):
            contact["email"] = new_email
            break
        print("  ⚠ Invalid email format.")

    new_address = input(f"  Address [{contact['address']}]: ").strip()
    if new_address:
        contact["address"] = new_address

    save_contacts(contacts)
    print(f"\n  ✅ Contact '{contact['name']}' updated successfully!")


def delete_contact(contacts):
    """Delete a contact after asking for confirmation."""
    print("\n  ── Delete a Contact ────────────────────")
    if not contacts:
        print("\n  (No contacts available to delete.)\n")
        return

    print_contacts_table(contacts)

    try:
        idx = int(input("  Enter the contact number to delete: ")) - 1
    except ValueError:
        print("  ⚠ Please enter a valid number.")
        return

    if idx < 0 or idx >= len(contacts):
        print("  ⚠ Invalid contact number.")
        return

    contact = contacts[idx]
    confirm = input(f"  Are you sure you want to delete '{contact['name']}'? (y/n): ").strip().lower()
    if confirm == "y":
        contacts.pop(idx)
        save_contacts(contacts)
        print(f"\n  ✅ Contact '{contact['name']}' deleted successfully!")
    else:
        print("  ❌ Deletion cancelled.")


def main():
    contacts = load_contacts()

    while True:
        clear_screen()
        print_header()

        choice = input("  Enter your choice (1-6): ").strip()

        if choice == "1":
            add_contact(contacts)
            pause()
        elif choice == "2":
            view_contacts(contacts)
            pause()
        elif choice == "3":
            search_contacts(contacts)
            pause()
        elif choice == "4":
            update_contact(contacts)
            pause()
        elif choice == "5":
            delete_contact(contacts)
            pause()
        elif choice == "6":
            print("\n  👋 Goodbye! Your contacts are saved.\n")
            break
        else:
            print("  ⚠ Invalid choice. Please enter a number between 1 and 6.")
            pause()


if __name__ == "__main__":
    main()
