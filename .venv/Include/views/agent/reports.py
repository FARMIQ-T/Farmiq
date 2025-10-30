import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def render():
    """Render the Agent Reports Dashboard."""
    
    st.subheader("Agent Reports")
    
    # Performance Overview
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Farmer Visits", "125/150", "83%")
    with col2:
        st.metric("Training Sessions", "35/40", "88%")
    with col3:
        st.metric("Success Rate", "92%", "+2%")
    with col4:
        st.metric("Satisfaction", "4.8/5.0", "+0.1")
    
    # Report Tabs
    tabs = st.tabs([
        "Performance Reports",
        "Activity Reports",
        "Impact Reports",
        "Custom Reports"
    ])
    
    with tabs[0]:
        st.write("#### Performance Reports")
        
        # Time Period Selection
        col1, col2 = st.columns(2)
        with col1:
            report_period = st.selectbox(
                "Report Period",
                ["Daily", "Weekly", "Monthly", "Quarterly", "Custom"],
                key="perf_period"
            )
        with col2:
            if report_period == "Custom":
                st.date_input("Select Date Range", key="perf_date_range")
        
        # Key Performance Indicators
        st.write("##### Key Performance Indicators")
        kpis = pd.DataFrame({
            'Metric': [
                'Farmer Visits',
                'Training Sessions',
                'Loan Applications',
                'Issue Resolution',
                'Documentation'
            ],
            'Target': [150, 40, 30, 50, 100],
            'Achieved': [125, 35, 28, 48, 95],
            'Status': ['On Track', 'On Track', 'Needs Focus',
                      'Excellent', 'On Track']
        })
        
        # Calculate completion percentages
        kpis['Completion'] = (kpis['Achieved'] / kpis['Target'] * 100).round(1)
        
        # Display KPIs with progress bars
        for _, kpi in kpis.iterrows():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{kpi['Metric']}**")
                st.progress(float(kpi['Completion']) / 100)
            with col2:
                st.write(f"{kpi['Achieved']}/{kpi['Target']}")
                st.write(f"Status: {kpi['Status']}")
        
        # Performance Trends
        st.write("##### Performance Trends")
        trends_data = pd.DataFrame({
            'Date': pd.date_range(start='2025-10-01', end='2025-10-30', freq='D'),
            'Visits': range(3, 33),
            'Success_Rate': [90 + i/10 for i in range(30)]
        })
        
        fig = px.line(trends_data, x='Date', y=['Visits', 'Success_Rate'],
                     title='Daily Performance Metrics')
        st.plotly_chart(fig)
    
    with tabs[1]:
        st.write("#### Activity Reports")
        
        # Activity Summary
        activities = pd.DataFrame({
            'Category': [
                'Farm Visits',
                'Training Sessions',
                'Loan Processing',
                'Issue Resolution',
                'Admin Tasks'
            ],
            'Hours': [80, 40, 20, 30, 10]
        })
        
        fig = px.pie(activities, names='Category', values='Hours',
                    title='Time Allocation by Activity')
        st.plotly_chart(fig)
        
        # Detailed Activity Log
        st.write("##### Activity Log")
        activity_log = pd.DataFrame({
            'Date': ['2025-10-30', '2025-10-30', '2025-10-29'],
            'Activity': ['Farm Visit', 'Training Session', 'Loan Assessment'],
            'Location': ['Nyeri', 'Community Center', 'Kiambu'],
            'Duration': ['2 hours', '3 hours', '1 hour'],
            'Outcome': [
                'Pest control advice given',
                'Completed Module 3',
                'Application processed'
            ]
        })
        st.dataframe(activity_log)
    
    with tabs[2]:
        st.write("#### Impact Reports")
        
        # Impact Metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Farmers Supported", "125", "+15")
            st.metric("Training Completion", "92%", "+5%")
            st.metric("Loan Success Rate", "85%", "+3%")
        
        with col2:
            st.metric("Yield Improvement", "+25%", "+5%")
            st.metric("Income Growth", "+30%", "+8%")
            st.metric("Technology Adoption", "75%", "+10%")
        
        # Impact Analysis
        st.write("##### Impact Analysis")
        impact_data = pd.DataFrame({
            'Metric': [
                'Yield',
                'Income',
                'Tech Adoption',
                'Market Access',
                'Financial Literacy'
            ],
            'Before': [100, 100, 100, 100, 100],
            'After': [125, 130, 175, 150, 165]
        })
        
        fig = px.bar(impact_data, x='Metric', y=['Before', 'After'],
                    title='Before vs After Analysis',
                    barmode='group')
        st.plotly_chart(fig)
        
        # Success Stories
        st.write("##### Success Stories")
        stories = pd.DataFrame({
            'Farmer': ['John Doe', 'Jane Smith', 'Mike Johnson'],
            'Achievement': [
                'Increased yield by 40%',
                'Secured market contract',
                'Expanded farm size'
            ],
            'Impact': [
                'Income grew by 45%',
                'Revenue up by 35%',
                'Hired 3 workers'
            ]
        })
        
        for _, story in stories.iterrows():
            with st.expander(f"{story['Farmer']}'s Success Story"):
                st.write(f"Achievement: {story['Achievement']}")
                st.write(f"Impact: {story['Impact']}")
    
    with tabs[3]:
        st.write("#### Custom Reports")
        
        # Report Builder
        with st.expander("Build Custom Report", expanded=True):
            st.write("##### Report Configuration")
            
            col1, col2 = st.columns(2)
            with col1:
                st.multiselect("Select Metrics",
                             ["Farmer Visits", "Training Sessions",
                              "Loan Applications", "Success Rate",
                              "Farmer Satisfaction"],
                             key="custom_metrics")
                st.multiselect("Include Charts",
                             ["Performance Trends", "Activity Distribution",
                              "Impact Analysis", "Success Metrics"],
                             key="custom_charts")
            
            with col2:
                st.selectbox("Report Period",
                           ["Last Week", "Last Month",
                            "Last Quarter", "Custom"],
                           key="custom_period")
                st.selectbox("Report Format",
                           ["PDF", "Excel", "Word"],
                           key="custom_format")
            
            st.multiselect("Additional Sections",
                          ["Executive Summary", "Detailed Analysis",
                           "Recommendations", "Future Plans"],
                          key="custom_sections")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.checkbox("Include Raw Data", key="include_raw_data")
            with col2:
                st.checkbox("Include Visuals", key="include_visuals")
            with col3:
                st.checkbox("Auto-schedule", key="auto_schedule")
            
            if st.button("Generate Report", key="generate_custom_report"):
                st.success("Custom report generated successfully!")
        
        # Saved Reports
        st.write("##### Saved Reports")
        saved_reports = pd.DataFrame({
            'Report Name': [
                'Monthly Performance Summary',
                'Quarterly Impact Analysis',
                'Training Effectiveness Report'
            ],
            'Generated': [
                '2025-10-30',
                '2025-10-01',
                '2025-09-30'
            ],
            'Type': ['Performance', 'Impact', 'Training'],
            'Format': ['PDF', 'Excel', 'PDF']
        })
        
        for _, report in saved_reports.iterrows():
            with st.expander(
                f"{report['Report Name']} ({report['Generated']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"Type: {report['Type']}")
                    st.write(f"Format: {report['Format']}")
                with col2:
                    st.button("View",
                             key=f"view_{report['Report Name']}")
                    st.button("Download",
                             key=f"download_{report['Report Name']}")

if __name__ == "__main__":
    render()