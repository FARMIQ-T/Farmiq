import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def render():
    """Render the Audit Logs Dashboard."""
    
    st.subheader("Audit Logs")
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.date_input("Start Date")
    with col2:
        st.date_input("End Date")
    with col3:
        st.selectbox(
            "Event Type",
            ["All", "User", "System", "Security", "Data", "Financial"]
        )
    with col4:
        st.selectbox(
            "Severity",
            ["All", "Info", "Warning", "Error", "Critical"]
        )
    
    # Search
    st.text_input("Search Logs")
    
    # Audit Log Tabs
    tabs = st.tabs([
        "Activity Logs",
        "System Logs",
        "Security Logs",
        "Data Logs"
    ])
    
    with tabs[0]:
        st.write("#### Activity Logs")
        
        # Activity Summary
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Activities", "2,500", "+150")
        with col2:
            st.metric("Active Users", "125", "+15")
        with col3:
            st.metric("Success Rate", "99.5%", "+0.2%")
        with col4:
            st.metric("Avg Response Time", "120ms", "-10ms")
        
        # Activity Log Table
        activities = pd.DataFrame({
            'Timestamp': [
                '2025-10-30 10:15:00',
                '2025-10-30 10:00:00',
                '2025-10-30 09:45:00',
                '2025-10-30 09:30:00'
            ],
            'User': ['John Doe', 'Jane Smith', 'Mike Johnson', 'Sarah Williams'],
            'Action': [
                'Profile Update',
                'Loan Application',
                'Market Price Update',
                'Crop Plan Creation'
            ],
            'Status': ['Success', 'Success', 'Failed', 'Success'],
            'Details': [
                'Updated contact information',
                'Submitted new loan application',
                'Error in price update',
                'Created new crop plan'
            ]
        })
        
        st.dataframe(activities)
    
    with tabs[1]:
        st.write("#### System Logs")
        
        # System Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("CPU Usage", "45%", "-5%")
        with col2:
            st.metric("Memory Usage", "65%", "+10%")
        with col3:
            st.metric("Disk Usage", "55%", "+2%")
        
        # System Events Chart
        system_events = pd.DataFrame({
            'Time': pd.date_range(start='2025-10-30 00:00', end='2025-10-30 23:59', freq='H'),
            'Events': [10, 15, 8, 12, 20, 25, 30, 35, 40, 38, 35, 30,
                      25, 28, 32, 35, 40, 38, 35, 30, 25, 20, 15, 10]
        })
        
        fig = px.line(system_events, x='Time', y='Events',
                     title='System Events Over Time')
        st.plotly_chart(fig)
        
        # System Log Table
        system_logs = pd.DataFrame({
            'Timestamp': system_events['Time'][:5],
            'Component': ['Database', 'API', 'Cache', 'Queue', 'Storage'],
            'Event': [
                'Connection Pool Reset',
                'Rate Limit Reached',
                'Cache Cleared',
                'Queue Processed',
                'Backup Completed'
            ],
            'Status': ['Success', 'Warning', 'Success', 'Success', 'Success']
        })
        
        st.dataframe(system_logs)
    
    with tabs[2]:
        st.write("#### Security Logs")
        
        # Security Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Failed Logins", "25", "-5")
        with col2:
            st.metric("Blocked IPs", "10", "+2")
        with col3:
            st.metric("Password Resets", "15", "+3")
        with col4:
            st.metric("2FA Usage", "85%", "+5%")
        
        # Security Events
        security_events = pd.DataFrame({
            'Timestamp': [
                '2025-10-30 10:15:00',
                '2025-10-30 10:00:00',
                '2025-10-30 09:45:00',
                '2025-10-30 09:30:00'
            ],
            'Event Type': [
                'Login Attempt',
                'Password Reset',
                'Permission Change',
                'API Access'
            ],
            'User/IP': [
                'user@example.com',
                '192.168.1.100',
                'admin@example.com',
                'api_user_1'
            ],
            'Status': ['Failed', 'Success', 'Success', 'Blocked'],
            'Details': [
                'Invalid credentials',
                'Password reset completed',
                'Admin rights granted',
                'Rate limit exceeded'
            ]
        })
        
        st.dataframe(security_events)
        
        # Security Alerts
        with st.expander("Active Security Alerts"):
            alerts = [
                "Multiple failed login attempts from IP: 192.168.1.100",
                "Unusual API access pattern detected",
                "New admin user created",
                "Database backup verification pending"
            ]
            for alert in alerts:
                st.warning(alert)
    
    with tabs[3]:
        st.write("#### Data Logs")
        
        # Data Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Records Updated", "1,500", "+200")
        with col2:
            st.metric("Data Exports", "25", "+5")
        with col3:
            st.metric("Storage Used", "2.5GB", "+0.2GB")
        with col4:
            st.metric("Backup Status", "Current", "")
        
        # Data Operations Log
        data_ops = pd.DataFrame({
            'Timestamp': [
                '2025-10-30 10:15:00',
                '2025-10-30 10:00:00',
                '2025-10-30 09:45:00',
                '2025-10-30 09:30:00'
            ],
            'Operation': [
                'Bulk Update',
                'Data Export',
                'Record Deletion',
                'Data Import'
            ],
            'User': [
                'John Doe',
                'System',
                'Jane Smith',
                'Mike Johnson'
            ],
            'Records': [500, 1000, 50, 200],
            'Status': ['Success', 'Success', 'Success', 'Failed']
        })
        
        st.dataframe(data_ops)
        
        # Data Changes Chart
        data_changes = pd.DataFrame({
            'Operation': ['Create', 'Update', 'Delete', 'Export'],
            'Count': [500, 1000, 50, 200]
        })
        
        fig = px.bar(data_changes, x='Operation', y='Count',
                    title='Data Operations Summary')
        st.plotly_chart(fig)
    
    # Export Options
    st.write("#### Export Options")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.selectbox("Export Format", ["CSV", "Excel", "JSON", "PDF"])
    with col2:
        st.checkbox("Include Timestamps")
    with col3:
        st.button("Export Logs")

if __name__ == "__main__":
    render()