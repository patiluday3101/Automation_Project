# import os
# import pandas as pd
# import PyPDF2
# import re
# from pdf2image import convert_from_path
# import pytesseract

# # Folder path containing PDFs
# folder_path = r"C:\Users\Computer Point\OneDrive\Desktop\E-Bill Downloader\Bills"
# output_excel = "output.xlsx"

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# consumer_number_patterns = [
#     re.compile(r'Consumer No[:\s]+(\d+)'),  
#     re.compile(r'(?:ग्राहक क्रमांक|�ाहक �मांक)[:\s]+(\d+)'),  
#     re.compile(r'\b\d{10}\b')
#     ]


# def extract_text_pypdf(pdf_path):
#     """Extract text from PDF using PyPDF2 (for text-based PDFs)."""
#     text = ""
#     try:
#         with open(pdf_path, "rb") as file:
#             reader = PyPDF2.PdfReader(file)
#             for page in reader.pages:
#                 if page.extract_text():
#                     text += page.extract_text() + " "
#     except Exception as e:
#         print(f"PyPDF2 failed for {pdf_path}: {e}")
#     return text.strip()

# def extract_text_ocr(pdf_path):
#     """Extract text from scanned PDF using OCR."""
#     text = ""
#     try:
#         images = convert_from_path(pdf_path)  # Convert PDF to images
#         for img in images:
#             text += pytesseract.image_to_string(img, lang="eng+mar") + " "  # English + Marathi
#     except Exception as e:
#         print(f"OCR failed for {pdf_path}: {e}")
#     return text.strip()

# def extract_consumer_number(pdf_path):
#     """Extract consumer number using both PyPDF2 and OCR."""
#     text = extract_text_pypdf(pdf_path)
#     if not text:  # If PyPDF2 fails, use OCR
#         text = extract_text_ocr(pdf_path)

#     for pattern in consumer_number_patterns:
#         match = pattern.search(text)
#         if match:
#             return match.group(0)  
#     return "Not Found"

# data = []

# for filename in os.listdir(folder_path):
#     if filename.endswith(".pdf"):
#         pdf_path = os.path.join(folder_path, filename)
#         consumer_number = extract_consumer_number(pdf_path)
#         data.append([filename, consumer_number])

# # Save data to Excel
# df = pd.DataFrame(data, columns=["File Name", "Consumer Number"])
# df.to_excel(output_excel, index=False)

# print(f"Extraction completed! Data saved to {output_excel}")
# import os
# import pandas as pd
# import PyPDF2
# import re
# from pdf2image import convert_from_path
# import pytesseract

# # Folder path containing PDFs
# folder_path = r"C:\Users\Computer Point\OneDrive\Desktop\E-Bill Downloader\Bills"
# output_excel = "output.xlsx"

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# consumer_number_patterns = [
#     re.compile(r'Consumer No[:\s]+(\d+)'),  # English pattern (has a capture group)
#     re.compile(r'(?:ग्राहक क्रमांक|�ाहक �मांक)[:\s]+(\d+)'),  # Marathi pattern (has a capture group)
#     re.compile(r'\bN\d{10}\b'),  # IVRS number pattern (no capture group)
#     re.compile(r"fcy la\[;k (\d+)"),
#     re.compile(r"Account No\.: (\d+)"),
#     re.compile(r"Unique Service Number\s*(\d+)"),
#     re.compile(r"IVRS\s*[:\-]?\s*([A-Z0-9]+)"),
#     re.compile(r"Consumer Number\s*:?\s*(\d+)")
# ]

# def extract_text_pypdf(pdf_path):
#     """Extract text from PDF using PyPDF2 (for text-based PDFs)."""
#     text = ""
#     try:
#         with open(pdf_path, "rb") as file:
#             reader = PyPDF2.PdfReader(file)
#             for page in reader.pages:
#                 extracted_text = page.extract_text()
#                 if extracted_text:
#                     text += extracted_text + " "
#     except Exception as e:
#         print(f"PyPDF2 failed for {pdf_path}: {e}")
#     return text.strip()

# def extract_text_ocr(pdf_path):
#     """Extract text from scanned PDF using OCR."""
#     text = ""
#     try:
#         images = convert_from_path(pdf_path, dpi=300)  # Higher DPI for better OCR accuracy
#         for img in images:
#             text += pytesseract.image_to_string(img, lang="eng+mar", config="--oem 3 --psm 6") + " "
#     except Exception as e:
#         print(f"OCR failed for {pdf_path}: {e}")
#     return text.strip()

# def extract_consumer_number(pdf_path):
#     """Extract consumer number or IVRS number from PDF."""
#     text = extract_text_pypdf(pdf_path)
#     if not text:  
#         text = extract_text_ocr(pdf_path)

#     for pattern in consumer_number_patterns:
#         match = pattern.search(text)
#         if match:
#             return match.group(1) if pattern.groups else match.group(0)  # Handle capture & full matches
#     return "Not Found"

# data = []

# for filename in os.listdir(folder_path):
#     if filename.endswith(".pdf"):
#         pdf_path = os.path.join(folder_path, filename)
#         consumer_number = extract_consumer_number(pdf_path)
#         data.append([filename, consumer_number])

# # Save data to Excel
# df = pd.DataFrame(data, columns=["File Name", "Consumer Number"])
# df.to_excel(output_excel, index=False)

# print(f"Extraction completed! Data saved to {output_excel}")
# import os
# import pandas as pd
# import PyPDF2
# import re
# from pdf2image import convert_from_path
# import pytesseract

