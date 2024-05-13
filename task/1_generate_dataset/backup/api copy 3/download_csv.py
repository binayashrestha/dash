import json
import csv
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the API token from the environment variable
api_token = os.getenv('API_TOKEN')

# Set the API endpoint URL and headers
url = 'https://dev.vyaguta.lftechnology.com.np/api/leave/leaves'
headers = {
    'Authorization': f'Bearer {api_token}'
}

# Set the query parameters
params = {
    'fetchType': 'all',
    'startDate': '2015-07-17',
    'endDate': '2024-05-05',
    'size': 10,
    'roleType': 'issuer'
}

# Send a GET request to the API
response = requests.get(url, headers=headers, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Extract the JSON data from the response
    json_data = response.json()

    # Define the keys to be included in the CSV
    selected_keys = [
        'id',
        'empId',
        'firstName',
        'lastName',
        'email',
        'designationName',
        'departmentDescription',
        'leaveIssuerId',
        'leaveIssuerFirstName',
        'leaveIssuerLastName',
        'startDate',
        'endDate',
        'leaveDays',
        'reason',
        'status',
        'leaveTypeName',
        'createdAt',
        'updatedAt'
    ]
    # Open a new CSV file for writing
    with open('output.csv', 'w', newline='') as csvfile:
        # Create a CSV writer object
        writer = csv.writer(csvfile)

        # Write the header row
        writer.writerow(selected_keys)

        # Write the data rows
        for row in json_data['data']:
            values = [row.get(key, '') for key in selected_keys]
            writer.writerow(values)

    print("CSV file created successfully!")
else:
    print(f"Error: {response.status_code} - {response.text}")