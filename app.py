import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import sqlite3

# Connect to database
@st.cache_resource
def get_engine():
    return create_engine('sqlite:///traffic_violations.db')

engine = get_engine()

# Function to get distinct values
def get_distinct(column):
    conn = sqlite3.connect('traffic_violations.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT DISTINCT {column} FROM violations WHERE {column} IS NOT NULL")
    results = [row[0] for row in cursor.fetchall()]
    conn.close()
    return results

# Sidebar filters
st.sidebar.header("Filters")

# Date range
date_min = st.sidebar.date_input("Start Date", value=pd.to_datetime('2023-01-01'))
date_max = st.sidebar.date_input("End Date", value=pd.to_datetime('2023-12-31'))

# Gender
gender_options = ['ALL'] + get_distinct('Gender')
gender = st.sidebar.selectbox("Gender", gender_options)

# Race
race_options = ['ALL'] + get_distinct('Race')
race = st.sidebar.selectbox("Race", race_options)

# Vehicle Type
vehicle_options = ['ALL'] + get_distinct('VehicleType')
vehicle = st.sidebar.selectbox("Vehicle Type", vehicle_options)

# Violation Type
violation_options = ['ALL'] + get_distinct('"Violation Type"')
violation_type = st.sidebar.selectbox("Violation Type", violation_options)

# Build query
query = "SELECT * FROM violations WHERE 1=1"
if gender != 'ALL':
    query += f" AND Gender = '{gender}'"
if race != 'ALL':
    query += f" AND Race = '{race}'"
if vehicle != 'ALL':
    query += f" AND VehicleType = '{vehicle}'"
if violation_type != 'ALL':
    query += f" AND \"Violation Type\" = '{violation_type}'"
query += f" AND \"Date Of Stop\" >= '{date_min}' AND \"Date Of Stop\" <= '{date_max}'"

# Load data
@st.cache_data
def load_data(query):
    return pd.read_sql(query, engine)

df = load_data(query)

st.write(f"Filtered Data: {len(df)} records")

# Summary stats
total = len(df)
accidents = df['Accident'].sum()
st.metric("Total Violations", total)
st.metric("With Accidents", accidents)

# Charts
st.header("Visualizations")

# Violations by Description
desc_count = df['Description'].value_counts().head(10)
desc_df = desc_count.reset_index()
desc_df.columns = ['Description', 'Count']
fig1 = px.bar(desc_df, x='Description', y='Count', title="Top Violations")
st.plotly_chart(fig1)

# By Hour
df['Hour'] = pd.to_datetime(df['Time Of Stop'], errors='coerce').dt.hour
hour_count = df['Hour'].value_counts().sort_index()
if not hour_count.empty:
    hour_df = hour_count.reset_index()
    hour_df.columns = ['Hour', 'Count']
    fig2 = px.line(hour_df, x='Hour', y='Count', title="Violations by Hour")
    st.plotly_chart(fig2)
else:
    st.write("No valid time data for hour chart")

# Map
df_clean = df.dropna(subset=['Latitude', 'Longitude'])
if not df_clean.empty:
    sample_size = min(1000, len(df_clean))
    fig3 = px.scatter_mapbox(df_clean.sample(sample_size), lat='Latitude', lon='Longitude', zoom=10, title="Violation Locations")
    fig3.update_layout(mapbox_style="carto-positron")
    st.plotly_chart(fig3)
else:
    st.write("No location data available")

# By Race
race_count = df['Race'].value_counts()
race_df = race_count.reset_index()
race_df.columns = ['Race', 'Count']
fig4 = px.pie(race_df, names='Race', values='Count', title="Violations by Race")
st.plotly_chart(fig4)