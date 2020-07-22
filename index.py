# -*- coding: utf-8 -*-
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app import app, server
from pages import home, page1, page2, page3, page4
import flask


nav_item1 = dbc.NavItem(dbc.NavLink("Overview", href="/pages/page1", external_link=True))
nav_item2 = dbc.NavItem(dbc.NavLink("Quality", href="/pages/page2", external_link=True))
nav_item3 = dbc.NavItem(dbc.NavLink("Multi-echo", href="/pages/page3", external_link=True))
nav_item4 = dbc.NavItem(dbc.NavLink("About", href="/pages/page4", external_link=True))

nav_bar_and_content_div = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    dbc.Navbar(
        dbc.Container(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(id='logo', src='assets/logo_jsheunis_3.jpeg', height="32px", className="avatar")),
                            dbc.Col(dbc.NavbarBrand("rt-me-fMRI", className="ml-2")),
                        ],
                        align="center",
                        no_gutters=True,
                    ),
                    href="/",
                ),
                dbc.NavbarToggler(id="navbar-toggler"),
                dbc.Collapse(
                    dbc.Nav(
                        [nav_item1, nav_item2, nav_item3, nav_item4], className="ml-auto", navbar=True
                    ),
                    id="navbar-collapse",
                    navbar=True,
                ),
            ]
        ),
        color="dark",
        dark=True,
        className="mb-5",
    ),

    html.Div(id='page-content')
    ]

)

def serve_layout():
    if flask.has_request_context():
        return nav_bar_and_content_div
    return html.Div([
        nav_bar_and_content_div,
        home.layout,
        page1.layout,
        page2.layout,
        page3.layout,
        page4.layout,
    ])


app.layout = serve_layout



###########################
# CALLBACKS AND FUNCTIONS #
###########################

# the same function (toggle_navbar_collapse) is used in all three callbacks
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open): # we use a callback to toggle the collapse on small screens
    if n:
        return not is_open
    return is_open


@app.callback(
    [Output('page-content', 'children'),
     Output('logo', 'src')],
    [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        logo_url = 'assets/logo_jsheunis_3.jpeg'
        return [home.layout, logo_url]
    elif pathname == '/pages/page1':
        logo_url = '../assets/logo_jsheunis_3.jpeg'
        return [page1.layout, logo_url]
    elif pathname == '/pages/page2':
        logo_url = '../assets/logo_jsheunis_3.jpeg'
        return [page2.layout, logo_url]
    elif pathname == '/pages/page3':
        logo_url = '../assets/logo_jsheunis_3.jpeg'
        return [page3.layout, logo_url]
    elif pathname == '/pages/page4':
        logo_url = '../assets/logo_jsheunis_3.jpeg'
        return [page4.layout, logo_url]
    else:
        return '404'



##############
# RUN SERVER #
##############

if __name__ == '__main__':
    app.run_server(debug=True)