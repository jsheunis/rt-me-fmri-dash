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
import numpy as np
import json


styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

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


# HEAD MOVEMENT TAB
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
# fig2b = go.Figure(layout=layout)
fig2b = make_subplots(rows=6, cols=1, shared_xaxes=True,
                    vertical_spacing=0.02)
i = 0
for colname in cols_tasksruns:
    data.append(df_fd[colname].to_numpy())
    fig2b.add_trace(go.Scatter(y=data[i], mode='lines', line = dict(color=sequential.Inferno[i+3], width=2), name=colname.capitalize()), row=i+1, col=1)
    fig2b.update_yaxes(title_text="", range=[0, 2], showticklabels=False, row=i+1, col=1)
    if i == 3:
        fig2b.update_yaxes(title_text="\t\tFramewise Displacement (0-2mm)", row=i+1, col=1)
    if i == 5:
        fig2b.update_xaxes(title_text="Functional volumes", row=i+1, col=1)

    i += 1

fig2b.update_layout(xaxis_showgrid=False, xaxis_zeroline=False,
                    title='Framewise displacement over time for all functional runs - '+sub)

# TSNR TAB

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


# Fig 4
layout = go.Layout(
    # title='Mean whole brain tSNR',
    xaxis = dict(
            tickmode = 'array',
            tickvals = [0, 1, 2, 3, 4, 5],
            ticktext = [val.capitalize() for val in cols_tasksruns]
        ),
    yaxis=dict(title='Mean whole brain tSNR'),
    margin={
      't': 6,
    }
)
fig4 = go.Figure(layout=layout)
dataTSNRmean = []
for i, sub in enumerate(all_subs):
    X = np.arange(6)
    Y1 = df_tsnrbrain.iloc[i].to_numpy()
    fig4.add_trace(go.Scatter(x=X, y=Y1, mode='lines+markers', name=sub, hovertemplate='<b>' + sub + '</b>: %{x}<br>TSNR mean = %{y:.2f} mm<extra></extra>'))


# PHYSIOLOGY TAB

# Fig 5 and 6
#Read in data
layout = go.Layout(title='Respiration signals for all subjects - task-rest_run-1',
        xaxis = dict(title = 'Time'),
        yaxis=dict(title='Respiration signals (a.u.)', range=[-250, 10]),
        margin={
          't': 40,
        })
fig5 = go.Figure(layout=layout)
layout = go.Layout(title='Cardiac signals for all subjects - task-rest_run-1',
        xaxis = dict(title = 'Time'),
        yaxis=dict(title='Cardiac signals (a.u.)', range=[-250, 10]),
        margin={
          't': 20,
        })
fig6 = go.Figure(layout=layout)

respData = {}
cardData = {}

for i, task in enumerate(tasks):
    for j, run in enumerate(runs):
        txt = 'task-' + task + '_run-' + run
        respData[txt] = pd.read_csv(os.path.join(data_dir, 'sub-all_task-' + task + '_run-' + run + '_desc-physioResp.tsv'), sep='\t')
        cardData[txt] = pd.read_csv(os.path.join(data_dir, 'sub-all_task-' + task + '_run-' + run + '_desc-physioCard.tsv'), sep='\t')

txt = 'task-rest_run-1'
for i, sub in enumerate(all_subs):
    r = respData[txt][sub].to_numpy()
    c = cardData[txt][sub].to_numpy()
    yr = 5*r - i*9
    yc = 5*c - i*9
    fig5.add_trace(go.Scatter(y=yr, mode='lines', line = dict(width=2), name=sub))
    fig6.add_trace(go.Scatter(y=yc, mode='lines', line = dict(width=1), name=sub))

fig5.update_layout(xaxis_showgrid=False, xaxis_zeroline=False, height=900)
fig6.update_layout(xaxis_showgrid=False, xaxis_zeroline=False, height=900)
fig5.update_yaxes(showticklabels=False)
fig6.update_yaxes(showticklabels=False)


# TASKS TAB
roi_tasks = ['motor', 'emotion']
roi_task_opts = [{'label': roitask.capitalize(), 'value': roitask} for roitask in roi_tasks]
overlapData = {}
for i, task in enumerate(roi_tasks):
    for j, run in enumerate(runs):
        txt = 'task-' + task + '_run-' + run
        overlapData[txt] = pd.read_csv(os.path.join(data_dir, 'sub-all_task-' + task + '_run-' + run + '_desc-roiOverlap.tsv'), sep='\t')

