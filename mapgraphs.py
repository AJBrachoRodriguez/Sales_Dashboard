import pandas as pd
import plotly.graph_objs as go
import json
from urllib.request import urlopen

# load the GeoJSON file with the geometry of Brazil
with urlopen('https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson') as response:
    geo_brazil = json.load(response)

# function:  create map
def create_graph(df):


    data = dict(
        type='choropleth',
        locationmode = 'geojson-id',
        geojson = geo_brazil,
        locations = df['initials_state'],
        featureidkey = 'properties.sigla',
        colorscale = 'blues',
        text = df['state_name'],
        z = df['valor_total'],
        customdata = df[['state_name','valor_total']],
        colorbar = {'title':'Incomes ($)','tickformat':'.3s'}
        )

    layout = dict(
        title = 'Incomes per States ($)',
        geo = dict(
            scope = 'south america',
            resolution = 50,
            lonaxis = dict(range=[-85,-30]),
            lataxis = dict(range=[-40,10]),
            showframe = False,
            showcoastlines = False,
            showland = False,
            landcolor = 'rgba(0,0,0,0)',
            showcountries = False,
            showlakes = False,
            showrivers = False,
            showocean = False,
            fitbounds = 'locations'
        ),
        title_x = 0,
        width = 800,
        height = 500
        )
    
    fig = go.Figure([data], layout=layout)
    fig.update_layout(geo = dict(bgcolor = 'rgba(00,0,0,0)'))
    fig.update_traces(hovertemplate="<b>%{customdata[0]}</b><br> Total incomes ($): %{customdata[1]:,.0f} <extra></extra>",marker_line_width = 0)

    return fig
   