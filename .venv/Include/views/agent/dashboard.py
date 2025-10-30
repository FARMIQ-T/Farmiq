import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

def render():
    """Render the Agent Dashboard."""
    
    st.subheader("Agent Dashboard")
    
    # Key Performance Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Assigned Farmers", "125", "+5")
    with col2:
        st.metric("Active Cases", "15", "-2")
    with col3:
        st.metric("Field Visits Today", "8", "+3")
    with col4:
        st.metric("Response Rate", "95%", "+2%")
    
    # Dashboard Tabs
    tabs = st.tabs([
        "Overview",
        "Tasks",
        "Schedule",
        "Performance"
    ])
    
    with tabs[0]:
        st.write("#### Daily Overview")
        
        # Today's Schedule
        st.write("##### Today's Schedule")
        schedule = pd.DataFrame({
            'Time': ['09:00 AM', '10:30 AM', '02:00 PM', '04:00 PM'],
            'Activity': ['Farm Visit', 'Training Session', 'Loan Assessment', 'Field Inspection'],
            'Farmer/Group': ['John Doe', 'Coffee Growers Group', 'Jane Smith', 'Mike Johnson'],
            'Location': ['Nyeri', 'Community Center', 'Kiambu', 'Thika'],
            'Status': ['Completed', 'In Progress', 'Pending', 'Pending']
        })
        st.dataframe(schedule)
        
        # Activity Map
        st.write("##### Activity Map")
        locations = pd.DataFrame({
            'Farmer': ['John Doe', 'Jane Smith', 'Mike Johnson'],
            'lat': [-1.2921, -1.2850, -1.3032],
            'lon': [36.8219, 36.8165, 36.8083],
            'Activity': ['Farm Visit', 'Loan Assessment', 'Field Inspection']
        })
        st.map(locations)
    
    with tabs[1]:
        st.write("#### Task Management")
        
        # Add New Task
        with st.expander("Add New Task"):
            col1, col2 = st.columns(2)
            with col1:
                st.selectbox("Task Type", [
                    "Farm Visit",
                    "Training Session",
                    "Loan Assessment",
                    "Field Inspection",
                    "Follow-up"
                ], key="new_task_type")
                st.selectbox("Farmer/Group", [
                    "John Doe",
                    "Jane Smith",
                    "Mike Johnson",
                    "Coffee Growers Group"
                ], key="new_task_farmer")
                st.date_input("Due Date", key="new_task_date")
            with col2:
                st.text_area("Description", key="new_task_desc")
                st.selectbox("Priority", ["High", "Medium", "Low"], key="new_task_priority")
            
            if st.button("Create Task", key="create_task_btn"):
                st.success("Task created successfully!")
        
        # Task List
        st.write("##### Task List")
        status_filter = st.selectbox("Filter by Status",
                                   ["All", "Pending", "In Progress", "Completed"],
                                   key="task_status_filter")
        
        tasks = pd.DataFrame({
            'Task': ['Farm Visit', 'Training Session', 'Loan Assessment'],
            'Farmer/Group': ['John Doe', 'Coffee Growers', 'Jane Smith'],
            'Due Date': ['2025-10-31', '2025-11-01', '2025-11-02'],
            'Priority': ['High', 'Medium', 'Low'],
            'Status': ['Pending', 'In Progress', 'Completed']
        })
        st.dataframe(tasks)
    
    with tabs[2]:
        st.write("#### Schedule Management")
        
        # Calendar View
        st.write("##### Weekly Calendar")
        calendar = pd.DataFrame({
            'Time': pd.date_range(start='2025-10-30', periods=7, freq='D'),
            'Morning': ['Farm Visit', 'Training', 'Office', 'Farm Visit',
                       'Assessment', 'Off', 'Training'],
            'Afternoon': ['Assessment', 'Farm Visit', 'Training', 'Office',
                        'Farm Visit', 'Off', 'Office']
        })
        st.dataframe(calendar)
        
        # Schedule Analytics
        col1, col2 = st.columns(2)
        
        with col1:
            activity_dist = pd.DataFrame({
                'Activity': ['Farm Visits', 'Training', 'Assessments', 'Office Work'],
                'Hours': [20, 15, 10, 15]
            })
            fig = px.pie(activity_dist, names='Activity', values='Hours',
                        title='Weekly Time Distribution')
            st.plotly_chart(fig)
        
        with col2:
            location_dist = pd.DataFrame({
                'Location': ['Nyeri', 'Kiambu', 'Thika', 'Office'],
                'Visits': [12, 8, 6, 10]
            })
            fig = px.bar(location_dist, x='Location', y='Visits',
                        title='Visits by Location')
            st.plotly_chart(fig)
    
    with tabs[3]:
        st.write("#### Performance Metrics")
        
        # Performance Overview
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Farmers Onboarded", "25", "+5")
            st.metric("Training Sessions", "12", "+2")
        with col2:
            st.metric("Loan Applications", "18", "+3")
            st.metric("Success Rate", "92%", "+1%")
        with col3:
            st.metric("Field Visits", "45", "+8")
            st.metric("Satisfaction Score", "4.8/5.0", "+0.2")
        
        # Performance Charts
        performance_data = pd.DataFrame({
            'Date': pd.date_range(start='2025-10-01', end='2025-10-30', freq='D'),
            'Visits': range(30, 60),
            'Success_Rate': [90 + i/10 for i in range(30)]
        })
        
        fig = px.line(performance_data, x='Date', y=['Visits', 'Success_Rate'],
                     title='Performance Trends')
        st.plotly_chart(fig)
        
        # Feedback Overview
        st.write("##### Recent Feedback")
        feedback = pd.DataFrame({
            'Date': ['2025-10-29', '2025-10-28', '2025-10-27'],
            'Farmer': ['John Doe', 'Jane Smith', 'Mike Johnson'],
            'Rating': [5, 4, 5],
            'Comment': [
                'Very helpful visit and clear explanations',
                'Good training session but could be more detailed',
                'Excellent support with loan application'
            ]
        })
        st.dataframe(feedback)

if __name__ == "__main__":
    render()