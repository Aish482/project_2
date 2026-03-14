import pandas as pd
import sqlalchemy
engine = sqlalchemy.create_engine('sqlite:///traffic_violations.db')
df = pd.read_sql('select "Time Of Stop" from violations limit 20', engine)
print(df)
print('parsed:')
print(pd.to_datetime(df['Time Of Stop'], format='%H:%M:%S', errors='coerce').head())
