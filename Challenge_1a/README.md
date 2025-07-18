# Challenge 1a: PDF Outline Extraction

## Project Structure

```
Challenge_1a/
├── sample_dataset/
│   ├── outputs/         # JSON files provided as outputs.
│   ├── pdfs/            # Input PDF files
│   └── schema/          # Output schema definition
│       └── output_schema.json
├── Dockerfile           # Docker container configuration
├── process_pdfs.py      # Sample processing script
└── README.md            # This file
```

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Place your input PDFs in:
   ```
   Challenge_1a/sample_dataset/pdfs/
   ```
3. Run the project:
   ```bash
   python process_pdfs.py
   ```
   The output will be written to:
   ```
   Challenge_1a/sample_dataset/outputs/output.json
   ```

## Docker

To build and run with Docker:
```bash
docker build --platform linux/amd64 -t <reponame.someidentifier> .
docker run --rm -v $(pwd)/input:/app/input:ro -v $(pwd)/output/repoidentifier/:/app/output --network none <reponame.someidentifier>
```

- The output will always be written to `sample_dataset/outputs/output.json`.
- In the output JSON, the `text` field for each tag is a list of strings, making it easier to distinguish multiple extracted texts.
- The output schema is defined in `sample_dataset/schema/output_schema.json`. 