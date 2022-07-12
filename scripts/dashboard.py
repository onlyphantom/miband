import pandas as pd
import altair as alt
from pyodide.http import open_url

run_1km = pd.read_csv(open_url("https://raw.githubusercontent.com/onlyphantom/miband/main/data/run_1km.csv"))

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

# chart = alt.Chart(run_1km).mark_circle().encode(
#     alt.X('startTime:T', title='Date', axis=alt.Axis(format='%Y-%m-%d', grid=False)),
#     alt.Y('seconds_per_km', axis=alt.Axis(title='', grid=False)),
#     tooltip=['monthdate(startTime)', 'distance(m)', 'calories(kcal)', 'speed_per_km'],
#     opacity=0.4,
# ).add_selection(
#     highlight
# ).properties(
#     # width=800,
#     # height=300
# )
    


# chart + chart.transform_loess(
#         'startTime',
#         'seconds_per_km',).interactive()
# 
lines = base.mark_line().encode(
    size=alt.condition(~highlight, alt.value(1), alt.value(3))
)

(points + lines).interactive()


grid = alt.Chart(run_1km).mark_rect().encode(
    alt.X('date(startTime):O', title='Date', axis=alt.Axis(grid=False)),
    alt.Y('month(startTime):O', title='Month', axis=alt.Axis(title='', grid=False)),
    color='mean(seconds_per_km):Q'
).interactive()

bubble = alt.Chart(run_1km).mark_circle().encode(
    alt.X('date(startTime):O', title='Day of Week', axis=alt.Axis(grid=False)),
    alt.Y('month(startTime):O', title='Month', axis=alt.Axis(title='', grid=False)),
    color=alt.Color("min(seconds_per_km):Q",
        legend=None
    ),
    size=alt.Size("seconds_per_km:Q", legend=None) 
).interactive()


(points + lines).interactive() | alt.vconcat(grid, bubble)