# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html


main_md = dcc.Markdown('''

A full descriptions of the dataset (including participant details, ethics approval, experimental design, MRI protocol, preprocessing, and data quality)
can be accessed in the data article:

[***Heunis et al., 2021. rt-me-fMRI: A task and resting state dataset for real-time, multi-echo fMRI methods development and validation. F1000Research.***](https://doi.org/10.12688/f1000research.29988.1)

The `rt-me-fMRI` dataset was collected to explore multi-echo functional magnetic resonance imaging (fMRI) methods for real-time applications.
It contains 6 runs of resting state and task data from 28 healthy volunteers, along with T1w scans and physiology data.


For each participant, data collected during a single scanning session consists of 7 individual acquisitions, depicted below.
The session started with a T1-weighted sequence to acquire a high resolution anatomical image.
This was followed by multi-echo functional MRI scans that were completed in two consecutive sets, each set consisting of 3 acquisitions: 1 resting state scan, 1 task scan to elicit a motor processing response, and one task scan to elicit an emotion processing response.
For the first set, the motor processing task consists of alternating rest and right-hand finger tapping, while the emotion processing task has alternating blocks of shape and face matching.
For the second set of scans, the motor and emotion processing tasks are similar but imagined versions of those in the first set.

''')


main_md2 = dcc.Markdown('''
In a typical real-time fMRI session, a set of anatomical and functional scans are usually acquired before the training starts.
These mostly undergo standard, minimal preprocessing steps to generate registration, segmentation, and localisation templates in the participant functional space, which assist real-time realignment, extraction of region-based signals, and serves to minimise the required per-volume processing time.
For this dataset, template data can (for example) be used to extract neurofeedback signals from applicable regions of interest (e.g. the motor cortex, the amygdala, or the fusiform face area).
Both the anatomical scan (together with an appropriately selected atlas) and the task scans of the first functional set can in principle be used to generate, respectively, anatomically and functionally localised regions of interest.

To facilitate the development of real-time multi-echo processing methods, all functional scans use a multi-echo EPI sequence with 3 echoes. The first resting state scan can be used to calculate quantitative multi-echo related data such as T2* or S0 maps, which can in turn be used for echo combination or other use cases during the subsequent scans.
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
                html.Div([
                    html.Img(src="/assets/data_descriptor.png", width="85%"),],
                    style={
                        'textAlign': 'center'
                    }
                ),
                html.Br([]),
                main_md2,
                ],
                style={
                    'marginLeft': '5%',
                    'maxWidth': '90%',
                }
            ),

])