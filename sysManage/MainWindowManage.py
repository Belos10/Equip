from PyQt5.QtWidgets import QMainWindow
from widgets.manage_widget import Widget_Manage_Widgets
import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from sysManage.Stren_Inquiry import Stren_Inquiry
from sysManage.strengthDisturb import strengthDisturb

class Manage_Widgets(QMainWindow, Widget_Manage_Widgets):
    def __init__(self, parent=None):
        super(Manage_Widgets, self).__init__(parent)
        self.setupUi(self)
        self.strengthDisturb = strengthDisturb()
        self.alocatMange = QWidget()
        self.purChasPlan = QWidget()
        self.mantanSupport = QWidget()

        self.tb_ManageWidget.addTab(self.strengthDisturb, "实力查询")
        self.tb_ManageWidget.setCurrentIndex(0)
        self.tb_ManageWidget.addTab(self.alocatMange, "调配管理")
        self.tb_ManageWidget.addTab(self.purChasPlan, "订购计划")
        self.tb_ManageWidget.addTab(self.mantanSupport, "维修保障")

