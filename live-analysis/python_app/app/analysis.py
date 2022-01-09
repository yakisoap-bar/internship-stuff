from PySide6 import QtCore, QtWidgets, QtGui

from Functions.Collect import *
from Functions.Request import *
from Functions.Status import *

class AnalysisWindow(QtWidgets.QWidget):
	def __init__(self) -> None:
		super().__init__()

		# Threading stuff
		self.analysis_thread = QtCore.QThread()

		self.configs()

	def configs(self):
		# App config things
		screen_size = self.getScreenRes()
		# self.setGeometry(0, 0, screen_size.width(), screen_size.height())
		self.window_title = "Live Classification"
		self.setWindowTitle(self.window_title)
		self.setWindowIcon(QtGui.QIcon('./img/icon.png'))

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
		self.worker.finished.connect(self.runAnalysisRecursion)

	def runAnalysisRecursion(self):
		self.analysis_thread.quit()
		self.worker.deleteLater()
		if self.run_analysis_btn_check:
			self.runAnalysisThread()
	

class Worker(QtCore.QObject):
	started = QtCore.Signal()
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
		print(predictions)
		self.finished.emit()