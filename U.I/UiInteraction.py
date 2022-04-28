# command for converting .ui to .py file --> pyuic5 -x mainWindow.ui -o main_window.py
from main_window import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import pytesseract
from PIL.Image import open as PIL_open
from os import getcwd
import os

class MyMainWindow(Ui_MainWindow):

     def __init__(self, MainWindow):

          # loading the properties from the ui python converted file
          self.setupUi(MainWindow) 

          #setting up actions to the buttons
          self.pickFileButton.mousePressEvent = self.press_pick_a_file
          self.doOCRButton.mousePressEvent = self.do_ocr

          self.languages = [("English", "eng"), ("French", "fra"), ("Hebrew", "heb")]
          self.langCombo.addItems(leng[0] for leng in self.languages)

          #the deault path when searching a file
          dir_path = r"~\OneDrive\pictures"
          if os.path.exists(dir_path):
               pass

          else:
               dir_path = r"~/Desktop"

          self.default_path = os.path.expanduser(dir_path)

     def press_pick_a_file(self, *args):
          #initializing a pick a file widget
          filename = QtWidgets.QFileDialog()

          #picking a file
           
          myDir = filename.getOpenFileName(filter = "Images (*.png *.jpg *.jpeg *.xml)", directory = self.default_path)

          #if a file is picked
          if myDir[0] != "":
               self.current_img_path = myDir[0]

               # setting the pixmap of the main label to the choosen image path
               mixmap = QtGui.QPixmap(self.current_img_path)
               # new_pixmap = my_label.pixmap()
               scaled_mixmap = mixmap.scaled(460, 647, QtCore.Qt.KeepAspectRatio)

               self.choosenImgLabel.setPixmap(scaled_mixmap)

     def do_ocr(self, *args):

          # setting the cmd path to the tesseract .exe (and changing the username to the actual username)
          user_name = getcwd().split("\\")[2]
          pytesseract.pytesseract.tesseract_cmd = f"C:/Users/{user_name}/AppData/Local/Programs/Tesseract-OCR/tesseract.exe"
                      
          #setting the language to the combo box value
          choosed_language = [leng[1] for leng in self.languages][self.langCombo.currentIndex()]
                      
          try:
               img = PIL_open(self.current_img_path)
                      
               # set the ocr result to the output label
               self.OCROut.setText(pytesseract.image_to_string(img, lang = choosed_language))

          except AttributeError:

               self.OCROut.setText(""""No image has been selected, please pick a file with the 'Pick a file button'""")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication([])
    MainWindow = QtWidgets.QMainWindow()
    mw = MyMainWindow(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())