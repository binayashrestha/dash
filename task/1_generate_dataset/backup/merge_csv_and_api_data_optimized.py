from dotenv import load_dotenv
import os
import requests
import csv
from io import StringIO
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

def validate_date(date_string: str) -> bool:
    """
    Validate a date string in the format YYYY-MM-DD.

    Args:
        date_string (str): Date string to validate.

    Returns:
        bool: True if the date string is valid, False otherwise.
    """
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def get_leaves_from_api(fetch_type: str, start_date: str, end_date: str, size: int, role_type: str) -> list:
    """
    Get leaves from API.

    Args:
        fetch_type (str): Fetch type.
        start_date (str): Start date.
        end_date (str): End date.
        size (int): Size.
        role_type (str): Role type.

    Returns:
        list: List of leaves.
    """
    if not validate_date(start_date) or not validate_date(end_date):
        raise ValueError("Invalid date format. Should be YYYY-MM-DD")

    url = os.getenv('API_ENDPOINT', "https://dev.vyaguta.lftechnology.com.np/api/leave/leaves")
    params = {
        'fetchType': fetch_type,
        'startDate': start_date,
        'endDate': end_date,
        'size': size,
        'roleType': role_type
    }
    api_token = os.getenv('API_TOKEN')

    headers = {
        'Authorization': f'Bearer {api_token}'
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json().get('data', [])
    except requests.RequestException as e:
        print(f"Error: {e}")
        return []

def get_leaves_from_csv(csv_file_path: str) -> list:
    """
    Get leaves from CSV file.

    Args:
        csv_file_path (str): CSV file path.

    Returns:
        list: List of leaves.
    """
    try:
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            return list(csv_reader)
    except FileNotFoundError:
        print(f"Error: File not found: {csv_file_path}")
        return []

def main():
    # Get leaves from API
    fetch_type = 'all'
    start_date = '2024-01-01'
    end_date = '2024-05-05'
    size = 10
    role_type = 'issuer'
    api_leaves = get_leaves_from_api(fetch_type, start_date, end_date, size, role_type)
    print("Leaves from API:")
    print(api_leaves)

    # Get leaves from CSV file
    csv_file_path = os.getenv('CSV_FILE_PATH', '/home/leapfrog/llm/llm_files/task/1_generate_dataset/api/output.csv')
    csv_leaves = get_leaves_from_csv(csv_file_path)
    print("\nLeaves from CSV file:")
    print(csv_leaves)

if __name__ == '__main__':
    main()