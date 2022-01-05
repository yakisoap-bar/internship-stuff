import sys, threading
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
		self.appLayout()
		self.show()
	
	@QtCore.Slot()
	def configs(self):
		# Declare global vars here
		self.check_set_config_iq = False		
		self.mainLayout = QtWidgets.QVBoxLayout()
		self.configLayout = QtWidgets.QHBoxLayout()
		self.multipliers = {
			"khz": 100,
			"mhz": 1000,
			"ghz": 10000
		}
		# Defaults
		self.num_records = 10
		self.center_freq = 2.44e9
		self.ref_level = 0
		self.bandwidth = 40e6

		# App config things
		screen_size = self.getScreenRes()
		# self.setGeometry(0, 0, 500, 300)
		# self.setGeometry(0, 0, screen_size.width(), screen_size.height())
		self.window_title = "Live Classification"
		self.setWindowTitle(self.window_title)
		self.setWindowIcon(QtGui.QIcon('./img/icon.png'))
	
	def appLayout(self):
		self.menuToolbar()
		container = QtWidgets.QWidget()
		container.setLayout(self.mainLayout)
		self.setCentralWidget(container)

	def buttons(self):
		# Stick all buttons here
		self.btnRunAnalysis()
		self.btnShowConfigs()
		self.configCenterFreq()
		self.configBandwidth()
		self.configRefLvl()
		self.configSamplingFreq()
		self.btnQuit()
	
	def getScreenRes(self):
		screen = QtWidgets.QApplication.primaryScreen()
		screen = screen.availableGeometry()
		return screen
	
	def menuToolbar(self):
		self.menu_toolbar = self.menuBar()
		self.file_menu = self.menu_toolbar.addMenu('&File')

	def contextMenuEvent(self, e):
		context = QtWidgets.QMenu(self)
		context.addAction(QtGui.QAction("Test 1", self))
		context.addAction(QtGui.QAction("Test 2", self))
		context.addAction(QtGui.QAction("Test 3", self))
		context.exec_(e.globalPos())

	def windowStatus(self, new_title):
		# can use this to show "Running..." or something
		self.setWindowTitle(new_title)
	
	def windowTitle(self, window_title):
		if window_title == 'Running...':
			self.quit_btn.setDisabled(True)

	def btnQuit(self):
		self.quit_btn = QtWidgets.QPushButton("Quit", self)
		self.mainLayout.addWidget(self.quit_btn)
		self.quit_btn.setCheckable(True)
		self.quit_btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
	
	def btnShowConfigs(self):
		self.show_configs_btn = QtWidgets.QPushButton("Configure", self)
		self.mainLayout.addWidget(self.show_configs_btn)
		self.show_configs_btn.setCheckable(True)
		self.show_configs_btn.clicked.connect(self.btnShowConfigsPressed)
	
	def btnShowConfigsPressed(self, checked):
		config_buttons = [
			self.center_freq_label,
			self.center_freq_input,
			self.center_freq_dropdown,
			self.bandwidth_label,
			self.bandwidth_input,
			self.bandwidth_dropdown,
			self.ref_lvl_label,
			self.ref_lvl_input,
			self.ref_lvl_slider,
			self.sampling_freq_label,
			self.sampling_freq_input,
		]

		if checked:
			# Add all the btns to layout
			for button in config_buttons:
				self.mainLayout.addWidget(button)
		else:
			# Remove from layout
			for button in config_buttons:
				self.mainLayout.removeWidget(button)

	def configBandwidth(self):
		self.bandwidth_label = QtWidgets.QLabel("Bandwidth")
		self.bandwidth_input = QtWidgets.QLineEdit()

		self.bandwidth_dropdown = QtWidgets.QComboBox()
		self.bandwidth_dropdown.addItems(["khz", "mhz"])
		self.bandwidth_dropdown.currentTextChanged.connect(self.configCenterFreqMultiplier)
	
	def configBandwidthMultiplier(self, multiplier):
		self.bwMultiplier = self.multipliers[multiplier]
		
	def configCenterFreq(self):
		self.center_freq_label = QtWidgets.QLabel("Center Frequency")
		self.center_freq_input = QtWidgets.QLineEdit()

		self.center_freq_dropdown = QtWidgets.QComboBox()
		self.center_freq_dropdown.addItems(["mhz", "ghz"])
		self.center_freq_dropdown.currentTextChanged.connect(self.configCenterFreqMultiplier)
	
	def configCenterFreqMultiplier(self, multiplier):
		self.cfMultiplier = self.multipliers[multiplier]

	def configSamplingFreq(self):
		self.sampling_freq_label = QtWidgets.QLabel("Sampling Frequency")
		self.sampling_freq_input = QtWidgets.QLineEdit()

	def configRefLvl(self):
		self.ref_lvl_label = QtWidgets.QLabel("Reference Level")
		self.ref_lvl_input = QtWidgets.QLineEdit()

		self.ref_lvl_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
		self.ref_lvl_slider.setMinimum(0)
		self.ref_lvl_slider.setMaximum(10)
		self.ref_lvl_slider.setSingleStep(1)
		self.ref_lvl_slider.valueChanged.connect(self.configRefLvlSliderVal)
	
	def configRefLvlSliderVal(self, value):
		self.ref_level = value
		
	def btnRunAnalysis(self):
		self.run_analysis_btn = QtWidgets.QPushButton("Run", self)
		self.mainLayout.addWidget(self.run_analysis_btn)
		self.run_analysis_btn.setCheckable(True)
		self.run_analysis_btn.clicked.connect(self.btnRunAnalysisPressed)

	def connectSA(self):
		if self.check_set_config_iq == False:
			config_block_iq(self.center_freq, self.ref_level, self.bandwidth, 1024)
			self.check_set_config_iq = True

	def btnRunAnalysisPressed(self, checked):
		self.run_analysis_btn_check = checked
		if self.run_analysis_btn_check:
			self.run_analysis_btn.setText("Stop")
			self.windowStatus(self.window_title)
		else:
			self.connectSA()
			self.run_analysis_btn.setText("Run")
			self.windowStatus("Running analysis...")
	
	def startAnalysis(self):
		# Maybe I should thread this function
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