import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import music_analyzer_classes

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css'
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

colors = {
    'text': '#3333ff'
}

#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')
dfdata = pd.read_csv('data/aggregated_data_with_features.csv')

cont_features = ['tempo','energy','liveness','duration_ms','loudness','instrumentalness','acousticness','speechiness']
dfdata = dfdata.dropna(subset = cont_features)
X = dfdata.sample(1)[cont_features].values
# point is a list or numpy array with 8 values. This one is a random sample
# from the data
point = X[0,:]
print(point)

predictor = music_analyzer_classes.Predictor()
#point = ('tempo','energy','liveness','duration_ms','loudness','instrumentalness','acousticness','speechiness')
dfpred = predictor.value(point,dfdata)

# Country codes conversion from ISO 3166-1 alpha-2 to ISO 3166-1 alpha-3
dfcountry = pd.read_csv('data/countryMap.txt',sep='\t')
dfpred['region'] = dfpred['region'].str.upper()
df = dfpred.merge(dfcountry,how='inner',left_on=['region'],right_on=['2let'])

data = [dict(
    type='choropleth',
    locations=df['3let'],
    z=df['relative_values'],
    text=df['Countrylet'],
#    colorscale=[[0, "rgb(5, 10, 172)"], [0.35, "rgb(40, 60, 190)"], [0.5, "rgb(70, 100, 245)"],
#                [0.6, "rgb(90, 120, 245)"], [0.7, "rgb(106, 137, 247)"], [1, "rgb(220, 220, 220)"]],
#    autocolorscale=False,
    autocolorscale=True,
    reversescale=True,
    showscale=False,
    marker=dict(
        line=dict(
            color='rgb(180,180,180)',
            width=0.5
        )
    ),
    # colorbar=dict(
    #    autotick=False,
    #    title='GDP<br>Billions US$'),
)]

layout = dict(
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection=dict(
            type='Mercator'
        )
    ),
    font=dict(
        color=colors['text']
    )
)

app.layout = html.Div(
    className='container-fluid',
    children=[
        html.Div(
            className='row',
            children=[
                html.H1(
                    children='Country Music Analyzer',
                    style=dict(
                        color=colors['text'],
                        textAlign='center'
                    ),
                    className='col'
                )
            ]
        ),
        html.Div(
            className='row',
            children=[
                html.P(children='Tool predicting country specific popularity of a song based on its '
                                'musical features',
                       style=dict(
                           color=colors['text'],
                           textAlign='center',
                       ),
                       className='col'
                       )
            ]
        ),
        html.Div(
            className='row justify-content-center',
            children=[
                html.Div(className='col',
                         children=[
                             dcc.Graph(
                                 id='world-choropleth',
                                 figure=dict(
                                     data=data,
                                     layout=layout
                                 )
                             )
                         ])
            ]
        ),
        html.Div(
            className='row justify-content-center',
            children=[
                html.Div(
                    className='col-sm-6',
                    children=[
                        html.Label('Tempo',
                                   style=dict(
                                       color=colors['text'],
                                       textAlign='center',
                                       display='block'
                                   )),
                        dcc.Slider(
                            id='tempo-slider',
                            min=0,
                            max=240,
                            step=1,
                            value=120,
                            updatemode='mouseup'
                        ),
                        html.Div(id='tempo-slider-output-container')
                    ]
                )
            ]
        ),
        html.Div(
            className='row justify-content-center',
            children=[
                html.Div(
                    className='col-sm-6',
                    children=[
                        html.Label('Energy',
                                   style=dict(
                                       color=colors['text'],
                                       textAlign='center',
                                       display='block'
                                   )),
                        dcc.Slider(
                            id='energy-slider',
                            min=0,
                            max=1,
                            step=0.05,
                            value=0.5,
                            updatemode='mouseup'
                        ),
                        html.Div(id='energy-slider-output-container')
                    ]
                )
            ]
        ),
        html.Div(
            className='row justify-content-center',
            children=[
                html.Div(
                    className='col-sm-6',
                    children=[
                        html.Label('Liveness',
                                   style=dict(
                                       color=colors['text'],
                                       textAlign='center',
                                       display='block'
                                   )),
                        dcc.Slider(
                            id='liveness-slider',
                            min=0,
                            max=1,
                            step=0.05,
                            value=0.5,
                            updatemode='mouseup'
                        ),
                        html.Div(id='liveness-slider-output-container')
                    ]
                )
            ]
        ),
        html.Div(
            className='row justify-content-center',
            children=[
                html.Div(
                    className='col-sm-6',
                    children=[
                        html.Label('Duration in ms',
                                   style=dict(
                                       color=colors['text'],
                                       textAlign='center',
                                       display='block'
                                   )),
                        dcc.Slider(
                            id='duration_ms-slider',
                            min=30000,
                            max=4000000,
                            step=1,
                            value=300000,
                            updatemode='mouseup'
                        ),
                        html.Div(id='duration_ms-slider-output-container')
                    ]
                )
            ]
        ),
        html.Div(
            className='row justify-content-center',
            children=[
                html.Div(
                    className='col-sm-6',
                    children=[
                        html.Label('Loudness',
                                   style=dict(
                                       color=colors['text'],
                                       textAlign='center',
                                       display='block'
                                   )),
                        dcc.Slider(
                            id='loudness-slider',
                            min=0,
                            max=5,
                            step=0.1,
                            value=2.5,
                            updatemode='mouseup'
                        ),
                        html.Div(id='loudness-slider-output-container')
                    ]
                )
            ]
        ),
        html.Div(
            className='row justify-content-center',
            children=[
                html.Div(
                    className='col-sm-6',
                    children=[
                        html.Label('Instrumentalness',
                                   style=dict(
                                       color=colors['text'],
                                       textAlign='center',
                                       display='block'
                                   )),
                        dcc.Slider(
                            id='instrumentalness-slider',
                            min=0,
                            max=1,
                            step=0.05,
                            value=0.5,
                            updatemode='mouseup'
                        ),
                        html.Div(id='instrumentalness-slider-output-container')
                    ]
                )
            ]
        ),
        html.Div(
            className='row justify-content-center',
            children=[
                html.Div(
                    className='col-sm-6',
                    children=[
                        html.Label('Acousticness',
                                   style=dict(
                                       color=colors['text'],
                                       textAlign='center',
                                       display='block'
                                   )),
                        dcc.Slider(
                            id='acousticness-slider',
                            min=0,
                            max=1,
                            step=0.05,
                            value=0.5,
                            updatemode='mouseup'
                        ),
                        html.Div(id='acousticness-slider-output-container')
                    ]
                )
            ]
        ),
        html.Div(
            className='row justify-content-center',
            children=[
                html.Div(
                    className='col-sm-6',
                    children=[
                        html.Label('Speechiness',
                                   style=dict(
                                       color=colors['text'],
                                       textAlign='center',
                                       display='block'
                                   )),
                        dcc.Slider(
                            id='speechiness-slider',
                            min=0,
                            max=1,
                            step=0.05,
                            value=0.5,
                            updatemode='mouseup'
                        ),
                        html.Div(id='speechiness-slider-output-container')
                    ]
                )
            ]
        )
    ])


