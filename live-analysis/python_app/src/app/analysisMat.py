from audioop import mul
import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtCore, QtWidgets, QtGui

from Functions.plutoSDR import PlutoSDR
from Functions.Request import predict_post
from Functions.Plotter import Plotter

class MainWindow(QtWidgets.QMainWindow):
	def __init__(self) -> None:
		super().__init__()

		# Layout things
		self.main_layout = QtWidgets.QGridLayout()
		self.prediction_layout = QtWidgets.QHBoxLayout()
		self.side_bar_layout = QtWidgets.QVBoxLayout()
		self.config_layout = QtWidgets.QFormLayout()
		self.chart_layout = QtWidgets.QVBoxLayout()
		self.bottom_bar = QtWidgets.QHBoxLayout()

		# Global vars
		self.check_filter = True	
		self.run_state = False
		self.__barStarted = False
		self.analysis_thread = QtCore.QThread()
		self.Plotter = Plotter()

		# Go do the math
		self.multipliers = {
			"khz": 1e3,
			"mhz": 1e6,
			"ghz": 1e9
		}

		# Default analyzing params
		self.params = {
			"num_records": 10,
			"center_freq": 2440e6, # Center Frequency
			"cfVal": 2440,
			"cfMultiplier": "mhz",
			"sample_rate": 0,
			"ref_level": 0,
			"rx_bandwidth": 40e6, # Bandwidth
			"bwVal": 40,
			"bwMultiplier": "khz",
			"record_length": 1024,
			"check_filter": True,
			"server_ip": '13.76.137.1'
		}

		self.configs()
		self.buttons()
		self.appLayout()
	
	def configs(self):
		# init app configs
		screen_size = self.getScreenRes()
		# self.setGeometry(0, 0, screen_size.width(), screen_size.height())
		self.window_title = "Live Classification"
		self.setWindowTitle(self.window_title)
		
		icon = QtGui.QIcon()	
		iconLocation = './img/icon.png'
		iconLocation = './img/networkneural.png'
		icon.addPixmap(QtGui.QPixmap(iconLocation), QtGui.QIcon.Selected, QtGui.QIcon.On)
		self.setWindowIcon(icon)
		self.initSDR()
	
	def appLayout(self):
		self.menuToolbar()
		self.main_layout.addLayout(self.side_bar_layout, 0, 0)
		self.main_layout.addLayout(self.config_layout, 1, 0)
		self.main_layout.addLayout(self.chart_layout, 2, 0)
		self.main_layout.addLayout(self.bottom_bar, 3, 0)

		self.container = QtWidgets.QWidget()
		self.container.setLayout(self.main_layout)
		self.setCentralWidget(self.container)
		# print(QtWidgets.QWidget.minimumWidth())

	def buttons(self):
		# Init all buttons here
		self.btnRunAnalysis()
		self.btnShowConfigs()
		# self.labelGetBatt()
		self.configCF()
		self.configBandwidth()
		self.configRefLvl()
		self.configSamplingFreq()
		self.configFilter()
	
		# Config buttons layout
		self.config_layout.addRow(self.filter_label, self.filter_checkbox)
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
			self.filter_label,
			self.filter_checkbox
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
		context.addAction(QtWidgets.Action("Stop/Start Analysis", self))
		context.exec_(e.globalPos())
	
	def btnShowConfigs(self):
		self.show_configs_btn = QtWidgets.QPushButton("Update Configurations", self)
		self.side_bar_layout.addWidget(self.show_configs_btn)
		self.show_configs_btn.clicked.connect(self.btnShowConfigsPressed)
	
	def btnShowConfigsPressed(self):
		# Calculate cf and bw with multipliers
		self.params["center_freq"] = int(self.params["cfVal"]*(self.multipliers[self.params['cfMultiplier']]))
		self.params["rx_bandwidth"] = int(self.params["bwVal"]*(self.multipliers[self.params['bwMultiplier']]))

		print(self.params)
	
	def configFilter(self):
		self.filter_label = QtWidgets.QLabel("Enable filtering")
		self.filter_checkbox = QtWidgets.QCheckBox()
		self.filter_checkbox.setCheckState(QtCore.Qt.Checked)
		self.filter_checkbox.stateChanged.connect(self.configFilterModified)
	
	def configFilterModified(self, check):
		if check == 2:
			check = True
		else:
			check = False

		self.params['check_filter'] = check
	
	def configBandwidth(self):
		self.bandwidth_label = QtWidgets.QLabel("Bandwidth")
		self.bandwidth_input = QtWidgets.QLineEdit()
		self.bandwidth_input.setText(str(self.params['bwVal']))
		self.bandwidth_input.textChanged.connect(self.configBandwidthInputModified)

		self.bandwidth_dropdown = QtWidgets.QComboBox()
		self.bandwidth_dropdown.addItems(["khz", "mhz"])

	def configBWMultiplier(self, multiplier):
		self.params["bwMultiplier"] = multiplier;
	
	def configBandwidthInputModified(self, bw_input):
		try:
			self.params['bwVal'] = float(bw_input)
		except ValueError:
			pass
	
	def configCF(self):
		self.cf_label = QtWidgets.QLabel("Center Frequency")
		self.cf_input = QtWidgets.QLineEdit()
		self.cf_input.setText(str(self.params['cfVal']))
		self.cf_input.textChanged.connect(self.configCFInputModified)

		self.cf_dropdown = QtWidgets.QComboBox()
		self.cf_dropdown.addItems(["mhz", "ghz"])
		self.cf_dropdown.currentTextChanged.connect(self.configCFMultiplier)

	def configCFMultiplier(self, multiplier):
		self.params['cfMultiplier'] = multiplier
	
	def configCFInputModified(self, cf_input):
		try:
			self.params['cfVal'] = float(cf_input)
		except ValueError:
			pass

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
		self.run_state = checked
		# TODO: Close and open matplotlib window accordingly
		if self.run_state:
			# GUI updates
			self.run_analysis_btn.setText("Stop")
			self.setWindowTitle("Running analysis...")

			# Run Analysis
			self.runAnalysisThread()
		else:
			# GUI updates
			self.run_analysis_btn.setText("Run")
			self.setWindowTitle(self.window_title)

			# Close Plotter
			self.Plotter.closeWindow()
	
	def labelGetBatt(self):
		batt_status = self.getBatt()
		batt_lvl = batt_status['charge']
		batt_plugged = batt_status['plugged_in']
		self.get_batt_label = QtWidgets.QLabel(f'Battery level: {batt_lvl}')
		self.get_batt_charge = QtWidgets.QLabel(f'Charging: {batt_plugged}')
		self.bottom_bar.addWidget(self.get_batt_label)
		self.bottom_bar.addWidget(self.get_batt_charge)
	
	def initSDR(self):
		self.SDR = PlutoSDR()
		self.btnShowConfigsPressed()
		self.SDR.initConfig(self.params['center_freq'], self.params['rx_bandwidth'], self.params['num_records'])

	def runAnalysisThread(self):
		self.worker = Worker(self.SDR, self.params) # init thread
		self.worker.moveToThread(self.analysis_thread)
		self.analysis_thread.started.connect(self.worker.runAnalysis)
		self.analysis_thread.start()
		self.worker.graphData.connect(self.Plotter.drawChart)
		self.worker.finished.connect(self.runAnalysisRecursion)
	
	def runAnalysisRecursion(self):
		'''Check if loop should stop'''
		self.analysis_thread.quit()
		self.worker.deleteLater()
		if self.run_state:
			self.runAnalysisThread()

class MatPlotLibWindow(QtCore.QObject):
	def __init__(self) -> None:
		super().__init__()
		self.analysis_thread = QtCore.QThread()
	
	def updateGraph(self):
		'''Update data for graph'''
		pass

	def updateAnalysisCheck(self, check):
		'''Update status, whether to run or not'''
		self.run_state = check

class Worker(QtCore.QObject):
	started = QtCore.Signal()
	graphData = QtCore.Signal(object)
	finished = QtCore.Signal()

	def __init__(self, SDR, params) -> None:
		super().__init__()
		self.SDR = SDR
		self.params = params

	def runAnalysis(self):
		self.started.emit()
		predictions = self.predict()
		self.graphData.emit(predictions)
		self.finished.emit()

	def predict(self):
		data = self.SDR.collect_iq()
		url = 'http://' + self.params['server_ip'] + ':3000/predict'
		predictions = predict_post(url, data, self.params['center_freq'], self.params['check_filter'])

		return predictions