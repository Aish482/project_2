import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sqlalchemy import create_engine
import sqlite3

# Connect to database
engine = create_engine('sqlite:///traffic_violations.db')

# Function to run query and get df
def run_query(query):
    return pd.read_sql(query, engine)

# 1. Most common violations
query = """
SELECT Description, COUNT(*) as count
FROM violations
GROUP BY Description
ORDER BY count DESC
LIMIT 10
"""
common_violations = run_query(query)
print("Most Common Violations:")
print(common_violations)

# Plot
plt.figure(figsize=(10,6))
sns.barplot(data=common_violations, x='count', y='Description')
plt.title('Top 10 Most Common Violations')
plt.savefig('common_violations.png')
# plt.show()

# 2. Violations by time of day
query = """
SELECT strftime('%H', 'Time Of Stop') as hour, COUNT(*) as count
FROM violations
WHERE 'Time Of Stop' IS NOT NULL
GROUP BY hour
ORDER BY hour
"""
time_violations = run_query(query)
time_violations['hour'] = time_violations['hour'].astype(int)
print("Violations by Hour:")
print(time_violations)

plt.figure(figsize=(10,6))
sns.lineplot(data=time_violations, x='hour', y='count')
plt.title('Violations by Hour of Day')
plt.savefig('violations_by_hour.png')
# plt.show()

# 3. Violations by race
query = """
SELECT Race, COUNT(*) as count
FROM violations
WHERE Race IS NOT NULL
GROUP BY Race
ORDER BY count DESC
"""
race_violations = run_query(query)
print("Violations by Race:")
print(race_violations)

plt.figure(figsize=(10,6))
sns.barplot(data=race_violations, x='count', y='Race')
plt.title('Violations by Race')
plt.savefig('violations_by_race.png')
# plt.show()

# 4. Vehicle makes
query = """
SELECT Make, COUNT(*) as count
FROM violations
WHERE Make IS NOT NULL
GROUP BY Make
ORDER BY count DESC
LIMIT 10
"""
make_violations = run_query(query)
print("Top Vehicle Makes:")
print(make_violations)

plt.figure(figsize=(10,6))
sns.barplot(data=make_violations, x='count', y='Make')
plt.title('Top 10 Vehicle Makes')
plt.savefig('top_makes.png')
# plt.show()

# 5. Accidents
query = """
SELECT Accident, COUNT(*) as count
FROM violations
GROUP BY Accident
"""
accident_count = run_query(query)
print("Accident Counts:")
print(accident_count)

# 6. Hotspots: Since lat lon, perhaps count by rounded lat lon
query = """
SELECT ROUND(Latitude, 2) as lat, ROUND(Longitude, 2) as lon, COUNT(*) as count
FROM violations
WHERE Latitude IS NOT NULL AND Longitude IS NOT NULL
GROUP BY lat, lon
ORDER BY count DESC
LIMIT 20
"""
hotspots = run_query(query)
print("Top Hotspots:")
print(hotspots)

# For heatmap, use plotly
fig = px.scatter_mapbox(hotspots, lat='lat', lon='lon', size='count', zoom=10)
fig.update_layout(mapbox_style="open-street-map")
fig.write_image('hotspots.png')

# Summary stats
total_violations = run_query("SELECT COUNT(*) as total FROM violations")['total'][0]
accidents = run_query("SELECT COUNT(*) as acc FROM violations WHERE Accident = 1")['acc'][0]
print(f"Total Violations: {total_violations}")
print(f"Violations with Accidents: {accidents}")

print("EDA completed. Plots saved.")