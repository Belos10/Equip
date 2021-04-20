from widgets.manage_widget import Widget_Manage_Widgets
from PyQt5.QtWidgets import QMainWindow, QWidget
from sysManage.strengthDisturb.strengthDisturb import strengthDisturb

class Manage_Widgets(QMainWindow, Widget_Manage_Widgets):
    def __init__(self, parent=None):
        super(Manage_Widgets, self).__init__(parent)
        self.setupUi(self)
        self.login = QWidget()
        self.strengthDisturb = strengthDisturb()
        self.alocatMange = QWidget()
        self.purChasPlan = QWidget()
        self.mantanSupport = QWidget()
        self.warStorage = QWidget()
        self.contractMange = QWidget()
        self.dangerGoods = QWidget()
        self.PosEngin = QWidget()
        self.dictSelect = QWidget()
        self.sysConfig = QWidget()

        self.setWindowTitle("核化装备管理系统")

        self.tb_ManageWidget.addTab(self.login, "登录")
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
        self.tb_ManageWidget.addTab(self.sysConfig, "系统配置")


