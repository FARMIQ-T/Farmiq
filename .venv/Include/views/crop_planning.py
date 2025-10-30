import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import calendar

def render():
    """Render the Crop Planning & Monitoring Dashboard."""
    
    st.subheader("Crop Planning & Monitoring")
    
    # Create tabs for different sections
    tabs = st.tabs(["Season Planning", "Crop Monitoring", "Weather Insights", "Recommendations"])
    
    with tabs[0]:
        st.subheader("Season Planning")
        
        # Season Selection
        col1, col2 = st.columns(2)
        with col1:
            season_year = st.selectbox("Year", list(range(2025, 2030)))
            season_type = st.selectbox("Season", ["Long Rains", "Short Rains"])
            
        with col2:
            start_date = st.date_input("Season Start Date")
            duration_weeks = st.number_input("Season Duration (weeks)", 12, 52, 16)
            
        # Crop Planning
        st.write("#### Crop Selection and Layout")
        
        with st.expander("Add New Crop Plan"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                crop_type = st.selectbox("Crop Type", [
                    "Maize", "Beans", "Potatoes", "Tomatoes", "Cabbage",
                    "Wheat", "Rice", "Sorghum", "Green Grams", "Cowpeas"
                ])
                variety = st.text_input("Variety")
                acres = st.number_input("Acres to Plant", 0.1, 100.0, 1.0)
                
            with col2:
                planting_method = st.selectbox("Planting Method", [
                    "Direct Seeding", "Transplanting", "Seed Drilling"
                ])
                row_spacing = st.number_input("Row Spacing (cm)", 15, 200, 75)
                plant_spacing = st.number_input("Plant Spacing (cm)", 15, 200, 30)
                
            with col3:
                expected_yield = st.number_input("Expected Yield (kg/acre)", 100, 10000)
                seed_requirement = st.number_input("Seed Requirement (kg/acre)")
                estimated_cost = st.number_input("Estimated Cost (KES/acre)")
            
            if st.button("Add to Plan"):
                st.success("Crop added to season plan!")
        
        # Display Crop Calendar
        st.write("#### Crop Calendar")
        
        # Sample crop calendar data - replace with database data
        crops_calendar = pd.DataFrame({
            'Crop': ['Maize', 'Beans', 'Potatoes'],
            'Start_Week': [1, 3, 2],
            'Duration_Weeks': [16, 12, 14]
        })
        
        # Create Gantt chart
        fig = px.timeline(
            crops_calendar,
            x_start=crops_calendar['Start_Week'].apply(lambda x: start_date + timedelta(weeks=x)),
            x_end=crops_calendar.apply(lambda x: start_date + timedelta(weeks=x['Start_Week'] + x['Duration_Weeks']), axis=1),
            y='Crop',
            title='Season Crop Calendar'
        )
        st.plotly_chart(fig, width="stretch")
        
    with tabs[1]:
        st.subheader("Crop Monitoring")
        
        # Crop Selection for Monitoring
        selected_crop = st.selectbox(
            "Select Crop to Monitor",
            ["Maize Field 1", "Beans Field 2", "Potatoes Field 3"]
        )
        
        # Growth Stage Tracking
        st.write("#### Growth Stage Tracking")
        
        col1, col2 = st.columns(2)
        with col1:
            current_stage = st.select_slider(
                "Current Growth Stage",
                options=["Germination", "Vegetative", "Flowering", "Grain Filling", "Maturity"]
            )
            days_in_stage = st.number_input("Days in Current Stage", 1, 60)
            
        with col2:
            plant_health = st.select_slider(
                "Overall Plant Health",
                options=["Poor", "Fair", "Good", "Excellent"]
            )
            pest_pressure = st.select_slider(
                "Pest/Disease Pressure",
                options=["None", "Low", "Medium", "High"]
            )
        
        # Growth Metrics
        st.write("#### Growth Metrics")
        
        # Sample growth data - replace with database data
        growth_data = pd.DataFrame({
            'Week': range(1, 9),
            'Height_cm': [5, 15, 30, 50, 80, 120, 150, 180],
            'Leaf_Count': [2, 4, 8, 12, 16, 18, 20, 20],
            'Health_Score': [95, 90, 92, 88, 85, 87, 89, 90]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=growth_data['Week'],
            y=growth_data['Height_cm'],
            name='Plant Height (cm)'
        ))
        fig.add_trace(go.Scatter(
            x=growth_data['Week'],
            y=growth_data['Health_Score'],
            name='Health Score',
            yaxis='y2'
        ))
        
        fig.update_layout(
            title='Growth Progress',
            yaxis=dict(title='Height (cm)'),
            yaxis2=dict(title='Health Score', overlaying='y', side='right')
        )
        st.plotly_chart(fig, width="stretch")
        
    with tabs[2]:
        st.subheader("Weather Insights")
        
        # Weather Overview
        st.write("#### Current Weather Conditions")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Temperature", "24°C", "2°C")
            st.metric("Soil Moisture", "65%", "-5%")
        with col2:
            st.metric("Rainfall (Last 24h)", "15mm", "10mm")
            st.metric("Humidity", "75%", "5%")
        with col3:
            st.metric("Wind Speed", "12 km/h", "-3 km/h")
            st.metric("Solar Radiation", "850 W/m²", "100 W/m²")
            
        # Weather Forecast
        st.write("#### 7-Day Forecast")
        
        # Sample forecast data - replace with API data
        forecast_data = pd.DataFrame({
            'Date': pd.date_range(start=datetime.now(), periods=7, freq='D'),
            'Temp_High': [26, 25, 27, 24, 23, 25, 26],
            'Temp_Low': [16, 15, 17, 14, 13, 15, 16],
            'Rain_Chance': [10, 20, 60, 80, 40, 20, 10],
            'Wind_Speed': [10, 12, 15, 18, 14, 11, 10]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=forecast_data['Date'],
            y=forecast_data['Rain_Chance'],
            name='Rain Chance %',
            marker_color='blue'
        ))
        fig.add_trace(go.Scatter(
            x=forecast_data['Date'],
            y=forecast_data['Temp_High'],
            name='High Temp °C',
            line=dict(color='red')
        ))
        fig.add_trace(go.Scatter(
            x=forecast_data['Date'],
            y=forecast_data['Temp_Low'],
            name='Low Temp °C',
            line=dict(color='blue')
        ))
        
        fig.update_layout(title='7-Day Weather Forecast')
        st.plotly_chart(fig, width="stretch")
        
    with tabs[3]:
        st.subheader("Recommendations")
        
        # Activity Recommendations
        st.write("#### Recommended Activities")
        
        # Sample recommendations - replace with AI/rule-based recommendations
        recommendations = [
            {
                "activity": "Apply Top Dressing Fertilizer",
                "crop": "Maize Field 1",
                "urgency": "High",
                "timing": "Next 2 days",
                "details": "Apply 50kg/acre of CAN fertilizer. Weather conditions are optimal."
            },
            {
                "activity": "Pest Monitoring",
                "crop": "Beans Field 2",
                "urgency": "Medium",
                "timing": "This week",
                "details": "Check for bean fly infestation. Recent weather conditions favor pest development."
            },
            {
                "activity": "Irrigation",
                "crop": "Potatoes Field 3",
                "urgency": "Low",
                "timing": "Monitor",
                "details": "Soil moisture adequate. Monitor due to rising temperatures."
            }
        ]
        
        for rec in recommendations:
            with st.expander(f"{rec['activity']} - {rec['crop']} (Urgency: {rec['urgency']})"):
                st.write(f"**Timing:** {rec['timing']}")
                st.write(f"**Details:** {rec['details']}")
                if st.button(f"Mark Complete - {rec['activity']}", key=rec['activity']):
                    st.success(f"Marked {rec['activity']} as completed!")
        
        # Risk Alerts
        st.write("#### Risk Alerts")
        
        # Sample risk alerts - replace with AI/sensor-based alerts
        risk_alerts = pd.DataFrame({
            'Risk_Type': ['Disease', 'Weather', 'Pest'],
            'Crop': ['Maize', 'All Crops', 'Beans'],
            'Risk_Level': ['High', 'Medium', 'Low'],
            'Description': [
                'High risk of rust disease due to humidity',
                'Possible hailstorm in next 48 hours',
                'Low aphid infestation detected'
            ]
        })
        
        for _, alert in risk_alerts.iterrows():
            color = {
                'High': 'red',
                'Medium': 'orange',
                'Low': 'green'
            }[alert['Risk_Level']]
            
            st.markdown(
                f"<div style='padding:10px;border-left:5px solid {color};margin:10px 0;'>"
                f"<strong>{alert['Risk_Type']} Risk - {alert['Crop']}</strong><br>"
                f"Level: {alert['Risk_Level']}<br>"
                f"{alert['Description']}"
                "</div>",
                unsafe_allow_html=True
            )

if __name__ == "__main__":
    render()