from PyQt5 import QtGui, QtWidgets, QtCore
import os



class MainWindow(QtWidgets.QWidget):

	def __init__(self):
		super().__init__()

		self.current_img_path = None

		self.setWindowTitle("Main app")

		# initializing of a layout
		self.setLayout(QtWidgets.QVBoxLayout())
		
		# initializing of a layout for the butt
		my_form_layout = QtWidgets.QFormLayout()

		#initializing a pick a file widget
		filename = QtWidgets.QFileDialog()

		# initialazing a label to hold the picture
		my_label = QtWidgets.QLabel()
		self.layout().addWidget(my_label)

		#initialazing a pick a file button
		pickFileButton = QtWidgets.QPushButton("Pick a file", clicked = lambda : press_pick_a_file())
		self.layout().addWidget(pickFileButton)

		#initialize label wich contain ocr result
		ocr_out = QtWidgets.QTextEdit("Ocr result will shown after you picked an image")
		self.layout().addWidget(ocr_out)

		#create a combo box
		my_combo = QtWidgets.QComboBox(
			editable = False)
		my_combo.addItems(["English", "French", "Hebrew"])
		my_combo.setCurrentIndex(0)
		self.layout().addWidget(my_combo)

		#initialazing a do ocr button
		do_ocr_button = QtWidgets.QPushButton("Extract text", clicked = lambda : do_ocr())
		self.layout().addWidget(do_ocr_button)

		


		self.show()

		def press_pick_a_file():

			#picking a file
			myDir = filename.getOpenFileName(filter = "Images (*.png *.jpg *.jpeg *.xml)")
			self.current_img_path = myDir[0]

			# setting the pixmap of the main label to the choosen image path
			mixmap = QtGui.QPixmap(myDir[0])
			# new_pixmap = my_label.pixmap()
			scaled_mixmap = mixmap.scaled(400, 400, QtCore.Qt.KeepAspectRatio)

			my_label.setPixmap(scaled_mixmap)


		def do_ocr():

			import pytesseract
			from PIL import Image
			import codecs

			# setting the cmd path to the tesseract .exe (and changing the username to the actual username)
			user_name = os.getcwd().split("\\")[2]
			pytesseract.pytesseract.tesseract_cmd = f"C:/Users/{user_name}/AppData/Local/Programs/Tesseract-OCR/tesseract.exe"
			
			#setting the language to the combo box value
			choosed_language = ["eng", "fra", "heb"][my_combo.currentIndex()]
			
			try:
				img = Image.open(self.current_img_path)
			
			

				# set the ocr result to the output label
				ocr_out.setText(pytesseract.image_to_string(img, lang = choosed_language))

			except AttributeError:

				ocr_out.setText(""""No image has been selected, please pick a file with the 'Pick a file button'""")
				


if __name__ == "__main__":

	app = QtWidgets.QApplication(["mdr"])
	mw = MainWindow()

	app.exec_()