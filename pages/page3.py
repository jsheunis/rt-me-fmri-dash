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
from plotly.io import write_html
import numpy as np
import json
import math

# Directories
data_dir = '../rt-me-fmri-data'

# Filenames

tsnrgm_fn = os.path.join(data_dir, 'sub-all_task-all_run-all_desc-tsnrgm.tsv')
tsnrwm_fn = os.path.join(data_dir, 'sub-all_task-all_run-all_desc-tsnrwm.tsv')
tsnrcsf_fn = os.path.join(data_dir, 'sub-all_task-all_run-all_desc-tsnrcsf.tsv')
tsnrbrain_fn = os.path.join(data_dir, 'sub-all_task-all_run-all_desc-tsnrbrain.tsv')

# Get data
participants_fn = os.path.join(data_dir, 'participants.tsv')
df_participants = pd.read_csv(participants_fn, sep='\t')

# Dataset specifics
all_subs = list(df_participants['participant_id'])
tasks = ['rest', 'motor', 'emotion']
runs = ['1', '2']
sub_opts = [{'label': sub, 'value': sub} for sub in all_subs]
task_opts = [{'label': task.capitalize(), 'value': task} for task in tasks]
run_opts = [{'label': 'Run '+run, 'value': run} for run in runs]
ts_names = ['t2starFIT', 'combinedMEt2starFIT', 'combinedMEte', 'combinedMEt2star', 'combinedMEtsnr', 'echo-2']
ts_opts = [{'label': ts, 'value': ts} for ts in ts_names]
tasks_1stlevel = ['motor', 'emotion']
tasks_1stlevel_opts = [{'label': task.capitalize(), 'value': task} for task in tasks_1stlevel]

summary_figs = ['peak', 'mean']
summary_fig_opts = [{'label': summary_fig.capitalize(), 'value': summary_fig} for summary_fig in summary_figs]

tsnr_regions = ['whole brain', 'lmotor', 'bamygdala']
tsnr_regions_labels = ['Whole brain', 'Left motor cortex', 'Bilateral amygdala']
tsnr_region_opts = [{'label': tsnr_regions_labels[i], 'value': region} for i, region in enumerate(tsnr_regions)]

tsnr_runs = ['all runs', 'motor_1', 'emotion_1', 'rest_2', 'motor_2', 'emotion_2']
tsnr_run_opts = [{'label': run.capitalize(), 'value': run} for run in tsnr_runs]

clusters = ['FWE', 'noFWE', 'anatROI', 'fweAND', 'fweOR']
cluster_names = ['Task (FWE)', 'Task (noFWE)', 'Atlas-based', 'All TS task (AND)', 'All TS task (OR)']
clusters_opts = [{'label': cluster_names[i], 'value': c} for i, c in enumerate(clusters)]

# echo_colnames = {'echo2', 'combTSNR', 'combT2STAR', 'combTE', 'combT2STARfit', 'T2STARfit'};
# cluster_colnames = {'FWE', 'noFWE', 'anatROI', 'fweAND', 'fweOR'};

# -------
# FIGURES
# -------
fig_tsnr_persub = go.Figure()
fig_tsnr_mean = go.Figure()
fig_clusters = go.Figure()
fig_tvals_summary = go.Figure()
fig_effect_summary = go.Figure()
fig_tvals_persub = go.Figure()
fig_effect_persub = go.Figure()
fig_psc_persub = go.Figure()
fig_psc_timeseries = go.Figure()
fig_psc_summary = go.Figure()


# -------------------------------------------------- #
# -------------------------------------------------- #
# -------------------------------------------------- #
# -------------------------------------------------- #
# -------------------------------------------------- #
# -------------------------------------------------- #

# ---------
# LAYOUT
# ---------


layout = html.Div([
    dcc.Store(id="store"),
    html.Div([
        dbc.Tabs(
            [
                dbc.Tab(label="Methods", tab_id="me-methods"),
                dbc.Tab(label="tSNR", tab_id="tsnr-page3"),
                dbc.Tab(label="Task regions", tab_id="clusters"),
                dbc.Tab(label="Contrast values", tab_id="cvals"),
                dbc.Tab(label="T-statistic values", tab_id="tvals"),
                dbc.Tab(label="Perc. signal change", tab_id="pscvals"),

            ],
            id="tabs-page3",
            active_tab="me-methods",
        ),],
        style={
            'marginBottom': 25,
            'marginTop': 25,
            'marginLeft': '5%',
            'maxWidth': '90%',
            'textAlign': 'left'
        }
    ),
    html.Div(id="tab-content-page3", className="p-4",
        style={
            'marginBottom': 25,
            'marginTop': 25,
            'marginLeft': '5%',
            'maxWidth': '90%',
        }
    ),
])



# ---------
# CALLBACKS
# ---------

