#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import matplotlib.pyplot as plt
from pymongo.mongo_client import MongoClient


# MongoDB configuration
MONGO_URI = "mongodb+srv://kgolatka:root@cluster0.vzbsfma.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "personal_income_expense_tracker"
COLLECTION_NAME = "users_financials"
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

incomes = ["Salary","Pocket Money","Other Income"]
expenses = ["Rent","Utilities","Groceries","Trip","Transport","Other Expenses"]

# Streamlit UI
st.title("Personal Income Expense Tracker")

# CRUD functions
def insert_financial(username,year,month, income, expenses, comments):
    
    data = {
        "username": username,
        "year": year,
        "month": month,
        "income": income,
        "expenses": expenses,
        "comments": comments
    }
    collection.insert_one(data)

def update_financial(username,year,month, income, expenses, comments):

    print("entered up")
    collection.update_one(
        {'$set': {'username':username,'year':year, 'month':month,'income': income, 'expenses': expenses, 'comments': comments}})

def fetch_all_financial():
    records =list(collection.find())
    if records:
        for record in records:
           
            st.subheader(f"Username: {record['username']}")
            st.write(f"Year: {record['year']}")
            st.write(f"Month: {record['month']}")

            st.header("Income:")
            for income_type, amount in record['income'].items():
                st.write(f"{income_type}: {amount}")

            st.header("Expenses:")
            for expense_type, amount in record['expenses'].items():
                st.write(f"{expense_type}: {amount}")

            st.header("Comments:")
            for i, comment in enumerate(record['comments']):
                st.write(f"Comment {i+1}: {comment}")

            st.markdown("---") 
    else:
        st.warning("No records found.")

def delete_record(username):
    # Construct the query to find the document to delete
    query = {"username": username}

    # Perform the delete operation
    result = collection.delete_one(query)

    # Check if the delete was successful
    if result.deleted_count > 0:
        print(f"Record deleted successfully for username: {username}")
    else:
        print(f"No matching document found for delete: {username}")

# def get_finance(username):
#     return list(collection.find({"username": username}))

def get_finance(username, year=None, month=None):
    query = {"username": username}
    if year:
        query["year"] = year
    if month:
        query["month"] = month
    return list(collection.find(query))

# Streamlit CRUD operations
operation = st.sidebar.selectbox("Select Operation", ["Insert", "Update", "Delete", "Fetch All", "Get Finance for the given user"])

