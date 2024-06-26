from dash import Dash, dcc, html, Input, Output, State, callback, Patch, clientside_callback
import plotly.express as px
import plotly.io as pio
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
import dash_ag_grid as dag

df = px.data.gapminder()
years = df.year.unique()
continents = df.continent.unique()




# 1. External Stylesheets Configuration:
# stylesheet with the .dbc class to style  dcc, DataTable and AG Grid components with a Bootstrap theme
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME, dbc_css])

# 2. Theme Switch and Control Setup:
color_mode_switch =  html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="switch"),
        dbc.Switch( id="switch", value=True, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="switch"),
    ]
)

# 3. Theme Changer and Header:
# The ThemeChangerAIO loads all 52  Bootstrap themed figure templates to plotly.io
theme_controls = html.Div(
    [ThemeChangerAIO(aio_id="theme"), color_mode_switch],
    className="hstack gap-3 mt-2"
)

header = html.H4(
    "Leave Analysis Dashbord", className="bg-primary text-white p-2 mb-2 text-center"
)




# 4. Data Grid Setup:
grid = dag.AgGrid(
    id="grid",
    columnDefs=[{"field": i} for i in df.columns],
    rowData=df.to_dict("records"),
    defaultColDef={"flex": 1, "minWidth": 120, "sortable": True, "resizable": True, "filter": True},
    dashGridOptions={"rowSelection":"multiple"},
)

# 2. Dropdown for Selecting Indicators:
dropdown = html.Div(
    [
        dbc.Label("Select indicator (y-axis)"),
        dcc.Dropdown(
            ["gdpPercap", "lifeExp", "pop"],
            "gdpPercap",
            id="indicator",
            clearable=False,
        ),
    ],
    className="mb-4",
)

# Checklist for Selecting Continents:
checklist = html.Div(
    [
        dbc.Label("Select Continents"),
        dbc.Checklist(
            id="continents",
            options=continents,
            value=continents,
            inline=True,
        ),
    ],
    className="mb-4",
)

# Year Range Slider:
slider = html.Div(
    [
        dbc.Label("Select Years"),
        dcc.RangeSlider(
            years[0],
            years[-1],
            5,
            id="years",
            marks=None,
            tooltip={"placement": "bottom", "always_visible": True},
            value=[years[2], years[-2]],
            className="p-0",
        ),
    ],
    className="mb-4",
)






'''
    The controls are placed inside a Bootstrap Card component.
'''
controls = dbc.Card(
    [dropdown, checklist, slider],
    body=True,
)

tab1 = dbc.Tab([dcc.Graph(id="line-chart", figure=px.line(template="bootstrap"))], label="Line Chart")
tab2 = dbc.Tab([dcc.Graph(id="scatter-chart", figure=px.scatter(template="bootstrap"))], label="Scatter Chart")
tab3 = dbc.Tab([grid], label="Grid", className="p-4")
tabs = dbc.Card([tab1])
tabs2 = dbc.Card([tab2])
tabs3 = dbc.Card([tab3])








app.layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col([header], width=10),
            dbc.Col([theme_controls], width=2)
        ]),
        dbc.Row([
            dbc.Col([
                controls,
            ],  width=4),
            dbc.Col([tabs], width=4),
            dbc.Col([tabs2], width=4),
        ]),
        dbc.Row([
            dbc.Col([tabs3], width=4),
        ])
    ],
    fluid=True,
    className="dbc dbc-ag-grid",
)


@callback(
    Output("line-chart", "figure" ),
    Output("scatter-chart", "figure"),
    Output("grid", "dashGridOptions"),
    Input("indicator", "value"),
    Input("continents", "value"),
    Input("years", "value"),
    State(ThemeChangerAIO.ids.radio("theme"), "value"),
    State("switch", "value"),
)
def update(indicator, continent, yrs, theme, color_mode_switch_on):

    if continent == [] or indicator is None:
        return {}, {}, {}

    theme_name = template_from_url(theme)
    template_name = theme_name if color_mode_switch_on else theme_name + "_dark"

    dff = df[df.year.between(yrs[0], yrs[1])]
    dff = dff[dff.continent.isin(continent)]

    fig = px.line(
        dff,
        x="year",
        y=indicator,
        color="continent",
        line_group="country",
        template=template_name
    )

    fig_scatter = px.scatter(
        dff[dff.year == yrs[0]],
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="continent",
        log_x=True,
        size_max=60,
        template=template_name,
        title="Gapminder %s: %s theme" % (yrs[1], template_name),
    )


    grid_filter = f"{continent}.includes(params.data.continent) && params.data.year >= {yrs[0]} && params.data.year <= {yrs[1]}"
    dashGridOptions = {
        "isExternalFilterPresent": {"function": "true"},
        "doesExternalFilterPass": {"function": grid_filter},
    }

    return fig, fig_scatter, dashGridOptions


# updates the Bootstrap global light/dark color mode
clientside_callback(
    """
    switchOn => {       
       document.documentElement.setAttribute('data-bs-theme', switchOn ? 'light' : 'dark');  
       return window.dash_clientside.no_update
    }
    """,
    Output("switch", "id"),
    Input("switch", "value"),
)


# This callback makes updating figures with the new theme much faster
@callback(
    Output("line-chart", "figure", allow_duplicate=True ),
    Output("scatter-chart", "figure", allow_duplicate=True),
    Input(ThemeChangerAIO.ids.radio("theme"), "value"),
    Input("switch", "value"),
    prevent_initial_call=True
)
def update_template(theme, color_mode_switch_on):
    theme_name = template_from_url(theme)
    template_name = theme_name if color_mode_switch_on else theme_name + "_dark"

    patched_figure = Patch()
    # When using Patch() to update the figure template, you must use the figure template dict
    # from plotly.io  and not just the template name
    patched_figure["layout"]["template"] = pio.templates[template_name]
    return patched_figure, patched_figure


if __name__ == "__main__":
    app.run_server(debug=True)