import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def render():
    """Render the Training Programs Dashboard for Agents."""
    
    st.subheader("Training Programs")
    
    # Training Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Programs", "5", "+1")
    with col2:
        st.metric("Total Participants", "150", "+15")
    with col3:
        st.metric("Completion Rate", "85%", "+3%")
    with col4:
        st.metric("Satisfaction Score", "4.7/5.0", "+0.2")
    
    # Training Tabs
    tabs = st.tabs([
        "Program Management",
        "Session Planning",
        "Resources",
        "Progress Tracking"
    ])
    
    with tabs[0]:
        st.write("#### Program Management")
        
        # New Program
        with st.expander("Create New Program", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.text_input("Program Name", key="prog_name")
                st.selectbox("Program Type",
                           ["Crop Management", "Financial Literacy",
                            "Market Access", "Technology Adoption"],
                           key="prog_type")
                st.number_input("Duration (weeks)",
                              min_value=1, max_value=12, value=4,
                              key="prog_duration")
            
            with col2:
                st.multiselect("Target Audience",
                             ["New Farmers", "Experienced Farmers",
                              "Youth Farmers", "Women Farmers"],
                             key="prog_audience")
                st.number_input("Maximum Participants",
                              min_value=5, max_value=50, value=20,
                              key="prog_max_participants")
                st.text_area("Program Description", key="prog_desc")
            
            if st.button("Create Program", key="create_program"):
                st.success("Program created successfully!")
        
        # Active Programs
        st.write("##### Active Programs")
        programs = pd.DataFrame({
            'Program': [
                'Advanced Crop Management',
                'Financial Planning',
                'Digital Farming',
                'Market Access Strategies',
                'Sustainable Practices'
            ],
            'Participants': [25, 30, 20, 35, 40],
            'Progress': ['Week 3/8', 'Week 2/6', 'Week 4/4',
                        'Week 1/6', 'Week 2/4'],
            'Status': ['On Track', 'On Track', 'Completing',
                      'Starting', 'On Track']
        })
        
        for _, program in programs.iterrows():
            with st.expander(f"{program['Program']} ({program['Status']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"Participants: {program['Participants']}")
                    st.write(f"Progress: {program['Progress']}")
                with col2:
                    st.button("View Details",
                             key=f"view_prog_{program['Program']}")
                    st.button("Manage Sessions",
                             key=f"sessions_{program['Program']}")
    
    with tabs[1]:
        st.write("#### Session Planning")
        
        # New Session
        with st.expander("Plan New Session"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.selectbox("Select Program",
                           programs['Program'].tolist(),
                           key="session_program")
                st.date_input("Session Date", key="session_date")
                st.time_input("Session Time", key="session_time")
            
            with col2:
                st.text_input("Topic", key="session_topic")
                st.selectbox("Session Type",
                           ["Classroom", "Field Demo", "Workshop",
                            "Discussion"],
                           key="session_type")
                st.text_area("Session Objectives", key="session_objectives")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.number_input("Duration (hours)",
                              min_value=1, max_value=8, value=2,
                              key="session_duration")
            with col2:
                st.text_input("Venue", key="session_venue")
            with col3:
                st.selectbox("Language",
                           ["English", "Swahili", "Mixed"],
                           key="session_language")
            
            st.multiselect("Required Materials",
                          ["Handouts", "Projector", "Demo Materials",
                           "Farm Tools", "Samples"],
                          key="session_materials")
            
            if st.button("Schedule Session", key="schedule_session"):
                st.success("Session scheduled successfully!")
        
        # Upcoming Sessions
        st.write("##### Upcoming Sessions")
        sessions = pd.DataFrame({
            'Date': ['2025-10-31', '2025-11-01', '2025-11-02'],
            'Program': ['Advanced Crop Management',
                       'Financial Planning',
                       'Digital Farming'],
            'Topic': ['Pest Management',
                     'Budgeting Basics',
                     'Farm Apps Usage'],
            'Participants': [25, 30, 20]
        })
        st.dataframe(sessions)
    
    with tabs[2]:
        st.write("#### Training Resources")
        
        # Resource Categories
        resource_types = [
            "Training Manuals",
            "Presentation Slides",
            "Video Content",
            "Assessment Tools",
            "Handouts"
        ]
        
        selected_type = st.selectbox("Resource Type",
                                   resource_types,
                                   key="resource_type")
        
        # Resource Library
        st.write("##### Available Resources")
        resources = pd.DataFrame({
            'Title': [
                'Crop Management Guide',
                'Financial Planning Templates',
                'Digital Tools Tutorial',
                'Market Analysis Framework',
                'Sustainable Farming Guide'
            ],
            'Type': [
                'Manual',
                'Template',
                'Video',
                'Template',
                'Manual'
            ],
            'Language': [
                'English/Swahili',
                'English',
                'English',
                'Swahili',
                'English/Swahili'
            ],
            'Last Updated': [
                '2025-10-15',
                '2025-10-20',
                '2025-10-25',
                '2025-10-28',
                '2025-10-30'
            ]
        })
        
        for _, resource in resources.iterrows():
            with st.expander(f"{resource['Title']} ({resource['Type']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"Language: {resource['Language']}")
                    st.write(f"Last Updated: {resource['Last Updated']}")
                with col2:
                    st.button("Preview",
                             key=f"preview_{resource['Title']}")
                    st.button("Download",
                             key=f"download_{resource['Title']}")
        
        # Upload New Resource
        with st.expander("Upload New Resource"):
            st.text_input("Resource Title", key="new_resource_title")
            st.selectbox("Resource Type",
                        resource_types,
                        key="new_resource_type")
            st.multiselect("Languages",
                          ["English", "Swahili"],
                          key="new_resource_lang")
            st.file_uploader("Upload File",
                            key="new_resource_file")
            st.text_area("Description", key="new_resource_desc")
            
            if st.button("Upload Resource", key="upload_resource"):
                st.success("Resource uploaded successfully!")
    
    with tabs[3]:
        st.write("#### Progress Tracking")
        
        # Program Selection
        selected_program = st.selectbox(
            "Select Program",
            programs['Program'].tolist(),
            key="track_program"
        )
        
        # Progress Overview
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Attendance Rate", "88%", "+2%")
        with col2:
            st.metric("Assessment Score", "85%", "+5%")
        with col3:
            st.metric("Practical Score", "90%", "+3%")
        
        # Participant Progress
        st.write("##### Participant Progress")
        progress = pd.DataFrame({
            'Participant': ['John Doe', 'Jane Smith', 'Mike Johnson'],
            'Attendance': ['5/6', '6/6', '4/6'],
            'Assessments': ['85%', '90%', '82%'],
            'Practical': ['88%', '92%', '85%'],
            'Status': ['On Track', 'Excellent', 'Needs Support']
        })
        st.dataframe(progress)
        
        # Progress Charts
        col1, col2 = st.columns(2)
        
        with col1:
            attendance_data = pd.DataFrame({
                'Session': range(1, 7),
                'Attendance': [25, 23, 24, 22, 25, 24]
            })
            fig = px.line(attendance_data,
                         x='Session',
                         y='Attendance',
                         title='Attendance Trend')
            st.plotly_chart(fig)
        
        with col2:
            performance_data = pd.DataFrame({
                'Assessment': ['Quiz 1', 'Quiz 2', 'Practical',
                             'Final'],
                'Score': [80, 85, 90, 88]
            })
            fig = px.bar(performance_data,
                        x='Assessment',
                        y='Score',
                        title='Assessment Scores')
            st.plotly_chart(fig)
        
        # Training Impact
        st.write("##### Training Impact")
        impact_metrics = pd.DataFrame({
            'Metric': [
                'Knowledge Improvement',
                'Skill Application',
                'Productivity Increase',
                'Technology Adoption'
            ],
            'Pre-Training': [60, 55, 50, 45],
            'Post-Training': [85, 80, 75, 70]
        })
        
        fig = px.bar(impact_metrics,
                    x='Metric',
                    y=['Pre-Training', 'Post-Training'],
                    title='Training Impact Analysis',
                    barmode='group')
        st.plotly_chart(fig)

if __name__ == "__main__":
    render()