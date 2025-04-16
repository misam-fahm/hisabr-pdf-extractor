# from flask import Flask, request, jsonify
# import os
# from flask_uploads import UploadSet, configure_uploads, DOCUMENTS
# import pdfplumber # type: ignore
# import json
# import re
# from flask_cors import CORS # type: ignore
# from collections import OrderedDict
# from flask import Response


# app = Flask(__name__)
# CORS(app)

# # Utility function to extract invoice details and items from a single PDF
# def extract_invoice_from_pdf(file, pdf_type="Gordon"):
#     invoice_details = {}
#     with pdfplumber.open(file) as pdf:
#         # Extract text from the first page
#         first_page = pdf.pages[0]
#         text = first_page.extract_text()
        
#         # Extract invoice number and date
#         for line in text.split('\n'):
#             if 'Invoice Date' in line:
#                 invoice_details['invoice_date'] = line.split(' ')[2]

#         match = re.search(r'Invoice\s+(\d+)', text)
#         if match:
#             invoice_details['invoice_number'] = match.group(1)

#         # Extract tables and data
#         pages = pdf.pages
#         data = []
#         for page in pages:
#             tables = page.extract_tables()
#             for table in tables:
#                 for row in table:
#                     cleaned_data = []
#                     for cell in row:
#                         if cell is not None:
#                             cleaned_data.append(cell)
#                     row = cleaned_data
#                     if row:
#                         data += row
        
#         # Parse invoice items
#         def parse_invoice_data(data, pdf_type):
#             items = []
#             parsed_items = []
#             i = 0
#             while i < len(data):
#                 if len(data[i]) == 6:  # Adjust this condition based on table structure
#                     item = OrderedDict({
#                         "item_code": data[i],
#                         "spec" : data[i+1],
#                         "qty_ship" :(data[i+2]).split(" ")[0] if " " in data[i+2] else data[i+2],
#                         "unit" : (data[i+2]).split(" ")[1] + (data[i+3]).split(" ")[0] if " " in data[i+2] else data[i+3],
#                         "item_description" : (data[i+3]).split(" ")[1]+(data[i+4]) if " " in data[i+3] else data[i+4],
#                         "category" : data[i+5],
#                         "invent_value" : data[i+6],
#                         "unit_price" : data[i+7],
#                         "tax" : data[i+8],
#                         "extended_price" : data[i+9],
#                         "type":pdf_type,
#                     })
#                     parsed_items.append(item)
#                     i+=10
#                 else:
#                     i += 1
#             return parsed_items

#         invoice_items = parse_invoice_data(data, pdf_type)

#     return {
#         "invoice_details": invoice_details,
#         "invoice_items": invoice_items
#     }

# # API route to handle single PDF upload and processing
# @app.route('/')
# async def index(request, path=""):
#     return json({'hello': path})

# @app.route('/convert-pdf', methods=['POST'])
# def convert_pdf():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file uploaded'}), 400

#     file = request.files['file']
#     if not file.filename.endswith(".pdf"):
#         return jsonify({'error': 'Invalid file format'}), 400

#     # Extract data from the uploaded PDF
#     extracted_data = extract_invoice_from_pdf(file)

#     # Serialize using json.dumps to respect OrderedDict order
#     return Response(
#         json.dumps(extracted_data, indent=4),
#         mimetype='application/json'
#     )

# # API route to process all PDFs in a directory
# @app.route('/process-pdfs', methods=['POST'])
# def process_pdfs():
#     path = 'JSON_PDFS/Gordon_3rd/'

#     if not os.path.exists(path):
#         return jsonify({'error': 'Directory does not exist'}), 400

#     all_invoices = []
#     for files in os.listdir(path):
#         if files.endswith(".pdf"):
#             file_path = os.path.join(path, files)
#             with open(file_path, 'rb') as pdf_file:
#                 extracted_data = extract_invoice_from_pdf(pdf_file)
#                 all_invoices.append(extracted_data)

#                 # Save extracted data as a JSON file
#                 invoice_number = extracted_data['invoice_details'].get('invoice_number', 'unknown_invoice')
#                 json_filename = f'{path}/{invoice_number}.json'
#                 with open(json_filename, 'w') as json_file:
#                     json.dump(extracted_data, json_file, indent=4)

#     # Serialize using json.dumps to respect OrderedDict order
#     return Response(
#         json.dumps({'message': 'Processed all PDFs', 'invoices': all_invoices}, indent=4),
#         mimetype='application/json'
#     )

# if __name__ == '_main_':
#     app.run(debug=True)













# from flask import Flask, request, jsonify
# import os

# app = Flask(__name__)

# # Create the uploads folder if it doesn't exist
# UPLOAD_FOLDER = 'uploads'
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route('/upload', methods=['POST'])
# def upload_pdf():
#     # Check if the post request has the file part
#     if 'file' not in request.files:
#         return jsonify({"error": "No file part"}), 400

#     file = request.files['file']

#     # If no file is selected
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400

#     # Check if the file is a PDF
#     if file and file.filename.endswith('.pdf'):
#         # Save the file
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#         file.save(filepath)
#         return jsonify({"message": "File uploaded successfully", "filename": file.filename}), 200
#     else:
#         return jsonify({"error": "Invalid file type. Only PDF files are allowed."}), 400

# if __name__ == "__main__":
#     app.run(debug=True)






# from flask import Flask, request, jsonify, Response
# import pdfplumber
# import json
# import re
# from flask_cors import CORS
# from collections import OrderedDict
# from io import BytesIO

# app = Flask(__name__)
# CORS(app)

# # Utility function to extract invoice details and items from a single PDF
# def extract_invoice_from_pdf(file, pdf_type="Gordon"):
#     invoice_details = {}
#     with pdfplumber.open(file) as pdf:
#         first_page = pdf.pages[0]
#         text = first_page.extract_text()
        
#         # Extract invoice number and date
#         for line in text.split('\n'):
#             if 'Invoice Date' in line:
#                 invoice_details['invoice_date'] = line.split(' ')[2]

#         match = re.search(r'Invoice\s+(\d+)', text)
#         if match:
#             invoice_details['invoice_number'] = match.group(1)

#         pages = pdf.pages
#         data = []
#         for page in pages:
#             tables = page.extract_tables()
#             for table in tables:
#                 for row in table:
#                     cleaned_data = []
#                     for cell in row:
#                         if cell is not None:
#                             cleaned_data.append(cell)
#                     row = cleaned_data
#                     if row:
#                         data += row

#         def parse_invoice_data(data, pdf_type):
#             items = []
#             parsed_items = []
#             i = 0
#             while i < len(data):
#                 if len(data[i]) == 6:
#                     item = OrderedDict({
#                         "item_code": data[i],
#                         "spec" : data[i+1],
#                         "qty_ship" :(data[i+2]).split(" ")[0] if " " in data[i+2] else data[i+2],
#                         "unit" : (data[i+2]).split(" ")[1] + (data[i+3]).split(" ")[0] if " " in data[i+2] else data[i+3],
#                         "item_description" : (data[i+3]).split(" ")[1]+(data[i+4]) if " " in data[i+3] else data[i+4],
#                         "category" : data[i+5],
#                         "invent_value" : data[i+6],
#                         "unit_price" : data[i+7],
#                         "tax" : data[i+8],
#                         "extended_price" : data[i+9],
#                         "type":pdf_type,
#                     })
#                     parsed_items.append(item)
#                     i+=10
#                 else:
#                     i += 1
#             return parsed_items

#         invoice_items = parse_invoice_data(data, pdf_type)

#     return {
#         "invoice_details": invoice_details,
#         "invoice_items": invoice_items
#     }

# def extract_invoice_from_pdf_2(file, pdf_type="Gordon"):
#     invoice_details = {}
#     with pdfplumber.open(file) as pdf:
#         first_page = pdf.pages[0]
#         text = first_page.extract_text()
    
#         # Extract invoice number and date
#         for line in text.split('\n'):
#             if 'Invoice Date' in line:
#                 invoice_details['invoice_date'] = line.split(' ')[2]
    
