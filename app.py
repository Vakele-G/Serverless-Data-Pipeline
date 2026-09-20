import os
import json
import boto3


os.environ["HOME"] = "/tmp"    # Force all generic home-directory caching to the writable /tmp folder

s3 = boto3.client("s3")
BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")
INDEX_PATH = "/tmp/storage"

query_engine = None

# Global initialization (Cold Start cache)
def initialize_engine():
    from llama_index.core import StorageContext, load_index_from_storage, Settings
    from llama_index.llms.openrouter import OpenRouter
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    from llama_index.llms.groq import Groq

    print("Loading models...")

    os.makedirs(INDEX_PATH, exist_ok=True)
    
    # Download index files from S3 to Lambda's /tmp directory
    objects = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix="storage/")
    for obj in objects.get("Contents", []):
        filename = obj["Key"].split("/")[-1]
        if filename:
            s3.download_file(BUCKET_NAME, obj["Key"], os.path.join(INDEX_PATH, filename))

    # Configure models
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5", cache_folder=os.environ.get("HF_HOME"))

    # selected_model = os.environ.get("LLM_MODEL", "openrouter/free")
    # print(f"Initializing OpenRouter with model: {selected_model}")
    # Settings.llm = OpenRouter(model=selected_model)

    Settings.llm = Groq(
        model="openai/gpt-oss-120b", 
        api_key=os.environ.get("GROQ_API_KEY")
    )


    storage_context = StorageContext.from_defaults(persist_dir=INDEX_PATH)
    index = load_index_from_storage(storage_context)

    return index.as_query_engine(similarity_top_k=4)


def lambda_handler(event, context):
    global query_engine

    expected_api_key = os.environ.get("API_SECRET_KEY")
    headers = event.get("headers", {})

    provided_api_key = headers.get("x-api-key")

    if not expected_api_key or provided_api_key != expected_api_key:
        return {
            "statusCode": 401,
            "body": json.dumps({"error": "Unauthorized: Invalid or missing API key"})
        }

    try:
        if query_engine is None:
            print("Cold start: Initializing RAG engine...")
            query_engine = initialize_engine()
            print("Engine initialized successfully.")

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