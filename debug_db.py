import database as db
import os
import sqlite3

# Clean up
if os.path.exists("library.db"):
    os.remove("library.db")

print("Initializing DB...")
db.init_db()

print("Adding Book...")
db.add_book("Test Book", "Author", "Genre", 5)

print("Adding Member...")
db.add_member("Test Member", "tm@tm.com", "111")

# Manually check ID
conn = sqlite3.connect("library.db")
c = conn.cursor()
c.execute("SELECT id, available_copies FROM books")
print(f"Books in DB: {c.fetchall()}")
conn.close()

print("Issuing Book 1 to Member 1...")
print(db.issue_book(1, 1))

conn = sqlite3.connect("library.db")
c = conn.cursor()
c.execute("SELECT id, available_copies FROM books")
print(f"Books after issue: {c.fetchall()}")
conn.close()

# Get txn id manually
conn = sqlite3.connect("library.db")
c = conn.cursor()
c.execute("SELECT id FROM transactions WHERE status='Issued'")
txn_id = c.fetchone()[0]
conn.close()
print(f"Transaction ID: {txn_id} (type: {type(txn_id)})")

print(f"Returning Book with txn_id {txn_id}...")
print(db.return_book(txn_id))

conn = sqlite3.connect("library.db")
c = conn.cursor()
c.execute("SELECT id, available_copies FROM books")
res = c.fetchall()
print(f"Books after return: {res}")
conn.close()

if res[0][1] == 5:
    print("SUCCESS")
else:
    print("FAILURE")
