import os
import boto3
from botocore.exceptions import NoCredentialsError

"""
Function to upload vector embeddings from /storage to S3 bucket
Alternatively you can drag and drop the files directly into the storage folder in your bucket via the
AWS Management Console
"""

BUCKET_NAME = "rag-knowledge-base-entry-2026"
STORAGE_DIR = "./storage"
S3_PREFIX = "storage/"  # The folder inside the S3 bucket

def upload_directory_to_s3():
    # Initialize the S3 client using your local AWS CLI credentials
    s3_client = boto3.client("s3")
    
    if not os.path.exists(STORAGE_DIR):
        print(f"❌ Error: The directory '{STORAGE_DIR}' does not exist.")
        print("Run your indexing script first (build_index.py) to generate the vector embeddings.")
        return

    print(f"🚀 Starting upload to s3://{BUCKET_NAME}/{S3_PREFIX}...")

    # Walk through the local storage directory
    for root, dirs, files in os.walk(STORAGE_DIR):
        for file in files:
            local_path = os.path.join(root, file)
            
            # Construct the destination path in S3
            # Example: ./storage/docstore.json -> storage/docstore.json
            relative_path = os.path.relpath(local_path, STORAGE_DIR)
            s3_key = os.path.join(S3_PREFIX, relative_path).replace("\\", "/")

            try:
                print(f"Uploading {file}...")
                s3_client.upload_file(local_path, BUCKET_NAME, s3_key)
            except FileNotFoundError:
                print(f"❌ The file {local_path} was not found.")
            except NoCredentialsError:
                print("❌ AWS credentials not available. Run 'aws configure' in your terminal.")
                return
            except Exception as e:
                print(f"❌ Failed to upload {file}: {e}")

    print("✅ All files uploaded successfully!")

if __name__ == "__main__":
    upload_directory_to_s3()