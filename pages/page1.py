# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html


main_md = dcc.Markdown('''

For each participant, data collected during a single scanning session consists of 7 individual scans, depicted below.
The session started with a T1-weighted sequence to acquire a high resolution anatomical image.
This was followed by multi-echo functional MRI scans that were completed in two consecutive runs, each run consisting of 3 scans: 1 resting state scan, 1 motor task scan, and one emotion task scan.
For functional Run 1, the motor task is a block paradigm with alternating blocks of rest and right-hand finger tapping, while the emotion task is an adapted Hariri block paradigm (citation) with alternating blocks of shape and face matching tasks.
For functional Run 2, the motor and emotion tasks are mentalised versions of those in functional Run 1, using the same block timing.

''')


main_md2 = dcc.Markdown('''
In a typical neurofeedback session, a set of anatomical and functional scans are usually acquired before the training starts. These mostly undergo standard, minimal preprocessing steps to generate registration, segmentation, and localisation templates in the participant functional space, which assist real-time realignment, extraction of region-based neurofeedback (or tissue compartment) signals, and serves to minimise the required per-volume processing time. For this dataset, template data are required for extracting the neurofeedback signals from the applicable regions of interest: the motor cortex and the amygdala. Both the anatomical scan (together with an appropriately selected atlas) and the task scans of functional Run 1 can be used to generate, respectively, anatomically and functionally localised regions of interest.

To facilitate the development of real-time multi-echo processing methods, all functional scans collected for Run 1 and Run 2 use a multi-echo EPI sequence with 3 echoes. The resting state scan of Run 1 can be used to calculate quantitative multi-echo related data such as T2* or S0 maps, which can in turn be used for echo combination or other use cases during the subsequent scans.
''')


layout = html.Div([
            html.Div(
                html.H2('Overview'),
                style={
                    'marginBottom': 25,
                    'marginTop': 25,
                    'marginLeft': '5%',
                    'maxWidth': '90%',
                    'textAlign': 'center'
                }
            ),
            html.Div([
                main_md,
                html.Img(src="/assets/data_descriptor.png", width="100%"),
                html.Br([]),
                html.Br([]),
                main_md2,
                ],
                style={
                    'marginLeft': '5%',
                    'maxWidth': '90%',
                }
            ),

])