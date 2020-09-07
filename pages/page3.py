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
cols_tasksruns = ['rest 1', 'motor 1', 'emotion 1', 'rest 2', 'motor 2', 'emotion 2']
sub_opts = [{'label': sub, 'value': sub} for sub in all_subs]
task_opts = [{'label': task.capitalize(), 'value': task} for task in tasks]
run_opts = [{'label': 'Run '+run, 'value': run} for run in runs]
ts_names = ['t2starFIT', 'combinedMEt2starFIT', 'combinedMEte', 'combinedMEt2star', 'combinedMEtsnr', 'echo-2']
ts_opts = [{'label': ts, 'value': ts} for ts in ts_names]
tasks_1stlevel = ['motor', 'emotion']
tasks_1stlevel_opts = [{'label': task.capitalize(), 'value': task} for task in tasks_1stlevel]

# -------
# FIGURES
# -------

# TSNR
# Fig 3.1
fig_tsnr_persub = go.Figure()
#Fig 3.2
layout = go.Layout(
        yaxis = dict(title = 'Mean tSNR in gray matter', range=[0, 200]),
        xaxis = dict(title='Time series'),
        margin = {
              't': 10,
            })
fig_tsnr_mean = go.Figure(layout=layout)
tsnrmean_fn = os.path.join(data_dir, 'sub-all_task-all_run-all_desc-GMtsnrmean.tsv')
df_tsnrmean = pd.read_csv(tsnrmean_fn, sep='\t')
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
    fig_tsnr_mean.add_trace(go.Violin(y=data2[x], line_color=sequential.Inferno[3+x], name=ts, points='all', pointpos=-0.4, meanline_visible=True, width=1, side='positive', box_visible=True))
fig_tsnr_mean.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, violinmode='group') # , legend={'traceorder':'reversed'}


# CLUSTERS
# Fig 3.4
fig_clusters = go.Figure()

# EFFECT SIZES
# Fig 3.3 AND 3.6
fig_tvals_peak = go.Figure()
fig_effect_peak = go.Figure()

# Fig 3.5
fig_tvals_persub = go.Figure()
fig_effect_persub = go.Figure()


fig_psc_persub = go.Figure()
fig_psc_timeseries = go.Figure()





# -------------------------------------------------- #
# -------------------------------------------------- #
# -------------------------------------------------- #
# -------------------------------------------------- #
# -------------------------------------------------- #
# -------------------------------------------------- #


