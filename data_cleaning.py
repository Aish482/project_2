import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import re

# Create SQLite database
engine = create_engine('sqlite:///traffic_violations.db')

# Define dtypes for efficient reading
dtypes = {
    'SeqID': 'str',
    'Date Of Stop': 'str',
    'Time Of Stop': 'str',
    'Agency': 'str',
    'SubAgency': 'str',
    'Description': 'str',
    'Location': 'str',
    'Latitude': 'str',
    'Longitude': 'str',
    'Accident': 'str',
    'Belts': 'str',
    'Personal Injury': 'str',
    'Property Damage': 'str',
    'Fatal': 'str',
    'Commercial License': 'str',
    'HAZMAT': 'str',
    'Commercial Vehicle': 'str',
    'Alcohol': 'str',
    'Work Zone': 'str',
    'Search Conducted': 'str',
    'Search Disposition': 'str',
    'Search Outcome': 'str',
    'Search Reason': 'str',
    'Search Reason For Stop': 'str',
    'Search Type': 'str',
    'Search Arrest Reason': 'str',
    'State': 'str',
    'VehicleType': 'str',
    'Year': 'str',
    'Make': 'str',
    'Model': 'str',
    'Color': 'str',
    'Violation Type': 'str',
    'Charge': 'str',
    'Article': 'str',
    'Contributed To Accident': 'str',
    'Race': 'str',
    'Gender': 'str',
    'Driver City': 'str',
    'Driver State': 'str',
    'DL State': 'str',
    'Arrest Type': 'str',
    'Geolocation': 'str'
}

# Function to clean boolean columns
def clean_bool(value):
    if pd.isna(value) or value == '':
        return False
    value = str(value).strip().upper()
    if value in ['YES', 'Y', 'TRUE', '1']:
        return True
    elif value in ['NO', 'N', 'FALSE', '0']:
        return False
    else:
        return False  # Default to False

# Function to standardize text
def standardize_text(value):
    if pd.isna(value):
        return value
    return str(value).strip().upper()

# Read and process in chunks
chunksize = 10000
for chunk in pd.read_csv('Traffic_Violations.csv', dtype=dtypes, chunksize=chunksize):
    # Clean Date Of Stop
    chunk['Date Of Stop'] = pd.to_datetime(chunk['Date Of Stop'], errors='coerce', format='%m/%d/%Y')

    # Clean Time Of Stop
    chunk['Time Of Stop'] = pd.to_datetime(chunk['Time Of Stop'], format='%H:%M:%S', errors='coerce').dt.time

    # Standardize Agency and SubAgency
    chunk['Agency'] = chunk['Agency'].apply(standardize_text)
    chunk['SubAgency'] = chunk['SubAgency'].apply(standardize_text)

    # Clean Description
    chunk['Description'] = chunk['Description'].str.strip()

    # Clean Location
    chunk['Location'] = chunk['Location'].str.strip()

    # Latitude and Longitude
    chunk['Latitude'] = pd.to_numeric(chunk['Latitude'], errors='coerce')
    chunk['Longitude'] = pd.to_numeric(chunk['Longitude'], errors='coerce')
    chunk.loc[chunk['Latitude'] == 0, 'Latitude'] = np.nan
    chunk.loc[chunk['Longitude'] == 0, 'Longitude'] = np.nan

    # Boolean columns
    bool_cols = ['Accident', 'Belts', 'Personal Injury', 'Property Damage', 'Fatal', 'Commercial License', 'HAZMAT', 'Commercial Vehicle', 'Alcohol', 'Work Zone', 'Search Conducted', 'Contributed To Accident']
    for col in bool_cols:
        chunk[col] = chunk[col].apply(clean_bool)

    # Search Disposition, Outcome, etc.
    chunk['Search Disposition'] = chunk['Search Disposition'].apply(standardize_text)
    chunk['Search Outcome'] = chunk['Search Outcome'].apply(standardize_text)
    chunk['Search Reason'] = chunk['Search Reason'].apply(standardize_text)
    chunk['Search Reason For Stop'] = chunk['Search Reason For Stop'].apply(standardize_text)
    chunk['Search Type'] = chunk['Search Type'].apply(standardize_text)
    chunk['Search Arrest Reason'] = chunk['Search Arrest Reason'].apply(standardize_text)

    # State
    chunk['State'] = chunk['State'].apply(standardize_text)

    # VehicleType
    chunk['VehicleType'] = chunk['VehicleType'].str.strip()

    # Year
    chunk['Year'] = pd.to_numeric(chunk['Year'], errors='coerce')
    chunk.loc[(chunk['Year'] < 1960) | (chunk['Year'] > 2025), 'Year'] = np.nan

    # Make, Model, Color
    chunk['Make'] = chunk['Make'].apply(standardize_text)
    chunk['Model'] = chunk['Model'].apply(standardize_text)
    chunk['Color'] = chunk['Color'].apply(standardize_text)

    # Violation Type
    chunk['Violation Type'] = chunk['Violation Type'].apply(standardize_text)

    # Charge, Article
    chunk['Charge'] = chunk['Charge'].str.strip()
    chunk['Article'] = chunk['Article'].apply(standardize_text)

    # Race, Gender
    chunk['Race'] = chunk['Race'].apply(standardize_text)
    chunk['Gender'] = chunk['Gender'].apply(standardize_text)
    chunk.loc[chunk['Gender'] == '', 'Gender'] = 'UNKNOWN'

    # Driver City, Driver State, DL State
    chunk['Driver City'] = chunk['Driver City'].apply(standardize_text)
    chunk['Driver State'] = chunk['Driver State'].apply(standardize_text)
    chunk['DL State'] = chunk['DL State'].apply(standardize_text)

    # Arrest Type
    chunk['Arrest Type'] = chunk['Arrest Type'].str.strip()

    # Geolocation: drop as redundant
    chunk.drop('Geolocation', axis=1, inplace=True)

    # Append to database
    chunk.to_sql('violations', engine, if_exists='append', index=False)

print("Data cleaning and loading completed.")
engine.dispose()