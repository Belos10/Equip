from PyQt5.QtWidgets import QWidget

from sysManage.strengthDisturb.select_setEquip import select_setEquip
from sysManage.strengthDisturb.select_setUnit import select_setUnit
from widgets.strengthDisturb.select_set import Widget_Select_Set

'''
    装备/单位目录设置
'''


class strengthSelectSet(QWidget, Widget_Select_Set):
    def __init__(self, parent=None):
        super(strengthSelectSet, self).__init__(parent)
        self.setupUi(self)

        self.selectSetUnit = select_setUnit()
        self.selectSetEquip = select_setEquip()

        self.sw_select_set.addWidget(self.selectSetUnit)
        self.sw_select_set.addWidget(self.selectSetEquip)
        self.sw_select_set.setCurrentIndex(0)

        self.signalConnect()

    def signalConnect(self):
        self.cb_setChoose.currentIndexChanged.connect(self.slotChangeSet)

    def slotChangeSet(self):
        if self.cb_setChoose.currentIndex() == 0:
            self.slotUnitDictInit()
        else:
            self.slotEquipDictInit()

    def slotUnitDictInit(self):
        self.sw_select_set.setCurrentIndex(0)
        self.selectSetUnit.slotUnitDictInit()

    def slotEquipDictInit(self):
        self.sw_select_set.setCurrentIndex(1)
        self.selectSetEquip.slotEquipDictInit()
