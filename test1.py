from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QTableWidgetItem, QAbstractItemView, QMessageBox, QApplication
from database.strengthDisturbSql import selectUnitInfoByDeptUper, selectAllDataAboutUnit, selectEquipInfoByEquipUper, \
    selectAllDataAboutEquip, addDataIntoUnit, addDataIntoEquip, updateDataIntoUnit, updateDataIntoEquip, delDataInEquip, delDataInUnit
from widgets.strengthDisturb.select_set import Widget_Select_Set
from test import Ui_Form
import sys


class test1(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(test1, self).__init__(parent)
        self.setupUi(self)
        self.pushButton_5.clicked.connect(self.hideT)
    def hideT(self):
        self.toolBox.hide()

