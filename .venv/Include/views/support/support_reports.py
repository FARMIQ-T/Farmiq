import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def render():
    """Render the Support Reports Dashboard."""
    
    st.subheader("Support Reports")
    
    # Report Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Resolution Rate", "95%", "+2%")
    with col2:
        st.metric("Avg Response Time", "2.5h", "-0.5h")
    with col3:
        st.metric("Customer Satisfaction", "4.8/5.0", "+0.1")
    with col4:
        st.metric("Active Tickets", "45", "-5")
    
    # Support Reports Tabs
    tabs = st.tabs([
        "Performance Metrics",
        "Ticket Analysis",
        "Agent Reports",
        "Custom Reports"
    ])
    
    with tabs[0]:
        st.write("#### Performance Metrics")
        
        # Time Period Selection
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Time Period",
                        ["Today", "This Week", "This Month",
                         "Last Month", "Custom"],
                        key="perf_period")
        with col2:
            st.multiselect("Metrics",
                          ["Resolution Time",
                           "Response Time",
                           "Customer Satisfaction",
                           "Ticket Volume"],
                          default=["Resolution Time",
                                 "Response Time"],
                          key="selected_metrics")
        
        # Performance Trends
        perf_data = pd.DataFrame({
            'Date': pd.date_range(start='2025-10-01',
                                periods=30,
                                freq='D'),
            'Resolution_Time': range(150, 120, -1),
            'Response_Time': range(60, 30, -1),
            'Satisfaction': [4.5 + x*0.01 for x in range(30)],
            'Volume': range(50, 80)
        })
        
        fig = px.line(perf_data,
                     x='Date',
                     y=['Resolution_Time', 'Response_Time'],
                     title='Support Performance Trends')
        st.plotly_chart(fig)
        
        # Key Statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("First Response", "15m", "-2m")
            st.metric("Resolution Time", "2.5h", "-0.5h")
        with col2:
            st.metric("SLA Compliance", "98%", "+1%")
            st.metric("First Contact Resolution", "85%", "+3%")
        with col3:
            st.metric("Escalation Rate", "5%", "-1%")
            st.metric("Reopened Tickets", "3%", "-0.5%")
    
    with tabs[1]:
        st.write("#### Ticket Analysis")
        
        # Ticket Distribution
        col1, col2 = st.columns(2)
        
        with col1:
            category_dist = pd.DataFrame({
                'Category': [
                    'Technical',
                    'Account',
                    'Billing',
                    'Product',
                    'General'
                ],
                'Count': [250, 200, 150, 100, 50]
            })
            fig = px.pie(category_dist,
                        names='Category',
                        values='Count',
                        title='Tickets by Category')
            st.plotly_chart(fig)
        
        with col2:
            priority_dist = pd.DataFrame({
                'Priority': ['High', 'Medium', 'Low'],
                'Count': [100, 350, 300]
            })
            fig = px.bar(priority_dist,
                        x='Priority',
                        y='Count',
                        title='Tickets by Priority')
            st.plotly_chart(fig)
        
        # Resolution Analysis
        resolution_data = pd.DataFrame({
            'Method': [
                'Self Service',
                'Agent Assistance',
                'Technical Team',
                'Escalation'
            ],
            'Percentage': [40, 35, 15, 10]
        })
        fig = px.pie(resolution_data,
                    names='Method',
                    values='Percentage',
                    title='Resolution Methods')
        st.plotly_chart(fig)
        
        # Ticket Timeline
        timeline_data = pd.DataFrame({
            'Hour': range(24),
            'Volume': [
                5, 2, 1, 1, 2, 5, 10, 20, 35, 45,
                40, 35, 38, 40, 35, 30, 25, 20,
                15, 12, 10, 8, 6, 4
            ]
        })
        fig = px.line(timeline_data,
                     x='Hour',
                     y='Volume',
                     title='Ticket Volume by Hour')
        st.plotly_chart(fig)
    
    with tabs[2]:
        st.write("#### Agent Reports")
        
        # Agent Performance
        agent_perf = pd.DataFrame({
            'Agent': ['Alice', 'Bob', 'Charlie', 'David'],
            'Tickets': [120, 115, 105, 95],
            'Avg_Response': ['10m', '12m', '15m', '11m'],
            'Resolution_Rate': [96, 94, 92, 95],
            'CSAT': [4.8, 4.7, 4.6, 4.7]
        })
        st.dataframe(agent_perf)
        
        # Agent Metrics
        col1, col2 = st.columns(2)
        
        with col1:
            workload = pd.DataFrame({
                'Agent': ['Alice', 'Bob', 'Charlie', 'David'],
                'Active': [12, 10, 8, 15]
            })
            fig = px.bar(workload,
                        x='Agent',
                        y='Active',
                        title='Current Workload')
            st.plotly_chart(fig)
        
        with col2:
            ratings = pd.DataFrame({
                'Agent': ['Alice', 'Bob', 'Charlie', 'David'],
                'Rating': [4.8, 4.7, 4.6, 4.7]
            })
            fig = px.bar(ratings,
                        x='Agent',
                        y='Rating',
                        title='Customer Satisfaction Ratings')
            st.plotly_chart(fig)
        
        # Specialization Analysis
        specialization = pd.DataFrame({
            'Category': [
                'Technical',
                'Account',
                'Billing',
                'Product'
            ],
            'Alice': [40, 20, 20, 20],
            'Bob': [20, 40, 20, 20],
            'Charlie': [20, 20, 40, 20],
            'David': [20, 20, 20, 40]
        })
        fig = px.bar(specialization,
                    x='Category',
                    y=['Alice', 'Bob', 'Charlie', 'David'],
                    title='Agent Specializations',
                    barmode='group')
        st.plotly_chart(fig)
    
    with tabs[3]:
        st.write("#### Custom Reports")
        
        # Report Builder
        with st.expander("Report Builder", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.multiselect(
                    "Select Metrics",
                    ["Resolution Time",
                     "Response Time",
                     "Customer Satisfaction",
                     "Ticket Volume",
                     "Agent Performance",
                     "Category Distribution"],
                    key="report_metrics"
                )
                st.selectbox(
                    "Time Range",
                    ["Last 7 Days",
                     "Last 30 Days",
                     "Last 90 Days",
                     "Custom"],
                    key="report_range"
                )
            
            with col2:
                st.multiselect(
                    "Group By",
                    ["Agent",
                     "Category",
                     "Priority",
                     "Status"],
                    key="report_group"
                )
                st.selectbox(
                    "Report Format",
                    ["PDF", "Excel", "CSV"],
                    key="report_format"
                )
            
            if st.button("Generate Report"):
                st.info("Generating custom report...")
        
        # Saved Reports
        st.write("##### Saved Reports")
        saved_reports = pd.DataFrame({
            'Name': [
                'Monthly Performance',
                'Agent Productivity',
                'Customer Satisfaction',
                'SLA Compliance'
            ],
            'Schedule': [
                'Monthly',
                'Weekly',
                'Daily',
                'Weekly'
            ],
            'Last Run': [
                '2025-10-30',
                '2025-10-29',
                '2025-10-30',
                '2025-10-29'
            ]
        })
        
        for _, report in saved_reports.iterrows():
            with st.expander(
                f"{report['Name']} ({report['Schedule']})"):
                st.write(f"Last Run: {report['Last Run']}")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.button("Run Now",
                             key=f"run_{report['Name']}")
                with col2:
                    st.button("Schedule",
                             key=f"schedule_{report['Name']}")
                with col3:
                    st.button("Download",
                             key=f"download_{report['Name']}")

if __name__ == "__main__":
    render()