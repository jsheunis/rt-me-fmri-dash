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
data_dir_v2 = 'data'

# Get data
participants_fn = os.path.join(data_dir_v2, 'participants.tsv')
df_participants = pd.read_csv(participants_fn, sep='\t')

# Dataset specifics
all_subs = list(df_participants['participant_id'])
tasks = ['rest', 'motor', 'emotion']
runs = ['1', '2']
subs2 = ['sub-001', 'sub-010']
sub2_opts = [{'label': sub, 'value': sub} for sub in subs2] 
sub_opts = [{'label': sub, 'value': sub} for sub in all_subs]
task_opts = [{'label': task.capitalize(), 'value': task} for task in tasks]
run_opts = [{'label': 'Run '+run, 'value': run} for run in runs]
ts_names = ['t2starFIT', 'combinedMEt2starFIT', 'combinedMEt2star', 'combinedMEte', 'combinedMEtsnr', 'echo-2']
ts_names_disp = ['T2*FIT', 'T2*FIT-combined', 'T2*-combined', 'TE-combined', 'tSNR-combined', 'Echo 2']
ts_opts = [{'label': ts_names_disp[i], 'value': ts} for i, ts in enumerate(ts_names)]
tasks_1stlevel = ['motor', 'emotion']
tasks_1stlevel_opts = [{'label': task.capitalize(), 'value': task} for task in tasks_1stlevel]

summary_figs = ['peak', 'mean']
summary_fig_opts = [{'label': summary_fig.capitalize(), 'value': summary_fig} for summary_fig in summary_figs]

tsnr_regions = ['whole brain', 'lmotor', 'bamygdala']
tsnr_regions_labels = ['Whole brain', 'Left motor cortex', 'Bilateral amygdala']
tsnr_region_opts = [{'label': tsnr_regions_labels[i], 'value': region} for i, region in enumerate(tsnr_regions)]

tsnr_runs = ['all runs', 'motor_1', 'emotion_1', 'rest_2', 'motor_2', 'emotion_2']
tsnr_runs = ['all runs', 'fingerTapping', 'emotionProcessing', 'rest_run-2', 'fingerTappingImagined', 'emotionProcessingImagined']
tsnr_run_names = ['All runs', 'Finger tapping', 'Emotion processing', 'Rest 2', 'Finger tapping (imagined)', 'Emotion processing (imagined)']
tsnr_run_opts = [{'label': tsnr_run_names[i], 'value': run} for i, run in enumerate(tsnr_runs)]

clusters = ['FWE', 'noFWE', 'anatROI', 'fweAND', 'fweOR']
cluster_names = ['Task (FWE)', 'Task (noFWE)', 'Atlas-based', 'All TS task (AND)', 'All TS task (OR)']
clusters_opts = [{'label': cluster_names[i], 'value': c} for i, c in enumerate(clusters)]

tasks_v2 = ['rest_run-1', 'fingerTapping', 'emotionProcessing', 'rest_run-2', 'fingerTappingImagined', 'emotionProcessingImagined']
tasks_v22 = ['fingerTapping', 'emotionProcessing', 'rest_run-2', 'fingerTappingImagined', 'emotionProcessingImagined']
tasks_v2_names = ['Rest 1', 'Finger tapping', 'Emotion processing', 'Rest 2', 'Finger tapping (imagined)', 'Emotion processing (imagined)']
tasks_v22_names = ['Finger tapping', 'Emotion processing', 'Rest 2', 'Finger tapping (imagined)', 'Emotion processing (imagined)']
task_opts_v2 = [{'label': tasks_v2_names[i], 'value': task} for i, task in enumerate(tasks_v2)]
task_opts_v22 = [{'label': tasks_v22_names[i], 'value': task} for i, task in enumerate(tasks_v22)]
tasks_1stlevel_v2 = ['fingerTapping', 'emotionProcessing', 'fingerTappingImagined', 'emotionProcessingImagined']
tasks_1stlevel_v2_names = ['Finger tapping', 'Emotion processing', 'Finger tapping (imagined)', 'Emotion processing (imagined)']
tasks_1stlevel_opts_v2 = [{'label': tasks_1stlevel_v2_names[i], 'value': task} for i, task in enumerate(tasks_1stlevel_v2)]

cnr_tcnr = ['cnr', 'tcnr']
cnr_tcnr_names = ['CNR', 'tCNR']
rtcnr_fig_opts = [{'label': cnr_tcnr_names[i], 'value': val} for i, val in enumerate(cnr_tcnr)]

clusters_v2 = ['FWE', 'noFWE', 'rleftMotor', 'rbilateralAmygdala', 'rfusiformGyrus', 'AND', 'OR']
cluster_names_v2 = ['Task (FWE)', 'Task (noFWE)', 'Atlas (left motor)', 'Atlas (amygdala)', 'Atlas (fusiform gyrus)', 'All TS task (AND)', 'All TS task (OR)']
clusters_opts_v2 = [{'label': cluster_names_v2[i], 'value': c} for i, c in enumerate(clusters_v2)]

psc_types = ['glm', 'offline', 'cumulative', 'cumulativebas', 'previousbas']
psc_types_names = ['GLM', 'Offline', 'Cumulative', 'Cumulative baseline', 'Previous baseline']
psc_types_opts = [{'label': psc_types_names[i], 'value': p} for i, p in enumerate(psc_types)]

overlapData = {}
for i, task in enumerate(tasks_1stlevel_v2):
    txt = 'task-' + task
    overlapData[txt] = pd.read_csv(os.path.join(data_dir_v2, 'multiecho', 'sub-all_task-' + task + '_desc-roiOverlap.tsv'), sep='\t')

overlap_colnames_disp = ['Echo 2', 'tSNR-combined', 'TE-combined', 'T2*-combined', 'T2*FIT-combined', 'T2*FIT']
overlap_colnames = ['echo2', 'combTSNR', 'combTE', 'combT2STAR', 'combT2STARfit', 'T2STARfit']
overlap_opts = [{'label': overlap_colnames_disp[i], 'value': ts} for i, ts in enumerate(overlap_colnames)]

clusters_overlap = ['FWE', 'noFWE']
cluster_names_overlap = ['Task (FWE)', 'Task (noFWE)']
clusters_opts_overlap = [{'label': cluster_names_overlap[i], 'value': c} for i, c in enumerate(clusters_overlap)]

# echo_colnames = {'echo2', 'combTSNR', 'combT2STAR', 'combTE', 'combT2STARfit', 'T2STARfit'};
# cluster_colnames = {'FWE', 'noFWE', 'anatROI', 'fweAND', 'fweOR'};

