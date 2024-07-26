import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io

def extract_text_from_pdf(pdf_path):

    try:
        pdf_document = fitz.open(pdf_path)

        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            image_list = page.get_images(full=True)
    
            full_text = ""
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]

                image = Image.open(io.BytesIO(image_bytes))

                text = pytesseract.image_to_string(image, lang='eng+swe+deu+fra')
                full_text += text
        
                print(f"Page {page_num + 1}, Image {img_index + 1}:")
                print(text)
                print("\n" + "="*80 + "\n")
        return full_text
    except:
        print(f"failed to scan {pdf_path}")
        return "fail"

if __name__ == "__main__":
    pdf = input("PDF PATH: ")
    extract_text_from_pdf(pdf)


