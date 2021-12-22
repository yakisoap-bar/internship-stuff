import sys, random
from PySide6 import QtCore, QtWidgets, QtGui

class Window(QtWidgets.QWidget):
	def __init__(self) -> None:
		super().__init__()

		self.setGeometry(50, 50, 500, 300)
		self.setWindowTitle("Live Classification")
		self.setWindowIcon(QtGui.QIcon('./img/icon.png'))

		# Some variables
		self.hello = ["End", "Me", "Plz"]

		# Create some buttons
		self.button = QtWidgets.QPushButton("PUSH BUTTON")
		self.text = QtWidgets.QLabel("End me",
									alignment=QtCore.Qt.AlignCenter)
		
		self.layout = QtWidgets.QVBoxLayout(self)
		self.layout.addWidget(self.text)
		self.layout.addWidget(self.button)

		# On button click, call function
		self.button.clicked.connect(self.changeText)

	
	@QtCore.Slot()
	def changeText(self):
		self.text.setText(random.choice(self.hello))

# Run the application
if __name__ == "__main__":
	app = QtWidgets.QApplication([])
	GUI = Window()

	GUI.resize(800,600)
	GUI.show()

	sys.exit(app.exec())