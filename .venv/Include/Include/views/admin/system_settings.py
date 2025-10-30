import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def render():
    """Render the System Settings Dashboard."""
    
    st.subheader("System Settings")
    
    # System Status
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("System Status", "Healthy", "Normal")
    with col2:
        st.metric("Response Time", "120ms", "-10ms")
    with col3:
        st.metric("Error Rate", "0.1%", "-0.05%")
    with col4:
        st.metric("Uptime", "99.99%", "+0.01%")
    
    # Settings Tabs
    tabs = st.tabs([
        "General Settings",
        "Security Settings",
        "Integration Settings",
        "Notification Settings"
    ])
    
    with tabs[0]:
        st.write("#### General Settings")
        
        # Application Settings
        with st.expander("Application Settings", expanded=True):
            st.selectbox("Default Language", ["English", "Swahili", "French"])
            st.selectbox("Timezone", ["UTC", "Africa/Nairobi", "Africa/Lagos"])
            st.number_input("Session Timeout (minutes)", value=30)
            st.selectbox("Date Format", ["YYYY-MM-DD", "DD-MM-YYYY", "MM/DD/YYYY"])
            
            col1, col2 = st.columns(2)
            with col1:
                st.checkbox("Enable Maintenance Mode")
            with col2:
                st.checkbox("Enable Debug Mode")
        
        # Data Management
        with st.expander("Data Management"):
            st.number_input("Data Retention Period (days)", value=365)
            st.number_input("Max Upload Size (MB)", value=10)
            st.selectbox("Default Export Format", ["CSV", "Excel", "JSON"])
            
            col1, col2 = st.columns(2)
            with col1:
                st.checkbox("Auto Backup Enabled")
            with col2:
                st.checkbox("Compress Exports")
    
    with tabs[1]:
        st.write("#### Security Settings")
        
        # Password Policy
        with st.expander("Password Policy", expanded=True):
            st.number_input("Minimum Password Length", value=8)
            st.checkbox("Require Special Characters")
            st.checkbox("Require Numbers")
            st.checkbox("Require Uppercase Letters")
            st.number_input("Password Expiry (days)", value=90)
            st.number_input("Failed Login Attempts", value=5)
        
        # Authentication Settings
        with st.expander("Authentication Settings"):
            st.checkbox("Enable Two-Factor Authentication")
            st.checkbox("Enable SSO")
            st.selectbox("SSO Provider", ["None", "Google", "Microsoft", "Custom"])
            st.text_input("SSO Client ID")
            st.text_input("SSO Client Secret", type="password")
        
        # API Security
        with st.expander("API Security"):
            st.checkbox("Enable API Rate Limiting")
            st.number_input("Rate Limit (requests/minute)", value=100)
            st.text_input("API Key")
            st.button("Generate New API Key")
    
    with tabs[2]:
        st.write("#### Integration Settings")
        
        # Database Configuration
        with st.expander("Database Configuration", expanded=True):
            st.text_input("Database Host")
            st.text_input("Database Name")
            st.text_input("Database User")
            st.text_input("Database Password", type="password")
            st.number_input("Connection Pool Size", value=10)
            st.button("Test Connection")
        
        # External Services
        with st.expander("External Services"):
            # SMS Gateway
            st.write("##### SMS Gateway")
            st.selectbox("SMS Provider", ["AfricasTalking", "Twilio", "Custom"])
            st.text_input("SMS API Key")
            st.text_input("SMS Sender ID")
            
            # Payment Gateway
            st.write("##### Payment Gateway")
            st.selectbox("Payment Provider", ["M-Pesa", "Stripe", "PayPal"])
            st.text_input("Payment API Key")
            st.text_input("Payment Secret", type="password")
            
            # Weather API
            st.write("##### Weather API")
            st.text_input("Weather API Key")
            st.selectbox("Update Frequency", ["Hourly", "Daily", "Weekly"])
    
    with tabs[3]:
        st.write("#### Notification Settings")
        
        # Email Notifications
        with st.expander("Email Notifications", expanded=True):
            st.text_input("SMTP Server")
            st.text_input("SMTP Port")
            st.text_input("SMTP Username")
            st.text_input("SMTP Password", type="password")
            st.text_input("From Email")
            st.checkbox("Enable SSL")
            
            st.write("##### Notification Templates")
            templates = [
                "Welcome Email",
                "Password Reset",
                "Account Verification",
                "Order Confirmation",
                "Payment Receipt"
            ]
            for template in templates:
                with st.expander(template):
                    st.text_area("Subject", key=f"email_{template}_subject")
                    st.text_area("Body", key=f"email_{template}_body")
                    st.selectbox("Language", ["English", "Swahili", "French"], key=f"email_{template}_lang")
        
        # SMS Notifications
        with st.expander("SMS Notifications"):
            st.checkbox("Enable SMS Notifications")
            st.number_input("Daily SMS Limit", value=1000)
            
            st.write("##### SMS Templates")
            sms_templates = [
                "Welcome Message",
                "OTP Verification",
                "Order Update",
                "Payment Reminder"
            ]
            for template in sms_templates:
                with st.expander(template):
                    st.text_area("Message Template", key=f"sms_{template}_message")
                    st.number_input("Max Length", value=160, key=f"sms_{template}_length")
        
        # Push Notifications
        with st.expander("Push Notifications"):
            st.checkbox("Enable Push Notifications")
            st.text_input("Firebase Server Key")
            st.number_input("Notification TTL (hours)", value=24)
            
            # Notification Categories
            categories = [
                "System Updates",
                "Security Alerts",
                "User Activities",
                "Market Updates"
            ]
            for category in categories:
                st.checkbox(f"Enable {category}")
        
        if st.button("Save Settings"):
            st.success("Settings saved successfully!")

if __name__ == "__main__":
    render()