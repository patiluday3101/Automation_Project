from pdf2image import convert_from_path
import pytesseract
import re
import json

def extract_text_with_ocr(pdf_path):
    images = convert_from_path(pdf_path)

    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)

    return text

def extract_bill_info(pdf_path):
    bill_info = {
        "consumer_number": None,
        "bill_date": None,
        "due_date": None,
        "amount": None,
        "power_factor": None,
        "total_consumption": None
    }

    # Extract text using OCR
    text = extract_text_with_ocr(pdf_path)

    # Debug: Print the extracted text
    print("Extracted Text:\n", text)

    # Regular expressions to extract information
    consumer_number_match = re.search(r"Unique Service Number\s*(\d+)", text, re.IGNORECASE)
    bill_date_match = re.search(r"Bill Date Due Date Disconnection Date\s*\n(\d{2}-[A-Za-z]{3}-\d{4}) (\d{2}-[A-Za-z]{3}-\d{4})", text, re.IGNORECASE)
    amount_match = re.search(r"Total Amount\s*([\d,]+\.\d{2})", text, re.IGNORECASE)
    power_factor_match = re.search(r"RMD\.\s*([\d\.]+)", text, re.IGNORECASE)
    total_consumption_match = re.search(r"Billed Units\s*(\d+)", text, re.IGNORECASE)


    # Populate the dictionary with extracted values
    if consumer_number_match:
        bill_info["consumer_number"] = consumer_number_match.group(1).strip()
    if bill_date_match:
        bill_info["bill_date"] = bill_date_match.group(1).strip()
    if bill_date_match:
        bill_info["bill_date"] = bill_date_match.group(1).strip()
        bill_info["due_date"] = bill_date_match.group(2).strip()
    if amount_match:
        bill_info["amount"] = float(amount_match.group(1).replace(",", ""))
    if power_factor_match:
        bill_info["power_factor"] = float(power_factor_match.group(1).strip())
    if total_consumption_match:
        bill_info["total_consumption"] = int(total_consumption_match.group(1).strip())

    return bill_info

# Path to the PDF file
pdf_path = r"C:\Users\Computer Point\OneDrive\Desktop\E-Bill Downloader\after12\131102A200010307_ebill (1).pdf"

# Extract the bill information
bill_info = extract_bill_info(pdf_path)

# Convert the dictionary to JSON format
bill_info_json = json.dumps(bill_info, indent=4)

# Print the JSON output
print(bill_info_json)