@app.callback(
    dash.dependencies.Output('tempo-slider-output-container', 'children'),
    [dash.dependencies.Input('tempo-slider', 'value')])
def update_tempo(value):
    return 'You have selected "{}"'.format(value)

@app.callback(
    dash.dependencies.Output('energy-slider-output-container', 'children'),
    [dash.dependencies.Input('energy-slider', 'value')])
def update_energy(value):
    return 'You have selected "{}"'.format(value)

@app.callback(
    dash.dependencies.Output('liveness-slider-output-container', 'children'),
    [dash.dependencies.Input('liveness-slider', 'value')])
def update_liveness(value):
    return 'You have selected "{}"'.format(value)

@app.callback(
    dash.dependencies.Output('duration_ms-slider-output-container', 'children'),
    [dash.dependencies.Input('duration_ms-slider', 'value')])
def update_duration_ms(value):
    return 'You have selected "{}"'.format(value)

@app.callback(
    dash.dependencies.Output('loudness-slider-output-container', 'children'),
    [dash.dependencies.Input('loudness-slider', 'value')])
def update_loudness(value):
    return 'You have selected "{}"'.format(value)

@app.callback(
    dash.dependencies.Output('instrumentalness-slider-output-container', 'children'),
    [dash.dependencies.Input('instrumentalness-slider', 'value')])
def update_instrumentalness(value):
    return 'You have selected "{}"'.format(value)

@app.callback(
    dash.dependencies.Output('acousticness-slider-output-container', 'children'),
    [dash.dependencies.Input('acousticness-slider', 'value')])
def update_acousticness(value):
    return 'You have selected "{}"'.format(value)

@app.callback(
    dash.dependencies.Output('speechiness-slider-output-container', 'children'),
    [dash.dependencies.Input('speechiness-slider', 'value')])
def update_speechiness(value):
    return 'You have selected "{}"'.format(value)

@app.callback(
    dash.dependencies.Output('world-choropleth', 'figure'),
#    [dash.dependencies.Input('tempo-slider', 'value')])
    [dash.dependencies.Input('tempo-slider', 'value'),
     dash.dependencies.Input('energy-slider', 'value'),
     dash.dependencies.Input('liveness-slider', 'value'),
     dash.dependencies.Input('duration_ms-slider', 'value'),
     dash.dependencies.Input('loudness-slider', 'value'),
     dash.dependencies.Input('instrumentalness-slider', 'value'),
     dash.dependencies.Input('acousticness-slider', 'value'),
     dash.dependencies.Input('speechiness-slider', 'value')])
def update_graph(tempo, energy, liveness, duration, loudness, instrumentalness, acousticness, speechiness):
    point = np.array([tempo, energy, liveness, duration, loudness, instrumentalness, acousticness, speechiness])
#    predictor = music_analyzer_classes.Predictor()
    dfpred = predictor.value(point,dfdata)

    # Country codes conversion from ISO 3166-1 alpha-2 to ISO 3166-1 alpha-3
    dfcountry = pd.read_csv('data/countryMap.txt',sep='\t')
    dfpred['region'] = dfpred['region'].str.upper()
    df = dfpred.merge(dfcountry,how='inner',left_on=['region'],right_on=['2let'])

    print(point)
    #print(df)

    data = [dict(
        type='choropleth',
        locations=df['3let'],
        z=df['relative_values'],
        text=df['Countrylet'],
    #    colorscale=[[0, "rgb(5, 10, 172)"], [0.35, "rgb(40, 60, 190)"], [0.5, "rgb(70, 100, 245)"],
    #                [0.6, "rgb(90, 120, 245)"], [0.7, "rgb(106, 137, 247)"], [1, "rgb(220, 220, 220)"]],
    #    autocolorscale=False,
        autocolorscale=True,
        reversescale=True,
        showscale=False,
        marker=dict(
            line=dict(
                color='rgb(180,180,180)',
                width=0.5
            )
        ),
        # colorbar=dict(
        #    autotick=False,
        #    title='GDP<br>Billions US$'),
    )]

    figure = dict(data=data,layout=layout)
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
