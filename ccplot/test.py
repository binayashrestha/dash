import pandas as pd

# Specify the URL of the CSV file
url = "https://raw.githubusercontent.com/binayashrestha/dash/main/task/1_generate_dataset/filtered_merged_output.csv"

# Read the CSV file from the URL into a DataFrame
df = pd.read_csv(url)

# Convert the 'startDate' column to datetime format
df['startDate'] = pd.to_datetime(df['startDate'])

# Extract the year into a new column
df['startYear'] = df['startDate'].dt.year

# Print the first few rows of the DataFrame
print(df)