#         match = re.search(r'Invoice\s+(\d+)', text)
#         if match:
#             invoice_details['invoice_number'] = match.group(1)
        
#         pages = pdf.pages
#         data = []
            
#         for page in pages:
#             tables = page.extract_tables()
#             for table in tables:
#                 for row in table:
#                     cleaned_data = []
#                     for cell in row:
#                         if cell is not None:
#                             cleaned_data.append(cell)
#                     row = cleaned_data
#                     if row:
#                         data += row

#     def filter_qty_ship(data):
#         data = data.split(" ")
#         if len(data)>=2:
#             return data[0]
#         else:
#             return data[-1]

#     def filter_unit(data):
#         data=data.split(" ")
#         if len(data)>=2:
#             return data[-1]

    
#     def filter_out_pack(data):
#         if 'x' in data : 
#             pack = data.split('x')[0]
#             return pack
#         elif 'X' in data :
#             pack = data.split('X')[0]
#             return pack

#     def filter_out_size(data):
#         print(data)
#         if 'x' in data : 
#             pack = data.split('x')[-1]
#             return pack
#         elif 'X' in data :
#             pack = data.split('X')[-1]
#             return pack
    
#     def parse_invoice_data(data,pdf_type):
#         items = []
#         parsed_items = []
#         i = 0

#         while i < len(data):
#             if len(data[i]) == 6:
#                 item = {
#                     "item_code": data[i],
#                     "qty_ord":data[i+1] if " " not in data[i+1] else data[i+1].split(" ")[0],
#                     "qty_ship":(filter_qty_ship(data[i+2]) if " " not in data[i+1] else (data[i+1]).split(" ")[0]),
#                     "unit":(filter_unit(data[i+2]) if len(data[i+3].split(" "))!=1 else data[i+3]) if " " not in data[i+1] else data[i+2].split(" ")[-1],
#                     "pack":(filter_out_pack(data[i+4]) if " " not in data[i+1] else filter_out_pack(data[i+3])) or filter_out_pack(data[i+3]),
#                     "size":(filter_out_size(data[i+4]) if " " not in data[i+1] else filter_out_size(data[i+3])) or filter_out_size(data[i+3]),
#                     "brand":(data[i+4] if len(data[i+3].split(" "))!=1 else data[i+5]) if " " not in data[i+1] else data[i+4],
#                     "item_description":(data[i+5] if len(data[i+3].split(" "))!=1 else data[i+6]) if " " not in data[i+1] else data[i+5],
#                     "category":(data[i+6] if len(data[i+3].split(" "))!=1 else data[i+7]) if " " not in data[i+1] else data[i+6],
#                     "inv_value":(data[i+7] if len(data[i+3].split(" "))!=1 else data[i+8]) if " " not in data[i+1] else data[i+7],
#                     "unit_price":(data[i+8] if len(data[i+3].split(" "))!=1 else data[i+9]) if " " not in data[i+1] else data[i+8],
#                     "spec":(data[i+9] if len(data[i+3].split(" "))!=1 else data[i+10]) if " " not in data[i+1] else data[i+9],
#                     "tax":(data[i+10] if len(data[i+3].split(" "))!=1 else data[i+11]) if " " not in data[i+1] else data[i+10],
#                     "extended_value":(data[i+11] if len(data[i+3].split(" "))!=1 else data[i+12]) if " " not in data[i+1] else data[i+11],
#                     "type":pdf_type
#                 }
                
#                 parsed_items.append(item)
#                 if " " not in data[i+1]:
#                     if len(data[i+3].split(" ")) != 1:
#                         i+=12
#                     else:
#                         i+=13
#                 else:
#                     i+=12
                    
#             else:
#                 i += 1
#         return parsed_items

#     invoice_items = parse_invoice_data(data,"Gordon")

#     return {
#     "invoice_details": invoice_details,
#     "invoice_items": invoice_items
#     }

# @app.route('/convert-pdf', methods=['POST'])
# def convert_pdf():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file uploaded'}), 400
    
#     pdf_type = request.form.get('pdf_type', 'detailed')
#     file = request.files['file']
#     if not file.filename.endswith(".pdf"):
#         return jsonify({'error': 'Invalid file format'}), 400

#     # Open the uploaded file as a BytesIO stream
#     file_stream = BytesIO(file.read())
#     # extracted_data = extract_invoice_from_pdf(file_stream)
#     if pdf_type == 'detailed':
#         extracted_data = extract_invoice_from_pdf_2(file_stream)
#     elif pdf_type == 'non-detailed':
#         extracted_data = extract_invoice_from_pdf(file_stream)
#     else:
#         return jsonify({'error': 'Invalid pdf_type'}), 400
#     return Response(
#         json.dumps(extracted_data, indent=4),
#         mimetype='application/json'
#     )

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, jsonify, Response
import os
import pdfplumber
import json
import re
from flask_cors import CORS
from collections import OrderedDict
# from flask import Response

app = Flask(__name__)
CORS(app)

# import pdfplumber
# import json
# import re
# import os

# Define a function to extract the data

# # Define the folder path containing PDF files
# pdf_folder_path = "All_PDFs/Second_Phase_PDFs/"
# json_folder_path = "All_JSONs"

# # Loop through all PDF files in the folder
# for filename in os.listdir(pdf_folder_path):
#     if filename.endswith(".pdf"):
#         pdf_path = os.path.join(pdf_folder_path, filename)
#         json_path = os.path.join(json_folder_path, filename.replace(".pdf", ".json"))

#         # Extract data from the PDF file
#         sales_data = extract_sales_data(pdf_path)

#         # Save extracted data to a JSON file
#         with open(json_path, "w") as json_file:
#             json.dump(sales_data, json_file, indent=4)

#         print(f"Extracted data from {filename} and saved to {json_path}")

def safe_float(value, default=0.0):
    try:
        return float(value.replace(',', ''))
    except (ValueError, TypeError):
        return default

def is_valid_item_code(value):
    """
    Validate if the item_code is a string or an integer but not a float.
    """
    if isinstance(value, str) and value.isdigit():
        return True  # Valid integer as string
    if isinstance(value, int):
        return True  # Valid integer
    return False  # Invalid if it's a float or something else

# Define the fallback function
def default_function(file):
    return {'error': 'Unknown PDF type'}

def detect_pdf_type(file):
    """Detect whether the PDF is detailed or non-detailed based on the number of columns in the first table.
    Returns 'detailed' or 'non-detailed'."""
    with pdfplumber.open(file) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()
            # print(f"Extracted text for detection: {text}")  # Debugging

        # Check for Sysco-specific identifiers
        if any('SYSCO' in line.upper() for line in text.split('\n')):
            return 'Sysco'

    # Check for detailed/non-detailed based on table structure
    # with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            if tables:
                # Check the first table
                first_table = tables[1]
                print(first_table)
                if len(first_table[1]) > 10:  # Adjust column count threshold as needed
                    return 'detailed'
                else:
                    return 'non-detailed'
    return 'unknown'  # If no tables or identifiers are found

def extract_total_tax(file):
    total_tax = 0.0
    with pdfplumber.open(file) as pdf:
        last_page = pdf.pages[-1]
        text = last_page.extract_text()
        # Regular expression to find lines that have 'Tax' and a number pattern
        tax_pattern = r'\(?\d*\)?\s*Tax\s*-\s*[\d\.]+\s*\$([\d\.]+)'  # Match 'Tax - 4.00 $1.48' type format
        
        # Find all tax matches in the text
        matches = re.findall(tax_pattern, text)
        # Loop through the matches and sum up the second number (the tax amount)
        for match in matches:
            total_tax += safe_float(match.replace('$', '').replace(',', ''))
    
    return total_tax

