FROM public.ecr.aws/lambda/python:3.12

# Update core build utilities, upgrade pip/setuptools
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy requirements directly into the Lambda task root
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install packages forcing pre-compiled binaries (prevents compiling numpy from source)
RUN pip install --no-cache-dir --only-binary=:numpy: -r ${LAMBDA_TASK_ROOT}/requirements.txt

# Set a specific cache directory so the model stays packed inside the image
ENV HF_HOME=${LAMBDA_TASK_ROOT}/.cache/huggingface

# Download and bake HuggingFace model into the container image
RUN python -c "from llama_index.embeddings.huggingface import HuggingFaceEmbedding; HuggingFaceEmbedding(model_name='BAAI/bge-small-en-v1.5', cache_folder='${HF_HOME}')"

COPY app.py ${LAMBDA_TASK_ROOT}

CMD ["app.lambda_handler"]