anat_vals = []
func_vals = []
func_vals_nooverlap = []

task = 'motor'
run = '1'
ts_names = ['echo2_FWE', 'echo2_noFWE', 'combTSNR_FWE', 'combTSNR_noFWE', 'combT2STAR_FWE', 'combT2STAR_noFWE', 'combTE_FWE', 'combTE_noFWE', 'combT2STARfit_FWE', 'combT2STARfit_noFWE', 'T2STARfit_FWE', 'T2STARfit_noFWE']
ts_name = ts_names[0]
ts_opts = [{'label': ts, 'value': ts} for ts in ts_names]
txt = 'task-' + task + '_run-' + run

for i, sub in enumerate(all_subs):
    anat_vals.append(overlapData[txt].loc[i, 'anat_roi'])
    func_vals.append(overlapData[txt].loc[i, ts_name])
    func_vals_nooverlap.append(anat_vals[-1] - func_vals[-1])

fig7 = go.Figure(data=[
    go.Bar(name='Func/Anat overlap', x=all_subs, y=func_vals, marker_color=sequential.Viridis[5]),
    go.Bar(name='Anat ROI (no overlap)', x=all_subs, y=func_vals_nooverlap, marker_color=sequential.Viridis[8])
])
# Change the bar mode
fig7.update_layout(barmode='stack', xaxis = dict(title = 'All participants', tickangle=45), yaxis = dict(title = 'Number of voxels'), margin={'t': 10})


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
                        dbc.Tab(label="Physiology", tab_id="physio"),
                        dbc.Tab(label="Tasks", tab_id="tasks"),
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


@app.callback(
    Output('click-data', 'children'),
    [Input('fig7', 'clickData')])
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)



# Callback for updating tsnr html and figure based on drop1, radio1, radio2 values
@app.callback(
     Output('drop1','value'),
    [Input('fig4', 'clickData')]
)
def reset_sub_tsnr_info(clickData):

    if clickData is None:
        raise PreventUpdate
    else:
        selected_sub = all_subs[clickData['points'][0]['curveNumber']]

    return selected_sub

  # "points": [
  #   {
  #     "curveNumber": 7,
  #     "pointNumber": 1,
  #     "pointIndex": 1,
  #     "x": 1,
  #     "y": 45.905129043942786
  #   }
  # ]






