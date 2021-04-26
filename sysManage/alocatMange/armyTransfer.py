from widgets.alocatMange.armyTransfer import Widget_Army_Transfer
import sys
from PyQt5.QtWidgets import QApplication,QWidget

class armyTransfer(QWidget, Widget_Army_Transfer):
    def __init__(self, parent=None):
        super(armyTransfer, self).__init__(parent)
        self.setupUi(self)

        self.tw_result.horizontalHeader().setVisible(False)
        self.tw_result.verticalHeader().setVisible(False)
        self.tw_result.setColumnCount(19)
        self.tw_result.setRowCount(2)

        self.orginRowCount = 0
        self.tw_result.setSpan(0, 0, 2, 1)
        self.tw_result.setSpan(0, 1, 1, 6)
        self.tw_result.setSpan(0, 7, 1, 3)
        self.tw_result.setSpan(0, 10, 1, 3)
        self.tw_result.setSpan(0, 13, 1, 2)