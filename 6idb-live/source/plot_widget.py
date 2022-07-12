import numpy as np
import pyqtgraph as pg
from pyqtgraph import QtGui, QtCore

from source.parameter_widget import Parameter

# ==================================================================================

class ImageWidget(QtGui.QWidget):

    def __init__(self, parameter : Parameter) -> None:
        super(ImageWidget, self).__init__()

        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)

# ==================================================================================

class LinePlotWidget(QtGui.QWidget):

    def __init__(self, parameter : Parameter) -> None:
        super(LinePlotWidget, self).__init__()

        self.parameter = parameter
        self.parameter.plot_widget = self

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.plotItem.setLabel(axis="left", text=f"{parameter.name} ({parameter.pvunits})")
        self.plot_widget.plotItem.setRange(xRange=[-10,0])
        self.curve = self.plot_widget.plotItem.plot(x=self.parameter.times, y=self.parameter.values, clear=True)

        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.plot_widget, 0, 0)

        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)

    # ------------------------------------------------------------------------------

    def update(self):
        
        now = pg.ptime.time()
        self.parameter.times.append(now - self.parameter.start_time)
        self.parameter.values.append(self.parameter.value)

        self.curve.setData(x=self.parameter.times, y=self.parameter.values, clear=True)
        self.curve.setPos(-(self.parameter.times[-1]), 0)


# ==================================================================================

        