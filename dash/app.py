# -*- coding: utf-8 -*-
import pandas as pd
import copy

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

df = pd.read_csv('cycle-hires-prepared.csv', index_col=0, parse_dates=True)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='London Bicycle Hires', style={'textAlign': 'center'}),

    html.Div(children='''
        Over seven years' worth of London daily bicycle hire data.
    ''', style={'textAlign': 'center'}),

    html.Div(
        dcc.Graph(
            id='timeseries-graph',
            figure={
                'data': [
                    {'x': df.index, 'y': df['Number of Bicycle Hires']},
                ],
                'layout': {
                    'title': 'Bicycle hires over time',
                    'yaxis': {'fixedrange': True}
                }
            }
        )
    ),

    html.Div(children=[
        html.Div(dcc.Graph(id='histogram-graph'), className='four columns'),
        html.Div(dcc.Graph(id='day-graph'), className='four columns'),
        html.Div(dcc.Graph(id='month-graph'), className='four columns')
    ])
])


@app.callback(
    Output('histogram-graph', 'figure'),
    [Input('timeseries-graph', 'relayoutData')])
def update_histogram(ts_selection):
    if ts_selection is not None and 'xaxis.range[0]' in ts_selection and \
                                    'xaxis.range[1]' in ts_selection:
        x0 = ts_selection['xaxis.range[0]']
        x1 = ts_selection['xaxis.range[1]']
        sub_df = df[(df.index >= x0) & (df.index <= x1)]
        xaxis = sub_df['Number of Bicycle Hires']
    else:
        xaxis = df['Number of Bicycle Hires']
    return {
        'data': [
            {'x': xaxis, 'type': 'histogram'},
        ],
        'layout': {
            'title': 'Daily bicycle hires histogram',
            'yaxis': {'title': 'Count'}
        }
    }


@app.callback(
    Output('day-graph', 'figure'),
    [Input('timeseries-graph', 'relayoutData')])
def update_day_graph(selection):
    if selection is not None and 'xaxis.range[0]' in selection and \
                                 'xaxis.range[1]' in selection:
        x0 = selection['xaxis.range[0]']
        x1 = selection['xaxis.range[1]']
        sub_df = df[(df.index >= x0) & (df.index <= x1)]
        df_d = sub_df.groupby(sub_df.index.dayofweek).mean()
    else:
        df_d = df.groupby(df.index.dayofweek).mean()
    return {
        'data': [
            {'x': df_d.index, 'y': df_d['Number of Bicycle Hires'],
             'type': 'bar'},
        ],
        'layout': {
            'title': 'Daily bicycle hires by day of week',
            'xaxis': {'ticktext': ['Sun', 'Mon', 'Tue', 'Wed',
                                   'Thu', 'Fri', 'Sat'],
                      'tickvals': [0, 1, 2, 3, 4, 5, 6]}
        }
    }


@app.callback(
    Output('month-graph', 'figure'),
    [Input('timeseries-graph', 'relayoutData')])
def update_month_graph(selection):
    if selection is not None and 'xaxis.range[0]' in selection and \
                                 'xaxis.range[1]' in selection:
        x0 = selection['xaxis.range[0]']
        x1 = selection['xaxis.range[1]']
        sub_df = df[(df.index >= x0) & (df.index <= x1)]
        df_m = sub_df.groupby(sub_df.index.month).mean()
    else:
        df_m = df.groupby(df.index.month).mean()
    return {
        'data': [
            {'x': df_m.index, 'y': df_m['Number of Bicycle Hires'],
             'type': 'bar'},
        ],
        'layout': {
            'title': 'Daily bicycle hires by month',
            'xaxis': {'ticktext': ['Jan', 'Feb', 'Mar', 'Apr',
                                   'May', 'Jun', 'Jul', 'Aug',
                                   'Sep', 'Oct', 'Nov', 'Dec'],
                      'tickvals': [1, 2, 3, 4, 5, 6, 7,
                                   8, 9, 10, 11, 12]}
        }
    }


if __name__ == '__main__':
    app.run_server(debug=True)
