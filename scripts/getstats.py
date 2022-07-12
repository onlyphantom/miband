from datetime import timedelta
import json
import pandas as pd
from pyodide.http import open_url

df = pd.read_csv(open_url("https://raw.githubusercontent.com/onlyphantom/miband/main/data/jan2022_to_june2022.csv"), parse_dates=['startTime'])
df['date'] = (df['startTime'] + timedelta(hours=7)).dt.strftime("%Y-%m-%d %H:%M")

# walk is type 6, run is type 1
total_walk_distance_km = df[df['type'] == 6]['distance(m)'].sum()/1000

runs = df[(df['type'] == 1) & (df['distance(m)'] >= 1000)].copy()
runs = runs.drop(columns=['type', 'maxPace(/meter)', 'minPace(/meter)', 'avgPace(/meter)'])
num_of_runs = runs.shape[0] # 63
total_run_distance_km = runs['distance(m)'].sum()/1000

# runs['mins_per_km'] = runs['sportTime(s)'] / runs['distance(m)'] * 60
runs['seconds_per_km'] = (1000 / runs['distance(m)']) * runs['sportTime(s)'] 

def create_m_s(seconds):
    m, s = divmod(seconds, 60)
    return "{:02.0f}:{:02.2f}".format(m, s)

runs['speed_per_km'] = runs['seconds_per_km'].map(lambda x: create_m_s(x))
runs = runs.sort_values(by='seconds_per_km')

toprows = [
    num_of_runs, 
    round(total_walk_distance_km,3), 
    round(total_run_distance_km,3), 
    round(total_walk_distance_km + total_run_distance_km,3),
    [
        runs['startTime'].min().strftime('%Y-%m-%d'),
        runs['startTime'].max().strftime('%Y-%m-%d'),
    ]
    ]


# runs['distance_rounded'] = (runs['distance(m)'].round(decimals=-3)/1000).astype('category')
runs['distance_rounded'] = (runs['distance(m)']//1000).astype('category')
bestruns = runs.groupby('distance_rounded').head(3)
# print(bestruns.to_json())

print(bestruns[['date', 'speed_per_km', 'calories(kcal)', 'distance_rounded']].set_index('date').reset_index().to_html(index=False, col_space=[100,50,50,50], table_id="bestruns", justify="justify", classes=['table table-dark table-striped table-bordered']))

run_1km = runs[runs['distance_rounded'] == 1.0].sort_values(by='startTime')


pb = runs.groupby('distance_rounded')['seconds_per_km'].agg(['mean', 'min']).rename_axis("distance(km)")
pb['mean'] = pb['mean'].map(lambda x: create_m_s(x))
pb['min'] = pb['min'].map(lambda x: create_m_s(x))

# alt: runs.groupby('distance_rounded')['seconds_per_km'].agg(
# ['mean', 'min']).reset_index()
avg_speed = pb.loc[:,'mean'].to_json()
top_speed = pb.loc[:,'min'].to_json()

toprows += [{'avg_speed': avg_speed, 'top_speed': top_speed}]
print(json.dumps(toprows))

print("<h4>Personal Best</h4>")
print(pb.reset_index().to_html(index=False, table_id="personalbest", justify="justify", classes=['table table-dark table-striped table-bordered']))
