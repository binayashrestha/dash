from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        fetch_type = request.form.get('fetchType')
        start_date = request.form.get('startDate')
        end_date = request.form.get('endDate')
        size = request.form.get('size')
        role_type = request.form.get('roleType')

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
        leaves = response.json().get('data', [])
        return render_template('index.html', leaves=leaves)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
