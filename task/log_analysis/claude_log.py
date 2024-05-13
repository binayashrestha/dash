import json
import time
from kafka import KafkaConsumer, KafkaProducer
from elasticsearch import Elasticsearch
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.ml.feature import StringIndexer, OneHotEncoder
from pyspark.ml.classification import RandomForestClassifier

# Data Ingestion
# Simulate log data generation and ingestion into Kafka
producer = KafkaProducer(bootstrap_servers='kafka:9092')
for _ in range(10):
    log_entry = {'timestamp': time.time(), 'level': 'INFO', 'message': 'This is a sample log message'}
    producer.send('log_topic', json.dumps(log_entry).encode('utf-8'))

# Data Storage and Processing
# Consume log data from Kafka and store in Elasticsearch
consumer = KafkaConsumer('log_topic', bootstrap_servers='kafka:9092')
es = Elasticsearch(['elasticsearch:9200'])
for msg in consumer:
    log_entry = json.loads(msg.value)
    es.index(index='logs', doc_type='log_entry', body=log_entry)

# Data Analysis
# Use Apache Spark to analyze log data from Elasticsearch
spark = SparkSession.builder.appName("LogAnalysis").getOrCreate()
df = spark.read.format("org.elasticsearch.spark.sql").option("es.nodes", "elasticsearch").option("es.port", "9200").load("logs/log_entry")

# Anomaly Detection
# Train a Random Forest model for anomaly detection
indexed = StringIndexer(inputCol="level", outputCol="levelIndex").fit(df).transform(df)
encoded = OneHotEncoder(inputCols=["levelIndex"], outputCols=["levelVec"]).transform(indexed)
rf = RandomForestClassifier().fit(encoded)

# Predict anomalies on new log data
new_logs = [
    {'timestamp': time.time(), 'level': 'INFO', 'message': 'This is a normal log message'},
    {'timestamp': time.time(), 'level': 'ERROR', 'message': 'This is an anomalous log message'}
]
predictions = rf.transform(encoded.createDataFrame(new_logs))
predictions.show()

# Monitoring and Alerting
# Monitor Kafka consumer lag and send alerts if lag exceeds a threshold
consumer_lag = consumer.metrics()['lag']
if consumer_lag > 1000:
    # Send alert
    print("High consumer lag detected!")