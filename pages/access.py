# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

ethics_md = dcc.Markdown('''
The `rt-me-fMRI` dataset was collected as part of a study for which ethics approval was granted.
The medical ethical review board at the Máxima Medisch Centrum (Veldhoven, The Netherlands) confirmed that the study protocol is in accordance with the Dutch national law on medical-scientific research conducted on human participants ([the WMO](https://wetten.overheid.nl/BWBR0009408/2020-01-01)).
''')
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
    html.H2('Data access',
    style={
        'textAlign': 'center',
        'marginBottom': 25,
        'marginTop': 25,
    }),
    dbc.Row([
        dbc.Col([
            html.H4('Download data',
            style={
                'textAlign': 'left',
                'marginBottom': 25,
                'marginTop': 25,
            }),
            html.Div(
                download_md,
                style={
                    'textAlign': 'justify',
                }
            ),
            
            dbc.Button(
                html.Span([html.I(className="fas fa-download ml-2"), '   Download rt-me-fMRI dataset']),
                href="https://dataverse.nl/dataverse/rt-me-fmri"
                # "&#8681; Download rt-me-fMRI dataset", className="mr-1"
                ),
            ]
        ),
        dbc.Col(
            html.Img(src="/assets/undraw_data_processing_yrrv.png", width="80%")
        ),
        ]
    ),
    
    html.H4('Attribution',
    style={
        'textAlign': 'left',
        'marginBottom': 25,
        'marginTop': 25,
    }),
    attribution1_md,
    html.Blockquote(
        'Data were provided (in part) by the Electrical Engineering Department, Eindhoven University of Technology, The Netherlands and Kempenhaeghe Epilepsy Center, Heeze, The Netherlands',
        style={
            'borderLeft': '4px solid rgb(98, 186, 181)',
            'paddingLeft': '1rem',
            'paddingRight': '1rem',
            'marginTop': '2rem',
            'marginBottom': '2rem',
            'marginLeft': '10rem',
            'marginRight': '10rem',
            'fontStyle': 'italic',
            'fontSize': '0.85em',
            'backgroundColor': 'rgb(237, 249, 247)',
            'paddingTop': '5px',
            'paddingBottom': '5px'
            
        }
    ),
    attribution2_md,
    html.Blockquote(
        'Heunis et al., 2020. Evaluating multi-echo fMRI combination and T2*-mapping for offline and real-time BOLD sensitivity. BioRxiv preprint.',
        style={
            'borderLeft': '4px solid rgb(98, 186, 181)',
            'paddingLeft': '1rem',
            'paddingRight': '1rem',
            'marginTop': '2rem',
            'marginBottom': '2rem',
            'marginLeft': '10rem',
            'marginRight': '10rem',
            'fontStyle': 'italic',
            'fontSize': '0.85em',
            'backgroundColor': 'rgb(237, 249, 247)',
            'paddingTop': '5px',
            'paddingBottom': '5px'
        }
    ),
    html.H4('Ethics approval',
    style={
        'textAlign': 'left',
        'marginBottom': 25,
        'marginTop': 25,
    }),
    ethics_md,
    html.H4('Informed consent',
    style={
        'textAlign': 'left',
        'marginBottom': 25,
        'marginTop': 25,
    }),
    consent_md,
    html.H4('GDPR compliance',
    style={
        'textAlign': 'left',
        'marginBottom': 25,
        'marginTop': 25,
    }),
    gdpr_md,
],
style={
    'marginBottom': 25,
    'marginTop': 25,
    'marginLeft': '5%',
    'maxWidth': '90%',
})