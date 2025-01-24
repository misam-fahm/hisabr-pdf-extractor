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

# Define the fallback function
def default_function(file):
    return {'error': 'Unknown PDF type'}

def detect_pdf_type(file):
    """Detect whether the PDF is detailed or non-detailed based on the number of columns in the first table.
    Returns 'detailed' or 'non-detailed'."""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            if tables:
                # Check the first table
                first_table = tables[1]
                print(first_table)
                if len(first_table[0]) > 10:  # Adjust column count threshold as needed
                    return 'detailed'
                else:
                    return 'non-detailed'
    return 'unknown'  # If no tables are found

# Utility function to extract invoice details and items from a single PDF
def extract_invoice_non_detailed(file):
    invoice_details = {}
    with pdfplumber.open(file) as pdf:
        # Extract text from the first page
        first_page = pdf.pages[0]
        text = first_page.extract_text()
        
        # Extract invoice number and date
        for line in text.split('\n'):
            if 'Invoice Date' in line:
                invoice_details['invoice_date'] = line.split(' ')[2]

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
        
        # Parse invoice items
        def parse_invoice_data(data):
            items = []
            parsed_items = []
            i = 0
            while i < len(data):
                if len(data[i]) == 6:  # Adjust this condition based on table structure
                    item = OrderedDict({
                        "item_code": data[i],
                        "spec" : data[i+1],
                        "qty_ship" :(data[i+2]).split(" ")[0] if " " in data[i+2] else data[i+2],
                        "unit" : (data[i+2]).split(" ")[1] + (data[i+3]).split(" ")[0] if " " in data[i+2] else data[i+3],
                        "item_description" : (data[i+3]).split(" ")[1]+(data[i+4]) if " " in data[i+3] else data[i+4],
                        "category" : data[i+5],
                        "invent_value" : data[i+6],
                        "unit_price" : data[i+7],
                        "tax" : data[i+8],
                        "extended_price" : data[i+9],
                    })
                    parsed_items.append(item)
                    i+=10
                else:
                    i += 1
            return parsed_items

        invoice_items = parse_invoice_data(data)

    return {
        "invoice_details": invoice_details,
        "invoice_items": invoice_items
    }

# API route to handle single PDF upload and processing
def extract_invoice_detailed(file):
    invoice_details = {}
    with pdfplumber.open(file) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()
    
        # Extract invoice number and date
        for line in text.split('\n'):
            if 'Invoice Date' in line:
                invoice_details['invoice_date'] = line.split(' ')[2]
    
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
                invoice_details["product_total"] = dt[0].split()[-1].replace('$','')
                invoice_details["misc"] = dt[1].split()[-1].replace('$','')
                invoice_details["sub_total"] = dt[2].split()[-1].replace('$','')
                try :
                    invoice_details["tax_1"] = dt[3].split()[-1].replace('$','')
                    invoice_details["tax_2"] = dt[4].split()[-1].replace('$','')
                except IndexError :
                    pass
            if "Invoice Total" in line :
                invoice_details["invoice_total"] = line.split(" ")[-1].replace('$','')

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
            if len(data[i]) == 6 and data[i].isdigit():
                item = {
                    "item_code": data[i],
                    "qty_ord":data[i+1] if " " not in data[i+1] else data[i+1].split(" ")[0],
                    "qty_ship":(filter_qty_ship(data[i+2]) if " " not in data[i+1] else (data[i+1]).split(" ")[0]),
                    "unit":(filter_unit(data[i+2]) if len(data[i+3].split(" "))!=1 else data[i+3]) if " " not in data[i+1] else data[i+2].split(" ")[-1],
                    "pack":(filter_out_pack(data[i+4]) if " " not in data[i+1] else filter_out_pack(data[i+3])) or filter_out_pack(data[i+3]),
                    "size":(filter_out_size(data[i+4]) if " " not in data[i+1] else filter_out_size(data[i+3])) or filter_out_size(data[i+3]),
                    "brand":(data[i+4] if len(data[i+3].split(" "))!=1 else data[i+5]) if " " not in data[i+1] else data[i+4],
                    "item_description":(data[i+5] if len(data[i+3].split(" "))!=1 else data[i+6]) if " " not in data[i+1] else data[i+5],
                    "category":(data[i+6] if len(data[i+3].split(" "))!=1 else data[i+7]) if " " not in data[i+1] else data[i+6],
                    "invent_value":(data[i+7] if len(data[i+3].split(" "))!=1 else data[i+8]) if " " not in data[i+1] else data[i+7],
                    "unit_price":(data[i+8] if len(data[i+3].split(" "))!=1 else data[i+9]) if " " not in data[i+1] else data[i+8],
                    "spec":(data[i+9] if len(data[i+3].split(" "))!=1 else data[i+10]) if " " not in data[i+1] else data[i+9],
                    "tax":(data[i+10] if len(data[i+3].split(" "))!=1 else data[i+11]) if " " not in data[i+1] else data[i+10],
                    "extended_value":(data[i+11] if len(data[i+3].split(" "))!=1 else data[i+12]) if " " not in data[i+1] else data[i+11],
                }
                
                parsed_items.append(item)
                if " " not in data[i+1]:
                    if len(data[i+3].split(" ")) != 1:
                        i+=12
                    else:
                        i+=13
                else:
                    i+=12
                    
            else:
                i += 1
        return parsed_items

    invoice_items = parse_invoice_data(data)

    return {
    "invoice_details": invoice_details,
    "invoice_items": invoice_items
    }

def extract_invoice_Sysco(file,pdf_type="Sysco"):
    invoice_details = {}
    with pdfplumber.open(file) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()
        
        # Extract invoice number and date
        for line in text.split('\n'):
            if 'TRUCK STOP' in line:
                invoice_details['invoice_number'] = line.split(' ')[3]
            
            # Extract date based on pattern or fallback
            date_match = re.search(r'DATE\s*:\s*(\d{2}/\d{2}/\d{2})', text)
            invoice_details['seller_name'] = pdf_type
            if date_match:
                invoice_details['invoice_date'] = date_match.group(1)
            elif 'SIGNED:' in line:
                invoice_details['invoice_date'] = line.split(' ')[-1]

        # Extract data from tables
        data = []
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    cleaned_row = [cell for cell in row if cell is not None]
                    if cleaned_row:
                        data.extend(cleaned_row)

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
                    "qty": data[i + 1] if data[i] != '1' else data[i],
                    # " ": data[i + 2] if data[i] != '1' else data[i + 2],
                    "unit": data[i + 3] if data[i] != '1' else data[i + 2],
                    "pack": data[i + 4] if data[i] != '1' else data[i + 3],
                    "size": data[i + 5] if data[i] != '1' else data[i + 4],
                    "item_description": data[i + 6] if data[i] != '1' else data[i + 5],
                    "item_code": data[i + 7] if data[i] != '1' else data[i + 6],
                    "unit_price": data[i + 8] if data[i] != '1' else data[i + 7],
                    "tax": data[i + 9] if data[i] != '1' else data[i + 8],
                    "extended_value": data[i + 10] if data[i] != '1' else data[i + 9],
                    "type": pdf_type
            }
            items.append(item)
            i += 9 if data[i] == '1' else 8
        else:
            i += 1


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

