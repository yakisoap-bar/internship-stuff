import sys, random
from PySide6 import QtCore, QtWidgets, QtGui

# Interacting with the SDR
from Functions.Collect import *
from Functions.Request import *
from Functions.Status import *

class Window(QtWidgets.QMainWindow):
	def __init__(self) -> None:
		super().__init__()

		self.configs()
		self.buttons()
		self.show()
	
	@QtCore.Slot()
	def configs(self):
		# Declare global vars here
		self.check_set_config_iq = False		
		# Defaults
		self.num_records = 10
		self.center_freq = 2.44e9
		self.ref_level = 0
		self.bandwidth = 40e6

		# App config things
		screen_size = self.getScreenRes()
		self.setGeometry(0, 0, screen_size.width(), screen_size.height())
		self.window_title = "Live Classification"
		self.setWindowTitle(self.window_title)
		self.setWindowIcon(QtGui.QIcon('./img/icon.png'))

	def buttons(self):
		# Stick all buttons here
		self.quitButton()

	def getScreenRes(self):
		screen = QtWidgets.QApplication.primaryScreen()
		screen = screen.availableGeometry()
		return screen

	def toggled(self, checked):
		self.check_checked = checked
		if self.check_checked:
			self.quit_btn.setText("Change plz")
			self.quit_btn.setEnabled(False)
		print(self.check_checked)
		self.windowStatus("Running...")
	
	def windowStatus(self, new_title):
		# can use this to show "Running..." or something
		self.setWindowTitle(new_title)
	
	def windowTitle(self, window_title):
		if window_title == 'Running...':
			self.quit_btn.setDisabled(True)

	def quitButton(self):
		self.quit_btn = QtWidgets.QPushButton("Quit", self)
		self.quit_btn.setCheckable(True)
		self.quit_btn.clicked.connect(QtCore.QCoreApplication.instance().quit)

	def runAnalysisBtn(self):
		# btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
		self.run_analysis_btn = QtWidgets.QPushButton("Run", self)
		self.run_analysis_btn.setCheckable(True)
		self.run_analysis_btn.clicked.connect(self.runAnalysisChecked)

	def connectSA(self):
		if self.check_set_config_iq == False:
			config_block_iq(self.center_freq, self.ref_level, self.bandwidth, 1024)
			self.check_set_config_iq = True

	def runAnalysisBtnPressed(self, checked):
		self.run_analysis_btn_check = checked
		if self.run_analysis_btn_check:
			self.run_analysis_btn.setText("Stop")
			self.windowStatus("Running analysis...")
		else:
			self.run_analysis_btn.setText("Run")
			self.windowStatus("Running analysis...")
	
	def runAnalysis(self):
		if self.check_set_config_iq == False:
			self.connectSA()
		
		# While run_analysis_btn is toggled to True
		while self.run_analysis_btn_check:
			data = acquire_block_iq(1024, self.num_records)
			predictions = predict_post('http://localhost:3000/predict', data)
			print(predictions)
			# print([predictions["signalNames"], predictions["predictions"]])

# Run the application
def main():
	app = QtWidgets.QApplication([])
	GUI = Window()
	sys.exit(app.exec())

if __name__ == "__main__":
	main()