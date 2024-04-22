# FinFlow: Personal Finance Tracker with MongoDB and Streamlit
FinFlow is a personal finance tracker that leverages MongoDB as the backend database and Streamlit for the user interface. It streamlines finance tracking by enabling income and expense input, date-range management, budget planning, and expense trend visualizations.

Table of Contents
Project Overview
MongoDB Integration
Finance Tracking Features
Streamlit Deployment

## Project Overview
FinFlow is designed to be a comprehensive personal finance tracker that simplifies the process of managing income and expenses. By combining the power of MongoDB for the backend and Streamlit for the user interface, FinFlow offers an efficient and user-friendly experience.

![IncomeExpenseTracker](https://github.com/kashmira92/Perosnal-Income-and-Expense-Tracker-Application-using-MongoDB/assets/48323327/0545f963-6de8-4fc7-91a7-6019548599db)

## MongoDB Integration
MongoDB Backend: Integrated MongoDB as the backend database, providing account creation and authentication scripts.
Improved Retrieval Speed: MongoDB integration led to a 60% improvement in retrieval speed.

## Finance Tracking Features
User Input: Enabled users to input income and expenses for accurate tracking.
Date-Range Management: Provided date-range management for users to analyze financial data over different periods.

## Visualizations: Offered budget planning and expense trends visualizations to help users understand their financial habits.
Streamlit Deployment
Streamlit UX: Deployed the personal finance tracker with Streamlit, offering a user-friendly experience.
Back-End Operations: Utilized Python and MongoDB for efficient back-end operations.

* "personal_income_expense_tracker.users_financials.csv" and "personal_income_expense_tracker.users_information.csv" are the two collections that were deployed on to mongoDB. "personal_income_expense_tracker.users_financials.csv" stores financial infromation of all the users in a single document for each month. "personal_income_expense_tracker.users_information.csv" stores user specific infromation once the user signup to the application.

* app.py contains the code of Flask application.

* streamlit_app.py contains the code of Front-end web application.

* requirements.txt contains the packages with versions required.
