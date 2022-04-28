from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import os, pytesseract
from PIL.Image import open as PIL_open
from OcrProcessingClass import OcrResult


class _Label(QtWidgets.QLabel):

     def __init__(self):
          super().__init__()

          # setup attributes
          self.x1, self.y1, self.x2, self.y2 = 0, 0 ,0, 0

          self.temporary_rectangle = None
          self.my_rectangles = []
     
     def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:

          self.x1, self.y1 = event.pos().x(), event.pos().y()
          self.x2, self.y2 = self.x1, self.y1

          self.repaint()

     def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:

          # saving the rectangle
          self.x2, self.y2 = event.pos().x(), event.pos().y()
          self.my_rectangles.append(self.constraint_rectangle(self.x1, self.y1, self.x2, self.y2))
          
          # resseting hthe temporary drawn rectangle
          self.temporary_rectangle = None

          # updating the widget appearence
          self.repaint()

     def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:

          self.x2, self.y2 = event.pos().x(), event.pos().y()

          #the temporary rectangle to be drawn
          self.temporary_rectangle = self.constraint_rectangle(self.x1, self.y1, self.x2, self.y2)
         
          self.repaint()

     def paintEvent(self, e):
          # calling the initial paintEvent
          super().paintEvent(e)

          # brush setup
          painter = QtGui.QPainter(self)
          painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)

          # pen setup
          pen = QtGui.QPen()
          pen.setColor(QtCore.Qt.red)
          pen.setWidth(3)
          painter.setPen(pen)

          # drawing the rectangles 
          if self.temporary_rectangle:
               painter.drawRect(self.temporary_rectangle)

          for rectangle in self.my_rectangles:
               painter.drawRect(rectangle)


          painter.end()

     def constraint_rectangle(self, x1, y1, x2, y2):
          """function that make sure the drawn rectangle is not outside the picture"""
          
          # contraining the value to the size of the pixmap
          p1 = QtCore.QPoint(max(0, min(x1, self.width()-1)), max(0, min(y1, self.height()-1)))
          p2 = QtCore.QPoint(max(0, min(x2, self.width()-1)), max(0, min(y2, self.height()-1)))

          return QtCore.QRect(p1, p2)

     def reset(self):
          self.temporary_rectangle = None
          self.my_rectangles = [] 

class CustomWidget(QtWidgets.QWidget):

     def __init__(self, SIZE, *args, **kwargs):
          super(CustomWidget, self).__init__(*args, **kwargs)

          size = QtCore.QSize(*SIZE)
          
          #the deault path when searching a file         
          dir_path = r"~\Pictures"
          if os.path.exists(dir_path):
               pass
          else:
               dir_path = r"~/Desktop"   

          # setup attributes
          self.default_path = os.path.expanduser(dir_path)
          self.scaled_pixmap = None
          self.word_dict = {}

          # setting up the layouts
          main_layout = QtWidgets.QVBoxLayout()
          self.labels_layout = QtWidgets.QHBoxLayout()
          main_layout.addLayout(self.labels_layout)

          # setting up the label holding the image
          self.img_label = _Label()
          self.img_label.setFrameStyle(1)
          self.labels_layout.addWidget(self.img_label)

          #setting up the label that contains the ocr output
          self.ocr_label = QtWidgets.QLabel()
          self.ocr_label.setFrameStyle(1)
          self.labels_layout.addWidget(self.ocr_label)

          # setting up the choose a file button
          self.choose_a_fileButton = QtWidgets.QPushButton("Pick a file", clicked = self.press_pick_a_file)
          main_layout.addWidget(self.choose_a_fileButton)

          # setting up the make ocr button
          self.do_ocr_button = QtWidgets.QPushButton("Extract Text", clicked = self.do_ocr)
          main_layout.addWidget(self.do_ocr_button)

          # setting up the combo box that choose the desired language of the ocr
          self.lang_combobox = QtWidgets.QComboBox()
          self.languages = [("English", "eng"), ("French", "fra"), ("Hebrew", "heb")]
          self.lang_combobox.addItems(leng[0] for leng in self.languages)
          main_layout.addWidget(self.lang_combobox)

          # setting up the combo box that choose the desired language of the ocr
          self.words_combo = QtWidgets.QComboBox()
          main_layout.addWidget(self.words_combo)

          # setting up the make a rect button
          self.show_rect_button = QtWidgets.QPushButton("show rect", clicked = self.show_rect)
          main_layout.addWidget(self.show_rect_button)

          # set up the size of the widget and the main layout
          self.setGeometry(QtCore.QRect(QtCore.QPoint(0,0), size))
          self.setLayout(main_layout)

     def press_pick_a_file(self, *args):

          #initializing a pick a file widget
          filename = QtWidgets.QFileDialog()

          #picking a file
          myDir = filename.getOpenFileName(filter = "Images (*.png *.jpg *.jpeg *.xml)", directory = self.default_path)

          #if a file is picked
          if myDir[0] != "":

               #reseting the img label to ensure previus changes are deleted
               self.img_label.reset()

               self.current_img_path = myDir[0]

               # setting the pixmap of the image label to the choosen image path
               mixmap = QtGui.QPixmap(self.current_img_path)
               self.scaled_pixmap = mixmap.scaled(460, 647, QtCore.Qt.KeepAspectRatio)
               self.img_label.setPixmap(self.scaled_pixmap)

               # resizing the label widget as needed
               self.img_label.setMinimumSize(self.scaled_pixmap.size())
               self.img_label.setGeometry(QtCore.QRect(self.img_label.pos(), self.img_label.pixmap().size()))
               self.img_label.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

     def do_ocr(self, *args):

          # setting the cmd path to the tesseract .exe
          pytesseract.pytesseract.tesseract_cmd = os.path.expanduser(r"~\AppData\Local\Programs\Tesseract-OCR\tesseract.exe")
        
          #setting the language to the combo box value
          choosed_language = [leng[1] for leng in self.languages][self.lang_combobox.currentIndex()]
                      
          try: 
               # reset the rectangles from the previous ocr
               self.img_label.my_rectangles = []

               img = PIL_open(self.current_img_path)
               self.original_img_height = img.height
                      
               # set the ocr result to the output label
               self.ocr_label.setText(pytesseract.image_to_string(img, lang = choosed_language))
               OcrResult.class_init(self.current_img_path, choosed_language)
               self.word_dict = OcrResult.my_dict
               

               #updating the combo box with words in the text
               self.words_combo.clear()
               self.words_combo.addItems(self.word_dict.keys())

          except AttributeError:

               self.ocr_label.setText("""No image has been selected, please pick a file with the 'Pick a file button'""")

     def show_rect(self):

          key = self.words_combo.currentText()
          x1, y1, x2, y2 = self.word_dict[key].box

          shrink_ratio = self.scaled_pixmap.height()/self.original_img_height
          y_offset = self.img_label.height()/2 - self.scaled_pixmap.height()/2
          x_offset = self.img_label.width()/2 - self.scaled_pixmap.width()/2

          x1 = int(x1 * shrink_ratio - 2 + x_offset)
          y1 = int(y1 * shrink_ratio - 2 + y_offset)
          x2 = int(x2 * shrink_ratio + 1 + x_offset)
          y2 = int(y2 * shrink_ratio + 1 + y_offset)

          rect = QtCore.QRect(QtCore.QPoint(x1, y1), QtCore.QPoint(x2, y2))

          self.img_label.my_rectangles.append(rect)
          self.img_label.repaint()

if __name__ == "__main__":
     app = QtWidgets.QApplication([])
     myWidget = CustomWidget((800, 600))
     myWidget.show()
     app.exec_()