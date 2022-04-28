class OcrResult:

     def __init__(self, output_ligne):

          self.level, self.page_num, self.block_num, self.par_num, self.line_num, self.word_num, self.left, self.top, self.width, self.height, self.conf, self.text = output_ligne

          self._box = 0,0,0,0
     
     @property
     def box(self):
          """return the top left and bottom right box position of the word"""

          return int(self.left), int(self.top), int(self.left) + int(self.width), int(self.top) + int(self.height)

     @classmethod
     def class_init(cls, img_path, language):

          import pytesseract
          from PIL import Image
          import codecs
          import cv2 as cv
          import os 
          import re
          user_name = os.getcwd().split('\\')[2]
          pytesseract.pytesseract.tesseract_cmd = os.path.expanduser(r"~\AppData\Local\Programs\Tesseract-OCR\tesseract.exe")
          img = Image.open(img_path)
          ocr_output = pytesseract.image_to_data(img, lang = language)

          def ocr_itd_formatting(ocr_output):

               """processing output image to data from pytesseract"""

               formated_out = ocr_output.split("\n")

               formated_out = [ligne.split(", ") for ligne in formated_out]

               formated_out = [ligne[0].split("\t") for ligne in formated_out]

               formated_out = [ligne for ligne in formated_out if ligne[-1] != ""][1:]

               return formated_out

          pytesseract_output = ocr_itd_formatting(ocr_output)
          cls.my_dict = {}
          for ligne in pytesseract_output:
               cls.my_dict[f"{ligne[-1]}"] = cls(ligne)

if __name__ == "__main__":
     OcrResult.class_init()


     rect = OcrResult.my_dict["John"].box
     print(rect)

