from widgets.alocatMange.transferManage import Widget_Transfer_Manage
import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget
from sysManage.alocatMange.armyTransfer import armyTransfer
#new
class transferManage(QMainWindow, Widget_Transfer_Manage):
    def __init__(self, parent=None):
        super(transferManage, self).__init__(parent)
        self.setupUi(self)

        self.armyTransfer = armyTransfer()

        self.sw_manageWIdget.addWidget(self.armyTransfer)
        self.tb_armyTransfer.setDisabled(True)
        self.sw_manageWIdget.setCurrentIndex(0)
