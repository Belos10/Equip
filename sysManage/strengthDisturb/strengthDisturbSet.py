import sys
from PyQt5.QtWidgets import QMainWindow,QApplication
from widgets.strengthDisturb.strengthDisturbSet import Widget_Strength_Disturb_Set
from sysManage.strengthDisturb.strengthSelectSet import strengthSelectSet
from sysManage.strengthDisturb.factoryYearSet import factoryYearSet
from sysManage.strengthDisturb.maintenManageSet import maintenManageSet

class strengthDisturbSet(QMainWindow, Widget_Strength_Disturb_Set):
    def __init__(self, parent=None):
        super(strengthDisturbSet, self).__init__(parent)
        self.setupUi(self)

        self.strengthSelectSet = strengthSelectSet(self)
        self.factoryYearSet = factoryYearSet(self)
        self.maintenManageSet = maintenManageSet(self)

        self.sw_setManage.addWidget(self.strengthSelectSet)
        self.sw_setManage.addWidget(self.factoryYearSet)
        self.sw_setManage.addWidget(self.maintenManageSet)

        self.signalConnect()
        self.tb_selectSet.setDisabled(True)
        self.tb_factoryYearSet.setDisabled(False)
        self.tb_maintenManageSet.setDisabled(False)

    def signalConnect(self):
        self.tb_selectSet.clicked.connect(self.slotSelectSet)
        self.tb_factoryYearSet.clicked.connect(self.slotFactoryYearSet)
        self.tb_maintenManageSet.clicked.connect(self.slotMaintenManageSet)

    def disconnectSlot(self):
        self.tb_selectSet.clicked.disconnect(self.slotSelectSet)

    def slotSelectSet(self):
        self.signalConnect()
        self.sw_setManage.setCurrentIndex(0)
        self.disconnectSlot()
        self.tb_selectSet.setDisabled(True)
        self.tb_factoryYearSet.setDisabled(False)
        self.tb_maintenManageSet.setDisabled(False)

    def slotFactoryYearSet(self):
        self.signalConnect()
        self.sw_setManage.setCurrentIndex(1)
        self.disconnectSlot()
        self.tb_selectSet.setDisabled(False)
        self.tb_factoryYearSet.setDisabled(True)
        self.tb_maintenManageSet.setDisabled(False)
        self.factoryYearSet._initTableWidget_()

    def slotMaintenManageSet(self):
        self.signalConnect()
        self.sw_setManage.setCurrentIndex(2)
        self.disconnectSlot()
        self.tb_selectSet.setDisabled(False)
        self.tb_factoryYearSet.setDisabled(False)
        self.tb_maintenManageSet.setDisabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = strengthDisturbSet()
    widget.show()
    sys.exit(app.exec_())