import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication

from widgets.strengthDisturb.equipmentBalance.equipmentBalanceResultUI import EquipmentBalanceResult


class Equip_Balance_Result(QWidget, EquipmentBalanceResult):
    def __init__(self, parent=None):
        super(Equip_Balance_Result, self).__init__(parent)
        self.setupUi(self)









if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Equip_Balance_Result()
    widget.show()
    sys.exit(app.exec_())