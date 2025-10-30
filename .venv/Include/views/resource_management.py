import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def render():
    """Render the Resource Management Dashboard."""
    
    st.subheader("Resource Management")
    
    # Create tabs for different sections
    tabs = st.tabs(["Inventory Management", "Equipment", "Labor", "Water Resources"])
    
    with tabs[0]:
        st.subheader("Inventory Management")
        
        # Add New Inventory Item
        with st.expander("Add New Inventory Item"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                item_type = st.selectbox("Item Type", [
                    "Seeds", "Fertilizer", "Pesticide", "Herbicide",
                    "Tools", "Packaging", "Other"
                ])
                item_name = st.text_input("Item Name")
                quantity = st.number_input("Quantity", 0.0, 10000.0)
                
            with col2:
                unit = st.selectbox("Unit", [
                    "kg", "liters", "pieces", "bags", "boxes"
                ])
                unit_cost = st.number_input("Unit Cost (KES)", 0.0)
                supplier = st.text_input("Supplier")
                
            with col3:
                purchase_date = st.date_input("Purchase Date")
                expiry_date = st.date_input("Expiry Date")
                storage_location = st.text_input("Storage Location")
                
            if st.button("Add Item"):
                st.success("Inventory item added successfully!")
        
        # Inventory Overview
        st.write("#### Current Inventory")
        
        # Sample inventory data - replace with database data
        inventory_df = pd.DataFrame({
            'Item_Type': ['Seeds', 'Fertilizer', 'Pesticide', 'Tools'],
            'Item_Name': ['Maize Seed', 'DAP', 'Insecticide', 'Sprayer'],
            'Quantity': [50, 200, 10, 2],
            'Unit': ['kg', 'kg', 'liters', 'pieces'],
            'Value': [25000, 40000, 8000, 6000]
        })
        
        # Inventory summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Items", len(inventory_df))
        with col2:
            st.metric("Total Value", f"KES {inventory_df['Value'].sum():,.2f}")
        with col3:
            st.metric("Low Stock Items", len(inventory_df[inventory_df['Quantity'] < 10]))
        
        # Inventory visualization
        fig = px.pie(inventory_df, values='Value', names='Item_Type',
                    title='Inventory Value Distribution')
        st.plotly_chart(fig, width="stretch")
        
        # Detailed inventory table
        st.write("#### Inventory Details")
        st.dataframe(inventory_df)
        
    with tabs[1]:
        st.subheader("Equipment Management")
        
        # Add New Equipment
        with st.expander("Add New Equipment"):
            col1, col2 = st.columns(2)
            
            with col1:
                equipment_name = st.text_input("Equipment Name")
                equipment_type = st.selectbox("Equipment Type", [
                    "Tractor", "Plough", "Harrow", "Planter",
                    "Sprayer", "Harvester", "Other"
                ])
                manufacturer = st.text_input("Manufacturer")
                model = st.text_input("Model")
                
            with col2:
                purchase_date = st.date_input("Purchase Date", key="equip_date")
                purchase_cost = st.number_input("Purchase Cost (KES)")
                condition = st.select_slider("Condition",
                    options=["Poor", "Fair", "Good", "Excellent"])
                status = st.selectbox("Status", [
                    "Operational", "Under Maintenance", "Out of Service"
                ])
                
            if st.button("Add Equipment"):
                st.success("Equipment added successfully!")
        
        # Equipment Overview
        st.write("#### Equipment Status")
        
        # Sample equipment data - replace with database data
        equipment_df = pd.DataFrame({
            'Equipment': ['Tractor', 'Plough', 'Sprayer', 'Planter'],
            'Status': ['Operational', 'Under Maintenance', 'Operational', 'Operational'],
            'Last_Service': ['2025-09-15', '2025-10-25', '2025-10-01', '2025-08-30'],
            'Next_Service': ['2025-12-15', '2025-11-25', '2025-12-01', '2025-11-30'],
            'Usage_Hours': [1200, 800, 400, 300]
        })
        
        # Equipment status summary
        status_counts = equipment_df['Status'].value_counts()
        fig = px.bar(status_counts, title='Equipment Status Overview')
        st.plotly_chart(fig, width="stretch")
        
        # Equipment maintenance calendar
        st.write("#### Maintenance Schedule")
        
        # Convert dates to datetime
        equipment_df['Next_Service'] = pd.to_datetime(equipment_df['Next_Service'])
        
        # Sort by next service date
        maintenance_schedule = equipment_df.sort_values('Next_Service')
        
        for _, equip in maintenance_schedule.iterrows():
            days_until = (equip['Next_Service'] - pd.Timestamp.now()).days
            status_color = 'red' if days_until < 7 else 'orange' if days_until < 14 else 'green'
            
            st.markdown(
                f"<div style='padding:10px;border-left:5px solid {status_color};margin:10px 0;'>"
                f"<strong>{equip['Equipment']}</strong><br>"
                f"Next Service: {equip['Next_Service'].strftime('%Y-%m-%d')} ({days_until} days)<br>"
                f"Current Status: {equip['Status']}"
                "</div>",
                unsafe_allow_html=True
            )
            
    with tabs[2]:
        st.subheader("Labor Management")
        
        # Add New Worker
        with st.expander("Add New Worker"):
            col1, col2 = st.columns(2)
            
            with col1:
                worker_name = st.text_input("Worker Name")
                id_number = st.text_input("ID Number")
                phone = st.text_input("Phone Number")
                work_type = st.selectbox("Work Type", [
                    "Permanent", "Seasonal", "Casual"
                ])
                
            with col2:
                skills = st.multiselect("Skills", [
                    "Planting", "Spraying", "Harvesting",
                    "Machine Operation", "Supervision"
                ])
                daily_rate = st.number_input("Daily Rate (KES)")
                start_date = st.date_input("Start Date")
                
            if st.button("Add Worker"):
                st.success("Worker added successfully!")
        
        # Labor Overview
        st.write("#### Workforce Summary")
        
        # Sample labor data - replace with database data
        labor_df = pd.DataFrame({
            'Worker_Type': ['Permanent', 'Seasonal', 'Casual'],
            'Count': [5, 8, 12],
            'Avg_Daily_Rate': [800, 600, 500],
            'Total_Cost': [120000, 144000, 180000]
        })
        
        # Workforce metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Workers", labor_df['Count'].sum())
        with col2:
            st.metric("Monthly Labor Cost", f"KES {labor_df['Total_Cost'].sum():,.2f}")
        with col3:
            st.metric("Avg Daily Rate", f"KES {labor_df['Avg_Daily_Rate'].mean():,.2f}")
        
        # Workforce visualization
        fig = px.bar(labor_df, x='Worker_Type', y=['Count'],
                    title='Workforce Distribution')
        st.plotly_chart(fig, width="stretch")
        
        # Labor cost analysis
        fig = px.pie(labor_df, values='Total_Cost', names='Worker_Type',
                    title='Labor Cost Distribution')
        st.plotly_chart(fig, width="stretch")
        
    with tabs[3]:
        st.subheader("Water Resource Management")
        
        # Water Source Management
        st.write("#### Water Sources")
        
        col1, col2 = st.columns(2)
        
        with col1:
            water_source = st.selectbox("Primary Water Source", [
                "Borehole", "River", "Rain Water", "Municipal"
            ])
            source_capacity = st.number_input("Source Capacity (m³/day)", 0.0)
            
        with col2:
            water_quality = st.select_slider("Water Quality",
                options=["Poor", "Fair", "Good", "Excellent"])
            ph_level = st.slider("pH Level", 0.0, 14.0, 7.0)
        
        # Water Usage Tracking
        st.write("#### Water Usage Monitoring")
        
        # Sample water usage data - replace with database data
        water_usage = pd.DataFrame({
            'Date': pd.date_range(start='2025-01-01', periods=10, freq='M'),
            'Usage_m3': [120, 150, 180, 200, 220, 180, 150, 130, 140, 160],
            'Rainfall_mm': [50, 60, 100, 120, 80, 40, 30, 45, 70, 90]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=water_usage['Date'],
            y=water_usage['Usage_m3'],
            name='Water Usage (m³)'
        ))
        fig.add_trace(go.Bar(
            x=water_usage['Date'],
            y=water_usage['Rainfall_mm'],
            name='Rainfall (mm)',
            yaxis='y2'
        ))
        
        fig.update_layout(
            title='Water Usage vs Rainfall',
            yaxis=dict(title='Water Usage (m³)'),
            yaxis2=dict(title='Rainfall (mm)', overlaying='y', side='right')
        )
        st.plotly_chart(fig, width="stretch")
        
        # Irrigation Planning
        st.write("#### Irrigation Schedule")
        
        # Sample irrigation schedule - replace with actual planning data
        irrigation_schedule = pd.DataFrame({
            'Field': ['Maize Field 1', 'Beans Field 2', 'Potatoes Field 3'],
            'Area_Acres': [2.5, 1.5, 1.0],
            'Water_Need_m3': [25, 15, 20],
            'Next_Irrigation': ['2025-10-31', '2025-11-01', '2025-10-30'],
            'Duration_Hrs': [3, 2, 2.5]
        })
        
        st.dataframe(irrigation_schedule)

if __name__ == "__main__":
    render()