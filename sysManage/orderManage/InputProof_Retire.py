from widgets.alocatMange.inputProof import widget_inputProof
from PyQt5.QtWidgets import QWidget,QDialog
from PyQt5 import QtCore
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QMessageBox,QPushButton
from database.OrderManageSql import updateOrderRetirePlanProof


class InputProof(QDialog,widget_inputProof):
    signal = QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(InputProof, self).__init__(parent)
        self.setupUi(self)
        self.currentYear = ''
        self.setWindowTitle("设置调拨依据")
        self.setWindowFlags(Qt.WindowTitleHint | Qt.CustomizeWindowHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint|Qt.Dialog)
        self.signalConnect()


    def signalConnect(self):
        self.pb_yes.clicked.connect(self.inputText)
        self.pb_cancel.clicked.connect(self.close)


    def setYear(self, year):
        self.currentYear = year


    def inputText(self):
        if self.le_inputText.text() == '':
            messageBox = QMessageBox()
            messageBox.setWindowTitle('提示')
            messageBox.setText('请输入调拨依据')
            messageBox.addButton(QPushButton('确定'), QMessageBox.YesRole)
            messageBox.exec_()
        else:
            updateOrderRetirePlanProof(self.currentYear, self.le_inputText.text())
            self.close()
            self.signal.emit('1')