layout = html.Div([
    dcc.Store(id="store"),
    html.Div([
        dbc.Tabs(
            [
                dbc.Tab(label="tSNR", tab_id="tsnr-page3"),
                dbc.Tab(label="1st-level clusters", tab_id="clusters"),
                dbc.Tab(label="Effect sizes", tab_id="cvals"),
                dbc.Tab(label="T-values", tab_id="tvals"),
                dbc.Tab(label="Perc. signal change", tab_id="pscvals"),

            ],
            id="tabs-page3",
            active_tab="tsnr-page3",
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


# Callback for updating figure based on drop1, radio1, radio2 values
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

        # if x == 0:
        #     fig_tsnr_persub.add_trace(go.Violin(x=data[x], line_color=sequential.Inferno[3+x], name=ts, points='all'))
        # else:
        #     fig_tsnr_persub.add_trace(go.Violin(x=data[x], line_color=sequential.Inferno[3+x], name=ts, points=False))

    fig_tsnr_persub.update_traces(orientation='h', side='positive', width=2, box_visible=True, meanline_visible=True)
    fig_tsnr_persub.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, legend={'traceorder':'reversed'})

    return fig_tsnr_persub



# Callback for updating run values
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




# Callback for updating figure based on drop2... values
@app.callback(
     Output('fig_tvals_persub', 'figure'),
    [Input('drop_subs_tvals','value'),
     Input('radio_tasks_tvals','value'),
     Input('radio_runs_tvals','value')]
)
def reset_tval_imgs(sub, task, run):

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
    tval_fn = os.path.join(data_dir, sub+'_task-'+task+'_run-'+run+'_desc-tmapvalues.tsv')
    df_tvals = pd.read_csv(tval_fn, sep='\t')

    for x, ts in enumerate(ts_names3[-2::-2]):


        new_dat = df_tvals[ts].dropna().to_numpy()

        data.append(new_dat)
        fig_tvals_persub.add_trace(go.Violin(x=data[x], line_color=sequential.Viridis[8-x], name=ts_names2[5-x], points=False))

    fig_tvals_persub.update_traces(orientation='h', side='positive', width=2, box_visible=True, meanline_visible=True)
    fig_tvals_persub.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, legend={'traceorder':'reversed'})

    return fig_tvals_persub



# Callback for updating figure based on drop2... values
@app.callback(
     Output('fig_tvals_peak', 'figure'),
    [Input('radio_tasks_tvalpeak','value'),
     Input('radio_runs_tvalpeak','value')]
)
def reset_tval_peak_img(task, run):
    layout = go.Layout(
        yaxis = dict(title = 'Peak T-values', range=[0, 40]),
        xaxis = dict(title='Time series'),
        margin = {
              't': 10,
            })
    fig_tvals_peak = go.Figure(layout=layout)

    tvalpeak_fn = os.path.join(data_dir, 'sub-all_task-all_run-all_desc-peakTvalues.tsv')
    df_tvalpeak = pd.read_csv(tvalpeak_fn, sep='\t')
    data_peak = []
    # ts_names3 = ['echo-2', 'combinedMEtsnr', 'combinedMEt2star', 'combinedMEte', 'combinedMEt2starFIT', 't2starFIT']
    ts_names2 = ['echo-2', 'combinedMEtsnr', 'combinedMEt2star', 'combinedMEte', 'combinedMEt2starFIT', 't2starFIT']
    ts_names3 = ['echo2_FWE', 'echo2_noFWE', 'combTSNR_FWE', 'combTSNR_noFWE', 'combT2STAR_FWE', 'combT2STAR_noFWE', 'combTE_FWE', 'combTE_noFWE', 'combT2STARfit_FWE', 'combT2STARfit_noFWE', 'T2STARfit_FWE', 'T2STARfit_noFWE']
    taskrun = task + '_' + run

    # only use FWE: ts_names3[0::2]
    for x, ts in enumerate(ts_names3[0::2]):
        txt = taskrun + '_' + ts
        temp_dat_peak = df_tvalpeak[txt].to_numpy()
        data_peak.append(temp_dat_peak)
        fig_tvals_peak.add_trace(go.Violin(y=data_peak[x], line_color=sequential.Viridis[3+x], name=ts_names2[x], points='all', pointpos=-0.4, meanline_visible=True, width=1, side='positive', box_visible=True))

    fig_tvals_peak.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, violinmode='group') # , legend={'traceorder':'reversed'}

    return fig_tvals_peak



# Callback for updating figure based on drop2... values
@app.callback(
     Output('fig_effect_peak', 'figure'),
    [Input('radio_tasks_effectpeak','value'),
     Input('radio_runs_effectpeak','value')]
)
def reset_effect_peak_img(task, run):
    layout = go.Layout(
            yaxis = dict(title = 'Peak contrast values'),
            xaxis = dict(title='Time series'),
            margin = {
                  't': 10,
                })
    fig_effect_peak = go.Figure(layout=layout)
    cvalpeak_fn = os.path.join(data_dir, 'sub-all_task-all_run-all_desc-peakConvalues.tsv')
    df_cvalpeak = pd.read_csv(cvalpeak_fn, sep='\t')
    data_peakCon = []
    ts_names2 = ['echo-2', 'combinedMEtsnr', 'combinedMEt2star', 'combinedMEte', 'combinedMEt2starFIT', 't2starFIT']
    ts_names3 = ['echo2_FWE', 'echo2_noFWE', 'combTSNR_FWE', 'combTSNR_noFWE', 'combT2STAR_FWE', 'combT2STAR_noFWE', 'combTE_FWE', 'combTE_noFWE', 'combT2STARfit_FWE', 'combT2STARfit_noFWE', 'T2STARfit_FWE', 'T2STARfit_noFWE']
    taskrun = task + '_' + run

    # only use FWE: ts_names3[0::2]
    for x, ts in enumerate(ts_names3[0::2]):
        txt = taskrun + '_' + ts
        temp_dat_peakCon = df_cvalpeak[txt].to_numpy()
        data_peakCon.append(temp_dat_peakCon)
        fig_effect_peak.add_trace(go.Violin(y=data_peakCon[x], line_color=sequential.Viridis[3+x], name=ts_names2[x], points='all', pointpos=-0.4, meanline_visible=True, width=1, side='positive', box_visible=True))
    fig_effect_peak.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, violinmode='group') # , legend={'traceorder':'reversed'}
    return fig_effect_peak




# Callback for updating figure based on drop2... values
@app.callback(
     Output('fig_effect_persub', 'figure'),
    [Input('drop_subs_effect','value'),
     Input('radio_tasks_effect','value'),
     Input('radio_runs_effect','value')]
)
def reset_contrast_imgs(sub, task, run):

    layout = go.Layout(
        yaxis = dict(title = 'Time series'),
        xaxis=dict(title='Effect size (a.u.)', range=[0, 15]),
        margin={
              't': 10,
            })
    fig_effect_persub = go.Figure(layout=layout)

    data = []
    ts_names2 = ['echo-2', 'combinedMEtsnr', 'combinedMEt2star', 'combinedMEte', 'combinedMEt2starFIT', 't2starFIT']
    ts_names3 = ['echo2_FWE', 'echo2_noFWE', 'combTSNR_FWE', 'combTSNR_noFWE', 'combT2STAR_FWE', 'combT2STAR_noFWE', 'combTE_FWE', 'combTE_noFWE', 'combT2STARfit_FWE', 'combT2STARfit_noFWE', 'T2STARfit_FWE', 'T2STARfit_noFWE']
    cval_fn = os.path.join(data_dir, sub+'_task-'+task+'_run-'+run+'_desc-cmapvalues.tsv')
    df_cvals = pd.read_csv(cval_fn, sep='\t')

    for x, ts in enumerate(ts_names3[-2::-2]):


        new_dat = df_cvals[ts].dropna().to_numpy()

        data.append(new_dat)
        fig_effect_persub.add_trace(go.Violin(x=data[x], line_color=sequential.Viridis[8-x], name=ts_names2[5-x], points=False))

    fig_effect_persub.update_traces(orientation='h', side='positive', width=2, box_visible=True, meanline_visible=True)
    fig_effect_persub.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, legend={'traceorder':'reversed'})

    return fig_effect_persub



