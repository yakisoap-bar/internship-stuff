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
		self.initPieChart()
		self.chart = QtCharts.QChart()
		self.chart.setTitle('Predictions')
		self.chart.addSeries(self.chart_data)
		self.chart.legend().setVisible(True)

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
		self.analysis_thread.started.connect(self.worker.run)
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

		self.updateChart = self.updateHorizontalBarChart
	
	def updateHorizontalBarChart(self, res):
		for i in range(0, len(res['signalNames'])):
			data = QtCharts.QBarSet(str(i))
			data.append(res['predictions'][i])
			self.chart_data.append(data)
		
		self.axisY = QtCharts.QBarCategoryAxis()
		self.axisY.append(res['signalNames'])
		self.chart.addAxis(self.axisY, QtCore.Qt.QtAlignLeft)
		self.chart_data.attachAxis(self.axisY)
		
		self.axisX = QtCharts.QValueAxis()
		self.chart.addAxis(self.axisX, QtCore.Qt.QtAlignBottom)
		self.chart_data.attachAxis(self.axisX)

		self.chart.legend().setAlignment(QtCore.Qt.AlignLeft)

class Worker(QtCore.QObject):
	started = QtCore.Signal()
	graphData = QtCore.Signal(object)
	finished = QtCore.Signal()

	def __init__(self, params) -> None:
		super().__init__()
		self.params = params

	@QtCore.Slot()
	def run(self):
		self.started.emit()
		# Predict
		config_block_iq(self.params['cf'], self.params['ref_level'], self.params['bandwidth'], 1024)
		data = acquire_block_iq(1024, self.params["num_records"])
		predictions = predict_post('http://localhost:3000/predict', data)

		# Update stuff here
		self.graphData.emit(predictions)
		self.finished.emit()