import PyPDF2
import re

# Path to the PDF file
pdf_path = "KsebBill_1157323008399.pdf"

# Open the PDF and extract text
with open(pdf_path, "rb") as file:
    reader = PyPDF2.PdfReader(file)
    text = "\n".join([page.extract_text() for page in reader.pages])

# Extract details using regex
consumer_number = re.search(r"Consumer#\s+(\d+)", text).group(1)
bill_number = re.search(r"Bill#\s+(\d+)", text).group(1)
bill_date = re.search(r"Bill Date\s+([\d-]+)", text).group(1)
due_date = re.search(r"Due Date\s+([\d-]+)", text).group(1)
amount = re.search(r"Net Payable.*?\s+([\d,]+)", text).group(1)
total_consumption = re.search(r"KWH Cumulative Import\s+\d+\.\d+\s+\d+\.\d+\s+\d+\s+(\d+)", text).group(1)

# Print extracted details
extracted_data = {
    "Consumer Number": consumer_number,
    "Bill Number": bill_number,
    "Bill Date": bill_date,
    "Due Date": due_date,
    "Amount": f"₹{amount}",
    "Total Consumption (kWh)": total_consumption,
}

for key, value in extracted_data.items():
    print(f"{key}: {value}")
