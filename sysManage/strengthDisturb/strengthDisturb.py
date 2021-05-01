from widgets.strengthDisturb.StrengthDisturb import Strength_Disturb_Widget
import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget
from sysManage.strengthDisturb.Stren_Inquiry import Stren_Inquiry
from sysManage.strengthDisturb.strengthDisturbSet import strengthDisturbSet
from sysManage.strengthDisturb.maintenMange import maintenManage
from sysManage.strengthDisturb.equipmentBalanceControl import Equip_Balance_Control
#new
class strengthDisturb(QMainWindow, Strength_Disturb_Widget):
    def __init__(self, parent=None):
        super(strengthDisturb, self).__init__(parent)
        self.setupUi(self)

        self.strenSelect = Stren_Inquiry(self)
        self.maintenMange = maintenManage(self)
        self.equipBalance = Equip_Balance_Control(self)
        self.applyRetire = QWidget(self)
        self.strengthDisturbSet = strengthDisturbSet(self)

        self.stackedWidget.addWidget(self.strenSelect)
        self.stackedWidget.addWidget(self.maintenMange)
        self.stackedWidget.addWidget(self.equipBalance)
        self.stackedWidget.addWidget(self.applyRetire)
        self.stackedWidget.addWidget(self.strengthDisturbSet)

        self.stackedWidget.setCurrentIndex(0)
        self.tb_strengthSelect.setDisabled(True)
        self.tb_applyRetire.setDisabled(False)
        self.tb_equipBalance.setDisabled(False)
        self.tb_maintenMange.setDisabled(False)
        self.tb_strengthDisturbSet.setDisabled(False)
        self.connectSignal()


    def connectSignal(self):
        self.tb_strengthSelect.clicked.connect(self.slotSelectStrength)
        self.tb_maintenMange.clicked.connect(self.slotMaintenMange)
        self.tb_equipBalance.clicked.connect(self.slotEquipBalance)
        self.tb_applyRetire.clicked.connect(self.slotApplyRetire)
        self.tb_strengthDisturbSet.clicked.connect(self.slotStrengthDisturbSet)

    def slotDisconnect(self):
        self.tb_strengthSelect.clicked.disconnect(self.slotSelectStrength)
        self.tb_maintenMange.clicked.disconnect(self.slotMaintenMange)
        self.tb_equipBalance.clicked.disconnect(self.slotEquipBalance)
        self.tb_applyRetire.clicked.disconnect(self.slotApplyRetire)
        self.tb_strengthDisturbSet.clicked.disconnect(self.slotStrengthDisturbSet)

    def slotSelectStrength(self):

        self.tb_strengthSelect.setDisabled(True)
        self.tb_applyRetire.setDisabled(False)
        self.tb_equipBalance.setDisabled(False)
        self.tb_maintenMange.setDisabled(False)
        self.tb_strengthDisturbSet.setDisabled(False)
        self.slotDisconnect()
        self.stackedWidget.setCurrentIndex(0)
        self.strenSelect._initStrenInquiry()
        self.connectSignal()

    def slotMaintenMange(self):
        self.tb_strengthSelect.setDisabled(False)
        self.tb_applyRetire.setDisabled(False)
        self.tb_equipBalance.setDisabled(False)
        self.tb_maintenMange.setDisabled(True)
        self.tb_strengthDisturbSet.setDisabled(False)

        self.slotDisconnect()
        self.stackedWidget.setCurrentIndex(1)
        self.connectSignal()
        self.maintenMange._initAll_()

    def slotEquipBalance(self):
        self.tb_strengthSelect.setDisabled(False)
        self.tb_applyRetire.setDisabled(False)
        self.tb_equipBalance.setDisabled(True)
        self.tb_maintenMange.setDisabled(False)
        self.tb_strengthDisturbSet.setDisabled(False)

        self.slotDisconnect()
        self.stackedWidget.setCurrentIndex(2)
        self.connectSignal()

    def slotApplyRetire(self):
        self.tb_strengthSelect.setDisabled(False)
        self.tb_applyRetire.setDisabled(True)
        self.tb_equipBalance.setDisabled(False)
        self.tb_maintenMange.setDisabled(False)
        self.tb_strengthDisturbSet.setDisabled(False)

        self.slotDisconnect()
        self.stackedWidget.setCurrentIndex(3)
        self.connectSignal()

    def slotStrengthDisturbSet(self):
        self.tb_strengthSelect.setDisabled(False)
        self.tb_applyRetire.setDisabled(False)
        self.tb_equipBalance.setDisabled(False)
        self.tb_maintenMange.setDisabled(False)
        self.tb_strengthDisturbSet.setDisabled(True)

        self.slotDisconnect()
        self.stackedWidget.setCurrentIndex(4)
        self.connectSignal()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = strengthDisturb()
    widget.show()
    sys.exit(app.exec_())