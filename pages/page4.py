# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html

main_md = dcc.Markdown('''

''')


layout = html.Div([
    html.H2('About',
    style={
        'textAlign': 'center',
        'marginBottom': 25,
        'marginTop': 25,
    }),
    main_md,
],
style={
    'marginBottom': 25,
    'marginTop': 25,
    'marginLeft': '5%',
    'maxWidth': '90%',
})