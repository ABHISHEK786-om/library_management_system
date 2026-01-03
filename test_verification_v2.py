import database as db
import os
import time

# Clean up previous db for testing
if os.path.exists("library.db"):
    os.remove("library.db")

print("Initializing DB...")
db.init_db()

print("\n--- Adding Book ---")
db.add_book("Test Book", "Author", "Genre", 5)
books = db.get_all_books()
val = books.loc[books['id'] == 1, 'available_copies'].values[0]
print(f"Initial copies: {val} (Expected 5)")

print("\n--- Adding Member ---")
db.add_member("Test Member", "test@test.com", "000")

print("\n--- Issuing Book ---")
res = db.issue_book(1, 1)
print(f"Issue result: {res}")
books = db.get_all_books()
val = books.loc[books['id'] == 1, 'available_copies'].values[0]
print(f"Copies after issue: {val} (Expected 4)")

print("\n--- Returning Book ---")
txns = db.get_transactions(active_only=True)
txn_id = txns.iloc[0]['id']
print(f"Returning txn {txn_id}...")
res = db.return_book(txn_id)
print(f"Return result: {res}")

books = db.get_all_books()
val = books.loc[books['id'] == 1, 'available_copies'].values[0]
print(f"Copies after return: {val} (Expected 5)")

if val == 5:
    print("SUCCESS: Logic Verified")
else:
    print("FAILURE: Return logic failed")
