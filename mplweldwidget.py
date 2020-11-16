from PyQt5.QtWidgets import*
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

class MplWeldWidget(QWidget):

    def __init__(self, parent = None):

        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.canvas.figure.subplots_adjust(left=0.18, right=0.9, bottom=0.16, top=0.9)
        self.setLayout(vertical_layout)