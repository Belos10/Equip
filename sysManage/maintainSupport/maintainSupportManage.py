import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from widgets.serviceSupport.MaintainSupport import widget_MaintainSupport
from sysManage.maintainSupport.serviceSupportMain import yearServiceSupport
'''
    功能：
        维修保障主界面
'''
class MaintainSupportManage(QMainWindow, widget_MaintainSupport):
    def __init__(self, parent=None):
        super(MaintainSupportManage, self).__init__(parent)
        self.setupUi(self)

        self.yearSerSup = yearServiceSupport()          # 维修计划
        self.maintainSchedule = QWidget()                # 维修进度
        self.materialManage = QWidget(self)             # 物资管理

        self.userInfo = None

        #添加页面
        self.sw_MaintainSup.addWidget(self.yearSerSup)
        self.sw_MaintainSup.addWidget(self.maintainSchedule)
        self.sw_MaintainSup.addWidget(self.materialManage)


        #初始化显示分配调整计划页面
        self.sw_MaintainSup.setCurrentIndex(0)
        self.tb_yearSerSup.setDisabled(True)
        self.tb_maintainSchedule.setDisabled(False)
        self.tb_materialManage.setDisabled(False)

        self.connectSignal()

    def initUserInfo(self, userInfo):
        self.userInfo = userInfo

    '''
        功能：
            信号连接
    '''
    def connectSignal(self):
        self.tb_yearSerSup.clicked.connect(self.slotYearSerSup)
        self.tb_maintainSchedule.clicked.connect(self.slotMaintainSchedule)
        self.tb_materialManage.clicked.connect(self.slotMaterialManage)


    '''
        功能：
            关闭信号
    '''
    def slotDisconnect(self):
        self.tb_yearSerSup.clicked.disconnect(self.slotYearSerSup)
        self.tb_maintainSchedule.clicked.disconnect(self.slotMaintainSchedule)
        self.tb_materialManage.clicked.disconnect(self.slotMaterialManage)


    '''
        功能：
            点击维修计划按钮
    '''
    def slotYearSerSup(self):
        self.sw_MaintainSup.setCurrentIndex(0)
        self.tb_yearSerSup.setDisabled(1)
        self.tb_maintainSchedule.setDisabled(False)
        self.tb_materialManage.setDisabled(0)
        self.yearSerSup.initAll()


    '''
        功能：
            点击维修进度按钮
    '''
    def slotMaintainSchedule(self):
        self.sw_MaintainSup.setCurrentIndex(1)
        self.tb_yearSerSup.setDisabled(0)
        self.tb_maintainSchedule.setDisabled(1)
        self.tb_materialManage.setDisabled(0)


    '''
        功能：
            点击物资管理按钮
    '''
    def slotMaterialManage(self):
        self.sw_MaintainSup.setCurrentIndex(2)
        self.tb_yearSerSup.setDisabled(False)
        self.tb_maintainSchedule.setDisabled(False)
        self.tb_materialManage.setDisabled(True)