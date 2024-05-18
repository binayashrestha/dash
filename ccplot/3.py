import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load the diabetes data from the CSV URL
url = "https://raw.githubusercontent.com/plotly/datasets/master/diabetes-vid.csv"
df = pd.read_csv(url)

# Create a scatter plot using Plotly Express
fig = px.scatter(
    df, x="BloodPressure", y="BMI", color="Age", hover_data=["Outcome"]
)

# Create a Dash app
app = Dash(__name__)

# Create a layout for the app
app.layout = html.Div(
    children=[
        html.H1(children="Blood Pressure vs BMI"),
        dcc.Dropdown(
            id="outcome-filter",
            options=[{"label": outcome, "value": outcome} for outcome in df["Outcome"].unique()],
            value="no",
        ),
        dcc.Graph(id="blood-pressure-vs-bmi"),
    ]
)

# Create a callback function to update the scatter plot when the dropdown selection changes
@app.callback(
    Output(component_id="blood-pressure-vs-bmi", component_property="figure"),
    Input(component_id="outcome-filter", component_property="value"),
)
def update_figure(selected_outcome):
    filtered_df = df[df["Outcome"] == selected_outcome]
    fig = px.scatter(filtered_df, x="BloodPressure", y="BMI", color="Age", hover_data=["Outcome"])
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)