# -------
# FIGURES
# -------
# Colormaps from https://colorbrewer2.org/#type=qualitative&scheme=Dark2&n=6
colors = [['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99', '#e31a1c'],
           ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33'],
           ['#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3', '#fdb462'],
           ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e', '#e6ab02']]
fig_tsnr_mean = go.Figure()
fig_tsnr_persub = go.Figure()
fig_clusters = go.Figure()
fig_overlap_summary = go.Figure()
fig_overlap_persub = go.Figure()
fig_tvals_summary = go.Figure()
fig_effect_summary = go.Figure()
fig_tvals_persub = go.Figure()
fig_effect_persub = go.Figure()
fig_psc_persub = go.Figure()
fig_psc_timeseries = go.Figure()
fig_psc_summary = go.Figure()
fig_cnr_offline = go.Figure()
fig_realtime_series = go.Figure()
fig_realtime_summary = go.Figure()


# Fig8
subnr = 0
vals = overlapData[txt].loc[subnr].to_numpy()
func_vals = vals[1:]
func_vals_nooverlap = vals[0] - func_vals
cols = list(overlapData[txt].columns)
cols = cols[1:]

fig8 = go.Figure(data=[
    go.Bar(name='Func/Anat overlap', x=cols, y=func_vals, marker_color=sequential.Viridis[5]),
    go.Bar(name='Anat ROI (no overlap)', x=cols, y=func_vals_nooverlap, marker_color=sequential.Viridis[8])
])
fig8.update_layout(barmode='stack', xaxis = dict(title = 'All time series', tickangle=45), yaxis = dict(title = 'Number of voxels'), margin={'t': 10})

# -------------------------------------------------- #
# -------------------------------------------------- #
# -------------------------------------------------- #
# -------------------------------------------------- #
# -------------------------------------------------- #
# -------------------------------------------------- #

# ------------ #
# ------------ #
# LAYOUT       #
# ------------ #
# ------------ #


layout = html.Div([
    dcc.Store(id="store"),
    html.Div([
        dbc.Tabs(
            [
                dbc.Tab(label="Methods", tab_id="me-methods"),
                dbc.Tab(label="tSNR", tab_id="tsnr-page3"),
                dbc.Tab(label="Task regions", tab_id="clusters"),
                dbc.Tab(label="Perc. signal change", tab_id="pscvals"),
                dbc.Tab(label="T-statistic values", tab_id="tvals"),
                dbc.Tab(label="Real-time", tab_id="realtime"),
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



# ------------ #
# ------------ #
# CALLBACKS    #
# ------------ #
# ------------ #

# TSNR MEAN: UPDATE FIGURE
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
        tsnrmean_fn = os.path.join(data_dir_v2, 'multiecho', 'sub-all_task-all_desc-GMtsnrmean.tsv')
    else:
        tsnrmean_fn = os.path.join(data_dir_v2, 'multiecho', 'sub-all_task-all_desc-' + tsnr_region + 'GMtsnrmean.tsv')


    df_tsnrmean = pd.read_csv(tsnrmean_fn, sep='\t')
    data2 = []
    ts_names2 = ['echo-2', 'combinedMEtsnr', 'combinedMEte', 'combinedMEt2star', 'combinedMEt2starFIT', 't2starFIT']
    ts_names2_disp = ['Echo 2', 'tSNR-combined', 'TE-combined', 'T2*-combined', 'T2*FIT-combined', 'T2*FIT']

    if tsnr_run == 'all runs':
        # cols_tasksruns = ['motor_1', 'emotion_1', 'rest_2', 'motor_2', 'emotion_2']
        cols_tasksruns = ['fingerTapping', 'emotionProcessing', 'rest_run-2', 'fingerTappingImagined', 'emotionProcessingImagined']
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
        fig_tsnr_mean.add_trace(go.Violin(y=data2[x], line_color=colors[3][x], name=ts_names2_disp[x], points='all', pointpos=-0.4, meanline_visible=True, width=1, side='positive', box_visible=True))

    fig_tsnr_mean.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, violinmode='group') # , legend={'traceorder':'reversed'}

    return fig_tsnr_mean


# TSNR PER SUB: UPDATE FIGURE
@app.callback(
     Output('fig_tsnr_persub', 'figure'),
    [Input('drop_subs','value'),
     Input('radio_tasks_tsnr2','value')]
)
def reset_metsnr_imgs(sub, task):

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
            GMtsnr_tsv = os.path.join(data_dir_v2, 'multiecho', sub+'_task-'+task+'_echo-2_desc-rapreproc_GMtsnr.tsv')
        else:
            GMtsnr_tsv = os.path.join(data_dir_v2, 'multiecho', sub+'_task-'+task+'_desc-' + ts + '_GMtsnr.tsv')

        df_GMtsnr = pd.read_csv(GMtsnr_tsv, sep='\t').dropna()
        new_dat = df_GMtsnr['tsnr'].to_numpy()
        if x == 0:
            new_dat[new_dat < 0] = math.nan
            new_dat[new_dat > 500] = math.nan
        data.append(new_dat)
        fig_tsnr_persub.add_trace(go.Violin(x=data[x], line_color=colors[3][5-x], name=ts_names_disp[x], points=False))

    fig_tsnr_persub.update_traces(orientation='h', side='positive', width=2, box_visible=True, meanline_visible=True, spanmode='hard')
    fig_tsnr_persub.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, legend={'traceorder':'reversed'})

    return fig_tsnr_persub


# CLUSTERS: UPDATE FIGURE
@app.callback(
     Output('fig_clusters', 'figure'),
    [Input('radio_tasks_clusters','value'),
     Input('drop_clusteropts_clusters','value')]
)
def reset_cluster_img(task, cluster):
    layout = go.Layout(
        yaxis = dict(title = 'Number of voxels', range=[-500, 5500]),
        xaxis = dict(title='Time series'),
        margin = {
              't': 10,
            })
    fig_clusters = go.Figure(layout=layout)
    tvalclusters_fn = os.path.join(data_dir_v2, 'multiecho', 'sub-all_task-all_desc-clusterSizes.tsv')
    df_tvalclusters = pd.read_csv(tvalclusters_fn, sep='\t')
    data_cluster = []
    ts_names = ['Echo 2', 'tSNR-combined', 'TE-combined', 'T2*-combined', 'T2*FIT-combined', 'T2*FIT']
    ts_names3 = ['echo2', 'combTSNR', 'combTE', 'combT2STAR', 'combT2STARfit', 'T2STARfit']

    for x, ts in enumerate(ts_names3):
        txt = task + '_' + ts + '_' + cluster
        temp_dat_cluster = df_tvalclusters[txt].to_numpy()
        data_cluster.append(temp_dat_cluster)
        fig_clusters.add_trace(go.Violin(y=data_cluster[x], line_color=colors[3][x], name=ts_names[x], points='all', pointpos=-0.4, meanline_visible=True, width=1, side='positive', box_visible=True))
    
    fig_clusters.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, violinmode='group') # , legend={'traceorder':'reversed'}
    return fig_clusters




# OVERLAP: UPDATE SUMMARY FIGURE
@app.callback(
     Output('fig_overlap_summary', 'figure'),
    [Input('radio_tasks_overlap','value'),
     Input('drop_timeseries_overlap','value'),
     Input('drop_clusteropts_overlap','value')] 
)
def reset_overlap_persub(task, timeseries, cluster):
    anat_vals = []
    func_vals = []
    func_vals_nooverlap = []
    cluster_ts_name = timeseries + '_' + cluster
    txt = 'task-' + task

    for i, sub in enumerate(all_subs):
        anat_vals.append(overlapData[txt].loc[i, 'anat_roi'])
        func_vals.append(overlapData[txt].loc[i, cluster_ts_name])
        func_vals_nooverlap.append(anat_vals[-1] - func_vals[-1])

    fig_overlap_summary = go.Figure(data=[
        go.Bar(name='Func/Anat overlap', x=all_subs, y=func_vals, marker_color=sequential.Magma[5]),
        go.Bar(name='Anat ROI (no overlap)', x=all_subs, y=func_vals_nooverlap, marker_color=sequential.Magma[7])
    ])
    # Change the bar mode
    fig_overlap_summary.update_layout(barmode='stack', xaxis = dict(title = 'All participants', tickangle=45), yaxis = dict(title = 'Number of voxels'), margin={'t': 10})

    return fig_overlap_summary


# OVERLAP: UPDATE persub FIGURE
@app.callback(
     Output('fig_overlap_persub', 'figure'),
    [Input('radio_tasks_overlap','value'),
     Input('drop_clusteropts_overlap','value'),
     Input('fig_overlap_summary','clickData')]
)
def reset_roi_img2(task, cluster, clickData):

    if clickData is None:
        selected_subnr = 0
    else:
        selected_subnr = clickData['points'][0]['pointIndex']

    txt = 'task-' + task
    vals = overlapData[txt].loc[selected_subnr].to_numpy()
    if cluster == 'FWE':
        func_vals = vals[1::2]
    else:
        func_vals = vals[2::2]
    
    func_vals_nooverlap = vals[0] - func_vals
    cols = list(overlapData[txt].columns)
    if cluster == 'FWE':
        cols = cols[1::2] #overlap_colnames_disp
    else:
        cols = cols[2::2] #overlap_colnames_disp
    

    fig_overlap_persub = go.Figure(data=[
        go.Bar(name='Func/Anat overlap', x=overlap_colnames_disp, y=func_vals, marker_color=sequential.Magma[5]),
        go.Bar(name='Anat ROI (no overlap)', x=overlap_colnames_disp, y=func_vals_nooverlap, marker_color=sequential.Magma[7])
    ])
    fig_overlap_persub.update_layout(barmode='stack', xaxis = dict(title = 'All time series', tickangle=45),
                       yaxis = dict(title = 'Number of voxels'), margin={'t': 40},
                       title='ROI overlap computed from all time series options - '+all_subs[selected_subnr])

    return fig_overlap_persub


# T-VALUES SUMMARY: UPDATE FIGURE
@app.callback(
     Output('fig_tvals_summary', 'figure'),
    [Input('radio_tasks_tvalsummary','value'),
     Input('drop_opts_tvalsummary','value'),
     Input('drop_clusteropts_tvalsummary','value')]
)
def reset_tval_summary_img(task, summary_opt, cluster_opt):
    layout = go.Layout(
        yaxis = dict(title = 'T-values'),
        xaxis = dict(title='Time series'),
        margin = {
              't': 10,
            })
    fig_tvals_summary = go.Figure(layout=layout)

    tval_fn = os.path.join(data_dir_v2, 'multiecho', 'sub-all_task-' + task + '_desc-' + summary_opt +'Tvalues.tsv')
    df_tval = pd.read_csv(tval_fn, sep='\t')
    data = []
    ts_names = ['Echo 2', 'tSNR-combined', 'TE-combined', 'T2*-combined', 'T2*FIT-combined', 'T2*FIT']
    ts_colnames = ['echo2', 'combTSNR', 'combTE', 'combT2STAR', 'combT2STARfit', 'T2STARfit']

    for x, ts in enumerate(ts_colnames):
        txt = ts + '_' + cluster_opt
        temp_dat = df_tval[txt].to_numpy()
        data.append(temp_dat)
        fig_tvals_summary.add_trace(go.Violin(y=data[x], line_color=colors[3][x], name=ts_names[x], points='all', pointpos=-0.4, meanline_visible=True, width=1, side='positive', box_visible=True))

    fig_tvals_summary.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, violinmode='group') # , legend={'traceorder':'reversed'}

    return fig_tvals_summary



# T-VALUES PER SUB: UPDATE FIGURE
@app.callback(
     Output('fig_tvals_persub', 'figure'),
    [Input('drop_subs_tvals','value'),
     Input('radio_tasks_tvals','value'),
     Input('drop_clusteropts_tvals','value')]
)
def reset_tval_imgs(sub, task, cluster_opt):

    layout = go.Layout(
        yaxis = dict(title = 'Time series'),
        xaxis=dict(title='T-value distributions', range=[0, 40]),
        margin={
              't': 10,
            })
    fig_tvals_persub = go.Figure(layout=layout)

    data = []
    ts_names2 = ['Echo 2', 'tSNR-combined', 'TE-combined', 'T2*-combined', 'T2*FIT-combined', 'T2*FIT']
    ts_colnames = ['echo2', 'combTSNR', 'combTE', 'combT2STAR', 'combT2STARfit', 'T2STARfit']
    tval_fn = os.path.join(data_dir_v2, 'multiecho', sub+'_task-'+task+'_desc-tmapvalues.tsv')
    df_tvals = pd.read_csv(tval_fn, sep='\t')

    for x, ts in enumerate(ts_colnames[::-1]):
        txt = ts + '_' + cluster_opt
        new_dat = df_tvals[txt].dropna().to_numpy()

        data.append(new_dat)
        fig_tvals_persub.add_trace(go.Violin(x=data[x], line_color=colors[3][5-x], name=ts_names2[5-x], points=False))

    fig_tvals_persub.update_traces(orientation='h', side='positive', width=2, box_visible=True, meanline_visible=True)
    fig_tvals_persub.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, legend={'traceorder':'reversed'})

    return fig_tvals_persub



# EFFECT SIZES SUMMARY: UPDATE FIGURE
@app.callback(
     Output('fig_effect_summary', 'figure'),
    [Input('radio_tasks_effectsummary','value'),
     Input('drop_opts_effectsummary','value'),
     Input('drop_clusteropts_effectsummary','value')]
)
def reset_effect_summary_img(task, summary_opt, cluster_opt):
    layout = go.Layout(
            yaxis = dict(title = 'Effect size'),
            xaxis = dict(title='Time series'),
            margin = {
                  't': 10,
                })
    fig_effect_summary = go.Figure(layout=layout)

    cval_fn = os.path.join(data_dir_v2, 'multiecho', 'sub-all_task-' + task + '_desc-' + summary_opt +'Cvalues.tsv')
    df_cval = pd.read_csv(cval_fn, sep='\t')
    data = []
    ts_names = ['Echo 2', 'tSNR-combined', 'TE-combined', 'T2*-combined', 'T2*FIT-combined', 'T2*FIT']
    ts_colnames = ['echo2', 'combTSNR', 'combTE', 'combT2STAR', 'combT2STARfit', 'T2STARfit']

    for x, ts in enumerate(ts_colnames):
        txt = ts + '_' + cluster_opt
        temp_dat = df_cval[txt].to_numpy()
        data.append(temp_dat)
        fig_effect_summary.add_trace(go.Violin(y=data[x], line_color=colors[3][x], name=ts_names[x], points='all', pointpos=-0.4, meanline_visible=True, width=1, side='positive', box_visible=True))

    fig_effect_summary.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, violinmode='group')
    return fig_effect_summary



# EFFECT SIZES PER SUBJECT: UPDATE FIGURE
@app.callback(
     Output('fig_effect_persub', 'figure'),
    [Input('drop_subs_effect','value'),
     Input('radio_tasks_effect','value'),
     Input('drop_clusteropts_effect','value')]
)
def reset_contrast_imgs(sub, task, cluster_opt):

    layout = go.Layout(
        yaxis = dict(title = 'Time series'),
        xaxis=dict(title='Effect size (a.u.)', range=[0, 15]),
        margin={
              't': 10,
            })
    fig_effect_persub = go.Figure(layout=layout)

    data = []
    ts_names2 = ['Echo 2', 'tSNR-combined', 'TE-combined', 'T2*-combined', 'T2*FIT-combined', 'T2*FIT']
    ts_colnames = ['echo2', 'combTSNR', 'combTE', 'combT2STAR', 'combT2STARfit', 'T2STARfit']
    cval_fn = os.path.join(data_dir_v2, 'multiecho', sub+'_task-'+task+'_desc-cmapvalues.tsv')
    df_cvals = pd.read_csv(cval_fn, sep='\t')

    for x, ts in enumerate(ts_colnames[::-1]):
        txt = ts + '_' + cluster_opt
        new_dat = df_cvals[txt].dropna().to_numpy()

        data.append(new_dat)
        fig_effect_persub.add_trace(go.Violin(x=data[x], line_color=colors[3][5-x], name=ts_names2[5-x], points=False))

    fig_effect_persub.update_traces(orientation='h', side='positive', width=2, box_visible=True, meanline_visible=True)
    fig_effect_persub.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, legend={'traceorder':'reversed'})

    return fig_effect_persub



