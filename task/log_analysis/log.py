import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import IsolationForest

# Simulated log data
data = {
    'timestamp': [datetime.now() for _ in range(1000)],
    'user_id': np.random.randint(1, 100, size=1000),
    'activity': np.random.choice(['login', 'logout', 'purchase', 'error', 'navigate'], size=1000),
    'response_time': np.random.exponential(scale=1.0, size=1000) # Response time in seconds
}

# Create a DataFrame
df = pd.DataFrame(data)

# Function to ingest logs
def ingest_logs(log_data):
    # Assuming log_data is a DataFrame
    return log_data

# Function to process logs
def process_logs(logs):
    # Example processing: Filter errors and explicitly copy to a new DataFrame
    error_logs = logs[logs['activity'] == 'error'].copy()
    return error_logs


# Function to detect anomalies in log data
def detect_anomalies(logs):
    # Using Isolation Forest for anomaly detection
    model = IsolationForest(n_estimators=50, contamination=0.1)
    logs['anomaly'] = model.fit_predict(logs[['response_time']])
    anomalies = logs[logs['anomaly'] == -1]
    return anomalies

# Main function to simulate log ingestion, processing and anomaly detection
def main():
    logs = ingest_logs(df)
    processed_logs = process_logs(logs)
    anomalies = detect_anomalies(processed_logs)
    print("Processed Logs Sample:")
    print(processed_logs.head(100))
    print("\nDetected Anomalies:")
    print(anomalies.head(100))

# Run the main function
if __name__ == "__main__":
    main()
