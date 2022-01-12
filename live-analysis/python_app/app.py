import sys, threading
from PySide6 import QtCore, QtWidgets, QtGui

from app.analysis import Worker, AnalysisWindow

from Functions.Collect import *
from Functions.Request import *
from Functions.Status import *

class mainWindow(QtWidgets.QMainWindow):
	def __init__(self) -> None:
		super().__init__()
		# Global vars
		self.analysis_window = AnalysisWindow()
		self.check_set_config_iq = False		
		self.mainLayout = QtWidgets.QGridLayout()
		self.sideBarLayout = QtWidgets.QVBoxLayout()
		self.config_layout = QtWidgets.QFormLayout()
		self.run_analysis_btn_check = False

		self.multipliers = {
			"khz": 100,
			"mhz": 100000,
			"ghz": 1000000000
		}

		# Default analyzing params
		self.params = {
			"num_records": 10,
			"cf": 2.44e9,
			"sample_rate": 0,
			"ref_level": 0,
			"bandwidth": 40e6,
			"record_length": 1024
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
		self.mainLayout.addLayout(self.sideBarLayout, 0, 0)
		self.mainLayout.addLayout(self.config_layout, 1, 0)

		self.container = QtWidgets.QWidget()
		self.container.setLayout(self.mainLayout)
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
	
		# Config buttons layout
		self.config_layout.addRow(self.cf_label)
		self.config_layout.addRow(self.cf_input, self.cf_dropdown)
		self.config_layout.addRow(self.bandwidth_label)
		self.config_layout.addRow(self.bandwidth_input, self.bandwidth_dropdown)
		self.config_layout.addRow(self.ref_lvl_label, self.ref_lvl_input)
		self.config_layout.addRow(self.ref_lvl_slider)
		self.config_layout.addRow(self.sampling_freq_label, self.sampling_freq_input)

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
		self.show_configs_btn = QtWidgets.QPushButton("Update Configurations", self)
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
			# self.resize(QtCore.QSize.minimumSizeHint())

			# Check through configs and save them to params
			self.analysis_window.updateParams(self.params)

	def configBandwidth(self):
		self.bandwidth_label = QtWidgets.QLabel("Bandwidth")
		self.bandwidth_input = QtWidgets.QLineEdit()
		self.bandwidth_input.textChanged.connect(self.configBandwidthInputModified)

		self.bandwidth_dropdown = QtWidgets.QComboBox()
		self.bandwidth_dropdown.addItems(["khz", "mhz"])
		self.bwMultiplier = self.multipliers["khz"]
		self.bandwidth_dropdown.currentTextChanged.connect(self.configCFMultiplier)

		self.bandwidth_input.setText(str(self.params['bandwidth']/self.bwMultiplier))
	
	def configBWMultiplier(self, multiplier):
		self.bwMultiplier = self.multipliers[multiplier]
	
	def configBandwidthInputModified(self, bw_input):
		try:
			self.params['bandwidth'] = float(bw_input)*self.bwMultiplier
		except ValueError:
			self.params['bandwidth'] = 0
	
	def configCF(self):
		self.cf_label = QtWidgets.QLabel("Center Frequency")
		self.cf_input = QtWidgets.QLineEdit()
		self.cf_input.textChanged.connect(self.configCFInputModified)

		self.cf_dropdown = QtWidgets.QComboBox()
		self.cf_dropdown.addItems(["mhz", "ghz"])
		self.cfMultiplier = self.multipliers['mhz']
		self.cf_dropdown.currentTextChanged.connect(self.configCFMultiplier)

		self.cf_input.setText(str(self.params['cf']/self.cfMultiplier))
	
	def configCFMultiplier(self, multiplier):
		self.cfMultiplier = self.multipliers[multiplier]
	
	def configCFInputModified(self, cf_input):
		try:
			self.params['cf'] = float(cf_input)*self.cfMultiplier
		except ValueError:
			self.params['cf'] = 0

	def configSamplingFreq(self):
		self.sampling_freq_label = QtWidgets.QLabel("Sampling Frequency")
		self.sampling_freq_input = QtWidgets.QLineEdit()
		self.sampling_freq_input.textChanged.connect(self.configSamplingFreqInputModified)

		self.sampling_freq_input.setText(str(self.params['sample_rate']))
	
	def configSamplingFreqInputModified(self, sample_input):
		self.params['sample_rate'] = int(sample_input)

	def configRefLvl(self):
		self.ref_lvl_label = QtWidgets.QLabel("Reference Level")
		self.ref_lvl_input = QtWidgets.QLineEdit()
		self.ref_lvl_input.textChanged.connect(self.configRefLvlInputModified)
		self.ref_lvl_input.setText(str(self.params['ref_level']))

		self.ref_lvl_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
		self.ref_lvl_slider.setMinimum(0)
		self.ref_lvl_slider.setMaximum(10)
		self.ref_lvl_slider.setSingleStep(1)
		self.ref_lvl_slider.valueChanged.connect(self.configRefLvlSliderVal)
	
	def configRefLvlInputModified(self, value):
		self.params['ref_level'] = int(value)
	
	def configRefLvlSliderVal(self, value):
		self.params['ref_level'] = value
		self.ref_lvl_input.clear()
		self.ref_lvl_input.insert(str(self.params['ref_level']))
		
	def btnRunAnalysis(self):
		self.run_analysis_btn = QtWidgets.QPushButton("Run", self)
		self.sideBarLayout.addWidget(self.run_analysis_btn)
		self.run_analysis_btn.setCheckable(True)
		self.run_analysis_btn.clicked.connect(self.btnRunAnalysisPressed)

	def btnRunAnalysisPressed(self, checked):
		self.run_analysis_btn_check = checked
		if self.run_analysis_btn_check:
			# GUI updates
			self.run_analysis_btn.setText("Stop")
			self.setWindowTitle("Running analysis...")

			# Open new window
			self.toggleAnalysisWindow()

			# Actual analysis
			self.connectSA()
			self.analysis_window.updateParams(self.params)
			self.analysis_window.updateAnalysisCheck(True)

		else:
			# GUI updates
			self.run_analysis_btn.setText("Run")
			self.setWindowTitle(self.window_title)

			# Close analysis window
			self.analysis_window.updateAnalysisCheck(False)
	
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
		batt = getBatteryStatus()
		print(batt)
		return batt["charge"]
	
	def toggleAnalysisWindow(self):
		# if self.analysis_window == None:
		# 	self.analysis_window = AnalysisWindow()
			self.analysis_window.show()
	
# Run the application
def main():
	app = QtWidgets.QApplication([])
	GUI = mainWindow()
	sys.exit(app.exec())

if __name__ == "__main__":
	main()