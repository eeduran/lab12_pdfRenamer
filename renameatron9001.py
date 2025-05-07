import os #os library is used to interact with the operating system (look at files, folders, etc)
import re #regular expression (re) library will be used to search for patterns in text
import pdfplumber 
from PyPDF2 import PdfReader, PdfWriter

## ******** BIG PICTURE VIEW FOR HOW THE SCRIPT WORKS IS FOUND ALL THE WAY AT THE BOTTOM **********
 
# Function to extract PO number and vendor name from page text
def extract_po_vendor(text):
    # Searches for "Purchase Order #:" then captures the 8 alphanumeric PO number that follows it
    # text parameter is where the text from the PDF page is passed
    po_match = re.search(r'Purchase Order #:\s*([A-Za-z0-9]{8})', text)

    # Searches for "Vendor:" then captures the vendor name that follows. Looks for "Ship to:" to find the end of the vendor name then
    # text parameter is where the text from the PDF page is passed
    vendor_match = re.search(r'Vendor:\s*(.*?)\s*Ship to:', text)
 
    # If both matches are found, extract the values and assign them to corresponding variables
    # group(1) will extract the po number and the vendor name respectively
    # strip() removes leading and trailing spaces from the matched strings
    # Data capture ONLY happens if the po and vendor matches were found
    if po_match and vendor_match:
        po = po_match.group(1).strip()
        vendor = vendor_match.group(1).strip()

        # Clean up vendor name for filenames
        # Vendor name is sanitized by removing characters that can be problematic in file names
        vendor = vendor.replace(' ', '_').replace('/', '_').replace('\\', '_').replace(':', '_')

        # Sets vendor length to 50 characters max
        if len(vendor) > 50:
            vendor = vendor[:50]  # Shorten if the vendor name is too long
        return f"{po}_{vendor}" # po and vendor are combined to simplify the file name and ensure accurate grouping
    return None # If no matches are found, return None
 
# Function to save grouped pages as a separate PDF
def save_grouped_pdf(group_name, page_indices, input_pdf_path, output_folder):

    #Saves the new PDF files in that folder. This is OS independent, will work on
    #Windows, Mac, Linux, etc. 
    #Then prints information for the user about the file being saved.
    output_path = os.path.join(output_folder, f"{group_name}_signed.pdf")
    print(f"Saving {output_path} with {len(page_indices)} page(s)")
 
    # pyPDF2 (PdfWriter)// Creates a new object named writer what will be used to write
    # the new PDF file. 
    writer = PdfWriter()

    # Open the input PDF file using PyPDF2 (PdfReader)
    # Will grab the pdf file in the current folder that was passed to the function
    with open(input_pdf_path, 'rb') as f:
        #pyPDF2 (PdfReader) // Creates a new object named reader that will be used to read
        #the input PDF file
        reader = PdfReader(f)

        # Responsible for grouping the related pages together to save them in the new PDF
        # this is where they are grouped by PO number and vendor name
        for index in page_indices:
            writer.add_page(reader.pages[index])  # Add the page to the writer
 
    # Write the merged PDF to the output path
    # This is where the new PDF file is created and saved
    with open(output_path, 'wb') as out_f:
        writer.write(out_f)
 
# This function will be used to split the large PDF into smaller PDFs
def split_large_pdf(input_pdf_path):

    output_folder = "output_pdfs"
    os.makedirs(output_folder, exist_ok=True) #checks if the output folder exists and creates it if it doesn't
    grouped_pages = {} #empty dictionary to store the grouped pages in the format of {group_key: [page_indices]}
 
    # Open the input PDF file using pdfplumber for text extraction
    with pdfplumber.open(input_pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:

                # Extract PO number and Vendor name
                group_key = extract_po_vendor(text)
                if group_key:
                    # Add page to the corresponding group
                    if group_key not in grouped_pages:
                        grouped_pages[group_key] = []
                    grouped_pages[group_key].append(i)
 
    # Save each group of pages as a separate PDF
    for group, pages in grouped_pages.items():
        save_grouped_pdf(group, pages, input_pdf_path, output_folder)
    print("\n Success. Check the 'output_pdfs' folder for results.")
 
# Run script on first PDF found in the folder
if __name__ == "__main__":
    # Find the first .pdf file in the current folder
    pdf_files = [f for f in os.listdir() if f.lower().endswith('.pdf')]
    if not pdf_files:
        print("X No PDF file found in this folder.")
    else:
        input_pdf = pdf_files[0]
        print(f"Found PDF: {input_pdf}")
        split_large_pdf(input_pdf)
    input("\nPress Enter to close...")

# ********** BIG PICTURE VIEW ***********

# The extract_po_vendor function specifically only extracts the PO number and vendor name
# from the text found on the given PDF file. And groups the pages accordingly. This one uses
# pdfplumber because it is much better at extracting text from PDF's than PyPDF2.

# The save_grouped_pdf function is responsible for saving the grouped pages as a new PDF file.
# This one uses PyPDF2 to create a new PDF file because it is better at writing PDF files than 
# pdfplumber.

# The split_large_pdf function is the "main" function so-to-speak. If you look closely,
# you'll see that this function also calls the previous two functions when it needs them to
# perform their specific tasks. 

# The bottom portion after if __name__ == "__main__": is the part of the code that runs when the script is executed.
# It specifically looks for the first PDF in the current folder and runs the split_large_pdf function on it.