def extract_invoice_due_date(file):
    with pdfplumber.open(file) as pdf:
        last_page = pdf.pages[-1]  # Access the last page
        text = last_page.extract_text()

        # Use a regex to search for "Due Date" followed by a date in dd/mm/yyyy format
        due_date_match = re.search(r'Due Date[:\s]*([\d/]{10})', text)

        # If a match is found, save the due date
        # if due_date_match:
        #     invoice_details['due_date'] = due_date_match.group(1)
        # else:
        #     invoice_details['due_date'] = "Not Found"  # Fallback if not found

        # return due_date_match.group(1) if due_date_match else "Not Found"
        if due_date_match:
            return due_date_match.group(1)  # Return the matched due date
        else:
            return "Not Found"

def extract_alpha(value):
    return "".join(c for c in value if c.isalpha())
    
def extract_sales_data(pdf_path):
    data = {}

    with pdfplumber.open(pdf_path) as pdf:
        # Loop through pages to find relevant data
        for page in pdf.pages:
            text = page.extract_text()
            # print(text)
            
            pattern = r"Sales Summary\s+(\d+)"
            match = re.search(pattern, text)

            if match:
                data["store_name"] = match.group(1)
                # print(match.group(1))
            # location_match = re.search(r'(\d+)\s*- Watikinsville', text)
            # data["store_name"] = location_match.group(1) if location_match else "Not Found"

             # Extract the date 'Sunday, January 1, 2023'
            date_match = re.search(r'(\w+,\s+\w+\s+\d{1,2},\s+\d{4})', text)
            data["sales_date"] = date_match.group(1) if date_match else "Not Found"

            if "Sales Summary" in text:
                data["Sale Summary"] = text.split('\n')[0].split("Sales Summary")[-1]
                data["Date"] = " ".join(text.split('\n')[1].split(" ")[-4:-1])

            if "Gross Sales" in text:
                lines = text.split("\n")

                # Extract specific sales summary details
                for line in lines:
                    if "Gross Sales" in line:
                        data['gross_sales'] = safe_float(line.split("$")[-1].split(" ")[0].replace('$', '').replace(',', ''))
                        data["order_count"] = safe_float(line.split(":")[-1].replace('$', '').replace(',', ''))
                    elif "Net Sales" in line:
                        data['net_sales'] = safe_float(line.split("$")[-1].split(" ")[0].replace('$', '').replace(',', ''))
                        data["guest_count"] = safe_float(line.split(":")[-1].replace('$', '').replace(',', ''))
                    elif "Order Average" in line:
                        data['order_average'] = safe_float(line.split(":")[-1].replace('$', '').replace(',', ''))
                    elif "Total No Sales Count" in line:
                        data["total_no_sales_count"] = safe_float(line.split(" ")[-1].replace('$', '').replace(',', ''))
                        if data['order_average'] == "":
                            data['order_average'] = safe_float(line.split(":")[-1].replace('$', '').replace(',', ''))
                    elif "Total Item Sales" in line:
                        data['total_item_sales'] = safe_float(line.split("$")[1].split(" ")[0].replace('$', '').replace(',', ''))
                        data["taxable_item_sales"] = safe_float(line.split(":")[-1].replace('$', '').replace(',', ''))
                    elif "Cash Tips Received" in line:
                        data['cash_tips_received'] = safe_float(line.split("$")[1].split(" ")[0].replace('$', '').replace(',', ''))
                        data["non_taxable_item_sales"] = safe_float(line.split(":")[-1].replace('$', '').replace(',', ''))
                    elif "+ Tax" in line:
                        data['tax_amt'] = safe_float(line.split("$")[1].replace('$', '').replace(',', ''))
                    elif "Surcharges" in line:
                        data['surcharges'] = safe_float(line.split("$")[1].split(" ")[0].replace('$', '').replace(',', ''))
                        data["deposits_accepted_amount"] = safe_float(line.split(":")[-1].replace('$', '').replace(',', ''))
                    elif "+ Cash Deposits Accepted" in line:
                        data['cash_deposits_accepted'] = safe_float(line.split("$")[1].split(" ")[0].replace('$', '').replace(',', ''))
                        data["deposits_redeemed_amount"] = safe_float(line.split(":")[-1].replace('$', '').replace(',', ''))
                    elif "- Deposits Redeemed" in line:
                        data['- Deposits Redeemed'] = "$" + line.split("$")[1]
                    elif "Paid In" in line:
                        data['paid_in'] = safe_float(line.split("$")[1].split(" ")[0].replace('$', '').replace(',', ''))
                        data["labor_cost"] = safe_float(line.split(":")[-1].replace('$', '').replace(',', ''))
                    elif "Paid Out" in line:
                        data['paid_out'] = safe_float(line.split("$")[1].split(" ")[0].replace('$', '').replace(',', ''))
                        data["labor_hours"] = safe_float(line.split(":")[-1].replace('$', '').replace(',', ''))
                    elif "- Discounts" in line:
                        data['discounts'] = safe_float(line.split("$")[1].split(" ")[0].replace('$', '').replace(',', ''))
                        data["labor_percent"] = safe_float(line.split(":")[-1].replace('$', '').replace(',', ''))
                    elif "- Promotions" in line:
                        data['promotions'] = safe_float(line.split("$")[1].split(" ")[0].replace('$', '').replace(',', ''))
                        data["sales_per_labor_hour"] = safe_float(line.split(":")[-1].replace('$', '').replace(',', ''))
                    elif "Gift Card Promotions" in line:
                        data['gift_card_promotions'] = safe_float(line.split("$")[1].replace('$', '').replace(',', ''))
                    elif "- Refunds" in line:
                        data['refunds'] = safe_float(line.split("$")[1].split(" ")[0].replace('$', '').replace(',', ''))
                        data["gift_card_issue_count"] = safe_float(line.split(":")[-1].replace('$', '').replace(',', ''))
                    elif "Voids" in line:
                        data['voids'] = safe_float(line.split("$")[1].split(" ")[0].replace('$', '').replace(',', ''))
                        data["gift_card_issue_amount"] = safe_float(line.split(":")[-1].replace('$', '').replace(',', ''))
                    elif "Non-Cash Payments" in line:
                        data['non_cash_payments'] = safe_float(line.split("$")[1].split(" ")[0].replace('$', '').replace(',', ''))
                        data["gift_card_reload_count"] = safe_float(line.split(":")[-1].replace('$', '').replace(',', ''))
                    elif "Non Revenue Items" in line:
                        data['non_revenue_items'] = safe_float(line.split("$")[1].split(" ")[0].replace('$', '').replace(',', ''))
                        data["gift_card_reload_amount"] = safe_float(line.split(":")[-1].replace('$', '').replace(',', ''))
                    elif "Cash Back" in line:
                        data['cash_back_amount'] = safe_float(line.split("$")[1].split(" ")[0].replace('$', '').replace(',', ''))
                        data["gift_card_cash_out_count"] = safe_float(line.split(":")[-1].replace('$', '').replace(',', ''))
                    elif "= Total Cash" in line:
                        data['total_cash_amount'] = safe_float(line.split("$")[1].split(" ")[0].replace('$', '').replace(',', ''))
                        data["gift_card_cash_out_amount"] = safe_float(line.split(":")[-1].replace('$', '').replace(',', ''))
                    elif "Donation Count" in line:
                        data['donation_count'] = safe_float(line.split(":")[-1].replace('$', '').replace(',', ''))
                    elif "Donation Total" in line:
                        data['donation_total_amount'] = safe_float(line.split(":")[-1].replace('$', '').replace(',', ''))

        # Revenue Centers
        # ```python
        revenue_centers = []
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split('\n')
            
            for line in lines:
                if "Revenue Centers" in line:
                    for section_line in lines[lines.index(line) + 1:]:
                        # Check for the end of relevant section
                        if section_line.strip() == "Tenders":
                            break
                        else:
                            # Use regex to match the required pattern
                            match = re.match(r"^\s*(\w+(?:[-\s]\w+)*?)\s", section_line)
                            if match:
                                # Ensure "Name" or "Total" are not in the first word of the line
                                first_word = section_line.split(" ")[0]
                                if "Total" not in first_word and "Name" not in first_word:
                                    # Split and assign values as needed
                                    words = section_line.split(" ")
                                    revenue_center = {}  # Create a new dictionary for each revenue center
                                    if words[1].isalpha():
                                        revenue_center['name'] = words[0] + " " + words[1]
                                        revenue_center['quantity'] = safe_float(words[2].replace(',', '')) if not words[2].isalpha() else safe_float(words[3].replace(',', ''))
                                        revenue_center['total'] = safe_float(words[3].replace('$', '').replace(',', '')) if not words[2].isalpha() else safe_float(words[4].replace('$', '').replace(',', ''))
                                        revenue_center["percent"] = safe_float(words[4].replace('%', '')) if not words[2].isalpha() else safe_float(words[5].replace('%', ''))
                                    else:
                                        revenue_center['name'] = words[0]
                                        revenue_center['quantity'] = safe_float(words[1].replace(',', ''))
                                        revenue_center['total'] = safe_float(words[2].replace('$', '').replace(',', ''))
                                        revenue_center["percent"] = safe_float(words[3].replace('%', ''))
        
                                    # Append the revenue center data to the list
                                    revenue_centers.append(revenue_center)
                                    
        # Store all revenue centers in the main data dictionary
        data["revenue_centers"] = revenue_centers

        # Tenders
        All_Tenders = []
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split('\n')
            
            for line in lines:
                if "Tenders" in line:
                    for section_line in lines[lines.index(line) + 1:]:
                        # Check for the end of relevant section
                        if section_line.strip() == "Cash Skims":
                            break
                        else:
                            # Use regex to match the required pattern
                            match = re.match(r"^\s*(\w+(?:[-\s\W*]\w+)*?)\s", section_line)
                            if match:
                                # Ensure "Name" or "Total" are not in the first word of the line
                                first_word = section_line.split(" ")[0]
                                if "Total" not in first_word and "Name" not in first_word:
                                    # Split and assign values as needed
                                    words = section_line.split(" ")
                                    tenders = {}  # Create a new dictionary for each revenue center
                                    tenders["name"] = " ".join(words[:-5])
                                    tenders["quantity"] = safe_float(words[-5].replace('$', '').replace(',', ''))
                                    tenders["payments"] = safe_float(words[-4].replace('$', '').replace(',', ''))
                                    tenders['tips'] = safe_float(words[-3].replace('$', '').replace(',', ''))
                                    tenders['total'] = safe_float(words[-2].replace('$', '').replace(',', ''))
                                    tenders['percent'] = safe_float(words[-1].replace('$', '').replace(',', ''))
                                    # Append the revenue center data to the list
                                    All_Tenders.append(tenders)
        
        # Store all tenders in the main data dictionary
        data["tenders"] = All_Tenders

        #Cash Skims
        Cash_Skims = []
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split('\n')
            
            for line in lines:
                if "Cash Skims" in line:
                    for section_line in lines[lines.index(line) + 1:]:
                        # Check for the end of relevant section
                        if section_line.strip() == "Discounts":
                            break
                        else:
                            # Use regex to match the required pattern
                            match = re.match(r"^\s*(\w+(?:[-\s\W*]\w+)*?)\s", section_line)
                            if match:
                                # Ensure "Name" or "Total" are not in the first word of the line
                                first_word = section_line.split(" ")[0]
                                if "Total" not in first_word and "Name" not in first_word:
                                    # Split and assign values as needed
                                    words = section_line.split(" ")
                                    skims = {}  # Create a new dictionary for each revenue center
                                    skims["Name"] = " ".join(words[:-2]) if not words[-2].isalpha() else " ".join(words[:-1])
                                    skims["Quantity"] = words[-2] if not words[-2].isalpha() else " " 
                                    skims["Total"] = words[-1]
                                    
                                    # Append the revenue center data to the list
                                    Cash_Skims.append(skims)
        
        # Store all tenders in the main data dictionary
        data["Cash Skims"] = Cash_Skims

        #Discounts
        Discounts = []
        for page in pdf.pages[1:]:
            text = page.extract_text()
            lines = text.split('\n')
            
            for line in lines:
                if "Discounts" in line:
                    for section_line in lines[lines.index(line) + 1:]:
                        # Check for the end of relevant section
                        if section_line.strip() == "Promotions":
                            break
                        else:
                            # Use regex to match the required pattern
                            match = re.match(r"^\s*([\W*\d*]* | [\d*\W*])(\w+(?:[-\s\W]\w+)*?)\s", section_line)
                            if match:
                                # Ensure "Name" or "Total" are not in the first word of the line
                                first_word = section_line.split(" ")[0]
                                if "Total" not in first_word and "Name" not in first_word:
                                    words = section_line.split(" ")
                                    discounts = {}  # Create a new dictionary for each revenue center
                                    discounts["Name"] = " ".join(words[:-3])
                                    discounts["Quantity"] = words[-3] 
                                    discounts["Total"] = words[-2]
                                    discounts["Percent"] = words[-1]
                                    
                                    # Append the revenue center data to the list
                                    Discounts.append(discounts)
        
        # Store all discounts in the main data dictionary
        data["Discounts"] = Discounts
        
        #Promotions
        # Promotions = []
        # in_promotions_section = False
        # for page in pdf.pages[1:]:
        #     text = page.extract_text()
        #     lines = text.split('\n')
            
        #     for line in lines:
        #         if "Promotions" in line:
        #             in_promotions_section = True
        #             continue

        #         if in_promotions_section and "Taxes" in line:
        #             in_promotions_section = False
        #             break

        #         if in_promotions_section:
        #             match = re.match(r"^\s*\$([\W\d*]* | [\d*\W*])(\w+(?:[-\s\W]\w+)*?)\s", line)
        #             if match:
        #                 words = line.split()
        #                 if len(words) >= 4:
        #                     if "Name" not in words and "Page" not in words and "Total" not in words and "Sales Summary" not in line and "UTC" not in line:
        #                         promotions = {
        #                             "Name": " ".join(words[:-3]),
        #                             "Quantity": words[-3],
        #                             "Total": words[-2],
        #                             "Percent": words[-1],
        #                         }
        #                         Promotions.append(promotions)

        # # Store Promotions in the data dictionary
        # data["Promotions"] = Promotions
        #Promotions
        Promotions = []
        in_promotions_section = False
        for page in pdf.pages[1:]:
            text = page.extract_text()
            lines = text.split('\n')
            
            for index,line in enumerate(lines):
                if "Promotions" in line:
                    in_promotions_section = True
                    continue

                if in_promotions_section and "Taxes" in line:
                    in_promotions_section = False
                    break

                if in_promotions_section:
                    # match = re.match(r"^\s*\$([\W\d*]* | [\d*\W*])(\w+(?:[-\s\W]\w+)*?)\s", line)
                    match = re.match(r"^\s*(\w[\w\s-]+)\s+(\d+)\s+\$([\d.,]+)\s+([\d.]+%)\s*$", line)
                    if match:
                        words = line.split()
                        if len(words) >= 4:
                            if "Name" not in words and "Page" not in words and "Total" not in words and "Sales Summary" not in line and "UTC" not in line:
                                # print(line,index)
                                if index + 2 < len(lines):  # Ensure the index is within bounds
                                    second_line_after = lines[index + 1]
                                    # bracket_match = re.search(r"\(\d+\)", second_line_after)
                                    # bracket_match = re.search(r"^.+?\s\(\d+\)", second_line_after)
                                    # bracket_match = re.search(r".*\(\d+\)", second_line_after)
                                    bracket_match = re.search(r"^[A-Za-z0-9\s]*\(\d+\)$", second_line_after)
                                    if bracket_match:
                                        # print(f"Bracketed Number Found in Second Line: {bracket_match.group(0)}")
                                        promotions = {
                                            "Name": " ".join(words[:-3])  + " " + bracket_match.group(0),
                                            "Quantity": words[-3],
                                            "Total": words[-2],
                                            "Percent": words[-1],
                                        }
                                        Promotions.append(promotions)
                                        
                                    else:
                                        # print("No Bracketed Number Found in Second Line.") 
                                            
                                        promotions = {
                                            "Name": " ".join(words[:-3]),
                                            "Quantity": words[-3],
                                            "Total": words[-2],
                                            "Percent": words[-1],
                                        }
                                        Promotions.append(promotions)
                                        
                                else:
                                    # print("No second line exists after the matched index.")
                                        
                                    promotions = {
                                        "Name": " ".join(words[:-3]),
                                        "Quantity": words[-3],
                                        "Total": words[-2],
                                        "Percent": words[-1],
                                    }
                                    Promotions.append(promotions)

        # Store Promotions in the data dictionary
        data["Promotions"] = Promotions
        #Taxes
        Taxes = []
        for page in pdf.pages[1:]:
            text = page.extract_text()
            lines = text.split('\n')
            
            for line in lines:
                if "Taxes" in line:
                    for section_line in lines[lines.index(line) + 1:]:
                        if section_line.strip() == "Destinations":
                            break
                        else:
                            match = re.match(r"^\s*(\w[\w\s-]+)\s+(\d+)\s+\$([\d.,]+)\s+([\d.]+%)\s*$", section_line)
                            if match:
                                first_word = section_line.split(" ")[0]
                                if "Total" not in first_word and "Name" not in first_word and "Page" not in first_word:
                                    words = section_line.split(" ")
                                    taxes = {}
                                    taxes["Name"] = " ".join(words[:-3])
                                    taxes["Quantity"] = words[-3] 
                                    taxes["Total"] = words[-2]
                                    taxes["Percent"] = words[-1]
                                    
                                    Taxes.append(taxes)
        
        data["Taxes"] = Taxes
        
        #Destinations
        Destinations = []
        for page in pdf.pages[1:]:
            text = page.extract_text()
            lines = text.split('\n')
            
            for line in lines:
                if "Destinations" in line:
                    for section_line in lines[lines.index(line) + 1:]:
                        if section_line.strip() == "Page":
                            break
                        else:
                            match = re.match(r"^\s*(\w[\w\s-]+)\s+(\d+)\s+\$([\d.,]+)\s+([\d.]+%)\s*$", section_line)
                            if match:
                                first_word = section_line.split(" ")[0]
                                if "Total" not in first_word and "Name" not in first_word and "Page" not in first_word:
                                    words = section_line.split(" ")
                                    destinations = {}
                                    destinations["Name"] = " ".join(words[:-3])
                                    destinations["Quantity"] = words[-3] 
                                    destinations["Total"] = words[-2]
                                    destinations["Percent"] = words[-1]
                                    
                                    Destinations.append(destinations)
        
        data["Destinations"] = Destinations
    return data

