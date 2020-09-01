# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
from app import app
import os
from plotly.colors import sequential, n_colors
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import numpy as np
import json
import math

# Directories
data_dir = '../rt-me-fmri-data'

# Filenames
participants_fn = os.path.join(data_dir, 'participants.tsv')
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
# ts_names = ['echo-2', 'combinedMEtsnr', 'combinedMEt2star', 'combinedMEte', 'combinedMEt2starFIT', 't2starFIT']
ts_names = ['t2starFIT', 'combinedMEt2starFIT', 'combinedMEte', 'combinedMEt2star', 'combinedMEtsnr', 'echo-2']
ts_opts = [{'label': ts, 'value': ts} for ts in ts_names]

tasks_1stlevel = ['motor', 'emotion']
tasks_1stlevel_opts = [{'label': task.capitalize(), 'value': task} for task in tasks_1stlevel]


#Fig 3.1
layout = go.Layout(
        yaxis = dict(title = 'Time series'),
        xaxis=dict(title='tSNR in gray matter', range=[-20, 280]),
        margin={
              't': 10,
            })
fig3_1 = go.Figure(layout=layout)


#Fig 3.2
tsnrmean_fn = os.path.join(data_dir, 'sub-all_task-all_run-all_desc-GMtsnrmean.tsv')
df_tsnrmean = pd.read_csv(tsnrmean_fn, sep='\t')

layout = go.Layout(
        yaxis = dict(title = 'Mean tSNR in gray matter', range=[0, 200]),
        xaxis = dict(title='Time series'),
        margin = {
              't': 10,
            })
fig3_2 = go.Figure(layout=layout)

data2 = []
ts_names2 = ['echo-2', 'combinedMEtsnr', 'combinedMEt2star', 'combinedMEte', 'combinedMEt2starFIT', 't2starFIT']
cols_tasksruns2 = ['motor_1', 'emotion_1', 'rest_2', 'motor_2', 'emotion_2']
for x, ts in enumerate(ts_names2):

    for c, coltaskrun in enumerate(cols_tasksruns2):
        txt = coltaskrun + '_' + ts
        if c == 0:
            temp_dat = df_tsnrmean[txt].to_numpy()
        else:
            temp_dat = np.concatenate((temp_dat, df_tsnrmean[txt].to_numpy()))


    data2.append(temp_dat)
    fig3_2.add_trace(go.Violin(y=data2[x], line_color=sequential.Inferno[3+x], name=ts, points='all', pointpos=-0.4, meanline_visible=True, width=1, side='positive', box_visible=True))

# fig3_2.update_traces(orientation='h', side='positive', width=2, box_visible=True, meanline_visible=True)fig.update_layout(violinmode='group')
fig3_2.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, violinmode='group') # , legend={'traceorder':'reversed'}



# Fig 3.3 AND 3.4
layout = go.Layout(
        yaxis = dict(title = 'Peak T-values', range=[0, 40]),
        xaxis = dict(title='Time series'),
        margin = {
              't': 10,
            })
fig3_3 = go.Figure(layout=layout)
layout = go.Layout(
        yaxis = dict(title = '1st level task cluster sizes'),
        xaxis = dict(title='Time series'),
        margin = {
              't': 10,
            })
fig3_4 = go.Figure(layout=layout)


tvalpeak_fn = os.path.join(data_dir, 'sub-all_task-all_run-all_desc-peakTvalues.tsv')
df_tvalpeak = pd.read_csv(tvalpeak_fn, sep='\t')
tvalclusters_fn = os.path.join(data_dir, 'sub-all_task-all_run-all_desc-TclusterSizes.tsv')
df_tvalclusters = pd.read_csv(tvalclusters_fn, sep='\t')
data_peak = []
data_cluster = []
# ts_names3 = ['echo-2', 'combinedMEtsnr', 'combinedMEt2star', 'combinedMEte', 'combinedMEt2starFIT', 't2starFIT']
ts_names2 = ['echo-2', 'combinedMEtsnr', 'combinedMEt2star', 'combinedMEte', 'combinedMEt2starFIT', 't2starFIT']
ts_names3 = ['echo2_FWE', 'echo2_noFWE', 'combTSNR_FWE', 'combTSNR_noFWE', 'combT2STAR_FWE', 'combT2STAR_noFWE', 'combTE_FWE', 'combTE_noFWE', 'combT2STARfit_FWE', 'combT2STARfit_noFWE', 'T2STARfit_FWE', 'T2STARfit_noFWE']
cols_tasksruns3 = ['motor_1', 'emotion_1', 'motor_2', 'emotion_2']
cols_tasksruns3 = ['motor_1']


