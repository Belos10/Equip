# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loginSet.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Widget_LoginSet(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1068, 800)
        self.gridLayout_4 = QtWidgets.QGridLayout(Form)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tw_unitResult = QtWidgets.QTableWidget(self.groupBox_3)
        self.tw_unitResult.setObjectName("tw_unitResult")
        self.tw_unitResult.setColumnCount(0)
        self.tw_unitResult.setRowCount(0)
        self.gridLayout_3.addWidget(self.tw_unitResult, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_3, 0, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.tw_userInfo = QtWidgets.QTableWidget(self.groupBox)
        self.tw_userInfo.setObjectName("tw_userInfo")
        self.tw_userInfo.setColumnCount(0)
        self.tw_userInfo.setRowCount(0)
        self.gridLayout.addWidget(self.tw_userInfo, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox, 1, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.cb_role = QtWidgets.QComboBox(self.groupBox_2)
        self.cb_role.setObjectName("cb_role")
        self.cb_role.addItem("")
        self.cb_role.addItem("")
        self.cb_role.addItem("")
        self.cb_role.addItem("")
        self.gridLayout_2.addWidget(self.cb_role, 1, 1, 1, 1)
        self.le_accont = QtWidgets.QLineEdit(self.groupBox_2)
        self.le_accont.setObjectName("le_accont")
        self.gridLayout_2.addWidget(self.le_accont, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 5, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1)
        self.le_unitID = QtWidgets.QLineEdit(self.groupBox_2)
        self.le_unitID.setObjectName("le_unitID")
        self.gridLayout_2.addWidget(self.le_unitID, 1, 4, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 1, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 0, 2, 1, 1)
        self.le_name = QtWidgets.QLineEdit(self.groupBox_2)
        self.le_name.setObjectName("le_name")
        self.gridLayout_2.addWidget(self.le_name, 0, 4, 1, 1)
        self.pb_del = QtWidgets.QPushButton(self.groupBox_2)
        self.pb_del.setObjectName("pb_del")
        self.gridLayout_2.addWidget(self.pb_del, 1, 7, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem3, 1, 5, 1, 1)
        self.pb_add = QtWidgets.QPushButton(self.groupBox_2)
        self.pb_add.setObjectName("pb_add")
        self.gridLayout_2.addWidget(self.pb_add, 1, 6, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 6, 1, 1)
        self.le_pswd = QtWidgets.QLineEdit(self.groupBox_2)
        self.le_pswd.setObjectName("le_pswd")
        self.gridLayout_2.addWidget(self.le_pswd, 0, 7, 1, 3)
        self.pb_update = QtWidgets.QPushButton(self.groupBox_2)
        self.pb_update.setObjectName("pb_update")
        self.gridLayout_2.addWidget(self.pb_update, 1, 8, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_2, 2, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox_3.setTitle(_translate("Form", "单位信息"))
        self.groupBox.setTitle(_translate("Form", "用户信息"))
        self.groupBox_2.setTitle(_translate("Form", "信息管理"))
        self.cb_role.setItemText(0, _translate("Form", "机关"))
        self.cb_role.setItemText(1, _translate("Form", "基地"))
        self.cb_role.setItemText(2, _translate("Form", "旅团"))
        self.cb_role.setItemText(3, _translate("Form", "库存"))
        self.label_5.setText(_translate("Form", "开始单位号："))
        self.label_2.setText(_translate("Form", "单位名字："))
        self.label_4.setText(_translate("Form", "角色："))
        self.label.setText(_translate("Form", "账号："))
        self.pb_del.setText(_translate("Form", "删除"))
        self.pb_add.setText(_translate("Form", "增加"))
        self.label_3.setText(_translate("Form", "密码："))
        self.pb_update.setText(_translate("Form", "修改"))
