# Expense_tracker
An Expense Tracker application that allows users to manage, review, and analyze their expenses through an interactive web interface, supported by a robust backend and reliable data management.


## Features

- The expense tracking feature allows users to efficiently record and manage their financial activities by storing detailed information for each expense.
- The application offers full CRUD (Create, Read, Update, Delete) operations, enabling efficient and seamless expense management.
- The application uses SQLite as the database for persistent data storage, with SQLAlchemy ORM handling database interactions.
- The frontend interface built with Streamlit provides a clean, user-friendly and responsive UI.
- To ensure reliability and prevent incorrect data entry, the project uses robust data validation mechanisms at multiple layers.
- The FastAPI backend manages the main business logic and handles API operations, ensuring smooth and secure data processing.

## Setup

Clone this repository:
```bash
git clone https://github.com/krishnarhajil/Expense_tracker
```

Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

If an access denied error is thrown while trying to acces the file Windows, execute in cmd or
```bash
cmd /c "venv\Scripts\activate.bat"
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the FastAPI backend:
```bash
python uvicorn main:app --reload
```
The API will be available at http://localhost:8000

Start the Streamlit frontend:
```bash
python -m streamlit run app.py
```
The frontend will be available at http://localhost:8501


## Testing with Postman

You can test the API endpoints using Postman:

Create a new expense:
```
POST http://localhost:8000/expenses/
Content-Type: application/json

{
    "description": "Groceries",
    "amount": 50.25,
    "category": "Food",
    "date": "2024-03-23T00:00:00"
}
```

Get all expenses:
```
GET http://localhost:8000/expenses/
```

Get a specific expense:
```
GET http://localhost:8000/expenses/1
```

Update an expense:
```
PUT http://localhost:8000/expenses/1
Content-Type: application/json

{
    "description": "Updated Groceries",
    "amount": 55.75,
    "category": "Food",
    "date": "2024-03-23T00:00:00"
}
```

Delete an expense:
```
DELETE http://localhost:8000/expenses/1
``` 
