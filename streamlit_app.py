import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#st.set_page_config(layout="wide")

BACKEND_URL = "https://app-flask-3gn5.onrender.com/"  # Flask API URL after deployment

st.title("Personal Income Expense Tracker")
def show_login_form():
    st.session_state['current_page'] = 'login'

def show_signup_form():
    st.session_state['current_page'] = 'signup'

def show_dashboard():
    st.session_state['current_page'] = 'dashboard'

def signup():
    st.subheader("Signup")
    first_name = st.text_input("First Name", key="signup_firstname")
    last_name = st.text_input("Last Name", key="signup_lastname")
    username = st.text_input("Username", key="signup_username")
    password = st.text_input("Password", type="password", key="signup_password")

    if st.button("Sign Up"):
        # Send a request to the backend API to create a new user
        response = requests.post(f"{BACKEND_URL}/signup", json={
            "FirstName": first_name,
            "LastName": last_name,
            "UserName": username,
            "Password": password
        })
        if response.status_code == 201:
            st.success("You have successfully signed up!")
        else:
            st.error("Sign up failed. Please try a different username.")

def login():
    st.subheader("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Log In"):
        # Send a request to the backend API to authenticate the user
        response = requests.post(f"{BACKEND_URL}/login", json={
            "UserName": username,
            "Password": password
        })
        if response.status_code == 200:
            # If the login is successful, you can store the username in the session
            st.session_state['username'] = username
            st.session_state['logged_in'] = True
            st.success("Logged in successfully!")
            show_dashboard()
        else:
            st.error("Login failed. Please check your username and password.")


# Function to add new income fields
def add_income():
    st.session_state['incomes_temp'].append({'source': '', 'amount': 0})

# Function to add new expense fields
def add_expense():
    st.session_state['expenses_temp'].append({'category': '', 'amount': 0})


def retrieve_financials(username):
    response = requests.get(f"{BACKEND_URL}/get_financials/{username}")
    if response.status_code == 200:
        financials = response.json()
        return financials
    else:
        st.error("Failed to retrieve financials.")
        return None

def retrieve_update_financials(username,year,month):
    response = requests.get(f"{BACKEND_URL}/get_update_financials/{username}/{year}/{month}")
    if response.status_code == 200:
        financials = response.json()
        return financials
    else:
        st.error("Failed to retrieve financials.")
        return None
    
def show_update_form1():

    field=st.selectbox("Select field to update", options=['income','expenses'])
    if field=='income' or field=='expenses':
        source=st.text_input("Source", key='source')
        amount=st.number_input("Amount", key="amount", min_value=0.0, step=0.01)
        #field_path=f"{field}.{source}"
        newvalue={f"{field}.{source}":amount}
        st.write(newvalue)
        if(st.button("Submit")):
            response = requests.post(f"{BACKEND_URL}/set_update_financials/{st.session_state['username']}/{st.session_state['update_year']}/{st.session_state['update_month']}/{field}/{source}/{amount}")
            if response.status_code == 201:
                st.success("Financial record updated successfully!")

def show_update_form():
    year = st.number_input("Year", min_value=2000, max_value=2100, value=2022)
    month = st.selectbox("Month", options=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
    st.session_state["update_year"]=year
    st.session_state["update_month"]=month
    if(st.button("Fetch")):
        user_update_financials = retrieve_update_financials(st.session_state['username'],int(year),month)
        if user_update_financials:
            # Convert the JSON response into a DataFrame for display
            st.write(user_update_financials)
            #if 'comments' in user_update_financials:
            #    comments = user_update_financials['comments']
            #    for comment in comments:
            #        st.write(comment) 
            df_update_financials = pd.DataFrame(user_update_financials)
            st.dataframe(df_update_financials)
    if(st.button("Update")):
        st.session_state['current_page']='update1'
        

def delete_financials(username, year, month):
    response = requests.delete(f"{BACKEND_URL}/delete_financials/{username}/{year}/{month}")
    return response

def show_delete_form():
    st.subheader("Delete Financial Record")

    year = st.number_input("Year of the Record to Delete", min_value=2000, max_value=2100, value=2022)
    month = st.selectbox("Month of the Record to Delete", options=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])

    if st.button("Delete Record"):
        response = delete_financials(st.session_state['username'], year, month)
        if response.status_code == 200:
            st.success("Record deleted successfully!")
        else:
            st.error("Failed to delete the record.")



