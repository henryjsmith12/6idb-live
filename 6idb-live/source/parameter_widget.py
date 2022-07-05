import epics
import numpy as np
from pyqtgraph import QtGui, QtCore
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
        self.parameter_tree = ParameterTree(showHeader=False)

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
        self.add_parameter_btn.clicked.connect(self.add_parameter)

    # ------------------------------------------------------------------------------

    def add_parameter(self):
        """
        Creates a Parameter object from user provided information
        """
        
        display_name = self.parameter_name_txt.text()
        pvname = self.parameter_pvname_txt.text()

        try:
            pv = epics.PV(pvname)
            if pv.connect():
                if type(pv.value) in [int, float]:
                    parameter = PrimitiveParameter(
                        display_name=display_name, 
                        pvname=pvname
                    )
                elif type(pv.value) == np.ndarray:
                    parameter = ImageParameter(
                        display_name=display_name, 
                        pvname=pvname
                    )
                else:
                    return
                
                # Adds parameter to widget
                self.parameter_tree.addParameters(parameter)

                # Resets text to add another parameter
                self.parameter_name_txt.setText("")
                self.parameter_pvname_txt.setText("")
                self.parameter_connected_lbl.setText("")
            else:
                self.parameter_connected_lbl.setText("Not Connected")
                self.parameter_connected_lbl.setStyleSheet("color: red")
        except:
            pass
            
# ==================================================================================

class PrimitiveParameter(SimpleParameter):
    """
    Parameter object for primitive types. Takes information from given PV.
    """

    def __init__(self, display_name : str, pvname : str) -> None:
        self.display_name = display_name
        self.pv = epics.PV(pvname)
        self.pvname = pvname
        self.pvtype = type(self.pv.value)
        
        if self.pvtype == float:
            str_type = "float"
        elif self.pvtype == int:
            str_type = "int"
        else:
            str_type = "str"

        super(PrimitiveParameter, self).__init__(
            name=display_name,
            value=self.pv.value,
            type=str_type,
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

    # ------------------------------------------------------------------------------

    def mouseMoveEvent(self, e):

        if e.buttons() == QtCore.Qt.LeftButton:
            drag = QtGui.QDrag(self)
            mime = QtCore.QMimeData()
            drag.setMimeData(mime)
            drag.exec_(QtCore.Qt.MoveAction)

# ==================================================================================

class ImageParameter(SimpleParameter):
    """
    Parameter object for a NumPy array.
    """
    
    def __init__(self, display_name : str, pvname : str) -> None:
        self.display_name = display_name
        self.pv = epics.PV(pvname)
        self.pvname = pvname
        self.image_array = self.pv.value
        str_value = f"Image: ({self.image_array.shape})"

        super(ImageParameter, self).__init__(
            name=display_name,
            value=str_value,
            type="str",
            readonly=True
        )

        epics.camonitor(pvname, callback=self.updateValue)

    # ------------------------------------------------------------------------------

    def updateValue(self, pvname=None, value=None, **kwargs):
        """
        Updates value as seen in the GUI
        """

        self.image_array = value

# ==================================================================================
        
        
        

        
