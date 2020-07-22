# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_table
from dash.dependencies import Input, Output
import numpy as np
import dash
import dash_bootstrap_components as dbc


# Styling
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# external CSS stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]



# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# img = datasets.fetch_localizer_button_task()['tmap']
# html_view = plotting.view_img(img, threshold=2, vmax=4, cut_coords=[-42, -16, 52], title="Motor contrast")
# html_view.save_as_html('viewer.html')

# Create app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
                ])
server = app.server

app.config.suppress_callback_exceptions = True

# app.layout = html.Div(children=[
#     html.H1(children='Hello Dash'),
#
#     html.Div(children='''
#         Dash: A web application framework for Python.
#     '''),
#
#
#     html.Iframe(id='target2', src='/assets/viewer.html', style={'border': 'none', 'width': '50%', 'height': 1000})
#
#
#
# ])
#
#
#
# if __name__ == '__main__':
#     app.run_server(debug=True)