# Import libraries
import streamlit as st
import requests

# Function to get AQI data from AQICN
def get_aqi(city, api_token):
    # Create the API URL with city and token
    url = f"http://api.waqi.info/feed/{city}/?token={api_token}"
    try:
        # Send a request to the API
        response = requests.get(url)
        # Convert the response to a Python dictionary
        data = response.json()
        # Check if the API call was successful
        if data["status"] == "ok":
            return data["data"]["aqi"]  # Return the AQI value
        else:
            return None  # Return None if the city isn't found
    except:
        return None  # Return None if there's an error (e.g., no internet)

# Main Streamlit app
st.title("Indian City AQI Dashboard")  # Set the page title

# Create a text box for the user to enter a city
city = st.text_input("Enter an Indian city name (e.g., Delhi, Mumbai):")

# Your AQICN API token (replace with the token you got)
API_TOKEN = "9194074afb7a02d71d038fa2a8120c7350946d04"

# Check if the user entered a city
if city:
    # Call the get_aqi function to fetch AQI
    aqi = get_aqi(city, API_TOKEN)
    if aqi is not None:
        # Display the AQI value
        st.write(f"The AQI for {city} is: **{aqi}**")
        # Categorize the AQI based on standard ranges
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
    else:
        # Show an error if AQI data couldn't be fetched
        st.error("Could not fetch AQI data. Check city name or try again later.")

# Add some information about AQI
st.markdown("""
### About AQI
The Air Quality Index (AQI) measures air pollution levels. Lower values mean better air quality, while higher values indicate greater health risks.
""")