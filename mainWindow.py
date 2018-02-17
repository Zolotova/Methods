import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,
                             QTextEdit, QGridLayout, QApplication)


class mainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        k = 0
        for i in 'αβγδε':
            self.initCoeff(i, 20 + k)
            k += 30
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Review')
        self.show()

    def initCoeff(self, name, coordY, control=1):
        label = QLabel(self)
        label.move(20, coordY)
        label.setText(name + ': ')
        self.qle = QLineEdit(self)
        self.qle.setFixedWidth(25)
        self.qle.textChanged[str].connect(self.onChanged)
        self.qle.setInputMask('#000')
        self.qle.move(40, coordY)

    def onChanged(self, text):
        if text:
            if int(text) > 100:
                self.qle.setText('100')
            if int(text) < -100:
                self.qle.setText('-100')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mainWindow()
    sys.exit(app.exec_())
