# -*- coding: utf-8 -*-
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc


main_md = dcc.Markdown('''

The `rt-me-fMRI` dataset was collected as part of a study to investigate improved real-time functional magnetic resonance imaging (fMRI) methods for applications in neurofeedback.
It contains multiple runs of resting state and task data from 28 healthy volunteers. 
''')

# The broad goal of the methods study is to work on improvements to the quality of the fMRI-based blood oxygen level-dependent (BOLD) signal in real-time.
# These improvements are investigated for applications in real-time fMRI neurofeedback, a method where participants are presented with visual feedback of their brain activity while they are inside the MRI scanner, and then asked to regulate the level of feedback.


card_browse = [
    dbc.CardBody(
        [
            html.H5("Overview", className="card-title"),
            html.P(
                "The rt-me-fMRI dataset consist of T1w, resting and task-based multi-echo fMRI data from 28 participants...",
                className="card-text",
            ),
            dbc.Button("See data description", color="light", href="/pages/page1", external_link=True),
        ]
    ),
]

card_visualize = [
    dbc.CardBody(
        [
            html.H5("Quality", className="card-title"),
            html.P(
                "Standard quality pipelines were applied to the data to allow quality control, inspection and visualization...",
                className="card-text",
            ),
            dbc.Button("Inspect data quality", color="light", href="/pages/page2", external_link=True),
        ]
    ),
]

card_submit = [
    dbc.CardBody(
        [
            html.H5("Multi-echo", className="card-title"),
            html.P(
                "New methods were developed for offline and real-time multi-echo fMRI combination and analysis...",
                className="card-text",
            ),
            dbc.Button("View multi-echo measures", color="light", href="/pages/page3", external_link=True),
        ]
    ),
]



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
                dbc.Col(dbc.Card(card_browse, color="primary", inverse=True )),
                dbc.Col(
                    dbc.Card(card_visualize, color="secondary", inverse=True)
                ),
                dbc.Col(dbc.Card(card_submit, color="info", inverse=True)),
            ],
            className="mb-4",
        ),
        ]
    )

    # html.H2(children='Browse through literature to find and visualize studies and their methods',
    #          style={
    #     'textAlign': 'center',
    # }),



],
style={
    'marginBottom': 25,
    'marginTop': 50,
    'marginLeft': '5%',
    'maxWidth': '90%'
})
