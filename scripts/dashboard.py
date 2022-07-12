import pandas as pd
import altair as alt
from pyodide.http import open_url

run_1km = pd.read_csv(open_url("https://raw.githubusercontent.com/onlyphantom/miband/main/data/run_1km.csv"))
# remove 1% percentile as outlier
run_1km = run_1km[run_1km['seconds_per_km'] < run_1km['seconds_per_km'].quantile(0.99)]


alt.renderers.set_embed_options(theme='dark')

highlight = alt.selection(type='single', on='mouseover',
                          fields=['day'], nearest=True)

base = alt.Chart(run_1km).encode(
    alt.X('startTime:T', title='Date', axis=alt.Axis(format='%Y-%m-%d', grid=False)),
    alt.Y('seconds_per_km', axis=alt.Axis(title='', grid=False)),
    # color=alt.Color('day(startTime):N', title='Day of Week'),
    color=alt.Color('day:N', 
        title='Day of Week', 
        legend=alt.Legend(title='Day of Week', orient='bottom-left', formatType='time', format='%A'),
    ),
).transform_timeunit(
    day='day(startTime)',
)

# if necessary, transform_fold convert wide-form data 
# into long-form data (opposite of pivot).
points = base.mark_circle().encode(
    opacity=alt.value(4),
    tooltip=['monthdate(startTime)', 'distance(m)', 'calories(kcal)', 'speed_per_km'],
).add_selection(
    highlight
)

lines = base.mark_line().encode(
    size=alt.condition(~highlight, alt.value(1), alt.value(3))
)

(points + lines).interactive()


grid = alt.Chart(run_1km).mark_rect().encode(
    alt.X('date(startTime):O', title='Date', axis=alt.Axis(grid=False)),
    alt.Y('month(startTime):O', title='Month', axis=alt.Axis(title='', grid=False)),
    color=alt.Color(
        'mean(seconds_per_km):Q', 
        legend=alt.Legend(title='Avg Speed')
    ),
    tooltip=['monthdate(startTime)', 'distance(m)', 'calories(kcal)', 'speed_per_km'],
).interactive()

bubble = alt.Chart(run_1km).mark_circle().encode(
    alt.X('date(startTime):O', title='Day of Week', axis=alt.Axis(grid=False)),
    alt.Y('month(startTime):O', title='Month', axis=alt.Axis(title='', grid=False)),
    size=alt.Size("seconds_per_km:Q", 
        legend=None, 
        scale=alt.Scale(range=[1, 500], domain=[300, run_1km['seconds_per_km'].min()])), 
    color=alt.Color("seconds_per_km:Q", legend=None),
        tooltip=['monthdate(startTime)', 'distance(m)', 'calories(kcal)', 'speed_per_km'],
).interactive()


(points + lines).interactive() | alt.vconcat(grid, bubble)