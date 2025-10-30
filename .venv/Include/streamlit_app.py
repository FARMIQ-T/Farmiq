import streamlit as st
import os
import importlib.util
import sys
import traceback


# --- PAGE SETUP ---
current_dir = os.path.dirname(os.path.abspath(__file__))

# --- UI Branding / page config ---
st.set_page_config(page_title="🌽👩‍🌾Farm IQ", layout="wide")
logo_path = os.path.join(current_dir, 'assets', 'logo.png')
if os.path.exists(logo_path):
    # show small logo in the sidebar if available
    st.sidebar.image(logo_path, width="stretch")  # Updated to use new width parameter

st.sidebar.title("🌽👩‍🌾 Farm IQ Dashboard")

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



    