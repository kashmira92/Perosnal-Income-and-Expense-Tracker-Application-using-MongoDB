import plotly.graph_objects as go  # pip install plotly
import streamlit as st 
import calendar  # Core Python Module
from datetime import datetime  # Core Python Module
# import sys
# sys.path.insert(1, "C:/past/your/coppied/path/here/streamlit_option_menu")
from streamlit_option_menu import option_menu
 # pip install streamlit
# from streamlit_option_menu import option_menu  # pip install streamlit-option-menu

import database as db  # local import

# -------------- SETTINGS --------------
incomes = ["Petty cash", "Allowance", "Other",  "Part-Time", "Salary", "Rental Income"]
expenses = ["Utilities", "Apparel", "Social Life", "Household", "Food", "Self-development", "Transportation", "Gift"]
currency = "USD"
page_title = "Personal Income - Expense Tracker"
page_icon = ":money_with_wings:"  # emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
layout = "centered"

# --------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)

# --- DROP DOWN VALUES FOR SELECTING THE PERIOD ---
years = [datetime.today().year, datetime.today().year-2, datetime.today().year -1, datetime.today().year + 1]
months = list(calendar.month_name[1:])
# usernames = 
# --- DATABASE INTERFACE ---
def get_all_periods():
    items = db.fetch_all_periods()
    periods = [item["key"] for item in items]
    return periods


# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["Data Entry", "Data Visualization", "Update Expense", "Delete Expense"],
    icons=["pencil-fill", "bar-chart-fill","calculator-fill", "book-fill"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)

# --- INPUT & SAVE PERIODS ---
if selected == "Data Entry":
    st.header(f"Data Entry in {currency}")
    with st.form("entry_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        col1.selectbox("Select Month:", months, key="month")
        col2.selectbox("Select Year:", years, key="year")
        col3.text_input("Enter Username:", "", key="username")
        # col3.text_area("", placeholder="Enter a username here ...", key="username")
        "---"
        with st.expander("Income"):
            for income in incomes:
                st.number_input(f"{income}:", min_value=0, format="%i", step=10, key=income)
        with st.expander("Expenses"):
            for expense in expenses:
                st.number_input(f"{expense}:", min_value=0, format="%i", step=10, key=expense)
        with st.expander("Comment"):
            comment = st.text_area("", placeholder="Enter a comment here ...")
            comments = [comment]  # Convert the comment to a list

        "---"
        submitted = st.form_submit_button("Save Data")
        if submitted:
            period = str(st.session_state["year"]) + "_" + str(st.session_state["month"]) + "_" + str(st.session_state["username"])
            incomes = {income: st.session_state[income] for income in incomes}
            expenses = {expense: st.session_state[expense] for expense in expenses}
            db.insert_period(period, incomes, expenses, comments)  # Pass the list of comments
            st.success("Data saved!")


# --- PLOT PERIODS ---
if selected == "Data Visualization":
    st.header("Data Visualization")
    with st.form("saved_periods"):
        period = st.selectbox("Select Period:", get_all_periods())
        submitted = st.form_submit_button("Plot Period")
        if submitted:
            # Get data from database
            period_data = db.get_period(period)
            comments = period_data.get("comments")
            expenses = period_data.get("expenses")
            incomes = period_data.get("income")
               # Create metrics
            total_income = sum(incomes.values())
            total_expense = sum(expenses.values())
            remaining_budget = total_income - total_expense
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Income", f"{total_income} {currency}")
            col2.metric("Total Expense", f"{total_expense} {currency}")
            col3.metric("Remaining Budget", f"{remaining_budget} {currency}")
            st.text(f"Comments: {comments}")
    
            # Create sankey chart
            label = list(incomes.keys()) + ["Total Income"] + list(expenses.keys())
            source = list(range(len(incomes))) + [len(incomes)] * len(expenses)
            target = [len(incomes)] * len(incomes) + [label.index(expense) for expense in expenses.keys()]
            value = list(incomes.values()) + list(expenses.values())
    
            # Data to dict, dict to sankey
            link = dict(source=source, target=target, value=value)
            node = dict(label=label, pad=20, thickness=30, color="#E694FF")
            data = go.Sankey(link=link, node=node)
    
            # Plot it!
            fig = go.Figure(data)
            fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))
            st.plotly_chart(fig, use_container_width=True)
    
    # Add update form 
if selected == "Update Expense":
    st.header("Update Income and Expenses")
    
    # Create a form to select the period and update income and expenses
    with st.form("update_income_expenses"):
        # Select period to update
        period = st.selectbox("Select Period:", get_all_periods())
        
        # Get existing data for the selected period
        period_data = db.get_period(period)
        existing_incomes = period_data.get("income", {})
        existing_expenses = period_data.get("expenses", {})

        # Display existing income and expenses for reference
        st.write("Existing Income:")
        st.write(existing_incomes)
        st.write("Existing Expenses:")
        st.write(existing_expenses)

        # Allow the user to update income
        new_incomes = {}
        for category in existing_incomes:
            new_amount = st.number_input(f"Enter new income for {category}:", value=existing_incomes[category])
            new_incomes[category] = new_amount

        # Allow the user to update expenses
        new_expenses = {}
        for category in existing_expenses:
            new_amount = st.number_input(f"Enter new expense for {category}:", value=existing_expenses[category])
            new_expenses[category] = new_amount

        # Submit button
        submitted = st.form_submit_button("Update Income and Expenses")

        if submitted:
            # Update income and expenses in the database
            db.update_period(period, new_incomes, new_expenses, [])

            # Display updated income and expenses
            updated_period_data = db.get_period(period)
            updated_incomes = updated_period_data.get("income", {})
            updated_expenses = updated_period_data.get("expenses", {})
            st.write("Updated Income:")
            st.write(updated_incomes)
            st.write("Updated Expenses:")
            st.write(updated_expenses)