# Utility function to extract invoice details and items from a single PDF
def extract_invoice_non_detailed(file):
    invoice_details = {}
    with pdfplumber.open(file) as pdf:
        # Extract text from the first page
        first_page = pdf.pages[0]
        text = first_page.extract_text()
        # Extract invoice number and date
        location_match = re.search(r'(\d+)\s* Wat?kinsville', text, re.IGNORECASE)
        # invoice_details["store_name"] = location_match.group(1) if location_match else "Not Found"
        if location_match:
            invoice_details["store_name"] = location_match.group(1)
        else:
            # If the first regex doesn't match, check the second regex
            second_match = re.search(r'(\d+)\s*Cordele', text, re.IGNORECASE)  # Replace with your second pattern
            if second_match:
                invoice_details["store_name"] = second_match.group(1)
            else:
                invoice_details["store_name"] = "Not Found"
        for line in text.split('\n'):
            if 'Invoice Date' in line:
                invoice_details['invoice_date'] = line.split(' ')[2]            
        if 'Gordon Food Service Inc' in text:
            invoice_details['seller_name'] = 'Gordon Food Service Inc'
        else:
            invoice_details['seller_name'] = 'UNKNOWN'
        match = re.search(r'Invoice\s+(\d+)', text)
        if match:
            invoice_details['invoice_number'] = match.group(1)

        # Extract tables and data
        pages = pdf.pages
        data = []
        for page in pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    cleaned_data = []
                    for cell in row:
                        if cell is not None:
                            cleaned_data.append(cell)
                    row = cleaned_data
                    if row:
                        data += row
        
        for line in data:
            if "SubTotal" in line:
                dt = line.split('\n')
                invoice_details["sub_total"] = safe_float(dt[0].split()[-1].replace('$','').replace(',', ''))
            if "Invoice Total" in line :
                invoice_details["invoice_total"] = safe_float(line.split(" ")[-1].replace('$','').replace(',', ''))
            if "Product Total" in line:
                dt = line.split('\n')
                invoice_details["product_total"] = safe_float(dt[0].split()[-1].replace('$','').replace(',', ''))
        
        # Parse invoice items
        def parse_invoice_data(data):
            items = []
            parsed_items = []
            i = 0
            while i < len(data):
                if len(data[i]) == 6 and is_valid_item_code(data[i]):  # Adjust this condition based on table structure
                    item = OrderedDict({
                        "item_code": data[i],
                        "spec" : data[i+1],
                        # # "qty_ship" :(data[i+2]).split(" ")[0] if " " in data[i+2] else data[i+2],
                        # "qty_ship": safe_float(data[i + 2].split(" ")[0] if " " in data[i + 2] else data[i + 2]),
                        # # "unit" : (data[i+2]).split(" ")[1] + (data[i+3]).split(" ")[0] if " " in data[i+2] else data[i+3],                        
                        # "unit": data[i + 3],
                        # # "item_description" : (data[i+3]).split(" ")[1]+(data[i+4]) if " " in data[i+3] else data[i+4],                        
                        # "item_description": data[i + 4],
                        # "category" : data[i+5],
                        # "invent_value" : safe_float(data[i+6]),
                        # "unit_price" : safe_float(data[i+7]),
                        # "tax" : safe_float(data[i+8]),
                        # "extended_price" : safe_float(data[i+9]),
                        "qty_ship": safe_float(data[i + 2].split(" ")[0] if " " in data[i + 2] else data[i + 2]),
                        "unit": extract_alpha(data[i+2].split(" ")[-1])+data[i+3] if not data[i+3].startswith(("SE ", "OX ")) else (
                            (data[i+2].split(" ")[1] if " " in data[i+2] else data[i+2]) + data[i+3].split(" ")[0]
                            if not data[i+2].isdigit() else ""
                        ),
                        # "item_description": (data[i + 4] if not data[i+3].startswith("SE") else data[i+3].replace("SE","")) if data[i+3].isalnum() else data[i+3].split(" ")[-1]+data[i+4],
                        "item_description": (data[i + 4] if not data[i+3].startswith(("SE ", "OX ")) else data[i+3].replace("SE ", "").replace("SE","").replace("OX ", "")),
                        "category": data[i + 5] if not data[i+3].startswith(("SE ", "OX ")) else data[i+4],
                        "invent_value": data[i + 6] if not data[i+3].startswith(("SE ", "OX ")) else data[i+5],
                        "unit_price": data[i + 7] if not data[i+3].startswith(("SE ", "OX ")) else data[i+6],
                        "tax": data[i + 8] if not data[i+3].startswith(("SE ", "OX ")) else data[i+7],
                        "extended_price": data[i + 9]if not data[i+3].startswith(("SE ", "OX ")) else data[i+8],
                        "type": "non-detailed"
                    })
                    parsed_items.append(item)
                    # i+=10
                    if not data[i+3].startswith(("SE ", "OX ")) :
                        i += 10
                    else:
                        i += 9
                else:
                    i += 1
            return parsed_items

        invoice_items = parse_invoice_data(data)
        # Calculate total of qty_ship
        qty_ship_total = sum(item['qty_ship'] for item in invoice_items)
        invoice_details['qty_ship_total'] = qty_ship_total
    invoice_details["tax_total"] = extract_total_tax(file)
    invoice_details['due_date'] = extract_invoice_due_date(file)

    return {
        "invoice_details": invoice_details,
        "invoice_items": invoice_items
    }

