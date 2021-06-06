from widgets.manage_widget import Widget_Manage_Widgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication,QMessageBox
from sysManage.strengthDisturb.strengthDisturb import strengthDisturb
from sysManage.alocatMange.alocatMange import alocatMange
from sysManage.dictSelect.dictSelect import dictSelect
from sysManage.login.login import login
from database.loginSql import selectUserInfoByAccont
from sysManage.login.loginSet import loginSet
from sysManage.dangerGoods.dangerGoods import DangerGoods
from sysManage.positionEngineer.positionEngineerMain import PositionEngineerMain
from sysManage.userInfo import get_value,set_value
#new
class Manage_Widgets(QMainWindow, Widget_Manage_Widgets):
    def __init__(self, parent=None):
        super(Manage_Widgets, self).__init__(parent)
        self.setupUi(self)
        self.setLogin = loginSet()
        self.strengthDisturb = strengthDisturb()
        self.alocatMange = alocatMange()
        self.purChasPlan = QWidget()
        self.mantanSupport = QWidget()
        self.warStorage = QWidget()
        self.contractMange = QWidget()
        self.dangerGoods = DangerGoods()
        self.PosEngin = PositionEngineerMain()
        self.dictSelect = dictSelect()
        self.sysConfig = QWidget()

        self.setWindowTitle("核化装备管理系统")
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
        self.tb_ManageWidget.addTab(self.setLogin, "登录设置")

        self.login = login()
        self.login.show()
        self.hide()

        self.signalConnect()

    def signalConnect(self):
        self.tb_ManageWidget.currentChanged.connect(self.slotCurrentChange)

        self.login.tb_cancel.clicked.connect(self.slotCloseSystem)

        self.login.tb_login.clicked.connect(self.slotLoginSystem)

    def slotCloseSystem(self):
        app = QApplication.instance()
        # 退出应用程序
        app.quit()

    def slotLoginSystem(self):
        self.accont = self.login.le_accont.text()
        self.pswd = self.login.le_pswd.text()
        if self.accont == "":
            reply = QMessageBox.question(self, '登录', '登陆失败，请输入账号',QMessageBox.Yes)
            return
        self.userInfo = selectUserInfoByAccont(self.accont)
        if self.userInfo:
            if self.userInfo[0][2] != self.pswd:
                reply = QMessageBox.question(self, '登录', '登录失败,密码错误', QMessageBox.Yes)
                return

        else:
            reply = QMessageBox.question(self, '登录', '登录失败,账号或密码错误', QMessageBox.Yes)
            return

        if self.userInfo[0][3] == "基地":
            self.tb_ManageWidget.removeTab(5)
            self.tb_ManageWidget.removeTab(0)
        elif self.userInfo[0][3] == "旅团":
            self.tb_ManageWidget.removeTab(5)
            self.tb_ManageWidget.removeTab(0)
        elif self.userInfo[0][3] == "仓库":
            self.tb_ManageWidget.removeTab(5)
            self.tb_ManageWidget.removeTab(0)
        set_value("totleUserInfo", self.userInfo)
        print("''''''''''''''''''''''''''''''''", get_value("totleUserInfo"))
        #self.strengthDisturb.initUserInfo(self.userInfo)
        #self.alocatMange.initUserInfo(self.userInfo)
        #self.PosEngin.slotInstallation()
        self.login.close()
        self.show()

    def slotCurrentChange(self):
        if self.tb_ManageWidget.currentWidget() == self.setLogin:
            self.setLogin.initWidgets()

