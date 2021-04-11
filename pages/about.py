# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

description_md = dcc.Markdown('''
`rt-me-fMRI` is a multi-echo functional magnetic resonance imaging dataset from 28 healthy volunteers, with four task-based and two resting state runs.
Its main purpose is to advance the development of methods for real-time multi-echo fMRI analysis with applications in neurofeedback, real-time quality control, and adaptive paradigms, although the variety of experimental task paradigms can support multiple use cases.
Tasks include finger tapping, emotional face and shape matching, imagined finger tapping and imagined emotion processing.

The `rt-me-fMRI` dataset was collected as part of a research project on fMRI neurofeedback methods, run in partnership by the [Electrical Engineering Department](https://www.tue.nl/en/our-university/departments/electrical-engineering/) at the Eindhoven University of Technology (The Netherlands), and [Philips research](https://www.philips.com/a-w/research/locations/eindhoven.html) (Eindhoven, The Netherlands).
The project was funded by the foundation [Health Holland LSH-TKI](https://www.health-holland.com/funding-opportunities) (grant LSHM16053-SGF).

For more information, please contact: `j.s.heunis(at)tue(dot)nl`

Below are links for easy access of the data, data derivatives, articles, and related output.

''')


# Further information is available at https://github.com/jsheunis/rt-me-fMRI
consent_md = dcc.Markdown('''
All participants provided fully informed and written consent to participate in the study and for their maximally de-identified data to be shared publicly under specific GDPR-compliant conditions.
Templates for informed consent and GDPR-conditions were adapted from the [Open Brain Consent](https://open-brain-consent.readthedocs.io/en/stable/gdpr/index.html) documentation.
''')
gdpr_md = dcc.Markdown('''
The dataset was collected, processed and shared in accordance with the European Union's [General Data Protection Regulation](https://gdpr.eu/tag/gdpr/) (GDPR) as approved by Data Protection Officers at the research institution.
These specific conditions aim for personal data privacy to be prioritised while adhering to FAIR data standards ("findable, accessible, interoperable, reusable"). 
Procedures included de-identifying brain images (e.g. removing personally identifiable information from image filenames and metadata and removing facial features from T1-weighted images), converting the data to BIDS format, employing a Data Use Agreement, and keeping participants fully informed about each of these steps and the associated risks and benefits.
''')
download_md = dcc.Markdown('''
Researchers wishing to use the `rt-me-fMRI` dataset for the purpose of scientific research or education in the field of functional magnetic resonance imaging have to agree to the terms of a [Data Use Agreement](https://github.com/jsheunis/rt-me-fMRI/blob/master/DUA.md) when downloading the data.

The dataset can be accessed on DataverseNL:

''')

attribution1_md = dcc.Markdown('''
Papers, book chapters, books, posters, oral presentations, and all other presentations of results derived from the `rt-me-fMRI` dataset should acknowledge the origin of the data as follows:
''')
attribution2_md = dcc.Markdown('''
In addition, please use the following citation:
''')

# [***Heunis et al., 2020. Evaluating multi-echo fMRI combination and T2\*-mapping for offline and real-time BOLD sensitivity. BioRxiv preprint.***]()




layout = html.Div([
    html.H2('About',
    style={
        'textAlign': 'center',
        'marginBottom': 25,
        'marginTop': 25,
    }),
    html.Br(),
    description_md,

    html.H2('Quick links',
    style={
        'textAlign': 'center',
        'marginBottom': 25,
        'marginTop': 25,
    }),
    dbc.Row([
        dbc.Col([
            html.Img(src="/assets/undraw_share_link_qtxe.png", width="80%",
                style={
                    'marginTop': '0px',
                }
                )
            ], width={"size": 5, "offset": 0}),
        dbc.Col([
            html.Br(),
            dbc.Button(
                html.Span([html.I(className="fas fa-download ml-2"), '   Download dataset']),
                href="https://dataverse.nl/dataverse/rt-me-fmri",
                style={
                    'marginLeft': '5px',
                    'marginRight': '10px',
                }
                # "&#8681; Download rt-me-fMRI dataset", className="mr-1"
                ),
            html.Br(),
            html.Br(),
            dbc.Button(
                html.Span([html.I(className="fas fa-book ml-2"), '   Data article']),
                href="https://doi.org/10.12688/f1000research.29988.1",
                style={
                    'marginLeft': '5px',
                    'marginRight': '10px',
                }
                # "&#8681; Download rt-me-fMRI dataset", className="mr-1"
            ),
            html.Br(),
            html.Br(),
            dbc.Button(
                html.Span([html.I(className="fas fa-book ml-2"), '   Methods article']),
                href="https://doi.org/10.1101/2020.12.08.416768",
                style={
                    'marginLeft': '5px',
                    'marginRight': '10px',
                }
                # "&#8681; Download rt-me-fMRI dataset", className="mr-1"
            ),

            ], width={"size": 3, "offset": 0}),
        dbc.Col([
            html.Br(),
            dbc.Button(
                html.Span([html.I(className="fab fa-github ml-2"), '   Project GitHub Repo']),
                href="https://github.com/jsheunis/rt-me-fMRI",
                style={
                    'marginLeft': '5px',
                    'marginRight': '10px',
                }
                # "&#8681; Download rt-me-fMRI dataset", className="mr-1"
                ),
            html.Br(),
            html.Br(),
            dbc.Button(
                html.Span([html.I(className="fab fa-github ml-2"), '   Dash App GitHub Repo']),
                href="https://github.com/jsheunis/rt-me-fmri-dash",
                style={
                    'marginLeft': '5px',
                    'marginRight': '10px',
                }
                # "&#8681; Download rt-me-fMRI dataset", className="mr-1"
            ),
            html.Br(),
            html.Br(),
            dbc.Button(
                html.Span([html.I(className="fab fa-github ml-2"), '   fMRwhy toolbox']),
                href="https://github.com/jsheunis/fMRwhy",
                style={
                    'marginLeft': '5px',
                    'marginRight': '10px',
                }
                # "&#8681; Download rt-me-fMRI dataset", className="mr-1"
            ),

            ], width={"size": 3, "offset": 0}),
        
        ]
    ),
    
],
style={
    'marginBottom': 25,
    'marginTop': 25,
    'marginLeft': '5%',
    'maxWidth': '90%',
})