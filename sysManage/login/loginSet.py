from PyQt5.QtCore import QProcess
from PyQt5.QtWidgets import QDialog, QLineEdit, QTableWidgetItem, QAbstractItemView, QMessageBox, QHeaderView, qApp

from database.connectAndDisSql import backUp, restore
# from main import restart
from widgets.login.loginSet import Widget_LoginSet
from database.strengthDisturbSql import selectAllDataAboutUnit
from database.loginSql import selectAllDataAboutLogin,insertIntoLogin,delFromLogin,findAllLoginAccontList,updateUserInfo
from PyQt5.Qt import Qt
from sysManage.component import getMessageBox
import os

class loginSet(QDialog, Widget_LoginSet):
    def __init__(self, parent=None):
        super(loginSet,self).__init__(parent)
        self.setupUi(self)
        self.initWidgets()
        self.basepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        self.tw_unitResult.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tw_userInfo.setSelectionMode(QAbstractItemView.SingleSelection)

        self.tw_userInfo.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tw_unitResult.setSelectionMode(QAbstractItemView.SingleSelection)

        self.tw_unitResult.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tw_userInfo.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tw_userInfo.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tw_unitResult.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.tw_userInfo.verticalHeader().hide()
        self.tw_unitResult.verticalHeader().hide()

        self.signalConnect()

    def signalConnect(self):
        self.tw_userInfo.itemClicked.connect(self.slotClickedItem)

        self.pb_add.clicked.connect(self.slotAddUserInfo)

        self.pb_del.clicked.connect(self.slotDelUserInfo)

        self.pb_update.clicked.connect(self.slotUpdateUserInfo)
        self.pb_backUp.clicked.connect(self.slotBackUp)
        self.pb_restore.clicked.connect(self.slotRestore)


    def initWidgets(self):
        self.tw_unitResult.clear()
        self.tw_userInfo.clear()
        self.unitResult = []
        selectSuccess = selectAllDataAboutUnit(self.unitResult)
        if selectSuccess != True:
            getMessageBox("初始化", "初始化登录界面失败", True, False)
            return
        self.userInfo = selectAllDataAboutLogin()

        userInfoTitle = ['账号', '名字', '密码', '权限', '单位根单位的上级单位']
        unitInfoTitle = ['单位编号', '单位名字', '上级单位编号', '单位别名', '是否为旅团']


        self.tw_userInfo.setColumnCount(len(userInfoTitle))
        self.tw_userInfo.setHorizontalHeaderLabels(userInfoTitle)
        self.tw_unitResult.setColumnCount(len(unitInfoTitle))
        self.tw_unitResult.setHorizontalHeaderLabels(unitInfoTitle)

        self.tw_unitResult.setRowCount(len(self.unitResult))
        self.tw_userInfo.setRowCount(len(self.userInfo))

        for i, user in enumerate(self.userInfo):
            item = QTableWidgetItem()
            item.setText(user[0])
            self.tw_userInfo.setItem(i, 0, item)
            item = QTableWidgetItem()
            item.setText(user[1])
            self.tw_userInfo.setItem(i, 1, item)
            item = QTableWidgetItem()
            item.setText(user[2])
            self.tw_userInfo.setItem(i, 2, item)
            item = QTableWidgetItem()
            item.setText(user[3])
            self.tw_userInfo.setItem(i, 3, item)
            item = QTableWidgetItem()
            item.setText(user[4])
            self.tw_userInfo.setItem(i, 4, item)

        for i, unitInfo in enumerate(self.unitResult):
            item = QTableWidgetItem()
            item.setText(unitInfo[0])
            self.tw_unitResult.setItem(i, 0, item)
            item = QTableWidgetItem()
            item.setText(unitInfo[1])
            self.tw_unitResult.setItem(i, 1, item)
            item = QTableWidgetItem()
            item.setText(unitInfo[2])
            self.tw_unitResult.setItem(i, 2, item)
            item = QTableWidgetItem()
            item.setText(unitInfo[3])
            self.tw_unitResult.setItem(i, 3, item)
            item = QTableWidgetItem()
            item.setText(unitInfo[4])
            self.tw_unitResult.setItem(i, 4, item)

    def slotDelUserInfo(self):
        reply = getMessageBox('删除', '是否删除该用户？', True, True)
        if reply == QMessageBox.Cancel:
            return
        else:
            delFromLogin(self.le_accont.text())
            getMessageBox('删除', '删除成功', True, False)
            self.initWidgets()

    def slotAddUserInfo(self):
        accont = self.le_accont.text()
        name = self.le_name.text()
        password = self.le_pswd.text()
        role = self.cb_role.currentText()
        unitID = self.le_unitID.text()
        accontList = findAllLoginAccontList()

        for ID in accontList:
            if accont == ID:
                getMessageBox('新增', '新增失败，账号存在，请重新输入', True, False)
                return

        if accont == "":
            getMessageBox('新增', '新增失败，请输入账号', True, False)
            return
        else:
            insertIntoLogin(accont, name, password, role, unitID)
            getMessageBox('新增', '新增成功', True, False)
            self.initWidgets()
            return

    def slotClickedItem(self):
        row = self.tw_userInfo.currentRow()
        role = self.tw_userInfo.item(row, 3).text()
        self.currentAccont = self.tw_userInfo.item(row, 0).text()
        self.le_accont.setText(self.tw_userInfo.item(row, 0).text())
        self.le_name.setText(self.tw_userInfo.item(row, 1).text())
        self.le_pswd.setText(self.tw_userInfo.item(row, 2).text())
        self.le_unitID.setText(self.tw_userInfo.item(row, 4).text())
        if role == "机关":
            self.cb_role.setCurrentIndex(0)
        elif role == "基地":
            self.cb_role.setCurrentIndex(1)
        elif role == "旅团":
            self.cb_role.setCurrentIndex(2)
        elif role == "库存":
            self.cb_role.setCurrentIndex(3)

    def slotUpdateUserInfo(self):
        accont = self.le_accont.text()
        name = self.le_name.text()
        password = self.le_pswd.text()
        role = self.cb_role.currentText()
        unitID = self.le_unitID.text()
        accontList = findAllLoginAccontList()

        if accont != self.currentAccont:
            getMessageBox('修改', '修改失败，账号无法修改', True, False)
            self.le_accont.setText(self.currentAccont)
            return

        updateUserInfo(accont, name, password, role, unitID)
        getMessageBox('修改', '修改成功', True, False)
        self.initWidgets()
        return



    def slotBackUp(self):
        self.setDisabled(True)
        backUp(self.basepath)
        getMessageBox('备份', '备份成功！', True, False)
        self.setDisabled(False)


    def slotRestore(self):
        self.setDisabled(True)
        restore(self.basepath)
        getMessageBox('恢复', '恢复备份成功！', True, False)
        self.setDisabled(False)

