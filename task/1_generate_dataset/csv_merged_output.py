from dotenv import load_dotenv
import os
import requests
import csv
from io import StringIO

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
    'id', 'empId', 'firstName', 'lastName', 'email', 'designationName',
    'departmentDescription', 'leaveIssuerId', 'leaveIssuerFirstName',
    'leaveIssuerLastName', 'startDate', 'endDate', 'leaveDays', 'reason',
    'status', 'leaveTypeName', 'createdAt', 'updatedAt'
]

# Filter the API response to include only the desired columns
filtered_api_leaves = [{col: leave.get(col) for col in desired_columns} for leave in api_leaves]

# Read the existing CSV file and filter the columns
csv_file_path = '/home/leapfrog/llm/llm_files/task/1_generate_dataset/api/output.csv'
csv_leaves = []
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        filtered_row = {col: row.get(col) for col in desired_columns}
        csv_leaves.append(filtered_row)

# Merge the two CSV files
merged_leaves = filtered_api_leaves + csv_leaves

# Define the columns for the filtered merged CSV file
filtered_merged_columns = [
    'empId', 'firstName', 'lastName', 'designationName', 'departmentDescription',
    'startDate', 'endDate', 'leaveDays', 'status', 'leaveTypeName'
]

# Filter the merged leaves to include only the specified columns
filtered_merged_leaves = [{col: leave.get(col) for col in filtered_merged_columns} for leave in merged_leaves]
