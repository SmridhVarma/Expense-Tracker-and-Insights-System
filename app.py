from pymongo import MongoClient
from bson.objectid import ObjectId
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import streamlit as st
import urllib.parse
import warnings
import streamlit_lottie
from dotenv import load_dotenv
import os
load_dotenv()
st.set_option('deprecation.showPyplotGlobalUse', False)
warnings.filterwarnings("ignore")

def init_connection():
    username = urllib.parse.quote_plus(os.getenv("username"))
    password = urllib.parse.quote_plus(os.getenv("password"))
    cluster_name = "demo-cluster"
    return MongoClient(f"mongodb+srv://{username}:{password}@{cluster_name}.m4cgmwf.mongodb.net/")
client = init_connection()

# Connect to MongoDB
db = client["expense_tracker"]
expenses_collection = db["expenses"]
users_collection = db["users"]

# --- HIDE STREAMLIT STYLE ---
st.set_page_config(page_title="Expense Tracker", page_icon=":money_with_wings:", layout="centered", initial_sidebar_state="auto")
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


# Function to check if user exists
def user_exists(username):
    user = users_collection.find_one({"username": username})
    return user is not None

# Function to add user
def add_user(username, password):
    if not user_exists(username):
        user_data = {
            "username": username,
            "password": password
        }
        users_collection.insert_one(user_data)
        return True
    else:
        return False

# Function to authenticate user
def authenticate_user(username, password):
    user = users_collection.find_one({"username": username, "password": password})
    return user is not None

# Function to add expense
def add_expense():
    st.header("Add Expense")
    # Define the URL of the Lottie animation
    lottie_url = "https://lottie.host/embed/20dbacc1-f6eb-429f-85f7-02f3fe2f8896/dS6CcAHKzc.json"
    # Embed the Lottie animation using an HTML iframe with CSS styling
    st.write(f'<iframe src="{lottie_url}" frameborder="0" allowfullscreen="true" scrolling="no" style="width: 200px; height: 200px; margin: 0 auto; display: block;"></iframe>', unsafe_allow_html=True)
    
    category = st.selectbox("Category", [" ","Food", "Transport", "Entertainment", "Bills", "Others"])
    expense_type = st.selectbox("Type", [" ","Needs", "Wants", "Unexpected", "Routine"])
    note = st.text_input("Note")
    amount = st.number_input("Amount", value=0.0)

    if st.button("Add Expense"):
        expense_data = {
            "category": category,
            "type": expense_type,
            "note": note,
            "amount": amount,
            "date": datetime.now()
        }
        expenses_collection.insert_one(expense_data)
        st.success("Expense added successfully!")

# Function to view all expenses with filtering and sorting options
def view_expenses():
    st.title("All Expenses")
    # Define the URL of the Lottie animation
    lottie_url = "https://lottie.host/embed/ff638fd6-4dee-41e2-81d7-a754cf26cc90/HCqr7inrji.json"
    # Embed the Lottie animation using an HTML iframe with CSS styling
    st.write(f'<iframe src="{lottie_url}" frameborder="0" allowfullscreen="true" scrolling="no" style="width: 200px; height: 200px; margin: 0 auto; display: block;"></iframe>', unsafe_allow_html=True)
    # Filtering options
    filter_type = st.selectbox("Type", ["All", "Needs", "Wants", "Unexpected", "Routine"], key="filter_type")
    filter_category = st.selectbox("Category", ["All", "Food", "Transport", "Entertainment", "Bills", "Others"], key="filter_category")

    # Sorting options
    sort_by = st.selectbox("Sort by", ["Date (Newest to Oldest)", "Date (Oldest to Newest)", "Amount (Low to High)", "Amount (High to Low)"], key="sort_by")

    # Get expenses based on filters
    filter_query = {}
    if filter_type != "All":
        filter_query["type"] = filter_type
    if filter_category != "All":
        filter_query["category"] = filter_category

    expenses_cursor = expenses_collection.find(filter_query)

    # Sorting expenses
    if sort_by == "Date (Newest to Oldest)":
        expenses_cursor = expenses_cursor.sort("date", -1)
    elif sort_by == "Date (Oldest to Newest)":
        expenses_cursor = expenses_cursor.sort("date", 1)
    elif sort_by == "Amount (Low to High)":
        expenses_cursor = expenses_cursor.sort("amount", 1)
    elif sort_by == "Amount (High to Low)":
        expenses_cursor = expenses_cursor.sort("amount", -1)

    expenses_df = pd.DataFrame(expenses_cursor)

    # Display expenses or message
    if expenses_df.empty:
        st.write("Great! No such expenses made.")
    else:
        st.dataframe(expenses_df.drop(columns='_id'))

