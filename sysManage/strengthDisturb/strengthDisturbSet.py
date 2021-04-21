import sys
from PyQt5.QtWidgets import QMainWindow,QApplication
from widgets.strengthDisturb.strengthDisturbSet import Widget_Strength_Disturb_Set
from sysManage.strengthDisturb.strengthSelectSet import strengthSelectSet

class strengthDisturbSet(QMainWindow, Widget_Strength_Disturb_Set):
    def __init__(self, parent=None):
        super(strengthDisturbSet, self).__init__(parent)
        self.setupUi(self)

        self.strengthSelectSet = strengthSelectSet(self)

        self.sw_setManage.addWidget(self.strengthSelectSet)
        self.signalConnect()
        self.tb_selectSet.setDisabled(True)

    def signalConnect(self):
        self.tb_selectSet.clicked.connect(self.slotSelectSet)

    def disconnectSlot(self):
        self.tb_selectSet.clicked.disconnect(self.slotSelectSet)

    def slotSelectSet(self):

        self.signalConnect()
        self.sw_setManage.setCurrentIndex(0)
        self.disconnectSlot()
        self.tb_selectSet.setDisabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = strengthDisturbSet()
    widget.show()
    sys.exit(app.exec_())