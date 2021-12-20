import sys, random
from PySide6 import QtCore, QtWidgets, QtGui

class Widget(QtWidgets.QWidget):
	def __init__(self) -> None:
		super().__init__()

		self.hello = ["End", "Me", "Plz"]

		self.button = QtWidgets.QPushButton("PUSH BUTTON")
		self.text = QtWidgets.QLabel("End me",
									alignment=QtCore.Qt.AlignCenter)
		
		self.layout = QtWidgets.QVBoxLayout(self)
		self.layout.addWidget(self.text)
		self.layout.addWidget(self.button)

		self.button.clicked.connect(self.magic)

	
	@QtCore.Slot()
	def magic(self):
		self.text.setText(random.choice(self.hello))

if __name__ == "__main__":
	app = QtWidgets.QApplication([])

	widget = Widget()
	widget.resize(800,600)
	widget.show()

	sys.exit(app.exec())