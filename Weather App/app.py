
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

# =========================================
# PAGE CONFIG
# =========================================
st.set_page_config(
    page_title="Animated Weather Dashboard",
    page_icon="🌦",
    layout="wide"
)

# =========================================
# API KEY
# =========================================
API_KEY = "f95bee8d9588d9649e6a90466bed53cc"

# =========================================
# BASE CSS
# =========================================
st.markdown("""
<style>

/* APP BACKGROUND */
.stApp {
    background: linear-gradient(
        135deg,
        #0f2027,
        #203a43,
        #2c5364
    );
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    color: white;
}

@keyframes gradientBG {
    0% {
        background-position: 0% 50%;
    }
    50% {
        background-position: 100% 50%;
    }
    100% {
        background-position: 0% 50%;
    }
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.9);
    backdrop-filter: blur(20px);
}

/* GLASS CARD */
.glass-card {
    background: rgba(255,255,255,0.08);
    border-radius: 25px;
    padding: 25px;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

/* METRIC CARD */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 15px;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
}

/* BUTTON */
.stButton > button {
    width: 100%;
    height: 50px;
    border-radius: 15px;
    border: none;
    background: linear-gradient(
        135deg,
        #3b82f6,
        #8b5cf6
    );
    color: white;
    font-size: 18px;
    font-weight: bold;
    transition: 0.3s ease;
}

.stButton > button:hover {
    transform: scale(1.02);
    box-shadow: 0 0 20px rgba(139,92,246,0.5);
}

/* INPUT */
.stTextInput input {
    background: rgba(255,255,255,0.08);
    color: white;
    border-radius: 12px;
}

/* TITLES */
h1,h2,h3,h4 {
    color: white;
}

/* SCROLLBAR */
::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-thumb {
    background: #3b82f6;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# HEADER
# =========================================
st.markdown("""
<div class="glass-card"
style="
text-align:center;
padding:35px;
margin-bottom:20px;
">

<h1 style="
font-size:60px;
font-weight:bold;
background: linear-gradient(to right,#60a5fa,#a78bfa);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
margin-bottom:10px;
">
🌍 Weather Analytics Dashboard
</h1>

<p style="
font-size:20px;
color:#d1d5db;
">
Real-Time Forecast • Interactive Charts • Live Maps
</p>

</div>
""", unsafe_allow_html=True)

# =========================================
# SIDEBAR
# =========================================
st.sidebar.title("⚙ Weather Controls")

city = st.sidebar.text_input(
    "🏙 Enter City Name",
    "Delhi"
)

get_weather = st.sidebar.button(
    "🌦 Get Weather Analytics"
)

st.sidebar.markdown("---")

st.sidebar.info(
    "Search any city to view live weather analytics, charts, and maps."
)

# =========================================
# SESSION STATE
# =========================================
if "weather_loaded" not in st.session_state:
    st.session_state.weather_loaded = False

if get_weather:
    st.session_state.weather_loaded = True

# =========================================
# CACHE WEATHER API
# =========================================
@st.cache_data

def get_weather_data(url):
    response = requests.get(url)
    return response.json()

# =========================================
# MAIN WEATHER SECTION
# =========================================
if st.session_state.weather_loaded:

    # CURRENT WEATHER API
    current_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    # FORECAST API
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

    # GET DATA
    current_data = get_weather_data(current_url)
    forecast_data = get_weather_data(forecast_url)

    if current_data["cod"] == 200:

        # WEATHER DETAILS
        temp = current_data["main"]["temp"]
        humidity = current_data["main"]["humidity"]
        wind = current_data["wind"]["speed"]
        desc = current_data["weather"][0]["description"]

        weather_condition = current_data["weather"][0]["main"]

        lat = current_data["coord"]["lat"]
        lon = current_data["coord"]["lon"]

        icon = current_data["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{icon}@2x.png"

        # =========================================
        # DYNAMIC BACKGROUND
        # =========================================

        background_css = ""

        # CLEAR
        if weather_condition == "Clear":

            background_css = """
            <style>
            .stApp {
                background: linear-gradient(
                    135deg,
                    #56ccf2,
                    #2f80ed
                );
            }
            </style>
            """

        # CLOUDS
        elif weather_condition == "Clouds":

            background_css = """
            <style>
            .stApp {
                background: linear-gradient(
                    135deg,
                    #757f9a,
                    #d7dde8
                );
            }
            </style>
            """

        # RAIN
        elif weather_condition == "Rain":

            background_css = """
            <style>
            .stApp {
                background: linear-gradient(
                    135deg,
                    #232526,
                    #414345
                );
            }

            .rain {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: 0;
            }

            .drop {
                position: absolute;
                width: 2px;
                height: 80px;
                background: linear-gradient(
                    transparent,
                    rgba(255,255,255,0.6)
                );
                animation: rain linear infinite;
            }

            @keyframes rain {
                0% {
                    transform: translateY(-100px);
                    opacity: 0;
                }

                10% {
                    opacity: 1;
                }

                100% {
                    transform: translateY(120vh);
                    opacity: 0;
                }
            }
            </style>

            <div class="rain">
                <div class="drop" style="left:5%; animation-duration:0.8s;"></div>
                <div class="drop" style="left:10%; animation-duration:1s;"></div>
                <div class="drop" style="left:15%; animation-duration:0.7s;"></div>
                <div class="drop" style="left:20%; animation-duration:1.1s;"></div>
                <div class="drop" style="left:25%; animation-duration:0.9s;"></div>
                <div class="drop" style="left:30%; animation-duration:0.8s;"></div>
                <div class="drop" style="left:35%; animation-duration:1.2s;"></div>
                <div class="drop" style="left:40%; animation-duration:0.7s;"></div>
                <div class="drop" style="left:45%; animation-duration:1s;"></div>
                <div class="drop" style="left:50%; animation-duration:0.9s;"></div>
                <div class="drop" style="left:55%; animation-duration:1.1s;"></div>
                <div class="drop" style="left:60%; animation-duration:0.8s;"></div>
                <div class="drop" style="left:65%; animation-duration:1s;"></div>
                <div class="drop" style="left:70%; animation-duration:0.7s;"></div>
                <div class="drop" style="left:75%; animation-duration:1.2s;"></div>
                <div class="drop" style="left:80%; animation-duration:0.9s;"></div>
                <div class="drop" style="left:85%; animation-duration:1s;"></div>
                <div class="drop" style="left:90%; animation-duration:0.8s;"></div>
            </div>
            """

        # THUNDERSTORM
        elif weather_condition == "Thunderstorm":

            background_css = """
            <style>
            .stApp {
                background: linear-gradient(
                    135deg,
                    #0f2027,
                    #203a43,
                    #2c5364
                );
            }

            .flash {
                position: fixed;
                width: 100%;
                height: 100%;
                background: white;
                opacity: 0;
                pointer-events: none;
                animation: lightning 6s infinite;
            }

            @keyframes lightning {
                0% {opacity:0;}
                1% {opacity:0.8;}
                2% {opacity:0;}
                100% {opacity:0;}
            }
            </style>

            <div class="flash"></div>
            """

        # SNOW
        elif weather_condition == "Snow":

            st.snow()

            background_css = """
            <style>
            .stApp {
                background: linear-gradient(
                    135deg,
                    #e6dada,
                    #274046
                );
            }
            </style>
            """

        # FOG / HAZE / MIST
        elif weather_condition in ["Mist", "Fog", "Haze"]:

            background_css = """
            <style>

            .stApp {
                background: linear-gradient(
                    135deg,
                    #141e30,
                    #243b55,
                    #0f172a
                );

                background-size: 400% 400%;
                animation: gradientBG 15s ease infinite;
                color: white;
            }

            @keyframes gradientBG {
                0% {
                    background-position: 0% 50%;
                }

                50% {
                    background-position: 100% 50%;
                }

                100% {
                    background-position: 0% 50%;
                }
            }

            </style>
            """

        st.markdown(background_css, unsafe_allow_html=True)

        # =========================================
        # METRICS
        # =========================================
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("🌡 Temperature", f"{temp} °C")
        col2.metric("💧 Humidity", f"{humidity}%")
        col3.metric("💨 Wind Speed", f"{wind} m/s")
        col4.metric("☁ Condition", desc.title())

        # WEATHER ICON
        st.markdown(
            f"""
            <div style='text-align:center;'>
                <img src="{icon_url}" width="150">
            </div>
            """,
            unsafe_allow_html=True
        )

        # =========================================
        # FORECAST DATAFRAME
        # =========================================
        forecast_list = forecast_data["list"]

        dates = []
        temps = []
        humidity_data = []
        wind_data = []

        for item in forecast_list:
            dates.append(item["dt_txt"])
            temps.append(item["main"]["temp"])
            humidity_data.append(item["main"]["humidity"])
            wind_data.append(item["wind"]["speed"])

        df = pd.DataFrame({
            "Date": dates,
            "Temperature": temps,
            "Humidity": humidity_data,
            "Wind Speed": wind_data
        })

        # =========================================
        # TEMPERATURE CHART
        # =========================================
        st.subheader("📈 Temperature Analytics")

        fig_temp = px.line(
            df,
            x="Date",
            y="Temperature",
            markers=True,
            title="Temperature Forecast"
        )

        fig_temp.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white")
        )

        st.plotly_chart(fig_temp, use_container_width=True)

        # =========================================
        # HUMIDITY CHART
        # =========================================
        st.subheader("💧 Humidity Analytics")

        fig_humidity = px.area(
            df,
            x="Date",
            y="Humidity",
            title="Humidity Forecast"
        )

        fig_humidity.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white")
        )

        st.plotly_chart(fig_humidity, use_container_width=True)

        # =========================================
        # WIND SPEED CHART
        # =========================================
        st.subheader("💨 Wind Speed Analytics")

        fig_wind = go.Figure()

        fig_wind.add_trace(
            go.Bar(
                x=df["Date"],
                y=df["Wind Speed"]
            )
        )

        fig_wind.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white")
        )

        st.plotly_chart(fig_wind, use_container_width=True)

        # =========================================
        # LIVE WEATHER MAP
        # =========================================
        st.subheader("🗺 Live Weather Map")

        # DARK MODERN MAP
        weather_map = folium.Map(
            location=[lat, lon],
            zoom_start=5,
            tiles="CartoDB Voyager"
        )

        # GLOWING MARKER
        folium.CircleMarker(
            location=[lat, lon],
            radius=20,
            popup=f"{city}: {temp}°C",
            color="#60a5fa",
            fill=True,
            fill_color="#3b82f6",
            fill_opacity=0.9
        ).add_to(weather_map)

        # HIDE BIG ATTRIBUTION STYLE
        weather_map.get_root().html.add_child(folium.Element("""
        <style>
        .leaflet-control-attribution {
            background: rgba(0,0,0,0.3) !important;
            color: white !important;
            font-size: 10px !important;
            border-radius: 8px;
            padding: 2px 8px;
        }
        </style>
        """))

        # SHOW MAP
        st_folium(
            weather_map,
            width=1200,
            height=500,
            returned_objects=[]
        )

        # =========================================
        # DATAFRAME
        # =========================================
        st.subheader("📋 Forecast Data")

        st.dataframe(df)

    else:
        st.error("❌ City not found")
