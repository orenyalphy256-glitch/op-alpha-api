import csv
import sqlite3
import os

DB = "data/contacts.db"
IMPORT_FILE = "99-Logs/contacts_import.csv"

def import_contacts():
    """Import contacts from a CSV file into the database."""
    if not os.path.exists(IMPORT_FILE):
        print(f"Import file not found: {IMPORT_FILE}")
        print("Please make sure the file exists before running this script.")

    with open(IMPORT_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        contacts = [(row["name"], row["phone"]) for row in reader]
    if not contacts:
        print("No contacts found in import file.")
        return
    
    with sqlite3.connect(DB) as conn:
        conn.executemany("INSERT INTO contacts (name, phone, created_at) VALUES (?, ?, datetime('now'))", contacts)
        conn.commit()
        print(f"Successfully imported{len(contacts)} contacts.")

if __name__ == "__main__":
    import_contacts()
        
