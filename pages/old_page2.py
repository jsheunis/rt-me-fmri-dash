# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import pandas as pd
from app import app
import os

# Directories
bids_dir = 'bids'
deriv_dir = os.path.join(bids_dir, 'derivatives')
preproc_dir = os.path.join(deriv_dir, 'fmrwhy-preproc')
qc_dir = os.path.join(deriv_dir, 'fmrwhy-qc')
me_dir = os.path.join(deriv_dir, 'fmrwhy-multiecho')

# Filenames
participants_fn = 'bids/participants.tsv'
fdmean_fn = os.path.join(qc_dir, 'sub-all_task-all_run-all_desc-fdmean.tsv')
fdsum_fn = os.path.join(qc_dir, 'sub-all_task-all_run-all_desc-fdsum.tsv')
tsnrgm_fn = os.path.join(qc_dir, 'sub-all_task-all_run-all_desc-tsnrgm.tsv')
tsnrwm_fn = os.path.join(qc_dir, 'sub-all_task-all_run-all_desc-tsnrwm.tsv')
tsnrcsf_fn = os.path.join(qc_dir, 'sub-all_task-all_run-all_desc-tsnrcsf.tsv')
tsnrbrain_fn = os.path.join(qc_dir, 'sub-all_task-all_run-all_desc-tsnrbrain.tsv')

# Get data
df_participants = pd.read_csv(participants_fn, sep='\t')
df_fdmean = pd.read_csv(fdmean_fn, sep='\t', lineterminator='\r')
df_fdsum = pd.read_csv(fdsum_fn, sep='\t', lineterminator='\r')
df_tsnrgm = pd.read_csv(tsnrgm_fn, sep='\t', lineterminator='\r')
df_tsnrwm = pd.read_csv(tsnrwm_fn, sep='\t', lineterminator='\r')
df_tsnrcsf = pd.read_csv(tsnrcsf_fn, sep='\t', lineterminator='\r')
df_tsnrbrain = pd.read_csv(tsnrbrain_fn, sep='\t', lineterminator='\r')

# Dataset specifics
all_subs = list(df_participants)
tasks = ['rest', 'motor', 'emotion']
runs = ['1', '2']
cols_tasksruns = ['rest 1', 'motor 1', 'emotion 1', 'rest 2', 'motor 2', 'emotion 2']


sub_opts = [
    {'label': 'sub-005', 'value': 'sub-005'},
]

task_opts = [
    {'label': 'Rest', 'value': 'rest'},
    {'label': 'Motor', 'value': 'motor'},
    {'label': 'Emotion', 'value': 'emotion'},
]

run_opts = [
    {'label': 'Run 1', 'value': '1'},
    {'label': 'Run 2', 'value': '2'},
]





filename = 'assets/rtfMRI_methods_review_included_studies_procsteps.txt'
df_studies = pd.read_csv(filename, sep='\t', lineterminator='\r')
df_studies = df_studies.dropna(axis='columns')
df_plot = df_studies.copy()
colnames = {
    'author':'Author',
    'vendor': 'Vendor',
    'magnet': 'Field strength',
    'software': 'Software',
    'stc': 'Slice time correction',
    'mc': '3D volume realignment',
    'ss': 'Spatial smoothing',
    'dr': 'Drift removal',
    'hmp': 'Realignment parameter regression',
    'ts': 'Temporal smoothing',
    'ff': 'Frequency filtering',
    'or': 'Outlier removal',
    'droi': 'Differential ROI',
    'resp': 'Respiratory noise removal',
    'doi': 'Article DOI'
}
plotnames = [
    {'label': 'Vendor', 'value': 'vendor'},
    {'label': 'Field strength', 'value': 'magnet'},
    {'label': 'Software', 'value': 'software'},
    {'label': 'Slice time correction', 'value': 'stc'},
    {'label': '3D volume realignment', 'value': 'mc'},
    {'label': 'Spatial smoothing', 'value': 'ss'},
    {'label': 'Drift removal', 'value': 'dr'},
    {'label': 'Realignment parameter regression', 'value': 'hmp'},
    {'label': 'Temporal smoothing', 'value': 'ts'},
    {'label': 'Frequency filtering', 'value': 'ff'},
    {'label': 'Outlier removal', 'value': 'or'},
    {'label': 'Differential ROI', 'value': 'droi'},
    {'label': 'Respiratory noise removal', 'value': 'resp'},
]

