from PyQt5.QtWidgets import QMainWindow
from widgets.StrengthDisturb import Strength_Disturb_Widget
import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget, QTreeWidgetItemIterator, QTreeWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from sysManage.InquiryResult import Inquiry_Result
from sysManage.addStrenthInfo import AddStrenthInfo
from database.ConnectAndSql import Clicked, insert_Clicked
from sysManage.Stren_Inquiry import Stren_Inquiry
from widgets.StrengthDisturb import Strength_Disturb_Widget

class strengthDisturb(QMainWindow, Strength_Disturb_Widget):
    def __init__(self, parent=None):
        super(strengthDisturb, self).__init__(parent)
        self.setupUi(self)
        self.login = QWidget(self)
        self.strenSelect = Stren_Inquiry(self)
        self.maintenMange = QWidget(self)
        self.equipBalance = QWidget(self)
        self.applyRetire = QWidget(self)

        self.stackedWidget.addWidget(self.login)
        self.stackedWidget.addWidget(self.strenSelect)
        self.stackedWidget.addWidget(self.maintenMange)
        self.stackedWidget.addWidget(self.equipBalance)
        self.stackedWidget.addWidget(self.applyRetire)
        self.stackedWidget.setCurrentIndex(0)
        self.actionstrengthSelect.setDisabled(False)
        self.actionapplyRetire.setDisabled(False)
        self.actionequipBalance.setDisabled(False)
        self.actionmaintenMange.setDisabled(False)
        self.connectSignal()


    def connectSignal(self):
        self.actionstrengthSelect.triggered.connect(self.slotSelectStrength)
        self.actionmaintenMange.triggered.connect(self.slotMaintenMange)
        self.actionequipBalance.triggered.connect(self.slotEquipBalance)
        self.actionapplyRetire.triggered.connect(self.slotApplyRetire)

    def slotDisconnect(self):
        self.actionstrengthSelect.triggered.disconnect(self.slotSelectStrength)
        self.actionmaintenMange.triggered.disconnect(self.slotMaintenMange)
        self.actionequipBalance.triggered.disconnect(self.slotEquipBalance)
        self.actionapplyRetire.triggered.disconnect(self.slotApplyRetire)

    def slotSelectStrength(self):

        self.actionstrengthSelect.setDisabled(True)
        self.actionapplyRetire.setDisabled(False)
        self.actionequipBalance.setDisabled(False)
        self.actionmaintenMange.setDisabled(False)
        self.slotDisconnect()
        self.stackedWidget.setCurrentIndex(1)
        self.connectSignal()

    def slotMaintenMange(self):
        self.actionstrengthSelect.setDisabled(False)
        self.actionapplyRetire.setDisabled(False)
        self.actionequipBalance.setDisabled(False)
        self.actionmaintenMange.setDisabled(True)

        self.slotDisconnect()
        self.stackedWidget.setCurrentIndex(2)
        self.connectSignal()

    def slotEquipBalance(self):

        self.actionstrengthSelect.setDisabled(False)
        self.actionapplyRetire.setDisabled(False)
        self.actionequipBalance.setDisabled(True)
        self.actionmaintenMange.setDisabled(False)

        self.slotDisconnect()
        self.stackedWidget.setCurrentIndex(3)
        self.connectSignal()

    def slotApplyRetire(self):

        self.actionstrengthSelect.setDisabled(False)
        self.actionapplyRetire.setDisabled(True)
        self.actionequipBalance.setDisabled(False)
        self.actionmaintenMange.setDisabled(False)

        self.slotDisconnect()
        self.stackedWidget.setCurrentIndex(4)
        self.connectSignal()


