import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from widgets.orderManage.orderManage import widget_orderManage
from sysManage.orderManage.OrderAllotPlan import OrderAllotPlan

'''
    功能：
        调配管理主界面
'''
class orderManage(QMainWindow, widget_orderManage):
    def __init__(self, parent=None):
        super(orderManage, self).__init__(parent)
        self.setupUi(self)

        self.orderPlan = QWidget()                  # 订购计划
        self.adjustOrder = QWidget()                # 订购计划调整
        self.orderAllotPlan = QWidget(self)      # 订购分配计划
        self.orderSchedule = QWidget()              # 订购进度
        self.retirePlan = QWidget()             # 订购退役计划
        self.userInfo = None

        #添加页面
        self.Order_stackedWidget.addWidget(self.orderPlan)
        self.Order_stackedWidget.addWidget(self.adjustOrder)
        self.Order_stackedWidget.addWidget(self.orderAllotPlan)
        self.Order_stackedWidget.addWidget(self.orderSchedule)
        self.Order_stackedWidget.addWidget(self.retirePlan)

        #初始化显示分配调整计划页面
        self.Order_stackedWidget.setCurrentIndex(0)
        self.tb_orderPlan.setDisabled(True)
        self.tb_adjustOrder.setDisabled(False)
        self.tb_orderAllotPlan.setDisabled(False)
        self.tb_orderSchedule.setDisabled(False)
        self.tb_retirePlan.setDisabled(False)
        self.connectSignal()

    def initUserInfo(self, userInfo):
        self.userInfo = userInfo

    '''
        功能：
            信号连接
    '''
    def connectSignal(self):
        self.tb_orderPlan.clicked.connect(self.slotOrderPlan)
        self.tb_adjustOrder.clicked.connect(self.slotAdjustOrder)
        self.tb_orderAllotPlan.clicked.connect(self.slotOrderAllotPlan)
        self.tb_orderSchedule.clicked.connect(self.slotOrderSchedule)
        self.tb_retirePlan.clicked.connect(self.slotRetirePlan)
        # self.transferManage.armyTransfer.pb_equipSet.clicked.connect(self.slotSetEquip)

    '''
        功能：
            关闭信号
    '''
    def slotDisconnect(self):
        self.tb_orderPlan.clicked.disconnect(self.slotOrderPlan)
        self.tb_adjustOrder.clicked.disconnect(self.slotAdjustOrder)
        self.tb_orderAllotPlan.clicked.disconnect(self.slotOrderAllotPlan)
        self.tb_orderSchedule.clicked.disconnect(self.slotOrderSchedule)
        self.tb_retirePlan.clicked.disconnect(self.slotRetirePlan)

    '''
        功能：
            点击订购计划按钮
    '''
    def slotOrderPlan(self):
        self.Order_stackedWidget.setCurrentIndex(0)
        self.tb_orderPlan.setDisabled(1)
        self.tb_adjustOrder.setDisabled(False)
        self.tb_orderAllotPlan.setDisabled(0)
        self.tb_orderSchedule.setDisabled(False)
        self.tb_retirePlan.setDisabled(False)
        # self.disturbPlan.initAll()

    '''
        功能：
            点击订购调整按钮
    '''
    def slotAdjustOrder(self):
        self.Order_stackedWidget.setCurrentIndex(1)
        self.tb_orderPlan.setDisabled(0)
        self.tb_adjustOrder.setDisabled(1)
        self.tb_orderAllotPlan.setDisabled(0)
        self.tb_orderSchedule.setDisabled(False)
        self.tb_retirePlan.setDisabled(False)
        # self.allotSchedule.initAll()

    '''
        功能：
            点击订购分配计划按钮
    '''
    def slotOrderAllotPlan(self):
        self.Order_stackedWidget.setCurrentIndex(2)
        self.tb_orderPlan.setDisabled(False)
        self.tb_adjustOrder.setDisabled(False)
        self.tb_orderAllotPlan.setDisabled(True)
        self.tb_orderSchedule.setDisabled(False)
        self.tb_retirePlan.setDisabled(False)
        # self.transferManage.slotArmyTransfer()

    '''
        功能：
            点击订购进度按钮
    '''
    def slotOrderSchedule(self):
        self.Order_stackedWidget.setCurrentIndex(3)
        self.tb_orderPlan.setDisabled(False)
        self.tb_adjustOrder.setDisabled(False)
        self.tb_orderAllotPlan.setDisabled(False)
        self.tb_orderSchedule.setDisabled(True)
        self.tb_retirePlan.setDisabled(False)

    '''
        功能：
            点击订购退役计划按钮
    '''
    def slotRetirePlan(self):
        self.Order_stackedWidget.setCurrentIndex(4)
        self.tb_orderPlan.setDisabled(False)
        self.tb_adjustOrder.setDisabled(False)
        self.tb_orderAllotPlan.setDisabled(False)
        self.tb_orderSchedule.setDisabled(False)
        self.tb_retirePlan.setDisabled(True)
        # self.disturbPlan.initAll()