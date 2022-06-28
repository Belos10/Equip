from PyQt5 import QtCore
from PyQt5.Qt import QRegExp, QRegExpValidator, Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QMessageBox, QPushButton

from widgets.strengthDisturb.inputStrength import widget_inputStrength

regx = QRegExp("[0-9]*")
class InputStrength(QDialog,widget_inputStrength):
    signal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(InputStrength, self).__init__(parent)
        self.setupUi(self)
        self.NewStrength = None
        # self.setWindowTitle("设置实力数")
        # # self.currentYear = ''
        # self.le_inputText.setValidator(QRegExpValidator(regx))

        validator = QRegExpValidator(regx)
        self.le_inputText.setValidator(validator)
        self.setWindowTitle("修改实力数")
        flags = Qt.Dialog
        flags = flags | Qt.WindowTitleHint | Qt.CustomizeWindowHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint
        self.setWindowFlags(flags)
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