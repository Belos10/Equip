# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'maintenManageSet.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Widget_Mainten_Manage_Set(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1109, 652)
        self.gridLayout_4 = QtWidgets.QGridLayout(Form)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setMaximumSize(QtCore.QSize(250, 16777215))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.le_first = QtWidgets.QLineEdit(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(70)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_first.sizePolicy().hasHeightForWidth())
        self.le_first.setSizePolicy(sizePolicy)
        self.le_first.setObjectName("le_first")
        self.horizontalLayout_7.addWidget(self.le_first)
        self.pb_firstSelect = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_firstSelect.sizePolicy().hasHeightForWidth())
        self.pb_firstSelect.setSizePolicy(sizePolicy)
        self.pb_firstSelect.setObjectName("pb_firstSelect")
        self.horizontalLayout_7.addWidget(self.pb_firstSelect)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.tw_first = QtWidgets.QTreeWidget(self.groupBox)
        self.tw_first.setObjectName("tw_first")
        self.tw_first.headerItem().setText(0, "1")
        self.verticalLayout_2.addWidget(self.tw_first)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox, 0, 0, 2, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tw_unit = QtWidgets.QTableWidget(self.groupBox_2)
        self.tw_unit.setObjectName("tw_unit")
        self.tw_unit.setColumnCount(3)
        self.tw_unit.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tw_unit.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_unit.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_unit.setHorizontalHeaderItem(2, item)
        self.verticalLayout.addWidget(self.tw_unit)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 1, 0, 1, 1)
        self.lb_unitID = QtWidgets.QLabel(self.groupBox_2)
        self.lb_unitID.setText("")
        self.lb_unitID.setObjectName("lb_unitID")
        self.gridLayout_2.addWidget(self.lb_unitID, 0, 1, 1, 1)
        self.pb_update = QtWidgets.QPushButton(self.groupBox_2)
        self.pb_update.setObjectName("pb_update")
        self.gridLayout_2.addWidget(self.pb_update, 0, 3, 2, 1)
        self.cb_isGroup = QtWidgets.QComboBox(self.groupBox_2)
        self.cb_isGroup.setObjectName("cb_isGroup")
        self.cb_isGroup.addItem("")
        self.cb_isGroup.addItem("")
        self.gridLayout_2.addWidget(self.cb_isGroup, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.gridLayout_4.addWidget(self.groupBox_2, 0, 1, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tw_publicEquip = QtWidgets.QTableWidget(self.groupBox_3)
        self.tw_publicEquip.setObjectName("tw_publicEquip")
        self.tw_publicEquip.setColumnCount(3)
        self.tw_publicEquip.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tw_publicEquip.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_publicEquip.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_publicEquip.setHorizontalHeaderItem(2, item)
        self.gridLayout_3.addWidget(self.tw_publicEquip, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_3, 1, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "编制数维护单位目录"))
        self.pb_firstSelect.setText(_translate("Form", "查询"))
        self.groupBox_2.setTitle(_translate("Form", "设置单位是否为旅团"))
        item = self.tw_unit.horizontalHeaderItem(0)
        item.setText(_translate("Form", "单位编号"))
        item = self.tw_unit.horizontalHeaderItem(1)
        item.setText(_translate("Form", "单位名字"))
        item = self.tw_unit.horizontalHeaderItem(2)
        item.setText(_translate("Form", "是否为旅团"))
        self.label_2.setText(_translate("Form", "当前单位编号："))
        self.label.setText(_translate("Form", "是否为旅团："))
        self.pb_update.setText(_translate("Form", "修改"))
        self.cb_isGroup.setItemText(0, _translate("Form", "是"))
        self.cb_isGroup.setItemText(1, _translate("Form", "否"))
        self.groupBox_3.setTitle(_translate("Form", "公用装备显示"))
        item = self.tw_publicEquip.horizontalHeaderItem(0)
        item.setText(_translate("Form", "装备编号"))
        item = self.tw_publicEquip.horizontalHeaderItem(1)
        item.setText(_translate("Form", "旅团编号"))
        item = self.tw_publicEquip.horizontalHeaderItem(2)
        item.setText(_translate("Form", "编制数"))
