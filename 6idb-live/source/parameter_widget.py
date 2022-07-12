import epics
import numpy as np
import pyqtgraph as pg
from pyqtgraph import QtGui, QtCore 

# ==================================================================================

class ParameterWidget(QtGui.QWidget):
    """
    Houses parameters and allows users to add new parameters.
    """

    def __init__(self, parent) -> None:
        super(ParameterWidget, self).__init__(parent)

        self.parent = parent

        # Widgets
        self.parameter_name_lbl = QtGui.QLabel("Display Name:")
        self.parameter_name_txt = QtGui.QLineEdit()
        self.parameter_name_txt.setPlaceholderText("Delta")
        self.parameter_pvname_lbl = QtGui.QLabel("PV Name:")
        self.parameter_pvname_txt = QtGui.QLineEdit()
        self.parameter_pvname_txt.setPlaceholderText("XXX:XX.XXX")
        self.parameter_connected_lbl = QtGui.QLabel()
        self.add_parameter_btn = QtGui.QPushButton("Add Parameter")
        self.add_parameter_btn.setAutoDefault(True)
        self.add_list_btn = QtGui.QPushButton("Add List")
        self.add_template_btn = QtGui.QPushButton("Add Template")
        self.parameter_tree = QtGui.QTreeWidget()
        self.parameter_tree.setColumnCount(3)
        self.parameter_tree.setHeaderLabels(["Name", "Value", "Units"])

        # Layout
        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.parameter_name_lbl, 0, 0, 1, 2)
        self.layout.addWidget(self.parameter_name_txt, 0, 2, 1, 4)
        self.layout.addWidget(self.parameter_pvname_lbl, 1, 0, 1, 2)
        self.layout.addWidget(self.parameter_pvname_txt, 1, 2, 1, 4)
        self.layout.addWidget(self.parameter_connected_lbl, 2, 0, 1, 2)
        self.layout.addWidget(self.add_parameter_btn, 2, 2, 1, 4)
        self.layout.addWidget(self.add_list_btn, 3, 0, 1, 3)
        self.layout.addWidget(self.add_template_btn, 3, 3, 1, 3)
        self.layout.addWidget(self.parameter_tree, 4, 0, 1, 6)

        # Signals
        self.add_parameter_btn.clicked.connect(self.addParameter)
        self.parameter_tree.itemDoubleClicked.connect(self.plotParameter)

    # ------------------------------------------------------------------------------

    def addParameter(self, name=None, pvname=None):
        """
        Creates a Parameter object from user provided information
        """
        if name is None or pvname is None:
            name = self.parameter_name_txt.text()
            pvname = self.parameter_pvname_txt.text()

        pv = epics.PV(pvname)
        if pv.connect():
            if type(pv.value) in [int, float]:
                parameter = Parameter(
                    name=name, 
                    pvname=pvname,
                    parent=self
                )
            else:
                return
            
            # Adds parameter to widget
            self.parameter_tree.addTopLevelItem(parameter)

            # Resets text to add another parameter
            self.parameter_name_txt.setText("")
            self.parameter_pvname_txt.setText("")
            self.parameter_connected_lbl.setText("")
        else:
            self.parameter_connected_lbl.setText("Not Connected")
            self.parameter_connected_lbl.setStyleSheet("color: red")

    # ------------------------------------------------------------------------------

    def plotParameter(self, parameter):

        from source.plot_widget import ImageWidget, LinePlotWidget 

        if parameter.pvtype in [int, float] and parameter.plot_widget == None:
            self.parent.plot_dock.addWidget(LinePlotWidget(parameter))
            
# ==================================================================================

class Parameter(QtGui.QTreeWidgetItem):

    def __init__(self, name : str, pvname : str, parent) -> None:
        super(Parameter, self).__init__()

        self.parent = parent

        self.name = name
        self.pvname = pvname
        self.pv = epics.PV(pvname)
        self.pvtype = type(self.pv.value)
        self.pvunits = self.pv.units
        self.values = [self.pv.value]
        self.plot_widget = None

        self.setText(0, str(self.name))
        self.setText(1, str(self.pv.value))
        self.setText(2, str(self.pv.units))

        epics.camonitor(pvname, callback=self.updateValue)

    # ------------------------------------------------------------------------------

    def updateValue(self, pvname=None, value=None, **kwargs):
        """
        Updates value as seen in the GUI
        """
        
        self.values.append(value)
        self.setText(1, str(self.pv.value))
        if self.plot_widget is not None:
            self.plot_widget.update()
        self.parent.parameter_tree.viewport().update()

# ==================================================================================