# TSNR PER SUB: UPDATE FIGURE
@app.callback(
     Output('fig_tsnr_mean', 'figure'),
    [Input('drop_regions_tsnrsummary','value'),
     Input('drop_runs_tsnrsummary','value')]
)
def reset_tsnr_summary(tsnr_region, tsnr_run):
    layout = go.Layout(
            yaxis = dict(title = 'Mean tSNR in gray matter', range=[0, 250]),
            xaxis = dict(title='Time series'),
            margin = {
                  't': 10,
                })
    fig_tsnr_mean = go.Figure(layout=layout)

    if tsnr_region == 'whole brain':
        tsnrmean_fn = os.path.join(data_dir, 'sub-all_task-all_run-all_desc-GMtsnrmean.tsv')
    else:
        tsnrmean_fn = os.path.join(data_dir, 'sub-all_task-all_run-all_desc-' + tsnr_region + 'GMtsnrmean.tsv')

    df_tsnrmean = pd.read_csv(tsnrmean_fn, sep='\t')
    data2 = []
    ts_names2 = ['echo-2', 'combinedMEtsnr', 'combinedMEt2star', 'combinedMEte', 'combinedMEt2starFIT', 't2starFIT']

    if tsnr_run == 'all runs':
        cols_tasksruns = ['motor_1', 'emotion_1', 'rest_2', 'motor_2', 'emotion_2']
    else:
        cols_tasksruns = [tsnr_run]

    for x, ts in enumerate(ts_names2):
        for c, coltaskrun in enumerate(cols_tasksruns):
            txt = coltaskrun + '_' + ts
            if c == 0:
                temp_dat = df_tsnrmean[txt].to_numpy()
            else:
                temp_dat = np.concatenate((temp_dat, df_tsnrmean[txt].to_numpy()))
        data2.append(temp_dat)
        fig_tsnr_mean.add_trace(go.Violin(y=data2[x], line_color=sequential.Inferno[3+x], name=ts, points='all', pointpos=-0.4, meanline_visible=True, width=1, side='positive', box_visible=True))

    fig_tsnr_mean.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, violinmode='group') # , legend={'traceorder':'reversed'}

    return fig_tsnr_mean


# TSNR PER SUB: UPDATE FIGURE
@app.callback(
     Output('fig_tsnr_persub', 'figure'),
    [Input('drop_subs','value'),
     Input('radio_tasks_tsnr','value'),
     Input('radio_runs_tsnr','value')]
)
def reset_metsnr_imgs(sub, task, run):

    layout = go.Layout(
        yaxis = dict(title = 'Time series'),
        xaxis=dict(title='Temporal signal-to-noise ratio (tSNR) in Gray Matter', range=[-20, 300]),
        height = 600,
        margin={
              't': 10,
            })
    fig_tsnr_persub = go.Figure(layout=layout)
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
        fig_tsnr_persub.add_trace(go.Violin(x=data[x], line_color=sequential.Inferno[8-x], name=ts, points=False))

    fig_tsnr_persub.update_traces(orientation='h', side='positive', width=2, box_visible=True, meanline_visible=True)
    fig_tsnr_persub.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, legend={'traceorder':'reversed'})

    return fig_tsnr_persub



# TSNR PER SUB: UPDATE RADIO BUTTONS
@app.callback(
     [Output('radio_runs_tsnr', 'options'),
      Output('radio_runs_tsnr', 'value')],
    [Input('radio_tasks_tsnr','value')],
    [State('radio_runs_tsnr', 'value')]
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




# T-VALUES SUMMARY: UPDATE FIGURE
@app.callback(
     Output('fig_tvals_summary', 'figure'),
    [Input('radio_tasks_tvalsummary','value'),
     Input('radio_runs_tvalsummary','value'),
     Input('drop_opts_tvalsummary','value'),
     Input('drop_clusteropts_tvalsummary','value')]
)
def reset_tval_summary_img(task, run, summary_opt, cluster_opt):
    layout = go.Layout(
        yaxis = dict(title = 'T-values', range=[0, 40]),
        xaxis = dict(title='Time series'),
        margin = {
              't': 10,
            })
    fig_tvals_summary = go.Figure(layout=layout)

    tval_fn = os.path.join(data_dir, 'sub-all_task-' + task + '_run-' + run + '_desc-' + summary_opt +'Tvalues.tsv')
    df_tval = pd.read_csv(tval_fn, sep='\t')
    data = []
    # ts_names3 = ['echo-2', 'combinedMEtsnr', 'combinedMEt2star', 'combinedMEte', 'combinedMEt2starFIT', 't2starFIT']
    ts_names = ['echo-2', 'combinedMEtsnr', 'combinedMEt2star', 'combinedMEte', 'combinedMEt2starFIT', 't2starFIT']
    ts_colnames = ['echo2', 'combTSNR', 'combT2STAR', 'combTE', 'combT2STARfit', 'T2STARfit']

    for x, ts in enumerate(ts_colnames):
        txt = ts + '_' + cluster_opt
        temp_dat = df_tval[txt].to_numpy()
        data.append(temp_dat)
        fig_tvals_summary.add_trace(go.Violin(y=data[x], line_color=sequential.Viridis[3+x], name=ts_names[x], points='all', pointpos=-0.4, meanline_visible=True, width=1, side='positive', box_visible=True))

    fig_tvals_summary.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, violinmode='group') # , legend={'traceorder':'reversed'}

    return fig_tvals_summary



