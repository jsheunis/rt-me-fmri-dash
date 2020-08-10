# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import pandas as pd
from app import app
import os
from plotly.colors import sequential, n_colors
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import json

# Directories
data_dir = 'assets'

# Filenames
participants_fn = 'assets/participants.tsv'
fdallsubs_fn = os.path.join(data_dir, 'sub-all_task-all_run-all_desc-fdallsubs.tsv')
fdmean_fn = os.path.join(data_dir, 'sub-all_task-all_run-all_desc-fdmean.tsv')
fdsum_fn = os.path.join(data_dir, 'sub-all_task-all_run-all_desc-fdsum.tsv')
tsnrgm_fn = os.path.join(data_dir, 'sub-all_task-all_run-all_desc-tsnrgm.tsv')
tsnrwm_fn = os.path.join(data_dir, 'sub-all_task-all_run-all_desc-tsnrwm.tsv')
tsnrcsf_fn = os.path.join(data_dir, 'sub-all_task-all_run-all_desc-tsnrcsf.tsv')
tsnrbrain_fn = os.path.join(data_dir, 'sub-all_task-all_run-all_desc-tsnrbrain.tsv')

# Get data
df_participants = pd.read_csv(participants_fn, sep='\t')
df_fdallsubs = pd.read_csv(fdallsubs_fn, sep='\t')
df_fdmean = pd.read_csv(fdmean_fn, sep='\t')
df_fdsum = pd.read_csv(fdsum_fn, sep='\t')
df_tsnrgm = pd.read_csv(tsnrgm_fn, sep='\t')
df_tsnrwm = pd.read_csv(tsnrwm_fn, sep='\t')
df_tsnrcsf = pd.read_csv(tsnrcsf_fn, sep='\t')
df_tsnrbrain = pd.read_csv(tsnrbrain_fn, sep='\t')

# Dataset specifics
all_subs = list(df_participants['participant_id'])
tasks = ['rest', 'motor', 'emotion']
runs = ['1', '2']
cols_tasksruns = ['rest 1', 'motor 1', 'emotion 1', 'rest 2', 'motor 2', 'emotion 2']
sub_opts = [{'label': sub, 'value': sub} for sub in all_subs]
task_opts = [{'label': task.capitalize(), 'value': task} for task in tasks]
run_opts = [{'label': 'Run '+run, 'value': run} for run in runs]

# figures
# Fig 1
colors = n_colors('rgb(5, 200, 200)', 'rgb(200, 10, 10)', 28, colortype='rgb')
data = []
layout = go.Layout(
    xaxis = dict(tickangle=45),
    yaxis=dict(title='Framewise displacement (mm)', range=[-0.3, 3]),
    margin={
      't': 10,
    }
)
fig = go.Figure(layout=layout)
i = 0
for colname, color in zip(all_subs, colors):
    data.append(df_fdallsubs[colname].to_numpy())
    fig.add_trace(go.Violin(y=data[i], line_color=color, name=colname, orientation='v', side='positive', width=1.8, points=False, box_visible=True, meanline_visible=True))
    i += 1
fig.update_layout(xaxis_showgrid=False, xaxis_zeroline=False)

# Fig 2 (A) and (B)
sub = 'sub-001'
fd_fn = os.path.join(data_dir, sub+'_task-all_run-all_desc-fd.tsv')
df_fd = pd.read_csv(fd_fn, sep='\t')
data = []
layout = go.Layout(title='Distributions of framewise displacement for all functional runs - '+sub,
        xaxis = dict(title = 'Task and Run'),
        yaxis=dict(title='Framewise displacement (mm)'))
fig2 = go.Figure(layout=layout)
i = 0
for colname in cols_tasksruns:
    data.append(df_fd[colname].to_numpy())
    fig2.add_trace(go.Violin(y=data[i], line_color=sequential.Inferno[i+3], name=colname.capitalize(), orientation='v', side='positive', width=1.5, points=False, box_visible=True, meanline_visible=True))
    i += 1
