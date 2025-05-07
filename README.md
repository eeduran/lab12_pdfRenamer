PDF Purchase Order Splitter

This Python script scans a large PDF file containing multiple purchase orders and automatically splits it into smaller PDF files. Each smaller file is grouped based on a unique combination of Purchase Order number and Vendor name. The new PDFs are saved inside a folder named 'output_pdfs'.

What This Script Does:
- Scans each page of a PDF file
- Extracts the PO number and Vendor name using text patterns
- Groups pages with the same PO number and Vendor
- Saves each group as a separate PDF (e.g., PO123456_VENDORNAME_signed.pdf)
- Works on Windows, macOS, and Linux

Folder Structure:
When you run the script, your folder will look like this:

your-folder/
├── your-large-pdf.pdf
├── script.py
└── output_pdfs/
    ├── PO123456_VENDOR1_signed.pdf
    ├── PO789012_VENDOR2_signed.pdf
    └── ...

How It Works:
1. The split_large_pdf() function is the main driver of the script.
2. It uses pdfplumber to read the text from each PDF page.
3. Each page’s text is passed to extract_po_vendor(), which uses regular expressions to extract the PO number and Vendor name.
4. Pages with the same PO number and Vendor name are grouped together.
5. For each group, save_grouped_pdf() is called to write those pages into a new PDF file using PyPDF2.

Requirements:
Install the required libraries using pip:

pip install pdfplumber PyPDF2

How to Use:
1. Place this script in a folder with your large .pdf file.
2. Make sure only one .pdf file is present in the folder. The script will use the first one it finds.
3. Run the script:

python script.py

4. Look inside the 'output_pdfs' folder for your split PDFs.

Why Two Libraries?
- pdfplumber is used to extract readable text from each PDF page.
- PyPDF2 is used to copy and save new PDFs from the original pages.

Both are needed because one is great for reading (pdfplumber), and the other is great for writing (PyPDF2).

Example Use Case:
You receive a bulk PDF file with hundreds of purchase orders packed into a single file. Instead of manually splitting the pages by hand, this script automatically extracts the PO number and Vendor name from each page and creates neatly organized PDFs per PO and Vendor.

Important Notes:
- PO numbers must match the format: "Purchase Order #: XXXXXXXX" (8 characters)
- Vendor names are extracted from the text between "Vendor:" and "Ship to:"
- Filenames are cleaned of special characters and limited to 50 characters to avoid filesystem issues.
