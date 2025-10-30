import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def render():
    """Render the User Management Dashboard."""
    
    st.subheader("User Management")
    
    # User Statistics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Users", "1,250", "+50")
    with col2:
        st.metric("Active Users", "980", "+35")
    with col3:
        st.metric("New Users (30d)", "75", "+15")
    with col4:
        st.metric("Verification Rate", "92%", "+2%")
    
    # User Management Tabs
    tabs = st.tabs(["User List", "User Analytics", "Role Management", "Access Logs"])
    
    with tabs[0]:
        st.write("#### User Directory")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.selectbox(
                "Status",
                ["All", "Active", "Inactive", "Pending", "Suspended"]
            )
        with col2:
            role_filter = st.selectbox(
                "Role",
                ["All", "Farmer", "Admin", "Agent", "Support"]
            )
        with col3:
            search = st.text_input("Search Users")
            
        # Sample user data - replace with database
        users = pd.DataFrame({
            'ID': range(1, 6),
            'Name': ['John Doe', 'Jane Smith', 'Mike Johnson', 'Sarah Williams', 'Tom Brown'],
            'Role': ['Farmer', 'Admin', 'Farmer', 'Agent', 'Support'],
            'Status': ['Active', 'Active', 'Inactive', 'Active', 'Active'],
            'Join_Date': ['2025-08-15', '2025-07-20', '2025-09-01', '2025-08-30', '2025-10-01'],
            'Last_Login': ['2025-10-29', '2025-10-30', '2025-09-15', '2025-10-28', '2025-10-30']
        })
        
        st.dataframe(users)
        
        # User Actions
        if st.button("Export User List"):
            st.download_button(
                "Download CSV",
                users.to_csv(index=False),
                "users.csv",
                "text/csv"
            )
    
    with tabs[1]:
        st.write("#### User Analytics")
        
        # User Growth
        date_range = pd.date_range(start='2025-05-01', end='2025-10-30', freq='M')
        growth_data = pd.DataFrame({
            'Date': date_range,
            'Users': [800, 900, 950, 1050, 1150, 1250][:len(date_range)]
        })
        
        fig = px.line(growth_data, x='Date', y='Users',
                     title='User Growth Over Time')
        st.plotly_chart(fig)
        
        # User Distribution
        col1, col2 = st.columns(2)
        
        with col1:
            role_dist = pd.DataFrame({
                'Role': ['Farmer', 'Admin', 'Agent', 'Support'],
                'Count': [1000, 25, 150, 75]
            })
            fig = px.pie(role_dist, names='Role', values='Count',
                        title='Users by Role')
            st.plotly_chart(fig)
            
        with col2:
            status_dist = pd.DataFrame({
                'Status': ['Active', 'Inactive', 'Pending', 'Suspended'],
                'Count': [980, 200, 50, 20]
            })
            fig = px.pie(status_dist, names='Status', values='Count',
                        title='Users by Status')
            st.plotly_chart(fig)
    
    with tabs[2]:
        st.write("#### Role Management")
        
        # Role List
        roles = pd.DataFrame({
            'Role': ['Admin', 'Farmer', 'Agent', 'Support'],
            'Users': [25, 1000, 150, 75],
            'Permissions': [
                'Full Access',
                'Limited Access',
                'Medium Access',
                'Support Access'
            ]
        })
        
        for _, role in roles.iterrows():
            with st.expander(f"{role['Role']} ({role['Users']} users)"):
                st.write(f"Permission Level: {role['Permissions']}")
                st.multiselect(
                    "Permissions",
                    [
                        "View Users",
                        "Edit Users",
                        "Delete Users",
                        "View Analytics",
                        "Manage Roles",
                        "Access Logs",
                        "System Settings"
                    ],
                    default=["View Users"],
                    key=f"perm_{role['Role']}"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    st.button(f"Update {role['Role']}", key=f"update_{role['Role']}")
                with col2:
                    st.button(f"Delete {role['Role']}", key=f"delete_{role['Role']}")
        
        # Add New Role
        with st.expander("Add New Role"):
            st.text_input("Role Name")
            st.multiselect(
                "Select Permissions",
                [
                    "View Users",
                    "Edit Users",
                    "Delete Users",
                    "View Analytics",
                    "Manage Roles",
                    "Access Logs",
                    "System Settings"
                ],
                key="new_role_permissions"
            )
            st.button("Create Role")
    
    with tabs[3]:
        st.write("#### Access Logs")
        
        # Log Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            st.date_input("Start Date")
        with col2:
            st.date_input("End Date")
        with col3:
            st.selectbox("Action Type",
                        ["All", "Login", "Logout", "Create", "Update", "Delete"])
        
        # Sample access logs
        logs = pd.DataFrame({
            'Timestamp': [
                '2025-10-30 10:15:00',
                '2025-10-30 10:00:00',
                '2025-10-30 09:45:00',
                '2025-10-30 09:30:00'
            ],
            'User': ['John Doe', 'Jane Smith', 'Mike Johnson', 'Sarah Williams'],
            'Action': ['Login', 'Update User', 'Delete User', 'Create User'],
            'Details': [
                'Successful login',
                'Updated user profile',
                'Deleted inactive user',
                'Created new farmer account'
            ]
        })
        
        st.dataframe(logs)

if __name__ == "__main__":
    render()