# Function to edit or delete an expense
def edit_delete_expenses():
    st.title("Edit or Delete Expenses")
    # Define the URL of the Lottie animation
    lottie_url = "https://lottie.host/embed/34491f22-84e8-41a7-a9f5-91f9073b7303/FNjG381TKd.json"
    # Embed the Lottie animation using an HTML iframe with CSS styling
    st.write(f'<iframe src="{lottie_url}" frameborder="0" allowfullscreen="true" scrolling="no" style="width: 300px; height: 300px; margin: 0 auto; display: block;"></iframe>', unsafe_allow_html=True)
    # Fetch all expenses from MongoDB
    expenses_cursor = expenses_collection.find()
    expenses_df = pd.DataFrame(expenses_cursor)

     # Display all expenses
    if not expenses_df.empty:
        selected_expense_note = st.selectbox("Select Expense to Edit/Delete", expenses_df['note'], help="Select an expense to edit or delete")

        if selected_expense_note:
            # Get the selected expense details
            selected_expense_details = expenses_df[expenses_df['note'] == selected_expense_note].iloc[0]

            st.write(f"Expense Note: {selected_expense_details['note']}")
            st.write(f"Category: {selected_expense_details['category']}")
            st.write(f"Type: {selected_expense_details['type']}")
            st.write(f"Amount: {selected_expense_details['amount']}")

            # Provide options to edit or delete the expense
            action = st.radio("Select Action", ["Edit Expense", "Delete Expense"])

            if action == "Edit Expense":
                # Edit expense form
                new_category = st.selectbox("Select New Category", ["Food", "Transport", "Entertainment", "Bills","Others"], index=["Food", "Transport", "Entertainment", "Bills","Others"].index(selected_expense_details['category']))
                new_type = st.selectbox("Select New Type", ["Needs", "Wants", "Unexpected", "Routine"], index=["Needs", "Wants", "Unexpected", "Routine"].index(selected_expense_details['type']))
                new_amount = st.number_input("Enter New Amount", value=selected_expense_details['amount'])

                if st.button("Update Expense"):
                    # Update expense in MongoDB
                    expenses_collection.update_one({"_id": selected_expense_details['_id']}, {"$set": {"category": new_category, "type": new_type, "amount": new_amount}})
                    st.success("Expense updated successfully!")

            elif action == "Delete Expense":
                if st.button("Confirm Delete"):
                    # Delete expense from MongoDB
                    expenses_collection.delete_one({"_id": selected_expense_details['_id']})
                    st.success("Expense deleted successfully!")
    else:
        st.write("No expenses found.")

# Function to plot expenses by day
def plot_expenses_by_day(expenses_df):
    expenses_df['date'] = pd.to_datetime(expenses_df['date']).dt.date
    expenses_by_day = expenses_df.groupby('date')['amount'].sum()
    plt.figure(figsize=(10, 6))
    plt.plot(expenses_by_day.index, expenses_by_day.values, marker='o', linestyle='-')
    plt.title('Expenses by Day')
    plt.xlabel('Date')
    plt.ylabel('Total Expenses (₹)')
    plt.xticks(rotation=45)
    st.pyplot()

# Function to plot expenses by type
def plot_expenses_by_type(expenses_df):
    expenses_by_type = expenses_df.groupby('type')['amount'].sum()
    plt.figure(figsize=(8, 6))
    plt.bar(expenses_by_type.index, expenses_by_type.values, color='skyblue')
    plt.title('Expenses by Type')
    plt.xlabel('Expense Type')
    plt.ylabel('Total Expenses (₹)')
    st.pyplot()

