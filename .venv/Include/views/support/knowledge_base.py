import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def render():
    """Render the Knowledge Base Dashboard."""
    
    st.subheader("Knowledge Base")
    
    # Knowledge Base Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Articles", "250", "+10")
    with col2:
        st.metric("Categories", "15", "+2")
    with col3:
        st.metric("Avg. Rating", "4.6/5.0", "+0.2")
    with col4:
        st.metric("Monthly Views", "1,500", "+200")
    
    # Knowledge Base Tabs
    tabs = st.tabs([
        "Article Management",
        "Categories",
        "Search Analytics",
        "User Feedback"
    ])
    
    with tabs[0]:
        st.write("#### Article Management")
        
        # New Article
        with st.expander("Create New Article", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                st.text_input("Title", key="article_title")
                st.selectbox("Category",
                           ["Getting Started", "Account Management",
                            "Technical Support", "Billing",
                            "Best Practices"],
                           key="article_category")
                st.multiselect("Tags",
                             ["Login", "Password", "Payment",
                              "Security", "Features"],
                             key="article_tags")
            
            with col2:
                st.selectbox("Status",
                           ["Draft", "Review", "Published"],
                           key="article_status")
                st.text_area("Summary", key="article_summary")
            
            st.text_area("Content", height=200, key="article_content")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.selectbox("Language",
                           ["English", "Swahili"],
                           key="article_language")
            with col2:
                st.multiselect("Related Articles",
                              ["Article 1", "Article 2", "Article 3"],
                              key="related_articles")
            with col3:
                st.file_uploader("Attachments",
                               accept_multiple_files=True,
                               key="article_attachments")
            
            if st.button("Save Article", key="save_article"):
                st.success("Article saved successfully!")
        
        # Article List
        st.write("##### Published Articles")
        articles = pd.DataFrame({
            'Title': [
                'Getting Started Guide',
                'Password Reset Guide',
                'Payment Methods',
                'Common Issues'
            ],
            'Category': [
                'Getting Started',
                'Account Management',
                'Billing',
                'Technical Support'
            ],
            'Views': [500, 300, 250, 450],
            'Rating': [4.8, 4.6, 4.5, 4.7],
            'Last Updated': [
                '2025-10-30',
                '2025-10-25',
                '2025-10-20',
                '2025-10-15'
            ]
        })
        
        for _, article in articles.iterrows():
            with st.expander(f"{article['Title']} ({article['Category']})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"Views: {article['Views']}")
                    st.write(f"Rating: {article['Rating']}/5.0")
                    st.write(f"Last Updated: {article['Last Updated']}")
                with col2:
                    st.button("Edit",
                             key=f"edit_{article['Title']}")
                    st.button("Archive",
                             key=f"archive_{article['Title']}")
    
    with tabs[1]:
        st.write("#### Category Management")
        
        # Category Overview
        categories = pd.DataFrame({
            'Category': [
                'Getting Started',
                'Account Management',
                'Technical Support',
                'Billing',
                'Best Practices'
            ],
            'Articles': [50, 40, 60, 30, 70],
            'Views': [2500, 2000, 3000, 1500, 3500]
        })
        
        fig = px.bar(categories,
                    x='Category',
                    y=['Articles', 'Views'],
                    title='Category Statistics',
                    barmode='group')
        st.plotly_chart(fig)
        
        # Category Management
        col1, col2 = st.columns(2)
        
        with col1:
            # Add Category
            st.write("##### Add Category")
            st.text_input("Category Name", key="new_category")
            st.text_area("Description", key="category_desc")
            st.selectbox("Parent Category",
                        ["None"] + categories['Category'].tolist(),
                        key="parent_category")
            if st.button("Add Category", key="add_category"):
                st.success("Category added successfully!")
        
        with col2:
            # Category Details
            st.write("##### Category Details")
            selected_category = st.selectbox(
                "Select Category",
                categories['Category'].tolist(),
                key="select_category"
            )
            st.metric("Total Articles",
                     str(categories[
                         categories['Category'] == selected_category
                     ]['Articles'].values[0]))
            st.metric("Total Views",
                     str(categories[
                         categories['Category'] == selected_category
                     ]['Views'].values[0]))
    
    with tabs[2]:
        st.write("#### Search Analytics")
        
        # Search Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Searches", "2,500", "+300")
        with col2:
            st.metric("Success Rate", "85%", "+5%")
        with col3:
            st.metric("Avg. Search Time", "2.5s", "-0.3s")
        
        # Popular Searches
        st.write("##### Popular Search Terms")
        searches = pd.DataFrame({
            'Term': [
                'password reset',
                'login issues',
                'payment methods',
                'account setup'
            ],
            'Searches': [250, 200, 180, 150],
            'Success_Rate': [90, 85, 88, 92]
        })
        
        fig = px.bar(searches,
                    x='Term',
                    y=['Searches', 'Success_Rate'],
                    title='Top Search Terms',
                    barmode='group')
        st.plotly_chart(fig)
        
        # Search Patterns
        st.write("##### Search Patterns")
        patterns = pd.DataFrame({
            'Hour': range(24),
            'Searches': [
                50, 30, 20, 10, 5, 15, 45, 80, 120, 150,
                140, 130, 145, 135, 120, 110, 100, 90,
                85, 70, 60, 55, 40, 35
            ]
        })
        
        fig = px.line(patterns, x='Hour', y='Searches',
                     title='Search Volume by Hour')
        st.plotly_chart(fig)
        
        # Failed Searches
        st.write("##### Failed Searches")
        failed = pd.DataFrame({
            'Term': [
                'advanced settings',
                'mobile app download',
                'api documentation',
                'pricing plans'
            ],
            'Searches': [50, 45, 40, 35],
            'Last_Search': [
                '2025-10-30',
                '2025-10-29',
                '2025-10-28',
                '2025-10-27'
            ]
        })
        st.dataframe(failed)
    
    with tabs[3]:
        st.write("#### User Feedback")
        
        # Feedback Overview
        col1, col2 = st.columns(2)
        
        with col1:
            ratings = pd.DataFrame({
                'Rating': [5, 4, 3, 2, 1],
                'Count': [500, 300, 100, 50, 25]
            })
            fig = px.pie(ratings, names='Rating', values='Count',
                        title='Article Ratings Distribution')
            st.plotly_chart(fig)
        
        with col2:
            feedback_metrics = pd.DataFrame({
                'Metric': ['Helpful', 'Clear', 'Complete', 'Up-to-date'],
                'Score': [4.8, 4.6, 4.5, 4.7]
            })
            fig = px.bar(feedback_metrics, x='Metric', y='Score',
                        title='Feedback Metrics')
            st.plotly_chart(fig)
        
        # Recent Feedback
        st.write("##### Recent Feedback")
        feedback = pd.DataFrame({
            'Article': [
                'Getting Started Guide',
                'Password Reset Guide',
                'Payment Methods'
            ],
            'Rating': [5, 4, 5],
            'Comment': [
                'Very helpful and clear',
                'Good but could use more screenshots',
                'Excellent instructions'
            ],
            'Date': [
                '2025-10-30',
                '2025-10-29',
                '2025-10-28'
            ]
        })
        
        for _, item in feedback.iterrows():
            with st.expander(f"{item['Article']} - {item['Rating']}/5.0"):
                st.write(f"Comment: {item['Comment']}")
                st.write(f"Date: {item['Date']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.button("Reply",
                             key=f"reply_{item['Article']}")
                with col2:
                    st.button("Flag for Review",
                             key=f"flag_{item['Article']}")

if __name__ == "__main__":
    render()