def show_create_form():
    incomes = {}
    expenses={}
    if 'incomes_temp' not in st.session_state:
        st.session_state['incomes_temp']=[]
    if 'incomes' not in st.session_state:
        st.session_state['incomes']={}
    if 'expenses_temp' not in st.session_state:
        st.session_state['expenses_temp']=[]
    if 'expenses' not in st.session_state:
        st.session_state['expenses']={}
    if 'comments' not in st.session_state:
        st.session_state['comments'] = ''

    for i in range(len(st.session_state['incomes_temp'])):
        with st.container():
            source=st.text_input(f"Income Source {i+1}", key=f"income_source_{i}")
            amount=st.number_input(f"Income Amount {i+1}", key=f"income_amount_{i}", min_value=0.0, step=0.01)
            if(source):
                st.session_state['incomes'][source]=amount


    # Button to add income fields

    st.button("Add Income Item", on_click=add_income)

    # Dynamic expense fields
    for i in range(len(st.session_state['expenses_temp'])):
        with st.container():
            source=st.text_input(f"Expense Category {i+1}", key=f"expense_category_{i}")
            amount=st.number_input(f"Expense Amount {i+1}", key=f"expense_amount_{i}", min_value=0.0, step=0.01)
            if(source):
                st.session_state['expenses'][source]=amount

    # Button to add expense fields
    st.button("Add Expense Item", on_click=add_expense)# Year and month selection
    st.session_state['year'] = st.number_input("Year", min_value=2000, max_value=2100, value=2022, step=1)
    st.session_state['month'] = st.selectbox("Month", options=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])

    # Comments text area
    st.text_area("Comments", key='comments')

    
    # Submit button for the form
    if st.button("Submit financial record"):
        financial_record = {
        'username': st.session_state['username'],
        'year': st.session_state['year'],
        'month': st.session_state['month'],
        'income': st.session_state['incomes'],
        'expenses': st.session_state['expenses'],
        'comments': st.session_state['comments'].split('\n')  # Split comments into a list
    }
    
        # POST the financial record to the Flask API
        response = requests.post(f"{BACKEND_URL}/create_financials", json=financial_record)
        if response.status_code == 201:
            st.success("Financial record created successfully!")
            # Clear the fields after successful submission
            st.session_state['incomes_temp'] = []
            st.session_state['expenses_temp'] = []
            st.session_state['incomes']={}
            st.session_state['expenses']={}

        else:
            st.error("A Financial record is already available for the given month and year")

