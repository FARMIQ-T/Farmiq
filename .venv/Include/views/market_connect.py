import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def render():
    """Render the Market Connect Dashboard."""
    
    st.subheader("Market Connect")
    
    # Create tabs for different sections
    tabs = st.tabs(["Market Overview", "Sales Management", "Buyer Network", "Price Analytics"])
    
    with tabs[0]:
        st.subheader("Market Overview")
        
        # Market Summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Active Buyers", "15", "+3")
            st.metric("Open Orders", "5", "+2")
        with col2:
            st.metric("Avg Daily Sales", "KES 25,000", "+15%")
            st.metric("Pending Deliveries", "3", "-1")
        with col3:
            st.metric("Market Rating", "4.8/5.0", "+0.2")
            st.metric("Payment Time", "2.5 days", "-0.5 days")
        
        # Market Price Trends
        st.write("#### Current Market Prices")
        
        # Sample market prices - replace with API/database data
        market_prices = pd.DataFrame({
            'Crop': ['Maize', 'Beans', 'Potatoes', 'Tomatoes'],
            'Current_Price': [45, 120, 35, 80],
            'Change': [2, -5, 3, 8],
            'Market_Demand': ['High', 'Medium', 'High', 'Medium']
        })
        
        for _, crop in market_prices.iterrows():
            change_color = 'green' if crop['Change'] > 0 else 'red'
            st.markdown(
                f"<div style='padding:10px;border-left:5px solid {change_color};margin:10px 0;'>"
                f"<strong>{crop['Crop']}</strong><br>"
                f"Price: KES {crop['Current_Price']}/kg ({crop['Change']:+d})<br>"
                f"Demand: {crop['Market_Demand']}"
                "</div>",
                unsafe_allow_html=True
            )
        
        # Price Trends
        st.write("#### Price Trends")
        
        selected_crop = st.selectbox(
            "Select Crop",
            market_prices['Crop'].tolist()
        )
        
        # Sample historical prices - replace with database data
        price_history = pd.DataFrame({
            'Date': pd.date_range(start='2025-01-01', periods=10, freq='M'),
            'Price': [42, 44, 43, 45, 46, 44, 45, 47, 46, 45],
            'Volume_Traded': [1000, 1200, 900, 1100, 1300, 1100, 1000, 1200, 1100, 1000]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=price_history['Date'],
            y=price_history['Price'],
            name='Price (KES/kg)'
        ))
        fig.add_trace(go.Bar(
            x=price_history['Date'],
            y=price_history['Volume_Traded'],
            name='Volume Traded (kg)',
            yaxis='y2'
        ))
        
        fig.update_layout(
            title=f'{selected_crop} Price Trend',
            yaxis2=dict(title='Volume (kg)', overlaying='y', side='right')
        )
        st.plotly_chart(fig, width="stretch")
        
    with tabs[1]:
        st.subheader("Sales Management")
        
        # Add New Sale
        with st.expander("Record New Sale"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                crop = st.selectbox("Crop", market_prices['Crop'].tolist())
                quantity = st.number_input("Quantity (kg)", 0.0)
                unit_price = st.number_input("Unit Price (KES/kg)", 0.0)
                
            with col2:
                buyer = st.selectbox("Buyer", [
                    "Farmer's Market", "ABC Wholesalers",
                    "XYZ Distributors", "Local Vendor"
                ])
                sale_date = st.date_input("Sale Date")
                payment_terms = st.selectbox("Payment Terms", [
                    "Cash on Delivery", "7 Days", "14 Days", "30 Days"
                ])
                
            with col3:
                quality_grade = st.selectbox("Quality Grade", ["A", "B", "C"])
                delivery_method = st.selectbox(
                    "Delivery Method",
                    ["Buyer Pickup", "Farm Delivery", "Market Delivery"]
                )
                
            if st.button("Record Sale"):
                st.success("Sale recorded successfully!")
        
        # Sales History
        st.write("#### Recent Sales")
        
        # Sample sales data - replace with database data
        sales_history = pd.DataFrame({
            'Date': ['2025-10-25', '2025-10-23', '2025-10-20'],
            'Crop': ['Maize', 'Beans', 'Potatoes'],
            'Quantity': [1000, 500, 2000],
            'Unit_Price': [45, 120, 35],
            'Total_Amount': [45000, 60000, 70000],
            'Buyer': ['ABC Wholesalers', 'XYZ Distributors', 'Local Vendor'],
            'Status': ['Delivered', 'Pending', 'Completed']
        })
        
        st.dataframe(sales_history)
        
        # Sales Analytics
        st.write("#### Sales Analytics")
        
        # Sales by crop
        sales_by_crop = pd.DataFrame({
            'Crop': market_prices['Crop'].tolist(),
            'Sales_Volume': [5000, 2000, 8000, 3000],
            'Sales_Value': [225000, 240000, 280000, 240000]
        })
        
        fig = px.bar(sales_by_crop,
                    x='Crop', y=['Sales_Volume', 'Sales_Value'],
                    title='Sales by Crop',
                    barmode='group')
        st.plotly_chart(fig, width="stretch")
        
    with tabs[2]:
        st.subheader("Buyer Network")
        
        # Add New Buyer
        with st.expander("Add New Buyer"):
            col1, col2 = st.columns(2)
            
            with col1:
                buyer_name = st.text_input("Buyer Name")
                contact_person = st.text_input("Contact Person")
                phone = st.text_input("Phone Number")
                email = st.text_input("Email")
                
            with col2:
                buyer_type = st.selectbox("Buyer Type", [
                    "Wholesaler", "Retailer", "Processor",
                    "Exporter", "Individual"
                ])
                preferred_crops = st.multiselect(
                    "Preferred Crops",
                    market_prices['Crop'].tolist()
                )
                payment_method = st.multiselect(
                    "Payment Methods",
                    ["Cash", "Bank Transfer", "Mobile Money"]
                )
                
            if st.button("Add Buyer"):
                st.success("Buyer added successfully!")
        
        # Buyer Directory
        st.write("#### Buyer Directory")
        
        # Sample buyer data - replace with database data
        buyers = pd.DataFrame({
            'Buyer': ['ABC Wholesalers', 'XYZ Distributors', 'Local Vendor'],
            'Type': ['Wholesaler', 'Distributor', 'Retailer'],
            'Preferred_Crops': ['Maize, Beans', 'Potatoes', 'All Crops'],
            'Total_Purchases': [250000, 180000, 120000],
            'Rating': [4.8, 4.5, 4.7]
        })
        
        for _, buyer in buyers.iterrows():
            with st.expander(f"{buyer['Buyer']} - {buyer['Type']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"Preferred Crops: {buyer['Preferred_Crops']}")
                    st.write(f"Total Purchases: KES {buyer['Total_Purchases']:,.2f}")
                with col2:
                    st.write(f"Rating: {buyer['Rating']}/5.0")
                    st.progress(buyer['Rating']/5.0)
        
    with tabs[3]:
        st.subheader("Price Analytics")
        
        # Price Comparison
        st.write("#### Market Price Comparison")
        
        # Sample market comparison data - replace with API/database data
        market_comparison = pd.DataFrame({
            'Market': ['Local Market', 'Regional Market', 'National Average'],
            'Maize': [45, 48, 46],
            'Beans': [120, 125, 118],
            'Potatoes': [35, 38, 36],
            'Tomatoes': [80, 85, 82]
        })
        
        fig = px.bar(market_comparison.melt(id_vars=['Market'], var_name='Crop', value_name='Price'),
                    x='Crop', y='Price', color='Market',
                    title='Price Comparison Across Markets',
                    barmode='group')
        st.plotly_chart(fig, width="stretch")
        
        # Price Forecasting
        st.write("#### Price Forecast")
        
        forecast_crop = st.selectbox("Select Crop for Forecast",
                                   market_prices['Crop'].tolist(),
                                   key='forecast')
        
        # Sample forecast data - replace with ML predictions
        forecast_data = pd.DataFrame({
            'Date': pd.date_range(start='2025-11-01', periods=12, freq='M'),
            'Price_Forecast': [46, 47, 48, 46, 45, 44, 45, 47, 48, 49, 48, 47],
            'Lower_Bound': [44, 45, 46, 44, 43, 42, 43, 45, 46, 47, 46, 45],
            'Upper_Bound': [48, 49, 50, 48, 47, 46, 47, 49, 50, 51, 50, 49]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=forecast_data['Date'],
            y=forecast_data['Price_Forecast'],
            name='Price Forecast',
            line=dict(color='blue')
        ))
        fig.add_trace(go.Scatter(
            x=forecast_data['Date'],
            y=forecast_data['Upper_Bound'],
            fill=None,
            name='Upper Bound',
            line=dict(color='rgba(0,100,255,0.2)')
        ))
        fig.add_trace(go.Scatter(
            x=forecast_data['Date'],
            y=forecast_data['Lower_Bound'],
            fill='tonexty',
            name='Lower Bound',
            line=dict(color='rgba(0,100,255,0.2)')
        ))
        fig.update_layout(title=f'{forecast_crop} Price Forecast (Next 12 Months)')
        st.plotly_chart(fig, width="stretch")
        
        # Market Insights
        st.write("#### Market Insights")
        
        # Sample insights - replace with AI-generated insights
        insights = [
            "Maize prices expected to rise 5% in next month due to reduced supply",
            "Increased demand for potatoes in regional markets",
            "New export opportunity identified for grade A beans",
            "Seasonal price drop expected for tomatoes in 2 months"
        ]
        
        for insight in insights:
            st.info(insight)

if __name__ == "__main__":
    render()