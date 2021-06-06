import re

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QDialog,QLineEdit
# from widgets.login.login import Widget_Login
from database.loginSql import findAllLoginAccontList
from PyQt5.Qt import Qt

from widgets.login.loginNew import Widget_Login_New


class login(QDialog, Widget_Login_New):

    def __init__(self, parent=None):
        super(login,self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("核化装备管理系统登录")
        self.initLoginWidget()
        self._startPos = None
        self._endPos = None
        self._tracking = False
        self.le_pswd.setEchoMode(QLineEdit.Password)
        self.le_accont.setText("root")
        self.le_pswd.setText("123456")
        # flags = Qt.Dialog
        # flags = flags | Qt.WindowTitleHint | Qt.CustomizeWindowHint | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint
        # self.setWindowFlags(flags)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

    def initLoginWidget(self):
        self.le_accont.setPlaceholderText("请输入账号")
        self.le_pswd.setPlaceholderText("请输入密码")

    def mouseMoveEvent(self, e: QMouseEvent):  # 重写移动事件
        if self._tracking:
            self._endPos = e.pos() - self._startPos
            self.move(self.pos() + self._endPos)

    def mousePressEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._startPos = QPoint(e.x(), e.y())
            self._tracking = True

    def mouseReleaseEvent(self, e: QMouseEvent):
        if e.button() == Qt.LeftButton:
            self._tracking = False
            self._startPos = None