def visualise():
    st.write("Annual Trend of Income and Expense")
    user_financials = retrieve_financials(st.session_state['username'])
    if user_financials:
    # Convert the JSON response into a DataFrame for display
        df = pd.DataFrame(user_financials)

        # Extract labels and values for the plot
        df['year'] = df['year'].astype(str)
        df['income_total'] = df['income'].apply(lambda x: sum(x.values()) if x else 0)
        df['expense_total'] = df['expenses'].apply(lambda x: sum(x.values()) if x else 0)

        # Using Seaborn lineplot
        plt.figure(figsize=(12, 6))
        sns.lineplot(x='year', y='income_total', data=df, label='Income', marker='o')
        sns.lineplot(x='year', y='expense_total', data=df, label='Expenses', marker='o')

        plt.title('Income and Expenses Over Years')
        plt.xlabel('Year')
        plt.ylabel('Amount (in $)')
        plt.xticks(rotation=45, ha='right')  # Rotate and align x-axis labels for better readability
        plt.legend()
        plt.tight_layout()
        st.set_option('deprecation.showPyplotGlobalUse', False)

        # Show the plot
        st.pyplot()  # Assuming st is Streamlit's st object

    st.write("Select the Year and Month for breakdown of the income and Expense:")

    year = st.number_input("Year", min_value=2000, max_value=2100, value=2022)
    month = st.selectbox("Month", options=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
    st.session_state["update_year"]=year
    st.session_state["update_month"]=month
    if(st.button("Fetch")):
        user_update_financials = retrieve_update_financials(st.session_state['username'],int(year),month)
        if user_update_financials:
            # Convert the JSON response into a DataFrame for display
            # st.write(user_update_financials)
            # df_update_financials = pd.DataFrame(user_update_financials)
            # st.dataframe(df_update_financials)
            user_data = list(user_update_financials)
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
            st.error("No financial record available for the given Month of the year")
            
def fetch_record():
    year = st.number_input("Year", min_value=2000, max_value=2100, value=2022)
    month = st.selectbox("Month", options=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
    st.session_state["update_year"]=year
    st.session_state["update_month"]=month
    if(st.button("Fetch")):
        user_update_financials = retrieve_update_financials(st.session_state['username'],int(year),month)
        if user_update_financials:
            # Convert the JSON response into a DataFrame for display
            st.write(user_update_financials)
            #if 'comments' in user_update_financials:
            #    comments = user_update_financials['comments']
            #    for comment in comments:
            #        st.write(comment) 
            df_update_financials = pd.DataFrame(user_update_financials)
            st.dataframe(df_update_financials)
def dashboard():
    
    # Here you can add the CRUD operations
    # For example, adding a new financial record:
    
    st.sidebar.title("Navigation")
    if st.session_state['current_page'] == 'dashboard':
        st.write(f"Welcome {st.session_state['username']}!")
        if st.sidebar.button("Create a new record"):
            st.session_state['current_page'] = 'create'
        if st.sidebar.button('Update existing record'):
            st.session_state['current_page'] = 'update'

        if(st.sidebar.button("Delete record")):
            st.session_state['current_page'] = 'delete'
        if st.sidebar.button("Fetch a record",key='retrieve'):
            st.session_state['current_page']='fetch'

    user_financials = retrieve_financials(st.session_state['username'])
    if user_financials:
        # Convert the JSON response into a DataFrame for display
        df_financials = pd.DataFrame(user_financials)
        df_financials=df_financials[['username','year','month', 'income','expenses', 'comments']]
        st.dataframe(df_financials)
        
    if st.sidebar.button("Visualize financials", key="visualize"):
        st.session_state['current_page'] = 'visualize'
    



if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'login'

if st.session_state['current_page'] == 'login':
    login()
    st.write("New user?")
    st.button("Go to Sign Up", on_click=show_signup_form)

elif st.session_state['current_page'] == 'signup':
    signup()
    st.button("Back to Login", on_click=show_login_form)

elif st.session_state['current_page'] == 'dashboard':
    #show_sidebar()
    dashboard()
    # Optionally, add a logout button
    col1, col2 = st.columns([1, 0.2])
    with col2:
        if st.button('Logout'):
            st.session_state['current_page'] = 'login'
            st.session_state.pop('username', None)  # Remove the username from the session

elif st.session_state['current_page']=='create':
    show_create_form()

    if st.button("Back"):
        st.session_state['current_page'] = 'dashboard'

elif st.session_state['current_page']=='update':
    show_update_form()

    if st.button("Dashboard"):
        st.session_state['current_page'] = 'dashboard'
elif st.session_state['current_page']=='update1':
    show_update_form1()

    if st.button("Back"):
        st.session_state['current_page'] = 'update'

elif st.session_state['current_page'] == 'delete':
    show_delete_form()
    if st.button("Dashboard"):
        st.session_state['current_page'] = 'dashboard'

elif st.session_state['current_page'] == 'visualize':
    visualise()
    if st.button("Dashboard"):
        st.session_state['current_page'] = 'dashboard'

elif st.session_state['current_page']=='fetch':
    fetch_record()
    if(st.button('Dashboard')):
        st.session_state['current_page']='dashboard'
