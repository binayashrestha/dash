import os
import requests
import csv
from flask import Flask, render_template, request
from io import StringIO


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    default_values = {
        'fetchType': 'all',
        'startDate': '2024/05/01',
        'endDate': '2024/05/04',
        'size': 10,
        'roleType': 'issuer'
    }

    if request.method == 'POST':
        fetch_type = request.form.get('fetchType', 'all')
        start_date = request.form.get('startDate', '')
        end_date = request.form.get('endDate', '')
        size = request.form.get('size', 10)
        role_type = request.form.get('roleType', 'issuer')

        url = "https://dev.vyaguta.lftechnology.com.np/api/leave/leaves"
        params = {
            'fetchType': fetch_type,
            'startDate': start_date,
            'endDate': end_date,
            'size': size,
            'roleType': role_type
        }
        headers = {
            'Authorization': f"Bearer {os.getenv('API_TOKEN')}"
        }
        response = requests.get(url, headers=headers, params=params)
        leaves = response.json().get('data', [])

        if 'csv_file' in request.files:
            csv_file = request.files['csv_file']
            if csv_file.filename != '':
                csv_data = csv_file.read().decode('utf-8')
                csv_reader = csv.DictReader(StringIO(csv_data))
                csv_leaves = list(csv_reader)
                leaves.extend(csv_leaves)

        print(leaves)
        return render_template('index.html', leaves=leaves, values=request.form)

    return render_template('index.html', values=default_values)

if __name__ == '__main__':
    app.run(debug=True)