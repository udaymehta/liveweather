import streamlit as st
import requests


def get_weather(query, aqi="yes"):
    API_KEY = st.secrets["WEATHER_API"]
    req_url = (
        f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={query}&aqi={aqi}"
    )
    req = requests.get(req_url)
    return req.json()


def main():
    st.set_page_config(page_title="Weather App", layout="centered")

    st.title("🌤 Live Weather Dashboard")
    city = st.text_input("Enter City Name", "Pune")

    if st.button("Get Weather"):
        data = get_weather(city)

        if "error" in data:
            st.error("City not found. Please try again.")
        else:
            location = data["location"]
            current = data["current"]
            air_quality = current["air_quality"]

            col1, col2 = st.columns(2)

            with col1:
                st.subheader(
                    f"📍 {location['name']}, {location['region']}, {location['country']}"
                )
                st.text(f"Local Time: {location['localtime']}")
                st.image(
                    f"https:{current['condition']['icon']}",
                    caption=current["condition"]["text"],
                )
                st.metric(
                    "Temperature",
                    f"{current['temp_c']}°C",
                    delta=f"Feels like {current['feelslike_c']}°C",
                )
                st.metric("Humidity", f"{current['humidity']}%")
                st.metric(
                    "Wind Speed", f"{current['wind_kph']} km/h ({current['wind_dir']})"
                )

            with col2:
                st.subheader("🌍 Air Quality Index")
                st.metric("CO", f"{air_quality['co']} µg/m³")
                st.metric("NO₂", f"{air_quality['no2']} µg/m³")
                st.metric("O₃", f"{air_quality['o3']} µg/m³")
                st.metric("PM2.5", f"{air_quality['pm2_5']} µg/m³")
                st.metric("PM10", f"{air_quality['pm10']} µg/m³")
                st.text(f"US-EPA Index: {air_quality['us-epa-index']}")
                st.text(f"GB-DEFRA Index: {air_quality['gb-defra-index']}")


if __name__ == "__main__":
    main()
