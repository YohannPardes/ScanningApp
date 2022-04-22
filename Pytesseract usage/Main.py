import pytesseract
from PIL import Image
import codecs
import cv2 as cv
import os 

user_name = os.getcwd().split('\\')[2]
pytesseract.pytesseract.tesseract_cmd = f"C:/Users/{user_name}/AppData/Local/Programs/Tesseract-OCR/tesseract.exe"

#test
img = Image.open(r'ScanningApp\Pytesseract usage\test.jpg')

output = pytesseract.image_to_string(img, lang = "fra")

print(output)

with codecs.open("output.txt.", "w", "utf-8") as file:

	file.write(output)