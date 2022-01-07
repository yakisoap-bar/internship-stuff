from PySide6 import QtCore, QtWidgets

from Functions.Collect import *
from Functions.Request import *
from Functions.Status import *

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