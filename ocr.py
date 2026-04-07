import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from PIL import Image


# Handles the OCR part of the process.
# Its job is to open one receipt image and turn the text in the image into plain text that the later parts of the robot can work with.
# This is one of the first actual processing steps, because the receipt data has to be extracted from the image before anything can be cleaned, categorized, or reported.
def extract_text(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)