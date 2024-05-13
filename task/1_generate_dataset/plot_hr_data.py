from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

# Integrated CSV data processing from csv_merged_output.py
from dotenv import load_dotenv
import os
import requests

load_dotenv()

url = "https://dev.vyaguta.lftechnology.com.np/api/leave/leaves"
params = {
    'fetchType': 'all',
    'startDate': '2023-01-01',
    'endDate': '2023-05-05',
    'size': 100,
    'roleType': 'issuer'
}
api_token = os.getenv('API_TOKEN')
headers = {
    'Authorization': f'Bearer {api_token}'
}
response = requests.get(url, headers=headers, params=params)
api_leaves = response.json().get('data', [])

# Define the desired columns
desired_columns = [
    'designationName', 'startDate', 'leaveDays'  # Updated column names
]

# Filter the API response to include only the desired columns
filtered_api_leaves = [{col: leave.get(col) for col in desired_columns} for leave in api_leaves]
df = pd.DataFrame(filtered_api_leaves)

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Title of Dash App', style={'textAlign':'center'}),
    dcc.Dropdown(df['designationName'].unique(), 'Some Default Designation', id='dropdown-selection'),
    dcc.Graph(id='graph-content')
])

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    dff = df[df['designationName'] == value]
    return px.line(dff, x='startDate', y='leaveDays')

if __name__ == '__main__':
    app.run(debug=True)
