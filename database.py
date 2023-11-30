import streamlit as st  # pip install streamlit
# from deta import Deta  # pip install deta


from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi

MONGO_URI = "mongodb+srv://kgolatka:root@cluster0.vzbsfma.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "personal_income_expense_tracker"
COLLECTION_NAME = "users_financials"
# Create a new client and connect to the server
client = MongoClient(MONGO_URI)

db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

def insert_period(period, incomes, expenses, comment):
    data = {
        "key": period,
        "incomes": incomes,
        "expenses": expenses,
        "comment": comment
    }
    collection.insert_one(data)

# def get_all_usernames():
    
    
def update_period(period, incomes, expenses, comment):
  collection.update_one(
    {"key": period},
    {"$set": {
      "incomes": incomes,
      "expenses": expenses, 
      "comment": comment  
    }}
  )

def fetch_all_periods():
    items = collection.find()
    return items

def get_period(period):
    return collection.find_one({"key": period})
# Load the environment variables
# DETA_KEY = "b0jAddiWaMf_3scH2wPKs4xfUXnPcDyfL7PPiTvznS5F"

# Initialize with a project key
# deta = Deta(DETA_KEY)

# This is how to create/connect a database
# db = deta.Base("monthly_expense")


# def insert_period(period, incomes, expenses, comment):
#     """Returns the report on a successful creation, otherwise raises an error"""
#     print("Inserting data:")
#     print("Period:", period)
#     print("Incomes:", incomes)
#     print("Expenses:", expenses)
#     print("Comment:", comment)
#     return db.put({"key": period, "incomes": incomes, "expenses": expenses, "comment": comment})

# def fetch_all_periods():
#     """Returns a dict of all periods"""
#     res = db.fetch()
#     return res.items


# def get_period(period):
#     """If not found, the function will return None"""
#     return db.get(period)
