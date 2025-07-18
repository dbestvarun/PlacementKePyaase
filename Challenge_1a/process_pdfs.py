import os
import json
from extractor import PDFOutlineExtractor

def process_pdfs():
    """
    Processes all PDF files in the pdfs directory and writes JSON output to outputs/output.json.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Absolute path to Challenge_1a/
    input_dir = os.path.join(base_dir, "sample_dataset", "pdfs")
    output_dir = os.path.join(base_dir, "sample_dataset", "outputs")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_dir, filename)
            json_path = os.path.join(output_dir, 'output.json')  # Always output to output.json

            print(f"Processing {pdf_path}...")
            try:
                extractor = PDFOutlineExtractor(pdf_path)
                result = extractor.extract()

                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)

                print(f"\u2705 Successfully generated {json_path}")

            except Exception as e:
                print(f"\u274c Error processing {pdf_path}: {e}")
                error_output = {"title": "", "outline": [], "error": str(e)}
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(error_output, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    process_pdfs()
