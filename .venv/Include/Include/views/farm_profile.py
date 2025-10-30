import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime

def render():
    """Render the Farm Profile Management Dashboard."""
    
    st.subheader("Farm Profile Management")
    
    # Create tabs for different sections
    tabs = st.tabs(["Basic Information", "Crop History", "Resource Tracking", "Performance Metrics"])
    
    with tabs[0]:
        st.subheader("Basic Farm Information")
        
        # Personal Information
        st.write("#### Personal Details")
        col1, col2 = st.columns(2)
        with col1:
            farmer_name = st.text_input("Farmer Name")
            phone_number = st.text_input("Phone Number")
            id_number = st.text_input("ID Number")
            
        with col2:
            location = st.text_input("Location")
            years_farming = st.number_input("Years of Farming Experience", 0, 50)
            coop_member = st.checkbox("Cooperative Member")
            
        # Farm Details
        st.write("#### Farm Details")
        col1, col2 = st.columns(2)
        with col1:
            total_acres = st.number_input("Total Farm Size (acres)", 0.1, 1000.0, 5.0)
            owned_acres = st.number_input("Owned Land (acres)", 0.0, total_acres, min(2.0, total_acres))
            leased_acres = st.number_input("Leased Land (acres)", 0.0, total_acres - owned_acres)
            
        with col2:
            soil_types = st.multiselect(
                "Soil Types",
                ["Sandy", "Clay", "Loam", "Silt", "Peat"],
                ["Loam"]
            )
            irrigation = st.selectbox(
                "Irrigation Type",
                ["Rainfed", "Drip", "Sprinkler", "Flood", "Other"]
            )
            
        # Save button for basic information
        if st.button("Save Basic Information"):
            st.success("Farm information saved successfully!")
            
    with tabs[1]:
        st.subheader("Crop History")
        
        # Current Season
        st.write("#### Current Season Crops")
        
        # Add new crop entry
        with st.expander("Add New Crop"):
            col1, col2 = st.columns(2)
            with col1:
                crop_name = st.text_input("Crop Name")
                variety = st.text_input("Variety")
                planting_date = st.date_input("Planting Date")
                acres_planted = st.number_input("Acres Planted", 0.1, total_acres)
                
            with col2:
                expected_yield = st.number_input("Expected Yield (kg/acre)", 1, 10000)
                inputs_cost = st.number_input("Input Costs (KES/acre)")
                market_price = st.number_input("Current Market Price (KES/kg)")
                
            if st.button("Add Crop"):
                st.success("Crop added successfully!")
        
        # Show current season summary
        st.write("#### Season Summary")
        
        # Sample data - replace with actual database data
        crops_df = pd.DataFrame({
            'Crop': ['Maize', 'Beans', 'Potatoes'],
            'Acres': [2.5, 1.5, 1.0],
            'Expected_Yield': [3000, 1500, 8000],
            'Market_Price': [50, 120, 40]
        })
        
        # Calculate potential revenue
        crops_df['Potential_Revenue'] = crops_df['Acres'] * crops_df['Expected_Yield'] * crops_df['Market_Price']
        
        # Plot crop distribution
        fig = px.pie(crops_df, values='Acres', names='Crop', title='Crop Distribution')
        st.plotly_chart(fig, width="stretch")
        
        # Plot potential revenue
        fig = px.bar(crops_df, x='Crop', y='Potential_Revenue', title='Potential Revenue by Crop')
        st.plotly_chart(fig, width="stretch")
        
    with tabs[2]:
        st.subheader("Resource Tracking")
        
        # Input Inventory
        st.write("#### Input Inventory")
        with st.expander("Add New Input"):
            col1, col2 = st.columns(2)
            with col1:
                input_type = st.selectbox(
                    "Input Type",
                    ["Seeds", "Fertilizer", "Pesticide", "Tools", "Other"]
                )
                input_name = st.text_input("Input Name")
                quantity = st.number_input("Quantity")
                
            with col2:
                unit_cost = st.number_input("Unit Cost (KES)")
                purchase_date = st.date_input("Purchase Date")
                supplier = st.text_input("Supplier")
                
            if st.button("Add Input"):
                st.success("Input added successfully!")
        
        # Equipment Tracking
        st.write("#### Equipment")
        with st.expander("Add Equipment"):
            col1, col2 = st.columns(2)
            with col1:
                equipment_name = st.text_input("Equipment Name")
                purchase_cost = st.number_input("Purchase Cost (KES)")
                purchase_year = st.number_input("Purchase Year", 1990, datetime.now().year)
                
            with col2:
                condition = st.select_slider(
                    "Condition",
                    options=["Poor", "Fair", "Good", "Excellent"]
                )
                maintenance_cost = st.number_input("Annual Maintenance Cost (KES)")
                
            if st.button("Add Equipment"):
                st.success("Equipment added successfully!")
                
    with tabs[3]:
        st.subheader("Performance Metrics")
        
        # Yield History
        st.write("#### Historical Yield Performance")
        
        # Sample yield history data - replace with actual database data
        yield_history = pd.DataFrame({
            'Season': ['2023 Long Rains', '2023 Short Rains', '2024 Long Rains'],
            'Maize': [2800, 2600, 3000],
            'Beans': [1400, 1600, 1500],
            'Potatoes': [7500, 8200, 8000]
        })
        
        # Plot yield trends
        fig = go.Figure()
        for crop in ['Maize', 'Beans', 'Potatoes']:
            fig.add_trace(go.Scatter(
                x=yield_history['Season'],
                y=yield_history[crop],
                name=crop
            ))
        fig.update_layout(title='Yield Trends by Crop (kg/acre)',
                         xaxis_title='Season',
                         yaxis_title='Yield (kg/acre)')
        st.plotly_chart(fig, width="stretch")
        
        # Financial Performance
        st.write("#### Financial Performance")
        
        # Sample financial data - replace with actual database data
        financial_data = pd.DataFrame({
            'Month': pd.date_range(start='2024-01-01', periods=6, freq='M'),
            'Revenue': [120000, 85000, 95000, 150000, 180000, 130000],
            'Expenses': [80000, 65000, 70000, 85000, 95000, 75000]
        })
        
        financial_data['Profit'] = financial_data['Revenue'] - financial_data['Expenses']
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=financial_data['Month'],
            y=financial_data['Revenue'],
            name='Revenue'
        ))
        fig.add_trace(go.Bar(
            x=financial_data['Month'],
            y=financial_data['Expenses'],
            name='Expenses'
        ))
        fig.add_trace(go.Scatter(
            x=financial_data['Month'],
            y=financial_data['Profit'],
            name='Profit',
            line=dict(color='green')
        ))
        fig.update_layout(title='Monthly Financial Performance',
                         barmode='group')
        st.plotly_chart(fig, width="stretch")

if __name__ == "__main__":
    render()