from PySide6 import QtCore, QtWidgets, QtGui, QtCharts

from Functions.Collect import *
from Functions.Request import *
from Functions.Status import *

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
		self.chart = QtCharts.QChart()
		self.chart.setTitle('Predictions')

		self.initBarChart()
		self.chart.addSeries(self.chart_data)

		self._chart_view = QtCharts.QChartView(self.chart)
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
		self.chart_data = QtCharts.QPieSeries()
		self.updateChart = self.updatePieChart

	def updatePieChart(self, res):
		for i in range(0, len(res['signalNames'])):
			self.chart_data.append(res['signalNames'][i], res['predictions'][i])
	
	def initBarChart(self):
		self.check_labels = False
		self.chart_data = QtCharts.QHorizontalBarSeries()
		self.chart.setAnimationOptions(QtCharts.QChart.SeriesAnimations)

		self.updateChart = self.updateHorizontalBarChart
	
	def updateHorizontalBarChart(self, res):
		# Round predictions
		predictions = res['predictions']
		for i in range(len(predictions)):
			predictions[i] = round(predictions[i]*100, 2)
		
		print(predictions)

		data = QtCharts.QBarSet("Confidence")
		data.append(predictions)
		self.chart_data.clear()
		self.chart_data.append(data)
		
		if self.check_chart_displayed == False:
			self.axisY = QtCharts.QBarCategoryAxis()
			self.axisY.append(res['signalNames'])
			self.chart.addAxis(self.axisY, QtCore.Qt.AlignLeft)
			self.chart_data.attachAxis(self.axisY)
			self.check_chart_displayed = True

			self.axisX = QtCharts.QValueAxis()
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
		predictions = predict_post('http://localhost:3000/predict', data)
		print(predictions)

		# Update stuff here
		self.graphData.emit(predictions)
		self.finished.emit()
	
	@QtCore.Slot()
	def runBatteryCheck(self):
		batt = getBatteryStatus()
		self.finished.emit(batt)