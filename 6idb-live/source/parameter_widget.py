import epics
from pyqtgraph import QtGui
from pyqtgraph.parametertree import ParameterTree
from pyqtgraph.parametertree.parameterTypes import SimpleParameter

# ==================================================================================

class ParameterWidget(QtGui.QWidget):
    """
    Houses parameters and allows users to add new parameters.
    """

    def __init__(self, parent=None) -> None:
        super(ParameterWidget, self).__init__(parent)

        # Widgets
        self.add_parameter_btn = QtGui.QPushButton("Add Parameter")
        self.parameter_tree = ParameterTree(showHeader=False)

        # Layout
        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.add_parameter_btn, 0, 0)
        self.layout.addWidget(self.parameter_tree, 1, 0, 1, 2)

        # Signals
        self.add_parameter_btn.clicked.connect(self.add_parameter)

    # ------------------------------------------------------------------------------

    def add_parameter(self):
        """
        Opens dialog to add new parameter and creates parameter.
        """

        dialog = AddParameterDialog()
        dialog.exec_()

        # Checks if dialog was accepted (with valid PV)
        if dialog != QtGui.QDialogButtonBox.Ok:

            # Creates parameter from PV name provided
            parameter = Parameter(
                display_name=dialog.display_name, 
                pvname=dialog.pvname
            )

            # Adds parameter to widget
            self.parameter_tree.addParameters(parameter)

            #parameter.sigStateChanged.connect()
            
# ==================================================================================

class AddParameterDialog(QtGui.QDialog):
    """
    Dialog that allows user to enter parameter information. Only valid PV names are 
    accepted.
    """

    def __init__(self) -> None:
        super(AddParameterDialog, self).__init__()

        self.setModal(False)
        self.connected = False
        self.display_name = None
        self.pvname = None

        # Widgets
        self.display_name_lbl = QtGui.QLabel("Display Name:")
        self.display_name_txt = QtGui.QLineEdit()
        self.display_name_txt.setPlaceholderText("Delta")
        self.pvname_lbl = QtGui.QLabel("PV Name:")
        self.pvname_txt = QtGui.QLineEdit()
        self.pvname_txt.setPlaceholderText("XXX:XX.XXX")
        self.connected_lbl = QtGui.QLabel()
        self.dialog_btns = QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok
        self.dialog_btn_box = QtGui.QDialogButtonBox(self.dialog_btns)
        self.dialog_btn_box.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)

        # Layout
        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.display_name_lbl, 0, 0)
        self.layout.addWidget(self.display_name_txt, 0, 1)
        self.layout.addWidget(self.pvname_lbl, 1, 0)
        self.layout.addWidget(self.pvname_txt, 1, 1)
        self.layout.addWidget(self.connected_lbl, 2, 0)
        self.layout.addWidget(self.dialog_btn_box, 2, 1)
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 1)

        # Signals
        self.pvname_txt.editingFinished.connect(self.validatePV)
        self.dialog_btn_box.accepted.connect(self.accept)
        self.dialog_btn_box.rejected.connect(self.reject)
        
    # ------------------------------------------------------------------------------

    def validatePV(self):
        """
        Validates given PV name.
        """

        pvname = self.pvname_txt.text()

        # Creates an EPICS PV from given PV name
        pv = epics.PV(pvname)

        # Checks if PV is valid
        if pv.connect():
            self.connected = True
            self.display_name = self.display_name_txt.text()
            self.pvname = pvname
            self.connected_lbl.setText("Connected")
            self.connected_lbl.setStyleSheet("color: green")
            self.dialog_btn_box.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.connected = False
            self.connected_lbl.setText("Not Connected")
            self.connected_lbl.setStyleSheet("color: red")
            self.dialog_btn_box.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)

# ==================================================================================

class Parameter(SimpleParameter):
    """
    Parameter object for primitive types. Takes information from given PV.
    """

    def __init__(self, display_name : str, pvname : str) -> None:
        self.display_name = display_name
        self.pv = epics.PV(pvname)
        self.pvname = pvname
        
        value = self.pv.value
        if type(value) == float:
            value_type = "float"
        elif type(value) == int:
            value_type = "int"
        elif type(value) == str:
            value_type = "str"
        else:
            value_type = None

        super(Parameter, self).__init__(
            name=display_name,
            value=value,
            type=value_type,
            suffix=self.pv.units,
            readonly=(not self.pv.write_access)
        )

        epics.camonitor(pvname, callback=self.updateValue)
        
    # ------------------------------------------------------------------------------

    def updateValue(self, pvname=None, value=None, **kwargs):
        """
        Updates value as seen in the GUI
        """

        self.setValue(value)

# ==================================================================================


        
        
        

        
