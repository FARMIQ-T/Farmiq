import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def render():
    """Render the Live Chat Support Dashboard."""
    
    st.subheader("Live Chat Support")
    
    # Chat Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Active Chats", "5", "-2")
    with col2:
        st.metric("Waiting", "3", "+1")
    with col3:
        st.metric("Avg Response", "45s", "-5s")
    with col4:
        st.metric("Satisfaction", "4.8/5.0", "+0.1")
    
    # Chat Support Tabs
    tabs = st.tabs([
        "Chat Console",
        "Queue Management",
        "Chat History",
        "Analytics"
    ])
    
    with tabs[0]:
        st.write("#### Chat Console")
        
        # Active Chats
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Chat List
            st.write("##### Active Chats")
            active_chats = pd.DataFrame({
                'User': ['John D.', 'Jane S.', 'Mike J.'],
                'Status': ['Active', 'Active', 'On Hold'],
                'Duration': ['10m', '5m', '15m']
            })
            
            for _, chat in active_chats.iterrows():
                if st.button(
                    f"{chat['User']} ({chat['Duration']})",
                    key=f"chat_{chat['User']}"
                ):
                    st.session_state.selected_chat = chat['User']
        
        with col2:
            # Chat Window
            st.write("##### Chat Window")
            
            # Chat Messages
            messages = pd.DataFrame({
                'Time': ['10:00', '10:01', '10:02'],
                'Sender': ['User', 'Agent', 'User'],
                'Message': [
                    'Hi, I need help with login',
                    'Sure, I can help. What issues are you facing?',
                    'Getting error message on login screen'
                ]
            })
            
            chat_container = st.container()
            with chat_container:
                for _, msg in messages.iterrows():
                    if msg['Sender'] == 'User':
                        st.text_area("",
                                   msg['Message'],
                                   key=f"msg_{msg['Time']}",
                                   height=50)
                    else:
                        st.text_area("",
                                   msg['Message'],
                                   key=f"reply_{msg['Time']}",
                                   height=50)
            
            # Quick Responses
            st.write("##### Quick Responses")
            quick_responses = [
                "Hi, how can I help you today?",
                "Could you please provide more details?",
                "Let me check that for you.",
                "Is there anything else I can help with?"
            ]
            
            col1, col2 = st.columns(2)
            with col1:
                selected_response = st.selectbox(
                    "Quick Response",
                    quick_responses,
                    key="quick_chat_response"
                )
            with col2:
                st.text_area("Custom Message",
                            key="custom_message",
                            height=100)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("Send Message", key="send_chat_msg")
            with col2:
                st.button("Transfer Chat", key="transfer_chat")
            with col3:
                st.button("End Chat", key="end_chat")
    
    with tabs[1]:
        st.write("#### Queue Management")
        
        # Queue Overview
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Queue Length", "3", "+1")
        with col2:
            st.metric("Avg Wait Time", "2m", "+30s")
        with col3:
            st.metric("Available Agents", "4", "-1")
        
        # Queue List
        st.write("##### Chat Queue")
        queue = pd.DataFrame({
            'Position': [1, 2, 3],
            'User': ['Alice', 'Bob', 'Charlie'],
            'Wait Time': ['1m', '2m', '3m'],
            'Topic': ['Technical', 'Billing', 'Account'],
            'Priority': ['High', 'Medium', 'Low']
        })
        
        for _, chat in queue.iterrows():
            with st.expander(
                f"#{chat['Position']} - {chat['User']} ({chat['Wait Time']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"Topic: {chat['Topic']}")
                    st.write(f"Priority: {chat['Priority']}")
                with col2:
                    st.button("Accept Chat",
                             key=f"accept_{chat['User']}")
                    st.button("Reassign",
                             key=f"reassign_{chat['User']}")
        
        # Queue Settings
        st.write("##### Queue Settings")
        col1, col2 = st.columns(2)
        with col1:
            st.number_input("Max Queue Size",
                          min_value=5,
                          max_value=50,
                          value=20,
                          key="max_queue")
            st.number_input("Max Wait Time (minutes)",
                          min_value=1,
                          max_value=30,
                          value=10,
                          key="max_wait")
        with col2:
            st.selectbox("Queue Algorithm",
                        ["First In First Out",
                         "Priority Based",
                         "Smart Routing"],
                        key="queue_algo")
            st.multiselect("Auto-assignment Rules",
                          ["Skills Based",
                           "Load Balanced",
                           "Language Match"],
                          key="assignment_rules")
    
    with tabs[2]:
        st.write("#### Chat History")
        
        # Search and Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            st.date_input("Date Range", key="chat_date")
        with col2:
            st.selectbox("Status",
                        ["All", "Completed", "Transferred", "Abandoned"],
                        key="chat_status")
        with col3:
            st.text_input("Search User", key="chat_search")
        
        # Chat History
        chat_history = pd.DataFrame({
            'Date': ['2025-10-30', '2025-10-30', '2025-10-29'],
            'User': ['John D.', 'Jane S.', 'Mike J.'],
            'Duration': ['15m', '10m', '20m'],
            'Agent': ['Alice', 'Bob', 'Charlie'],
            'Rating': [5, 4, 5],
            'Status': ['Completed', 'Transferred', 'Completed']
        })
        
        for _, chat in chat_history.iterrows():
            with st.expander(
                f"{chat['Date']} - {chat['User']} ({chat['Status']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"Agent: {chat['Agent']}")
                    st.write(f"Duration: {chat['Duration']}")
                    st.write(f"Rating: {chat['Rating']}/5.0")
                with col2:
                    st.button("View Transcript",
                             key=f"transcript_{chat['User']}")
                    st.button("Export Chat",
                             key=f"export_{chat['User']}")
    
    with tabs[3]:
        st.write("#### Chat Analytics")
        
        # Time Period Selection
        st.selectbox("Time Period",
                    ["Today", "This Week", "This Month", "Custom"],
                    key="chat_analytics_period")
        
        # Chat Volume
        chat_volume = pd.DataFrame({
            'Hour': range(24),
            'Chats': [
                10, 5, 2, 1, 1, 2, 8, 15, 25, 35,
                30, 28, 32, 35, 30, 25, 20, 18,
                15, 12, 10, 8, 5, 3
            ]
        })
        
        fig = px.line(chat_volume, x='Hour', y='Chats',
                     title='Chat Volume by Hour')
        st.plotly_chart(fig)
        
        # Performance Metrics
        col1, col2 = st.columns(2)
        
        with col1:
            # Response Time Distribution
            response_dist = pd.DataFrame({
                'Time': ['<30s', '30-60s', '1-2m', '>2m'],
                'Percentage': [45, 30, 15, 10]
            })
            fig = px.pie(response_dist,
                        names='Time',
                        values='Percentage',
                        title='Response Time Distribution')
            st.plotly_chart(fig)
        
        with col2:
            # Chat Topics
            topics = pd.DataFrame({
                'Topic': [
                    'Technical',
                    'Account',
                    'Billing',
                    'General'
                ],
                'Count': [100, 80, 60, 40]
            })
            fig = px.bar(topics, x='Topic', y='Count',
                        title='Chats by Topic')
            st.plotly_chart(fig)
        
        # Agent Performance
        st.write("##### Agent Performance")
        performance = pd.DataFrame({
            'Agent': ['Alice', 'Bob', 'Charlie', 'David'],
            'Chats': [50, 45, 48, 42],
            'Avg_Response': ['30s', '35s', '28s', '40s'],
            'Resolution_Rate': [95, 92, 94, 90],
            'Rating': [4.8, 4.7, 4.9, 4.6]
        })
        st.dataframe(performance)
        
        # Satisfaction Metrics
        st.write("##### Satisfaction Metrics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("CSAT Score", "4.7/5.0", "+0.2")
        with col2:
            st.metric("First Response", "92%", "+3%")
        with col3:
            st.metric("Resolution Rate", "95%", "+2%")

if __name__ == "__main__":
    render()