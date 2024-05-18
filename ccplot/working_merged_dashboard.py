from dash import Dash, dcc, html, Input, Output, State, callback, Patch, clientside_callback
import plotly.express as px
import plotly.io as pio
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
import dash_ag_grid as dag
from datetime import date

df = px.data.gapminder()
years = df.year.unique()
continents = df.continent.unique()

# 1. External Stylesheets Configuration:
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME, dbc_css])

# 2. Theme Switch and Control Setup:
color_mode_switch = html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="switch"),
        dbc.Switch(id="switch", value=True, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="switch"),
    ]
)

# 3. Theme Changer and Header:
theme_controls = html.Div(
    [ThemeChangerAIO(aio_id="theme"), color_mode_switch],
    className="hstack gap-3 mt-2"
)

header = html.H4(
    "Leave Analysis Dashboard", className="bg-primary text-white p-2 mb-2 text-center"
)

# 4. Data Grid Setup:
grid = dag.AgGrid(
    id="grid",
    columnDefs=[{"field": i} for i in df.columns],
    rowData=df.to_dict("records"),
    defaultColDef={"flex": 1, "minWidth": 120, "sortable": True, "resizable": True, "filter": True},
    dashGridOptions={"rowSelection": "multiple"},
)

# Dropdown for Selecting Indicators:
dropdown = html.Div(
    [
        dbc.Label("Select indicator (y-axis)"),
        dcc.Dropdown(
            ["gdpPercap", "lifeExp", "pop"],
            "pop",
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

# Date Picker and Record Size Input:
datepicker_controls = html.Div(
    [
        html.Div(
            [
                html.Div("Start Date:"),
                dcc.DatePickerSingle(
                    id="start-date-picker",
                    min_date_allowed=date(2023, 1, 1),
                    max_date_allowed=date(2023, 12, 31),
                    initial_visible_month=date(2023, 1, 1),
                    date=date(2023, 1, 1),
                    display_format="YYYY/MM/DD",
                ),
                html.Div(id="start-date-output"),
            ],
            style={"display": "flex", "alignItems": "center", "marginBottom": "10px"},
        ),
        html.Div(
            [
                html.Div("End Date:"),
                dcc.DatePickerSingle(
                    id="end-date-picker",
                    min_date_allowed=date(2023, 1, 1),
                    max_date_allowed=date(2023, 12, 31),
                    initial_visible_month=date(2023, 5, 5),
                    date=date(2023, 5, 5),
                    display_format="YYYY/MM/DD",
                ),
                html.Div(id="end-date-output"),
            ],
            style={"display": "flex", "alignItems": "center"},
        ),
        html.Div(
            [
                html.Div("Record Size:"),
                dcc.Input(
                    id="record-size-input",
                    type="text",
                    placeholder="Additional Info",
                    debounce=True,
                    value="10",
                    style={"marginLeft": "10px"},
                ),
                html.Div(id="record-size-output"),
            ]
        )
    ],
    className="mb-4",
)

controls = dbc.Card(
    [datepicker_controls, dropdown, checklist, slider],
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
            ], width=4),
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
    Output("line-chart", "figure"),
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

# Callbacks for date pickers and record size input
@callback(Output("start-date-output", "children"), Input("start-date-picker", "date"))
def update_start_date_output(date_value):
    try:
        if date_value:
            date_object = date.fromisoformat(date_value)
            date_string = date_object.strftime("%B %d, %Y")
            return f"Start Date: {date_string}"
        else:
            return "Start Date: Not selected"
    except ValueError:
        return "Invalid date format"

@callback(Output("end-date-output", "children"), Input("end-date-picker", "date"))
def update_end_date_output(date_value):
    try:
        if date_value:
            date_object = date.fromisoformat(date_value)
            date_string = date_object.strftime("%B %d, %Y")
            return f"End Date: {date_string}"
        else:
            return "End Date: Not selected"
    except ValueError:
        return "Invalid date format"

@callback(Output("record-size-output", "children"), Input("record-size-input", "value"))
def update_record_size_output(input_value):
    if input_value:
        return f"Record Size: {input_value}"
    else:
        return "Record Size: Not specified"

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
    Output("line-chart", "figure", allow_duplicate=True),
    Output("scatter-chart", "figure", allow_duplicate=True),
    Input(ThemeChangerAIO.ids.radio("theme"), "value"),
    Input("switch", "value"),
    prevent_initial_call=True
)
def update_template(theme, color_mode_switch_on):
    theme_name = template_from_url(theme)
    template_name = theme_name if color_mode_switch_on else theme_name + "_dark"

    patched_figure = Patch()
    patched_figure["layout"]["template"] = pio.templates[template_name]
    return patched_figure, patched_figure

if __name__ == "__main__":
    app.run_server(debug=True)