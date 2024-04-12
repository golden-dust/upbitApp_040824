import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

form_class = uic.loadUiType("ui/comboBoxTest.ui")[0]

class MainWin(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.comboBox_setting()
        self.comboBox.currentIndexChanged.connect(self.comboBox_selected)

    def comboBox_setting(self):
        menulist = ['SELECT A DAY', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        self.comboBox.addItems(menulist)

    def comboBox_selected(self):
        selected = self.comboBox.currentText()
        self.outputLabel.setText(selected)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWin()
    win.show()
    app.exit(app.exec_())