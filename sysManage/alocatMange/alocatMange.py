from widgets.strengthDisturb.StrengthDisturb import Strength_Disturb_Widget
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from widgets.alocatMange.alocatMange import Widget_Alocat_Mange
from sysManage.alocatMange.transferManage import transferManage
from sysManage.alocatMange.DisturbPlan import DisturbPlan
from sysManage.alocatMange.alocatManageSet import alocatManageSet
from sysManage.alocatMange.AllotSchedule import AllotSchedule
from sysManage.alocatMange.retirePlan import retirePlan

'''
    功能：
        调配管理主界面
'''
class alocatMange(QMainWindow, Widget_Alocat_Mange):
    def __init__(self, parent=None):
        super(alocatMange, self).__init__(parent)
        self.setupUi(self)

        self.disturbPlan = DisturbPlan(self)            #分配调整计划
        self.allotSchedule = AllotSchedule()        #调拨进度
        self.transferManage = transferManage(self)  #调拨单管理
        self.retirePlan = retirePlan(self)              #退役报废计划
        # self.alocatSet = alocatManageSet(self)  # 调配管理设置
        self.userInfo = None

        #添加页面
        self.stackedWidget.addWidget(self.disturbPlan)
        self.stackedWidget.addWidget(self.allotSchedule)
        self.stackedWidget.addWidget(self.transferManage)
        self.stackedWidget.addWidget(self.retirePlan)
        # self.stackedWidget.addWidget(self.alocatSet)

        #初始化显示分配调整计划页面
        self.stackedWidget.setCurrentIndex(0)
        self.tb_disturbPlan.setDisabled(True)
        self.tb_disturbSchedule.setDisabled(False)
        self.tb_disturbManage.setDisabled(False)
        # self.tb_alocatSet.setDisabled(False)
        self.tb_retirePlan.setDisabled(False)
        self.connectSignal()

    def initUserInfo(self, userInfo):
        self.userInfo = userInfo

    '''
        功能：
            信号连接
    '''
    def connectSignal(self):
        self.tb_disturbPlan.clicked.connect(self.slotDisturbPlan)
        self.tb_disturbSchedule.clicked.connect(self.slotDisturbSchedule)
        self.tb_disturbManage.clicked.connect(self.slotDisturbManage)
        # self.tb_alocatSet.clicked.connect(self.slotAlocatSet)
        self.tb_retirePlan.clicked.connect(self.slotRetirePlan)
        # self.transferManage.armyTransfer.pb_equipSet.clicked.connect(self.slotSetEquip)

    '''
        功能：
            关闭信号
    '''
    def slotDisconnect(self):
        self.tb_disturbPlan.clicked.disconnect(self.slotDisturbPlan)
        self.tb_disturbSchedule.clicked.disconnect(self.slotDisturbSchedule)
        self.tb_disturbManage.clicked.disconnect(self.slotDisturbManage)
        # self.tb_alocatSet.clicked.disconnect(self.slotAlocatSet)
        self.tb_retirePlan.clicked.disconnect(self.slotRetirePlan)

    '''
        功能：
            点击分配调整计划按钮
    '''
    def slotDisturbPlan(self):
        self.stackedWidget.setCurrentIndex(0)
        self.tb_disturbPlan.setDisabled(1)
        self.tb_disturbSchedule.setDisabled(False)
        self.tb_disturbManage.setDisabled(0)
        # self.tb_alocatSet.setDisabled(False)
        self.tb_retirePlan.setDisabled(False)
        self.disturbPlan.initAll()

    '''
        功能：
            点击调拨进度按钮
    '''
    def slotDisturbSchedule(self):
        self.stackedWidget.setCurrentIndex(1)
        self.tb_disturbPlan.setDisabled(0)
        self.tb_disturbSchedule.setDisabled(1)
        self.tb_disturbManage.setDisabled(0)
        # self.tb_alocatSet.setDisabled(False)
        self.tb_retirePlan.setDisabled(False)
        self.allotSchedule.initAll()

    '''
        功能：
            点击调拨单管理按钮
    '''
    def slotDisturbManage(self):
        self.stackedWidget.setCurrentIndex(2)
        self.tb_disturbPlan.setDisabled(False)
        self.tb_disturbSchedule.setDisabled(False)
        self.tb_disturbManage.setDisabled(True)
        # self.tb_alocatSet.setDisabled(False)
        self.tb_retirePlan.setDisabled(False)
        self.transferManage.slotArmyTransfer()

    def slotAlocatSet(self):
        self.stackedWidget.setCurrentIndex(4)
        self.tb_disturbPlan.setDisabled(False)
        self.tb_disturbSchedule.setDisabled(False)
        self.tb_disturbManage.setDisabled(False)
        # self.tb_alocatSet.setDisabled(True)
        self.tb_retirePlan.setDisabled(False)

    def slotSetEquip(self):
        self.stackedWidget.setCurrentIndex(4)
        self.tb_disturbPlan.setDisabled(False)
        self.tb_disturbSchedule.setDisabled(False)
        self.tb_disturbManage.setDisabled(False)
        # self.tb_alocatSet.setDisabled(True)
        self.tb_retirePlan.setDisabled(False)
        self.alocatSet.dictSet.slotEquipDictInit()

    '''
        功能：
            点击退役报废计划按钮
    '''
    def slotRetirePlan(self):
        self.stackedWidget.setCurrentIndex(3)
        self.tb_disturbPlan.setDisabled(False)
        self.tb_disturbSchedule.setDisabled(False)
        self.tb_disturbManage.setDisabled(False)
        # self.tb_alocatSet.setDisabled(False)
        self.tb_retirePlan.setDisabled(True)
        self.disturbPlan.initAll()