import sqlite3, csv

DB = "data/contacts.db"

with sqlite3.connect(DB) as conn:
    cur = conn.execute("SELECT name, phone, created_at FROM contacts")
    with open("99-Logs/contacts_export.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "phone", "created_at"])
        for row in cur:
            writer.writerow(row)