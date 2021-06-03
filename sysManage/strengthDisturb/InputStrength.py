from widgets.strengthDisturb.inputStrength import widget_inputStrength
from PyQt5.QtWidgets import QWidget,QDialog
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox,QPushButton
from database.alocatMangeSql import updateDisturbPlanProof


class InputStrength(QDialog,widget_inputStrength):
    signal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(InputStrength, self).__init__(parent)
        self.setupUi(self)
        self.NewStrength = None
        # self.currentYear = ''
        self.signalConnect()


    def signalConnect(self):
        self.pb_yes.clicked.connect(self.inputText)
        self.pb_cancel.clicked.connect(self.close)


    # def setYear(self, year):
    #     self.currentYear = year


    def inputText(self):
        if self.le_inputText.text() == '':
            messageBox = QMessageBox()
            messageBox.setWindowTitle('提示')
            messageBox.setText('请输入新实力数')
            messageBox.addButton(QPushButton('确定'), QMessageBox.YesRole)
            messageBox.exec_()
        else:
            self.NewStrength = self.le_inputText.text()
            self.close()
            self.signal.emit('1')