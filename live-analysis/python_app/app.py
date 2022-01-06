import sys, threading
from PySide6 import QtCore, QtWidgets, QtGui

# Interacting with the SDR
from Functions.Collect import *
from Functions.Request import *
from Functions.Status import *

class mainWindow(QtWidgets.QMainWindow):
	def __init__(self) -> None:
		super().__init__()
		# Declare global vars here
		self.check_set_config_iq = False		
		self.mainLayout = QtWidgets.QGridLayout
		self.sideBarLayout = QtWidgets.QVBoxLayout()
		self.configLayout = QtWidgets.QVBoxLayout()
		self.run_analysis_btn_check = False

		self.multipliers = {
			"khz": 1000,
			"mhz": 10000,
			"ghz": 100000
		}

		# Default analyzing params
		self.num_records = 10
		self.center_freq = 2.44e9
		self.ref_level = 0
		self.bandwidth = 40e6

		self.configs()
		self.buttons()
		self.appLayout()
		self.show()
		self.startAnalysis()
	
	@QtCore.Slot()
	def configs(self):
		# App config things
		# self.setGeometry(0, 0, screen_size.width(), screen_size.height())
		self.window_title = "Live Classification"
		self.setWindowTitle(self.window_title)
		self.setWindowIcon(QtGui.QIcon('./img/icon.png'))
	
	def appLayout(self):
		self.menuToolbar()
		self.sideBarLayout.addLayout(self.configLayout)

		self.container = QtWidgets.QWidget()
		self.container.setLayout(self.sideBarLayout)
		self.setCentralWidget(self.container)

	def buttons(self):
		# Stick all buttons here
		self.btnRunAnalysis()
		self.btnShowConfigs()
		self.configCenterFreq()
		self.configBandwidth()
		self.configRefLvl()
		self.configSamplingFreq()

		self.config_buttons = [
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
		# All the config buttons are a pain
		for button in self.config_buttons:
			self.configLayout.addWidget(button)
			button.hide()
	
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
	
	def btnShowConfigs(self):
		self.show_configs_btn = QtWidgets.QPushButton("Configure", self)
		self.sideBarLayout.addWidget(self.show_configs_btn)
		self.show_configs_btn.setCheckable(True)
		self.show_configs_btn.clicked.connect(self.btnShowConfigsPressed)
	
	def btnShowConfigsPressed(self, checked):

		if checked:
			# Add all the btns to layout
			for button in self.config_buttons:
				button.show()
		else:
			# Remove from layout
			for button in self.config_buttons:
				button.hide()
			self.resize(QtCore.QSize.minimumSizeHint())

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
		self.sideBarLayout.addWidget(self.run_analysis_btn)
		self.run_analysis_btn.setCheckable(True)
		self.run_analysis_btn.clicked.connect(self.btnRunAnalysisPressed)

	def connectSA(self):
		if self.check_set_config_iq == False:
			device_connect()
			self.check_set_config_iq = True

	def btnRunAnalysisPressed(self, checked):
		self.run_analysis_btn_check = checked
		if self.run_analysis_btn_check:
			self.run_analysis_btn.setText("Stop")
			self.setWindowTitle(self.window_title)
			self.startAnalysis()
		else:
			self.run_analysis_btn.setText("Run")
			self.setWindowTitle("Running analysis...")
		
	def getBatt(self):
		self.connectSA()
		print(getBatteryStatus())
	
	def startAnalysis(self):
		# Maybe I should thread this function
		# While run_analysis_btn is toggled to True
		self.connectSA()
		while self.run_analysis_btn_check:
			config_block_iq(self.center_freq, self.ref_level, self.bandwidth, 1024)
			data = acquire_block_iq(1024, self.num_records)
			predictions = predict_post('http://localhost:3000/predict', data)
			print(predictions)
			# print([predictions["signalNames"], predictions["predictions"]])
	
# Run the application
def main():
	app = QtWidgets.QApplication([])
	GUI = mainWindow()
	sys.exit(app.exec())

if __name__ == "__main__":
	main()