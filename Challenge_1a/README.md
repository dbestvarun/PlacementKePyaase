# Challenge 1a: PDF Outline Extraction

## Project Structure

```
Challenge_1a/
├── sample_dataset/
│   ├── outputs/         # JSON files provided as outputs (one per input PDF)
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
   Challenge_1a/sample_dataset/outputs/<input_filename>.json
   ```
   For example, `file1.pdf` will produce `file1.json` in the outputs folder. All PDFs in the input folder will be processed and a separate JSON file will be created for each.

## Docker

To build and run with Docker:
```bash
docker build --platform linux/amd64 -t challenge1a .
```

- For Command Prompt (cmd.exe):
  ```cmd
  docker run --rm -v "%cd%\sample_dataset\pdfs":/app/sample_dataset/pdfs:ro -v "%cd%\sample_dataset\outputs":/app/sample_dataset/outputs --network none challenge1a
  ```
- For PowerShell:
  ```powershell
  docker run --rm -v "${PWD}/sample_dataset/pdfs:/app/sample_dataset/pdfs:ro" -v "${PWD}/sample_dataset/outputs:/app/sample_dataset/outputs" --network none challenge1a
  ```

- The output will always be written to `sample_dataset/outputs/<input_filename>.json` for each input PDF.
- The output schema is defined in `sample_dataset/schema/output_schema.json`. 