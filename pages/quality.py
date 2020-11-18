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


# ------------ #
# ------------ #
# DATA SETUP   #
# ------------ #
# ------------ #
# styles = {
#     'pre': {
#         'border': 'thin lightgrey solid',
#         'overflowX': 'scroll'
#     }
# }

# Directories
data_dir = '../rt-me-fmri-data-v2/quality'

# Filenames
participants_fn = os.path.join('../rt-me-fmri-data-v2', 'participants.tsv')
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
tasks_v2 = ['rest_run-1', 'fingerTapping', 'emotionProcessing', 'rest_run-2', 'fingerTappingImagined', 'emotionProcessingImagined']
tasks_v2_names = ['Rest 1', 'Finger tapping', 'Emotion processing', 'Rest 2', 'Finger tapping (imagined)', 'Emotion processing (imagined)']
task_opts_v2 = [{'label': tasks_v2_names[i], 'value': task} for i, task in enumerate(tasks_v2)]
tasks_1stlevel_v2 = ['fingerTapping', 'emotionProcessing', 'fingerTappingImagined', 'emotionProcessingImagined']
tasks_1stlevel_v2_names = ['Finger tapping', 'Emotion processing', 'Finger tapping (imagined)', 'Emotion processing (imagined)']
tasks_1stlevel_opts_v2 = [{'label': tasks_1stlevel_v2_names[i], 'value': task} for i, task in enumerate(tasks_1stlevel_v2)]

# Physiology data
respData = {}
cardData = {}
for i, task in enumerate(tasks_v2):
    txt = 'task-' + task
    respData[txt] = pd.read_csv(os.path.join(data_dir, 'sub-all_task-' + task + '_desc-physioResp.tsv'), sep='\t')
    cardData[txt] = pd.read_csv(os.path.join(data_dir, 'sub-all_task-' + task + '_desc-physioCard.tsv'), sep='\t')


# ------------ #
# ------------ #
# FIGURES      #
# ------------ #
# ------------ #

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
fig2 = go.Figure()
fig2b = go.Figure()

