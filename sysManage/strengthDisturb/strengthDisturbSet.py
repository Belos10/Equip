import sys
from PyQt5.QtWidgets import QMainWindow,QApplication
from widgets.strengthDisturb.strengthDisturbSet import Widget_Strength_Disturb_Set
from sysManage.strengthDisturb.strengthSelectSet import strengthSelectSet
from sysManage.strengthDisturb.maintenManageSet import maintenManageSet
#new
class strengthDisturbSet(QMainWindow, Widget_Strength_Disturb_Set):
    def __init__(self, parent=None):
        super(strengthDisturbSet, self).__init__(parent)
        self.setupUi(self)

        self.strengthSelectSet = strengthSelectSet(self)
        self.maintenManageSet = maintenManageSet(self)

        self.sw_setManage.addWidget(self.strengthSelectSet)
        self.sw_setManage.addWidget(self.maintenManageSet)

        self.signalConnect()
        self.tb_selectSet.setDisabled(True)
        self.tb_maintenManageSet.setDisabled(False)

    def signalConnect(self):
        self.tb_selectSet.clicked.connect(self.slotSelectSet)
        self.tb_maintenManageSet.clicked.connect(self.slotMaintenManageSet)

    def getUserInfo(self, userInfo):
        self.userInfo = userInfo
        self.strengthSelectSet.getUserInfo(self.userInfo)
        self.maintenManageSet.getUserInfo(self.userInfo)

    def disconnectSlot(self):
        self.tb_selectSet.clicked.disconnect(self.slotSelectSet)

    def slotSelectSet(self):
        self.signalConnect()
        self.sw_setManage.setCurrentIndex(0)
        self.disconnectSlot()
        self.tb_selectSet.setDisabled(True)
        self.tb_maintenManageSet.setDisabled(False)

    def slotMaintenManageSet(self):
        self.signalConnect()
        self.sw_setManage.setCurrentIndex(1)
        self.disconnectSlot()
        self.tb_selectSet.setDisabled(False)
        self.tb_maintenManageSet.setDisabled(True)
        self.maintenManageSet._initAll_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = strengthDisturbSet()
    widget.show()
    sys.exit(app.exec_())