import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def render():
    """Render the Ticket Management Dashboard."""
    
    st.subheader("Ticket Management")
    
    # Ticket Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Open Tickets", "15", "-3")
    with col2:
        st.metric("Avg Response Time", "30 mins", "-5 mins")
    with col3:
        st.metric("Resolution Rate", "92%", "+2%")
    with col4:
        st.metric("Satisfaction", "4.7/5.0", "+0.1")
    
    # Ticket Management Tabs
    tabs = st.tabs([
        "Ticket Queue",
        "Ticket Creation",
        "Resolution Center",
        "Analytics"
    ])
    
    with tabs[0]:
        st.write("#### Ticket Queue")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            st.selectbox("Status",
                        ["All", "Open", "In Progress", "Resolved", "Closed"],
                        key="ticket_status")
        with col2:
            st.selectbox("Priority",
                        ["All", "High", "Medium", "Low"],
                        key="ticket_priority")
        with col3:
            st.selectbox("Category",
                        ["All", "Technical", "Account", "Billing",
                         "General Inquiry"],
                        key="ticket_category")
        
        # Ticket List
        tickets = pd.DataFrame({
            'ID': ['TKT-001', 'TKT-002', 'TKT-003'],
            'Subject': [
                'Login Issue',
                'Payment Failed',
                'App Not Loading'
            ],
            'User': ['John Doe', 'Jane Smith', 'Mike Johnson'],
            'Status': ['Open', 'In Progress', 'Open'],
            'Priority': ['High', 'Medium', 'Low'],
            'Created': [
                '2025-10-30 09:00',
                '2025-10-30 10:30',
                '2025-10-30 11:15'
            ]
        })
        
        for _, ticket in tickets.iterrows():
            with st.expander(
                f"{ticket['ID']} - {ticket['Subject']} ({ticket['Status']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"User: {ticket['User']}")
                    st.write(f"Priority: {ticket['Priority']}")
                    st.write(f"Created: {ticket['Created']}")
                with col2:
                    st.selectbox("Update Status",
                                ["Open", "In Progress", "Resolved", "Closed"],
                                key=f"status_{ticket['ID']}")
                    st.button("View Details",
                             key=f"view_{ticket['ID']}")
    
    with tabs[1]:
        st.write("#### Create New Ticket")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("User ID/Name", key="new_ticket_user")
            st.selectbox("Category",
                        ["Technical", "Account", "Billing",
                         "General Inquiry"],
                        key="new_ticket_category")
            st.selectbox("Priority",
                        ["High", "Medium", "Low"],
                        key="new_ticket_priority")
        
        with col2:
            st.text_input("Subject", key="new_ticket_subject")
            st.text_area("Description", key="new_ticket_desc")
            st.file_uploader("Attachments",
                           accept_multiple_files=True,
                           key="new_ticket_files")
        
        if st.button("Create Ticket", key="create_ticket"):
            st.success("Ticket created successfully!")
    
    with tabs[2]:
        st.write("#### Resolution Center")
        
        # Resolution Tools
        col1, col2 = st.columns(2)
        
        with col1:
            st.selectbox("Select Ticket",
                        tickets['ID'].tolist(),
                        key="resolve_ticket_id")
            
            resolution_types = [
                "Issue Resolution",
                "Feature Request",
                "Bug Fix",
                "Account Update",
                "Information Provided"
            ]
            st.selectbox("Resolution Type",
                        resolution_types,
                        key="resolution_type")
        
        with col2:
            st.text_area("Resolution Notes",
                        key="resolution_notes")
            st.multiselect("Applied Solutions",
                          ["Password Reset", "Account Update",
                           "Bug Fix", "Configuration Change"],
                          key="applied_solutions")
        
        # Resolution Actions
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("Resolve Ticket", key="resolve_ticket")
        with col2:
            st.button("Escalate", key="escalate_ticket")
        with col3:
            st.button("Request Info", key="request_info")
        
        # Communication History
        st.write("##### Communication History")
        comms = pd.DataFrame({
            'Time': [
                '2025-10-30 09:15',
                '2025-10-30 09:30',
                '2025-10-30 09:45'
            ],
            'From': ['User', 'Support', 'User'],
            'Message': [
                'Having trouble logging in',
                'Please try clearing cache',
                'Still not working'
            ]
        })
        st.dataframe(comms)
        
        # Quick Responses
        st.write("##### Quick Responses")
        responses = [
            "Please try clearing your cache and cookies",
            "Could you please provide more details?",
            "I'll escalate this to our technical team",
            "Have you tried restarting the application?"
        ]
        
        selected_response = st.selectbox("Select Response",
                                       responses,
                                       key="quick_response")
        st.button("Send Response", key="send_response")
    
    with tabs[3]:
        st.write("#### Ticket Analytics")
        
        # Time Period Selection
        period = st.selectbox("Time Period",
                            ["Today", "This Week", "This Month", "Custom"],
                            key="analytics_period")
        
        # Ticket Volume Trends
        volume_data = pd.DataFrame({
            'Date': pd.date_range(start='2025-10-01', end='2025-10-30',
                                freq='D'),
            'Tickets': range(10, 40)
        })
        
        fig = px.line(volume_data, x='Date', y='Tickets',
                     title='Ticket Volume Trend')
        st.plotly_chart(fig)
        
        # Category Distribution
        col1, col2 = st.columns(2)
        
        with col1:
            category_dist = pd.DataFrame({
                'Category': [
                    'Technical',
                    'Account',
                    'Billing',
                    'General'
                ],
                'Count': [50, 30, 20, 15]
            })
            fig = px.pie(category_dist, names='Category', values='Count',
                        title='Tickets by Category')
            st.plotly_chart(fig)
        
        with col2:
            resolution_time = pd.DataFrame({
                'Category': [
                    'Technical',
                    'Account',
                    'Billing',
                    'General'
                ],
                'Minutes': [45, 30, 25, 15]
            })
            fig = px.bar(resolution_time, x='Category', y='Minutes',
                        title='Avg Resolution Time by Category')
            st.plotly_chart(fig)
        
        # Support Team Performance
        st.write("##### Team Performance")
        performance = pd.DataFrame({
            'Agent': ['Alice', 'Bob', 'Charlie', 'David'],
            'Tickets_Handled': [45, 38, 42, 35],
            'Avg_Response_Time': [25, 28, 22, 30],
            'Resolution_Rate': [95, 92, 94, 90],
            'Satisfaction': [4.8, 4.7, 4.9, 4.6]
        })
        st.dataframe(performance)
        
        # SLA Compliance
        st.write("##### SLA Compliance")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Response Time SLA", "95%", "+2%")
        with col2:
            st.metric("Resolution Time SLA", "92%", "+3%")
        with col3:
            st.metric("Customer Satisfaction", "4.7/5.0", "+0.1")

if __name__ == "__main__":
    render()