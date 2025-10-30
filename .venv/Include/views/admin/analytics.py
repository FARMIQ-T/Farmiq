import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def render():
    """Render the Analytics & Reports Dashboard."""
    
    st.subheader("Analytics & Reports")
    
    # Time Period Selection
    col1, col2 = st.columns(2)
    with col1:
        period = st.selectbox(
            "Time Period",
            ["Last 7 Days", "Last 30 Days", "Last 90 Days", "Last Year", "Custom"]
        )
    with col2:
        if period == "Custom":
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Users", "1,250", "+50")
    with col2:
        st.metric("Active Farmers", "980", "+35")
    with col3:
        st.metric("Total Transactions", "KES 2.5M", "+15%")
    with col4:
        st.metric("Average Loan Size", "KES 50K", "+5%")
    
    # Analytics Tabs
    tabs = st.tabs([
        "User Analytics",
        "Financial Analytics",
        "Farm Analytics",
        "Custom Reports"
    ])
    
    with tabs[0]:
        st.write("#### User Analytics")
        
        # User Growth
        date_range = pd.date_range(start='2025-05-01', end='2025-10-30', freq='D')
        user_growth = pd.DataFrame({
            'Date': date_range,
            'Users': range(800, 800 + len(date_range))
        })
        
        fig = px.line(user_growth, x='Date', y='Users',
                     title='User Growth Trend')
        st.plotly_chart(fig)
        
        # User Demographics
        col1, col2 = st.columns(2)
        
        with col1:
            location_data = pd.DataFrame({
                'Location': ['Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Others'],
                'Users': [400, 300, 200, 150, 200]
            })
            fig = px.pie(location_data, names='Location', values='Users',
                        title='Users by Location')
            st.plotly_chart(fig)
        
        with col2:
            age_data = pd.DataFrame({
                'Age_Group': ['18-25', '26-35', '36-45', '46-55', '55+'],
                'Users': [200, 400, 350, 200, 100]
            })
            fig = px.bar(age_data, x='Age_Group', y='Users',
                        title='Users by Age Group')
            st.plotly_chart(fig)
    
    with tabs[1]:
        st.write("#### Financial Analytics")
        
        # Transaction Overview
        transactions = pd.DataFrame({
            'Date': pd.date_range(start='2025-10-01', end='2025-10-30'),
            'Value': [round(x) for x in range(80000, 110000, 1000)]
        })
        
        fig = px.line(transactions, x='Date', y='Value',
                     title='Daily Transaction Volume')
        st.plotly_chart(fig)
        
        # Financial Metrics
        col1, col2 = st.columns(2)
        
        with col1:
            loan_data = pd.DataFrame({
                'Status': ['Active', 'Completed', 'Defaulted', 'Pending'],
                'Amount': [1500000, 800000, 100000, 300000]
            })
            fig = px.pie(loan_data, names='Status', values='Amount',
                        title='Loan Portfolio Distribution')
            st.plotly_chart(fig)
        
        with col2:
            revenue_data = pd.DataFrame({
                'Source': ['Loan Interest', 'Service Fees', 'Commissions'],
                'Amount': [500000, 300000, 200000]
            })
            fig = px.bar(revenue_data, x='Source', y='Amount',
                        title='Revenue Sources')
            st.plotly_chart(fig)
    
    with tabs[2]:
        st.write("#### Farm Analytics")
        
        # Crop Distribution
        crop_data = pd.DataFrame({
            'Crop': ['Maize', 'Beans', 'Potatoes', 'Tomatoes', 'Others'],
            'Area': [500, 300, 200, 150, 100],
            'Production': [2500, 900, 4000, 3000, 500]
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(crop_data, names='Crop', values='Area',
                        title='Land Usage by Crop')
            st.plotly_chart(fig)
        
        with col2:
            fig = px.bar(crop_data, x='Crop', y='Production',
                        title='Production by Crop')
            st.plotly_chart(fig)
        
        # Yield Analysis
        # Create date range for exactly 10 months
        month_range = pd.date_range(start='2025-01-01', periods=10, freq='M')
        yield_data = pd.DataFrame({
            'Month': month_range,
            'Actual_Yield': [85, 82, 88, 90, 87, 92, 89, 91, 88, 90],
            'Expected_Yield': [80, 80, 80, 80, 80, 80, 80, 80, 80, 80]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=yield_data['Month'],
            y=yield_data['Actual_Yield'],
            name='Actual Yield'
        ))
        fig.add_trace(go.Scatter(
            x=yield_data['Month'],
            y=yield_data['Expected_Yield'],
            name='Expected Yield'
        ))
        fig.update_layout(title='Yield Performance Over Time')
        st.plotly_chart(fig)
    
    with tabs[3]:
        st.write("#### Custom Reports")
        
        # Report Builder
        with st.expander("Report Builder", expanded=True):
            st.multiselect(
                "Select Metrics",
                [
                    "User Growth",
                    "Transaction Volume",
                    "Loan Performance",
                    "Crop Production",
                    "Revenue Analysis",
                    "User Demographics"
                ],
                key="report_metrics"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                st.selectbox("Chart Type",
                            ["Line Chart", "Bar Chart", "Pie Chart", "Table"])
            with col2:
                st.selectbox("Export Format", ["PDF", "Excel", "CSV"])
            
            if st.button("Generate Report"):
                st.info("Generating report... Please wait.")
        
        # Saved Reports
        st.write("#### Saved Reports")
        saved_reports = pd.DataFrame({
            'Report Name': [
                'Monthly User Analysis',
                'Quarterly Financial Report',
                'Annual Farm Performance',
                'Weekly Transaction Summary'
            ],
            'Last Generated': [
                '2025-10-30',
                '2025-10-01',
                '2025-09-30',
                '2025-10-25'
            ],
            'Format': ['PDF', 'Excel', 'PDF', 'CSV']
        })
        
        for _, report in saved_reports.iterrows():
            with st.expander(f"{report['Report Name']} ({report['Format']})"):
                st.write(f"Last Generated: {report['Last Generated']}")
                col1, col2 = st.columns(2)
                with col1:
                    st.button("Regenerate", key=f"regen_{report['Report Name']}")
                with col2:
                    st.button("Download", key=f"download_{report['Report Name']}")

if __name__ == "__main__":
    render()