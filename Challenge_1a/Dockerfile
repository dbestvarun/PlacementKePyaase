FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy code and dataset structure
COPY process_pdfs.py ./
COPY extractor.py ./
COPY sample_dataset/ ./sample_dataset/

# Set the working directory to /app
WORKDIR /app

# Default command to run the processing script
CMD ["python", "process_pdfs.py"] 