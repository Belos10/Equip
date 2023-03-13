import ctypes

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget

from sysManage.alocatMange.alocatMange import alocatMange
from sysManage.contractMangement.contractMangementMain import ContractManagementMain
from sysManage.dangerGoods.dangerGoods import DangerGoods
from sysManage.dictSelect.dictSelect import dictSelect
from sysManage.login.login import login
from sysManage.login.loginSet import loginSet
from sysManage.maintainSupport.maintainSupportManage import MaintainSupportManage
from sysManage.orderManage.OrderManage import OrderManage
from sysManage.positionEngineer.positionEngineerMain import PositionEngineerMain
from sysManage.strengthDisturb.strengthDisturb import strengthDisturb
from sysManage.warStore.WarStoreMain import WarStoreMain
from widgets.manage_widget import Widget_Manage_Widgets

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

#new
class Manage_Widgets(QMainWindow, Widget_Manage_Widgets):
    signal = pyqtSignal()
    def __init__(self, parent=None):
        super(Manage_Widgets, self).__init__(parent)
        self.setupUi(self)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setLogin = loginSet()
        self.strengthDisturb = strengthDisturb()
        self.alocatMange = alocatMange()
        self.purChasPlan = OrderManage()
        self.mantanSupport = MaintainSupportManage()
        self.warStorage = WarStoreMain()
        self.contractMange = ContractManagementMain()
        self.dangerGoods = DangerGoods()
        self.PosEngin = PositionEngineerMain()
        self.dictSelect = dictSelect()
        self.loginStatus = False
        # self.sysConfig = QWidget()s
        # self.setWindowTitle("装备管理系统")
        # self.setStyleSheet("color:black")
        self.setWindowIcon(QIcon(":/pic/system.png"))
        self.tb_ManageWidget.addTab(self.strengthDisturb, "实力分布")
        self.tb_ManageWidget.setCurrentIndex(0)
        self.tb_ManageWidget.addTab(self.alocatMange, "调配管理")
        self.tb_ManageWidget.addTab(self.purChasPlan, "订购计划")
        self.tb_ManageWidget.addTab(self.mantanSupport, "维修保障")
        self.tb_ManageWidget.addTab(self.warStorage, "战储物资")
        self.tb_ManageWidget.addTab(self.contractMange, "合同管理")
        self.tb_ManageWidget.addTab(self.dangerGoods, "防化危险品")
        self.tb_ManageWidget.addTab(self.PosEngin, "阵地工程")
        self.tb_ManageWidget.addTab(self.dictSelect, "目录查询")
        # self.tb_ManageWidget.addTab(self.sysConfig, "系统配置")
        self.tb_ManageWidget.addTab(self.setLogin, "登录设置")

        self.login = login()
        self.login.show()
        self.hide()
        self.center()
        self.signalConnect()

    def center(self):
        print("center")
        self.size = QDesktopWidget().screenGeometry()
        self.resize = self.geometry()
        self.move((self.size.width() - self.resize.width()) / 2, (self.size.height() - self.resize.height()) / 2)

    def signalConnect(self):
        self.tb_ManageWidget.currentChanged.connect(self.slotCurrentChange)

        # self.login.tb_cancel.clicked.connect(self.slotCloseSystem)
        #
        # self.login.tb_login.clicked.connect(self.slotLoginSystem)



    def slotCurrentChange(self):
        if self.tb_ManageWidget.currentWidget() == self.setLogin:
            self.setLogin.initWidgets()
        if self.tb_ManageWidget.currentWidget() == self.strengthDisturb:
            self.strengthDisturb.strenSelect.initSelectYear()
        if self.tb_ManageWidget.currentWidget() == self.PosEngin:
            self.PosEngin.slotInstallation()

