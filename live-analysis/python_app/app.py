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
		self.analysis_thread = QtCore.QThread()

		self.analysis_window = AnalysisWindow()
		self.worker = Worker()

		self.main_layout = QtWidgets.QGridLayout()
		self.prediction_layout = QtWidgets.QHBoxLayout()
		self.side_bar_layout = QtWidgets.QVBoxLayout()
		self.config_layout = QtWidgets.QFormLayout()
		self.bottom_bar = QtWidgets.QHBoxLayout()

		self.check_set_config_iq = False		
		self.run_analysis_btn_check = False
		self.check_open_configs = False

		self.multipliers = {
			"khz": 1e2,
			"mhz": 1e5,
			"ghz": 1e8
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
		
		icon = QtGui.QIcon()	
		iconLocation = './img/icon.png'
		iconLocation = './img/networkneural.png'
		icon.addPixmap(QtGui.QPixmap(iconLocation), QtGui.QIcon.Selected, QtGui.QIcon.On)
		self.setWindowIcon(icon)
	
	def appLayout(self):
		self.menuToolbar()
		self.main_layout.addLayout(self.side_bar_layout, 0, 0)
		self.main_layout.addLayout(self.config_layout, 1, 0)
		self.main_layout.addLayout(self.bottom_bar, 3, 0)

		self.container = QtWidgets.QWidget()
		self.container.setLayout(self.main_layout)
		self.setCentralWidget(self.container)

	def buttons(self):
		# Stick all buttons here
		self.btnRunAnalysis()
		self.btnShowConfigs()
		self.labelGetBatt()
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
	
	def getScreenRes(self):
		screen = QtWidgets.QApplication.primaryScreen()
		screen = screen.availableGeometry()
		return screen
	
	def menuToolbar(self):
		self.menu_toolbar = self.menuBar()
		self.file_menu = self.menu_toolbar.addMenu('&File')

	def contextMenuEvent(self, e):
		context = QtWidgets.QMenu(self)
		context.addAction(QtGui.QAction("Stop/Start Analysis", self))
		context.exec_(e.globalPos())
	
	def btnShowConfigs(self):
		self.show_configs_btn = QtWidgets.QPushButton("Update Configurations", self)
		self.side_bar_layout.addWidget(self.show_configs_btn)
		self.show_configs_btn.clicked.connect(self.btnShowConfigsPressed)
	
	def btnShowConfigsPressed(self):
		self.analysis_window.updateParams(self.params)
		print(self.params)

	def configBandwidth(self):
		self.bandwidth_label = QtWidgets.QLabel("Bandwidth")
		self.bandwidth_input = QtWidgets.QLineEdit()
		self.bandwidth_input.textChanged.connect(self.configBandwidthInputModified)

		self.bandwidth_dropdown = QtWidgets.QComboBox()
		self.bandwidth_dropdown.addItems(["khz", "mhz"])
		self.bwMultiplier = self.multipliers["khz"]
		self.bandwidth_dropdown.currentTextChanged.connect(self.configBWMultiplier)

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
		self.side_bar_layout.addWidget(self.run_analysis_btn)
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
	
	def labelGetBatt(self):
		batt_status = self.getBatt()
		batt_lvl = batt_status['charge']
		batt_plugged = batt_status['plugged_in']
		self.get_batt_label = QtWidgets.QLabel(f'Battery level: {batt_lvl}')
		self.get_batt_charge = QtWidgets.QLabel(f'Charging: {batt_plugged}')
		self.bottom_bar.addWidget(self.get_batt_label)
		self.bottom_bar.addWidget(self.get_batt_charge)
		# self.get_batt_btn.clicked.connect(self.btnGetBattPressed)

	def btnGetBattPressed(self):
		self.get_batt_btn.setText(str(self.getBatt()))

	def connectSA(self):
		if self.check_set_config_iq == False:
			device_connect()
			self.check_set_config_iq = True

	def getBatt(self):
		self.connectSA()
		batt = getBatteryStatus()
		return batt
	
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