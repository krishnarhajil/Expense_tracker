import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import json
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API URL
API_URL = "http://localhost:8000"

def get_total_expenses(expenses):
    return sum(expense['amount'] for expense in expenses)

def get_expenses_by_category(expenses):
    df = pd.DataFrame(expenses)
    return df.groupby('category')['amount'].sum().reset_index()

def main():
    # Sidebar
    with st.sidebar:
        st.title("💰")
        st.markdown("---")
        page = st.selectbox(
            "",
            ["Add Expense", "View Expenses", "Update Expense", "Delete Expense"],
            index=0
        )
        st.markdown("---")

    if page == "Add Expense":
        st.title("➕ Add New Expense")
        
        # Create form with better styling
        with st.form("add_expense_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                description = st.text_input("Description", placeholder="Enter expense description")
                amount = st.number_input("Amount", min_value=0.0, step=0.01, placeholder="Enter amount")
            
            with col2:
                category = st.text_input("Category", placeholder="Enter category")
                date = st.date_input("Date")
            
            submitted = st.form_submit_button("Add Expense")
            
            if submitted:
                if not description or not category:
                    st.error("Please fill in all required fields")
                    return
                
                datetime_obj = datetime.combine(date, datetime.min.time())
                
                expense_data = {
                    "description": description,
                    "amount": float(amount),
                    "category": category,
                    "date": datetime_obj.isoformat()
                }
                
                try:
                    response = requests.post(f"{API_URL}/expenses/", json=expense_data)
                    if response.status_code == 200:
                        st.success("✅ Expense added successfully!")
                        st.experimental_rerun()
                    else:
                        error_detail = response.json().get("detail", "Unknown error")
                        st.error(f"Error adding expense: {error_detail}")
                except requests.exceptions.ConnectionError:
                    st.error("Could not connect to the server. Make sure the backend is running.")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    elif page == "View Expenses":
        st.title("📋 View All Expenses")
        
        try:
            response = requests.get(f"{API_URL}/expenses/")
            if response.status_code == 200:
                expenses = response.json()
                if not expenses:
                    st.info("No expenses found. Add some expenses to get started!")
                else:
                    df = pd.DataFrame(expenses)
                    df['date'] = pd.to_datetime(df['date']).dt.date
                    df['created_at'] = pd.to_datetime(df['created_at'])
                    
                    # Add filters
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        category_filter = st.multiselect(
                            "Filter by Category",
                            options=df['category'].unique(),
                            default=df['category'].unique()
                        )
                    
                    with col2:
                        date_range = st.date_input(
                            "Date Range",
                            value=(df['date'].min(), df['date'].max()),
                            min_value=df['date'].min(),
                            max_value=df['date'].max()
                        )
                    
                    with col3:
                        amount_range = st.slider(
                            "Amount Range",
                            min_value=float(df['amount'].min()),
                            max_value=float(df['amount'].max()),
                            value=(float(df['amount'].min()), float(df['amount'].max()))
                        )
                    
                    # Apply filters
                    filtered_df = df[
                        (df['category'].isin(category_filter)) &
                        (df['date'].between(date_range[0], date_range[1])) &
                        (df['amount'].between(amount_range[0], amount_range[1]))
                    ]
                    
                    # Display filtered data
                    st.dataframe(filtered_df, use_container_width=True)
                    
                    # Summary statistics
                    st.subheader("Summary Statistics")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Total Filtered Expenses", f"${filtered_df['amount'].sum():,.2f}")
                    
                    with col2:
                        st.metric("Average Expense", f"${filtered_df['amount'].mean():,.2f}")
                    
                    with col3:
                        st.metric("Number of Expenses", len(filtered_df))
            else:
                st.error("Error fetching expenses")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the server. Make sure the backend is running.")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    elif page == "Update Expense":
        st.title("✏️ Update Expense")
        
        try:
            response = requests.get(f"{API_URL}/expenses/")
            if response.status_code == 200:
                expenses = response.json()
                if not expenses:
                    st.info("No expenses found to update.")
                else:
                    expense_dict = {f"{exp['id']} - {exp['description']}": exp for exp in expenses}
                    selected_expense = st.selectbox("Select expense to update", list(expense_dict.keys()))
                    
                    if selected_expense:
                        expense_id = int(selected_expense.split(" - ")[0])
                        expense = expense_dict[selected_expense]
                        
                        with st.form("update_expense_form"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                description = st.text_input("Description", value=expense['description'])
                                amount = st.number_input("Amount", min_value=0.0, step=0.01, value=expense['amount'])
                            
                            with col2:
                                category = st.text_input("Category", value=expense['category'])
                                date = st.date_input("Date", value=datetime.strptime(expense['date'], "%Y-%m-%dT%H:%M:%S").date())
                            
                            submitted = st.form_submit_button("Update Expense")
                            
                            if submitted:
                                datetime_obj = datetime.combine(date, datetime.min.time())
                                
                                expense_data = {
                                    "description": description,
                                    "amount": float(amount),
                                    "category": category,
                                    "date": datetime_obj.isoformat()
                                }
                                
                                response = requests.put(f"{API_URL}/expenses/{expense_id}", json=expense_data)
                                if response.status_code == 200:
                                    st.success("✅ Expense updated successfully!")
                                    st.experimental_rerun()
                                else:
                                    error_detail = response.json().get("detail", "Unknown error")
                                    st.error(f"Error updating expense: {error_detail}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the server. Make sure the backend is running.")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    elif page == "Delete Expense":
        st.title("🗑️ Delete Expense")
        
        try:
            response = requests.get(f"{API_URL}/expenses/")
            if response.status_code == 200:
                expenses = response.json()
                if not expenses:
                    st.info("No expenses found to delete.")
                else:
                    expense_dict = {f"{exp['id']} - {exp['description']}": exp for exp in expenses}
                    selected_expense = st.selectbox("Select expense to delete", list(expense_dict.keys()))
                    
                    if selected_expense:
                        expense_id = int(selected_expense.split(" - ")[0])
                        expense = expense_dict[selected_expense]
                        
                        # Show expense details before deletion
                        st.subheader("Expense Details")
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Description", expense['description'])
                        
                        with col2:
                            st.metric("Amount", f"${expense['amount']:,.2f}")
                        
                        with col3:
                            st.metric("Category", expense['category'])
                        
                        with col4:
                            st.metric("Date", datetime.strptime(expense['date'], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d"))
                        
                        if st.button("Delete Expense", type="primary"):
                            response = requests.delete(f"{API_URL}/expenses/{expense_id}")
                            if response.status_code == 200:
                                st.success("✅ Expense deleted successfully!")
                                st.experimental_rerun()
                            else:
                                error_detail = response.json().get("detail", "Unknown error")
                                st.error(f"Error deleting expense: {error_detail}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the server. Make sure the backend is running.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 