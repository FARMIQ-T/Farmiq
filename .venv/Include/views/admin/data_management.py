import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def render():
    """Render the Data Management Dashboard."""
    
    st.subheader("Data Management")
    
    # Data Overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Records", "25,000", "+1,500")
    with col2:
        st.metric("Storage Used", "2.5GB", "+0.2GB")
    with col3:
        st.metric("Last Backup", "2h ago", "On Schedule")
    with col4:
        st.metric("Data Quality", "98%", "+1%")
    
    # Data Management Tabs
    tabs = st.tabs([
        "Data Overview",
        "Backup & Recovery",
        "Data Quality",
        "Data Integration"
    ])
    
    with tabs[0]:
        st.write("#### Data Overview")
        
        # Data Distribution
        data_dist = pd.DataFrame({
            'Category': [
                'User Data',
                'Farm Data',
                'Financial Data',
                'Market Data',
                'System Logs'
            ],
            'Size_GB': [0.8, 0.6, 0.5, 0.4, 0.2],
            'Records': [10000, 8000, 4000, 2000, 1000]
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(data_dist, names='Category', values='Size_GB',
                        title='Storage Distribution')
            st.plotly_chart(fig)
        
        with col2:
            fig = px.bar(data_dist, x='Category', y='Records',
                        title='Records by Category')
            st.plotly_chart(fig)
        
        # Data Growth
        date_range = pd.date_range(start='2025-05-01', end='2025-10-30', freq='M')
        growth_data = pd.DataFrame({
            'Date': date_range,
            'Size_GB': [1.5, 1.8, 2.0, 2.2, 2.4, 2.5][:len(date_range)]
        })
        
        fig = px.line(growth_data, x='Date', y='Size_GB',
                     title='Data Growth Over Time')
        st.plotly_chart(fig)
    
    with tabs[1]:
        st.write("#### Backup & Recovery")
        
        # Backup Status
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("##### Latest Backups")
            backups = pd.DataFrame({
                'Type': ['Full', 'Incremental', 'Full', 'Incremental'],
                'Date': ['2025-10-30', '2025-10-29', '2025-10-28', '2025-10-27'],
                'Size': ['2.5GB', '0.2GB', '2.4GB', '0.15GB'],
                'Status': ['Success', 'Success', 'Success', 'Success']
            })
            st.dataframe(backups)
        
        with col2:
            st.write("##### Backup Schedule")
            st.selectbox("Backup Frequency",
                        ["Daily", "Weekly", "Monthly"])
            st.time_input("Backup Time")
            st.multiselect(
                "Backup Type",
                ["Full Backup", "Incremental Backup", "Differential Backup"],
                key="backup_type_select"
            )
            st.number_input("Retention Period (days)", value=30)
        
        # Recovery Options
        with st.expander("Recovery Options"):
            st.selectbox("Recovery Point",
                        ["Latest Backup", "Custom Date", "Pre-defined Point"])
            st.selectbox("Recovery Type",
                        ["Full Recovery", "Selective Recovery"])
            st.multiselect("Select Data Categories",
                          ["User Data", "Farm Data", "Financial Data"],
                          key="recovery_data_categories")
            st.checkbox("Verify Before Recovery")
            st.button("Start Recovery")
    
    with tabs[2]:
        st.write("#### Data Quality")
        
        # Quality Metrics
        quality_metrics = pd.DataFrame({
            'Metric': [
                'Completeness',
                'Accuracy',
                'Consistency',
                'Timeliness',
                'Validity'
            ],
            'Score': [98, 95, 97, 99, 96],
            'Change': [+1, -0.5, +0.8, 0, +1.2]
        })
        
        fig = px.bar(quality_metrics, x='Metric', y='Score',
                    title='Data Quality Metrics')
        st.plotly_chart(fig)
        
        # Data Issues
        st.write("##### Data Quality Issues")
        issues = pd.DataFrame({
            'Category': ['User Data', 'Farm Data', 'Financial Data'],
            'Missing_Fields': [25, 15, 10],
            'Invalid_Values': [12, 8, 5],
            'Duplicates': [5, 3, 2]
        })
        
        st.dataframe(issues)
        
        # Data Cleansing
        with st.expander("Data Cleansing Tools"):
            st.selectbox("Select Operation",
                        ["Remove Duplicates", "Fill Missing Values",
                         "Standardize Format", "Validate Data"])
            st.multiselect("Select Tables",
                          ["Users", "Farms", "Transactions", "Crops"],
                          key="cleansing_tables")
            st.button("Run Cleansing")
    
    with tabs[3]:
        st.write("#### Data Integration")
        
        # Integration Status
        st.write("##### Active Integrations")
        integrations = pd.DataFrame({
            'Service': [
                'Weather API',
                'Market Price API',
                'SMS Gateway',
                'Payment Gateway'
            ],
            'Status': ['Active', 'Active', 'Active', 'Active'],
            'Last_Sync': [
                '2025-10-30 10:00',
                '2025-10-30 09:45',
                '2025-10-30 09:30',
                '2025-10-30 09:15'
            ],
            'Success_Rate': ['99%', '98%', '100%', '99%']
        })
        
        st.dataframe(integrations)
        
        # New Integration
        with st.expander("Add New Integration"):
            st.selectbox("Integration Type",
                        ["API", "Database", "File Import", "Custom"])
            st.text_input("Service Name")
            st.text_input("API Key/Connection String")
            st.selectbox("Data Format", ["JSON", "XML", "CSV", "Custom"])
            st.number_input("Sync Interval (minutes)", value=15)
            st.checkbox("Enable Error Notifications")
            st.button("Add Integration")
        
        # Sync History
        st.write("##### Sync History")
        sync_history = pd.DataFrame({
            'Timestamp': pd.date_range(start='2025-10-30 00:00',
                                     end='2025-10-30 10:00',
                                     freq='2H'),
            'Records_Synced': [500, 450, 600, 550, 480, 520],
            'Duration_Sec': [25, 22, 28, 26, 24, 25]
        })
        
        fig = px.line(sync_history,
                     x='Timestamp',
                     y=['Records_Synced', 'Duration_Sec'],
                     title='Sync Performance')
        st.plotly_chart(fig)

if __name__ == "__main__":
    render()