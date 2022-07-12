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

        self.start_time = pg.ptime.time()
        self.times = [0]

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.plotItem.setLabel(axis="left", text=f"{parameter.name} ({parameter.pvunits})")
        self.plot_widget.plotItem.setRange(xRange=[-10,0])
        self.curve = self.plot_widget.plotItem.plot(x=self.times, y=self.parameter.values, clear=True)

        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.plot_widget, 0, 0)
        

    # ------------------------------------------------------------------------------

    def update(self):
        now = pg.ptime.time()
        self.times.append(now - self.start_time)
        self.curve.setData(x=self.times, y=self.parameter.values, clear=True)
        self.curve.setPos(-(now - self.start_time), 0)


# ==================================================================================

        