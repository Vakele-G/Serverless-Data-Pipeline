WTC-PCWZJ6UM
# Serverless-RAG-system

**What is this project?**
This is a Retrieval-Augmented Generation (RAG) pipeline deployed on AWS using serverless infrastructure.
You upload a PDF document to the system and ask it questions based on that document. It will read through provided documents and generate a clear, accurate answer based strictly on the text.

**Technical Architecture**

The Stack

    Storage (Amazon S3): For storing the pre-calculated vector index files in an S3 bucket.

    Compute (AWS Lambda): Query retrieval and LLM generation are handled on-demand via a Lambda Function URL, allowing the application to scale to zero when idle.

    Containerization (Amazon ECR): Because machine learning libraries exceed Lambda's standard deployment limits, the environment (including llama-index and HuggingFace models) is packaged via Docker and stored in ECR.

    Language Models:

        Embeddings: BAAI/bge-small-en-v1.5 for semantic chunking and high-fidelity search context.

        Generation: Meta's Llama 3.3 model (accessed via OpenRouter) to deliver precise, context-aware technical answers.