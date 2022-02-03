from PySide2 import QtCore, QtWidgets, QtGui, QtCharts

from Functions.Collect import *
from Functions.Request import *
from Functions.Status import *

class MainWindow(QtWidgets.QMainWindow):
	def __init__(self) -> None:
		super().__init__()
		# Global vars
		# self.worker = Worker()

		self.analysis_window = None
		self.main_layout = QtWidgets.QGridLayout()
		self.prediction_layout = QtWidgets.QHBoxLayout()
		self.side_bar_layout = QtWidgets.QVBoxLayout()
		self.config_layout = QtWidgets.QFormLayout()
		self.chart_layout = QtWidgets.QVBoxLayout()
		self.bottom_bar = QtWidgets.QHBoxLayout()

		self.check_set_config_iq = False		
		self.run_analysis_btn_check = False
		self.check_open_configs = False
		self.check_chart_displayed = False
		self.check_filter = True	

		self.multipliers = {
			"khz": 1e3,
			"mhz": 1e6,
			"ghz": 1e9
		}

		# Default analyzing params
		self.params = {
			"num_records": 10,
			"cf": 2.44e9,
			"sample_rate": 0,
			"ref_level": 0,
			"bandwidth": 40e6,
			"record_length": 1024,
			"check_filter": True
		}

		self.configs()
		self.buttons()
		self.appLayout()
	
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
		try:
			self.analysis_window.updateParams(self.params)
		except AttributeError:
			pass
		finally:
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
		if self.analysis_window == None:
			self.analysis_window = AnalysisWindow()
			self.analysis_window.show()


class AnalysisWindow(QtWidgets.QWidget):
	def __init__(self) -> None:
		super().__init__()

		self.analysis_thread = QtCore.QThread()
		self.check_chart_displayed = False

		self.configs()
		self.updateLayout()

	def configs(self):
		# App config things
		screen_size = self.getScreenRes()
		self.setGeometry(0, 0, screen_size.width(), screen_size.height())
		self.window_title = "Live Classification"
		self.setWindowTitle(self.window_title)
		self.setWindowIcon(QtGui.QIcon('./img/icon.png'))
	
	def updateLayout(self):
		self.chart = QtCharts.QtCharts.QChart()
		self.chart.setTitle('Predictions')

		self.initBarChart()
		self.chart.addSeries(self.chart_data)

		self._chart_view = QtCharts.QtCharts.QChartView(self.chart)
		self._chart_view.setRenderHint(QtGui.QPainter.Antialiasing)

		layout = QtWidgets.QVBoxLayout()
		layout.addWidget(self._chart_view)
		self.setLayout(layout)

	def getScreenRes(self):
		screen = QtWidgets.QApplication.primaryScreen()
		screen = screen.availableGeometry()
		return screen
	
	def updateAnalysisCheck(self, check):
		self.run_analysis_btn_check = check
		if self.run_analysis_btn_check:
			self.runAnalysisThread()
	
	def updateParams(self, params):
		self.params = params

	def runAnalysisThread(self):
		self.worker = Worker(self.params)
		self.worker.moveToThread(self.analysis_thread)
		self.analysis_thread.started.connect(self.worker.runAnalysis)
		self.analysis_thread.start()
		self.worker.graphData.connect(self.updateGraph)
		self.worker.finished.connect(self.runAnalysisRecursion)

	def runAnalysisRecursion(self):
		self.analysis_thread.quit()
		self.worker.deleteLater()
		if self.run_analysis_btn_check:
			self.runAnalysisThread()

	def updateGraph(self, res):
		if res[0] == 200:
			res = res[1]
			self.chart_data.clear()
			self.updateChart(res)
		else:
			print(res)
	
	def initPieChart(self):
		self.chart_data = QtCharts.QtCharts.QPieSeries()
		self.updateChart = self.updatePieChart

	def updatePieChart(self, res):
		for i in range(0, len(res['signalNames'])):
			self.chart_data.append(res['signalNames'][i], res['predictions'][i])
	
	def initBarChart(self):
		self.check_labels = False
		self.chart_data = QtCharts.QtCharts.QHorizontalBarSeries()
		# self.chart.setAnimationOptions(QtCharts.QtCharts.QChart.SeriesAnimations)

		self.updateChart = self.updateHorizontalBarChart
	
	def setBarColour(self, filter_res):
		# Need to check the filter status on recv rather than on local or the update of colours lag
		if filter_res:
			# Set Green
			self.data.setColor(QtGui.QColor("#369c5c"))
		else:
			# Set Blue
			self.data.setColor(QtGui.QColor("#4271b8"))

	def updateHorizontalBarChart(self, res):
		# Round predictions
		predictions = res['predictions']
		filter_res = res['filtered']
		for i in range(len(predictions)):
			predictions[i] = round(predictions[i]*100, 2)
		
		print(predictions)

		self.data = QtCharts.QtCharts.QBarSet("Confidence")
		self.data.append(predictions)
		self.setBarColour(filter_res)
		self.chart_data.clear()
		self.chart_data.append(self.data)
		
		if self.check_chart_displayed == False:
			self.axisY = QtCharts.QtCharts.QBarCategoryAxis()
			self.axisY.append(res['signalNames'])
			self.chart.addAxis(self.axisY, QtCore.Qt.AlignLeft)
			self.chart_data.attachAxis(self.axisY)
			self.check_chart_displayed = True

			self.axisX = QtCharts.QtCharts.QValueAxis()
			self.axisX.setRange(0, 100)
			self.chart.addAxis(self.axisX, QtCore.Qt.AlignBottom)
			self.chart_data.attachAxis(self.axisX)

			self.chart.legend().setAlignment(QtCore.Qt.AlignBottom)
			self.chart.legend().setVisible(True)

		else:
			self.axisX.applyNiceNumbers()
	
class Worker(QtCore.QObject):
	started = QtCore.Signal()
	graphData = QtCore.Signal(object)
	finished = QtCore.Signal()

	def __init__(self, params) -> None:
		super().__init__()
		self.params = params

	@QtCore.Slot()
	def runAnalysis(self):
		self.started.emit()
		# Predict
		config_block_iq(self.params['cf'], self.params['ref_level'], self.params['bandwidth'], self.params['record_length'], self.params['sample_rate'])
		data = acquire_block_iq(1024, self.params["num_records"])
		predictions = predict_post('http://localhost:3000/predict', data, self.params['cf'], self.params['check_filter'])
		print(predictions)

		# Update stuff here
		self.graphData.emit(predictions)
		self.finished.emit()
	
	@QtCore.Slot()
	def runBatteryCheck(self):
		batt = getBatteryStatus()
		self.finished.emit(batt)