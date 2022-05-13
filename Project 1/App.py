import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

DATE_TIME = "date/time"
DATA_URL = (
    "D:\Vehicle_Collision_Project_Data_Science\Motor_Vehicle_Collisions_-_Crashes.csv"
)
st.title("Motor Vehicle Collisions in New York City")
st.markdown("This application is a Streamlit based dashboard that is used\n "
            "to analyze motor vehicle collisions in New York City 🗽💥🚗")

@st.cache(persist=True) #we use st.cache to prevent computer from reloading all 100k rows again and again, through cache it is able to store the loaded data and use it again and again in the application, with reloading the data everytime
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[['CRASH_DATE','CRASH_TIME']])
    data.dropna(subset=['LATITUDE','LONGITUDE'], inplace=True) #we need latitude and longitude columns' rows to be not null so that the data on graphs can be plotted accurately, without causing any error
    lowercase = lambda x:str(x).lower()
    data.rename(lowercase ,axis='columns', inplace=True) #converting all the column names to lowercase
    data.rename(columns={"crash_date_crash_time":"date/time"}, inplace=True) #renaming the column to date/time for ease access
    return data


data = load_data(100000)  #running data (100k rows) through the function
original_data = data

st.header("Where are the most people injured in NYC?")
injured_people = st.slider("Number of persons injured in vehicle collisions", 0, 19)
st.map(data.query("injured_persons >= @injured_people")[["latitude", "longitude"]].dropna(how="any")) #showing the number of people or more that are injured, based upon the latitude and longitude
                    #for ex : if injured_persons in the table(csv) is = 5 ; show areas where 5 or more collisions happened


st.header("How many collisions occured during a given time of the day?")
hour = st.slider("Hour to look at",0,23)


data = data[data['date/time'].dt.hour == hour]
st.markdown("Vehicle Collision between %i:00 and %i:00" % (hour, (hour + 1) % 24))
midpoint = (np.average(data['latitude']) , np.average(data['longitude']))

st.write(pdk.Deck(
    map_style = "mapbox://styles/mapbox/light-v9",   #code for visualizing the 3d map, taking midpoints of latitute and longitude
    initial_view_state={
        "latitude" : midpoint[0],
        "longitude": midpoint[1],
        "zoom":11,
        "pitch": 50,
    },

    layers = [
        pdk.Layer(
            "HexagonLayer",
            data = data [['date/time', 'latitude', 'longitude']],
            get_position = ["longitude", "latitude"], #marking positions according to latitude and longitude
            auto_highlight = True,
            radius = 100, #radius of each individual point
            extruded = True, # this line makes the point appear to be 3D
            pickable = True,
            elevation_scale = 4,
            elevation_range = [0,1000],
        ),
    ],
))


if st.checkbox("Show Raw Data" , False): #inserting a checkbox, to give user an option to see raw data or not
    st.subheader("Raw Data by minute between %i:00 and %i:00" % (hour, (hour +1 ) % 24))
    st.write(data)

st.subheader("Breakdown by minute between %i:00 and %i:00" % (hour, (hour +1 ) % 24))
filtered = data [
    (data[DATE_TIME].dt.hour >= hour) & (data[DATE_TIME].dt.hour < (hour+1))
]

hist = np.histogram(filtered[DATE_TIME].dt.minute, bins=60, range=(0,60))[0]
chart_data = pd.DataFrame({"minute": range(60), "crashes": hist})

fig = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute','crashes'], height=400)
st.write(fig)

st.header("Top 5 dangerous streets by affected class")
select =st.selectbox('Affected Class', ['Pedestrians', 'Cyclists', 'Motorists'])

if select == 'Pedestrians':
    st.write(original_data.query("injured_pedestrians > 1")[["on_street_name","injured_pedestrians"]].sort_values(by=['injured_pedestrians'], ascending=False).dropna(how="any")[:5])

elif select == 'Cyclists':
    st.write(original_data.query("injured_cyclists > 1")[["on_street_name","injured_cyclists"]].sort_values(by=['injured_cyclists'], ascending=False).dropna(how="any")[:5])

else:
    st.write(original_data.query("injured_motorists > 1")[["on_street_name","injured_motorists"]].sort_values(by=['injured_motorists'], ascending=False).dropna(how="any")[:5])
