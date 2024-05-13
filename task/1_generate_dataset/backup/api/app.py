from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    url = "https://dev.vyaguta.lftechnology.com.np/api/leave/leaves"
    params = {
        'fetchType': 'all',
        'startDate': '2021-07-17',
        'endDate': '2024-04-23',
        'size': 10,
        'roleType': 'issuer'
    }
    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImlkIjoiNDAwIn0sImlhdCI6MTU4NTExNjQzMH0.b-XFiavU0CI_V06xSqnZf2o7n4MGA9ojIn3SEiyHSho'  # This should be a valid token
    }
    response = requests.get(url, headers=headers, params=params)
    leaves = response.json().get('data', [])

    return render_template('index.html', leaves=leaves)

if __name__ == '__main__':
    app.run(debug=True)