# Function to extract detailed invoices
def extract_invoice_detailed(file):
    invoice_details = {}
    with pdfplumber.open(file) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()
        # Extract invoice number and date
        location_match = re.search(r'(\d+)\s* Wat?kinsville', text, re.IGNORECASE)
        # invoice_details["store_name"] = location_match.group(1) if location_match else "Not Found"
        if location_match:
            invoice_details["store_name"] = location_match.group(1)
        else:
            # If the first regex doesn't match, check the second regex
            second_match = re.search(r'(\d+)\s*Cordele', text, re.IGNORECASE)  # Replace with your second pattern
            if second_match:
                invoice_details["store_name"] = second_match.group(1)
            else:
                invoice_details["store_name"] = "Not Found"
        for line in text.split('\n'):
            if 'Invoice Date' in line:
                invoice_details['invoice_date'] = line.split(' ')[2]            
                # parts = line.split(' ')
                # for part in parts:
                #     if re.match(r'\d{2}/\d{2}/\d{4}', part):  # Match MM/DD/YYYY format
                #         invoice_details['due_date'] = part
                #         break
            if any('Gordon Food Service Inc' in line for line in text.split('\n')):
                invoice_details['seller_name'] = 'Gordon Food Service Inc'
            else:
                invoice_details['seller_name'] = 'UNKNOWN'

        match = re.search(r'Invoice\s+(\d+)', text)
        if match:
            invoice_details['invoice_number'] = match.group(1)
        
        pages = pdf.pages
        data = []
            
        for page in pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    cleaned_data = []
                    for cell in row:
                        if cell is not None:
                            cleaned_data.append(cell)
                    row = cleaned_data
                    if row:
                        data += row

        for line in data:
            if "Product Total" in line:
                dt = line.split('\n')
                invoice_details["product_total"] = safe_float(dt[0].split()[-1].replace('$','').replace(',', ''))
                invoice_details["misc"] = safe_float(dt[1].split()[-1].replace('$','').replace(',', ''))
                invoice_details["sub_total"] = safe_float(dt[2].split()[-1].replace('$','').replace(',', ''))
                try :
                    invoice_details["tax_1"] = dt[3].split()[-1].replace('$','').replace(',', '')
                    invoice_details["tax_2"] = dt[4].split()[-1].replace('$','').replace(',', '')
                except IndexError :
                    pass
            # if "Product Total" in line :
            #     invoice_details["product_total"] = line.split(" ")[-1].replace('$','').replace(',', '')
            # if "Misc" in line :
            #     invoice_details["misc"] = line.split(" ")[-1].replace('$','').replace(',', '')
            # if "SubTotal" in line :
            #     invoice_details["sub_total"] = line.split(" ")[-1].replace('$','').replace(',', '')
            if "Invoice Total" in line :
                invoice_details["invoice_total"] = safe_float(line.split(" ")[-1].replace('$','').replace(',', ''))
            # if 'Due Date' in line:
            #     due_date_match = re.search(r'Due Date[:\s]+(\d{2}/\d{2}/\d{4})', text)
            #     if due_date_match:
            #         invoice_details['due_date'] = due_date_match.group(1)

    invoice_details["tax_total"] = extract_total_tax(file)
    invoice_details['due_date'] = extract_invoice_due_date(file)
    def filter_qty_ship(data):
        data = data.split(" ")
        if len(data)>=2:
            return data[0]
        else:
            return data[-1]

    def filter_unit(data):
        data=data.split(" ")
        if len(data)>=2:
            return data[-1]
    
    def filter_out_pack(data):
        if 'x' in data : 
            pack = data.split('x')[0]
            return pack
        elif 'X' in data :
            pack = data.split('X')[0]
            return pack

    def filter_out_size(data):
        print(data)
        if 'x' in data : 
            pack = data.split('x')[-1]
            return pack
        elif 'X' in data :
            pack = data.split('X')[-1]
            return pack
    
    def parse_invoice_data(data):
        items = []
        parsed_items = []
        i = 0

        while i < len(data):
            # item_code_match = re.match(r'^\d{6}$', data[i])  # 6-digit item code
            # if item_code_match:
            if len(data[i]) == 6 and is_valid_item_code(data[i]):
                # item = {
                #     "item_code": data[i],
                #     "qty_ord": safe_float(data[i + 1].split(" ")[0] if " " in data[i + 1] else data[i + 1]),
                #     "qty_ship": safe_float(data[i + 2].split(" ")[0] if " " in data[i + 2] else data[i + 2]),
                #     "unit": filter_unit(data[i+2]) if len(data[i+3].split(" ")) != 1 else data[i+3],
                #     "pack": filter_out_pack(data[i + 4]) if " " not in data[i + 1] else filter_out_pack(data[i + 3]),
                #     "size": filter_out_size(data[i + 4]) if " " not in data[i + 1] else filter_out_size(data[i + 3]),
                #     "brand": data[i + 4] if len(data[i + 3].split(" ")) != 1 else data[i + 5],
                #     "item_description": data[i + 5] if len(data[i + 3].split(" ")) != 1 else data[i + 6],
                #     "category": data[i + 6] if len(data[i + 3].split(" ")) != 1 else data[i + 7],
                #     "invent_value": data[i + 7] if len(data[i + 3].split(" ")) != 1 else data[i + 8],
                #     "unit_price": data[i + 8] if len(data[i + 3].split(" ")) != 1 else data[i + 9],
                #     "spec": data[i + 9] if len(data[i + 3].split(" ")) != 1 else data[i + 10],
                #     "tax": data[i + 10] if len(data[i + 3].split(" ")) != 1 else data[i + 11],
                #     "extended_value": data[i + 11] if len(data[i + 3].split(" ")) != 1 else data[i + 12],
                #     "type": "detailed",
                #     # "qty_ord":data[i+1] if " " not in data[i+1] else data[i+1].split(" ")[0],
                #     # "qty_ship":(filter_qty_ship(data[i+2]) if " " not in data[i+1] else (data[i+1]).split(" ")[0]),
                #     # "qty_ord": safe_float(data[i + 1].split(" ")[0] if " " in data[i + 1] else data[i + 1]),
                #     # "qty_ship": safe_float(data[i + 2].split(" ")[0] if " " in data[i + 2] else data[i + 2]),
                #     # "unit":(filter_unit(data[i+2]) if len(data[i+3].split(" "))!=1 else data[i+3]) if " " not in data[i+1] else data[i+2].split(" ")[-1],
                #     # "pack":(filter_out_pack(data[i+4]) if " " not in data[i+1] else filter_out_pack(data[i+3])) or filter_out_pack(data[i+3]),
                #     # "size":(filter_out_size(data[i+4]) if " " not in data[i+1] else filter_out_size(data[i+3])) or filter_out_size(data[i+3]),
                #     # "brand":(data[i+4] if len(data[i+3].split(" "))!=1 else data[i+5]) if " " not in data[i+1] else data[i+4],
                #     # "item_description":(data[i+5] if len(data[i+3].split(" "))!=1 else data[i+6]) if " " not in data[i+1] else data[i+5],
                #     # "category":(data[i+6] if len(data[i+3].split(" "))!=1 else data[i+7]) if " " not in data[i+1] else data[i+6],
                #     # "invent_value":(data[i+7] if len(data[i+3].split(" "))!=1 else data[i+8]) if " " not in data[i+1] else data[i+7],
                #     # "unit_price":(data[i+8] if len(data[i+3].split(" "))!=1 else data[i+9]) if " " not in data[i+1] else data[i+8],
                #     # "spec":(data[i+9] if len(data[i+3].split(" "))!=1 else data[i+10]) if " " not in data[i+1] else data[i+9],
                #     # "tax":(data[i+10] if len(data[i+3].split(" "))!=1 else data[i+11]) if " " not in data[i+1] else data[i+10],
                #     # "extended_value":(data[i+11] if len(data[i+3].split(" "))!=1 else data[i+12]) if " " not in data[i+1] else data[i+11],
                # }
                item = {
                    "item_code": data[i],
                    # "qty_ord":data[i+1] if " " not in data[i+1] else data[i+1].split(" ")[0],
                    # "qty_ship":(filter_qty_ship(data[i+2]) if " " not in data[i+1] else (data[i+1]).split(" ")[0]),
                    # "qty_ship": float(data[i + 2].split(" ")[0] if " " not in data[i + 2] else (data[i + 2]).split(" ")[0]),
                    "qty_ord": safe_float(data[i + 1].split(" ")[0] if " " in data[i + 1] else data[i + 1]),
                    "qty_ship": safe_float(data[i + 2].split(" ")[0] if " " in data[i + 2] else data[i + 2]),
                    "unit": (filter_unit(data[i+2]) if len(data[i+3].split(" "))!=1 else data[i+3]) if " " not in data[i+1] else data[i+2].split(" ")[-1],
                    "pack": (filter_out_pack(data[i+4]) if " " not in data[i+1] else filter_out_pack(data[i+3])) or filter_out_pack(data[i+3]),
                    "size": (filter_out_size(data[i+4]) if " " not in data[i+1] else filter_out_size(data[i+3])) or filter_out_size(data[i+3]),
                    "pack_size": data[i+4],
                    "brand": (data[i+4] if len(data[i+3].split(" "))!=1 else data[i+5]) if " " not in data[i+1] else data[i+4],
                    "item_description": (data[i+5] if len(data[i+3].split(" "))!=1 else data[i+6]) if " " not in data[i+1] else data[i+5],
                    "category": (data[i+6] if len(data[i+3].split(" "))!=1 else data[i+7]) if " " not in data[i+1] else data[i+6],
                    "invent_value": safe_float((data[i+7] if len(data[i+3].split(" "))!=1 else data[i+8]) if " " not in data[i+1] else data[i+7]),
                    "unit_price": safe_float((data[i+8] if len(data[i+3].split(" "))!=1 else data[i+9]) if " " not in data[i+1] else data[i+8]),
                    "spec": (data[i+9] if len(data[i+3].split(" "))!=1 else data[i+10]) if " " not in data[i+1] else data[i+9],
                    "tax": safe_float((data[i+10] if len(data[i+3].split(" "))!=1 else data[i+11]) if " " not in data[i+1] else data[i+10]),
                    "extended_price": safe_float((data[i+11] if len(data[i+3].split(" "))!=1 else data[i+12]) if " " not in data[i+1] else data[i+11]),
                    "type": "detailed",
                }
                parsed_items.append(item)
                if " " not in data[i+1]:
                    if len(data[i+3].split(" ")) != 1:
                        i += 12
                    else:
                        i += 13
                else:
                    i += 12
            else:
                i += 1
        return parsed_items

    invoice_items = parse_invoice_data(data)
    qty_ship_total = sum(item['qty_ship'] for item in invoice_items)
    invoice_details['qty_ship_total'] = qty_ship_total

    return {
    "invoice_details": invoice_details,
    "invoice_items": invoice_items
    }

