import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, QAbstractItemView, QMessageBox, QDialog, QDialogButtonBox
from widgets.strengthDisturb.inquiry_result import Widget_Inquiry_Result
from database.strengthDisturbSql import selectAboutStrengthByUnitListAndEquipList, selectUnitIsHaveChild, selectEquipIsHaveChild,\
    selectAboutStrengthByEquipShow,selectAboutStrengthByUnitShow, updateStrengthAboutStrengrh,\
    updateStrengthAboutStrengrh,updateEquipUnit
from PyQt5.Qt import Qt
from widgets.strengthDisturb.dialogEquipUnit import Widget_Equip_Unit_Set
#new

class equipUnitSet(QDialog, Widget_Equip_Unit_Set):
    def __init__(self, parent=None):
        super(equipUnitSet, self).__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.slotClickedButton)

    def initEquipID(self, equipID):
        self.equipID = equipID

    def slotClickedButton(self):
        unit = self.le_equipUnit.text()
        updateEquipUnit(unit, self.equipID)

