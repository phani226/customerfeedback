import sqlite3
import os

OLD_DB = "feedback.db"
TEMP_DB = "feedback_temp.db"

if not os.path.exists(OLD_DB):
    print("Old database does not exist.")
    exit()

# Connect to old database
conn_old = sqlite3.connect(OLD_DB)
cursor_old = conn_old.cursor()

# Fetch old feedback data
try:
    cursor_old.execute("SELECT id, name, message FROM feedback")
    old_data = cursor_old.fetchall()
except sqlite3.OperationalError as e:
    print("Error reading old feedback table:", e)
    old_data = []

conn_old.close()

# Create a new database with username column
conn_new = sqlite3.connect(TEMP_DB)
cursor_new = conn_new.cursor()

cursor_new.execute("""
    CREATE TABLE feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        message TEXT NOT NULL
    )
""")

# Map old 'name' to 'username' and insert
for row in old_data:
    _id, name, message = row
    username = name  # You can map differently if needed
    cursor_new.execute("INSERT INTO feedback (username, message) VALUES (?, ?)", (username, message))

conn_new.commit()
conn_new.close()

# Backup old DB and replace
os.rename(OLD_DB, OLD_DB.replace(".db", "_backup.db"))
os.rename(TEMP_DB, OLD_DB)

print("Migration completed. Old DB backed up as feedback_backup.db.")
