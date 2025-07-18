import fitz  # PyMuPDF uses 'fitz' as the import name
import json
from collections import Counter
import re

class PDFOutlineExtractor:
    """
    Extracts a structured outline (Title, H1, H2, H3) from a PDF file
    using a dynamic, style-based heuristic approach.
    """

    def __init__(self, pdf_path):
        self.doc = fitz.open(pdf_path)
        self.styles = self._profile_document_styles()
        self.body_style = self.styles['body_style']
        self.heading_styles = self.styles['heading_styles']

    def _profile_document_styles(self):
        """
        Pass 1: Profile the document to find the most common font style (body text)
        and identify potential heading styles.
        """
        spans = []
        for page in self.doc:
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if block["type"] == 0:  # Text block
                    for line in block["lines"]:
                        for span in line["spans"]:
                            spans.append({
                                "size": round(span["size"]),
                                "font": span["font"],
                                "flags": span["flags"],
                                "text": span["text"].strip()
                            })

        # Filter out empty spans
        spans = [s for s in spans if s['text']]
        if not spans:
            return {'body_style': None, 'heading_styles': {}}

        # Most common style (assumed body text)
        style_counts = Counter((s['size'], s['font']) for s in spans)
        (body_size, body_font), _ = style_counts.most_common(1)[0]
        body_style = {'size': body_size, 'font': body_font}

        # Identify heading sizes (larger than body text)
        potential_heading_sizes = sorted(
            {s['size'] for s in spans if s['size'] > body_size},
            reverse=True
        )

        # Map top 3 sizes to H1, H2, H3
        heading_styles = {}
        if len(potential_heading_sizes) > 0:
            heading_styles['H1'] = potential_heading_sizes[0]
        if len(potential_heading_sizes) > 1:
            heading_styles['H2'] = potential_heading_sizes[1]
        if len(potential_heading_sizes) > 2:
            heading_styles['H3'] = potential_heading_sizes[2]

        return {'body_style': body_style, 'heading_styles': heading_styles}

    def _is_heading(self, span):
        """Check if a span is likely a heading based on its style."""
        size = round(span['size'])
        is_bold = span['flags'] & 16  # Font flag for bold

        if size > self.body_style['size']:
            return True
        if size == self.body_style['size'] and is_bold:
            return True
        return False

    def _get_heading_level(self, size):
        """Get the heading level (H1, H2, H3) for a given font size."""
        for level, h_size in self.heading_styles.items():
            if size == h_size:
                return level
        return None

    def extract(self):
        """
        Pass 2: Extract title and outline based on the profiled styles.
        """
        title = ""
        outline = []

        # Heuristic for Title: Largest font size on the first page
        first_page_spans = []
        if len(self.doc) > 0:
            first_page = self.doc[0]
            blocks = first_page.get_text("dict")["blocks"]
            for block in blocks:
                if block["type"] == 0:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            if span["text"].strip():
                                first_page_spans.append(span)

        if first_page_spans:
            title_span = max(first_page_spans, key=lambda s: s['size'])
            title = title_span['text'].strip()

        # Extract headings from all pages
        for page_num, page in enumerate(self.doc, 1):
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                if block['type'] == 0:  # Text block
                    block_lines = block['lines']
                    for line in block_lines:
                        if not line['spans']:
                            continue
                        block_text = " ".join([
                            span['text'].strip()
                            for span in line['spans'] if span['text'].strip()
                        ])

                        if not block_text or len(block_text) < 3 or len(block_text) > 150:
                            continue

                        first_span = line['spans'][0]
                        span_size = round(first_span['size'])

                        if self._is_heading(first_span):
                            level = self._get_heading_level(span_size)
                            if level:
                                outline.append({
                                    "level": level,
                                    "text": block_text,
                                    "page": page_num
                                })

        # Post-processing: Merge consecutive lines of the same heading style
        if not outline:
            return {"title": title, "outline": []}

        merged_outline = [outline[0]]
        for i in range(1, len(outline)):
            prev = merged_outline[-1]
            curr = outline[i]
            if curr['level'] == prev['level'] and curr['page'] == prev['page']:
                if isinstance(merged_outline[-1]['text'], list):
                    merged_outline[-1]['text'].append(curr['text'])
                else:
                    merged_outline[-1]['text'] = [merged_outline[-1]['text'], curr['text']]
            else:
                merged_outline.append(curr)

        # Ensure all 'text' fields are lists
        for entry in merged_outline:
            if not isinstance(entry['text'], list):
                entry['text'] = [entry['text']]

        return {"title": title, "outline": merged_outline}