if operation == "Insert":
    st.header("Insert Income and Expense")
    username = st.text_input("Enter Name of the User")
    year = st.text_input("Enter year")
    month = st.selectbox("Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])

    st.subheader("Income:")
    income_types = ["Object", "Other", "Rental Income", "Allowance", "Part-time"]
    income_data = {}
    for income_type in income_types:
        amount = st.number_input(f"{income_type} Income", key=f"{income_type}_income", value=0.0)
        income_data[income_type] = amount
    st.subheader("Expenses:")
    expense_types = ["Rent", "Groceries", "Car", "Apparel", "Social Life", "Gift", "Beauty"]
    expense_data = {}
    for expense_type in expense_types:
        amount = st.number_input(f"{expense_type} Expense", key=f"{expense_type}_expense", value=0.0)
        expense_data[expense_type] = amount

    st.subheader("Comments:")
    comments = []
    for i in range(10):
        comment = st.text_area(f"Comment {i+1}", key=f"comment_{i+1}")
        comments.append(comment)
        
    if st.button("Insert"):
        insert_financial(username,year,month, income_data, expense_data, comments)
        st.success("Data Inserted Successfully!")


elif operation == "Update":
    st.header("Update Period")

    search_username = st.text_input("Enter Username to Search")

    if st.button("Search"):
        existing_data = get_finance(search_username)

        if existing_data:
            # Display existing data
            st.write(f"Username: {search_username}")

            # Input for updating data
            with st.form(key='update_form'):
                username = st.text_input("Enter Name of the User", value=existing_data.get("username", ""))
                st.write("Income:")
                income_data = {}
                for income_type in incomes:
                    amount = st.number_input(f"{income_type} Income", key=f"{income_type}_income", value=existing_data.get("income", {}).get(income_type, 0.0))
                    income_data[income_type] = amount

                st.write("Expenses:")
                expense_types = ["Rent", "Groceries", "Car", "Apparel", "Social Life", "Gift", "Beauty"]
                expense_data = {}
                for expense_type in expenses:
                    amount = st.number_input(f"{expense_type} Expense", key=f"{expense_type}_expense", value=existing_data.get("expenses", {}).get(expense_type, 0.0))
                    expense_data[expense_type] = amount

                st.write("Comments:")
                comments = []
                for i in range(10):
                    comment = st.text_area(f"Comment {i+1}", key=f"comment_{i+1}", value=existing_data.get("comments", [])[i] if i < len(existing_data.get("comments", [])) else "")
                    comments.append(comment)

                # Allow user to update data
                if st.form_submit_button("Update1"):
                    print("Button clicked")
                    year = existing_data.get("year", 2025)  # You might want to get the actual year from the existing data
                    month = existing_data.get("month", "April")  # You might want to get the actual month from the existing data
                    update_financial(username, year, month, income_data, expense_data, comments)
                    st.success("Data updated successfully!")
        else:
            st.warning(f"No data found for username: {search_username}")

elif operation == "Fetch All":
    st.header("Fetch All Financial")
    financials = fetch_all_financial()
    for finance in financials:
        st.write(finance)

elif operation == "Delete":
    search_username = st.text_input("Enter Username to Search")
    if st.button("Delete Record"):
        print("Delete button clicked")
        delete_record(search_username)
        st.success("Record deleted successfully!")
        
    
elif operation == "Get Finance for the given user":
    st.header("Get Specific Finance")
    username = st.text_input("Enter username to Retrieve")
    selected_year = st.selectbox("Select Year", [""] + sorted(set(record["year"] for record in get_finance(username))))
    selected_month = st.selectbox("Select Month", [""] + sorted(set(record["month"] for record in get_finance(username, year=selected_year))))

    if st.button("Fetch Data"):
        if not selected_year or not selected_month:
            st.warning("Please select both year and month.")
        else:
            user_data = get_finance(username, year=selected_year, month=selected_month)
            if user_data:
                st.write(user_data)
                
# Plot a bar graph for income and expenses
            incomes = user_data[0].get("income", {})
            expenses = user_data[0].get("expenses", {})

            plt.figure(figsize=(10, 6))
            plt.bar(['Income'], [sum(incomes.values())], label='Income', color='green')
            plt.bar(['Expense'], [sum(expenses.values())], label='Expense', color='red')
            plt.xlabel('Categories')
            plt.ylabel('Amount')
            plt.title('Income and Expense Overview')
            plt.legend()
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot()
                
                # Colors for Income Sources Overview
            income_colors = ['#FFD700', '#FF6347', '#87CEFA', '#90EE90', '#FFB6C1']

                # Create subplots for Income Sources and Expense Categories
            fig, axes = plt.subplots(1, 2, figsize=(18, 10))

                # Plot pie chart for Income Sources Overview
            axes[0].pie(incomes.values(), labels=incomes.keys(), autopct='%1.1f%%', startangle=140, colors=income_colors)
            axes[0].set_title('Income Sources Distribution', fontsize=16)

                # Colors for Expense Categories Overview
            expense_colors = ['#FFD700', '#FF6347', '#87CEFA', '#90EE90', '#FFB6C1', '#FFFFE0', '#E0FFFF', '#D3D3D3']

                # Plot pie chart for Expense Categories Overview
            axes[1].pie(expenses.values(), labels=expenses.keys(), autopct='%1.1f%%', startangle=140, colors=expense_colors)
            axes[1].set_title('Expense Categories Distribution', fontsize=16)

                # Adjust layout
            plt.tight_layout()
                # Display the subplots
            st.pyplot()
            
        
    else:
        st.warning("Username not found")

# Close MongoDB connection (optional, Streamlit will handle it automatically)
# client.close()