# PERCENTAGE SIGNAL CHANGE SUMMARY: UPDATE FIGURE
@app.callback(
     Output('fig_psc_summary', 'figure'),
    [Input('radio_tasks_pscsummary','value'),
     Input('drop_opts_pscsummary','value'),
     Input('drop_clusteropts_pscsummary','value')]
)
def reset_psc_summary_img(task, summary_opt, cluster_opt):
    layout = go.Layout(
            yaxis = dict(title = 'Precentage signal change'), # , range=[-0.5, 2]
            xaxis = dict(title='Time series'),
            margin = {
                  't': 10,
                })
    fig_psc_summary = go.Figure(layout=layout)
    psc_fn = os.path.join(data_dir_v2, 'multiecho', 'sub-all_task-' + task +'_desc-' + summary_opt +'PSCvalues.tsv')
    df_psc = pd.read_csv(psc_fn, sep='\t')
    data = []
    ts_names = ['Echo 2', 'tSNR-combined', 'TE-combined', 'T2*-combined', 'T2*FIT-combined', 'T2*FIT']
    ts_colnames = ['echo2', 'combTSNR', 'combTE', 'combT2STAR', 'combT2STARfit', 'T2STARfit']

    for x, ts in enumerate(ts_colnames):
        txt = ts + '_' + cluster_opt
        temp_dat = df_psc[txt].to_numpy()
        data.append(temp_dat)
        fig_psc_summary.add_trace(go.Violin(y=data[x], line_color=colors[3][x], name=ts_names[x], points='all', pointpos=-0.4, meanline_visible=True, width=1, side='positive', box_visible=True))
    fig_psc_summary.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, violinmode='group') # , legend={'traceorder':'reversed'}
    return fig_psc_summary


