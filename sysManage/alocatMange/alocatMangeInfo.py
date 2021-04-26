from widgets.strengthDisturb.StrengthDisturb import Strength_Disturb_Widget
import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget
from widgets.alocatMange.alocatMange import Widget_Alocat_Mange

class alocatMange(QMainWindow, Widget_Alocat_Mange):
    def __init__(self, parent=None):
        super(alocatMange, self).__init__(parent)
        self.setupUi(self)

        self.allotPlan = QWidget(self)
        self.allotSchedule = QWidget(self)
        self.allotManage = QWidget(self)

        self.stackedWidget.addWidget(self.allotPlan)
        self.stackedWidget.addWidget(self.allotSchedule)
        self.stackedWidget.addWidget(self.allotManage)

        self.stackedWidget.setCurrentIndex(0)
        self.tb_disturbPlan.setDisabled(True)
        self.tb_disturbSchedule.setDisabled(False)
        self.tb_disturbManage.setDisabled(False)
        self.connectSignal()

    def connectSignal(self):
        self.tb_disturbPlan.clicked.connect(self.slotAllotPlan)
        self.tb_disturbSchedule.clicked.connect(self.slotAllotSchedule)
        self.tb_disturbManage.clicked.connect(self.slotAllotManage)

    def slotDisconnect(self):
        self.tb_disturbPlan.clicked.disconnect(self.slotAllotPlan)
        self.tb_disturbSchedule.clicked.disconnect(self.slotAllotSchedule)
        self.tb_disturbManage.clicked.disconnect(self.slotAllotManage)

    def slotAllotPlan(self):
        pass

    def slotAllotSchedule(self):
        pass

    def slotAllotManage(self):
        pass