# Function to plot expenses by category
def plot_expenses_by_category(expenses_df):
    expenses_by_category = expenses_df.groupby('category')['amount'].sum()
    plt.figure(figsize=(8, 6))
    plt.bar(expenses_by_category.index, expenses_by_category.values, color='salmon')
    plt.title('Expenses by Category')
    plt.xlabel('Expense Category')
    plt.ylabel('Total Expenses (₹)')
    st.pyplot()

# Function to calculate and display remaining amount
def remaining_amount(salary, expenses_df):
    remaining_amount = round(st.session_state.salary - expenses_df['amount'].sum(), 2)
    total_expenses = expenses_df['amount'].sum()
    remaining = round(salary - total_expenses,2)
    st.write(f"Total Salary: ₹ {salary}")
    st.write(f"Total Expenses: ₹ {total_expenses}")
    st.write(f"Remaining Amount: ₹ {remaining}")

# Function to view insights
def view_insights(expenses_df):
    st.title("Insights")
    # Define the URL of the Lottie animation
    lottie_url = "https://lottie.host/embed/ed7a3ebb-968f-4ec1-8468-28ee554b7914/NjXHPk6p4A.json"
    # Embed the Lottie animation using an HTML iframe with CSS styling
    st.write(f'<iframe src="{lottie_url}" frameborder="0" allowfullscreen="true" scrolling="no" style="width: 300px; height: 300px; margin: 0 auto; display: block;"></iframe>', unsafe_allow_html=True)

    # Enter salary and display remaining amount
    st.subheader("Remaining Amount")
    if 'salary' not in st.session_state:
        st.session_state.salary = st.number_input("Enter Your Salary", min_value=0.0, step=1000.0)
    else:
        st.session_state.salary = st.number_input("Enter Your Salary", min_value=0.0, step=1000.0, value=st.session_state.salary)
    remaining_amount(st.session_state.salary, expenses_df)

    # Plot expenses by day
    st.subheader("Expenses by Day")
    plot_expenses_by_day(expenses_df)

    # Plot expenses by type
    st.subheader("Expenses by Type")
    plot_expenses_by_type(expenses_df)

    # Plot expenses by category
    st.subheader("Expenses by Category")
    plot_expenses_by_category(expenses_df)

# Function for login page
def login_page():
    st.title("Login")
    # Define the URL of the Lottie animation
    lottie_url = "https://lottie.host/embed/4e8b6a4e-e552-48f5-9edf-428a2ade06a8/xAlKEzNnbS.json"
    # Embed the Lottie animation using an HTML iframe with CSS styling
    st.write(f'<iframe src="{lottie_url}" frameborder="0" allowfullscreen="true" scrolling="no" style="width: 200px; height: 200px; margin: 0 auto; display: block;"></iframe>', unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate_user(username, password):
            st.success("Login successful!")
            return True
        else:
            st.error("Invalid username or password")
            return False

# Function for sign-up page
def signup_page():
    st.title("Sign Up")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        if password == confirm_password:
            if add_user(username, password):
                st.success("Account created successfully! Please log in.")
            else:
                st.error("Username already exists. Please choose a different username.")
        else:
            st.error("Passwords do not match. Please try again.")
                                                
delete_filter = {
    "note": {
        "$in": [
            "Groceries",
            "Taxi Ride",
            "Movie Tickets",
            "Electricity",
            "Medical Expenses",
            "Lunch",
            "Bus Fare",
            "Concert Tickets",
            "Internet",
            "Repair Work"
        ]
    }
}

deleted_expenses = expenses_collection.delete_many(delete_filter)
# Main app
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    st.sidebar.title("Navigation")
    expenses_data = list(expenses_collection.find())
    expenses_df = pd.DataFrame(expenses_data)
    selected_page = st.sidebar.radio("Go to", ["Add Expense", "Edit/Delete Expense","View Expenses", "Insights"])
    if selected_page == "Add Expense":
        add_expense()
    elif selected_page == "Edit/Delete Expense":
        edit_delete_expenses()
    elif selected_page == "View Expenses":
        view_expenses()
    elif selected_page == "Insights":
        view_insights(expenses_df)

else:
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Login", "Sign Up"])
    if page == "Login":
        if login_page():
            st.session_state.logged_in = True
            st.sidebar.empty()
    elif page == "Sign Up":
        signup_page()