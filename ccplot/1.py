import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load the dataset
url = "https://raw.githubusercontent.com/plotly/datasets/master/diabetes-vid.csv"
df = pd.read_csv(url)

# Initialize the Dash app (normally in a standalone script)
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    dcc.Dropdown(
        id='outcome-dropdown',
        options=[{'label': x, 'value': x} for x in df['Outcome'].unique()],
        value=df['Outcome'].unique()[0],
        clearable=False
    ),
    dcc.Graph(id='scatter-plot')
])

# Define the callback to update the graph
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('outcome-dropdown', 'value')]
)
def update_graph(selected_outcome):
    filtered_df = df[df['Outcome'] == selected_outcome]
    fig = px.scatter(filtered_df, x='BloodPressure', y='BMI', color='Age',
                     title=f"Blood Pressure vs. BMI, Filtered by Outcome {selected_outcome}")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
