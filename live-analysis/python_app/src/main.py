import sys
from PyQt5 import QtWidgets
from app.analysis_pluto import MainWindow

# Run the application
def main():
	app = QtWidgets.QApplication([])
	GUI = MainWindow()
	GUI.show()
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
