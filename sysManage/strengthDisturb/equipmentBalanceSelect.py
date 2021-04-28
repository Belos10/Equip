import sys

from PyQt5.QtWidgets import QWidget, QApplication

from widgets.strengthDisturb.equipmentBalance.equipmentBalanceSelectUI import EquipmentBalanceSelectUI


class Equip_Balance_Select(QWidget, EquipmentBalanceSelectUI):
    def __init__(self, parent=None):
        super(Equip_Balance_Select, self).__init__(parent)
        self.setupUi(self)
        self.year = 0














if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Equip_Balance_Select()
    widget.show()
    sys.exit(app.exec_())