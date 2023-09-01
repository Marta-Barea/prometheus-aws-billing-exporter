import os
import boto3
import pandas as pd
import tempfile
import zipfile
from prometheus_client import Gauge, start_http_server
from dotenv import load_dotenv
import time

load_dotenv()

# Load AWS credentials from environment variables
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')

# Define Prometheus metrics
gauge_usage_quantity = Gauge('usage_quantity', 'Usage Quantity', ['product_name'])
gauge_blended_cost = Gauge('blended_cost', 'Blended Cost', ['product_name'])
gauge_unblended_cost = Gauge('unblended_cost', 'UnBlended Cost', ['product_name'])


# Set up boto3 S3 client
s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

def download_latest_file_from_s3(bucket_name):
    # List objects in bucket
    objects = s3_client.list_objects_v2(Bucket=bucket_name)
    
    # Find the latest file based on LastModified attribute
    latest_file = max(objects.get('Contents', []), key=lambda x: x['LastModified'])
    
    # Download the file to a temporary location
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    s3_client.download_file(bucket_name, latest_file['Key'], temp_file.name)

    return temp_file.name

def filter_and_sum(df):
    # Filter desired columns
    desired_columns = ["ProductName", "UsageQuantity", "BlendedRate", "BlendedCost", "UnBlendedRate", "UnBlendedCost"]
    df = df[desired_columns]
    
    # Group by 'ProductName' and sum the other columns
    df_summed = df.groupby('ProductName').sum().reset_index()
    return df_summed

def expose_metrics_to_prometheus(df):
    for _, row in df.iterrows():
        product_name = row["ProductName"]
        gauge_usage_quantity.labels(product_name=product_name).set(row["UsageQuantity"])
        gauge_blended_cost.labels(product_name=product_name).set(row["BlendedCost"])
        gauge_unblended_cost.labels(product_name=product_name).set(row["UnBlendedCost"])

def main():
    # Start the HTTP server to expose metrics
    start_http_server(8000)

    # Load bucket_name from environment variables
    while True:
        print("Updating metrics...")
        bucket_name = os.environ.get('S3_BUCKET_NAME')
        temp_zip_path = download_latest_file_from_s3(bucket_name)
        
        # Unzip the file to get the CSV
        with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
            # Assuming there's only one file in the ZIP and you want to extract that
            extracted_file_name = zip_ref.namelist()[0]
            with zip_ref.open(extracted_file_name) as csv_file:
                df = pd.read_csv(csv_file, encoding="ISO-8859-1")
        
        if df is not None:
            result_df = filter_and_sum(df)
            expose_metrics_to_prometheus(result_df)
        
        time.sleep(60)

if __name__ == "__main__":
    main()
