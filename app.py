import streamlit as st
import database as db
import pandas as pd

# Initialize DB
db.init_db()

st.set_page_config(page_title="Library Management System", layout="wide")

st.title("📚 Library Management System")

# Sidebar Navigation
menu = ["Dashboard", "Manage Books", "Manage Members", "Issue/Return Book"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Dashboard":
    st.header("Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    books = db.get_all_books()
    members = db.get_all_members()
    transactions = db.get_transactions(active_only=True)
    
    with col1:
        st.metric("Total Books", len(books))
    with col2:
        st.metric("Total Members", len(members))
    with col3:
        st.metric("Active Loans", len(transactions))
        
    st.subheader("Recently Added Books")
    if not books.empty:
        st.dataframe(books.tail(5))
    else:
        st.info("No books available.")

elif choice == "Manage Books":
    st.header("Manage Books")
    
    tab1, tab2 = st.tabs(["Add Book", "View All Books"])
    
    with tab1:
        with st.form("book_form"):
            title = st.text_input("Book Title")
            author = st.text_input("Author")
            genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Sci-Fi", "Biography", "History", "Other"])
            copies = st.number_input("Total Copies", min_value=1, value=1)
            
            submitted = st.form_submit_button("Add Book")
            if submitted:
                if title and author:
                    if db.add_book(title, author, genre, copies):
                        st.success(f"Book '{title}' added successfully!")
                    else:
                        st.error("Failed to add book.")
                else:
                    st.warning("Please fill in all fields.")
                    
    with tab2:
        books_df = db.get_all_books()
        st.dataframe(books_df, use_container_width=True)
        
        # Delete Book Section
        st.subheader("Delete Book")
        book_id_to_delete = st.number_input("Enter Book ID to Delete", min_value=0, step=1)
        if st.button("Delete Book"):
            db.delete_book(book_id_to_delete)
            st.rerun()

elif choice == "Manage Members":
    st.header("Manage Members")
    
    tab1, tab2 = st.tabs(["Register Member", "View Members"])
    
    with tab1:
        with st.form("member_form"):
            name = st.text_input("Member Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone Number")
            
            submitted = st.form_submit_button("Register Member")
            if submitted:
                if name and email:
                    if db.add_member(name, email, phone):
                        st.success(f"Member '{name}' registered successfully!")
                    else:
                        st.error("Failed to register member. Email might be duplicate.")
                else:
                    st.warning("Name and Email are required.")

    with tab2:
        members_df = db.get_all_members()
        st.dataframe(members_df, use_container_width=True)

elif choice == "Issue/Return Book":
    st.header("Issue / Return Operations")
    
    op_type = st.radio("Operation Type", ["Issue Book", "Return Book"])
    
    if op_type == "Issue Book":
        st.subheader("Issue a Book")
        
        # We need to select book and member. 
        # For better UX, let's load them, but for large datasets, ID input is safer. 
        # For this demo, let's show tables to help user find IDs or use dropdowns if small.
        # Let's use simple ID inputs for now to be robust.
        
        col1, col2 = st.columns(2)
        with col1:
             st.info("Find Book ID from 'Manage Books'")
             book_id = st.number_input("Book ID", min_value=1, step=1)
        with col2:
             st.info("Find Member ID from 'Manage Members'")
             member_id = st.number_input("Member ID", min_value=1, step=1)
             
        if st.button("Issue Book"):
            result = db.issue_book(book_id, member_id)
            if result == "Success":
                st.success("Book issued successfully!")
            else:
                st.error(f"Error: {result}")
                
    elif op_type == "Return Book":
        st.subheader("Return a Book")
        
        # Show active transactions to pick from
        active_txns = db.get_transactions(active_only=True)
        if active_txns.empty:
            st.info("No active loans found.")
        else:
            st.dataframe(active_txns)
            txn_id = st.number_input("Transaction ID to Return", min_value=1, step=1)
            
            if st.button("Return Book"):
                result = db.return_book(txn_id)
                if result == "Success":
                    st.success("Book returned successfully!")
                    st.rerun()
                else:
                    st.error(f"Error: {result}")

st.markdown("---")
st.caption("Library System v1.0")
