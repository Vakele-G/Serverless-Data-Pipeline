import boto3
import urllib.parse
from clean_data import clean_csv_string

# boto3 is the official AWS SDK for Python. It allows the code to S3

s3_client = boto3.client("s3")

def lambda_handler(event, context):
    """
    This is the front door. AWS automatically passes the 'event' dictionary
    which contains the details about the file that was just uploaded.
    """

    # Extract the bucket name and file name from the event 
    source_bucket = event["Records"][0]["s3"]["bucket"]["name"]

    # Use urllib to safely decode the name and file name from the event
    file_key = urllib.parse.unquote_plus(event["Records"][0]["s3"]["object"]["key"], encoding="utf-8")

    print(f"Triggered by file: {file_key} in bucket: {source_bucket}")

    try:
        # Download raw CSV file from S3 into Lambda's memory
        response = s3_client.get_object(Bucket=source_bucket, Key=file_key)
        raw_csv_text = response["Body"].read().decode("utf-8")

        # Pass the data into the csv cleaner function
        clean_csv_text = clean_csv_string(raw_csv_text)

        # Define where the cleaned data is going
        destination_bucket = "vakele-processed-data-output-2026"
        clean_file_key =  f"clean_{file_key}"

        # Upload cleaned data to output bucket
        s3_client.put_object(
            Bucket=destination_bucket,
            Key=clean_file_key,
            Body=clean_csv_text.encode("utf-8")
        )

        print(f"Success! Cleaned file saved to {destination_bucket}/{clean_file_key}")

        return {"statusCode": 200,
                "body": "File processed successfully"
                }
    except Exception as e:
        print(f"Error processing file {file_key}: {str(e)}")
        raise e