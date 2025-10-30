import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def render():
    """Render the Field Visits Dashboard for Agents."""
    
    st.subheader("Field Visits")
    
    # Visit Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Today's Visits", "8/10", "80%")
    with col2:
        st.metric("Weekly Visits", "35/40", "88%")
    with col3:
        st.metric("Monthly Target", "125/150", "83%")
    with col4:
        st.metric("Average Duration", "45 mins", "+5 mins")
    
    # Field Visit Tabs
    tabs = st.tabs([
        "Visit Planning",
        "Visit Reports",
        "Route Optimization",
        "Visit Analytics"
    ])
    
    with tabs[0]:
        st.write("#### Visit Planning")
        
        # New Visit
        with st.expander("Schedule New Visit", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.selectbox("Farmer",
                           ["John Doe", "Jane Smith", "Mike Johnson"],
                           key="visit_farmer")
                st.date_input("Visit Date", key="visit_date")
                st.time_input("Visit Time", key="visit_time")
            
            with col2:
                st.selectbox("Visit Type",
                           ["Regular Check", "Issue Resolution",
                            "Training", "Assessment"],
                           key="visit_type")
                st.text_area("Visit Purpose", key="visit_purpose")
                st.multiselect("Required Tools",
                             ["Soil Test Kit", "Moisture Meter",
                              "GPS Device", "Tablet"],
                             key="visit_tools")
            
            if st.button("Schedule Visit", key="schedule_visit"):
                st.success("Visit scheduled successfully!")
        
        # Visit Schedule
        st.write("##### Upcoming Visits")
        schedule = pd.DataFrame({
            'Date': ['2025-10-31', '2025-10-31', '2025-11-01'],
            'Time': ['09:00 AM', '02:00 PM', '10:00 AM'],
            'Farmer': ['John Doe', 'Jane Smith', 'Mike Johnson'],
            'Location': ['Nyeri', 'Kiambu', 'Thika'],
            'Type': ['Regular Check', 'Training', 'Assessment']
        })
        st.dataframe(schedule)
        
        # Visit Map
        st.write("##### Visit Locations")
        locations = pd.DataFrame({
            'Farmer': ['John Doe', 'Jane Smith', 'Mike Johnson'],
            'lat': [-1.2921, -1.2850, -1.3032],
            'lon': [36.8219, 36.8165, 36.8083]
        })
        st.map(locations)
    
    with tabs[1]:
        st.write("#### Visit Reports")
        
        # New Report
        with st.expander("Submit Visit Report"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.selectbox("Select Visit",
                           ["John Doe - 2025-10-30 09:00 AM",
                            "Jane Smith - 2025-10-30 02:00 PM"],
                           key="report_visit")
                st.slider("Visit Duration (minutes)",
                         15, 120, 45,
                         key="visit_duration")
                st.multiselect("Activities Completed",
                             ["Farm Inspection", "Soil Testing",
                              "Training", "Issue Resolution"],
                             key="visit_activities")
            
            with col2:
                st.selectbox("Farm Status",
                           ["Excellent", "Good", "Fair", "Needs Attention"],
                           key="farm_status")
                st.text_area("Observations", key="visit_observations")
                st.text_area("Recommendations", key="visit_recommendations")
            
            st.file_uploader("Upload Photos", accept_multiple_files=True,
                           key="visit_photos")
            
            if st.button("Submit Report", key="submit_report"):
                st.success("Report submitted successfully!")
        
        # Recent Reports
        st.write("##### Recent Visit Reports")
        reports = pd.DataFrame({
            'Date': ['2025-10-30', '2025-10-29', '2025-10-28'],
            'Farmer': ['John Doe', 'Jane Smith', 'Mike Johnson'],
            'Type': ['Regular Check', 'Training', 'Assessment'],
            'Status': ['Completed', 'Completed', 'Pending Review']
        })
        
        for _, report in reports.iterrows():
            with st.expander(f"{report['Date']} - {report['Farmer']}"):
                st.write(f"Visit Type: {report['Type']}")
                st.write(f"Status: {report['Status']}")
                col1, col2 = st.columns(2)
                with col1:
                    st.button("View Details",
                             key=f"view_report_{report['Farmer']}")
                with col2:
                    st.button("Download Report",
                             key=f"download_report_{report['Farmer']}")
    
    with tabs[2]:
        st.write("#### Route Optimization")
        
        # Route Planning
        col1, col2 = st.columns(2)
        
        with col1:
            st.date_input("Route Date", key="route_date")
            st.multiselect("Select Visits",
                          ["John Doe - Nyeri",
                           "Jane Smith - Kiambu",
                           "Mike Johnson - Thika"],
                          key="route_visits")
        
        with col2:
            st.selectbox("Transportation",
                        ["Car", "Motorcycle", "Public Transport"],
                        key="route_transport")
            st.number_input("Max Visits per Day",
                          min_value=1, max_value=10, value=5,
                          key="max_visits")
        
        if st.button("Optimize Route", key="optimize_route"):
            st.success("Route optimized successfully!")
        
        # Route Map
        st.write("##### Optimized Route")
        st.map(locations)  # Reusing locations DataFrame from earlier
        
        # Route Details
        st.write("##### Route Schedule")
        route = pd.DataFrame({
            'Time': ['09:00 AM', '10:30 AM', '02:00 PM'],
            'Farmer': ['John Doe', 'Jane Smith', 'Mike Johnson'],
            'Location': ['Nyeri', 'Kiambu', 'Thika'],
            'Distance': ['0 km', '15 km', '25 km'],
            'Duration': ['1h', '1h', '1h']
        })
        st.dataframe(route)
    
    with tabs[3]:
        st.write("#### Visit Analytics")
        
        # Visit Statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Completion Rate", "92%", "+2%")
        with col2:
            st.metric("Farmer Satisfaction", "4.8/5.0", "+0.1")
        with col3:
            st.metric("Issue Resolution", "95%", "+3%")
        
        # Visit Trends
        # Create date range for exactly 10 weeks
        week_range = pd.date_range(start='2025-09-01', periods=10, freq='W')
        visit_data = pd.DataFrame({
            'Week': week_range,
            'Planned': range(35, 45),
            'Completed': range(32, 42)
        })
        
        fig = px.line(visit_data, x='Week', y=['Planned', 'Completed'],
                     title='Visit Completion Trends')
        st.plotly_chart(fig)
        
        # Visit Types Distribution
        col1, col2 = st.columns(2)
        
        with col1:
            type_dist = pd.DataFrame({
                'Type': ['Regular Check', 'Training',
                        'Assessment', 'Issue Resolution'],
                'Count': [50, 30, 25, 20]
            })
            fig = px.pie(type_dist, names='Type', values='Count',
                        title='Visits by Type')
            st.plotly_chart(fig)
        
        with col2:
            location_dist = pd.DataFrame({
                'Location': ['Nyeri', 'Kiambu', 'Thika', 'Others'],
                'Visits': [40, 35, 30, 20]
            })
            fig = px.bar(location_dist, x='Location', y='Visits',
                        title='Visits by Location')
            st.plotly_chart(fig)

if __name__ == "__main__":
    render()