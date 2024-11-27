import pytesseract
from PIL import Image
from pathlib import Path

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

BASE_DIR = Path(__file__).resolve().parent.parent

extracted_text = pytesseract.image_to_string(Image.open('1.jpg'))
print(extracted_text)
