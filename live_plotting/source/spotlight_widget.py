from pyqtgraph import QtGui

from source.parameter_widget import Parameter

# ==================================================================================

class SpotlightWidget(QtGui.QWidget):
    """
    Widget to display parameter details in the spotlight dock.
    """

    def __init__(self, parameter : Parameter, parent=None) -> None:
        super(SpotlightWidget, self).__init__(parent)

        self.parameter = parameter