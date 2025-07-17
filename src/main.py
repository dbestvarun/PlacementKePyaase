import os
import json
from extractor import PDFOutlineExtractor

def process_pdfs():
    """
    Processes all PDF files in the input directory and writes JSON output.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Absolute path to /src/
    input_dir = os.path.join(base_dir, "input")
    output_dir = os.path.join(base_dir, "output")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_dir, filename)
            json_filename = os.path.splitext(filename)[0] + '.json'
            json_path = os.path.join(output_dir, json_filename)

            print(f"Processing {pdf_path}...")
            try:
                extractor = PDFOutlineExtractor(pdf_path)
                result = extractor.extract()

                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)

                print(f"✅ Successfully generated {json_path}")

            except Exception as e:
                print(f"❌ Error processing {pdf_path}: {e}")
                error_output = {"title": "", "outline": [], "error": str(e)}
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(error_output, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    process_pdfs()
