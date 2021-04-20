from widgets.strengthDisturb.StrengthDisturb import Strength_Disturb_Widget
import sys
from PyQt5.QtWidgets import QMainWindow,QApplication,QWidget
from widgets.alocatMange.alocatMange import Widget_Alocat_Mange

class alocatMange(QMainWindow, Widget_Alocat_Mange):
    def __init__(self, parent=None):
        super(alocatMange, self).__init__(parent)
        self.setupUi(self)

        self.disturbPlan = QWidget(self)
        self.disturbSchedule = QWidget(self)
        self.disturbManage = QWidget(self)

        self.stackedWidget.addWidget(self.disturbPlan)
        self.stackedWidget.addWidget(self.disturbSchedule)
        self.stackedWidget.addWidget(self.disturbManage)

        self.stackedWidget.setCurrentIndex(0)
        self.tb_disturbPlan.setDisabled(True)
        self.tb_disturbSchedule.setDisabled(False)
        self.tb_disturbManage.setDisabled(False)
        self.connectSignal()

    def connectSignal(self):
        self.tb_disturbPlan.clicked.connect(self.slotDisturbPlan)
        self.tb_disturbSchedule.clicked.connect(self.slotDisturbSchedule)
        self.tb_disturbManage.clicked.connect(self.slotDisturbManage)

    def slotDisconnect(self):
        self.tb_disturbPlan.clicked.disconnect(self.slotDisturbPlan)
        self.tb_disturbSchedule.clicked.disconnect(self.slotDisturbSchedule)
        self.tb_disturbManage.clicked.disconnect(self.slotDisturbManage)

    def slotDisturbPlan(self):
        pass

    def slotDisturbSchedule(self):
        pass

    def slotDisturbManage(self):
        pass