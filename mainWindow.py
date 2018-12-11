from __future__ import unicode_literals
import sys
import os
import numpy as np
import matplotlib
from calculateFunction import *
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets, QtGui
from guiWindow import *
from numpy import arange, sin, pi, array
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random


class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=8, height=6, dpi=100):
        fig = plt.figure(1, figsize=(width, height))
        plt.subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)

    def update_figure(self, size, listData=0):
        red = random.random()
        green = random.random()
        blue = random.random()

        color = np.array([red, green, blue])
        if listData:
            plt.plot(listData.keys(), listData.values(), color=color)
        plt.xlim(size['A'], size['B'])
        plt.ylim(size['C'], size['D'])
        self.draw()

    def clear(self):
        plt.cla()
        self.draw()


def setValid(self):
    regex = QtGui.QRegExpValidator(QtCore.QRegExp("^-(0.\d+)$|^(0)(\.\d+)?$|^-?[1-9](\.\d+)?$|^-?[1-9]\d(\.\d+)?$|^-?100&"), self)
    self.ui.alpha.setValidator(regex)
    self.ui.betta.setValidator(regex)
    self.ui.k.setValidator(regex)
    self.ui.epsilon.setValidator(regex)
    self.ui.delta.setValidator(regex)
    self.ui.axesA.setValidator(regex)
    self.ui.axesB.setValidator(regex)
    self.ui.axesC.setValidator(regex)
    self.ui.axesD.setValidator(regex)
    self.ui.tau.setValidator(regex)


def showWarningMessage(w, text):
    pass


class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        setValid(self)
        self.ui.graphicsView.item = MyDynamicMplCanvas(self.ui.graphicsView, width=8.8, height=6.3, dpi=100)
        self.ui.graphicsView.item.mpl_connect('button_press_event', self.onclick)
        self.ui.pushButton.clicked.connect(self.prepareData)

        self.prepareData()

    def onclick(self, event):
        ix, iy = event.xdata, event.ydata
        if ix == None or iy == None:
            return
        self.findFunction(ix, iy)

    def findFunction(self, ix, iy):
        x0, y0 = ix, iy
        dictionaryFuture = {ix: iy}
        dictionaryBack = {ix: iy}
        for i in range(self.coefN):
            ix = ix + self.step * findPoint(ix, iy, self.system['x'])
            iy = iy + self.step * findPoint(ix, iy, self.system['y'])
            dictionaryFuture[ix] = iy
        print(ix, iy)
        ix, iy = x0, y0
        for i in range(self.coefN):
            ix = ix - self.step * findPoint(ix, iy, self.system['x'])
            iy = iy - self.step * findPoint(ix, iy, self.system['y'])
            dictionaryBack[ix] = iy
        print(ix, iy)
        self.ui.graphicsView.item.update_figure(self.size, dictionaryFuture)
        self.ui.graphicsView.item.update_figure(self.size, dictionaryBack)


        # print(ix, iy)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Enter or str(event.key()) == '16777220':
            self.prepareData()

    def prepareData(self):
        self.system = {}
        self.system['x'] = 'α*x+β*y*y+k*x*x+φ'
        self.system['y'] = 'δ*x*x+ε*y+ρ*x+ψ'

        self.system['x'] = self.setFunctionX(self.system['x'])
        self.system['y'] = self.setFunctionY(self.system['y'])

        self.step = float(self.ui.tau.text() or 0.01)
        try:
            self.coefN = int(self.ui.coef_n.text())
        except ValueError:
            self.coefN = 5
        try:
            self.size = {'A': float(self.ui.axesA.text() or -5), 'B': float(self.ui.axesB.text() or -1),
                               'C': float(self.ui.axesC.text() or -2), 'D': float(self.ui.axesD.text() or 5)}
        except ValueError:
            self.size = {'A': -10, 'B': 10, 'C': -10, 'D': 10}
        self.setInputValue(self.size, self.coefN)
        self.ui.graphicsView.item.clear()
        self.ui.graphicsView.item.update_figure(self.size)


    def setFunctionX(self, functionSource):
        func = functionSource.replace('α', self.ui.alpha.text() or '10')
        func = func.replace('β', self.ui.betta.text() or '10')
        func = func.replace('k', self.ui.k.text() or '1')
        func = func.replace('φ', self.ui.fi.text() or '1')
        return func

    def setFunctionY(self, functionSource):
        func = functionSource.replace('δ', self.ui.delta.text() or '1')
        func = func.replace('ε', self.ui.epsilon.text() or '1')
        func = func.replace('ρ', self.ui.ro.text() or '1')
        func = func.replace('ψ', self.ui.psi.text() or '1')
        return func

    def setInputValue(self, size, N):
        self.ui.axesA.setText(str(size['A']))
        self.ui.axesB.setText(str(size['B']))
        self.ui.axesC.setText(str(size['C']))
        self.ui.axesD.setText(str(size['D']))
        self.ui.coef_n.setText(str(N))
        self.ui.alpha.setText(self.ui.alpha.text() or '10')
        self.ui.betta.setText(self.ui.betta.text() or '10')
        self.ui.k.setText(self.ui.k.text() or '1')
        self.ui.fi.setText(self.ui.fi.text() or '1')
        self.ui.delta.setText(self.ui.delta.text() or '1')
        self.ui.epsilon.setText(self.ui.epsilon.text() or '1')
        self.ui.ro.setText(self.ui.ro.text() or '1')
        self.ui.psi.setText(self.ui.psi.text() or '1')
        self.ui.tau.setText(self.ui.tau.text() or '0.01')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    # prepareDate()
    sys.exit(app.exec_())
