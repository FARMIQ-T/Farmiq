import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def render():
    """Render the FAQ Management Dashboard."""
    
    st.subheader("FAQ Management")
    
    # FAQ Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total FAQs", "125", "+5")
    with col2:
        st.metric("Categories", "8", "+1")
    with col3:
        st.metric("Most Viewed", "Login Issues", "↑")
    with col4:
        st.metric("Search Success", "92%", "+2%")
    
    # FAQ Management Tabs
    tabs = st.tabs([
        "FAQ Editor",
        "Category Management",
        "Search Analytics",
        "User Feedback"
    ])
    
    with tabs[0]:
        st.write("#### FAQ Editor")
        
        # Add/Edit FAQ
        with st.expander("Add/Edit FAQ", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.text_input("Question", key="faq_question")
                st.selectbox("Category",
                           ["Account Management",
                            "Technical Support",
                            "Billing",
                            "Services",
                            "Security",
                            "Mobile App",
                            "Troubleshooting",
                            "General"],
                           key="faq_category")
            with col2:
                st.text_area("Answer", height=150, key="faq_answer")
                st.multiselect("Tags",
                             ["Login", "Password", "Account",
                              "Payment", "Technical", "Mobile",
                              "Security", "Profile"],
                             key="faq_tags")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.selectbox("Status",
                           ["Published", "Draft", "Under Review"],
                           key="faq_status")
            with col2:
                st.selectbox("Priority",
                           ["High", "Medium", "Low"],
                           key="faq_priority")
            with col3:
                st.number_input("Display Order",
                              min_value=1,
                              max_value=100,
                              value=1,
                              key="faq_order")
            
            if st.button("Save FAQ", key="save_faq"):
                st.success("FAQ saved successfully!")
        
        # FAQ List
        st.write("##### FAQ List")
        faqs = pd.DataFrame({
            'Question': [
                'How do I reset my password?',
                'Where can I view my transactions?',
                'How do I update my profile?'
            ],
            'Category': [
                'Account Management',
                'Technical Support',
                'Account Management'
            ],
            'Status': ['Published', 'Published', 'Draft'],
            'Views': [150, 120, 80]
        })
        
        for _, faq in faqs.iterrows():
            with st.expander(f"{faq['Question']} ({faq['Category']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"Status: {faq['Status']}")
                    st.write(f"Views: {faq['Views']}")
                with col2:
                    st.button("Edit",
                             key=f"edit_{faq['Question']}")
                    st.button("Delete",
                             key=f"delete_{faq['Question']}")
    
    with tabs[1]:
        st.write("#### Category Management")
        
        # Add Category
        with st.expander("Add Category", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.text_input("Category Name", key="category_name")
                st.text_area("Description", key="category_desc")
            with col2:
                st.number_input("Display Order",
                              min_value=1,
                              max_value=10,
                              value=1,
                              key="category_order")
                st.selectbox("Status",
                           ["Active", "Inactive"],
                           key="category_status")
            
            if st.button("Add Category", key="add_category"):
                st.success("Category added successfully!")
        
        # Category List
        st.write("##### Categories")
        categories = pd.DataFrame({
            'Category': [
                'Account Management',
                'Technical Support',
                'Billing',
                'Services'
            ],
            'FAQs': [25, 30, 20, 15],
            'Views': [500, 450, 300, 250],
            'Status': ['Active', 'Active', 'Active', 'Inactive']
        })
        st.dataframe(categories)
        
        # Category Analytics
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(categories,
                        names='Category',
                        values='FAQs',
                        title='FAQs by Category')
            st.plotly_chart(fig)
        
        with col2:
            fig = px.bar(categories,
                        x='Category',
                        y='Views',
                        title='Views by Category')
            st.plotly_chart(fig)
    
    with tabs[2]:
        st.write("#### Search Analytics")
        
        # Search Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Searches", "1,250", "+50")
        with col2:
            st.metric("Success Rate", "85%", "+3%")
        with col3:
            st.metric("Avg Search Time", "1.2s", "-0.1s")
        
        # Search Trends
        search_data = pd.DataFrame({
            'Date': pd.date_range(start='2025-10-01',
                                periods=30,
                                freq='D'),
            'Searches': range(100, 130),
            'Success': range(85, 115)
        })
        
        fig = px.line(search_data,
                     x='Date',
                     y=['Searches', 'Success'],
                     title='Search Trends')
        st.plotly_chart(fig)
        
        # Popular Searches
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("##### Top Searches")
            top_searches = pd.DataFrame({
                'Term': [
                    'password reset',
                    'login error',
                    'payment failed',
                    'account locked'
                ],
                'Count': [50, 45, 40, 35]
            })
            st.dataframe(top_searches)
        
        with col2:
            st.write("##### Failed Searches")
            failed_searches = pd.DataFrame({
                'Term': [
                    'mobile app download',
                    'refund policy',
                    'contact support',
                    'subscription'
                ],
                'Count': [20, 18, 15, 12]
            })
            st.dataframe(failed_searches)
    
    with tabs[3]:
        st.write("#### User Feedback")
        
        # Feedback Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Rating", "4.5/5.0", "+0.2")
        with col2:
            st.metric("Helpful Rate", "92%", "+3%")
        with col3:
            st.metric("Total Ratings", "850", "+25")
        
        # Recent Feedback
        st.write("##### Recent Feedback")
        feedback = pd.DataFrame({
            'Date': ['2025-10-30', '2025-10-29', '2025-10-28'],
            'FAQ': [
                'How do I reset my password?',
                'Where can I view my transactions?',
                'How do I update my profile?'
            ],
            'Rating': [5, 4, 5],
            'Comment': [
                'Very helpful!',
                'Could be clearer',
                'Solved my issue'
            ]
        })
        
        for _, item in feedback.iterrows():
            with st.expander(f"{item['FAQ']} - {item['Rating']}/5"):
                st.write(f"Date: {item['Date']}")
                st.write(f"Comment: {item['Comment']}")
                col1, col2 = st.columns(2)
                with col1:
                    st.button("Mark as Reviewed",
                             key=f"review_{item['FAQ']}")
                with col2:
                    st.button("Send Response",
                             key=f"respond_{item['FAQ']}")
        
        # Feedback Analysis
        col1, col2 = st.columns(2)
        
        with col1:
            rating_dist = pd.DataFrame({
                'Rating': ['5 stars', '4 stars', '3 stars',
                          '2 stars', '1 star'],
                'Count': [500, 200, 100, 30, 20]
            })
            fig = px.pie(rating_dist,
                        names='Rating',
                        values='Count',
                        title='Rating Distribution')
            st.plotly_chart(fig)
        
        with col2:
            feedback_trend = pd.DataFrame({
                'Week': pd.date_range(start='2025-09-01',
                                    periods=8,
                                    freq='W'),
                'Rating': [4.3, 4.4, 4.5, 4.5, 4.6, 4.6, 4.7, 4.5]
            })
            fig = px.line(feedback_trend,
                         x='Week',
                         y='Rating',
                         title='Rating Trend')
            st.plotly_chart(fig)

if __name__ == "__main__":
    render()