# AWS S3 Data Exporter for Prometheus

This Python script fetches AWS billing data from an S3 bucket, processes the data, and then exposes relevant billing metrics via Prometheus.

## 🚀 Features

- S3 File Download: Downloads the most recent file from an S3 bucket.
- CSV Extraction: Extracts metrics from a CSV file that is zipped.
- Prometheus Metrics Exposure: Exposes metrics such as usage_quantity, blended_cost, and unblended_cost per AWS product to Prometheus.

## 📋 Prerequisites

Python: Version 3.11.4
Python Libraries: Ensure the following libraries are installed:
- boto3 (Version 1.24.28)
- pandas (Version 2.1.0)
- prometheus_client (Version 0.17.1)
- python-dotenv (Version 1.0.0)

## 🔧 Setup

1. Clone the Repository:

```bash
git clone git@github.com:Marta-Barea/prometheus-aws-billing-exporter 
```

2. Install Required Libraries:

A requirements.txt is available. You can easily install the required libraries using pip:

```bash
pip install -r requirements.txt
```

3. Environment Configuration:

Set up your AWS credentials and the desired S3 bucket name in a .env file.

```env
AWS_ACCESS_KEY=YOUR_AWS_ACCESS_KEY
AWS_SECRET_KEY=YOUR_AWS_SECRET_KEY
S3_BUCKET_NAME=YOUR_S3_BUCKET_NAME
```

## 🚀 Running the Script

To run the script:

```bash
python3 main.py
```

This will launch an HTTP server on port 8000 for Prometheus to scrape.

## 📊 Metrics

- usage_quantity: Represents the usage amount of a specific AWS product.
- blended_cost: Represents the combined cost for a specific AWS product.
- unblended_cost: Represents the individual, uncombined cost for a specific AWS product.

Each metric is labeled by its respective product name.

## 🔒 Note

Ensure the AWS IAM user associated with the provided credentials has the required permissions to list and fetch objects from the specified S3 bucket.