# TSNR TAB
# Fig 3, 4, 4b
fig3 = go.Figure()
layout = go.Layout(
    xaxis = dict(
            tickmode = 'array',
            tickvals = [0, 1, 2, 3, 4, 5],
            ticktext = tasks_v2_names
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
# Fig 4b
layout = go.Layout(
            yaxis = dict(title = 'tSNR'), # , range=[-0.5, 2]
            margin = {
                  't': 10,
                })
fig4b = go.Figure(layout=layout)
dataTSNRmean = []
for x, taskrun in enumerate(tasks_v2):
    temp_dat = df_tsnrgm[taskrun].to_numpy()
    dataTSNRmean.append(temp_dat)
    fig4b.add_trace(go.Violin(y=dataTSNRmean[x], line_color=sequential.Inferno[3+x], name=tasks_v2_names[x], points='all', pointpos=-0.4, meanline_visible=True, width=1, side='positive', box_visible=True))
fig4b.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, violinmode='group')

# PHYSIOLOGY TAB
# Fig 5 and 6
fig5 = go.Figure()
fig6 = go.Figure()



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

main_md = dcc.Markdown('''
Hello!
''')

layout = html.Div([
            dcc.Store(id="store"),
            html.Div([
                dbc.Tabs(
                    [
                        dbc.Tab(label="Description", tab_id="description"),
                        dbc.Tab(label="Head movement", tab_id="head_movement"),
                        dbc.Tab(label="tSNR", tab_id="tsnr"),
                        dbc.Tab(label="Physiology", tab_id="physio"),
                        dbc.Tab(label="Tasks", tab_id="tasks"),
                    ],
                    id="tabs",
                    active_tab="description",
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


# ------------ #
# ------------ #
# CALLBACKS    #
# ------------ #
# ------------ #


# Callback for updating Fig2 based on Fig1 clickData
@app.callback(
    [Output('fig2', 'figure'),
     Output('fig2b', 'figure'),
     Output('sub_fd', 'children')],
    [Input('fig1', 'clickData')]
)
def update_fd_persub_figs(clickData):
    if clickData is None:
        selected_sub = 'sub-001'
        # raise PreventUpdate
    else:
        selected_sub = clickData['points'][0]['x']

    fd_fn = os.path.join(data_dir, selected_sub+'_task-all_run-all_desc-fd.tsv')
    df_fd = pd.read_csv(fd_fn, sep='\t')
    data = []
    layout = go.Layout(yaxis=dict(title='Framewise displacement (mm)'))

    fig2 = go.Figure(layout=layout)
    fig2b = make_subplots(rows=6, cols=1, shared_xaxes=True,
                        vertical_spacing=0.02)

    for i, colname in enumerate(tasks_v2):
        data.append(df_fd[colname].to_numpy())
        fig2.add_trace(go.Violin(y=data[i], line_color=sequential.Inferno[i+3], name=tasks_v2_names[i], orientation='v', side='positive', width=1.5, points=False, box_visible=True, meanline_visible=True))
        fig2b.add_trace(go.Scatter(y=data[i], mode='lines', line = dict(color=sequential.Inferno[i+3], width=2), name=tasks_v2_names[i]), row=i+1, col=1)
        fig2b.update_yaxes(title_text="", range=[0, 2], showticklabels=False, row=i+1, col=1)
        if i == 3:
            fig2b.update_yaxes(title_text="\t\tFramewise Displacement (0-2mm)", row=i+1, col=1)
        if i == 5:
            fig2b.update_xaxes(title_text="Functional volumes", row=i+1, col=1)

    fig2.update_layout(xaxis_showgrid=False, xaxis_zeroline=False, margin = {'t': 10})
    fig2b.update_layout(xaxis_showgrid=False, xaxis_zeroline=False, margin = {'t': 10})

    new_heading = 'Framewise displacement distributions and timeseries: ' + selected_sub

    return [fig2, fig2b, new_heading]



# # Callback for updating tsnr html and figure based on drop1, radio1, radio2 values
# @app.callback(
#      Output('drop1','value'),
#     [Input('fig4', 'clickData')]
# )
# def reset_sub_tsnr_info(clickData):

#     if clickData is None:
#         raise PreventUpdate
#     else:
#         selected_sub = all_subs[clickData['points'][0]['curveNumber']]

#     return selected_sub


# Callback for updating tsnr figure based on subject and task
@app.callback(
     Output('fig3', 'figure'),
    [Input('drop_subs_tsnr','value'),
     Input('radio_tasks_tsnr','value')]
)
def reset_tsnr_imgs(sub, task):

    braintsnr_tsv = os.path.join(data_dir, sub+'_task-' + task + '_echo-2_desc-rapreproc_braintsnr.tsv')
    GMtsnr_tsv = os.path.join(data_dir, sub+'_task-' + task + '_echo-2_desc-rapreproc_GMtsnr.tsv')
    WMtsnr_tsv = os.path.join(data_dir, sub+'_task-' + task + '_echo-2_desc-rapreproc_WMtsnr.tsv')
    CSFtsnr_tsv = os.path.join(data_dir, sub+'_task-' + task + '_echo-2_desc-rapreproc_CSFtsnr.tsv')
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
    fig3.update_layout(xaxis_showgrid=True, yaxis_showgrid=True, xaxis_zeroline=False, legend={'traceorder':'reversed'})

    return fig3


# Callback for updating cardiac and respiratory plot figures based on task
@app.callback(
    [Output('fig5', 'figure'),
     Output('fig6', 'figure'),
     Output('resp_heading', 'children'),
     Output('card_heading', 'children')],
    [Input('radio3phys','value')]
)
def reset_phys_imgs(task):

    txt = 'task-' + task
    layout = go.Layout(
            xaxis = dict(title = 'Time'),
            yaxis=dict(title='Respiration signals (a.u.)', range=[-250, 10]),
            margin={
              't': 20,
            })
    fig5 = go.Figure(layout=layout)
    layout = go.Layout(
            xaxis = dict(title = 'Time'),
            yaxis=dict(title='Cardiac signals (a.u.)', range=[-250, 10]),
            margin={
              't': 20,
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

    resp_heading = 'Respiratory signals for all subjects: ' + task
    card_heading = 'Cardiac signals for all subjects: ' + task

    return [fig5, fig6, resp_heading, card_heading]


# @app.callback(
#      Output('fig7', 'figure'),
#     [Input('radio5roi','value'),
#      Input('radio6roi','value'),
#      Input('dropts','value')]
# )
# def reset_roi_img1(task, run, ts_name):

#     anat_vals = []
#     func_vals = []
#     func_vals_nooverlap = []
#     txt = 'task-' + task + '_run-' + run

#     for i, sub in enumerate(all_subs):
#         anat_vals.append(overlapData[txt].loc[i, 'anat_roi'])
#         func_vals.append(overlapData[txt].loc[i, ts_name])
#         func_vals_nooverlap.append(anat_vals[-1] - func_vals[-1])

#     fig7 = go.Figure(data=[
#         go.Bar(name='Func/Anat overlap', x=all_subs, y=func_vals, marker_color=sequential.Viridis[5]),
#         go.Bar(name='Anat ROI (no overlap)', x=all_subs, y=func_vals_nooverlap, marker_color=sequential.Viridis[8])
#     ])
#     # Change the bar mode
#     fig7.update_layout(barmode='stack', xaxis = dict(title = 'All participants', tickangle=45), yaxis = dict(title = 'Number of voxels'), margin={'t': 10})

#     return fig7


# @app.callback(
#      Output('fig8', 'figure'),
#     [Input('radio5roi','value'),
#      Input('radio6roi','value'),
#      Input('fig7','clickData')]
# )
# def reset_roi_img2(task, run, clickData):

#     if clickData is None:
#         selected_subnr = 0
#     else:
#         selected_subnr = clickData['points'][0]['pointIndex']

#     txt = 'task-' + task + '_run-' + run
#     vals = overlapData[txt].loc[selected_subnr].to_numpy()
#     func_vals = vals[1:]
#     func_vals_nooverlap = vals[0] - func_vals
#     cols = list(overlapData[txt].columns)
#     cols = cols[1:]

#     fig8 = go.Figure(data=[
#         go.Bar(name='Func/Anat overlap', x=cols, y=func_vals, marker_color=sequential.Viridis[5]),
#         go.Bar(name='Anat ROI (no overlap)', x=cols, y=func_vals_nooverlap, marker_color=sequential.Viridis[8])
#     ])
#     fig8.update_layout(barmode='stack', xaxis = dict(title = 'All time series', tickangle=45),
#                        yaxis = dict(title = 'Number of voxels'), margin={'t': 40},
#                        title='ROI overlap computed from all time series options - '+all_subs[selected_subnr])

#     return fig8

# @app.callback(
#     Output('click-data', 'children'),
#     [Input('fig7', 'clickData')])
# def display_click_data(clickData):
#     return json.dumps(clickData, indent=2)



# ------------- #
# ------------- #
# LAYOUT UPDATE #
# ------------- #
# ------------- #

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
        if active_tab == "description":
            return [
                html.H2('Quality assessment', style={'textAlign': 'center'}),
                ]
        elif active_tab == "head_movement":
            return [
                html.H2('Head movement', style={'textAlign': 'center'}),
                html.Br([]),
                html.H5('Summarized framewise displacement over all runs', style={'textAlign': 'left'}),
                dbc.Row(
                    dbc.Col(
                        dcc.Graph(figure=fig, id='fig1')
                    )
                ),
                html.Br([]),
                html.H5('Framewise displacement distributions and timeseries: sub-001', id='sub_fd', style={'textAlign': 'left'}),
                html.P('(Click on a subject distribution above to change the options below)', style={'textAlign': 'left'}),
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
                html.H2('Temporal signal-to-noise ratio', style={'textAlign': 'center'}),
                html.Br([]),
                html.H5('Mean gray matter tSNR distributions over all runs', style={'textAlign': 'left'}),
                html.Br([]),
                dbc.Row(
                    dbc.Col(
                        dcc.Graph(figure=fig4b, id='fig4b')
                    )
                ),
                html.H5('Summary of mean gray matter tSNR for all subjects', style={'textAlign': 'left'}),
                html.Br([]),
                dbc.Row(
                    dbc.Col(
                        dcc.Graph(figure=fig4, id='fig4')
                    )
                ),

                html.H5('Mean gray matter tSNR distributions per tissue compartment', style={'textAlign': 'left'}),
                html.Br([]),
                dbc.Row([
                    dbc.Col([
                        dbc.Row([
                            dbc.Col([
                                dcc.Dropdown(
                                    id='drop_subs_tsnr',
                                    options=sub_opts,
                                    value='sub-001',
                                )
                                ], width={"size": 10, "offset": 0}),
                        ]),
                        html.Br([]),
                        dbc.Row(
                            dbc.Col([
                                dbc.RadioItems(
                                    options=task_opts_v2,
                                    value='rest_run-1',
                                    id="radio_tasks_tsnr",
                                )],
                            )
                        ),
                    ], width={"size": 4, "offset": 0}),
                    dbc.Col([

                        dcc.Graph(figure=fig3, id='fig3')],
                        style={
                            'textAlign': 'left',
                        },
                        width={"size": 8, "offset": 0}
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
                            options=task_opts_v2,
                            value='rest_run-1',
                            id="radio3phys",
                            inline=True,
                        )
                    ],
                    style={'textAlign': 'center'},
                    width={"size": 12, "offset": 0}),
                ]),
                html.Br([]),
                html.Br([]),
                html.H5('Respiratory signals for all subjects: rest_run-1', id='resp_heading', style={'textAlign': 'left'}),
                dbc.Row(
                    dbc.Col(
                        dcc.Graph(figure=fig5, id='fig5')
                    )
                ),
                html.Br([]),
                html.H5('Cardiac signals for all subjects: rest_run-1', id='card_heading', style={'textAlign': 'left'}),
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
                        html.H5('Finger Tapping - Group level Tmap', style={'textAlign': 'center'}),
                        html.Iframe(id='task_map1', src='/assets/sub-all_task-fingerTapping_space-MNI152_desc-2ndlevel_tmap.html', style={'border': 'none', 'width': '100%', 'height': 250}),
                        ]
                    ),
                    dbc.Col([
                        html.H5('Emotion Processing - Group level Tmap', style={'textAlign': 'center'}),
                        html.Iframe(id='task_map2', src='/assets/sub-all_task-emotionProcessing_space-MNI152_desc-2ndlevel_tmap.html', style={'border': 'none', 'width': '100%', 'height': 250}),
                        ]
                    )]
                ),
                dbc.Row([
                    dbc.Col([
                        html.H5('Finger Tapping (imagined) - Group level Tmap', style={'textAlign': 'center'}),
                        html.Iframe(id='task_map3', src='/assets/sub-all_task-fingerTappingImagined_space-MNI152_desc-2ndlevel_tmap.html', style={'border': 'none', 'width': '100%', 'height': 250}),
                        ]
                    ),
                    dbc.Col([
                        html.H5('Emotion Processing (imagined) - Group level Tmap', style={'textAlign': 'center'}),
                        html.Iframe(id='task_map4', src='/assets/sub-all_task-emotionProcessingImagined_space-MNI152_desc-2ndlevel_tmap.html', style={'border': 'none', 'width': '100%', 'height': 250}),
                        ]
                    )]
                ),
                # /Users/jheunis/Documents/Websites/rt-me-fmri-data-v2/quality/sub-all_task-fingerTapping_space-MNI152_desc-2ndlevel_tmap.html
                # html.Br([]),
                # html.H2('Regions of interest', style={'textAlign': 'center'}),
                # html.Br([]),
                # dbc.Row([
                #     dbc.Col([
                #         # dbc.Label('Task'),
                #         dbc.RadioItems(
                #             options=roi_task_opts,
                #             value='motor',
                #             id="radio5roi",
                #             inline=True,
                #         )
                #     ],
                #     style={'textAlign': 'right'},
                #     width={"size": 3, "offset": 1}),
                #     dbc.Col([
                #         dbc.RadioItems(
                #             options=run_opts,
                #             value='1',
                #             id="radio6roi",
                #             inline=True,
                #         )
                #     ],
                #     style={'textAlign': 'left'},
                #     width={"size": 3, "offset": 1}),
                #     dbc.Col([
                #         dcc.Dropdown(
                #             id='dropts',
                #             options=ts_opts,
                #             value=ts_names[0],
                #         )
                #     ],
                #     style={'textAlign': 'left'},
                #     width={"size": 2, "offset": 0}),
                # ]),
                # dbc.Row(
                #     dbc.Col(
                #         dcc.Graph(figure=fig7, id='fig7')
                #     )
                # ),
                # # dbc.Row(
                # #     dbc.Col(
                # #         html.Pre(id='click-data', style=styles['pre']),
                # #     )
                # # ),
                # html.Br([]),
                # dbc.Row(
                #     dbc.Col(
                #         dcc.Graph(figure=fig8, id='fig8')
                #     )
                # ),
            ]

    return "No tab selected"


# TASKS TAB

# overlapData = {}
# for i, task in enumerate(tasks_1stlevel_v2):
#     txt = 'task-' + task
#     overlapData[txt] = pd.read_csv(os.path.join(data_dir, 'sub-all_task-' + task + '_desc-roiOverlap.tsv'), sep='\t')

# anat_vals = []
# func_vals = []
# func_vals_nooverlap = []

# task = 'motor'
# run = '1'
# ts_names = ['echo2_FWE', 'echo2_noFWE', 'combTSNR_FWE', 'combTSNR_noFWE', 'combT2STAR_FWE', 'combT2STAR_noFWE', 'combTE_FWE', 'combTE_noFWE', 'combT2STARfit_FWE', 'combT2STARfit_noFWE', 'T2STARfit_FWE', 'T2STARfit_noFWE']
# ts_name = ts_names[0]
# ts_opts = [{'label': ts, 'value': ts} for ts in ts_names]
# txt = 'task-' + task + '_run-' + run

# for i, sub in enumerate(all_subs):
#     anat_vals.append(overlapData[txt].loc[i, 'anat_roi'])
#     func_vals.append(overlapData[txt].loc[i, ts_name])
#     func_vals_nooverlap.append(anat_vals[-1] - func_vals[-1])

# fig7 = go.Figure(data=[
#     go.Bar(name='Func/Anat overlap', x=all_subs, y=func_vals, marker_color=sequential.Viridis[5]),
#     go.Bar(name='Anat ROI (no overlap)', x=all_subs, y=func_vals_nooverlap, marker_color=sequential.Viridis[8])
# ])
# # Change the bar mode
# fig7.update_layout(barmode='stack', xaxis = dict(title = 'All participants', tickangle=45), yaxis = dict(title = 'Number of voxels'), margin={'t': 10})


# # Fig8
# subnr = 0
# vals = overlapData[txt].loc[subnr].to_numpy()
# func_vals = vals[1:]
# func_vals_nooverlap = vals[0] - func_vals
# cols = list(overlapData[txt].columns)
# cols = cols[1:]

# fig8 = go.Figure(data=[
#     go.Bar(name='Func/Anat overlap', x=cols, y=func_vals, marker_color=sequential.Viridis[5]),
#     go.Bar(name='Anat ROI (no overlap)', x=cols, y=func_vals_nooverlap, marker_color=sequential.Viridis[8])
# ])
# fig8.update_layout(barmode='stack', xaxis = dict(title = 'All time series', tickangle=45), yaxis = dict(title = 'Number of voxels'), margin={'t': 10})