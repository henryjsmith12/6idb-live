import pyqtgraph as pg
from pyqtgraph import QtGui
from pyqtgraph.dockarea import Dock, DockArea

from source.parameters import ParameterWidget

# ==================================================================================

class MainWindow(QtGui.QWidget):
    
    def __init__ (self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Window attributes
        self.setGeometry(100, 100, 1024, 768)
        self.setWindowTitle("6-ID-B Live")

        # Widgets
        self.parameter_widget = ParameterWidget()

        # Docks
        self.dock_area = DockArea(parent=self)
        self.parameter_dock = Dock(
            name="Parameters",
            hideTitle=True,
            widget=self.parameter_widget,
            size=(100,300)
        )
        self.spotlight_dock = Dock(
            name="Spotlight",
            hideTitle=True,
            widget=None,
            size=(200,300)
        )
        self.dock_area.addDock(self.parameter_dock)
        self.dock_area.addDock(self.spotlight_dock, "left", self.parameter_dock)

        # LAYOUT -------------------------------------------------------------------
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.dock_area)
        self.setLayout(self.layout)

# ==================================================================================