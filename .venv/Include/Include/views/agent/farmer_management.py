import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def render():
    """Render the Farmer Management Dashboard for Agents."""
    
    st.subheader("Farmer Management")
    
    # Overview Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Farmers", "125", "+5")
    with col2:
        st.metric("Active Farmers", "115", "+3")
    with col3:
        st.metric("New This Month", "8", "+2")
    with col4:
        st.metric("Success Rate", "92%", "+1%")
    
    # Farmer Management Tabs
    tabs = st.tabs([
        "Farmer Directory",
        "Onboarding",
        "Progress Tracking",
        "Communications"
    ])
    
    with tabs[0]:
        st.write("#### Farmer Directory")
        
        # Search and Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text_input("Search Farmers", key="farmer_search")
        with col2:
            st.selectbox("Filter by Location",
                        ["All", "Nyeri", "Kiambu", "Thika"],
                        key="location_filter")
        with col3:
            st.selectbox("Filter by Status",
                        ["All", "Active", "Inactive", "New"],
                        key="status_filter")
        
        # Farmer List
        farmers = pd.DataFrame({
            'Name': ['John Doe', 'Jane Smith', 'Mike Johnson'],
            'Location': ['Nyeri', 'Kiambu', 'Thika'],
            'Farm Size': ['5 acres', '3 acres', '7 acres'],
            'Main Crops': ['Coffee, Maize', 'Tea, Beans', 'Maize, Potatoes'],
            'Status': ['Active', 'Active', 'New'],
            'Last Visit': ['2025-10-29', '2025-10-25', '2025-10-30']
        })
        
        for _, farmer in farmers.iterrows():
            with st.expander(f"{farmer['Name']} - {farmer['Location']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"Farm Size: {farmer['Farm Size']}")
                    st.write(f"Main Crops: {farmer['Main Crops']}")
                    st.write(f"Status: {farmer['Status']}")
                with col2:
                    st.write(f"Last Visit: {farmer['Last Visit']}")
                    st.button("Schedule Visit", key=f"visit_{farmer['Name']}")
                    st.button("View Details", key=f"details_{farmer['Name']}")
    
    with tabs[1]:
        st.write("#### Farmer Onboarding")
        
        # New Farmer Registration
        with st.expander("Register New Farmer", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.text_input("Farmer Name", key="new_farmer_name")
                st.text_input("Phone Number", key="new_farmer_phone")
                st.text_input("ID Number", key="new_farmer_id")
                st.selectbox("Location",
                           ["Nyeri", "Kiambu", "Thika"],
                           key="new_farmer_location")
            
            with col2:
                st.number_input("Farm Size (acres)", key="new_farmer_size")
                st.multiselect("Main Crops",
                             ["Coffee", "Tea", "Maize", "Beans", "Potatoes"],
                             key="new_farmer_crops")
                st.text_area("Additional Notes", key="new_farmer_notes")
            
            if st.button("Register Farmer", key="register_farmer"):
                st.success("Farmer registered successfully!")
        
        # Recent Registrations
        st.write("##### Recent Registrations")
        registrations = pd.DataFrame({
            'Date': ['2025-10-30', '2025-10-29', '2025-10-28'],
            'Farmer': ['Mike Johnson', 'Sarah Wilson', 'James Brown'],
            'Location': ['Thika', 'Nyeri', 'Kiambu'],
            'Status': ['Pending Training', 'Documentation', 'Completed']
        })
        st.dataframe(registrations)
    
    with tabs[2]:
        st.write("#### Progress Tracking")
        
        # Farmer Selection
        selected_farmer = st.selectbox(
            "Select Farmer",
            ["John Doe", "Jane Smith", "Mike Johnson"],
            key="progress_farmer"
        )
        
        # Progress Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Training Complete", "4/5", "+1")
            st.metric("Farm Score", "85/100", "+5")
        with col2:
            st.metric("Loan Status", "Active", "")
            st.metric("Repayment Rate", "95%", "+2%")
        with col3:
            st.metric("Yield Improvement", "+25%", "+5%")
            st.metric("Market Access", "Connected", "")
        
        # Progress Charts
        # Create date range for exactly 6 months
        month_range = pd.date_range(start='2025-05-01', periods=6, freq='M')
        progress_data = pd.DataFrame({
            'Month': month_range,
            'Farm_Score': [70, 72, 75, 78, 82, 85],
            'Yield': [100, 105, 110, 115, 120, 125]
        })
        
        fig = px.line(progress_data,
                     x='Month',
                     y=['Farm_Score', 'Yield'],
                     title='Farmer Progress Over Time')
        st.plotly_chart(fig)
        
        # Activity Timeline
        st.write("##### Activity Timeline")
        timeline = pd.DataFrame({
            'Date': ['2025-10-30', '2025-10-15', '2025-10-01'],
            'Activity': ['Farm Visit', 'Training Session', 'Loan Disbursement'],
            'Outcome': ['Pest Control Advice', 'Completed Module 3', 'KES 50,000']
        })
        st.dataframe(timeline)
    
    with tabs[3]:
        st.write("#### Communications")
        
        # Message Center
        with st.expander("Send New Message"):
            col1, col2 = st.columns(2)
            with col1:
                st.multiselect("Recipients",
                              ["John Doe", "Jane Smith", "Mike Johnson"],
                              key="msg_recipients")
                st.selectbox("Message Type",
                            ["Update", "Reminder", "Alert", "Training"],
                            key="msg_type")
            with col2:
                st.text_input("Subject", key="msg_subject")
                st.text_area("Message", key="msg_content")
            
            col1, col2 = st.columns(2)
            with col1:
                st.selectbox("Channel",
                            ["SMS", "WhatsApp", "Email"],
                            key="msg_channel")
            with col2:
                st.selectbox("Priority",
                            ["Normal", "High", "Urgent"],
                            key="msg_priority")
            
            if st.button("Send Message", key="send_message"):
                st.success("Message sent successfully!")
        
        # Message History
        st.write("##### Recent Communications")
        messages = pd.DataFrame({
            'Date': ['2025-10-30', '2025-10-29', '2025-10-28'],
            'Recipient': ['John Doe', 'All Farmers', 'Jane Smith'],
            'Type': ['Reminder', 'Update', 'Alert'],
            'Channel': ['SMS', 'WhatsApp', 'SMS'],
            'Status': ['Delivered', 'Sent', 'Read']
        })
        st.dataframe(messages)
        
        # Communication Analytics
        col1, col2 = st.columns(2)
        
        with col1:
            channel_stats = pd.DataFrame({
                'Channel': ['SMS', 'WhatsApp', 'Email'],
                'Messages': [150, 100, 50]
            })
            fig = px.pie(channel_stats, names='Channel', values='Messages',
                        title='Messages by Channel')
            st.plotly_chart(fig)
        
        with col2:
            response_stats = pd.DataFrame({
                'Type': ['Updates', 'Reminders', 'Alerts', 'Training'],
                'Response_Rate': [85, 90, 95, 80]
            })
            fig = px.bar(response_stats, x='Type', y='Response_Rate',
                        title='Response Rates by Message Type')
            st.plotly_chart(fig)

if __name__ == "__main__":
    render()