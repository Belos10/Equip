import sys
# from fbs_runtime.application_context.PyQt5 import ApplicationContext
import threading

from PyQt5.Qt import QObject
from PyQt5.QtCore import pyqtSignal, QProcess
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, qApp

from database.loginSql import selectUserInfoByAccont
from PyQt5 import sip, Qt, QtGui

from sysManage.MainWindowManage import Manage_Widgets
from sysManage.component import getMessageBox
from sysManage.login.login import login
from icons.readQss import readQss
import os

from sysManage.userInfo import set_value
from utills.test import FramelessWindow

'''
    显示主界面
'''
class mainManage(QObject):
    def __init__(self):
        super(mainManage,self).__init__()
        # self.login = login()
        # self.login.show()
        self.mainwnd = FramelessWindow()
        # self.mainwnd.setWindowIcon(QIcon(":/pic/system.png"))
        self.widget = Manage_Widgets()
        self.mainwnd.setWidget(self.widget)
        self.mainwnd.show()
        self.mainwnd._widget.login.tb_login.clicked.connect(self.slotLoginSystem)
        self.mainwnd._widget.login.tb_cancel.clicked.connect(self.slotCloseSystem)
        self.mainwnd.titleBar.hide()

    def slotCloseSystem(self):
        app = QApplication.instance()
        # 退出应用程序
        app.quit()


    def slotLoginSystem(self):
        self.mainwnd._widget.login.accont = self.mainwnd._widget.login.le_accont.text()
        self.mainwnd._widget.login.pswd = self.mainwnd._widget.login.le_pswd.text()
        if self.mainwnd._widget.login.accont == "":
            getMessageBox('登录', '登陆失败，请输入账号', True, False)
            # reply = QMessageBox.question(self, '登录', '登陆失败，请输入账号',QMessageBox.Yes)
            return
        self.mainwnd._widget.login.userInfo = selectUserInfoByAccont(self.mainwnd._widget.login.accont)
        if self.mainwnd._widget.login.userInfo:
            if self.mainwnd._widget.login.userInfo[0][2] != self.mainwnd._widget.login.pswd:
                getMessageBox('登录', '登录失败,密码错误', True, False)
                # reply = QMessageBox.question(self, '登录', '登录失败,密码错误', QMessageBox.Yes)
                return

        else:
            reply = getMessageBox('登录', '登录失败,账号或密码错误', True, False)
            # reply = QMessageBox.question(self, '登录', '登录失败,账号或密码错误', QMessageBox.Yes)
            return

        if self.mainwnd._widget.login.userInfo[0][3] == "基地":
            self.mainwnd._widget.login.tb_ManageWidget.removeTab(5)
            self.mainwnd._widget.login.tb_ManageWidget.removeTab(0)
        elif self.mainwnd._widget.login.userInfo[0][3] == "旅团":
            self.mainwnd._widget.login.tb_ManageWidget.removeTab(5)
            self.mainwnd._widget.login.tb_ManageWidget.removeTab(0)
        elif self.mainwnd._widget.login.userInfo[0][3] == "仓库":
            self.mainwnd._widget.login.tb_ManageWidget.removeTab(5)
            self.mainwnd._widget.login.tb_ManageWidget.removeTab(0)
        set_value("totleUserInfo", self.mainwnd._widget.login.userInfo)
        # self.strengthDisturb.initUserInfo(self.userInfo)
        # self.alocatMange.initUserInfo(self.userInfo)
        # self.PosEngin.slotInstallation()
        self.mainwnd._widget.login.close()

        self.mainwnd._widget.show()
        self.mainwnd.titleBar.show()
        self.mainwnd.center()
        # self.mainwnd.showMaximized()
def restart():
    qApp.quit()
    # QProcess 类的作用是启动一个外部的程序并与之交互，并且没有父子关系。
    p = QProcess()
    # applicationFilePath() 返回应用程序可执行文件的文件路径
    p.startDetached(qApp.applicationFilePath())
if __name__ == "__main__":
    # appctxt = ApplicationContext()
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    app = QApplication(sys.argv)
    widget = mainManage()
    basepath=os.path.split(os.path.abspath(__file__))[0]
    # path = basepath + "\\icons\\ElegantDark.qss"
    # path = basepath + "\\icons\\rcc\\qss\\static\\baseStyle.qss"
    path=os.path.join(basepath,"./icons/ElegantDark.qss")
    with open(path, 'r', encoding="utf-8") as f:
        qssStyle = f.read()
    app.setStyleSheet(qssStyle)
    # exit_code = appctxt.app.exec_()
    exitCode = sys.exit(app.exec_())



python2: raw_input("please input any key to exit!")
python3: input("please input any key to exit!")