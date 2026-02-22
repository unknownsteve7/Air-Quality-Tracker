import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="Global Air Quality & Weather Tracker",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    /* Ensure text is readable */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
    }
    .footer {
        text-align: center;
        padding: 20px;
        color: #666;
    }
    </style>
    """, unsafe_allow_html=True)

def load_data():
    conn = sqlite3.connect('weather_history.db')
    query = "SELECT * FROM city_metrics"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def get_aqi_color(aqi_label):
    colors = {
        "Good": "#28a745",
        "Fair": "#ffc107",
        "Moderate": "#fd7e14",
        "Poor": "#dc3545",
        "Very Poor": "#721c24"
    }
    return colors.get(aqi_label, "#6c757d")

def main():
    st.title("Global Air Quality & Weather Insights")
    st.markdown("---")

    try:
        df = load_data()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.info("Make sure you've run the pipeline first to populate the database.")
        return

    st.sidebar.header("Navigation")
    city_list = df['city'].unique()
    selected_city = st.sidebar.selectbox("Select a City", city_list)
    
    city_data = df[df['city'] == selected_city].iloc[0]

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Temperature", f"{city_data['main.temp']:.1f}°C")
    with col2:
        st.metric("Humidity", f"{city_data['main.humidity']}%")
    with col3:
        aqi_label = city_data['air_quality_index']
        st.metric("Air Quality", aqi_label)
    with col4:
        st.metric("AQI Score", int(city_data['main.aqi']))

    st.markdown("---")

    left_col, right_col = st.columns([2, 1])

    with left_col:
        st.subheader("City Locations & Air Quality")
        map_df = df.copy()
        map_df.rename(columns={'coord.lat': 'lat', 'coord.lon': 'lon'}, inplace=True)
        
        fig_map = px.scatter_mapbox(
            map_df, 
            lat="lat", 
            lon="lon", 
            hover_name="city", 
            hover_data=["main.temp", "air_quality_index"],
            color="main.aqi",
            color_continuous_scale=px.colors.sequential.Reds,
            size=[15]*len(map_df),
            zoom=3, 
            height=500
        )
        fig_map.update_layout(mapbox_style="carto-positron")
        fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig_map, use_container_width=True)

    with right_col:
        st.subheader("Health Insights")
        aqi = city_data['air_quality_index']
        
        recommendations = {
            "Good": "Air quality is satisfactory. Feel free to enjoy outdoor activities.",
            "Fair": "Air quality is acceptable; however, some pollutants may affect sensitive individuals.",
            "Moderate": "Sensitive groups should reduce prolonged outdoor exertion.",
            "Poor": "Everyone may begin to experience health effects. Plan indoor activities.",
            "Very Poor": "Health alert: everyone may experience more serious health effects. Stay indoors!"
        }
        
        st.info(recommendations.get(aqi, "No recommendation available."))
        
        st.write("**Pollutant Breakdown:**")
        pollutants = {
            "PM2.5": city_data['components.pm2_5'],
            "PM10": city_data['components.pm10'],
            "CO": city_data['components.co'],
            "O3": city_data['components.o3']
        }
        for p, val in pollutants.items():
            st.write(f"- **{p}:** {val:.2f} µg/m³")

    st.markdown("---")
    
    st.subheader("Comparative Analysis")
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        fig_temp = px.bar(
            df, 
            x='city', 
            y='main.temp', 
            title="Temperature Comparison (°C)",
            color='main.temp',
            color_continuous_scale='Bluered'
        )
        st.plotly_chart(fig_temp, use_container_width=True)

    with chart_col2:
        fig_aqi = px.bar(
            df, 
            x='city', 
            y='main.aqi', 
            title="AQI Score Comparison (Higher is worse)",
            color='air_quality_index',
            color_discrete_map={
                "Good": "#28a745", "Fair": "#ffc107", 
                "Moderate": "#fd7e14", "Poor": "#dc3545", "Very Poor": "#721c24"
            }
        )
        st.plotly_chart(fig_aqi, use_container_width=True)

    st.markdown("---")
    data_time = city_data['dt_x']
    st.markdown(f"<div class='footer'>Data last captured by API: {data_time} | Dashboard View Refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