# PSC: UPDATE OFFLINE CNR FIGURE
@app.callback(
    Output('fig_cnr_offline', 'figure'),
    [Input('drop_opts_cnroffline','value'),
     Input('radio_tasks_cnroffline','value'),
     Input('drop_clusteropts_cnroffline','value')]
)
def reset_psc_cnr_img(cnr_opt, task, cluster_opt):

    layout = go.Layout(
        xaxis = dict(title = 'Time series'),
        yaxis = dict(title='Percentage signal change', range=[-0.5, 2]),
        margin={
              't': 10,
            })
    fig_cnr_offline = go.Figure(layout=layout)
    cnr_fn = os.path.join(data_dir_v2, 'multiecho', 'sub-all_task-' + task + '_desc-offlineROI' + cnr_opt + '.tsv')
    df_cnr = pd.read_csv(cnr_fn, sep='\t')

    data = []
    ts_names = ['Echo 2', 'tSNR-combined', 'TE-combined', 'T2*-combined', 'T2*FIT-combined', 'T2*FIT']
    ts_colnames = ['echo2', 'combTSNR', 'combTE', 'combT2STAR', 'combT2STARfit', 'T2STARfit']

    # ['glm_RTecho2', 'kalm_RTecho2', 'glm_RTcombinedTSNR', 'kalm_RTcombinedTSNR', 'glm_RTcombinedT2STAR', 'kalm_RTcombinedT2STAR', 'glm_RTcombinedTE', 'kalm_RTcombinedTE', 'glm_RTcombinedRTt2star', 'kalm_RTcombinedRTt2star', 'glm_RTt2starFIT', 'kalm_RTt2starFIT', 'glm_RTs0FIT', 'kalm_RTs0FIT']

    for x, ts in enumerate(ts_colnames):
        txt = ts + '_' + cluster_opt
        temp_dat = df_cnr[txt].to_numpy()
        data.append(temp_dat)
        fig_cnr_offline.add_trace(go.Violin(y=data[x], line_color=colors[3][x], name=ts_names[x], points='all', pointpos=-0.4, meanline_visible=True, width=1, side='positive', box_visible=True))
    
    fig_cnr_offline.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, violinmode='group') # , legend={'traceorder':'reversed'}

    return fig_cnr_offline



