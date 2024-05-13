from dotenv import load_dotenv
import os
import requests
import csv

load_dotenv()

url = "https://dev.vyaguta.lftechnology.com.np/api/leave/leaves"
params = {
    'fetchType': 'all',
    'startDate': '2024-01-01',
    'endDate': '2024-05-05',
    'size': 1,
    'roleType': 'issuer'
}
api_token = os.getenv('API_TOKEN')
headers = {
    'Authorization': f'Bearer {api_token}'
}
response = requests.get(url, headers=headers, params=params)
api_leaves = response.json().get('data', [])

csv_file_path = '/home/leapfrog/llm/llm_files/task/1_generate_dataset/api/output.csv'
csv_leaves = []
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    csv_leaves = list(csv_reader)

merged_leaves = api_leaves + csv_leaves
print("Merged Leaves:")
print(merged_leaves)