def extract_invoice_Sysco(file):
    invoice_details = {}
    with pdfplumber.open(file) as pdf:
        first_page = pdf.pages[-1]
        text = first_page.extract_text()
        location_match = re.search(r'(\d+)\s+DQ\s+WATKINSVILLE', text, re.IGNORECASE)
        # invoice_details["store_name"] = location_match.group(1) if location_match else "Not Found"
        if location_match:
            invoice_details["store_name"] = location_match.group(1)
        else:
            # If the first regex doesn't match, check the second regex
            second_match = re.search(r'(\d+)\s*DQ\s+Cordele', text, re.IGNORECASE)  # Replace with your second pattern
            if second_match:
                invoice_details["store_name"] = second_match.group(1)
            else:
                invoice_details["store_name"] = "Not Found"
        # print(text)
        for line in text.split('\n'):
            
            def parse_float(value):
                try:
                    # Attempt to parse the float, remove any spaces and handle hyphen as negative sign
                    value_new = (value.replace("-",""))
                    # print(value_new) 
                    return float(value_new)   
                except ValueError:
                    return ""

            if "LAST PAGE" in line:
                due_date = line.split(' ')[0]
                invoice_details["due_date"] = due_date

            if "S U B" in line:
                sub_total = line.split(' ')[-1]
                invoice_details["sub_total"] = parse_float(sub_total)

            if "S UB" in line:
                # print("this line",line)
                next_line = text.split('\n')[i + 1]
                # print("next line",next_line)
                sub_total = next_line.split(' ')[-1]
                # print(sub_total)
                invoice_details["sub_total"] = parse_float(sub_total)

            if "TAX" in line:
                tax_total = line.split(' ')[-1]
                invoice_details["tax_total"] = parse_float(tax_total)

            if "INVOICE" in line:
                # Search for the number after the word 'INVOICE'
                words = line.split()
                for i, word in enumerate(words):
                    if word.upper() == "INVOICE":
                        # Check the next word for a valid number
                        if i + 1 < len(words):
                            possible_number = words[i + 1]
                            try:
                                # Try to convert it to a float
                                invoice_details["invoice_total"] = float(possible_number)
                                # print(f"Invoice Total: {invoice_details['Invoice Total']}")
                            except ValueError:
                                pass  # Skip if not a valid number

            if "T OT A L" in line:
                words = line.split()
                # print(words)
                prev_line = text.split('\n')[i - 1]
                # print(prev_line) 
                if "INVOICE" in prev_line :
                    invoice_details["invoice_total"] = parse_float(words[-1])
                else :
                    print("not found")

    lines = text.split('\n')

    # Initialize dictionary to store the result
    # invoice_details = {}

    # Iterate over lines with index
    for i, line in enumerate(lines):
        line = line.strip()  # Clean up any leading/trailing whitespace

        # Check if "T OT A L" is in the line
        if "T OT A L" in line:
            words = line.split()

            # Ensure there's a previous line to check
            if i > 0:  # i > 0 means there's a previous line to access
                prev_line = lines[i - 1].strip()  # Get the previous line
                next_line = lines[i + 1].strip()
                if "INVOICE" in prev_line:
                    print(prev_line)
                    # Parse the last word from the line (which should be the amount)
                    invoice_details["invoice_total"] = parse_float(words[-1])
                    print(f"Invoice Total: {invoice_details['invoice_total']}")
                elif "S U B" in prev_line or "S UB" in prev_line or "SUB" in prev_line:
                    invoice_details["sub_total"] = parse_float(words[-1])
                elif "INVOICE" in next_line:
                    invoice_details["tax_total"] = parse_float(words[-1])
            else:
                print("No previous line found")

    invoice_details["product_total"] = 0
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            for line in text.split('\n') :
                if "GROUP TOTAL**" in line:
                    last_part = line.split(" ")[-1]
                    # num = float(line.split(" ")[-1])
                    # invoice_details["product_total"] += num
                    try:
                        num = float(last_part.strip())
                        invoice_details["product_total"] += num
                    except ValueError:
                        print(f"Warning: Could not convert '{last_part}' to a number.")
                        
    with pdfplumber.open(file) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()
        
        # Extract invoice number and date
        for line in text.split('\n'):
            if 'TRUCK STOP' in line:
                invoice_details['invoice_number'] = line.split(' ')[3]
            
            # Extract date based on pattern or fallback
            date_match = re.search(r'DATE\s*:\s*(\d{2}/\d{2}/\d{2})', text)
            # invoice_details['seller_name'] = pdf_type
            if date_match:
                invoice_details['invoice_date'] = date_match.group(1)
            elif 'SIGNED:' in line:
                invoice_details['invoice_date'] = line.split(' ')[-1]

        if 'SYSCO ATLANTA LLC' in text:
            invoice_details['seller_name'] = 'SYSCO ATLANTA LLC'
        else:
            invoice_details['seller_name'] = 'UNKNOWN'
        # Extract data from tables
        data = []
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    cleaned_row = [cell for cell in row if cell is not None]
                    if cleaned_row:
                        data.extend(cleaned_row)
            # # Extract SUBTOTAL, TAX TOTAL, and INVOICE TOTAL using regex
            # subtotal_match = re.search(r'SUB\s*TOTAL\s*([\d,]+\.\d{2})', text)
            # if subtotal_match:
            #     invoice_details['subtotal'] = subtotal_match.group(1)
            # else:
            #     invoice_details['subtotal'] = "Not Found"

        # Extract due date, subtotal, tax, and invoice total using refined regex
        # last_page = pdf.pages[-1]
        # text = last_page.extract_text()
        # invoice_details['due_date'] = extract_invoice_due_date(file, "sysco")
        # for last_page in pdf.pages[-1]:
        #     text = last_page.extract_text()
            
        #     # Extract "PAYABLE ON OR BEFORE" date
        #     payable_date_match = re.search(r'PAYABLE ON OR BEFORE\s*[:\-]?\s*(\d{2}/\d{2}/\d{2})', text)
        #     if payable_date_match:
        #         invoice_details['due_date'] = payable_date_match.group(1)
            
        #     # Extract SUBTOTAL, TAX, and TOTAL using regex patterns
        #     subtotal_match = re.search(r'SUB\s*TOTAL\s*[:\-]?\s*([\d,]+\.\d{2})', text)
        #     if subtotal_match:
        #         invoice_details['subtotal'] = safe_float(subtotal_match.group(1).replace(',', ''))
                
        #     tax_match = re.search(r'TAX\s*TOTAL\s*[:\-]?\s*([\d,]+\.\d{2})', text)
        #     if tax_match:
        #         invoice_details['tax'] = safe_float(tax_match.group(1).replace(',', ''))
                
        #     invoice_total_match = re.search(r'INVOICE\s*TOTAL\s*[:\-]?\s*([\d,]+\.\d{2})', text)
        #     if invoice_total_match:
        #         invoice_details['invoice_total'] = safe_float(invoice_total_match.group(1).replace(',', ''))


    # Placeholder for parsing Sysco-specific table data
    # Customize this logic for Sysco's table structure
    items = []
    i = 0
    while i < len(data):
        if data[i] in ['C', 'F', 'D', '1']:
            if data[i] == '1' and data[i+3] not in "123456789-":
                break
            else:  # Adjust based on Sysco table structure
                item = {
                    "loc": "" if data[i] == '1' else data[i],
                    "qty_ship": safe_float(data[i + 1] if data[i] != '1' else data[i]),
                    # " ": data[i + 2] if data[i] != '1' else data[i + 2],
                    "unit": data[i + 3] if data[i] != '1' else data[i + 2],
                    "pack": data[i + 4] if data[i] != '1' else data[i + 3],
                    "size": data[i + 5] if data[i] != '1' else data[i + 4],
                    "pack_size": data[i + 4] if data[i] != '1' else data[i + 3] + data[i + 5] if data[i] != '1' else data[i + 4],
                    "item_description": data[i + 6] if data[i] != '1' else data[i + 5],
                    "item_code": data[i + 7] if data[i] != '1' else data[i + 6],
                    "unit_price": safe_float(data[i + 8] if data[i] != '1' else data[i + 7]),
                    "tax": safe_float(data[i + 9] if data[i] != '1' else data[i + 8]),
                    "extended_price": safe_float(data[i + 10] if data[i] != '1' else data[i + 9]),
                    "type": "sysco",
            }
            items.append(item)
            i += 9 if data[i] == '1' else 8
        else:
            i += 1

    qty_ship_total = sum(item['qty_ship'] for item in items)
    invoice_details['qty_ship_total'] = qty_ship_total

    return {
        "invoice_details": invoice_details,
        "invoice_items": items
    }