# PERCENTAGE SIGNAL CHANGE PER SUBJECT: UPDATE FIGURES
@app.callback(
    [Output('fig_psc_persub', 'figure'),
     Output('fig_psc_timeseries', 'figure')],
    [Input('drop_subs_psc','value'),
     Input('radio_tasks_psc','value'),
     Input('drop_clusteropts_psc','value')]
)
def reset_psc_imgs(sub, task, cluster_opt):

    layout = go.Layout(
        yaxis = dict(title = 'Time series'),
        xaxis=dict(title='Percentage signal change', range=[-5, 10]),
        margin={
              't': 10,
            })
    fig_psc_persub = go.Figure(layout=layout)

    data = []
    ts_names2 = ['Echo 2', 'tSNR-combined', 'TE-combined', 'T2*-combined', 'T2*FIT-combined', 'T2*FIT']
    ts_colnames = ['echo2', 'combTSNR', 'combTE', 'combT2STAR', 'combT2STARfit', 'T2STARfit']

    psc_fn = os.path.join(data_dir_v2, 'multiecho', sub+'_task-'+task+'_desc-PSCvalues.tsv')
    df_psc = pd.read_csv(psc_fn, sep='\t')

    for x, ts in enumerate(ts_colnames[::-1]):
        txt = ts + '_' + cluster_opt
        new_dat = df_psc[txt].dropna().to_numpy()
        data.append(new_dat)
        fig_psc_persub.add_trace(go.Violin(x=data[x], line_color=colors[3][5-x], name=ts_names2[5-x], points=False))

    fig_psc_persub.update_traces(orientation='h', side='positive', width=2, box_visible=True, meanline_visible=True)
    fig_psc_persub.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, legend={'traceorder':'reversed'})

    layout = go.Layout(
        yaxis = dict(title = 'Percentage signal change', range=[-2.5, 2.5]),
        xaxis=dict(title='Time (functional volumes)'),
        margin={
              't': 10,
            })
    fig_psc_timeseries = go.Figure(layout=layout)

    psc_ts_fn = os.path.join(data_dir_v2, 'multiecho', sub+'_task-'+task+'_desc-PSCtimeseries.tsv')
    df_psc_ts = pd.read_csv(psc_ts_fn, sep='\t')
    data_pscts = []
    for i, ts in enumerate(ts_colnames):
        txt = ts + '_' + cluster_opt
        data_pscts.append(df_psc_ts[txt].to_numpy())
        fig_psc_timeseries.add_trace(go.Scatter(y=data_pscts[i], mode='lines', line = dict(color=colors[3][i], width=2), name=ts_names2[i] ))
        fig_psc_timeseries.update_yaxes(showticklabels=True)

    fig_psc_timeseries.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False)

    return [fig_psc_persub, fig_psc_timeseries]



# REALTIME: UPDATE SUMMARY FIGURE
@app.callback(
    Output('fig_realtime_summary', 'figure'),
    [Input('drop_opts_realtimesummary','value'),
     Input('radio_tasks_realtimesummary','value'),
     Input('drop_clusteropts_realtimesummary','value'),
     Input('drop_pscopts_realtimesummary','value')]
)
def reset_realtime_summary_img(cnr_opt, task, cluster_opt, psc_opt):

    layout = go.Layout(
        xaxis = dict(title = 'Time series'),
        yaxis = dict(title='Percentage signal change', range=[-0.5, 3]),
        margin={
              't': 10,
            })
    fig_realtime_summary = go.Figure(layout=layout)

    if psc_opt == 'glm':
        cnr_fn = os.path.join(data_dir_v2, 'realtime', 'sub-all_task-' + task + '_desc-' + cluster_opt +'_ROI' + cnr_opt + '.tsv')
        df_cnr = pd.read_csv(cnr_fn, sep='\t')
        data = []
        ts_names = ['Echo 2', 'tSNR-combined', 'TE-combined', 'T2*-combined', 'T2*FIT-combined', 'T2*FIT']
        rtts_colnames = ['RTecho2', 'RTcombinedTSNR', 'RTcombinedTE', 'RTcombinedT2STAR', 'RTcombinedRTt2star', 'RTt2starFIT']

        # ['glm_RTecho2', 'kalm_RTecho2', 'glm_RTcombinedTSNR', 'kalm_RTcombinedTSNR', 'glm_RTcombinedT2STAR', 'kalm_RTcombinedT2STAR', 'glm_RTcombinedTE', 'kalm_RTcombinedTE', 'glm_RTcombinedRTt2star', 'kalm_RTcombinedRTt2star', 'glm_RTt2starFIT', 'kalm_RTt2starFIT', 'glm_RTs0FIT', 'kalm_RTs0FIT']
        for x, ts in enumerate(rtts_colnames):
            txt = 'glm_' + ts
            temp_dat = df_cnr[txt].to_numpy()
            data.append(temp_dat)
            fig_realtime_summary.add_trace(go.Violin(y=data[x], line_color=colors[3][x], name=ts_names[x], points='all', pointpos=-0.4, meanline_visible=True, width=1, side='positive', box_visible=True))
        
        fig_realtime_summary.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, violinmode='group') # , legend={'traceorder':'reversed'}
    else:
        cnr_fn = os.path.join(data_dir_v2, 'realtime', 'sub-all_task-' + task + '_desc-realtimeROI' + cnr_opt + '_' + psc_opt + '.tsv')
        df_cnr = pd.read_csv(cnr_fn, sep='\t')
        data = []
        ts_names = ['Echo 2', 'tSNR-combined', 'TE-combined', 'T2*-combined', 'T2*FIT-combined', 'T2*FIT']
        rtts_colnames = ['RTecho2', 'RTcombinedTSNR', 'RTcombinedTE', 'RTcombinedT2STAR', 'RTcombinedRTt2star', 'RTt2starFIT']

        # ['glm_RTecho2', 'kalm_RTecho2', 'glm_RTcombinedTSNR', 'kalm_RTcombinedTSNR', 'glm_RTcombinedT2STAR', 'kalm_RTcombinedT2STAR', 'glm_RTcombinedTE', 'kalm_RTcombinedTE', 'glm_RTcombinedRTt2star', 'kalm_RTcombinedRTt2star', 'glm_RTt2starFIT', 'kalm_RTt2starFIT', 'glm_RTs0FIT', 'kalm_RTs0FIT']
        # realtimeROItcnr
        for x, ts in enumerate(rtts_colnames):
            txt = ts + '_' + cluster_opt
            temp_dat = df_cnr[txt].to_numpy()
            data.append(temp_dat)
            fig_realtime_summary.add_trace(go.Violin(y=data[x], line_color=colors[3][x], name=ts_names[x], points='all', pointpos=-0.4, meanline_visible=True, width=1, side='positive', box_visible=True))
        
        fig_realtime_summary.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, violinmode='group') # , legend={'traceorder':'reversed'}

    return fig_realtime_summary


