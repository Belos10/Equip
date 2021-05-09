from widgets.strengthDisturb.StrengthDisturb import Strength_Disturb_Widget
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from widgets.alocatMange.alocatMange import Widget_Alocat_Mange
from sysManage.alocatMange.transferManage import transferManage
from sysManage.alocatMange.DisturbPlan import DisturbPlan
from sysManage.alocatMange.alocatManageSet import alocatManageSet

'''
    功能：
        调配管理主界面
'''
class alocatMange(QMainWindow, Widget_Alocat_Mange):
    def __init__(self, parent=None):
        super(alocatMange, self).__init__(parent)
        self.setupUi(self)

        self.disturbPlan = DisturbPlan()            #分配调整计划
        self.disturbSchedule = QWidget(self)        #调拨进度
        self.transferManage = transferManage(self)  #调拨单管理
        self.alocatSet = alocatManageSet(self)              #调配管理设置

        #添加页面
        self.stackedWidget.addWidget(self.disturbPlan)
        self.stackedWidget.addWidget(self.disturbSchedule)
        self.stackedWidget.addWidget(self.transferManage)
        self.stackedWidget.addWidget(self.alocatSet)

        #初始化显示分配调整计划页面
        self.stackedWidget.setCurrentIndex(0)
        self.tb_disturbPlan.setDisabled(True)
        self.tb_disturbSchedule.setDisabled(False)
        self.tb_disturbManage.setDisabled(False)
        self.tb_alocatSet.setDisabled(False)
        self.connectSignal()

    '''
        功能：
            信号连接
    '''
    def connectSignal(self):
        self.tb_disturbPlan.clicked.connect(self.slotDisturbPlan)
        self.tb_disturbSchedule.clicked.connect(self.slotDisturbSchedule)
        self.tb_disturbManage.clicked.connect(self.slotDisturbManage)
        self.tb_alocatSet.clicked.connect(self.slotAlocatSet)
        self.transferManage.armyTransfer.pb_equipSet.clicked.connect(self.slotSetEquip)

    '''
        功能：
            关闭信号
    '''
    def slotDisconnect(self):
        self.tb_disturbPlan.clicked.disconnect(self.slotDisturbPlan)
        self.tb_disturbSchedule.clicked.disconnect(self.slotDisturbSchedule)
        self.tb_disturbManage.clicked.disconnect(self.slotDisturbManage)

    '''
        功能：
            点击分配调整计划按钮
    '''
    def slotDisturbPlan(self):
        self.stackedWidget.setCurrentIndex(0)
        self.tb_disturbPlan.setDisabled(1)
        self.tb_disturbSchedule.setDisabled(False)
        self.tb_disturbManage.setDisabled(0)
        self.tb_alocatSet.setDisabled(False)

    '''
        功能：
            点击调拨进度按钮
    '''
    def slotDisturbSchedule(self):
        pass

    '''
        功能：
            点击调拨单管理按钮
    '''
    def slotDisturbManage(self):
        self.stackedWidget.setCurrentIndex(2)
        self.tb_disturbPlan.setDisabled(False)
        self.tb_disturbSchedule.setDisabled(False)
        self.tb_disturbManage.setDisabled(True)
        self.tb_alocatSet.setDisabled(False)

    def slotAlocatSet(self):
        self.stackedWidget.setCurrentIndex(3)
        self.tb_disturbPlan.setDisabled(False)
        self.tb_disturbSchedule.setDisabled(False)
        self.tb_disturbManage.setDisabled(False)
        self.tb_alocatSet.setDisabled(True)

    def slotSetEquip(self):
        self.stackedWidget.setCurrentIndex(3)
        self.tb_disturbPlan.setDisabled(False)
        self.tb_disturbSchedule.setDisabled(False)
        self.tb_disturbManage.setDisabled(False)
        self.tb_alocatSet.setDisabled(True)
        self.alocatSet.dictSet.slotEquipDictInit()