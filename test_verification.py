import database as db
import os

# Clean up previous db for testing
if os.path.exists("library.db"):
    os.remove("library.db")

print("Initializing DB...")
db.init_db()

print("\n--- Testing Books ---")
db.add_book("The Great Gatsby", "F. Scott Fitzgerald", "Fiction", 5)
db.add_book("1984", "George Orwell", "Sci-Fi", 3)
books = db.get_all_books()
print(f"Books added: {len(books)}")
print(books[['title', 'available_copies']])

print("\n--- Testing Members ---")
db.add_member("John Doe", "john@example.com", "1234567890")
members = db.get_all_members()
print(f"Members added: {len(members)}")
print(members[['name', 'email']])

print("\n--- Testing Transactions ---")
# Issue book id 1 to member id 1
print("Issuing book 1 to member 1...")
res = db.issue_book(1, 1)
print(f"Result: {res}")

books = db.get_all_books()
print("Book 1 available copies (should be 4):", books.loc[books['id'] == 1, 'available_copies'].values[0])

# Return book
txns = db.get_transactions(active_only=True)
txn_id = txns.iloc[0]['id']
print(f"Returning transaction {txn_id}...")
res = db.return_book(txn_id)
print(f"Result: {res}")

books = db.get_all_books()
print("Book 1 available copies (should be 5):", books.loc[books['id'] == 1, 'available_copies'].values[0])

print("\nVerification Complete.")
