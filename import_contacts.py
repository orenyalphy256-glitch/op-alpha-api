import sqlite3, csv

DB = "data/contacts.db"
with sqlite3.connect(DB) as conn:
    cur = conn.cursor()
    with open("99-Logs/contacts_import.csv", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for r in reader:
            try:
                cur.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)", (r["name"], r["phone"]))
            except sqlite3.IntegrityError:
                continue
            conn.commit()