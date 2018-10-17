import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css'
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

colors = {
    'text': '#3333ff'
}

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_world_gdp_with_codes.csv')

data = [dict(
    type='choropleth',
    locations=df['CODE'],
    z=df['GDP (BILLIONS)'],
    text=df['COUNTRY'],
    colorscale=[[0, "rgb(5, 10, 172)"], [0.35, "rgb(40, 60, 190)"], [0.5, "rgb(70, 100, 245)"],
                [0.6, "rgb(90, 120, 245)"], [0.7, "rgb(106, 137, 247)"], [1, "rgb(220, 220, 220)"]],
    autocolorscale=False,
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
                            id='my-slider',
                            min=0,
                            max=200,
                            step=1,
                            value=10,
                            updatemode='mouseup'
                        ),
                        html.Div(id='slider-output-container')
                    ]
                )
            ]
        )
    ])


@app.callback(
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('my-slider', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)


if __name__ == '__main__':
    app.run_server(debug=True)
