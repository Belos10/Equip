# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'maintenanceContractSigningUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class MaintenanceContractSigningUI(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1479, 871)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setContentsMargins(10, 0, 10, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName("gridLayout")
        self.pb_select = QtWidgets.QPushButton(self.groupBox_2)
        self.pb_select.setMinimumSize(QtCore.QSize(100, 25))
        self.pb_select.setObjectName("pb_select")
        self.gridLayout.addWidget(self.pb_select, 2, 8, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 0, 1, 1)
        self.le_contactNo = QtWidgets.QLineEdit(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_contactNo.sizePolicy().hasHeightForWidth())
        self.le_contactNo.setSizePolicy(sizePolicy)
        self.le_contactNo.setMinimumSize(QtCore.QSize(100, 25))
        self.le_contactNo.setMaximumSize(QtCore.QSize(100, 25))
        self.le_contactNo.setObjectName("le_contactNo")
        self.gridLayout.addWidget(self.le_contactNo, 2, 2, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 2, 5, 1, 1)
        self.le_Unit = QtWidgets.QLineEdit(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_Unit.sizePolicy().hasHeightForWidth())
        self.le_Unit.setSizePolicy(sizePolicy)
        self.le_Unit.setMaximumSize(QtCore.QSize(100, 25))
        self.le_Unit.setObjectName("le_Unit")
        self.gridLayout.addWidget(self.le_Unit, 2, 6, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 2, 7, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setMinimumSize(QtCore.QSize(50, 25))
        self.label_2.setMaximumSize(QtCore.QSize(100, 25))
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(80, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 2, 3, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 2, 9, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(50, 25))
        self.label_3.setMaximumSize(QtCore.QSize(150, 25))
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 4, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        spacerItem6 = QtWidgets.QSpacerItem(40, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem6)
        self.tw_result = QtWidgets.QTableWidget(self.groupBox_2)
        self.tw_result.setMinimumSize(QtCore.QSize(400, 200))
        self.tw_result.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tw_result.setObjectName("tw_result")
        self.tw_result.setColumnCount(0)
        self.tw_result.setRowCount(0)
        self.verticalLayout_2.addWidget(self.tw_result)
        spacerItem7 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem7)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tb_add = QtWidgets.QToolButton(self.groupBox_2)
        self.tb_add.setMinimumSize(QtCore.QSize(50, 25))
        self.tb_add.setMaximumSize(QtCore.QSize(120, 50))
        self.tb_add.setObjectName("tb_add")
        self.horizontalLayout.addWidget(self.tb_add)
        self.tb_del = QtWidgets.QToolButton(self.groupBox_2)
        self.tb_del.setMinimumSize(QtCore.QSize(50, 25))
        self.tb_del.setMaximumSize(QtCore.QSize(120, 50))
        self.tb_del.setObjectName("tb_del")
        self.horizontalLayout.addWidget(self.tb_del)
        self.tb_outputToExcel = QtWidgets.QToolButton(self.groupBox_2)
        self.tb_outputToExcel.setMaximumSize(QtCore.QSize(120, 50))
        self.tb_outputToExcel.setObjectName("tb_outputToExcel")
        self.horizontalLayout.addWidget(self.tb_outputToExcel)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 1, 1, 1)
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
        self.gridLayout_2.addWidget(self.wg_directory, 0, 0, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(10, 10, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem8, 1, 1, 1, 1)
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
        self.pb_select.setText(_translate("Form", "查询"))
        self.label_2.setText(_translate("Form", "合同号"))
        self.label_3.setText(_translate("Form", "承制单位"))
        self.tb_add.setText(_translate("Form", "新增"))
        self.tb_del.setText(_translate("Form", "删除"))
        self.tb_outputToExcel.setText(_translate("Form", "导出至Excel"))
