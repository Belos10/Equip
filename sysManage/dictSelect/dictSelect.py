from widgets.strengthDisturb.StrengthDisturb import Strength_Disturb_Widget
import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget
from widgets.dictSelect.dictSelect import Widget_Dict_Select
#new
class dictSelect(QMainWindow, Widget_Dict_Select):
    def __init__(self, parent=None):
        super(dictSelect, self).__init__(parent)
        self.setupUi(self)

        self.equipHandbook = QWidget(self)
        self.factoryDict = QWidget(self)
        self.presentRoom = QWidget(self)
        self.regularManage = QWidget(self)

        self.sw_dictSelectMange.addWidget(self.equipHandbook)
        self.sw_dictSelectMange.addWidget(self.factoryDict)
        self.sw_dictSelectMange.addWidget(self.presentRoom)
        self.sw_dictSelectMange.addWidget(self.regularManage)

        self.sw_dictSelectMange.setCurrentIndex(0)
        self.tb_equipHandbook.setDisabled(True)
        self.tb_factoryDict.setDisabled(False)
        self.tb_presentRoom.setDisabled(False)
        self.tb_regularManage.setDisabled(False)
        self.connectSignal()

    def connectSignal(self):
        self.tb_equipHandbook.clicked.connect(self.slotEquipHandbook)
        self.tb_factoryDict.clicked.connect(self.slotFactoryDict)
        self.tb_presentRoom.clicked.connect(self.slotPresentRoom)
        self.tb_regularManage.clicked.connect(self.slotRegularManage)

    def slotDisconnect(self):
        self.tb_equipHandbook.clicked.disconnect(self.slotEquipHandbook)
        self.tb_factoryDict.clicked.disconnect(self.slotFactoryDict)
        self.tb_presentRoom.clicked.disconnect(self.slotPresentRoom)
        self.tb_regularManage.clicked.disconnect(self.slotRegularManage)

    def slotEquipHandbook(self):
        self.sw_dictSelectMange.setCurrentIndex(0)
        self.tb_equipHandbook.setDisabled(True)
        self.tb_factoryDict.setDisabled(False)
        self.tb_presentRoom.setDisabled(False)
        self.tb_regularManage.setDisabled(False)

    def slotFactoryDict(self):
        self.sw_dictSelectMange.setCurrentIndex(1)
        self.tb_equipHandbook.setDisabled(False)
        self.tb_factoryDict.setDisabled(True)
        self.tb_presentRoom.setDisabled(False)
        self.tb_regularManage.setDisabled(False)

    def slotPresentRoom(self):
        self.sw_dictSelectMange.setCurrentIndex(2)
        self.tb_equipHandbook.setDisabled(False)
        self.tb_factoryDict.setDisabled(False)
        self.tb_presentRoom.setDisabled(True)
        self.tb_regularManage.setDisabled(False)

    def slotRegularManage(self):
        self.sw_dictSelectMange.setCurrentIndex(3)
        self.tb_equipHandbook.setDisabled(False)
        self.tb_factoryDict.setDisabled(False)
        self.tb_presentRoom.setDisabled(False)
        self.tb_regularManage.setDisabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = dictSelect()
    widget.show()
    sys.exit(app.exec_())