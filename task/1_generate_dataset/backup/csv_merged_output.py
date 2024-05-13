from dotenv import load_dotenv
import os
import requests
import csv

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

# Convert filtered API response to a CSV file
api_csv_file_path = '/home/leapfrog/llm/llm_files/task/1_generate_dataset/api/api_output.csv'
with open(api_csv_file_path, 'w', newline='') as api_csv_file:
    csv_writer = csv.DictWriter(api_csv_file, fieldnames=desired_columns)
    csv_writer.writeheader()
    csv_writer.writerows(filtered_api_leaves)

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

# Write the merged leaves to a new CSV file
merged_csv_file_path = '/home/leapfrog/llm/llm_files/task/1_generate_dataset/api/merged_output.csv'
with open(merged_csv_file_path, 'w', newline='') as merged_csv_file:
    csv_writer = csv.DictWriter(merged_csv_file, fieldnames=desired_columns)
    csv_writer.writeheader()
    csv_writer.writerows(merged_leaves)


# Define the columns for the filtered merged CSV file
filtered_merged_columns = [
    'empId', 'firstName', 'lastName', 'designationName', 'departmentDescription',
    'startDate', 'endDate', 'leaveDays', 'status', 'leaveTypeName'
]

# Filter the merged leaves to include only the specified columns
filtered_merged_leaves = [{col: leave.get(col) for col in filtered_merged_columns} for leave in merged_leaves]

# Write the filtered merged leaves to a new CSV file
filtered_merged_csv_file_path = '/home/leapfrog/llm/llm_files/task/1_generate_dataset/api/filtered_merged_output.csv'
with open(filtered_merged_csv_file_path, 'w', newline='') as filtered_merged_csv_file:
    csv_writer = csv.DictWriter(filtered_merged_csv_file, fieldnames=filtered_merged_columns)
    csv_writer.writeheader()
    csv_writer.writerows(filtered_merged_leaves)

print(f"Merged Leaves successfully written to {merged_csv_file_path}")