# Callback for updating tsnr html and figure based on drop1, radio1, radio2 values
@app.callback(
    [Output('tsnr_map', 'src'),
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
    [Output('fig2', 'figure'),
     Output('fig2b', 'figure')],
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
        fig2b = make_subplots(rows=6, cols=1, shared_xaxes=True,
                            vertical_spacing=0.02)

        i = 0
        for colname in cols_tasksruns:
            data.append(df_fd[colname].to_numpy())
            fig2.add_trace(go.Violin(y=data[i], line_color=sequential.Inferno[i+3], name=colname.capitalize(), orientation='v', side='positive', width=1.5, points=False, box_visible=True, meanline_visible=True))
            fig2b.add_trace(go.Scatter(y=data[i], mode='lines', line = dict(color=sequential.Inferno[i+3], width=2), name=colname.capitalize()), row=i+1, col=1)
            fig2b.update_yaxes(title_text="", range=[0, 2], showticklabels=False, row=i+1, col=1)
            if i == 3:
                fig2b.update_yaxes(title_text="\t\tFramewise Displacement (0-2mm)", row=i+1, col=1)
            if i == 5:
                fig2b.update_xaxes(title_text="Functional volumes", row=i+1, col=1)
            i += 1

        fig2.update_layout(xaxis_showgrid=False, xaxis_zeroline=False)
        fig2b.update_layout(xaxis_showgrid=False, xaxis_zeroline=False,
                            title='Framewise displacement over time for all functional runs - '+selected_sub)


        return [fig2, fig2b]




@app.callback(
    [Output('fig5', 'figure'),
     Output('fig6', 'figure')],
    [Input('radio3phys','value'),
     Input('radio4phys','value')]
)
def reset_phys_imgs(task, run):

    txt = 'task-' + task + '_run-' + run
    layout = go.Layout(title='Respiration signals for all subjects - ' + txt,
            xaxis = dict(title = 'Time'),
            yaxis=dict(title='Respiration signals (a.u.)', range=[-250, 10]),
            margin={
              't': 40,
            })
    fig5 = go.Figure(layout=layout)
    layout = go.Layout(title='Cardiac signals for all subjects - ' + txt,
            xaxis = dict(title = 'Time'),
            yaxis=dict(title='Cardiac signals (a.u.)', range=[-250, 10]),
            margin={
              't': 30,
            })
    fig6 = go.Figure(layout=layout)

    for i, sub in enumerate(all_subs):
        r = respData[txt][sub].to_numpy()
        c = cardData[txt][sub].to_numpy()
        yr = 5*r - i*9
        yc = 5*c - i*9
        fig5.add_trace(go.Scatter(y=yr, mode='lines', line = dict(width=2), name=sub))
        fig6.add_trace(go.Scatter(y=yc, mode='lines', line = dict(width=1), name=sub))

    fig5.update_layout(xaxis_showgrid=False, xaxis_zeroline=False, height=900)
    fig6.update_layout(xaxis_showgrid=False, xaxis_zeroline=False, height=900)
    fig5.update_yaxes(showticklabels=False)
    fig6.update_yaxes(showticklabels=False)

    return [fig5, fig6]


@app.callback(
     Output('fig7', 'figure'),
    [Input('radio5roi','value'),
     Input('radio6roi','value'),
     Input('dropts','value')]
)
def reset_roi_img1(task, run, ts_name):

    anat_vals = []
    func_vals = []
    func_vals_nooverlap = []
    txt = 'task-' + task + '_run-' + run

    for i, sub in enumerate(all_subs):
        anat_vals.append(overlapData[txt].loc[i, 'anat_roi'])
        func_vals.append(overlapData[txt].loc[i, ts_name])
        func_vals_nooverlap.append(anat_vals[-1] - func_vals[-1])

    fig7 = go.Figure(data=[
        go.Bar(name='Func/Anat overlap', x=all_subs, y=func_vals, marker_color=sequential.Viridis[5]),
        go.Bar(name='Anat ROI (no overlap)', x=all_subs, y=func_vals_nooverlap, marker_color=sequential.Viridis[8])
    ])
    # Change the bar mode
    fig7.update_layout(barmode='stack', xaxis = dict(title = 'All participants', tickangle=45), yaxis = dict(title = 'Number of voxels'), margin={'t': 10})

    return fig7


@app.callback(
     Output('fig8', 'figure'),
    [Input('radio5roi','value'),
     Input('radio6roi','value'),
     Input('fig7','clickData')]
)
def reset_roi_img2(task, run, clickData):

    if clickData is None:
        selected_subnr = 0
    else:
        selected_subnr = clickData['points'][0]['pointIndex']

    txt = 'task-' + task + '_run-' + run
    vals = overlapData[txt].loc[selected_subnr].to_numpy()
    func_vals = vals[1:]
    func_vals_nooverlap = vals[0] - func_vals
    cols = list(overlapData[txt].columns)
    cols = cols[1:]

    fig8 = go.Figure(data=[
        go.Bar(name='Func/Anat overlap', x=cols, y=func_vals, marker_color=sequential.Viridis[5]),
        go.Bar(name='Anat ROI (no overlap)', x=cols, y=func_vals_nooverlap, marker_color=sequential.Viridis[8])
    ])
    fig8.update_layout(barmode='stack', xaxis = dict(title = 'All time series', tickangle=45),
                       yaxis = dict(title = 'Number of voxels'), margin={'t': 40},
                       title='ROI overlap computed from all time series options - '+all_subs[selected_subnr])

    return fig8







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
                        dcc.Graph(figure=fig2b, id='fig2b')
                    )
                ),
                ]
        elif active_tab == "tsnr":
            return [
                html.H2('tSNR', style={'textAlign': 'center'}),
                html.Br([]),
                dbc.Row(
                    dbc.Col(
                        dcc.Graph(figure=fig4, id='fig4')
                    )
                ),

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
                            html.Iframe(id='tsnr_map', src='/assets/sub-001_task-rest_run-1_echo-2_space-MNI152_desc-rapreproc_tsnr.html', style={'border': 'none', 'width': '100%', 'height': 250})],
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

                ]
        elif active_tab == "physio":
            return [
                html.H2('Physiology', style={'textAlign': 'center'}),
                html.Br([]),
                dbc.Row([
                    dbc.Col([
                        # dbc.Label('Task'),
                        dbc.RadioItems(
                            options=task_opts,
                            value='rest',
                            id="radio3phys",
                            inline=True,
                        )
                    ],
                    style={'textAlign': 'right'},
                    width={"size": 6, "offset": 0}),
                    dbc.Col([
                        dbc.RadioItems(
                            options=run_opts,
                            value='1',
                            id="radio4phys",
                            inline=True,
                        )
                    ],
                    style={'textAlign': 'left'},
                    width={"size": 4, "offset": 1}),
                ]),
                html.Br([]),
                dbc.Row(
                    dbc.Col(
                        dcc.Graph(figure=fig5, id='fig5')
                    )
                ),
                dbc.Row(
                    dbc.Col(
                        dcc.Graph(figure=fig6, id='fig6')
                    )
                ),
                ]
        elif active_tab == "tasks":
            return [
                html.H2('Tasks', style={'textAlign': 'center'}),
                html.Br([]),
                dbc.Row([
                    dbc.Col([
                        html.H5('Motor Run 1 - Group level Tmap', style={'textAlign': 'center'}),
                        html.Iframe(id='task_map1', src='/assets/sub-all_task-motor_run-1_echo-2_space-MNI152_desc-2ndlevel_tmap.html', style={'border': 'none', 'width': '100%', 'height': 250}),
                        ]
                    ),
                    dbc.Col([
                        html.H5('Motor Run 2 - Group level Tmap', style={'textAlign': 'center'}),
                        html.Iframe(id='task_map2', src='/assets/sub-all_task-motor_run-2_echo-2_space-MNI152_desc-2ndlevel_tmap.html', style={'border': 'none', 'width': '100%', 'height': 250}),
                        ]
                    )]
                ),
                dbc.Row([
                    dbc.Col([
                        html.H5('Emotion Run 1 - Group level Tmap', style={'textAlign': 'center'}),
                        html.Iframe(id='task_map3', src='/assets/sub-all_task-emotion_run-1_echo-2_space-MNI152_desc-2ndlevel_tmap.html', style={'border': 'none', 'width': '100%', 'height': 250}),
                        ]
                    ),
                    dbc.Col([
                        html.H5('Emotion Run 2 - Group level Tmap', style={'textAlign': 'center'}),
                        html.Iframe(id='task_map4', src='/assets/sub-all_task-emotion_run-2_echo-2_space-MNI152_desc-2ndlevel_tmap.html', style={'border': 'none', 'width': '100%', 'height': 250}),
                        ]
                    )]
                ),
                html.Br([]),
                html.H2('Regions of interest', style={'textAlign': 'center'}),
                html.Br([]),
                dbc.Row([
                    dbc.Col([
                        # dbc.Label('Task'),
                        dbc.RadioItems(
                            options=roi_task_opts,
                            value='motor',
                            id="radio5roi",
                            inline=True,
                        )
                    ],
                    style={'textAlign': 'right'},
                    width={"size": 3, "offset": 1}),
                    dbc.Col([
                        dbc.RadioItems(
                            options=run_opts,
                            value='1',
                            id="radio6roi",
                            inline=True,
                        )
                    ],
                    style={'textAlign': 'left'},
                    width={"size": 3, "offset": 1}),
                    dbc.Col([
                        dcc.Dropdown(
                            id='dropts',
                            options=ts_opts,
                            value=ts_names[0],
                        )
                    ],
                    style={'textAlign': 'left'},
                    width={"size": 2, "offset": 0}),
                ]),
                dbc.Row(
                    dbc.Col(
                        dcc.Graph(figure=fig7, id='fig7')
                    )
                ),
                # dbc.Row(
                #     dbc.Col(
                #         html.Pre(id='click-data', style=styles['pre']),
                #     )
                # ),
                html.Br([]),
                dbc.Row(
                    dbc.Col(
                        dcc.Graph(figure=fig8, id='fig8')
                    )
                ),
            ]

    return "No tab selected"