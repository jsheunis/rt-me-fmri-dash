# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
from app import app
import urllib.parse
import json


layout = html.Div([
    html.H2('Multi-echo measures',
    style={
        'textAlign': 'center',
        'marginBottom': 25,
        'marginTop': 25,
    }),
],
style={
    'marginBottom': 25,
    'marginTop': 25,
    'marginLeft': '5%',
    'maxWidth': '90%',
})