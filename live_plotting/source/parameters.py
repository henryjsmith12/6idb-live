import epics
import pyqtgraph as pg
from pyqtgraph import QtGui
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem

# ==================================================================================

class ParameterWidget(QtGui.QWidget):
    
    def __init__(self, parent=None) -> None:
        super(ParameterWidget, self).__init__(parent)

        # Parameters
        self.add_parameter = Parameter.create(
            name="add",
            title="+",
            type="action"
        )
        self.parameters = [self.add_parameter]
        self.paramter_group = Parameter.create(
            name="PV Parameters", 
            type="group", 
            children=self.parameters
        )

        # Parameter Tree
        self.parameter_tree = ParameterTree()
        self.parameter_tree.setParameters(self.paramter_group, showTop=False)

        # Layout
        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.parameter_tree)

        # Signals
        self.add_parameter.sigStateChanged.connect(self.create_parameter)

    # ------------------------------------------------------------------------------

    def create_parameter(self):
        dialog = CreateParameterDialog()
        dialog.exec_()

# ==================================================================================

class PVParameter(Parameter):

    def __init__(self, parent=None) -> None:
        super(PVParameter, self).__init__(parent)

# ==================================================================================

class CreateParameterDialog(QtGui.QDialog):
    
    def __init__(self) -> None:
        super(CreateParameterDialog, self).__init__()

        # Widgets
        self.pvname_lbl = QtGui.QLabel("PV Name: ")
        self.pvname_txt = QtGui.QLineEdit()
        self.add_btn = QtGui.QPushButton("Add")
        self.add_btn.setDefault(True)
        self.cancel_btn = QtGui.QPushButton("Cancel")
        self.cancel_btn.setDefault(False)

        # Layout
        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.pvname_lbl, 0, 0, 1, 2)
        self.layout.addWidget(self.pvname_txt, 0, 2, 1, 4)
        self.layout.addWidget(self.add_btn, 1, 4, 1, 1)
        self.layout.addWidget(self.cancel_btn, 1, 5, 1, 1)

        # Signals

# ==================================================================================