# only use FWE: ts_names3[0::2]
for taskrun in cols_tasksruns3:
    for x, ts in enumerate(ts_names3[0::2]):
        txt = taskrun + '_' + ts
        temp_dat_peak = df_tvalpeak[txt].to_numpy()
        temp_dat_cluster = df_tvalclusters[txt].to_numpy()
        data_peak.append(temp_dat_peak)
        data_cluster.append(temp_dat_cluster)
        fig3_3.add_trace(go.Violin(y=data_peak[x], line_color=sequential.Viridis[3+x], name=ts_names2[x], points='all', pointpos=-0.4, meanline_visible=True, width=1, side='positive', box_visible=True))
        fig3_4.add_trace(go.Violin(y=data_cluster[x], line_color=sequential.Viridis[3+x], name=ts_names2[x], points='all', pointpos=-0.4, meanline_visible=True, width=1, side='positive', box_visible=True))

# fig3_2.update_traces(orientation='h', side='positive', width=2, box_visible=True, meanline_visible=True)fig.update_layout(violinmode='group')
fig3_3.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, violinmode='group') # , legend={'traceorder':'reversed'}
fig3_4.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, violinmode='group') # , legend={'traceorder':'reversed'}

# Fig 3.4


# Fig 3.5
layout = go.Layout(
        yaxis = dict(title = 'T-value distributions in thresholded clusters', range=[0, 40]),
        xaxis = dict(title='Time series'),
        margin = {
              't': 10,
            })
fig3_5 = go.Figure(layout=layout)


# -------------------------------------------------- #
# -------------------------------------------------- #
# -------------------------------------------------- #
# -------------------------------------------------- #
# -------------------------------------------------- #
# -------------------------------------------------- #

main_md1 = dcc.Markdown('''
Temporal signal-to-noise ratios (tSNR) were calculated for the single echo time series (echo 2), all of the combined time series (x4), and the T2*-FIT time series.
The mean tSNR in gray matter is shown below, per time series, for all runs of all participants (excluding the template run, i.e. Rest run 1) 
''')

main_md2 = dcc.Markdown('''
To get a more representative picture of the distribution of tSNR values for the various time series,
the inputs below can be used to view tSNR per participant, task, and run.
''')

main_md3 = dcc.Markdown('''
''')

layout = html.Div([

    html.H2('Multi-echo measures',
    style={
        'textAlign': 'center',
        'marginBottom': 25,
        'marginTop': 25,
    }),
    html.Br([]),
    html.H5('Mean gray matter tSNR'),
    main_md1,
    html.Br([]),
    dbc.Row([
        dbc.Col([

            dcc.Graph(figure=fig3_2, id='fig3_2')],
            style={
                'textAlign': 'left',
            },
            width={"size": 12, "offset": 0}
        ),

    ]),
    html.H5('Gray matter tSNR distributions'),
    main_md2,
    html.Br([]),
    dbc.Row([
        dbc.Col([
            dbc.Row(dbc.Col([
                # dbc.Label('Participant'),
                dcc.Dropdown(
                    id='drop_subs',
                    options=sub_opts,
                    value='sub-001',
                )],
            )),
            html.Br([]),
            dbc.Row(dbc.Col([
                # dbc.Label('Task'),
                dbc.RadioItems(
                    options=task_opts,
                    value='rest',
                    id="radio_tasks",
                    inline=True,
                )],
            )),
            html.Br([]),
            dbc.Row(dbc.Col([
                # dbc.Label('Run'),
                dbc.RadioItems(
                    options=run_opts,
                    value='2',
                    id="radio_runs",
                    inline=True,
                )],
            )),
        ], width={"size": 3, "offset": 0}),
        dbc.Col([

            dcc.Graph(figure=fig3_1, id='fig3_1')],
            style={
                'textAlign': 'left',
            },
            width={"size": 9, "offset": 0}
        ),
    ]),
    html.Br([]),
    html.H5('1st level task peak T-values'),
    main_md1,
    html.Br([]),
    dbc.Row([
        dbc.Col([

            dcc.Graph(figure=fig3_3, id='fig3_3')],
            style={
                'textAlign': 'left',
            },
            width={"size": 12, "offset": 0}
        ),

    ]),
    html.Br([]),
    html.H5('1st level task cluster sizes'),
    main_md1,
    html.Br([]),
    dbc.Row([
        dbc.Col([

            dcc.Graph(figure=fig3_4, id='fig3_4')],
            style={
                'textAlign': 'left',
            },
            width={"size": 12, "offset": 0}
        ),

    ]),
    html.H5('1st level T-value distributions'),
    main_md3,
    html.Br([]),
    dbc.Row([
        dbc.Col([
            dbc.Row(dbc.Col([
                # dbc.Label('Participant'),
                dcc.Dropdown(
                    id='drop_subs2',
                    options=sub_opts,
                    value='sub-001',
                )],
            )),
            html.Br([]),
            dbc.Row(dbc.Col([
                # dbc.Label('Task'),
                dbc.RadioItems(
                    options=tasks_1stlevel_opts,
                    value='motor',
                    id="radio_tasks2",
                    inline=True,
                )],
            )),
            html.Br([]),
            dbc.Row(dbc.Col([
                # dbc.Label('Run'),
                dbc.RadioItems(
                    options=run_opts,
                    value='1',
                    id="radio_runs2",
                    inline=True,
                )],
            )),
        ], width={"size": 3, "offset": 0}),
        dbc.Col([

            dcc.Graph(figure=fig3_5, id='fig3_5')],
            style={
                'textAlign': 'left',
            },
            width={"size": 9, "offset": 0}
        ),
    ]),
    ],
    style={
        'marginBottom': 25,
        'marginTop': 25,
        'marginLeft': '5%',
        'maxWidth': '90%',
    }
)



