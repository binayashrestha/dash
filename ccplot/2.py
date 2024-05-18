import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# Load the data from the CSV file
url = 'https://raw.githubusercontent.com/plotly/datasets/master/diabetes-vid.csv'
df = pd.read_csv(url)

# Create the Dash app
app = Dash(__name__)

# Set up the app layout
app.layout = html.Div([
    html.H1('Diabetes Dashboard'),
    
    dcc.Dropdown(
        id='outcome-dropdown',
        options=[{'label': outcome, 'value': outcome} for outcome in df['Outcome'].unique()],
        value=df['Outcome'].unique()[0]
    ),
    
    dcc.Graph(id='scatter-plot')
])

# Set up the callback to update the scatter plot
@app.callback(
    Output('scatter-plot', 'figure'),
    Input('outcome-dropdown', 'value')
)
def update_scatter_plot(selected_outcome):
    filtered_df = df[df['Outcome'] == selected_outcome]
    
    fig = px.scatter(filtered_df, x='BMI', y='BloodPressure', color='Age',
                     title=f'Blood Pressure vs BMI (Outcome: {selected_outcome})')
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)