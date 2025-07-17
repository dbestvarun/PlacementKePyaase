# Project Title

A brief description of the project.

## Project Structure

```
/
├── Dockerfile
├── README.md
├── requirements.txt
└── src/
    ├── main.py
    └── extractor.py
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the project:
   ```bash
   python src/main.py
   ```

## Docker

To build and run with Docker:
```bash
docker build -t my-python-app .
docker run --rm my-python-app
``` 