# Callback for updating figure based on drop2... values
@app.callback(
    [Output('fig_psc_persub', 'figure'),
     Output('fig_psc_timeseries', 'figure')],
    [Input('drop_subs_psc','value'),
     Input('radio_tasks_psc','value'),
     Input('radio_runs_psc','value')]
)
def reset_psc_imgs(sub, task, run):

    layout = go.Layout(
        yaxis = dict(title = 'Time series'),
        xaxis=dict(title='Percentage signal change', range=[0, 10]),
        margin={
              't': 10,
            })
    fig_psc_persub = go.Figure(layout=layout)

    data = []
    ts_names2 = ['echo-2', 'combinedMEtsnr', 'combinedMEt2star', 'combinedMEte', 'combinedMEt2starFIT', 't2starFIT']
    ts_names3 = ['echo2_FWE', 'echo2_noFWE', 'combTSNR_FWE', 'combTSNR_noFWE', 'combT2STAR_FWE', 'combT2STAR_noFWE', 'combTE_FWE', 'combTE_noFWE', 'combT2STARfit_FWE', 'combT2STARfit_noFWE', 'T2STARfit_FWE', 'T2STARfit_noFWE']
    psc_fn = os.path.join(data_dir, sub+'_task-'+task+'_run-'+run+'_desc-PSCvalues.tsv')
    df_psc = pd.read_csv(psc_fn, sep='\t')

    for x, ts in enumerate(ts_names3[-2::-2]):
        new_dat = df_psc[ts].dropna().to_numpy()
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
    for i, colname in enumerate(ts_names4):
        data_pscts.append(df_psc_ts[colname].to_numpy())
        fig_psc_timeseries.add_trace(go.Scatter(y=data_pscts[i], mode='lines', line = dict(color=sequential.Viridis[8-i], width=2), name=colname ))
        fig_psc_timeseries.update_yaxes(showticklabels=True)

    fig_psc_timeseries.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, legend={'traceorder':'reversed'})
    # fig2b.update_layout(xaxis_showgrid=False, xaxis_zeroline=False,
    #                     title='Framewise displacement over time for all functional runs - '+selected_sub)


    return [fig_psc_persub, fig_psc_timeseries]



