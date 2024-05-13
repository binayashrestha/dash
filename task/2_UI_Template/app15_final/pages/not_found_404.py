import dash
from dash import html

dash.register_page(__name__)

layout = html.Div(children=[
    html.H1(children='Page not found'),

    html.Div(children='''
        This is a custom 404 page layout
    '''),
])