# REALTIME: UPDATE TIMESERIES FIGURE
@app.callback(
    Output('fig_realtime_series', 'figure'),
    [Input('drop_subs_realtime','value'),
     Input('radio_tasks_realtimeseries','value'),
     Input('drop_clusteropts_realtimeseries','value'),
     Input('drop_pscopts_realtimeseries','value')]
)
def reset_realtime_series_img(sub, task, cluster_opt, psc_opt):

    layout = go.Layout(
        yaxis = dict(title = 'Percentage signal change', range=[-2.5, 2.5]),
        xaxis=dict(title='Time (functional volumes)'),
        margin={
              't': 10,
            })
    fig_realtime_series = go.Figure(layout=layout)

    if psc_opt == 'glm':
        psc_ts_fn = os.path.join(data_dir_v2, 'realtime', sub + '_task-' + task + '_desc-' + cluster_opt + '_ROIpsc.tsv')
        df_psc_ts = pd.read_csv(psc_ts_fn, sep='\t')
        ts_names = ['Echo 2', 'tSNR-combined', 'TE-combined', 'T2*-combined', 'T2*FIT-combined', 'T2*FIT']
        rtts_colnames = ['RTecho2', 'RTcombinedTSNR', 'RTcombinedTE', 'RTcombinedT2STAR', 'RTcombinedRTt2star', 'RTt2starFIT']
        data_pscts = []
        for i, ts in enumerate(rtts_colnames):
            txt = 'glm_' + ts
            data_pscts.append(df_psc_ts[txt].to_numpy())
            fig_realtime_series.add_trace(go.Scatter(y=data_pscts[i], mode='lines', line = dict(color=colors[3][i], width=2), name=ts_names[i] ))
            fig_realtime_series.update_yaxes(showticklabels=True)
        fig_realtime_series.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False)
    else:
        psc_ts_fn = os.path.join(data_dir_v2, 'realtime', sub + '_task-' + task + '_desc-realtimeROIsignals_psc' + psc_opt + '.tsv')
        df_psc_ts = pd.read_csv(psc_ts_fn, sep='\t')
        ts_names = ['Echo 2', 'tSNR-combined', 'TE-combined', 'T2*-combined', 'T2*FIT-combined', 'T2*FIT']
        rtts_colnames = ['RTecho2', 'RTcombinedTSNR', 'RTcombinedTE', 'RTcombinedT2STAR', 'RTcombinedRTt2star', 'RTt2starFIT']
        data_pscts = []
        for i, ts in enumerate(rtts_colnames):
            txt = ts + '_' + cluster_opt
            data_pscts.append(df_psc_ts[txt].to_numpy())
            fig_realtime_series.add_trace(go.Scatter(y=data_pscts[i], mode='lines', line = dict(color=colors[3][i], width=2), name=ts_names[i] ))
            fig_realtime_series.update_yaxes(showticklabels=True)
        fig_realtime_series.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False)

    return fig_realtime_series



