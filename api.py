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


from flask import Flask, request, jsonify
import os
import pdfplumber
import json
import re
from flask_cors import CORS
from collections import OrderedDict
from flask import Response

app = Flask(__name__)
CORS(app)

# Utility function to extract invoice details and items from a single PDF
def extract_invoice_Gordon(file, pdf_type="Gordon"):
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
        def parse_invoice_data(data, pdf_type):
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
                        "type":pdf_type,
                    })
                    parsed_items.append(item)
                    i+=10
                else:
                    i += 1
            return parsed_items

        invoice_items = parse_invoice_data(data, pdf_type)

    return {
        "invoice_details": invoice_details,
        "invoice_items": invoice_items
    }

# API route to handle single PDF upload and processing
def extract_invoice_Gordon_detailed(file, pdf_type="Gordon"):
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
    
    def parse_invoice_data(data,pdf_type):
        items = []
        parsed_items = []
        i = 0

        while i < len(data):
            if len(data[i]) == 6:
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
                    "inv_value":(data[i+7] if len(data[i+3].split(" "))!=1 else data[i+8]) if " " not in data[i+1] else data[i+7],
                    "unit_price":(data[i+8] if len(data[i+3].split(" "))!=1 else data[i+9]) if " " not in data[i+1] else data[i+8],
                    "spec":(data[i+9] if len(data[i+3].split(" "))!=1 else data[i+10]) if " " not in data[i+1] else data[i+9],
                    "tax":(data[i+10] if len(data[i+3].split(" "))!=1 else data[i+11]) if " " not in data[i+1] else data[i+10],
                    "extended_value":(data[i+11] if len(data[i+3].split(" "))!=1 else data[i+12]) if " " not in data[i+1] else data[i+11],
                    "type":pdf_type
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

    invoice_items = parse_invoice_data(data,"Gordon")

    return {
    "invoice_details": invoice_details,
    "invoice_items": invoice_items
    }

@app.route('/convert-pdf', methods=['POST'])
def convert_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    pdf_type = request.form.get('pdf_type', 'Gordon')  # Default to 'Gordon' if not provided

    if not file.filename.endswith(".pdf"):
        return jsonify({'error': 'Invalid file format'}), 400

    # Extract data from the uploaded PDF using the selected type
    pdf_type_to_function_and_template = {
        'detailed': (extract_invoice_Gordon_detailed, "template1"),
        'default': (extract_invoice_Gordon, "template2")
    }

    # Get the corresponding function and template based on pdf_type
    extract_function, template = pdf_type_to_function_and_template.get(pdf_type, pdf_type_to_function_and_template['default'])

    # Call the selected function with the file and template
    extracted_data = extract_function(file, template)

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
                extracted_data = extract_invoice_from_pdf(pdf_file)
                all_invoices.append(extracted_data)

                # Save extracted data as a JSON file
                invoice_number = extracted_data['invoice_details'].get('invoice_number', 'unknown_invoice')
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

