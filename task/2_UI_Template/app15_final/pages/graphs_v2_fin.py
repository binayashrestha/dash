import dash
from dash import html, dcc

dash.register_page(__name__, order=1, name='Graphs', title='Dash App | Graphs')

layout = html.Div(children=[
    html.H1(children='This is our Graphs page'),

    html.Div(children='''
        This is our Graphs page content.
    '''),
])