# Callback for updating figure based on drop2... values
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
     Input('fig_tvals_peak', 'figure'),
     Input('fig_clusters', 'figure')]
)
def on_button_click(n, fig_tsnr_mean, fig_tvals_peak, fig_clusters):
    if n is None:
        return "Not clicked."
    else:
        write_html(fig_tsnr_mean, os.path.join(data_dir, 'fig_tsnr_mean.html'))
        write_html(fig_tvals_peak, os.path.join(data_dir, 'fig_tvals_peak.html'))
        write_html(fig_clusters, os.path.join(data_dir, 'fig_clusters.html'))
        return f"{n}"





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
    main_md1 = dcc.Markdown('''
    Temporal signal-to-noise ratios (tSNR) were calculated for the single echo time series (echo 2), all of the combined time series (x4), and the T2*-FIT time series.
    The distribution of mean tSNR in gray matter is shown below, per time series, for all runs of all participants (excluding the template run, i.e. Rest run 1) 
    ''')

    main_md2 = dcc.Markdown('''
    To get a more representative picture of the distribution of tSNR values for the various time series,
    the inputs below can be used to view tSNR per participant, task, and run.
    ''')

    main_md3 = dcc.Markdown('''
    Cluster sizes, i.e. amount of voxels, after thresholding (FWE, p < 0.05, extent threshold = 0) of statistical maps that were derived from 1st level analysis of all time series.
    ''')


    if active_tab is not None:
        if active_tab == "tsnr-page3":
            return [
                html.H2('tSNR in gray matter', style={'textAlign': 'center'}),
                html.H5('Mean tSNR'),
                main_md1,
                html.Br([]),
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
                html.H2('1st level task cluster sizes', style={'textAlign': 'center'}),
                html.Br([]),
                main_md3,
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
                ]
        elif active_tab == "tvals":
            return [
                html.H2('T-values in task clusters', style={'textAlign': 'center'}),
                html.Br([]),
                main_md1,
                html.Br([]),
                html.H5('Peak T-values'),
                dbc.Row([
                    dbc.Col([
                        dbc.Row(dbc.Col([
                            # dbc.Label('Task'),
                            dbc.RadioItems(
                                options=tasks_1stlevel_opts,
                                value='motor',
                                id="radio_tasks_tvalpeak",
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
                                id="radio_runs_tvalpeak",
                                inline=True,
                            )],
                        )),
                    ], width={"size": 5, "offset": 1}),
                ]),
                dbc.Row([
                    dbc.Col([

                        dcc.Graph(figure=fig_tvals_peak, id='fig_tvals_peak')],
                        style={
                            'textAlign': 'left',
                        },
                        width={"size": 12, "offset": 0}
                    ),

                ]),
                html.Br([]),
                html.H5('T-value distributions'),
                main_md3,
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
                html.H2('Effect sizes in task clusters', style={'textAlign': 'center'}),
                html.Br([]),
                main_md3,
                html.Br([]),
                html.H5('Peak effect sizes'),
                dbc.Row([
                    dbc.Col([
                        dbc.Row(dbc.Col([
                            # dbc.Label('Task'),
                            dbc.RadioItems(
                                options=tasks_1stlevel_opts,
                                value='motor',
                                id="radio_tasks_effectpeak",
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
                                id="radio_runs_effectpeak",
                                inline=True,
                            )],
                        )),
                    ], width={"size": 5, "offset": 1}),
                ]),
                dbc.Row([
                    dbc.Col([

                        dcc.Graph(figure=fig_effect_peak, id='fig_effect_peak')],
                        style={
                            'textAlign': 'left',
                        },
                        width={"size": 12, "offset": 0}
                    ),

                ]),
                html.H5('Effect size distributions'),
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
                html.H2('PSC in task clusters', style={'textAlign': 'center'}),
                html.Br([]),
                main_md3,
                html.Br([]),
                # html.H5('Peak effect sizes'),
                # dbc.Row([
                #     dbc.Col([
                #         dbc.Row(dbc.Col([
                #             # dbc.Label('Task'),
                #             dbc.RadioItems(
                #                 options=tasks_1stlevel_opts,
                #                 value='motor',
                #                 id="radio_tasks_effectpeak",
                #                 inline=True,
                #             )],
                #         )),
                #     ], width={"size": 4, "offset": 2}),
                #     dbc.Col([
                #         dbc.Row(dbc.Col([
                #             # dbc.Label('Run'),
                #             dbc.RadioItems(
                #                 options=run_opts,
                #                 value='1',
                #                 id="radio_runs_effectpeak",
                #                 inline=True,
                #             )],
                #         )),
                #     ], width={"size": 5, "offset": 1}),
                # ]),
                # dbc.Row([
                #     dbc.Col([
                #
                #         dcc.Graph(figure=fig_effect_peak, id='fig_effect_peak')],
                #         style={
                #             'textAlign': 'left',
                #         },
                #         width={"size": 12, "offset": 0}
                #     ),
                #
                # ]),
                html.H5('PSC distributions'),
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
                    ], width={"size": 3, "offset": 0}),
                    dbc.Col([

                        dcc.Graph(figure=fig_psc_persub, id='fig_psc_persub')],
                        style={
                            'textAlign': 'left',
                        },
                        width={"size": 9, "offset": 0}
                    ),
                ]),
                html.H5('PSC time series in atlas-based anatomical ROI'),
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

