import boto3
import urllib.parse
import json
from data_cleaner import clean_csv_string

s3_client = boto3.client("s3")

def lambda_handler(event, context):
    # Extract bucket and file key from the S3 trigger event
    source_bucket = event["Records"][0]["s3"]["bucket"]["name"]
    file_key = urllib.parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"], encoding="utf-8")

    print(f"Triggered by file: {file_key} in bucket: {source_bucket}")

    try:
        # 1. Download the raw file from S3
        response = s3_client.get_object(Bucket=source_bucket, Key=file_key)
        raw_file_text = response["Body"].read().decode("utf-8")

        # 2. NEW STEP: Parse the raw text as JSON and extract the actual CSV data
        payload = json.loads(raw_file_text)
        actual_csv_text = payload.get("raw_csv", "")

        # 3. Pass the extracted data into your original csv cleaner function
        clean_csv_text = clean_csv_string(actual_csv_text)

        # 4. Define destination settings
        destination_bucket = "vakele-processed-data-output-2026"
        clean_file_key = f"clean_{file_key}"

        # 5. Upload the genuinely cleaned CSV data
        s3_client.put_object(
            Bucket=destination_bucket,
            Key=clean_file_key,
            Body=clean_csv_text.encode("utf-8")
        )

        print(f"Success! Cleaned file saved to {destination_bucket}/{clean_file_key}")

        return {
            "statusCode": 200,
            "body": json.dumps("File processed successfully")
        }
    except Exception as e:
        print(f"Error processing file {file_key}: {str(e)}")
        raise e