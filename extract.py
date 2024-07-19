import os
import json
import fitz  # PyMuPDF

# color printing
from rich.console import Console
console = Console()

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        pdf_document = fitz.open(pdf_path)
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
    except Exception as e:
        console.print(f"Error processing {pdf_path}: {e}", style="red")
    return text

def process_pdfs(pdf_directory, output_file):
    pdf_texts = {}
    for root, _, files in os.walk(pdf_directory):
        for file in files:
            if file.endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                text = extract_text_from_pdf(pdf_path)
                if text:
                    pdf_texts[pdf_path] = text
                    console.print(f"Processed {pdf_path}")
                else:
                    console.print(f"No text found in {pdf_path}", style="yellow")
                

    with open(output_file, 'w') as f:
        json.dump(pdf_texts, f, indent=4)

if __name__ == "__main__":
    pdf_directory = "certificates"
    output_file = "certificate_texts.json"
    process_pdfs(pdf_directory, output_file)
