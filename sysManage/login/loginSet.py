from PyQt5.QtWidgets import QDialog,QLineEdit,QTableWidgetItem,QAbstractItemView,QMessageBox,QHeaderView
from widgets.login.loginSet import Widget_LoginSet
from database.strengthDisturbSql import selectAllDataAboutUnit
from database.loginSql import selectAllDataAboutLogin,insertIntoLogin,delFromLogin,findAllLoginAccontList,updateUserInfo
from PyQt5.Qt import Qt

class loginSet(QDialog, Widget_LoginSet):
    def __init__(self, parent=None):
        super(loginSet,self).__init__(parent)
        self.setupUi(self)
        self.initWidgets()

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

    def initWidgets(self):
        self.tw_unitResult.clear()
        self.tw_userInfo.clear()
        self.unitResult = []
        selectSuccess = selectAllDataAboutUnit(self.unitResult)
        if selectSuccess != True:
            QMessageBox.information(self, "初始化", "初始化登录界面失败")
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
        reply = QMessageBox.question(self, '删除', '是否删除该用户？', QMessageBox.Yes, QMessageBox.Cancel)
        if reply == QMessageBox.Cancel:
            return
        else:
            delFromLogin(self.le_accont.text())
            reply = QMessageBox.question(self, '删除', '删除成功', QMessageBox.Yes)
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
                reply = QMessageBox.question(self, '新增', '新增失败，账号存在，请重新输入', QMessageBox.Yes)
                return

        if accont == "":
            reply = QMessageBox.question(self, '新增', '新增失败，请输入账号', QMessageBox.Yes)
            return
        else:
            insertIntoLogin(accont, name, password, role, unitID)
            reply = QMessageBox.question(self, '新增', '新增成功', QMessageBox.Yes)
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
            reply = QMessageBox.question(self, '修改', '修改失败，账号无法修改', QMessageBox.Yes)
            self.le_accont.setText(self.currentAccont)
            return

        updateUserInfo(accont, name, password, role, unitID)
        reply = QMessageBox.question(self, '修改', '修改成功', QMessageBox.Yes)
        self.initWidgets()
        return