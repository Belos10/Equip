# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ServiceSupportNewUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class ServiceSupportNewUI(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1566, 1136)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.wg_directory = QtWidgets.QWidget(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wg_directory.sizePolicy().hasHeightForWidth())
        self.wg_directory.setSizePolicy(sizePolicy)
        self.wg_directory.setObjectName("wg_directory")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.wg_directory)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_2.addWidget(self.wg_directory)
        spacerItem = QtWidgets.QSpacerItem(1529, 13, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem1 = QtWidgets.QSpacerItem(80, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 3, 3, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 3, 5, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setMinimumSize(QtCore.QSize(50, 25))
        self.label_2.setMaximumSize(QtCore.QSize(100, 25))
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 3, 0, 1, 1)
        self.cb_selectedType = QtWidgets.QComboBox(self.groupBox_2)
        self.cb_selectedType.setMinimumSize(QtCore.QSize(0, 25))
        self.cb_selectedType.setObjectName("cb_selectedType")
        self.gridLayout.addWidget(self.cb_selectedType, 3, 2, 1, 1)
        self.pb_select = QtWidgets.QPushButton(self.groupBox_2)
        self.pb_select.setMinimumSize(QtCore.QSize(50, 25))
        self.pb_select.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pb_select.setObjectName("pb_select")
        self.gridLayout.addWidget(self.pb_select, 3, 4, 1, 1)
        self.gridLayout.setColumnStretch(0, 3)
        self.gridLayout.setColumnStretch(1, 3)
        self.gridLayout.setColumnStretch(2, 3)
        self.gridLayout.setColumnStretch(3, 3)
        self.gridLayout.setColumnStretch(4, 3)
        self.gridLayout.setColumnStretch(5, 3)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.lv_year = QtWidgets.QListView(self.groupBox_2)
        self.lv_year.setObjectName("lv_year")
        self.verticalLayout.addWidget(self.lv_year)
        self.pb_addYear = QtWidgets.QPushButton(self.groupBox_2)
        self.pb_addYear.setObjectName("pb_addYear")
        self.verticalLayout.addWidget(self.pb_addYear)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.tw_result = QtWidgets.QTableWidget(self.groupBox_2)
        self.tw_result.setMinimumSize(QtCore.QSize(400, 200))
        self.tw_result.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tw_result.setObjectName("tw_result")
        self.tw_result.setColumnCount(0)
        self.tw_result.setRowCount(0)
        self.horizontalLayout_2.addWidget(self.tw_result)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 9)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        spacerItem4 = QtWidgets.QSpacerItem(1529, 13, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tb_add = QtWidgets.QPushButton(self.groupBox_2)
        self.tb_add.setMinimumSize(QtCore.QSize(50, 25))
        self.tb_add.setMaximumSize(QtCore.QSize(120, 50))
        self.tb_add.setObjectName("tb_add")
        self.horizontalLayout.addWidget(self.tb_add)
        self.tb_del = QtWidgets.QPushButton(self.groupBox_2)
        self.tb_del.setMinimumSize(QtCore.QSize(50, 25))
        self.tb_del.setMaximumSize(QtCore.QSize(120, 50))
        self.tb_del.setObjectName("tb_del")
        self.horizontalLayout.addWidget(self.tb_del)
        self.tb_input = QtWidgets.QPushButton(self.groupBox_2)
        self.tb_input.setMinimumSize(QtCore.QSize(50, 25))
        self.tb_input.setMaximumSize(QtCore.QSize(120, 50))
        self.tb_input.setObjectName("tb_input")
        self.horizontalLayout.addWidget(self.tb_input)
        self.pb_output = QtWidgets.QPushButton(self.groupBox_2)
        self.pb_output.setMaximumSize(QtCore.QSize(120, 50))
        self.pb_output.setObjectName("pb_output")
        self.horizontalLayout.addWidget(self.pb_output)
        self.tb_outputToExcel = QtWidgets.QPushButton(self.groupBox_2)
        self.tb_outputToExcel.setMaximumSize(QtCore.QSize(120, 50))
        self.tb_outputToExcel.setObjectName("tb_outputToExcel")
        self.horizontalLayout.addWidget(self.tb_outputToExcel)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        spacerItem5 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem5)
        self.horizontalLayout_5.addWidget(self.groupBox_2)
        self.widget = QtWidgets.QWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(0, 755))
        self.widget.setObjectName("widget")
        self.horizontalLayout_5.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "阵地工程"))
        self.label_2.setText(_translate("Form", "    项目筛选"))
        self.pb_select.setText(_translate("Form", "查询"))
        self.label_5.setText(_translate("Form", "     年份筛选"))
        self.pb_addYear.setText(_translate("Form", "新增年份"))
        self.tb_add.setText(_translate("Form", "新增"))
        self.tb_del.setText(_translate("Form", "删除"))
        self.tb_input.setText(_translate("Form", "导入数据包"))
        self.pb_output.setText(_translate("Form", "导出数据包"))
        self.tb_outputToExcel.setText(_translate("Form", "导出至Excel"))