srs = df_plot['vendor'].value_counts()
xx = srs.index.to_list()
yy = srs.values

dataframe = df_plot.loc[df_plot['vendor'] == 'Siemens']
srs2 = dataframe['magnet'].value_counts()
xx2 = srs2.index.to_list()
yy2 = srs2.values


main_md = dcc.Markdown('''
Hello!
''')

layout = html.Div([
            html.Div([
                html.H2('Visualize'),
                ],
                style={
                    'marginBottom': 25,
                    'marginTop': 25,
                    'marginLeft': '5%',
                    'maxWidth': '90%',
                    'textAlign': 'center'
                }
            ),

            html.Div([
                dbc.Row(
                        [
                            dbc.Col([
                                dbc.Label('Participant'),
                                dcc.Dropdown(
                                    id='drop1',
                                    options=sub_opts,
                                    value='sub-005',
                                )],
                                width={"size": 2, "offset": 1}, # figure out offset
                            ),
                            dbc.Col([
                                dbc.Label('Task'),
                                dbc.RadioItems(
                                    options=task_opts,
                                    value='rest',
                                    id="radio1",
                                    inline=True,
                                )],
                                width={"size": 3, "offset": 1}, # figure out offset
                            ),
                            dbc.Col([
                                dbc.Label('Run'),
                                dbc.RadioItems(
                                    options=run_opts,
                                    value='1',
                                    id="radio2",
                                    inline=True,
                                )],
                                width={"size": 3, "offset": 1}, # figure out offset
                            ),
                        ],
                        justify="start"
                ),
                html.Br([]),
                dbc.Row(
                    dbc.Col(
                        html.Iframe(id='target2', src='/assets/viewer.html', style={'border': 'none', 'width': '50%', 'height': 250}),
                        style={
                            'textAlign': 'center',
                        }
                    )
                ),
                ],
                style={
                    'marginLeft': '5%',
                    'maxWidth': '90%',

                }
            ),
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(dcc.Dropdown(
                                id='drop-1',
                                options=plotnames,
                                value='vendor',
                                ),
                                width={"size": 4, "offset": 1}, # figure out offset
                            ),
                            dbc.Col(dcc.Dropdown(
                                id='drop-2',
                                options=plotnames,
                                value='vendor',
                                ),
                                width={"size": 4, "offset": 2},
                            ),
                        ],
                        justify="start"
                    ),
                    html.Br([]),
                    dbc.Row(
                        [
                            dbc.Col(html.H6(
                                id='graph-1-title',
                                children='Vendor (hover to show options of second feature; click to display studies)',
                                style={
                                    'textAlign': 'center',
                                }),
                                # width={"size": 6, "offset": 3}
                            ),
                            dbc.Col(html.H6(
                                id='graph-2-title',
                                children='Field strength options when Vendor = Siemens',
                                style={
                                    'textAlign': 'center',
                                }),
                                # width={"size": 6, "offset": 3}
                            )
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(html.Div(
                                dcc.Graph(
                                    id='graph-1',
                                    figure={
                                        'data': [
                                            {'x': xx, 'y': yy, 'type': 'bar', 'name': 'Vendors', 'marker': {'color': '#9EBC9F'}},
                                        ],
                                    }
                                ),
                            )),
                            dbc.Col(html.Div(
                               dcc.Graph(
                                id='graph-2',
                                    figure={
                                        'data': [
                                            {'x': xx2, 'y': yy2, 'type': 'bar', 'name': 'Field strength', 'marker': {'color': '#D3B88C'}},
                                        ],
                                    }
                                ),
                            )),
                        ]
                    ),
                ],
                style={
                    'marginBottom': 25,
                    'marginTop': 25,
                    'marginLeft': '5%',
                    'maxWidth': '90%',
                }
            ),
            html.Div(
                id='table-1',
                style={
                    'marginBottom': 25,
                    'marginTop': 25,
                    'marginLeft': '5%',
                    'maxWidth': '90%',
                }
            )
])