fig2.update_layout(xaxis_showgrid=False, xaxis_zeroline=False)

# Fig 2B
layout = go.Layout(title='Framewise displacement over time for all functional runs - '+sub,
        xaxis = dict(title = 'Functional volumes'),
        yaxis=dict(title='FD per task and run (mm)', range=[0.0, 0.5]))
fig2b = go.Figure(layout=layout)
i = 0
for colname in cols_tasksruns:
    data.append(df_fd[colname].to_numpy())
    fig2b.add_trace(go.Scatter(y=data[i], mode='lines', line = dict(color=sequential.Inferno[i+3], width=2), name=colname.capitalize()))
    i += 1
fig2b.update_layout(xaxis_showgrid=False, xaxis_zeroline=False)



#Fig 3
sub = 'sub-001'
braintsnr_tsv = os.path.join(data_dir, sub+'_task-rest_run-1_echo-2_desc-rapreproc_braintsnr.tsv')
GMtsnr_tsv = os.path.join(data_dir, sub+'_task-rest_run-1_echo-2_desc-rapreproc_GMtsnr.tsv')
WMtsnr_tsv = os.path.join(data_dir, sub+'_task-rest_run-1_echo-2_desc-rapreproc_WMtsnr.tsv')
CSFtsnr_tsv = os.path.join(data_dir, sub+'_task-rest_run-1_echo-2_desc-rapreproc_CSFtsnr.tsv')
df_braintsnr = pd.read_csv(braintsnr_tsv, sep='\t').dropna()
df_GMtsnr = pd.read_csv(GMtsnr_tsv, sep='\t').dropna()
df_WMtsnr = pd.read_csv(WMtsnr_tsv, sep='\t').dropna()
df_CSFtsnr = pd.read_csv(CSFtsnr_tsv, sep='\t').dropna()
dat1 = df_braintsnr['tsnr'].to_numpy()
dat2 = df_GMtsnr['tsnr'].to_numpy()
dat3 = df_WMtsnr['tsnr'].to_numpy()
dat4 = df_CSFtsnr['tsnr'].to_numpy()
layout = go.Layout(
        yaxis = dict(title = 'Masks'),
        xaxis=dict(title='Temporal signal-to-noise ratio (tSNR)', range=[-20, 250]),
        margin={
              't': 10,
            })
fig3 = go.Figure(layout=layout)
fig3.add_trace(go.Violin(x=dat1, line_color=sequential.Inferno[5], name='Brain'))
fig3.add_trace(go.Violin(x=dat2, line_color=sequential.Inferno[6], name='GM'))
fig3.add_trace(go.Violin(x=dat3, line_color=sequential.Inferno[7], name='WM'))
fig3.add_trace(go.Violin(x=dat4, line_color=sequential.Inferno[8], name='CSF'))
fig3.update_traces(orientation='h', side='positive', width=3, points=False)
fig3.update_layout(xaxis_showgrid=False, xaxis_zeroline=False)






main_md = dcc.Markdown('''
Hello!
''')

layout = html.Div([
            dcc.Store(id="store"),
            html.Div([
                dbc.Tabs(
                    [
                        dbc.Tab(label="Head movement", tab_id="head_movement"),
                        dbc.Tab(label="tSNR", tab_id="tsnr"),
                    ],
                    id="tabs",
                    active_tab="head_movement",
                ),],
                style={
                    'marginBottom': 25,
                    'marginTop': 25,
                    'marginLeft': '5%',
                    'maxWidth': '90%',
                    'textAlign': 'left'
                }
            ),
            html.Div(id="tab-content", className="p-4",
                style={
                    'marginBottom': 25,
                    'marginTop': 25,
                    'marginLeft': '5%',
                    'maxWidth': '90%',
                }),
])



