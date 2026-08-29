import os
import json
import boto3
from llama_index.core import StorageContext, load_index_from_storage, Settings
from llama_index.llms.openrouter import OpenRouter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

s3 = boto3.client("s3")
BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
INDEX_PATH = "/tmp/storage"

# Global initialization (Cold Start cache)
def initialize_engine():
    os.makedirs(INDEX_PATH, exist_ok=True)
    
    # Download index files from S3 to Lambda's /tmp directory
    objects = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix="storage/")
    for obj in objects.get("Contents", []):
        filename = obj["Key"].split("/")[-1]
        if filename:
            s3.download_file(BUCKET_NAME, obj["Key"], os.path.join(INDEX_PATH, filename))

    # Configure models
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    Settings.llm = OpenRouter(
        api_key=os.environ.get("OPENROUTER_API_KEY"),
        model="meta-llama/llama-3.3-70b-instruct:free",
        max_tokens=512,
        temperature=0.1
    )

    storage_context = StorageContext.from_defaults(persist_dir=INDEX_PATH)
    index = load_index_from_storage(storage_context)
    return index.as_query_engine(similarity_top_k=4)

query_engine = initialize_engine()

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        question = body.get("question", "")
        
        if not question:
            return {"statusCode": 400, "body": json.dumps({"error": "Missing 'question' in request body"})}

        response = query_engine.query(question)
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"question": question, "answer": str(response)})
        }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}