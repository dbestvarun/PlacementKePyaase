# Step 1: Specify the base image with the required platform
# Using python:3.11-slim for a small and secure base.
# The --platform flag ensures compatibility with the amd64 evaluation environment.
FROM --platform=linux/amd64 python:3.11-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the requirements file and install dependencies
# This ensures all dependencies are bundled within the container for offline execution.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Step 4: Copy the application source code into the container
COPY src/ ./src/

# Step 5: Define the command to run the application
# This will be executed when the container starts, processing files from /app/input.
CMD ["python", "src/main.py"]
