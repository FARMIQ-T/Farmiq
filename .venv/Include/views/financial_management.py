import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def render():
    """Render the Financial Management Dashboard."""
    
    st.subheader("Financial Management")
    
    # Create tabs for different sections
    tabs = st.tabs(["Overview", "Income & Expenses", "Loans & Credit", "Financial Planning"])
    
    with tabs[0]:
        st.subheader("Financial Overview")
        
        # Key Financial Metrics
        col1, col2, col3 = st.columns(3)
        
        # Sample data - replace with database data
        with col1:
            st.metric("Total Revenue (YTD)", "KES 850,000", "+15%")
            st.metric("Cash on Hand", "KES 125,000", "-5%")
        with col2:
            st.metric("Total Expenses (YTD)", "KES 520,000", "+8%")
            st.metric("Outstanding Loans", "KES 200,000", "-10%")
        with col3:
            st.metric("Net Profit (YTD)", "KES 330,000", "+25%")
            st.metric("Credit Score", "750", "+50")
        
        # Financial Health Indicators
        st.write("#### Financial Health Indicators")
        
        # Sample financial ratios - replace with calculated values
        financial_health = pd.DataFrame({
            'Metric': ['Debt-to-Income Ratio', 'Current Ratio', 'Profit Margin', 'Return on Investment'],
            'Value': [0.35, 1.8, 0.28, 0.22],
            'Status': ['Good', 'Excellent', 'Good', 'Fair']
        })
        
        for _, metric in financial_health.iterrows():
            status_color = {'Excellent': 'green', 'Good': 'blue', 'Fair': 'orange', 'Poor': 'red'}[metric['Status']]
            st.markdown(
                f"<div style='padding:10px;border-left:5px solid {status_color};margin:10px 0;'>"
                f"<strong>{metric['Metric']}</strong><br>"
                f"Value: {metric['Value']:.2f}<br>"
                f"Status: {metric['Status']}"
                "</div>",
                unsafe_allow_html=True
            )
        
    with tabs[1]:
        st.subheader("Income & Expenses")
        
        # Transaction Entry
        with st.expander("Add New Transaction"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                transaction_type = st.selectbox("Transaction Type", ["Income", "Expense"])
                category = st.selectbox(
                    "Category",
                    ["Crop Sales", "Input Purchases", "Labor", "Equipment",
                     "Loan Payment", "Transport", "Other"]
                )
                
            with col2:
                amount = st.number_input("Amount (KES)", 0.0)
                date = st.date_input("Date")
                
            with col3:
                description = st.text_input("Description")
                payment_method = st.selectbox(
                    "Payment Method",
                    ["Cash", "M-PESA", "Bank Transfer", "Credit"]
                )
                
            if st.button("Add Transaction"):
                st.success("Transaction recorded successfully!")
        
        # Income & Expense Analysis
        st.write("#### Monthly Summary")
        
        # Sample transaction data - replace with database data
        transactions = pd.DataFrame({
            'Month': pd.date_range(start='2025-01-01', periods=10, freq='M'),
            'Income': [95000, 82000, 78000, 88000, 92000, 85000, 79000, 90000, 87000, 94000],
            'Expenses': [65000, 55000, 48000, 52000, 58000, 50000, 45000, 54000, 51000, 57000]
        })
        
        transactions['Profit'] = transactions['Income'] - transactions['Expenses']
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=transactions['Month'],
            y=transactions['Income'],
            name='Income'
        ))
        fig.add_trace(go.Bar(
            x=transactions['Month'],
            y=transactions['Expenses'],
            name='Expenses'
        ))
        fig.add_trace(go.Scatter(
            x=transactions['Month'],
            y=transactions['Profit'],
            name='Profit',
            line=dict(color='green')
        ))
        
        fig.update_layout(title='Monthly Financial Performance')
        st.plotly_chart(fig, width="stretch")
        
        # Expense Breakdown
        st.write("#### Expense Analysis")
        
        # Sample expense categories - replace with database data
        expenses = pd.DataFrame({
            'Category': ['Input Purchases', 'Labor', 'Equipment', 'Transport', 'Loan Payment', 'Other'],
            'Amount': [180000, 150000, 80000, 45000, 40000, 25000]
        })
        
        fig = px.pie(expenses, values='Amount', names='Category',
                    title='Expense Distribution')
        st.plotly_chart(fig, width="stretch")
        
    with tabs[2]:
        st.subheader("Loans & Credit")
        
        # Loan Summary
        st.write("#### Active Loans")
        
        # Sample loan data - replace with database data
        loans = pd.DataFrame({
            'Loan_ID': ['L001', 'L002', 'L003'],
            'Type': ['Term Loan', 'Input Credit', 'Equipment'],
            'Amount': [200000, 50000, 150000],
            'Interest_Rate': [0.15, 0.12, 0.14],
            'Start_Date': ['2025-01-15', '2025-03-01', '2025-06-15'],
            'Term_Months': [24, 6, 18],
            'Balance': [150000, 20000, 130000]
        })
        
        for _, loan in loans.iterrows():
            with st.expander(f"{loan['Type']} - KES {loan['Amount']:,.2f}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"Start Date: {loan['Start_Date']}")
                    st.write(f"Term: {loan['Term_Months']} months")
                    st.write(f"Interest Rate: {loan['Interest_Rate']:.1%}")
                with col2:
                    st.write(f"Balance: KES {loan['Balance']:,.2f}")
                    progress = 1 - (loan['Balance'] / loan['Amount'])
                    st.progress(progress)
        
        # Credit Score Tracking
        st.write("#### Credit Score History")
        
        # Sample credit score history - replace with database data
        credit_history = pd.DataFrame({
            'Date': pd.date_range(start='2025-01-01', periods=10, freq='M'),
            'Score': [680, 695, 705, 720, 715, 730, 745, 750, 755, 750]
        })
        
        fig = px.line(credit_history, x='Date', y='Score',
                     title='Credit Score Trend')
        st.plotly_chart(fig, width="stretch")
        
    with tabs[3]:
        st.subheader("Financial Planning")
        
        # Budget Planning
        st.write("#### Budget Planning")
        
        col1, col2 = st.columns(2)
        
        with col1:
            planning_month = st.selectbox("Month", [
                "January", "February", "March", "April",
                "May", "June", "July", "August",
                "September", "October", "November", "December"
            ])
            
        with col2:
            planning_year = st.selectbox("Year", list(range(2025, 2030)))
        
        # Budget Categories
        st.write("#### Budget Categories")
        
        budget_categories = [
            "Seed Purchase", "Fertilizers", "Pesticides",
            "Labor", "Equipment Maintenance", "Fuel",
            "Transport", "Loan Payments", "Other"
        ]
        
        budget_data = {}
        for category in budget_categories:
            budget_data[category] = st.number_input(f"{category} (KES)", 0.0)
        
        if st.button("Save Budget"):
            st.success("Budget saved successfully!")
        
        # Cash Flow Projection
        st.write("#### Cash Flow Projection")
        
        # Sample cash flow projection - replace with calculated values
        projection = pd.DataFrame({
            'Month': pd.date_range(start='2025-01-01', periods=12, freq='M'),
            'Projected_Income': [90000, 85000, 80000, 95000, 100000, 88000,
                               92000, 87000, 93000, 89000, 94000, 98000],
            'Projected_Expenses': [60000, 55000, 50000, 65000, 70000, 58000,
                                 62000, 57000, 63000, 59000, 64000, 68000]
        })
        
        projection['Net_Cash_Flow'] = projection['Projected_Income'] - projection['Projected_Expenses']
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=projection['Month'],
            y=projection['Projected_Income'],
            name='Projected Income'
        ))
        fig.add_trace(go.Bar(
            x=projection['Month'],
            y=projection['Projected_Expenses'],
            name='Projected Expenses'
        ))
        fig.add_trace(go.Scatter(
            x=projection['Month'],
            y=projection['Net_Cash_Flow'],
            name='Net Cash Flow',
            line=dict(color='green')
        ))
        
        fig.update_layout(title='12-Month Cash Flow Projection')
        st.plotly_chart(fig, width="stretch")

if __name__ == "__main__":
    render()