import numpy as np
from pyqtgraph import QtGui, QtCore

from source.parameter_widget import Parameter

# ==================================================================================

class ImageWidget(QtGui.QWidget):

    def __init__(self, parameter : Parameter) -> None:
        super(ImageWidget, self).__init__()

# ==================================================================================

class LinePlotWidget(QtGui.QWidget):

    def __init__(self, parameter : Parameter) -> None:
        super(LinePlotWidget, self).__init__()