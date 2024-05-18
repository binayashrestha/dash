import dash
from dash import dcc, html, Input, Output, callback
from datetime import date

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.Div(
            [
                html.Div("Start Date:"),
                dcc.DatePickerSingle(
                    id="start-date-picker",
                    min_date_allowed=date(2023, 1, 1),  # More readable date objects
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
                    value="10",  # Set default value to 10
                    style={"marginLeft": "10px"},
                ),
                html.Div(id="record-size-output"),  
            ]
        )
    ]
)


# Callback for start date picker
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


# Callback for end date picker (simplified)
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


# New callback for record size input
@callback(
    Output("record-size-output", "children"), Input("record-size-input", "value")
)
def update_record_size_output(input_value):
    if input_value:
        return f"Record Size: {input_value}"
    else:
        return "Record Size: Not specified"


if __name__ == "__main__":
    app.run_server(debug=True)