# Callback for updating dropdown2 based on dropdown1 value
@app.callback(
    Output('target2', 'src'),
    [Input('drop1','value'),
     Input('radio1','value'),
     Input('radio2','value')]
)
def reset_tsnr_img(sub, task, run):

    html_fn = '/assets/' + sub + '_task-' + task + '_run-' + run + '_echo-2_desc-rapreproc_tsnr.html'
    return html_fn
















# Callback for updating graph 1
@app.callback(
    [Output('graph-1', 'figure'),
     Output('graph-1-title', 'children')],
    [Input('drop-1','value')]
)
def update_graph(feature):

    srs = df_plot[feature].value_counts()
    xx = srs.index.to_list()
    yy = srs.values
    txt = colnames[feature]

    fig={
        'data': [
            {'x': xx, 'y': yy, 'type': 'bar', 'name': txt, 'marker': {'color': '#9EBC9F'}},
        ],
    }

    title = txt + ' (hover to show options of second feature; click to display studies)'

    return [fig, title]

# Callback for updating dropdown2 based on dropdown1 value
@app.callback(
    [Output('drop-2', 'options'),
     Output('drop-2', 'value')],
    [Input('drop-1','value')]
)
def reset_dropdown2_opts(value):
    plotnames_2 = [x for x in plotnames if x['value'] != value]
    value_2 = plotnames_2[0]['value']
    return plotnames_2, value_2


# Callback for updating graph 2 based on graph1 hoverData and dropdowns
@app.callback(
    [Output('graph-2', 'figure'),
     Output('graph-2-title', 'children')],
    [Input('graph-1', 'hoverData'),
     Input('drop-1','value'),
     Input('drop-2','value')]
)
def update_graph(hoverData, feature1, feature2):
    if hoverData is None or feature1 is None or feature2 is None:
        raise PreventUpdate
    else:
        x = hoverData['points'][0]['x']
        dataframe = df_plot.loc[df_plot[feature1] == x]
        srs = dataframe[feature2].value_counts()
        xx = srs.index.to_list()
        yy = srs.values
        txt = colnames[feature2] + ' options when ' + colnames[feature1] + ' = ' + x

        fig={
            'data': [
                {'x': xx, 'y': yy, 'type': 'bar', 'name': txt, 'marker': {'color': '#D3B88C'}},
            ],
        }

        title = txt

        return [fig, title]


# Callback for showing table 1 after filtering on feature 1
@app.callback(
    Output('table-1', 'children'),
    [Input('graph-1', 'clickData'),
     Input('drop-1','value')])
def generate_table(clickData, feature, max_rows=20):

    if clickData is None:
        raise PreventUpdate
    else:
        x = clickData['points'][0]['x']

        dataframe = df_plot.loc[df_plot[feature] == x]
        table=html.Table([
            html.Thead(
                html.Tr([html.Th(col) for col in list(colnames.values())])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(writeElement(i, col, dataframe)) for col in dataframe.columns],
                ) for i in range(min(len(dataframe), max_rows))
            ]),
            ],
            className='qcsummary',
        )

        # class="table-row" data-href="http://tutorialsplane.com"

        heading=html.H4('Showing studies where ' + colnames[feature] + ' = ' + x,
                        style={'textAlign': 'center',})

        # table = dbc.Table.from_dataframe(dataframe,
        #                                  striped=True,
        #                                  bordered=True,
        #                                  hover=True,
        #                                  responsive=True,
        #                                  className='qcsummary'
        #                                  )

        return [heading, table]


def writeElement(i, col, dataframe):
    if col == 'doi':
        hrf = 'https://doi.org/'+dataframe.iloc[i][col]
        return html.A([dataframe.iloc[i][col]], href=hrf, target="_blank")
    else:
        return dataframe.iloc[i][col]