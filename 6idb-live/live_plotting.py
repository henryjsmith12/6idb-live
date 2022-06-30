import pyqtgraph as pg

from source.main_window import MainWindow

# ==================================================================================

app = pg.mkQApp("6-ID-B Live")
window = MainWindow()
window.show()
pg.mkQApp().exec_()

# ==================================================================================