@app.route('/convert-pdf', methods=['POST'])
def convert_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    if not file.filename.endswith(".pdf"):
        return jsonify({'error': 'Invalid file format'}), 400

    # Detect PDF type dynamically
    pdf_type = detect_pdf_type(file)

    # Extract data from the uploaded PDF using the selected type
    pdf_type_to_function_and_template = {
        'detailed': extract_invoice_detailed,
        'non-detailed': extract_invoice_non_detailed,
        'Sysco': extract_invoice_Sysco,
    }

    # Get the corresponding function and template based on pdf_type
    extract_function = pdf_type_to_function_and_template.get(pdf_type, default_function)

    # Call the selected function with the file and template
    extracted_data = extract_function(file)

    # if pdf_type == 'detailed':
    #     extracted_data = extract_invoice_Gordon_detailed(file, pdf_type)
    # else:
    #     extracted_data = extract_invoice_Gordon(file, pdf_type)

    return Response(
        json.dumps(extracted_data, indent=4),
        mimetype='application/json'
    )
@app.route('/process-invoice', methods=['POST'])
def process_invoice():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    if not file.filename.endswith(".pdf"):
        return jsonify({'error': 'Invalid file format'}), 400

    # Detect PDF type dynamically
    pdf_type = detect_pdf_type(file)

    # Extract data from the uploaded PDF using the selected type
    pdf_type_to_function_and_template = {
        'detailed': extract_invoice_detailed,
        'non-detailed': extract_invoice_non_detailed,
        'Sysco': extract_invoice_Sysco,
    }

    # Get the corresponding function and template based on pdf_type
    extract_function = pdf_type_to_function_and_template.get(pdf_type, default_function)

    # Call the selected function with the file and template
    extracted_data = extract_function(file)

    # if pdf_type == 'detailed':
    #     extracted_data = extract_invoice_Gordon_detailed(file, pdf_type)
    # else:
    #     extracted_data = extract_invoice_Gordon(file, pdf_type)

    return Response(
        json.dumps(extracted_data, indent=4),
        mimetype='application/json'
    )

