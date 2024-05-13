from flask import Flask, render_template, request
import requests
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/', methods=['GET', 'POST'])
def index():
    default_values = {
        'fetchType': 'all',
        'startDate': '',
        'endDate': '',
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
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImlkIjoiNDAwIn0sImlhdCI6MTU4NTExNjQzMH0.b-XFiavU0CI_V06xSqnZf2o7n4MGA9ojIn3SEiyHSho'  # This should be a valid token
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            leaves = response.json().get('data', [])
            app.logger.debug("API data fetched successfully")
        else:
            app.logger.error(f"Failed to fetch data: {response.status_code} {response.text}")
            leaves = []

        return render_template('index.html', leaves=leaves, values=request.form)

    return render_template('index.html', values=default_values)

if __name__ == '__main__':
    app.run(debug=True)
