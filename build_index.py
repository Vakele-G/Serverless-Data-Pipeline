from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Load the embedding model
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# Read the PDF
documents = SimpleDirectoryReader(input_files=["data/N5-Industrial-Electronics.pdf"]).load_data()

# Build the index and save to the local storage folder
index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)
index.storage_context.persist(persist_dir="./storage")