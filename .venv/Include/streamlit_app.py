import streamlit as st
import os
import importlib.util
import sys
import traceback
from dotenv import load_dotenv
from supabase import create_client, Client
import pandas as pd
from datetime import datetime
from services.database_service import DatabaseService

# Load environment variables
load_dotenv()

# Initialize Supabase client and database service
def init_services():
    """Initialize Supabase client and database service with caching using Streamlit session state"""
    if 'supabase' not in st.session_state or 'db_service' not in st.session_state:
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY')
        if not url or not key:
            st.error("Missing Supabase credentials. Please check .env file")
            st.stop()
        
        st.session_state.supabase = create_client(url, key)
        st.session_state.db_service = DatabaseService(url, key)
    
    return st.session_state.supabase, st.session_state.db_service

def get_or_create_anonymous_user():
    """Get existing anonymous session or create new one"""
    supabase, _ = init_services()
    
    if 'anon_user' not in st.session_state:
        try:
            response = supabase.auth.sign_in_anonymously()
            st.session_state.anon_user = response.user
        except Exception as e:
            st.error(f"Error creating anonymous session: {str(e)}")
            return None
    
    return st.session_state.anon_user


# --- PAGE SETUP ---
current_dir = os.path.dirname(os.path.abspath(__file__))

# --- UI Branding / page config ---
st.set_page_config(page_title="🌽👩‍🌾Farm IQ", layout="wide")
logo_path = os.path.join(current_dir, 'assets', 'logo.png')
if os.path.exists(logo_path):
    # show small logo in the sidebar if available
    st.sidebar.image(logo_path, width="stretch")  # Updated to use new width parameter

st.sidebar.title("🌽👩‍🌾 Farm IQ Dashboard")

# Initialize services
if 'supabase' not in st.session_state or 'db_service' not in st.session_state:
    init_services()

# Ensure anonymous user session
user = get_or_create_anonymous_user()
if not user:
    st.error("Failed to initialize user session")
    st.stop()

# Display user session info in sidebar
st.sidebar.success(f"Session ID: {user.id[:8]}...")

# --- NAVIGATION SETUP [WITH SECTIONS] ---
# Define each page as a tuple: (relative_module_path, title, icon)
pages = {
    "Farmer Apps": {
        "Farm Profile": ("views/farm_profile.py", "Farm Profile Management", "👨‍🌾"),
        "Credit Score": ("views/credit_dashboard.py", "Credit Score Dashboard", "📊"),
        "Crop Planning": ("views/crop_planning.py", "Crop Planning & Monitoring", "🌱"),
        "Resources": ("views/resource_management.py", "Resource Management", "🚜"),
        "Financial": ("views/financial_management.py", "Financial Management", "💰"),
        "Market": ("views/market_connect.py", "Market Connect", "🏪")
    },
    "Agent Apps": {
        "Dashboard": ("views/agent/dashboard.py", "Agent Dashboard", "📊"),
        "Farmer Mgmt": ("views/agent/farmer_management.py", "Farmer Management", "👥"),
        "Field Visits": ("views/agent/field_visits.py", "Field Visits", "🚗"),
        "Training": ("views/agent/training_programs.py", "Training Programs", "📚"),
        "Reports": ("views/agent/reports.py", "Agent Reports", "📝")
    },
    "Support Apps": {
        "Tickets": ("views/support/ticket_management.py", "Ticket Management", "🎫"),
        "Knowledge": ("views/support/knowledge_base.py", "Knowledge Base", "📚"),
        "Chat": ("views/support/live_chat.py", "Live Chat Support", "💬"),
        "FAQ": ("views/support/faq_management.py", "FAQ Management", "❓"),
        "Reports": ("views/support/support_reports.py", "Support Reports", "📊")
    },
    "Admin Apps": {
        "Users": ("views/admin/user_management.py", "User Management", "👥"),
        "System": ("views/admin/system_settings.py", "System Settings", "⚙️"),
        "Analytics": ("views/admin/analytics.py", "Analytics & Reports", "📈"),
        "Data": ("views/admin/data_management.py", "Data Management", "💾"),
        "Audit": ("views/admin/audit_logs.py", "Audit Logs", "📋")
    }
}

# --- NAVIGATION ---
section = st.sidebar.selectbox("Select Apps", list(pages.keys()))
page_name = st.sidebar.radio("Choose App", list(pages[section].keys()))
module_rel_path, page_title, page_icon = pages[section][page_name]

st.sidebar.markdown("Made with Precision")

st.title(page_title)

# Ensure services are available in session state for other modules
if 'supabase' not in st.session_state or 'db_service' not in st.session_state:
    init_services()

# Build absolute path to the selected page and execute it.
module_path = os.path.join(current_dir, module_rel_path)
if not os.path.exists(module_path):
    st.error(f"Page not found: {module_path}")
else:
    try:
        # Import the page module from its file path and prefer calling its
        # render() function if present. This is safer than executing the
        # module with runpy because it supports testing and clearer error
        # handling.
        module_name = os.path.splitext(os.path.basename(module_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        # Ensure the include directory is on sys.path so relative imports work
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        spec.loader.exec_module(module)

        if hasattr(module, "render"):
            module.render()
        else:
            st.warning("The page module does not expose a render() function; the module was imported but nothing was rendered.")
    except Exception:
        st.error("An error occurred while loading the page. See details below.")
        st.text(traceback.format_exc())



    