# @app.callback(
#     Output('click-data', 'children'),
#     [Input('fig7', 'clickData')])
# def display_click_data(clickData):
#     return json.dumps(clickData, indent=2)



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

    *Note: due to storage limitations, the data of only two participants are available; for the app with all participant data, please refer to the about section.*
    ''')

    md_cluster_1 = dcc.Markdown('''
    Task-based GLM-analysis was done on all 6 time series of all 4 tasks, for each participant.
    Thresholding of the resulting statistical maps was done at two levels: a conservative level (FWE, p < 0.05, extent threshold = 0)
    and a less stringent threshold (no FWE, p < 0.001, 20 voxel extent threshold).
    These are shortened, respectively, as `Task (FWE)` and `Task (noFWE)`.
    In both cases, the number of surviving voxels determine the cluster size.
    
    Several other clusters / regions were also prepared within which the statistical values and other results of the multi-echo time series are calculated and compared.
    The anatomical ROI derived from an atlas-based region (from the Jülich atlas) mapped to the subject functional space is called `Atlas-based`.
    Then, the FWE-thresholded cluster images from all 6 time series (per task, per participant) were combined using both a logical AND and a logical OR procedure.
    These are shortened as `All TS task (AND)` and `All TS task (OR)` respectively. 
    ''')

    md_cluster_2 = dcc.Markdown('''
    
    
    ''')

    md_tval_1 = dcc.Markdown('''
    T-statistic values resulting from 1st-level analysis, and corresponding to the contrast values, were extracted for each of the 6 time series within the defined regions/clusters.
    The peak and mean values were calculated. This was done for all tasks and runs (2x2). 
    Below, the dropdowns and radio buttons can be used to update the figure.
    For a detailed explanation of the options in the task region dropdown, see the bottom of the "Task regions" tab page.
      
    ''')

    md_tval_2 = dcc.Markdown('''
    Here you can view the T-value distributions (within a selected region) of all time series per subject, task, and run.

    *Note: due to storage limitations, the data of only two participants are available; for the app with all participant data, please refer to the about section.*
    ''')

    md_effectsize_1 = dcc.Markdown('''
    Contrast values (no units) resulting from 1st-level analysis were extracted for each of the 6 time series within the defined regions/clusters.
    The peak and mean values were calculated. This was done for all tasks and runs (2x2). 
    Below, the dropdowns and radio buttons can be used to update the figure.
    For a detailed explanation of the options in the task region dropdown, see the bottom of the "Task regions" tab page.
    ''')

    md_effectsize_2 = dcc.Markdown('''
    Here you can view the contrast value distributions (within a selected region) of all time series per subject, task, and run. 

    *Note: due to storage limitations, the data of only two participants are available; for the app with all participant data, please refer to the about section.*
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

    *Note: due to storage limitations, the data of only two participants are available; for the app with all participant data, please refer to the about section.*
    ''')

    md_psc_3 = dcc.Markdown('''
    For the same subject, task, run, and region/cluster selected above, this figure shows the 6 time series in terms of percentage signal change.
    This percentage signal change was calculated per voxel and time point with regards to the particular time series mean,
    and then averaged over all voxels within each selected region respectively.   
    ''')


    md_psc_4 = dcc.Markdown('''
    Temporal percentage signal change (tPSC) was calculated offline for all 6 minimally processed time series.
    This was done per voxel and time point with regards to the respecitve time series mean, and then averaged over all voxels within predetermined ROIs.
    This was followed by calculations for functional contrast and temporal contrast-to-noise ratio (tCNR) within the same ROIs.
    To calculate the functional contrast in ROIs, the average tPSC in volumes classified as being part of "OFF" condition blocks are subtracted from the average signal in volumes classified as being part of each "ON" condition block.
    Visually, this corresponds to the average amplitude difference between conditions in the tPSC signal.
    To calculate tCNR, the functional contrast in an ROI is divided by the time series standard deviation of the tPSC signal in the same ROI.
    ''')

    md_methods_1 = dcc.Markdown('''
    The `rt-me-fMRI` dataset was used in the following study:

    [***Heunis et al., 2020. The effects of multi-echo fMRI combination and rapid T2\*-mapping on offline and real-time BOLD sensitivity. bioRxiv.***](https://doi.org/10.1101/2020.12.08.416768)

    The main concepts and analysis steps that were investigated include:
    - Echo combination for signal recovery
    - Echo combination weights
    - Combining multi-echo data
    - Comparing the resulting timeseries
    
    The measures resulting from these analysis steps can be explored using the various tabs on this page (**tSNR**, **Task Regions**, etc)
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
    Comparison metrics include tSNR, percentage signal change as effect size, T-statistic values, temporal percentage signal change (tPSC), functional contrasts, and temporal contrast to noise ratio (tCNR).
    These can all be explored via the tabs on this page. 
    ''')

    md_realtime_1 = dcc.Markdown('''
    All six minimally processed time series were analysed per-volume, i.e. in simulated real-time. This included:
    - Spatial smoothing using a Gaussian kernel with FWHM at 7 mm
    - Spatial averaging of voxel signals with defined ROIs
    - Cumulative GLM-based detrending of the ROI signals, including linear and quadratic trend regressors.

    These processed signals were then used to calculate per-volume temporal percentage signal change (tPSC) from mean.
    The mean was defined in several ways, including the mean of the preceding baseline "OFF" block; the cumulative mean; and the cumulative baseline "OFF" block mean.

    To calculate the functional contrast in ROIs, the average tPSC in volumes classified as being part of "OFF" condition blocks are subtracted from the average signal in volumes classified as being part of each "ON" condition block.
    Visually, this corresponds to the average amplitude difference between conditions in the tPSC signal.
    To calculate tCNR, the functional contrast in an ROI is divided by the time series standard deviation of the tPSC signal in the same ROI.
    ''')

    md_realtime_2 = dcc.Markdown('''
    The tPSC signals, as described above, are provided here per participant, task, ROI, and mean calculation-type.

    *Note: due to storage limitations, the data of only two participants are available; for the app with all participant data, please refer to the about section.*
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
                    html.Img(src="/assets/prior_weights.png", width="60%"),
                    style={
                        'textAlign': 'center'
                    }
                ),
                html.Br([]),
                md_methods_4,
                html.Div(
                    html.Img(src="/assets/rapid_t2star_mapping.png", width="60%"),
                    style={
                        'textAlign': 'center'
                    }
                ),
                html.Br([]),
                html.Br([]),
                html.H5('Combining multi-echo data'),
                md_methods_5,
                html.Div(
                    html.Img(src="/assets/combination_process.png", width="60%"),
                    style={
                        'textAlign': 'center'
                    }
                ),
                html.Br([]),
                html.Br([]),
                html.H5('Analysing and comparing resulting data'),
                md_methods_6,
                html.Br([]),
                html.Div(
                    html.Img(src="/assets/time_series_analysis.png", width="60%"),
                    style={
                        'textAlign': 'center'
                    }
                ),
                html.Br([]),
                md_methods_7,
                
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
                    ], width={"size": 3, "offset": 1}),
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
                        dbc.Row([
                            dbc.Col([
                                dcc.Dropdown(
                                    id='drop_subs',
                                    options=sub2_opts,
                                    value='sub-001',
                                )
                                ], width={"size": 10, "offset": 0}),
                        ]),
                        html.Br([]),
                        dbc.Row(
                            dbc.Col([
                                dbc.RadioItems(
                                    options=task_opts_v22,
                                    value='fingerTapping',
                                    id="radio_tasks_tsnr2",
                                )],
                            )
                        ),
                    ], width={"size": 4, "offset": 0}),
                    dbc.Col([

                        dcc.Graph(figure=fig_tsnr_persub, id='fig_tsnr_persub')],
                        style={
                            'textAlign': 'left',
                        },
                        width={"size": 8, "offset": 0}
                    ),
                ]),
                ]
        elif active_tab == "clusters":
            return [
                html.H2('Task regions and cluster sizes', style={'textAlign': 'center'}),
                html.H5('Clusters/regions for comparisons'),
                md_cluster_1,
                html.Br([]),
                dbc.Row([
                    dbc.Col([
                        dbc.Row(
                            dbc.Col([
                                dbc.RadioItems(
                                    options=tasks_1stlevel_opts_v2,
                                    value='fingerTapping',
                                    id="radio_tasks_clusters",
                                    inline=True,
                                )],
                            )
                        ),
                    ], width={"size": 6, "offset": 1}),
                    dbc.Col([
                        dbc.Row(dbc.Col([
                            dcc.Dropdown(
                                id='drop_clusteropts_clusters',
                                options=clusters_opts,
                                value='FWE',
                            )
                            ],
                        )),
                    ], width={"size": 2, "offset": 1}),
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
                html.H5('Anatomical-functional ROI overlap'),
                md_cluster_2,
                html.Br([]),
                dbc.Row([
                    dbc.Col([
                        dbc.Row(
                            dbc.Col([
                                dbc.RadioItems(
                                    options=tasks_1stlevel_opts_v2,
                                    value='fingerTapping',
                                    id="radio_tasks_overlap",
                                    inline=True,
                                )],
                            )
                        ),
                    ], width={"size": 5, "offset": 1}),
                    dbc.Col([
                        dbc.Row(dbc.Col([
                            dcc.Dropdown(
                                id='drop_timeseries_overlap',
                                options=overlap_opts,
                                value='echo2',
                            )
                            ],
                        )),
                    ], width={"size": 2, "offset": 0}),
                    dbc.Col([
                        dbc.Row(dbc.Col([
                            dcc.Dropdown(
                                id='drop_clusteropts_overlap',
                                options=clusters_opts_overlap,
                                value='FWE',
                            )
                            ],
                        )),
                    ], width={"size": 2, "offset": 1}),
                ]),
                dbc.Row(
                    dbc.Col(
                        dcc.Graph(figure=fig_overlap_summary, id='fig_overlap_summary')
                    )
                ),
                html.Br([]),
                dbc.Row(
                    dbc.Col(
                        dcc.Graph(figure=fig_overlap_persub, id='fig_overlap_persub')
                    )
                ),
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
                                    options=tasks_1stlevel_opts_v2,
                                    value='fingerTapping',
                                    id="radio_tasks_tvalsummary",
                                    inline=True,
                                )],
                            )
                        ),
                    ], width={"size": 4, "offset": 1}),
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
                                options=sub2_opts,
                                value='sub-001',
                            )],
                        )),
                        html.Br([]),
                        dbc.Row(dbc.Col([
                            # dbc.Label('Task'),
                            dbc.RadioItems(
                                options=tasks_1stlevel_opts_v2,
                                value='fingerTapping',
                                id="radio_tasks_tvals",
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
                    ], width={"size": 2, "offset": 0}),
                    dbc.Col([
                        dbc.Row(
                            dbc.Col([
                                dbc.RadioItems(
                                    options=tasks_1stlevel_opts_v2,
                                    value='fingerTapping',
                                    id="radio_tasks_pscsummary",
                                    inline=True,
                                )],
                            )
                        ),
                    ], width={"size": 6, "offset": 1}),
                    dbc.Col([
                        dbc.Row(dbc.Col([
                            dcc.Dropdown(
                                id='drop_clusteropts_pscsummary',
                                options=clusters_opts,
                                value='FWE',
                            )
                            ],
                        )),
                    ], width={"size": 2, "offset": 0}),
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

                html.H5('CNR summary'),
                md_psc_4,
                html.Br([]),
                dbc.Row([
                    dbc.Col([
                        dbc.Row(dbc.Col([
                            dcc.Dropdown(
                                id='drop_opts_cnroffline',
                                options=rtcnr_fig_opts,
                                value='cnr',
                            )
                            ],
                        )),
                    ], width={"size": 2, "offset": 0}),
                    dbc.Col([
                        dbc.Row(
                            dbc.Col([
                                dbc.RadioItems(
                                    options=tasks_1stlevel_opts_v2,
                                    value='fingerTapping',
                                    id="radio_tasks_cnroffline",
                                    inline=True,
                                )],
                            )
                        ),
                    ], width={"size": 6, "offset": 1}),
                    dbc.Col([
                        dbc.Row(dbc.Col([
                            dcc.Dropdown(
                                id='drop_clusteropts_cnroffline',
                                options=clusters_opts,
                                value='FWE',
                            )
                            ],
                        )),
                    ], width={"size": 2, "offset": 0}),
                ]),
                dbc.Row([
                    dbc.Col([

                        dcc.Graph(figure=fig_cnr_offline, id='fig_cnr_offline')],
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
                            dcc.Dropdown(
                                id='drop_subs_psc',
                                options=sub2_opts,
                                value='sub-001',
                            )],
                        )),
                        html.Br([]),
                        dbc.Row(dbc.Col([
                            dbc.RadioItems(
                                options=tasks_1stlevel_opts_v2,
                                value='fingerTapping',
                                id="radio_tasks_psc",
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
        elif active_tab == "realtime":
            return [
                html.H2('Real-time / per-volume signals', style={'textAlign': 'center'}),
                html.H5('CNR summary'),
                md_realtime_1,
                html.Br([]),
                dbc.Row([
                    dbc.Col([
                        dbc.Row(dbc.Col([
                            dcc.Dropdown(
                                id='drop_opts_realtimesummary',
                                options=rtcnr_fig_opts,
                                value='cnr',
                            )
                            ],
                        )),
                    ], width={"size": 2, "offset": 0}),
                    dbc.Col([
                        dbc.Row(
                            dbc.Col([
                                dbc.RadioItems(
                                    options=tasks_1stlevel_opts_v2,
                                    value='fingerTapping',
                                    id="radio_tasks_realtimesummary",
                                    inline=True,
                                )],
                            )
                        ),
                    ], width={"size": 6, "offset": 0}),
                    dbc.Col([
                        dbc.Row(dbc.Col([
                            dcc.Dropdown(
                                id='drop_clusteropts_realtimesummary',
                                options=clusters_opts_v2,
                                value='FWE',
                            )
                            ],
                        )),
                    ], width={"size": 2, "offset": 0}),
                    dbc.Col([
                        dbc.Row(dbc.Col([
                            dcc.Dropdown(
                                id='drop_pscopts_realtimesummary',
                                options=psc_types_opts,
                                value='cumulativebas',
                            )
                            ],
                        )),
                    ], width={"size": 2, "offset": 0}),
                ]),
                dbc.Row([
                    dbc.Col([

                        dcc.Graph(figure=fig_realtime_summary, id='fig_realtime_summary')],
                        style={
                            'textAlign': 'left',
                        },
                        width={"size": 12, "offset": 0}
                    ),

                ]),
                html.H5('Real-time ROI signal plots'),
                md_realtime_2,
                html.Br([]),
                dbc.Row([
                    dbc.Col([
                        dbc.Row(dbc.Col([
                            dcc.Dropdown(
                                id='drop_subs_realtime',
                                options=sub2_opts,
                                value='sub-001',
                            )
                            ],
                        )),
                    ], width={"size": 2, "offset": 0}),
                    dbc.Col([
                        dbc.Row(
                            dbc.Col([
                                dbc.RadioItems(
                                    options=tasks_1stlevel_opts_v2,
                                    value='fingerTapping',
                                    id="radio_tasks_realtimeseries",
                                    inline=True,
                                )],
                            )
                        ),
                    ], width={"size": 6, "offset": 0}),
                    dbc.Col([
                        dbc.Row(dbc.Col([
                            dcc.Dropdown(
                                id='drop_clusteropts_realtimeseries',
                                options=clusters_opts_v2,
                                value='FWE',
                            )
                            ],
                        )),
                    ], width={"size": 2, "offset": 0}),
                    dbc.Col([
                        dbc.Row(dbc.Col([
                            dcc.Dropdown(
                                id='drop_pscopts_realtimeseries',
                                options=psc_types_opts,
                                value='cumulativebas',
                            )
                            ],
                        )),
                    ], width={"size": 2, "offset": 0}),
                ]),
                dbc.Row([
                    dbc.Col([

                        dcc.Graph(figure=fig_realtime_series, id='fig_realtime_series')],
                        style={
                            'textAlign': 'left',
                        },
                        width={"size": 12, "offset": 0}
                    ),

                ]),
            ]

    return "No tab selected"