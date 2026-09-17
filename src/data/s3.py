import os
from io import BytesIO

import boto3
import pandas as pd
from dotenv import load_dotenv


load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")


def get_s3_client():
    """Create and return an authenticated Amazon S3 client."""
    return boto3.client("s3", region_name=AWS_REGION)


def list_raw_files():
    """Return the objects stored in the raw S3 data layer."""
    s3 = get_s3_client()

    response = s3.list_objects_v2(
        Bucket=BUCKET_NAME,
        Prefix="raw/"
    )

    return [
        obj["Key"]
        for obj in response.get("Contents", [])
    ]


def load_csv_from_s3(key):
    """Load a CSV file from S3 into a pandas DataFrame."""
    s3 = get_s3_client()

    response = s3.get_object(
        Bucket=BUCKET_NAME,
        Key=key
    )

    return pd.read_csv(
        BytesIO(response["Body"].read())
    )


if __name__ == "__main__":
    df = load_csv_from_s3("raw/cell2celltrain.csv")

    print(f"Rows: {df.shape[0]:,}")
    print(f"Columns: {df.shape[1]}")
    print("\nFirst five rows:")
    print(df.head())