# Callback for updating tsnr html and figure based on drop1, radio1, radio2 values
@app.callback(
    [Output('target2', 'src'),
     Output('fig3', 'figure')],
    [Input('drop1','value'),
     Input('radio1','value'),
     Input('radio2','value')]
)
def reset_tsnr_imgs(sub, task, run):

    html_fn = '/assets/' + sub + '_task-' + task + '_run-' + run + '_echo-2_space-MNI152_desc-rapreproc_tsnr.html'

    braintsnr_tsv = os.path.join(data_dir, sub+'_task-' + task + '_run-' + run + '_echo-2_desc-rapreproc_braintsnr.tsv')
    GMtsnr_tsv = os.path.join(data_dir, sub+'_task-' + task + '_run-' + run + '_echo-2_desc-rapreproc_GMtsnr.tsv')
    WMtsnr_tsv = os.path.join(data_dir, sub+'_task-' + task + '_run-' + run + '_echo-2_desc-rapreproc_WMtsnr.tsv')
    CSFtsnr_tsv = os.path.join(data_dir, sub+'_task-' + task + '_run-' + run + '_echo-2_desc-rapreproc_CSFtsnr.tsv')
    df_braintsnr = pd.read_csv(braintsnr_tsv, sep='\t').dropna()
    df_GMtsnr = pd.read_csv(GMtsnr_tsv, sep='\t').dropna()
    df_WMtsnr = pd.read_csv(WMtsnr_tsv, sep='\t').dropna()
    df_CSFtsnr = pd.read_csv(CSFtsnr_tsv, sep='\t').dropna()
    dat1 = df_braintsnr['tsnr'].to_numpy()
    dat2 = df_GMtsnr['tsnr'].to_numpy()
    dat3 = df_WMtsnr['tsnr'].to_numpy()
    dat4 = df_CSFtsnr['tsnr'].to_numpy()
    layout = go.Layout(
            yaxis = dict(title = 'Masks'),
            xaxis=dict(title='Temporal signal-to-noise ratio (tSNR)', range=[-20, 250]),
            # autosize=False,
            # width=500,
            margin={
                  't': 0,
                })
    fig3 = go.Figure(layout=layout)
    fig3.add_trace(go.Violin(x=dat1, line_color=sequential.Inferno[5], name='Brain'))
    fig3.add_trace(go.Violin(x=dat2, line_color=sequential.Inferno[6], name='GM'))
    fig3.add_trace(go.Violin(x=dat3, line_color=sequential.Inferno[7], name='WM'))
    fig3.add_trace(go.Violin(x=dat4, line_color=sequential.Inferno[8], name='CSF'))
    fig3.update_traces(orientation='h', side='positive', width=3, points=False)
    fig3.update_layout(xaxis_showgrid=False, xaxis_zeroline=False)

    return [html_fn, fig3]



# Callback for updating Fig2 based on Fig1 clickData
@app.callback(
    Output('fig2', 'figure'),
    [Input('fig1', 'clickData')]
)
def update_graph(clickData):
    if clickData is None:
        raise PreventUpdate
    else:
        selected_sub = clickData['points'][0]['x']
        fd_fn = os.path.join(data_dir, selected_sub+'_task-all_run-all_desc-fd.tsv')
        df_fd = pd.read_csv(fd_fn, sep='\t')
        data = []
        layout = go.Layout(title='Distributions of framewise displacement for all functional runs - '+selected_sub,
                xaxis = dict(title = 'Task and Run'),
                yaxis=dict(title='Framewise displacement (mm)'))
        fig2 = go.Figure(layout=layout)
        i = 0
        for colname in cols_tasksruns:
            data.append(df_fd[colname].to_numpy())
            fig2.add_trace(go.Violin(y=data[i], line_color=sequential.Inferno[i+3], name=colname.capitalize(), orientation='v', side='positive', width=1.5, points=False, box_visible=True, meanline_visible=True))
            i += 1
        fig2.update_layout(xaxis_showgrid=False, xaxis_zeroline=False)

        return fig2