# T-VALUES PER SUB: UPDATE FIGURE
@app.callback(
     Output('fig_tvals_persub', 'figure'),
    [Input('drop_subs_tvals','value'),
     Input('radio_tasks_tvals','value'),
     Input('radio_runs_tvals','value'),
     Input('drop_clusteropts_tvals','value')]
)
def reset_tval_imgs(sub, task, run, cluster_opt):

    layout = go.Layout(
        yaxis = dict(title = 'Time series'),
        xaxis=dict(title='T-value distributions', range=[0, 40]),
        margin={
              't': 10,
            })
    fig_tvals_persub = go.Figure(layout=layout)

    data = []
    ts_names2 = ['echo-2', 'combinedMEtsnr', 'combinedMEt2star', 'combinedMEte', 'combinedMEt2starFIT', 't2starFIT']
    ts_names3 = ['echo2_FWE', 'echo2_noFWE', 'combTSNR_FWE', 'combTSNR_noFWE', 'combT2STAR_FWE', 'combT2STAR_noFWE', 'combTE_FWE', 'combTE_noFWE', 'combT2STARfit_FWE', 'combT2STARfit_noFWE', 'T2STARfit_FWE', 'T2STARfit_noFWE']
    ts_colnames = ['echo2', 'combTSNR', 'combT2STAR', 'combTE', 'combT2STARfit', 'T2STARfit']
    tval_fn = os.path.join(data_dir, sub+'_task-'+task+'_run-'+run+'_desc-tmapvalues.tsv')
    df_tvals = pd.read_csv(tval_fn, sep='\t')

    for x, ts in enumerate(ts_colnames[::-1]):
        txt = ts + '_' + cluster_opt
        new_dat = df_tvals[txt].dropna().to_numpy()

        data.append(new_dat)
        fig_tvals_persub.add_trace(go.Violin(x=data[x], line_color=sequential.Viridis[8-x], name=ts_names2[5-x], points=False))

    fig_tvals_persub.update_traces(orientation='h', side='positive', width=2, box_visible=True, meanline_visible=True)
    fig_tvals_persub.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, legend={'traceorder':'reversed'})

    return fig_tvals_persub







# EFFECT SIZES SUMMARY: UPDATE FIGURE
@app.callback(
     Output('fig_effect_summary', 'figure'),
    [Input('radio_tasks_effectsummary','value'),
     Input('radio_runs_effectsummary','value'),
     Input('drop_opts_effectsummary','value'),
     Input('drop_clusteropts_effectsummary','value')]
)
def reset_effect_summary_img(task, run, summary_opt, cluster_opt):
    layout = go.Layout(
            yaxis = dict(title = 'Effect size'),
            xaxis = dict(title='Time series'),
            margin = {
                  't': 10,
                })
    fig_effect_summary = go.Figure(layout=layout)

    cval_fn = os.path.join(data_dir, 'sub-all_task-' + task + '_run-' + run + '_desc-' + summary_opt +'Cvalues.tsv')
    df_cval = pd.read_csv(cval_fn, sep='\t')
    data = []
    ts_names = ['echo-2', 'combinedMEtsnr', 'combinedMEt2star', 'combinedMEte', 'combinedMEt2starFIT', 't2starFIT']
    ts_colnames = ['echo2', 'combTSNR', 'combT2STAR', 'combTE', 'combT2STARfit', 'T2STARfit']

    for x, ts in enumerate(ts_colnames):
        txt = ts + '_' + cluster_opt
        temp_dat = df_cval[txt].to_numpy()
        data.append(temp_dat)
        fig_effect_summary.add_trace(go.Violin(y=data[x], line_color=sequential.Viridis[3+x], name=ts_names[x], points='all', pointpos=-0.4, meanline_visible=True, width=1, side='positive', box_visible=True))

    fig_effect_summary.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, violinmode='group')
    return fig_effect_summary



# EFFECT SIZES PER SUBJECT: UPDATE FIGURE
@app.callback(
     Output('fig_effect_persub', 'figure'),
    [Input('drop_subs_effect','value'),
     Input('radio_tasks_effect','value'),
     Input('radio_runs_effect','value'),
     Input('drop_clusteropts_effect','value')]
)
def reset_contrast_imgs(sub, task, run, cluster_opt):

    layout = go.Layout(
        yaxis = dict(title = 'Time series'),
        xaxis=dict(title='Effect size (a.u.)', range=[0, 15]),
        margin={
              't': 10,
            })
    fig_effect_persub = go.Figure(layout=layout)

    data = []
    ts_colnames = ['echo2', 'combTSNR', 'combT2STAR', 'combTE', 'combT2STARfit', 'T2STARfit']
    ts_names2 = ['echo-2', 'combinedMEtsnr', 'combinedMEt2star', 'combinedMEte', 'combinedMEt2starFIT', 't2starFIT']
    ts_names3 = ['echo2_FWE', 'echo2_noFWE', 'combTSNR_FWE', 'combTSNR_noFWE', 'combT2STAR_FWE', 'combT2STAR_noFWE', 'combTE_FWE', 'combTE_noFWE', 'combT2STARfit_FWE', 'combT2STARfit_noFWE', 'T2STARfit_FWE', 'T2STARfit_noFWE']
    cval_fn = os.path.join(data_dir, sub+'_task-'+task+'_run-'+run+'_desc-cmapvalues.tsv')
    df_cvals = pd.read_csv(cval_fn, sep='\t')

    for x, ts in enumerate(ts_colnames[::-1]):
        txt = ts + '_' + cluster_opt
        new_dat = df_cvals[txt].dropna().to_numpy()

        data.append(new_dat)
        fig_effect_persub.add_trace(go.Violin(x=data[x], line_color=sequential.Viridis[8-x], name=ts_names2[5-x], points=False))

    fig_effect_persub.update_traces(orientation='h', side='positive', width=2, box_visible=True, meanline_visible=True)
    fig_effect_persub.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, legend={'traceorder':'reversed'})

    return fig_effect_persub



