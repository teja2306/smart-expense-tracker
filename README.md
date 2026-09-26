# SmartSpend – Personal Expense Manager

SmartSpend is a Python-based desktop application for recording, managing, and analyzing personal expenses. It provides a simple graphical interface to track spending, manage a budget, search transactions, and view category-wise expense information.

## Features

* Add and record expenses
* Store expense data using SQLite
* View all saved expenses
* Search expenses by category, description, or date
* Delete selected expenses
* Set and update a budget
* Display total spending
* Display highest expense
* View recent transactions
* Analyze spending by category
* Display category-wise spending percentages
* Show visual spending distribution
* Display basic rule-based smart spending insights
* Validate expense and budget inputs

## Technologies Used

* Python
* Tkinter
* SQLite
* ttk
* SQL

## Database

SmartSpend uses SQLite for local data storage.

The database contains two tables:

### Expenses Table

Stores:

* Expense ID
* Amount
* Category
* Description
* Date

### Budget Table

Stores:

* Budget amount

The database and required tables are created automatically when the application is run.

## CRUD Operations

* **Create:** Add new expenses and save a budget
* **Read:** View and search expenses
* **Update:** Update the saved budget
* **Delete:** Delete selected expenses

## Project Structure

```text
SmartSpend/
│
├── expense_tracker.py
├── expenses.db
└── README.md
```

## How to Run

### 1. Install Python

Make sure Python is installed on your system.

### 2. Download or Clone the Project

Open the project folder in VS Code or a terminal.

### 3. Run the Application

```bash
python expense_tracker.py
```

The SmartSpend desktop application will open.

## Application Sections

### Dashboard

Displays:

* Total spending
* Budget
* Remaining amount
* Highest expense
* Recent transactions
* Smart spending insights

### Expenses

Allows users to:

* View expenses
* Search transactions
* Delete selected expenses

### Analytics

Provides:

* Total spending
* Category-wise expense breakdown
* Spending percentage
* Visual spending distribution

### Budget

Allows users to:

* Set a budget
* Update the budget
* Monitor spending against the budget
* View remaining or exceeded amount

### Add Expense

Users can enter:

* Amount
* Category
* Description

The current date is automatically stored with each expense.

## Smart Insights

The application provides basic **rule-based insights** based on spending and budget information.

Examples include:

* Highest spending category
* Budget not set
* Budget exceeded
* More than 80% of the budget used
* Spending within the budget

> Note: The current version uses rule-based logic and does not use Machine Learning or Artificial Intelligence.

## Purpose

This project was developed to practice:

* Python programming
* GUI development using Tkinter
* SQLite database connectivity
* SQL queries
* CRUD operations
* Input validation
* Basic data analysis

## Future Improvements

* Add expense editing functionality
* Implement accurate monthly and yearly expense tracking
* Add CSV/Excel export
* Add advanced charts and reports
* Add user login and authentication
* Add spending prediction using Machine Learning
* Add recurring expense tracking

## Author

Developed as a Python project for learning and practical application development.
