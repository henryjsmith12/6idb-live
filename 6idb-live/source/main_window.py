from pyqtgraph import QtGui
from pyqtgraph.dockarea import Dock, DockArea

from source.parameter_widget import ParameterWidget

# ==================================================================================

class MainWindow(QtGui.QWidget):
    """
    Window holding DockArea for GUI.
    """    

    def __init__ (self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Window attributes
        self.setGeometry(100, 100, 1024, 768)
        self.setWindowTitle("6-ID-B Live")

        # Widgets
        self.parameter_widget = ParameterWidget(parent=self)

        # Test Parameters
        self.parameter_widget.addParameter("Delta", "6idb1:m18.RBV")
        self.parameter_widget.addParameter("Eta", "6idb1:m17.RBV")

        # Docks
        self.dock_area = DockArea(parent=self)
        self.parameter_dock = Dock(
            name="Parameters",
            hideTitle=True,
            widget=self.parameter_widget,
            size=(100,300)
        )
        self.plot_dock = Dock(
            name="Plotting",
            hideTitle=True,
            widget=None,
            size=(200,300)
        )
        self.dock_area.addDock(self.parameter_dock)
        self.dock_area.addDock(self.plot_dock, "left", self.parameter_dock)

        # Layout
        self.layout = QtGui.QVBoxLayout()
        self.layout.addWidget(self.dock_area)
        self.setLayout(self.layout)

# ==================================================================================