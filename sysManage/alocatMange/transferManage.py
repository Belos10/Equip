from widgets.alocatMange.transferManage import Widget_Transfer_Manage
from sysManage.alocatMange.rocketTransfer import rocketTransfer
import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget
from sysManage.alocatMange.armyTransfer import armyTransfer

'''
   调拨单管理界面
'''
class transferManage(QMainWindow, Widget_Transfer_Manage):
    def __init__(self, parent=None):
        super(transferManage, self).__init__(parent)
        self.setupUi(self)

        self.armyTransfer = armyTransfer()
        self.rocketTransfer = rocketTransfer()

        self.sw_manageWIdget.addWidget(self.armyTransfer)
        self.sw_manageWIdget.addWidget(self.rocketTransfer)
        self.tb_armyTransfer.setDisabled(True)
        self.sw_manageWIdget.setCurrentIndex(0)

        self.signalConnect()

    def signalConnect(self):
        self.tb_armyTransfer.clicked.connect(self.slotArmyTransfer)
        self.tb_rocketTransfer.clicked.connect(self.slotRocketTransfer)

    def slotArmyTransfer(self):
        self.tb_armyTransfer.setDisabled(True)
        self.tb_rocketTransfer.setDisabled(False)
        self.sw_manageWIdget.setCurrentIndex(0)

    def slotRocketTransfer(self):
        self.tb_armyTransfer.setDisabled(False)
        self.tb_rocketTransfer.setDisabled(True)
        self.sw_manageWIdget.setCurrentIndex(1)