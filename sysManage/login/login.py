import re

from PyQt5.QtWidgets import QDialog,QLineEdit
from widgets.login.login import Widget_Login
from database.loginSql import findAllLoginAccontList
from PyQt5.Qt import Qt

class login(QDialog, Widget_Login):

    def __init__(self, parent=None):
        super(login,self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("核化装备管理系统登录")
        self.initLoginWidget()
        self.le_pswd.setEchoMode(QLineEdit.Password)
        self.le_accont.setText("root")
        self.le_pswd.setText("123456")
        flags = Qt.Dialog
        flags = flags | Qt.WindowTitleHint | Qt.CustomizeWindowHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint
        self.setWindowFlags(flags)

    def initLoginWidget(self):
        self.le_accont.setPlaceholderText("请输入账号")
        self.le_pswd.setPlaceholderText("请输入密码")