# # Folder path containing PDFs
# folder_path = r"C:\Users\Computer Point\OneDrive\Desktop\E-Bill Downloader\Bills"
# output_excel = "output.xlsx"

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# consumer_number_patterns = [
#     re.compile(r'Consumer No[:\s]+(\d+)'),  
#     re.compile(r'(?:ग्राहक क्रमांक| ाहक  मांक)[:\s]+(\d+)'),  
#     re.compile(r'\b\d{10}\b')
#     ]


# def extract_text_pypdf(pdf_path):
#     """Extract text from PDF using PyPDF2 (for text-based PDFs)."""
#     text = ""
#     try:
#         with open(pdf_path, "rb") as file:
#             reader = PyPDF2.PdfReader(file)
#             for page in reader.pages:
#                 if page.extract_text():
#                     text += page.extract_text() + " "
#     except Exception as e:
#         print(f"PyPDF2 failed for {pdf_path}: {e}")
#     return text.strip()

# def extract_text_ocr(pdf_path):
#     """Extract text from scanned PDF using OCR."""
#     text = ""
#     try:
#         images = convert_from_path(pdf_path)  # Convert PDF to images
#         for img in images:
#             text += pytesseract.image_to_string(img, lang="eng+mar") + " "  # English + Marathi
#     except Exception as e:
#         print(f"OCR failed for {pdf_path}: {e}")
#     return text.strip()

# def extract_consumer_number(pdf_path):
#     """Extract consumer number using both PyPDF2 and OCR."""
#     text = extract_text_pypdf(pdf_path)
#     if not text:  # If PyPDF2 fails, use OCR
#         text = extract_text_ocr(pdf_path)

#     for pattern in consumer_number_patterns:
#         match = pattern.search(text)
#         if match:
#             return match.group(0)  
#     return "Not Found"

# data = []

# for filename in os.listdir(folder_path):
#     if filename.endswith(".pdf"):
#         pdf_path = os.path.join(folder_path, filename)
#         consumer_number = extract_consumer_number(pdf_path)
#         data.append([filename, consumer_number])

# # Save data to Excel
# df = pd.DataFrame(data, columns=["File Name", "Consumer Number"])
# df.to_excel(output_excel, index=False)

# print(f"Extraction completed! Data saved to {output_excel}")
import os
import pandas as pd
import PyPDF2
import re
from pdf2image import convert_from_path
import pytesseract

folder_path = r"C:\Users\Computer Point\OneDrive\Desktop\E-Bill Downloader\Bills"
output_excel = "output.xlsx"

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

consumer_number_patterns = [
    re.compile(r'Consumer No[:\s]+(\d+)'), 
    re.compile(r'(?:ग्राहक क्रमांक| ाहक  मांक)[:\s]+(\d+)'), 
    re.compile(r'\bN\d{10}\b'),  
    re.compile(r"fcy la\[;k (\d+)"),
    re.compile(r"Account No\.: (\d+)"),
    re.compile(r"Unique Service Number\s*(\d+)"),
    re.compile(r"IVRS\s*[:\-]?\s*([A-Z0-9]+)"),
    re.compile(r"Consumer Number\s*:?\s*(\d+)"),
    re.compile(r'ds-ua\s+:\s+(\d+)'),
    re.compile(r'(?:काउंट सं\.|Account No\.)\s*:\s*(\d+)'),
    re.compile(r'सिव\s*स\s*मांक\s*:\s*(\d+)'),
    re.compile(r'b\d{12}\b'),
    re.compile(r'Account ID\s*\n\s*(\d+)'),
    re.compile(r'Account No:\s*(\d+)'),
    re.compile(r'(\d{10,12})\s+\d+/\d+\s+[A-Z-]+,\d{2}'),
    re.compile(r'Consumer Id\s*:\s*(\d+)'),
    re.compile(r"Amount payable upto due date\s*:\s*(\d+)\s*([0-9]{2}-[A-Za-z]+-[0-9]{4})"),
    re.compile(r"Account[-\s]?(\d{10})"),
    re.compile(r"Service\s*Connection\s*Number\s*[:\-]?\s*(\d{2}-\d{3}-\d{3}-\d{3})")
]

def extract_text_pypdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text + " "
    except Exception as e:
        print(f"PyPDF2 failed for {pdf_path}: {e}")
    return text.strip()

def extract_text_ocr(pdf_path):
    text = ""
    try:
        images = convert_from_path(pdf_path, dpi=300) 
        for img in images:
            text += pytesseract.image_to_string(img, lang="eng+mar", config="--oem 3 --psm 6") + " "
    except Exception as e:
        print(f"OCR failed for {pdf_path}: {e}")
    return text.strip()

def extract_consumer_number(pdf_path):
    text = extract_text_pypdf(pdf_path)
    if not text:  
        text = extract_text_ocr(pdf_path)

    for pattern in consumer_number_patterns:
        match = pattern.search(text)
        if match:
            return match.group(1) if pattern.groups else match.group(0)  
    return "Not Found"

data = []

for filename in os.listdir(folder_path):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(folder_path, filename)
        consumer_number = extract_consumer_number(pdf_path)
        data.append([filename, consumer_number])

# Save data to Excel
df = pd.DataFrame(data, columns=["File Name", "Consumer Number"])
df.to_excel(output_excel, index=False)

print(f"Extraction completed! Data saved to {output_excel}")