@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab")],
)
def render_tab_content(active_tab):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab is not None:
        if active_tab == "head_movement":
            return [
                html.H2('Head movement', style={'textAlign': 'center'}),
                dbc.Row(
                    dbc.Col(
                        dcc.Graph(figure=fig, id='fig1')
                    )
                ),
                dbc.Row(
                    dbc.Col(
                        dcc.Graph(figure=fig2, id='fig2')
                    )
                ),
                dbc.Row(
                    dbc.Col(
                        dcc.Graph(figure=fig2b, id='fig2')
                    )
                ),
                ]
        elif active_tab == "tsnr":
            return [
                html.H2('tSNR', style={'textAlign': 'center'}),
                html.Br([]),
                dbc.Row([
                    dbc.Col([
                        dbc.Row(dbc.Col([
                            # dbc.Label('Participant'),
                            dcc.Dropdown(
                                id='drop1',
                                options=sub_opts,
                                value='sub-001',
                            )],
                        )),
                        dbc.Row(dbc.Col([
                            # dbc.Label('Task'),
                            dbc.RadioItems(
                                options=task_opts,
                                value='rest',
                                id="radio1",
                                inline=True,
                            )],
                        )),
                        dbc.Row(dbc.Col([
                            # dbc.Label('Run'),
                            dbc.RadioItems(
                                options=run_opts,
                                value='1',
                                id="radio2",
                                inline=True,
                            )],
                        )),
                        html.Br([]),
                        dbc.Row(dbc.Col([
                            # dbc.Label('Run'),
                            html.Iframe(id='target2', src='/assets/sub-001_task-rest_run-1_echo-2_space-MNI152_desc-rapreproc_tsnr.html', style={'border': 'none', 'width': '100%', 'height': 250})],
                        )),
                    ], width={"size": 6, "offset": 0}),
                    dbc.Col([

                        dcc.Graph(figure=fig3, id='fig3')],
                        style={
                            'textAlign': 'left',
                        },
                        width={"size": 6, "offset": 0}
                    ),
                ]),

                html.Br([]),
                html.Br([]),
                html.Br([]),

                # dbc.Row(
                #         [
                #             dbc.Col([
                #                 dbc.Label('Participant'),
                #                 dcc.Dropdown(
                #                     id='drop1',
                #                     options=sub_opts,
                #                     value='sub-005',
                #                 )],
                #                 width={"size": 2, "offset": 0}, # figure out offset
                #             ),
                #             dbc.Col([
                #                 dbc.Label('Task'),
                #                 dbc.RadioItems(
                #                     options=task_opts,
                #                     value='rest',
                #                     id="radio1",
                #                     inline=True,
                #                 )],
                #                 width={"size": 4, "offset": 0}, # figure out offset
                #             ),
                #             dbc.Col([
                #                 dbc.Label('Run'),
                #                 dbc.RadioItems(
                #                     options=run_opts,
                #                     value='1',
                #                     id="radio2",
                #                     inline=True,
                #                 )],
                #                 width={"size": 3, "offset": 0}, # figure out offset
                #             ),
                #         ],
                #         justify="start"
                # ),
                html.Br([]),
                dbc.Row(
                    # dbc.Col([
                    #     html.Iframe(id='target2', src='/assets/viewer.html', style={'border': 'none', 'width': '50%', 'height': 250}),
                    #     dcc.Graph(figure=fig3, id='fig3')],
                    #     style={
                    #         'textAlign': 'left',
                    #     }
                    # )
                ),
                ]
    return "No tab selected"








def writeElement(i, col, dataframe):
    if col == 'doi':
        hrf = 'https://doi.org/'+dataframe.iloc[i][col]
        return html.A([dataframe.iloc[i][col]], href=hrf, target="_blank")
    else:
        return dataframe.iloc[i][col]