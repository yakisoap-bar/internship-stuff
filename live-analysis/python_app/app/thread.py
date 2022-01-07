from PySide6 import QtCore

class WorkerSignals(QtCore.QObject):
	finished = QtCore.Signal()
	error = QtCore.Signal(tuple)
	result = QtCore.Signal(object)
	progress = QtCore.Signal(int)

class Worker(QtCore.QRunnable):
	def __init__(self, fn, *args, **kwargs) -> None:
		super(Worker, self).__init__()
		self.fn = fn
		self.args = args
		self.kwargs = kwargs
		self.signals = WorkerSignals()
		self.kwargs['progress_callback'] = self.signals.progress

	@QtCore.Slot()
	def run(self):
		try:
			result = self.fn(*self.args, **self.kwargs)
		except:
			traceback.print_exc()
			exctype, value = sys.exc_info()[:2]
			self.signals.error.emit((exctype, value, traceback.format_exc()))
		else:
			self.signals.result.emit(result)
		finally:
			self.signals.finished.emit()