import sys, threading
from PySide6 import QtCore, QtWidgets, QtGui

from app.analysis import Worker

from Functions.Collect import *
from Functions.Request import *
from Functions.Status import *

class mainWindow(QtWidgets.QMainWindow):
	def __init__(self) -> None:
		super().__init__()

		# Threading stuff
		self.thread = QtCore.QThread()

		# Global vars
		self.check_set_config_iq = False		
		self.mainLayout = QtWidgets.QGridLayout
		self.sideBarLayout = QtWidgets.QVBoxLayout();
		self.configLayout = QtWidgets.QVBoxLayout()
		self.run_analysis_btn_check = False

		self.multipliers = {
			"khz": 1000,
			"mhz": 10001000,
			"ghz": 10
		}

		# Default analyzing params
		self.params = {
			"num_records": 10,
			"cf": 2.44e9,
			"ref_level": 0,
			"bandwidth": 40e6
		}

		self.configs()
		self.buttons()
		self.appLayout()
		self.show()
	
	@QtCore.Slot()
	def configs(self):
		# App config things
		screen_size = self.getScreenRes()
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
		self.btnGetBatt()
		self.configCF()
		self.configBandwidth()
		self.configRefLvl()
		self.configSamplingFreq()

		self.config_buttons = [
			self.cf_label,
			self.cf_input,
			self.cf_dropdown,
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

			# Check through configs and save them to params

	def configBandwidth(self):
		self.bandwidth_label = QtWidgets.QLabel("Bandwidth")
		self.bandwidth_input = QtWidgets.QLineEdit()
		self.bandwidth_input.textChanged.connect(self.configBandwidthInput)

		self.bandwidth_dropdown = QtWidgets.QComboBox()
		self.bandwidth_dropdown.addItems(["khz", "mhz"])
		self.bandwidth_dropdown.currentTextChanged.connect(self.configCFMultiplier)
	
	def configBWMultiplier(self, multiplier):
		self.bwMultiplier = self.multipliers[multiplier]
	
	def configBandwidthInput(self, bw_input):
		self.bw_input = bw_input
	
	def configCF(self):
		self.cf_label = QtWidgets.QLabel("Center Frequency")
		self.cf_input = QtWidgets.QLineEdit()

		self.cf_dropdown = QtWidgets.QComboBox()
		self.cf_dropdown.addItems(["mhz", "ghz"])
		self.cf_dropdown.currentTextChanged.connect(self.configCFMultiplier)
	
	def configCFMultiplier(self, multiplier):
		self.cfMultiplier = self.multipliers[multiplier]
	
	def configCFInput(self, cf_input):
		self.cf_input = cf_input

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

	def btnRunAnalysisPressed(self, checked):
		self.run_analysis_btn_check = checked
		if self.run_analysis_btn_check:
			self.run_analysis_btn.setText("Stop")
			self.setWindowTitle("Running analysis...")
			self.connectSA()
			self.runAnalysisThread()
		else:
			self.run_analysis_btn.setText("Run")
			self.setWindowTitle(self.window_title)
			try:
				self.thread.exit()
			except:
				pass
	
	def runAnalysisThread(self):
		self.worker = Worker(self.params)
		self.worker.moveToThread(self.thread)
		self.thread.started.connect(self.worker.run)
		self.thread.start()
		self.worker.finished.connect(self.runAnalysisRecursion)

	def runAnalysisRecursion(self):
		print(self.run_analysis_btn_check)
		self.thread.quit()
		self.worker.deleteLater()
		if self.run_analysis_btn_check:
			self.runAnalysisThread()
	
	def btnGetBatt(self):
		self.get_batt_btn = QtWidgets.QPushButton("Battery", self)
		self.sideBarLayout.addWidget(self.get_batt_btn)
		self.get_batt_btn.clicked.connect(self.btnGetBattPressed)

	def btnGetBattPressed(self):
		self.get_batt_btn.setText(str(self.getBatt()))

	def connectSA(self):
		if self.check_set_config_iq == False:
			device_connect()
			self.check_set_config_iq = True

	def getBatt(self):
		self.connectSA()
		batt = getBatteryStatus()["charge"]
		return batt
	
	def updateAnalysisState(self, status):
		self.run_analysis = status

	def runAnalysis(self, params):
		# While run_analysis is toggled to True
		self.connectSA()
		while self.run_analysis_btn_check:
			config_block_iq(params['cf'], params['ref_level'], params['bandwidth'], 1024)
			data = acquire_block_iq(1024, self.params["num_records"])
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