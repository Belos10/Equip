from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QTableWidgetItem, QAbstractItemView, QMessageBox, QApplication, QTableWidget
from database.strengthDisturbSql import selectUnitInfoByDeptUper, selectAllDataAboutUnit, selectEquipInfoByEquipUper, \
    selectAllDataAboutEquip, addDataIntoUnit, addDataIntoEquip, updateDataIntoUnit, updateDataIntoEquip, delDataInEquip, delDataInUnit
from widgets.strengthDisturb.select_set import Widget_Select_Set
from test2 import Ui_Form
from test1 import test1
import sys


class test3(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(test3, self).__init__(parent)
        self.setupUi(self)

        self.test = test1(self)
        self.gridLayout.addWidget(self.test)
        self.test.show()
        self.table = QTableWidget(self)
        self.gridLayout.addWidget(self.table)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = test3()
    widget.show()
    sys.exit(app.exec_())