# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'armyTransfer.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Widget_Army_Transfer(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1198, 752)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(0, 5, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.widget)
        self.groupBox.setMaximumSize(QtCore.QSize(110, 16777215))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setContentsMargins(5, -1, 5, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lw_yearChoose = QtWidgets.QListWidget(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lw_yearChoose.sizePolicy().hasHeightForWidth())
        self.lw_yearChoose.setSizePolicy(sizePolicy)
        self.lw_yearChoose.setMaximumSize(QtCore.QSize(80, 16777215))
        self.lw_yearChoose.setObjectName("lw_yearChoose")
        item = QtWidgets.QListWidgetItem()
        self.lw_yearChoose.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.lw_yearChoose.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.lw_yearChoose.addItem(item)
        self.verticalLayout.addWidget(self.lw_yearChoose)
        self.tb_add = QtWidgets.QPushButton(self.groupBox)
        self.tb_add.setMaximumSize(QtCore.QSize(75, 16777215))
        self.tb_add.setObjectName("tb_add")
        self.verticalLayout.addWidget(self.tb_add)
        self.tb_del = QtWidgets.QPushButton(self.groupBox)
        self.tb_del.setMaximumSize(QtCore.QSize(75, 16777215))
        self.tb_del.setObjectName("tb_del")
        self.verticalLayout.addWidget(self.tb_del)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.widget)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setContentsMargins(5, 11, 5, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tw_result = QtWidgets.QTableWidget(self.groupBox_2)
        self.tw_result.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tw_result.setObjectName("tw_result")
        self.tw_result.setColumnCount(19)
        self.tw_result.setRowCount(2)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setHorizontalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setHorizontalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setHorizontalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setHorizontalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setHorizontalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setHorizontalHeaderItem(15, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setHorizontalHeaderItem(16, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setHorizontalHeaderItem(17, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setHorizontalHeaderItem(18, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setItem(0, 8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setItem(0, 9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setItem(0, 11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setItem(0, 12, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setItem(0, 14, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setItem(0, 15, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setItem(0, 16, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setItem(0, 17, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setItem(0, 18, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setItem(1, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setItem(1, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setItem(1, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setItem(1, 5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setItem(1, 6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setItem(1, 7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setItem(1, 8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setItem(1, 9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setItem(1, 10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setItem(1, 11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setItem(1, 12, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setItem(1, 13, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setItem(1, 14, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setItem(1, 15, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setItem(1, 16, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setItem(1, 17, item)
        item = QtWidgets.QTableWidgetItem()
        self.tw_result.setItem(1, 18, item)
        self.verticalLayout_2.addWidget(self.tw_result)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setContentsMargins(-1, 10, -1, 10)
        self.gridLayout.setObjectName("gridLayout")
        self.pb_outputToExcel = QtWidgets.QPushButton(self.groupBox_2)
        self.pb_outputToExcel.setObjectName("pb_outputToExcel")
        self.gridLayout.addWidget(self.pb_outputToExcel, 0, 7, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.pb_save = QtWidgets.QPushButton(self.groupBox_2)
        self.pb_save.setObjectName("pb_save")
        self.gridLayout.addWidget(self.pb_save, 0, 5, 1, 1)
        self.pb_del = QtWidgets.QPushButton(self.groupBox_2)
        self.pb_del.setObjectName("pb_del")
        self.gridLayout.addWidget(self.pb_del, 0, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 10, 1, 1)
        self.pb_add = QtWidgets.QPushButton(self.groupBox_2)
        self.pb_add.setObjectName("pb_add")
        self.gridLayout.addWidget(self.pb_add, 0, 1, 1, 1)
        self.pb_equipSet = QtWidgets.QPushButton(self.groupBox_2)
        self.pb_equipSet.setObjectName("pb_equipSet")
        self.gridLayout.addWidget(self.pb_equipSet, 0, 9, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 0, 4, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 0, 6, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 0, 8, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.gridLayout_3.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "年份筛选"))
        __sortingEnabled = self.lw_yearChoose.isSortingEnabled()
        self.lw_yearChoose.setSortingEnabled(False)
        item = self.lw_yearChoose.item(0)
        item.setText(_translate("Form", "全部"))
        item = self.lw_yearChoose.item(1)
        item.setText(_translate("Form", "2001年"))
        item = self.lw_yearChoose.item(2)
        item.setText(_translate("Form", "2002年"))
        self.lw_yearChoose.setSortingEnabled(__sortingEnabled)
        self.tb_add.setText(_translate("Form", "新增"))
        self.tb_del.setText(_translate("Form", "删除"))
        self.groupBox_2.setTitle(_translate("Form", "查询结果"))
        item = self.tw_result.verticalHeaderItem(0)
        item.setText(_translate("Form", "New Row"))
        item = self.tw_result.verticalHeaderItem(1)
        item.setText(_translate("Form", "New Row"))
        item = self.tw_result.horizontalHeaderItem(0)
        item.setText(_translate("Form", "New Column"))
        item = self.tw_result.horizontalHeaderItem(1)
        item.setText(_translate("Form", "New Column"))
        item = self.tw_result.horizontalHeaderItem(2)
        item.setText(_translate("Form", "New Column"))
        item = self.tw_result.horizontalHeaderItem(3)
        item.setText(_translate("Form", "New Column"))
        item = self.tw_result.horizontalHeaderItem(4)
        item.setText(_translate("Form", "New Column"))
        item = self.tw_result.horizontalHeaderItem(5)
        item.setText(_translate("Form", "New Column"))
        item = self.tw_result.horizontalHeaderItem(6)
        item.setText(_translate("Form", "New Column"))
        item = self.tw_result.horizontalHeaderItem(7)
        item.setText(_translate("Form", "New Column"))
        item = self.tw_result.horizontalHeaderItem(8)
        item.setText(_translate("Form", "New Column"))
        item = self.tw_result.horizontalHeaderItem(9)
        item.setText(_translate("Form", "New Column"))
        item = self.tw_result.horizontalHeaderItem(10)
        item.setText(_translate("Form", "New Column"))
        item = self.tw_result.horizontalHeaderItem(11)
        item.setText(_translate("Form", "New Column"))
        item = self.tw_result.horizontalHeaderItem(12)
        item.setText(_translate("Form", "New Column"))
        item = self.tw_result.horizontalHeaderItem(13)
        item.setText(_translate("Form", "New Column"))
        item = self.tw_result.horizontalHeaderItem(14)
        item.setText(_translate("Form", "New Column"))
        item = self.tw_result.horizontalHeaderItem(15)
        item.setText(_translate("Form", "New Column"))
        item = self.tw_result.horizontalHeaderItem(16)
        item.setText(_translate("Form", "New Column"))
        item = self.tw_result.horizontalHeaderItem(17)
        item.setText(_translate("Form", "New Column"))
        item = self.tw_result.horizontalHeaderItem(18)
        item.setText(_translate("Form", "New Column"))
        __sortingEnabled = self.tw_result.isSortingEnabled()
        self.tw_result.setSortingEnabled(False)
        item = self.tw_result.item(0, 0)
        item.setText(_translate("Form", "序号"))
        item = self.tw_result.item(0, 1)
        item.setText(_translate("Form", "调拨单信息"))
        item = self.tw_result.item(0, 8)
        item.setText(_translate("Form", "交装单位"))
        item = self.tw_result.item(0, 11)
        item.setText(_translate("Form", "接装单位"))
        item = self.tw_result.item(0, 14)
        item.setText(_translate("Form", "装备名称"))
        item = self.tw_result.item(0, 15)
        item.setText(_translate("Form", "计量单位"))
        item = self.tw_result.item(0, 16)
        item.setText(_translate("Form", "应发数"))
        item = self.tw_result.item(0, 18)
        item.setText(_translate("Form", "备注"))
        item = self.tw_result.item(1, 1)
        item.setText(_translate("Form", "调拨单号"))
        item = self.tw_result.item(1, 2)
        item.setText(_translate("Form", "调拨日期"))
        item = self.tw_result.item(1, 3)
        item.setText(_translate("Form", "调拨依据"))
        item = self.tw_result.item(1, 4)
        item.setText(_translate("Form", "调拨"))
        item = self.tw_result.item(1, 5)
        item.setText(_translate("Form", "调拨方式"))
        item = self.tw_result.item(1, 6)
        item.setText(_translate("Form", "运输方式"))
        item = self.tw_result.item(1, 7)
        item.setText(_translate("Form", "有效日期"))
        item = self.tw_result.item(1, 8)
        item.setText(_translate("Form", "单位名称"))
        item = self.tw_result.item(1, 9)
        item.setText(_translate("Form", "联系人"))
        item = self.tw_result.item(1, 10)
        item.setText(_translate("Form", "联系电话"))
        item = self.tw_result.item(1, 11)
        item.setText(_translate("Form", "单位名称"))
        item = self.tw_result.item(1, 12)
        item.setText(_translate("Form", "联系人"))
        item = self.tw_result.item(1, 13)
        item.setText(_translate("Form", "联系电话"))
        item = self.tw_result.item(1, 16)
        item.setText(_translate("Form", "质量"))
        item = self.tw_result.item(1, 17)
        item.setText(_translate("Form", "数量"))
        self.tw_result.setSortingEnabled(__sortingEnabled)
        self.pb_outputToExcel.setText(_translate("Form", "导出至Excel"))
        self.pb_save.setText(_translate("Form", "保存"))
        self.pb_del.setText(_translate("Form", "删除"))
        self.pb_add.setText(_translate("Form", "新增"))
        self.pb_equipSet.setText(_translate("Form", "装备设置"))
