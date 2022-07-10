import pandas as pd
from pyodide.http import open_url

df = pd.read_csv(open_url("https://raw.githubusercontent.com/onlyphantom/miband/main/data/jan2022_to_june2022.csv"))
# walk is type 6, run is type 1
runs = df[(df['type'] == 1) & (df['distance(m)'] >= 1000)].copy()
num_of_runs = runs.shape[0] # 63
print(num_of_runs)

# runs['mins_per_km'] = runs['sportTime(s)'] / runs['distance(m)'] * 60
runs['seconds_per_km'] = (1000 / runs['distance(m)']) * runs['sportTime(s)'] 
m, s = divmod(runs['seconds_per_km'], 60)

def create_m_s(seconds):
    m, s = divmod(seconds, 60)
    return "{:02.0f}:{:02.2f}".format(m, s)

runs['speed_per_km'] = runs['seconds_per_km'].map(lambda x: create_m_s(x))
runs = runs.sort_values(by='seconds_per_km')
print(runs.head().to_html())