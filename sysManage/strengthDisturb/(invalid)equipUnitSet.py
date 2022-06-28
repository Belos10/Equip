from PyQt5.QtWidgets import QDialog

from database.strengthDisturbSql import updateEquipUnit
from widgets.strengthDisturb.dialogEquipUnit import Widget_Equip_Unit_Set


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

