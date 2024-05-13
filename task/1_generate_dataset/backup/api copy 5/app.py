from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import requests
import csv
from io import StringIO

app = Flask(__name__)

load_dotenv()

@app.route('/', methods=['GET', 'POST'])
def index():
    form_data = {
        'startDate': '2023-01-01',
        'endDate': '2023-05-05',
        'size': 10
    }

    if request.method == 'POST':
        # Handle form submission and CSV file upload
        form_data = request.form
        csv_file = request.files.get('csv_file')

        if csv_file:
            # Process the uploaded CSV file
            csv_data = csv_file.read().decode('utf-8')
            csv_leaves = list(csv.DictReader(StringIO(csv_data)))
        else:
            csv_leaves = []

        # Make API request to fetch leave records
        url = "https://dev.vyaguta.lftechnology.com.np/api/leave/leaves"
        params = {
            'fetchType': 'all',
            'startDate': form_data.get('startDate', '2023-01-01'),
            'endDate': form_data.get('endDate', '2023-05-05'),
            'size': form_data.get('size', 10),
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
            'empId', 'firstName', 'lastName', 'designationName', 'departmentDescription',
            'startDate', 'endDate', 'leaveDays', 'status', 'leaveTypeName'
        ]

        # Filter the API response to include only the desired columns
        filtered_api_leaves = [{col: leave.get(col) for col in desired_columns} for leave in api_leaves]

        # Merge the API leaves and CSV leaves
        merged_leaves = filtered_api_leaves + csv_leaves

        return render_template('index.html', leaves=merged_leaves, form_data=form_data)
    else:
        return render_template('index.html', form_data=form_data)

if __name__ == '__main__':
    app.run(debug=True)