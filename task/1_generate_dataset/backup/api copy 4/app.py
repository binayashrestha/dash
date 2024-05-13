import os
import requests
import csv
from flask import Flask, render_template, request
from io import StringIO


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    leaves = []
    form_data = {}

    if request.method == 'POST':
        form_data = request.form.to_dict()

        if 'csv_file' in request.files:
            csv_file = request.files['csv_file']
            if csv_file.filename != '':
                csv_data = csv_file.read().decode('utf-8')
                csv_reader = csv.DictReader(StringIO(csv_data))
                leaves = list(csv_reader)

        if not leaves:
            fetch_type = form_data.get('fetchType', 'all')
            start_date = form_data.get('startDate', '')
            end_date = form_data.get('endDate', '')
            size = form_data.get('size', 10)
            role_type = form_data.get('roleType', 'issuer')

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

        return render_template('index.html', leaves=leaves, form_data=form_data)

    return render_template('index.html', form_data=form_data)

if __name__ == '__main__':
    app.run(debug=True)