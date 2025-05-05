import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import pandas as pd

# Function to get AQI from AQICN API
def get_aqi(city, api_token):
    url = f"http://api.waqi.info/feed/{city}/?token={api_token}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        if data.get("status") == "ok":
            aqi = data.get("data", {}).get("aqi")
            if aqi is not None:
                return aqi
            else:
                st.error("AQI value not found in response")
                return None
        else:
            st.error(f"API Error: {data.get('data', {}).get('message', 'Unknown error')}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"API Request Failed: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected Error: {str(e)}")
        return None

# Function to get AQI color based on value
def get_aqi_color(aqi):
    if aqi is not None:
        if aqi <= 50:
            return "green"  # Good
        elif aqi <= 100:
            return "yellow"  # Moderate
        elif aqi <= 150:
            return "orange"  # Unhealthy for Sensitive Groups
        elif aqi <= 200:
            return "red"  # Unhealthy
        elif aqi <= 300:
            return "purple"  # Very Unhealthy
        else:
            return "maroon"  # Hazardous
    return "gray"  # Default if aqi is None

st.title("Indian City AQI Dashboard")

# User input for city
city = st.text_input("Enter an Indian city name or specific location (e.g., Delhi, Major Dhyan Chand National Stadium, Delhi, Delhi, India):", value="Delhi")

# Load API token from secrets
API_TOKEN = st.secrets["AQICN_TOKEN"]

# City coordinates (simplified for major cities and specific locations)
city_coords = {
    "Delhi": [28.6139, 77.2090],
    "Major Dhyan Chand National Stadium, Delhi, Delhi, India": [28.6139, 77.2090],
    "Mumbai": [19.0760, 72.8777],
    "Bangalore": [12.9716, 77.5946],
    "Chennai": [13.0827, 80.2707],
    "Kolkata": [22.5726, 88.3639],
    "Pune": [18.5204, 73.8567],
    "Hyderabad": [17.3850, 78.4867],
    "Ahmedabad": [23.0225, 72.5714]
}

if city:
    # Fetch AQI
    aqi = get_aqi(city, API_TOKEN)
    if aqi is not None:
        st.write(f"The AQI for {city} is: **{aqi}**")
        if aqi <= 50:
            st.success("Good: Air quality is satisfactory.")
        elif aqi <= 100:
            st.info("Moderate: Air quality is acceptable.")
        elif aqi <= 150:
            st.warning("Unhealthy for Sensitive Groups.")
        elif aqi <= 200:
            st.error("Unhealthy: Everyone may experience health effects.")
        elif aqi <= 300:
            st.error("Very Unhealthy: Health alert.")
        else:
            st.error("Hazardous: Health warning of emergency conditions.")

        # Create map centered on India
        m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

        # Check for coordinates
        if city in city_coords:
            coords = city_coords[city]
        elif city.lower().capitalize() in city_coords:
            coords = city_coords[city.lower().capitalize()]
        else:
            st.warning(f"Map coordinates for {city} not available. Showing AQI data only.")
            coords = None

        # Add marker if coordinates are available
        if coords:
            folium.CircleMarker(
                location=coords,
                radius=10,
                popup=f"{city}: AQI {aqi}",
                color=get_aqi_color(aqi),
                fill=True,
                fill_color=get_aqi_color(aqi)
            ).add_to(m)

            # Display map with explicit return
            map_output = st_folium(m, width=700, height=500, key=f"map_{city}")
            if not map_output:
                st.warning("Map did not render. Please try refreshing the page or updating your browser.")
    else:
        st.error("Could not fetch AQI data. Check city name or try again later.")

st.markdown("""
### About AQI
The Air Quality Index (AQI) measures air pollution levels. Lower values mean better air quality, while higher values indicate greater health risks.
""")