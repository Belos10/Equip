from widgets.alocatMange.alocatManageSet import Widget_Alocat_Manage_Set
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from widgets.alocatMange.alocatMange import Widget_Alocat_Mange
from sysManage.alocatMange.transferManage import transferManage
from sysManage.alocatMange.DisturbPlan import DisturbPlan
from sysManage.alocatMange.alocatDictSet import alocatDictSet

'''
    功能：
        调配管理主界面
'''
class alocatManageSet(QMainWindow, Widget_Alocat_Manage_Set):
    def __init__(self, parent=None):
        super(alocatManageSet, self).__init__(parent)
        self.setupUi(self)

        self.dictSet = alocatDictSet()

        self.sw_setWidget.addWidget(self.dictSet)
        self.sw_setWidget.setCurrentIndex(0)