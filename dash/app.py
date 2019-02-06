# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

df = pd.read_csv('cycle-hires-prepared.csv', index_col=0, parse_dates=True)
df_d = df.groupby(df.index.dayofweek).mean()
df_m = df.groupby(df.index.month).mean()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    html.Div(
        dcc.Graph(
            id='timeseries-graph',
            figure={
                'data': [
                    {'x': df.index, 'y': df['Number of Bicycle Hires']},
                ],
                'layout': {
                    'title': 'Bicycle hires over time'
                }
            }
        )
    ),

    html.Div(children=[
        html.Div(
            dcc.Graph(
                id='histogram-graph',
                figure={
                    'data': [
                        {'x': df['Number of Bicycle Hires'],
                         'type': 'histogram'},
                    ],
                    'layout': {
                        'title': 'Number of daily bicycle hires histogram'
                    }
                }
            ), style={'width': '33%', 'display': 'inline-block'}
        ),
        html.Div(
            dcc.Graph(
                id='day-graph',
                figure={
                    'data': [
                        {'x': df_d.index, 'y': df_d['Number of Bicycle Hires'],
                         'type': 'bar'},
                    ],
                    'layout': {
                        'title': 'Daily bicycle hires by day of week'
                    }
                }
            ), style={'width': '33%', 'display': 'inline-block'}
        ),
        html.Div(
            dcc.Graph(
                id='month-graph',
                figure={
                    'data': [
                        {'x': df_m.index, 'y': df_m['Number of Bicycle Hires'],
                         'type': 'bar'},
                    ],
                    'layout': {
                        'title': 'Daily bicycle hires by month'
                    }
                }
            ), style={'width': '33%', 'display': 'inline-block'}
        )
    ])
])


if __name__ == '__main__':
    app.run_server(debug=True)
