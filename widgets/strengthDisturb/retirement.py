# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'retirement.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Widget_Retirement(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1094, 791)
        self.gridLayout_3 = QtWidgets.QGridLayout(Form)
        self.gridLayout_3.setContentsMargins(10, 0, 10, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName("gridLayout")
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
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(-1, -1, -1, 5)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.le_first = QtWidgets.QLineEdit(self.wg_directory)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(70)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_first.sizePolicy().hasHeightForWidth())
        self.le_first.setSizePolicy(sizePolicy)
        self.le_first.setObjectName("le_first")
        self.horizontalLayout.addWidget(self.le_first)
        self.pb_firstSelect = QtWidgets.QPushButton(self.wg_directory)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_firstSelect.sizePolicy().hasHeightForWidth())
        self.pb_firstSelect.setSizePolicy(sizePolicy)
        self.pb_firstSelect.setObjectName("pb_firstSelect")
        self.horizontalLayout.addWidget(self.pb_firstSelect)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tw_first = QtWidgets.QTreeWidget(self.wg_directory)
        self.tw_first.setObjectName("tw_first")
        self.tw_first.headerItem().setText(0, "1")
        self.verticalLayout.addWidget(self.tw_first)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(-1, -1, -1, 5)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.le_second = QtWidgets.QLineEdit(self.wg_directory)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(70)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_second.sizePolicy().hasHeightForWidth())
        self.le_second.setSizePolicy(sizePolicy)
        self.le_second.setObjectName("le_second")
        self.horizontalLayout_2.addWidget(self.le_second)
        self.pb_secondSelect = QtWidgets.QPushButton(self.wg_directory)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_secondSelect.sizePolicy().hasHeightForWidth())
        self.pb_secondSelect.setSizePolicy(sizePolicy)
        self.pb_secondSelect.setObjectName("pb_secondSelect")
        self.horizontalLayout_2.addWidget(self.pb_secondSelect)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.tw_second = QtWidgets.QTreeWidget(self.wg_directory)
        self.tw_second.setObjectName("tw_second")
        self.tw_second.headerItem().setText(0, "1")
        self.verticalLayout_3.addWidget(self.tw_second)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        self.gridLayout.addWidget(self.wg_directory, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_2, 0, 1, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(Form)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tw_result = QtWidgets.QTableWidget(self.groupBox_3)
        self.tw_result.setObjectName("tw_result")
        self.tw_result.setColumnCount(0)
        self.tw_result.setRowCount(0)
        self.gridLayout_2.addWidget(self.tw_result, 0, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(-1, 5, -1, 5)
        self.horizontalLayout_5.setSpacing(10)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.pb_save = QtWidgets.QPushButton(self.groupBox_3)
        self.pb_save.setMinimumSize(QtCore.QSize(100, 20))
        self.pb_save.setObjectName("pb_save")
        self.horizontalLayout_5.addWidget(self.pb_save)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.pb_input = QtWidgets.QPushButton(self.groupBox_3)
        self.pb_input.setObjectName("pb_input")
        self.horizontalLayout_5.addWidget(self.pb_input)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.pb_output = QtWidgets.QPushButton(self.groupBox_3)
        self.pb_output.setObjectName("pb_output")
        self.horizontalLayout_5.addWidget(self.pb_output)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.pb_outputToExcel = QtWidgets.QPushButton(self.groupBox_3)
        self.pb_outputToExcel.setObjectName("pb_outputToExcel")
        self.horizontalLayout_5.addWidget(self.pb_outputToExcel)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 1, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_3, 0, 2, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setMinimumSize(QtCore.QSize(85, 0))
        self.groupBox.setMaximumSize(QtCore.QSize(85, 16777215))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 5)
        self.gridLayout_4.setHorizontalSpacing(10)
        self.gridLayout_4.setVerticalSpacing(5)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.lw_year = QtWidgets.QListWidget(self.groupBox)
        self.lw_year.setObjectName("lw_year")
        self.gridLayout_4.addWidget(self.lw_year, 0, 0, 1, 1)
        self.tb_del = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_del.sizePolicy().hasHeightForWidth())
        self.tb_del.setSizePolicy(sizePolicy)
        self.tb_del.setMaximumSize(QtCore.QSize(70, 25))
        self.tb_del.setObjectName("tb_del")
        self.gridLayout_4.addWidget(self.tb_del, 2, 0, 1, 1)
        self.tb_add = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_add.sizePolicy().hasHeightForWidth())
        self.tb_add.setSizePolicy(sizePolicy)
        self.tb_add.setMaximumSize(QtCore.QSize(70, 25))
        self.tb_add.setObjectName("tb_add")
        self.gridLayout_4.addWidget(self.tb_add, 1, 0, 1, 1)
        self.gridLayout_4.setRowStretch(0, 25)
        self.gridLayout_4.setRowStretch(1, 2)
        self.gridLayout_4.setRowStretch(2, 2)
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)

        self.retranslateUi(Form)
        self.tw_first.setMinimumSize(300, 500)
        self.tw_second.setMinimumSize(300, 500)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox_2.setTitle(_translate("Form", "目录查询"))
        self.pb_firstSelect.setText(_translate("Form", "查询"))
        self.pb_secondSelect.setText(_translate("Form", "查询"))
        self.groupBox_3.setTitle(_translate("Form", "查询结果"))
        self.pb_save.setText(_translate("Form", "保存"))
        self.pb_input.setText(_translate("Form", "导入数据包"))
        self.pb_output.setText(_translate("Form", "导出数据包"))
        self.pb_outputToExcel.setText(_translate("Form", "导出到Excel"))
        self.groupBox.setTitle(_translate("Form", "年份筛选"))
        self.tb_del.setText(_translate("Form", "删除"))
        self.tb_add.setText(_translate("Form", "新增"))