# PERCENTAGE SIGNAL CHANGE SUMMARY: UPDATE FIGURE
@app.callback(
     Output('fig_psc_summary', 'figure'),
    [Input('radio_tasks_pscsummary','value'),
     Input('radio_runs_pscsummary','value'),
     Input('drop_opts_pscsummary','value'),
     Input('drop_clusteropts_pscsummary','value')]
)
def reset_psc_summary_img(task, run, summary_opt, cluster_opt):
    layout = go.Layout(
            yaxis = dict(title = 'Precentage signal change'),
            xaxis = dict(title='Time series'),
            margin = {
                  't': 10,
                })
    fig_psc_summary = go.Figure(layout=layout)
    psc_fn = os.path.join(data_dir, 'sub-all_task-' + task + '_run-' + run + '_desc-' + summary_opt +'PSCvalues.tsv')
    df_psc = pd.read_csv(psc_fn, sep='\t')
    data = []
    ts_names = ['echo-2', 'combinedMEtsnr', 'combinedMEt2star', 'combinedMEte', 'combinedMEt2starFIT', 't2starFIT']
    ts_colnames = ['echo2', 'combTSNR', 'combT2STAR', 'combTE', 'combT2STARfit', 'T2STARfit']

    for x, ts in enumerate(ts_colnames):
        txt = ts + '_' + cluster_opt
        temp_dat = df_psc[txt].to_numpy()
        data.append(temp_dat)
        fig_psc_summary.add_trace(go.Violin(y=data[x], line_color=sequential.Viridis[3+x], name=ts_names[x], points='all', pointpos=-0.4, meanline_visible=True, width=1, side='positive', box_visible=True))
    fig_psc_summary.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, violinmode='group') # , legend={'traceorder':'reversed'}
    return fig_psc_summary



# PERCENTAGE SIGNAL CHANGE PER SUBJECT: UPDATE FIGURES
@app.callback(
    [Output('fig_psc_persub', 'figure'),
     Output('fig_psc_timeseries', 'figure')],
    [Input('drop_subs_psc','value'),
     Input('radio_tasks_psc','value'),
     Input('radio_runs_psc','value'),
     Input('drop_clusteropts_psc','value')]
)
def reset_psc_imgs(sub, task, run, cluster_opt):

    layout = go.Layout(
        yaxis = dict(title = 'Time series'),
        xaxis=dict(title='Percentage signal change', range=[-5, 10]),
        margin={
              't': 10,
            })
    fig_psc_persub = go.Figure(layout=layout)

    data = []
    ts_names2 = ['echo-2', 'combinedMEtsnr', 'combinedMEt2star', 'combinedMEte', 'combinedMEt2starFIT', 't2starFIT']
    ts_names3 = ['echo2_FWE', 'echo2_noFWE', 'combTSNR_FWE', 'combTSNR_noFWE', 'combT2STAR_FWE', 'combT2STAR_noFWE', 'combTE_FWE', 'combTE_noFWE', 'combT2STARfit_FWE', 'combT2STARfit_noFWE', 'T2STARfit_FWE', 'T2STARfit_noFWE']
    ts_colnames = ['echo2', 'combTSNR', 'combT2STAR', 'combTE', 'combT2STARfit', 'T2STARfit']

    # for x, ts in enumerate(ts_colnames):
    #     txt = ts + '_' + cluster_opt
    psc_fn = os.path.join(data_dir, sub+'_task-'+task+'_run-'+run+'_desc-PSCvalues.tsv')
    df_psc = pd.read_csv(psc_fn, sep='\t')

    for x, ts in enumerate(ts_colnames[::-1]):
        txt = ts + '_' + cluster_opt
        new_dat = df_psc[txt].dropna().to_numpy()
        data.append(new_dat)
        fig_psc_persub.add_trace(go.Violin(x=data[x], line_color=sequential.Viridis[8-x], name=ts_names2[5-x], points=False))

    fig_psc_persub.update_traces(orientation='h', side='positive', width=2, box_visible=True, meanline_visible=True)
    fig_psc_persub.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, legend={'traceorder':'reversed'})

    layout = go.Layout(
        yaxis = dict(title = 'Percentage signal change', range=[-2, 2]),
        xaxis=dict(title='Time (functional volumes)'),
        margin={
              't': 10,
            })
    fig_psc_timeseries = go.Figure(layout=layout)

    psc_ts_fn = os.path.join(data_dir, sub+'_task-'+task+'_run-'+run+'_desc-PSCtimeseries.tsv')
    df_psc_ts = pd.read_csv(psc_ts_fn, sep='\t')
    ts_names4 = ['echo2', 'combTSNR', 'combT2STAR', 'combTE', 'combT2STARfit', 'T2STARfit']
    data_pscts = []
    for i, ts in enumerate(ts_colnames):
        txt = ts + '_' + cluster_opt
        data_pscts.append(df_psc_ts[txt].to_numpy())
        fig_psc_timeseries.add_trace(go.Scatter(y=data_pscts[i], mode='lines', line = dict(color=sequential.Viridis[3+i], width=2), name=ts_names2[i] ))
        fig_psc_timeseries.update_yaxes(showticklabels=True)

    fig_psc_timeseries.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False)

    return [fig_psc_persub, fig_psc_timeseries]



# CLUSTERS: UPDATE FIGURE
@app.callback(
     Output('fig_clusters', 'figure'),
    [Input('radio_tasks_clusters','value'),
     Input('radio_runs_clusters','value')]
)
def reset_cluster_img(task, run):
    layout = go.Layout(
        yaxis = dict(title = '1st level task cluster sizes', range=[-500, 5500]),
        xaxis = dict(title='Time series'),
        margin = {
              't': 10,
            })
    fig_clusters = go.Figure(layout=layout)
    tvalclusters_fn = os.path.join(data_dir, 'sub-all_task-all_run-all_desc-TclusterSizes.tsv')
    df_tvalclusters = pd.read_csv(tvalclusters_fn, sep='\t')
    data_cluster = []
    ts_names2 = ['echo-2', 'combinedMEtsnr', 'combinedMEt2star', 'combinedMEte', 'combinedMEt2starFIT', 't2starFIT']
    ts_names3 = ['echo2_FWE', 'echo2_noFWE', 'combTSNR_FWE', 'combTSNR_noFWE', 'combT2STAR_FWE', 'combT2STAR_noFWE', 'combTE_FWE', 'combTE_noFWE', 'combT2STARfit_FWE', 'combT2STARfit_noFWE', 'T2STARfit_FWE', 'T2STARfit_noFWE']

    # only use FWE: ts_names3[0::2]
    taskrun = task + '_' + run
    for x, ts in enumerate(ts_names3[0::2]):
        txt = taskrun + '_' + ts
        temp_dat_cluster = df_tvalclusters[txt].to_numpy()
        data_cluster.append(temp_dat_cluster)
        fig_clusters.add_trace(go.Violin(y=data_cluster[x], line_color=sequential.Viridis[3+x], name=ts_names2[x], points='all', pointpos=-0.4, meanline_visible=True, width=1, side='positive', box_visible=True))
    fig_clusters.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, violinmode='group') # , legend={'traceorder':'reversed'}
    return fig_clusters