# Callback for updating figure based on drop1, radio1, radio2 values
@app.callback(
     Output('fig3_1', 'figure'),
    [Input('drop_subs','value'),
     Input('radio_tasks','value'),
     Input('radio_runs','value')]
)
def reset_metsnr_imgs(sub, task, run):

    layout = go.Layout(
        yaxis = dict(title = 'Time series'),
        xaxis=dict(title='Temporal signal-to-noise ratio (tSNR) in Gray Matter', range=[-20, 300]),
        height = 600,
        margin={
              't': 10,
            })
    fig3_1 = go.Figure(layout=layout)

    data = []

    for x, ts in enumerate(ts_names):
        if x == 5:
            GMtsnr_tsv = os.path.join(data_dir, sub+'_task-'+task+'_run-'+run+'_echo-2_desc-rapreproc_GMtsnr.tsv')
        else:
            GMtsnr_tsv = os.path.join(data_dir, sub+'_task-'+task+'_run-'+run+'_desc-' + ts + '_GMtsnr.tsv')

        df_GMtsnr = pd.read_csv(GMtsnr_tsv, sep='\t').dropna()

        new_dat = df_GMtsnr['tsnr'].to_numpy()

        if x == 0:
            new_dat[new_dat < 0] = math.nan
            new_dat[new_dat > 500] = math.nan

        data.append(new_dat)
        fig3_1.add_trace(go.Violin(x=data[x], line_color=sequential.Inferno[8-x], name=ts, points=False))

        # if x == 0:
        #     fig3_1.add_trace(go.Violin(x=data[x], line_color=sequential.Inferno[3+x], name=ts, points='all'))
        # else:
        #     fig3_1.add_trace(go.Violin(x=data[x], line_color=sequential.Inferno[3+x], name=ts, points=False))

    fig3_1.update_traces(orientation='h', side='positive', width=2, box_visible=True, meanline_visible=True)
    fig3_1.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, legend={'traceorder':'reversed'})

    return fig3_1



# Callback for updating run values
@app.callback(
     [Output('radio_runs', 'options'),
      Output('radio_runs', 'value')],
    [Input('radio_tasks','value')],
    [State('radio_runs', 'value')]
)
def reset_metsnr_imgs(task, run):

    if task == 'rest':
        options = [
            {'label': 'Run 1', 'value': '1', 'disabled': True},
            {'label': 'Run 2', 'value': '2'},
        ]
        run_out = '2'
    else:
        options = [
            {'label': 'Run 1', 'value': '1'},
            {'label': 'Run 2', 'value': '2'},
        ]
        run_out = run

    return [options, run_out]




# Callback for updating figure based on drop2... values
@app.callback(
     Output('fig3_5', 'figure'),
    [Input('drop_subs2','value'),
     Input('radio_tasks2','value'),
     Input('radio_runs2','value')]
)
def reset_tval_imgs(sub, task, run):

    layout = go.Layout(
        yaxis = dict(title = 'Time series'),
        xaxis=dict(title='T-values', range=[0, 40]),
        margin={
              't': 10,
            })
    fig3_5 = go.Figure(layout=layout)

    data = []
    ts_names2 = ['echo-2', 'combinedMEtsnr', 'combinedMEt2star', 'combinedMEte', 'combinedMEt2starFIT', 't2starFIT']
    ts_names3 = ['echo2_FWE', 'echo2_noFWE', 'combTSNR_FWE', 'combTSNR_noFWE', 'combT2STAR_FWE', 'combT2STAR_noFWE', 'combTE_FWE', 'combTE_noFWE', 'combT2STARfit_FWE', 'combT2STARfit_noFWE', 'T2STARfit_FWE', 'T2STARfit_noFWE']
    tval_fn = os.path.join(data_dir, sub+'_task-'+task+'_run-'+run+'_desc-tmapvalues.tsv')
    df_tvals = pd.read_csv(tval_fn, sep='\t')

    for x, ts in enumerate(ts_names3[-2::-2]):


        new_dat = df_tvals[ts].dropna().to_numpy()

        data.append(new_dat)
        fig3_5.add_trace(go.Violin(x=data[x], line_color=sequential.Viridis[8-x], name=ts_names2[5-x], points=False))

    fig3_5.update_traces(orientation='h', side='positive', width=2, box_visible=True, meanline_visible=True)
    fig3_5.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, legend={'traceorder':'reversed'})

    return fig3_5


