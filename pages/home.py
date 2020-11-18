# -*- coding: utf-8 -*-
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc


# Create markdown to display on home page
main_md = dcc.Markdown('''
The `rt-me-fMRI` dataset was collected to explore multi-echo functional magnetic resonance imaging (fMRI) methods for real-time applications.
It contains 6 runs of resting state and task data from 28 healthy volunteers, along with T1w scans and physiology data.
''')

# Create card components to display on home page
card_access = [
    dbc.CardBody(
        [
            html.H5("Access", className="card-title"),
            html.P(
                "The BIDS-compatible rt-me-fMRI dataset is accessible via a GDPR-compliant data use agreement on DataverseNL...",
                className="card-text",
            ),
            dbc.Button("Access the dataset", color="light", href="/pages/access", external_link=True),
        ]
    ),
]
card_overview = [
    dbc.CardBody(
        [
            html.H5("Overview", className="card-title"),
            html.P(
                "The rt-me-fMRI dataset consist of T1w, resting and task-based multi-echo fMRI data from 28 participants...",
                className="card-text",
            ),
            dbc.Button("See data description", color="light", href="/pages/overview", external_link=True),
        ]
    ),
]
card_quality = [
    dbc.CardBody(
        [
            html.H5("Quality", className="card-title"),
            html.P(
                "Standard quality pipelines were applied to the data to allow quality control, inspection and visualization...",
                className="card-text",
            ),
            dbc.Button("Inspect data quality", color="light", href="/pages/quality", external_link=True),
        ]
    ),
]
card_multiecho = [
    dbc.CardBody(
        [
            html.H5("Multi-echo", className="card-title"),
            html.P(
                "New methods were developed for offline and real-time multi-echo fMRI combination and analysis...",
                className="card-text",
            ),
            dbc.Button("View multi-echo measures", color="light", href="/pages/multiecho", external_link=True),
        ]
    ),
]

# Create home page layout
layout = html.Div([
    html.H1(
        children='Real-time multi-echo fMRI',
        style={
            'textAlign': 'center',
        }
    ),
    html.Div(
        html.Img(src="/assets/melogo3.png", width="30%"),
        style={ 'textAlign': 'center'}
    ),
    html.Div([
        main_md,],
        style={
            'marginLeft': '5%',
            'maxWidth': '90%',
        }
    ),
    html.Br(),
    html.Div([
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_access, color="dark", inverse=True)),
                dbc.Col(dbc.Card(card_overview, color="primary", inverse=True )),
                dbc.Col(dbc.Card(card_quality, color="secondary", inverse=True)),
                dbc.Col(dbc.Card(card_multiecho, color="info", inverse=True)),
                
            ],
            className="mb-4",
        ),
        ]
    )
],
style={
    'marginBottom': 25,
    'marginTop': 50,
    'marginLeft': '5%',
    'maxWidth': '90%'
})