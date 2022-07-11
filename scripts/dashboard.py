import pandas as pd
import altair as alt
from pyodide.http import open_url

run_1km = pd.read_csv(open_url("https://raw.githubusercontent.com/onlyphantom/miband/main/data/run_1km.csv"))

# if necessary, transform_fold convert wide-form data 
# into long-form data (opposite of pivot).
chart = alt.Chart(run_1km).mark_circle(
        opacity=0.6
    ).encode(
        alt.X('startTime:T', title='Date'),
        alt.Y('seconds_per_km'),
        color='day(startTime):N',
        tooltip=['monthdate(startTime)', 'distance(m)', 'calories(kcal)', 'speed_per_km']
    )
    
chart + chart.transform_loess(
        'startTime',
        'seconds_per_km',
    ).mark_line(size=2, opacity=0.4).interactive()