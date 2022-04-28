import pytesseract
from PIL import Image
import codecs
import cv2 as cv
import os 

user_name = os.getcwd().split('\\')[2]
pytesseract.pytesseract.tesseract_cmd = os.path.expanduser(r"~\AppData\Local\Programs\Tesseract-OCR\tesseract.exe")
print(os.getcwd())
#test
img = Image.open(r'Pytesseract usage\teste4.jpg')

output = pytesseract.image_to_string(img, lang = "fra")

dictionnary = pytesseract.image_to_(img, lang = "fra")

# exists image_to_ -> data, xml, pandas, boxes, alto_xml and many more

print(dictionnary)

# with codecs.open("output.txt.", "w", "utf-8") as file:

# 	file.write(output)