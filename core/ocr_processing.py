import os
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

# Developer Comments:
# This module handles OCR (Optical Character Recognition) processing for image and PDF files.
# It uses Tesseract via the pytesseract library to extract text (e.g., notes) from images.
# If a PDF file is uploaded, it converts the PDF pages to images using pdf2image, then applies OCR.

# Configure Tesseract executable path (you need to set this path correctly for your system)
# Make sure Tesseract-OCR is installed in your system, and adjust this path accordingly.
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# Function to process OCR on an image file
def ocr_from_image(image_path):
    """
    Extracts text from an image using Tesseract OCR.

    :param image_path: Path to the image file.
    :return: Extracted text as a string.
    """
    # Open the image file
    img = Image.open(image_path)

    # Apply Tesseract OCR to the image
    extracted_text = pytesseract.image_to_string(img)

    # Return the extracted text
    return extracted_text


# Function to process OCR on a PDF file
def ocr_from_pdf(pdf_path):
    """
    Extracts text from a PDF file by converting each page to an image and then applying OCR.

    :param pdf_path: Path to the PDF file.
    :return: Extracted text as a string (from all PDF pages).
    """
    # Convert PDF pages to a list of images
    images = convert_from_path(pdf_path)

    extracted_text = ""

    # Apply OCR to each image (representing each PDF page)
    for page_number, img in enumerate(images):
        page_text = pytesseract.image_to_string(img)
        extracted_text += f"\n\n--- Page {page_number + 1} ---\n\n" + page_text

    # Return the combined text from all PDF pages
    return extracted_text


# Function to handle OCR based on file type (image or PDF)
def ocr_process_file(file_path):
    """
    Determines if the file is an image or PDF, and processes it accordingly to extract text using OCR.

    :param file_path: Path to the file (can be an image or a PDF).
    :return: Extracted text as a string.
    """
    # Check the file extension to determine the type of file
    file_extension = file_path.lower().rsplit('.', 1)[1]

    if file_extension in ['jpg', 'jpeg', 'png']:
        # If the file is an image, process it with the ocr_from_image function
        return ocr_from_image(file_path)
    elif file_extension == 'pdf':
        # If the file is a PDF, process it with the ocr_from_pdf function
        return ocr_from_pdf(file_path)
    else:
        raise ValueError("Unsupported file format for OCR. Supported formats: JPG, JPEG, PNG, PDF.")


# Function to clean OCR text (optional, for better downstream processing)
def clean_ocr_text(ocr_text):
    """
    Cleans the extracted OCR text by removing unnecessary characters or formatting issues.

    :param ocr_text: The raw OCR text extracted from an image or PDF.
    :return: Cleaned text as a string.
    """
    # Basic cleaning example (removing extra newlines, trimming spaces, etc.)
    cleaned_text = ocr_text.replace('\n\n', '\n').strip()

    # Additional cleaning rules can be added here as needed for the specific application
    return cleaned_text


# Example of how this module could be used:
if __name__ == "__main__":
    # Test OCR on an image
    image_file = 'path_to_your_image.jpg'
    ocr_text = ocr_process_file(image_file)
    print(f"Extracted text from image:\n{ocr_text}")

    # Test OCR on a PDF
    pdf_file = 'path_to_your_pdf.pdf'
    ocr_text_pdf = ocr_process_file(pdf_file)
    print(f"Extracted text from PDF:\n{ocr_text_pdf}")
