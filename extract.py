import os
import sqlite3
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
        text = "error"
    return text

def initialize_database(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    # Create FTS virtual table for full-text search
    c.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS pdfs
        USING fts5(path, text)
    ''')
    conn.commit()
    return conn

def process_pdfs(pdf_directory, db_path):
    conn = initialize_database(db_path)
    c = conn.cursor()

    for root, _, files in os.walk(pdf_directory):
        for file in files:
            if file.endswith('.pdf'):
                pdf_path = os.path.join(root, file)
                
                # Check if the PDF has already been processed
                c.execute('SELECT 1 FROM pdfs WHERE path = ?', (pdf_path,))
                if c.fetchone():
                   console.print(f"Skipping already processed file: {pdf_path}", style="blue")
                   continue
                
                text = extract_text_from_pdf(pdf_path)
                if not text:
                    console.print(f"No text found in {pdf_path}", style="yellow")
                    import ocr
                    text = "image " + ocr.extract_text_from_pdf(pdf_path)

                c.execute('INSERT INTO pdfs (path, text) VALUES (?, ?)', (pdf_path, text))
                conn.commit()
                console.print(f"Processed {pdf_path}")

    conn.close()

if __name__ == "__main__":
    import config
    db_path = config.certificate_db_file
    process_pdfs(config.certificate_folder, db_path)