@app.route('/process-sales', methods=['POST'])
def process_sales():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    if not file.filename.endswith(".pdf"):
        return jsonify({'error': 'Invalid file format'}), 400

    # Detect PDF type dynamically
    # pdf_type = detect_pdf_type(file)

    # # Extract data from the uploaded PDF using the selected type
    # pdf_type_to_function_and_template = {
    #     'detailed': extract_invoice_detailed,
    #     'non-detailed': extract_invoice_non_detailed,
    #     'Sysco': extract_invoice_Sysco,
    # }

    # Get the corresponding function and template based on pdf_type
    # extract_function = pdf_type_to_function_and_template.get(pdf_type, default_function)

    # Call the selected function with the file and template
    extracted_data = extract_sales_data(file)

    # if pdf_type == 'detailed':
    #     extracted_data = extract_invoice_Gordon_detailed(file, pdf_type)
    # else:
    #     extracted_data = extract_invoice_Gordon(file, pdf_type)

    return Response(
        json.dumps(extracted_data, indent=4),
        mimetype='application/json'
    )

# API route to process all PDFs in a directory
@app.route('/process-pdfs', methods=['POST'])
def process_pdfs():
    path = 'JSON_PDFS/Gordon_3rd/'

    if not os.path.exists(path):
        return jsonify({'error': 'Directory does not exist'}), 400

    all_invoices = []
    for files in os.listdir(path):
        if files.endswith(".pdf"):
            file_path = os.path.join(path, files)
            with open(file_path, 'rb') as pdf_file:
                pdf_type = detect_pdf_type(pdf_file)
                if pdf_type == 'detailed':
                    extracted_data = extract_invoice_detailed(pdf_file)
                elif pdf_type == 'non-detailed':
                    extracted_data = extract_invoice_non_detailed(pdf_file)
                else:
                    extracted_data = {'error': f'Could not determine type for {files}'}
                
                all_invoices.append(extracted_data)

                # Save extracted data as a JSON file
                invoice_number = extracted_data.get('invoice_details', {}).get('invoice_number', 'unknown_invoice')
                json_filename = f'{path}/{invoice_number}.json'
                with open(json_filename, 'w') as json_file:
                    json.dump(extracted_data, json_file, indent=4)

    # Serialize using json.dumps to respect OrderedDict order
    return Response(
        json.dumps({'message': 'Processed all PDFs', 'invoices': all_invoices}, indent=4),
        mimetype='application/json'
    )

if __name__ == '_main_':
    app.run(debug=True)

