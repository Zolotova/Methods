from __future__ import unicode_literals
import sys
import os
import random
import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""

    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)


class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.cla()
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.main_widget = QtWidgets.QWidget(self)

        l = QtWidgets.QVBoxLayout(self.main_widget)
        sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        dc = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        l.addWidget(sc)
        l.addWidget(dc)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("All hail matplotlib!", 2000)


class MainWindow(QtWidgets):

    def __init__(self):
        super().__init__()
        self.initUI()
        # prepare figure
        self.figure = Figure()
        self.axes = self.figure.add_subplot( 111 )
        self.canvas = FigureCanvas( self.figure )
        self.layoutPlot.addWidget( self.canvas )

    def plot(self):
        vb = pg.ViewBox()
        self.graphicsView.setCentralItem(vb)

    def initUI(self):
        k = 0
        for i in 'αβγδε':
            self.initCoeff(i, 20 + k)
            k += 30
        self.setGeometry(300, 100, 600, 600)
        self.setWindowTitle('Review')
        self.show()

    def initCoeff(self, name, coordY, control=1):
        label = QLabel(self)
        label.move(20, coordY)
        label.setText(name + ': ')
        self.qle = QLineEdit(self)
        self.qle.setFixedWidth(25)
        self.qle.textChanged[str].connect(self.onChanged)
        self.qle.setInputMask('#999')
        self.qle.move(40, coordY)

    def onChanged(self, text):
        if text:
            if not text[0].isdigit():
                text = text[1:]
            if int(text) > 100:
                self.qle.setText('100')
            if int(text) < -100:
                self.qle.setText('-100')


if __name__ == '__main__':
    qApp = QtWidgets.QApplication(sys.argv)

    aw = ApplicationWindow()
    aw.show()
    sys.exit(qApp.exec_())
