# Cool analysis stuff goes here
import sys, threading
from PySide6 import QtCore, QtWidgets, QtGui

# Interacting with the SDR
from Functions.Collect import *
from Functions.Request import *
from Functions.Status import *

class Window(QtWidgets.QWidget):
	def __init__(self) -> None:
		super().__init__()
		# Declare global vars here
		self.mainLayout = QtWidgets.QGridLayout
		self.sideBarLayout = QtWidgets.QVBoxLayout()
		self.configLayout = QtWidgets.QVBoxLayout()

		self.configs()
		self.buttons()
		self.appLayout()
		self.show()
		self.startAnalysis()
	
	@QtCore.Slot()
	def configs(self):
		# App config things
		screen_size = self.getScreenRes()
		self.setGeometry(0, 0, screen_size.width(), screen_size.height())
		self.window_title = "Live Classification"
		self.setWindowTitle(self.window_title)
		self.setWindowIcon(QtGui.QIcon('./img/icon.png'))
	
	def appLayout(self):
		self.menuToolbar()
		self.sideBarLayout.addLayout(self.configLayout)

		container = QtWidgets.QWidget()
		container.setLayout(self.sideBarLayout)
		self.setCentralWidget(container)

	def buttons(self):
		# Stick all buttons here
		self.btnRunAnalysis()
		self.btnShowConfigs()
		self.configCenterFreq()
		self.configBandwidth()
		self.configRefLvl()
		self.configSamplingFreq()

		self.config_buttons = [
			self.center_freq_label,
			self.center_freq_input,
			self.center_freq_dropdown,
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
	
	def contextMenuEvent(self, e):
		context = QtWidgets.QMenu(self)
		context.addAction(QtGui.QAction("Test 1", self))
		context.addAction(QtGui.QAction("Test 2", self))
		context.addAction(QtGui.QAction("Test 3", self))
		context.exec_(e.globalPos())