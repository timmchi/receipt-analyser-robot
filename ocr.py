import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from PIL import Image

def extract_text(image_path):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)