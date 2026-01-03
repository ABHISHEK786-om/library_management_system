import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = "library.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()
    
    # Books Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            genre TEXT,
            total_copies INTEGER NOT NULL,
            available_copies INTEGER NOT NULL
        )
    ''')
    
    # Members Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            phone TEXT,
            registration_date DATE DEFAULT (date('now'))
        )
    ''')
    
    # Transactions Table (for Issues/Returns)
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER,
            member_id INTEGER,
            issue_date DATE DEFAULT (date('now')),
            return_date DATE,
            status TEXT DEFAULT 'Issued',
            FOREIGN KEY (book_id) REFERENCES books (id),
            FOREIGN KEY (member_id) REFERENCES members (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# --- Book Operations ---
def add_book(title, author, genre, total_copies):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO books (title, author, genre, total_copies, available_copies) VALUES (?, ?, ?, ?, ?)', 
                  (title, author, genre, total_copies, total_copies))
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        conn.close()

def get_all_books():
    conn = get_connection()
    df = pd.read_sql('SELECT * FROM books', conn)
    conn.close()
    return df

def delete_book(book_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()

# --- Member Operations ---
def add_member(name, email, phone):
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute('INSERT INTO members (name, email, phone) VALUES (?, ?, ?)', (name, email, phone))
        conn.commit()
        return True
    except Exception as e: # Handle duplicate email probably
        print(e)
        return False
    finally:
        conn.close()

def get_all_members():
    conn = get_connection()
    df = pd.read_sql('SELECT * FROM members', conn)
    conn.close()
    return df

# --- Transaction Operations ---
def issue_book(book_id, member_id):
    conn = get_connection()
    c = conn.cursor()
    
    # Check availability
    c.execute('SELECT available_copies FROM books WHERE id = ?', (book_id,))
    result = c.fetchone()
    if not result or result[0] <= 0:
        conn.close()
        return "Book not available"
    
    try:
        # Create transaction
        c.execute('INSERT INTO transactions (book_id, member_id, status) VALUES (?, ?, ?)', (book_id, member_id, 'Issued'))
        
        # Decrease stock
        c.execute('UPDATE books SET available_copies = available_copies - 1 WHERE id = ?', (book_id,))
        
        conn.commit()
        return "Success"
    except Exception as e:
        return str(e)
    finally:
        conn.close()

def return_book(transaction_id):
    conn = get_connection()
    c = conn.cursor()
    
    # Get details
    c.execute('SELECT book_id, status FROM transactions WHERE id = ?', (transaction_id,))
    txn = c.fetchone()
    if not txn:
        conn.close()
        return "Transaction not found"
    
    if txn[1] == "Returned":
        conn.close()
        return "Book already returned"
    
    book_id = txn[0]
    
    try:
        # Update transaction
        c.execute('UPDATE transactions SET return_date = date("now"), status = "Returned" WHERE id = ?', (transaction_id,))
        
        # Increase stock
        c.execute('UPDATE books SET available_copies = available_copies + 1 WHERE id = ?', (book_id,))
        
        conn.commit()
        return "Success"
    except Exception as e:
        return str(e)
    finally:
        conn.close()

def get_transactions(active_only=False):
    conn = get_connection()
    query = '''
        SELECT t.id, b.title, m.name, t.issue_date, t.return_date, t.status 
        FROM transactions t
        JOIN books b ON t.book_id = b.id
        JOIN members m ON t.member_id = m.id
    '''
    if active_only:
        query += " WHERE t.status = 'Issued'"
        
    df = pd.read_sql(query, conn)
    conn.close()
    return df