@app.callback(
    Output("example-output", "children"),
    [Input("example-button", "n_clicks"),
     Input('fig_tsnr_mean', 'figure'),
     Input('fig_tvals_summary', 'figure'),
     Input('fig_clusters', 'figure')]
)
def on_button_click(n, fig_tsnr_mean, fig_tvals_summary, fig_clusters):
    if n is None:
        return "Not clicked."
    else:
        write_html(fig_tsnr_mean, os.path.join(data_dir, 'fig_tsnr_mean.html'))
        write_html(fig_tvals_summary, os.path.join(data_dir, 'fig_tvals_summary.html'))
        write_html(fig_clusters, os.path.join(data_dir, 'fig_clusters.html'))
        return f"{n}"




# UPDATE PAGE 3 LAYOUT BASED ON TAB SELECTION
@app.callback(
    Output("tab-content-page3", "children"),
    [Input("tabs-page3", "active_tab")],
)
def render_tab_content_page3(active_tab):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    md_tsnr_1 = dcc.Markdown('''
    Whole brain temporal signal-to-noise ratios (tSNR) were calculated for all 6 time series, i.e.:
    - the single echo time series (echo 2),
    - all of the combined time series (x4),
    - and the T2\*-FIT time series.
    The distribution of mean tSNR in gray matter is shown below, per time series, for all runs of all participants (excluding the template run)
    
    The regions (whole brain, amygdala, motor cortex) and the runs (All runs, or individual runs) can be selected from the respective dropdowns to update the figure. 
    ''')

    md_tsnr_2 = dcc.Markdown('''
    To get a more representative view of the distribution of tSNR values for the various time series,
    the inputs below can be used to view whole brain gray matter tSNR per participant, task, and run.
    ''')

    md_cluster_1 = dcc.Markdown('''
    1st level analysis was done on all 6 time series, per task and per run (i.e. 6x2x2 = 24 times).
    After thresholding of the resulting statistical maps (FWE, p < 0.05, extent threshold = 0), surviving cluster sizes were calculated in terms of the number of voxels.
    These are shown below per task and run (use the radio buttons to switch between the options).  
    ''')

    md_cluster_2 = dcc.Markdown('''
    Several other clusters / regions were prepared within which the statistical values and other results of the multi-echo time series are calculated and compared.
    The abovementioned thresholding of the statistical maps resulting from 1st-level analysis is shortened as `Task (FWE)`.
    A less stringent threshold was also applied (no FWE, p < 0.001, 20 voxel extent threshold) and was shortened `Task (noFWE)`.
    The anatomical ROI derived from an atlas-based region (from the Jülich atlas) mapped to the subject functional space is called `Atlas-based`.
    Then, the FWE thresholded cluster images from all 6 time series were combined using both a logical AND and a logical OR.
    These are shortened as `All TS task (AND)` and `All TS task (OR)` respectively. 
    
    ''')

    md_tval_1 = dcc.Markdown('''
    T-statistic values resulting from 1st-level analysis, and corresponding to the contrast values, were extracted for each of the 6 time series within the defined regions/clusters.
    The peak and mean values were calculated. This was done for all tasks and runs (2x2). 
    Below, the dropdowns and radio buttons can be used to update the figure.
    For a detailed explanation of the options in the task region dropdown, see the bottom of the "Task regions" tab page.
      
    ''')

    md_tval_2 = dcc.Markdown('''
    Here you can view the T-value distributions (within a selected region) of all time series per subject, task, and run.
    ''')

    md_effectsize_1 = dcc.Markdown('''
    Contrast values (no units) resulting from 1st-level analysis were extracted for each of the 6 time series within the defined regions/clusters.
    The peak and mean values were calculated. This was done for all tasks and runs (2x2). 
    Below, the dropdowns and radio buttons can be used to update the figure.
    For a detailed explanation of the options in the task region dropdown, see the bottom of the "Task regions" tab page.
    ''')

    md_effectsize_2 = dcc.Markdown('''
    Here you can view the contrast value distributions (within a selected region) of all time series per subject, task, and run. 
    ''')

    md_psc_1 = dcc.Markdown('''
    Contrast values (no units) resulting from 1st-level analysis were extracted for each of the 6 time series within the defined regions/clusters.
    These were converted to percentage signal change (PSC) in order to provide a standardised effect size measure ([method described here](http://www.sbirc.ed.ac.uk/cyril/bold_percentage/BOLD_percentage.html)).
    The peak and mean values were then calculated. This was done for all tasks and runs (2x2). 
    Below, the dropdowns and radio buttons can be used to update the figure.
    For a detailed explanation of the options in the task region dropdown, see the bottom of the "Task regions" tab page.
    ''')

    md_psc_2 = dcc.Markdown('''
    Here you can view the percentage signal change distributions (within a selected region) of all time series per subject, task, run.
    ''')

    md_psc_3 = dcc.Markdown('''
    For the same subject, task, run, and region/cluster selected above, this figure shows the 6 time series in terms of percentage signal change.
    This percentage signal change was calculated per voxel and time point with regards to the particular time series mean,
    and then averaged over all voxels within each selected region respectively.   
    ''')

    md_methods_1 = dcc.Markdown('''
    Below is an overview of the main concepts and analysis steps that are followed to generate the main results for this work:
    - Echo combination for signal recovery
    - Echo combination weights
    - Combining multi-echo data
    - Comparing the resulting timeseries
    
    The measures resulting from these analysis steps can be explored using the various tabs on this page (tSNR, 1st-level clusters, etc)
    ''')

    md_methods_2 = dcc.Markdown('''One of the main known uses and benefits of multi-echo fMRI is echo-combination for signal recovery in areas of dropout.
    In a standard single-echo fMRI sequence, each volume is acquired at an echo time (after transverse excitation) that is optimized for the best whole brain contrast,
    which is close to the average T2\* value of whole brain grey matter.
    This results in sub-optimal region-specific contrasts due to the fact that T2\* varies across the brain, roughly as a function of local tissue type.
    By acquiring multiple images along the signal decay curve, one can use a simplified Bloch-equation to estimate local signal decay parameters,
    which can in turn be used as weighting factors in a multi-echo combination procedure.
    This can yield combined fMRI data with less signal dropout and improved local BOLD sensitivity.
    ''')

    md_methods_3 = dcc.Markdown('''Combination of multi-echo data usually occurs via a weighted combination.
    Weights can take on scalar values that are constant or that vary spatially across the brain.
    Typical combinations include: T2\*-weighted, tSNR-weighted, and TE-weighted.
    For this data, prior weights are calculated from the template functional run, i.e. `task-rest_run-1`.
    ''')

    md_methods_4 = dcc.Markdown('''Additionally, decay parameters T2\* and S0 can also be estimated per volume (and thus in real-time),
    after which the so-called T2\*-FIT map can be used as the weighting factor to combine that specific multi-echo volume.
    ''')

    md_methods_5 = dcc.Markdown('''For this pipeline, each functional run (excluding the template run) are combined using various combination schemes.
    To allow fair comparison with an accepted baseline (i.e. "what would results from standard fMRI look like?"), the middle/2nd echo timeseries (with TE=28ms) is also extracted as is.
    Additionally, the T2\*-FIT time series is extracted too. This yields 6 resulting time series for each single multi-echo time series: the 2nd echo, 4 combined time series and the T2\*-FIT time series.
    ''')

    md_methods_6 = dcc.Markdown('''Finally, several analysis steps are run on each of the 6 time series to allow comparison.
    ''')

    md_methods_7 = dcc.Markdown(''' 
    ''')

    if active_tab is not None:
        if active_tab == "me-methods":
            return [
                html.H2('Multi-echo analysis methods', style={'textAlign': 'center'}),
                html.H5('Summary'),
                md_methods_1,
                html.Br([]),
                html.H5('Multi-echo combination'),
                md_methods_2,
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            html.Br([]),
                            html.Br([]),
                            html.Img(src="/assets/me_fig_recovery.png", width="100%")],
                            style={
                                'textAlign': 'center'
                            }
                        ),
                    ], width={"size": 5, "offset": 1}),
                    dbc.Col([
                        html.Div(
                            html.Img(src="/assets/me_math2.png", width="100%"),
                            style={
                                'textAlign': 'center'
                            }
                        ),
                    ], width={"size": 5, "offset": 1}),
                ]),

                html.Br([]),
                html.H5('Multi-echo combination weights'),
                md_methods_3,
                html.Br([]),
                html.Div(
                    html.Img(src="/assets/me_fig_priorweights.png", width="60%"),
                    style={
                        'textAlign': 'center'
                    }
                ),
                html.Br([]),
                md_methods_4,
                html.Div(
                    html.Img(src="/assets/me_fig_rtT2star.png", width="60%"),
                    style={
                        'textAlign': 'center'
                    }
                ),
                html.Br([]),
                html.Br([]),
                html.H5('Combining multi-echo data'),
                md_methods_5,
                html.Div(
                    html.Img(src="/assets/me_fig_combinedTS.png", width="60%"),
                    style={
                        'textAlign': 'center'
                    }
                ),
                html.Br([]),
                html.Br([]),
                html.H5('Comparing resulting data'),
                md_methods_6,
                html.Br([]),
                html.Div(
                    html.Img(src="/assets/me_fig_compare.png", width="60%"),
                    style={
                        'textAlign': 'center'
                    }
                ),
            ]
        elif active_tab == "tsnr-page3":
            return [
                html.H2('tSNR in gray matter', style={'textAlign': 'center'}),
                html.H5('Mean tSNR'),
                md_tsnr_1,
                html.Br([]),
                dbc.Row([
                    dbc.Col([
                        dbc.Row(dbc.Col([
                            dcc.Dropdown(
                                id='drop_regions_tsnrsummary',
                                options=tsnr_region_opts,
                                value='whole brain',
                            )
                            ],
                        )),
                    ], width={"size": 3, "offset": 2}),
                    dbc.Col([
                        dbc.Row(dbc.Col([
                            dcc.Dropdown(
                                id='drop_runs_tsnrsummary',
                                options=tsnr_run_opts,
                                value='all runs',
                            )
                            ],
                        )),
                    ], width={"size": 2, "offset": 2}),
                ]),
                dbc.Row([
                    dbc.Col([

                        dcc.Graph(figure=fig_tsnr_mean, id='fig_tsnr_mean')],
                        style={
                            'textAlign': 'left',
                        },
                        width={"size": 12, "offset": 0}
                    ),

                ]),
                html.H5('tSNR distributions'),
                md_tsnr_2,
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
                                id="radio_tasks_tsnr",
                                inline=True,
                            )],
                        )),
                        html.Br([]),
                        dbc.Row(dbc.Col([
                            # dbc.Label('Run'),
                            dbc.RadioItems(
                                options=run_opts,
                                value='2',
                                id="radio_runs_tsnr",
                                inline=True,
                            )],
                        )),
                    ], width={"size": 3, "offset": 0}),
                    dbc.Col([

                        dcc.Graph(figure=fig_tsnr_persub, id='fig_tsnr_persub')],
                        style={
                            'textAlign': 'left',
                        },
                        width={"size": 9, "offset": 0}
                    ),
                ]),
                ]
        elif active_tab == "clusters":
            return [
                html.H2('Task regions and sizes', style={'textAlign': 'center'}),
                html.H5('1st-level cluster sizes'),
                md_cluster_1,
                html.Br([]),
                dbc.Row([
                    dbc.Col([
                        dbc.Row(dbc.Col([
                            # dbc.Label('Task'),
                            dbc.RadioItems(
                                options=tasks_1stlevel_opts,
                                value='motor',
                                id="radio_tasks_clusters",
                                inline=True,
                            )],
                        )),
                    ], width={"size": 4, "offset": 2}),
                    dbc.Col([
                        dbc.Row(dbc.Col([
                            # dbc.Label('Run'),
                            dbc.RadioItems(
                                options=run_opts,
                                value='1',
                                id="radio_runs_clusters",
                                inline=True,
                            )],
                        )),
                    ], width={"size": 5, "offset": 1}),
                ]),
                dbc.Row([
                    dbc.Col([

                        dcc.Graph(figure=fig_clusters, id='fig_clusters')],
                        style={
                            'textAlign': 'left',
                        },
                        width={"size": 12, "offset": 0}
                    ),

                ]),
                html.H5('Clusters/regions for comparisons'),
                md_cluster_2,
                ]
        elif active_tab == "tvals":
            return [
                html.H2('T-statistic values', style={'textAlign': 'center'}),
                html.H5('T-statistic summary'),
                md_tval_1,
                html.Br([]),
                dbc.Row([
                    dbc.Col([
                        dbc.Row(dbc.Col([
                            dcc.Dropdown(
                                id='drop_opts_tvalsummary',
                                options=summary_fig_opts,
                                value='peak',
                            )
                            ],
                        )),
                    ], width={"size": 2, "offset": 1}),
                    dbc.Col([
                        dbc.Row(
                            dbc.Col([
                                dbc.RadioItems(
                                    options=tasks_1stlevel_opts,
                                    value='motor',
                                    id="radio_tasks_tvalsummary",
                                    inline=True,
                                )],
                            )
                        ),
                    ], width={"size": 2, "offset": 1}),
                    dbc.Col([
                        dbc.Row(
                            dbc.Col([
                                dbc.RadioItems(
                                    options=run_opts,
                                    value='1',
                                    id="radio_runs_tvalsummary",
                                    inline=True,
                                )],
                            )
                        ),
                    ], width={"size": 2, "offset": 0}),
                    dbc.Col([
                        dbc.Row(dbc.Col([
                            dcc.Dropdown(
                                id='drop_clusteropts_tvalsummary',
                                options=clusters_opts,
                                value='FWE',
                            )
                            ],
                        )),
                    ], width={"size": 2, "offset": 1}),
                ]),
                dbc.Row([
                    dbc.Col([

                        dcc.Graph(figure=fig_tvals_summary, id='fig_tvals_summary')],
                        style={
                            'textAlign': 'left',
                        },
                        width={"size": 12, "offset": 0}
                    ),

                ]),
                html.Br([]),
                html.H5('T-statistic distributions'),
                md_tval_2,
                html.Br([]),
                dbc.Row([
                    dbc.Col([
                        dbc.Row(dbc.Col([
                            # dbc.Label('Participant'),
                            dcc.Dropdown(
                                id='drop_subs_tvals',
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
                                id="radio_tasks_tvals",
                                inline=True,
                            )],
                        )),
                        html.Br([]),
                        dbc.Row(dbc.Col([
                            # dbc.Label('Run'),
                            dbc.RadioItems(
                                options=run_opts,
                                value='1',
                                id="radio_runs_tvals",
                                inline=True,
                            )],
                        )),
                        html.Br([]),
                        dbc.Row(dbc.Col([
                            dcc.Dropdown(
                                id='drop_clusteropts_tvals',
                                options=clusters_opts,
                                value='FWE',
                            )],
                        )),
                    ], width={"size": 3, "offset": 0}),
                    dbc.Col([

                        dcc.Graph(figure=fig_tvals_persub, id='fig_tvals_persub')],
                        style={
                            'textAlign': 'left',
                        },
                        width={"size": 9, "offset": 0}
                    ),
                ]),
                ]
        elif active_tab == "cvals":
            return [
                html.H2('Contrast values', style={'textAlign': 'center'}),
                html.H5('Contrast value summary'),
                md_effectsize_1,
                html.Br([]),
                dbc.Row([
                    dbc.Col([
                        dbc.Row(dbc.Col([
                            dcc.Dropdown(
                                id='drop_opts_effectsummary',
                                options=summary_fig_opts,
                                value='peak',
                            )
                            ],
                        )),
                    ], width={"size": 2, "offset": 1}),
                    dbc.Col([
                        dbc.Row(
                            dbc.Col([
                                dbc.RadioItems(
                                    options=tasks_1stlevel_opts,
                                    value='motor',
                                    id="radio_tasks_effectsummary",
                                    inline=True,
                                )],
                            )
                        ),
                    ], width={"size": 2, "offset": 1}),
                    dbc.Col([
                        dbc.Row(
                            dbc.Col([
                                dbc.RadioItems(
                                    options=run_opts,
                                    value='1',
                                    id="radio_runs_effectsummary",
                                    inline=True,
                                )],
                            )
                        ),
                    ], width={"size": 2, "offset": 0}),
                    dbc.Col([
                        dbc.Row(dbc.Col([
                            dcc.Dropdown(
                                id='drop_clusteropts_effectsummary',
                                options=clusters_opts,
                                value='FWE',
                            )
                            ],
                        )),
                    ], width={"size": 2, "offset": 1}),
                ]),
                dbc.Row([
                    dbc.Col([

                        dcc.Graph(figure=fig_effect_summary, id='fig_effect_summary')],
                        style={
                            'textAlign': 'left',
                        },
                        width={"size": 12, "offset": 0}
                    ),

                ]),
                html.H5('Contrast value distributions'),
                md_effectsize_2,
                html.Br([]),
                dbc.Row([
                    dbc.Col([
                        dbc.Row(dbc.Col([
                            # dbc.Label('Participant'),
                            dcc.Dropdown(
                                id='drop_subs_effect',
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
                                id="radio_tasks_effect",
                                inline=True,
                            )],
                        )),
                        html.Br([]),
                        dbc.Row(dbc.Col([
                            # dbc.Label('Run'),
                            dbc.RadioItems(
                                options=run_opts,
                                value='1',
                                id="radio_runs_effect",
                                inline=True,
                            )],
                        )),
                        html.Br([]),
                        dbc.Row(dbc.Col([
                            dcc.Dropdown(
                                id='drop_clusteropts_effect',
                                options=clusters_opts,
                                value='FWE',
                            )],
                        )),
                    ], width={"size": 3, "offset": 0}),
                    dbc.Col([

                        dcc.Graph(figure=fig_effect_persub, id='fig_effect_persub')],
                        style={
                            'textAlign': 'left',
                        },
                        width={"size": 9, "offset": 0}
                    ),
                ])
            ]
        elif active_tab == "pscvals":
            return [
                html.H2('Percentage signal change', style={'textAlign': 'center'}),
                html.H5('PSC summary'),
                md_psc_1,
                html.Br([]),
                dbc.Row([
                    dbc.Col([
                        dbc.Row(dbc.Col([
                            dcc.Dropdown(
                                id='drop_opts_pscsummary',
                                options=summary_fig_opts,
                                value='peak',
                            )
                            ],
                        )),
                    ], width={"size": 2, "offset": 1}),
                    dbc.Col([
                        dbc.Row(
                            dbc.Col([
                                dbc.RadioItems(
                                    options=tasks_1stlevel_opts,
                                    value='motor',
                                    id="radio_tasks_pscsummary",
                                    inline=True,
                                )],
                            )
                        ),
                    ], width={"size": 2, "offset": 1}),
                    dbc.Col([
                        dbc.Row(
                            dbc.Col([
                                dbc.RadioItems(
                                    options=run_opts,
                                    value='1',
                                    id="radio_runs_pscsummary",
                                    inline=True,
                                )],
                            )
                        ),
                    ], width={"size": 2, "offset": 0}),
                    dbc.Col([
                        dbc.Row(dbc.Col([
                            dcc.Dropdown(
                                id='drop_clusteropts_pscsummary',
                                options=clusters_opts,
                                value='FWE',
                            )
                            ],
                        )),
                    ], width={"size": 2, "offset": 1}),
                ]),
                dbc.Row([
                    dbc.Col([

                        dcc.Graph(figure=fig_psc_summary, id='fig_psc_summary')],
                        style={
                            'textAlign': 'left',
                        },
                        width={"size": 12, "offset": 0}
                    ),

                ]),
                html.H5('PSC distributions in selected cluster/ROI'),
                md_psc_2,
                html.Br([]),
                dbc.Row([
                    dbc.Col([
                        dbc.Row(dbc.Col([
                            # dbc.Label('Participant'),
                            dcc.Dropdown(
                                id='drop_subs_psc',
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
                                id="radio_tasks_psc",
                                inline=True,
                            )],
                        )),
                        html.Br([]),
                        dbc.Row(dbc.Col([
                            # dbc.Label('Run'),
                            dbc.RadioItems(
                                options=run_opts,
                                value='1',
                                id="radio_runs_psc",
                                inline=True,
                            )],
                        )),
                        html.Br([]),
                        dbc.Row(dbc.Col([
                            dcc.Dropdown(
                                id='drop_clusteropts_psc',
                                options=clusters_opts,
                                value='FWE',
                            )],
                        )),
                    ], width={"size": 3, "offset": 0}),
                    dbc.Col([

                        dcc.Graph(figure=fig_psc_persub, id='fig_psc_persub')],
                        style={
                            'textAlign': 'left',
                        },
                        width={"size": 9, "offset": 0}
                    ),
                ]),
                html.H5('PSC time series in selected cluster/ROI'),
                md_psc_3,
                html.Br([]),
                dbc.Row([
                    dbc.Col([

                        dcc.Graph(figure=fig_psc_timeseries, id='fig_psc_timeseries')],
                        style={
                            'textAlign': 'left',
                        },
                        width={"size": 12, "offset": 0}
                    ),

                ]),
            ]

    return "No tab selected"