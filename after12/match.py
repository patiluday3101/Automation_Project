# import os
# import re
# import fitz  # PyMuPDF
# import pandas as pd

# def extract_consumer_number_from_pdf(pdf_path):
#     try:
#         doc = fitz.open(pdf_path)
#         for page in doc:
#             text = page.get_text()
            
#             # Common regex patterns for consumer numbers (adjust as needed)
#             patterns = [
#                 re.compile(r'Consumer No[:\s]+(\d+)'),  # English pattern
#                 re.compile(r'(?:ग्राहक क्रमांक|�ाहक �मांक)[:\s]+(\d+)'),  # Marathi pattern (Handles misinterpretation)
#                 re.compile(r'\b(\d{10})\b')  # Generic 10-digit number pattern
#             ]
            
#             for pattern in patterns:
#                 match = re.search(pattern, text)
#                 if match:
#                     return match.group(1)
#     except Exception as e:
#         print(f"Error reading {pdf_path}: {e}")
#     return None

# def process_pdfs(folder_path, output_excel):
#     results = []
#     for file in os.listdir(folder_path):
#         if file.endswith(".pdf"):
#             file_path = os.path.join(folder_path, file)
#             filename_match = re.match(r'(\d{10,12})', file)
#             if filename_match:
#                 filename_consumer_number = filename_match.group(1)
#                 pdf_consumer_number = extract_consumer_number_from_pdf(file_path)
#                 match_status = "Yes" if pdf_consumer_number == filename_consumer_number else "No"
#                 results.append([file, match_status])
#             else:
#                 results.append([file, "Invalid Filename"])
    
#     df = pd.DataFrame(results, columns=["File Name", "Match Status"])
#     df.to_excel(output_excel, index=False)
#     print(f"Results saved to {output_excel}")

# # Set folder path and output Excel file
# folder_path = r"C:\Users\Computer Point\OneDrive\Desktop\E-Bill Downloader\Bills"
# output_excel = "match.xlsx"
# process_pdfs(folder_path, output_excel)
import os
import re
import fitz  # PyMuPDF
import pandas as pd
import pytesseract
from pdf2image import convert_from_path

# Set path to Tesseract OCR (Windows users)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_ocr(pdf_path):
    text = ""
    try:
        images = convert_from_path(pdf_path, dpi=300)  # Higher DPI for better OCR accuracy
        for img in images:
            text += pytesseract.image_to_string(img, lang="eng+mar", config="--oem 3 --psm 6") + " "
    except Exception as e:
        print(f"OCR failed for {pdf_path}: {e}")
    return text.strip()

def extract_consumer_number_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = " ".join(page.get_text() for page in doc)

        # If no text is extracted, use OCR
        if not text.strip():
            print(f"No text found in {pdf_path}, using OCR...")
            text = extract_text_ocr(pdf_path)

        # Common regex patterns for consumer numbers
        patterns = [
            re.compile(r'Consumer No[:\s]+(\d+)'),  # English pattern
            re.compile(r'(?:ग्राहक क्रमांक|�ाहक �मांक)[:\s]+(\d+)'),  # Marathi pattern (Handles misinterpretation)
            re.compile(r'\bN\d{10}\b')

        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return None

def process_pdfs(folder_path, output_excel):
    results = []
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            file_path = os.path.join(folder_path, file)
            filename_match = re.match(r'(\d{10,12})', file)
            if filename_match:
                filename_consumer_number = filename_match.group(1)
                pdf_consumer_number = extract_consumer_number_from_pdf(file_path)
                match_status = "Yes" if pdf_consumer_number == filename_consumer_number else "No"
                results.append([file, pdf_consumer_number or "Not Found", match_status])
            else:
                results.append([file, "Invalid Filename", "N/A"])
    
    df = pd.DataFrame(results, columns=["File Name", "Extracted Consumer No", "Match Status"])
    df.to_excel(output_excel, index=False)
    print(f"Results saved to {output_excel}")

# Set folder path and output Excel file
folder_path = r"C:\Users\Computer Point\OneDrive\Desktop\E-Bill Downloader\Bills"
output_excel = "match.xlsx"
process_pdfs(folder_path, output_excel)
