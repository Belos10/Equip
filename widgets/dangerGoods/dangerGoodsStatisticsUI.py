# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dangerGoodsStatisticsUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class DangerGoodsStatisticsUI(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1216, 755)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.widget = QtWidgets.QWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(0, 755))
        self.widget.setObjectName("widget")
        self.horizontalLayout_5.addWidget(self.widget)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_2.setSpacing(5)
        self.gridLayout_2.setObjectName("gridLayout_2")
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
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
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
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        self.gridLayout_2.addWidget(self.wg_directory, 0, 0, 1, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.tw_result = QtWidgets.QTableWidget(self.groupBox_2)
        self.tw_result.setMinimumSize(QtCore.QSize(400, 200))
        self.tw_result.setObjectName("tw_result")
        self.tw_result.setColumnCount(0)
        self.tw_result.setRowCount(0)
        self.verticalLayout_4.addWidget(self.tw_result)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.tb_input = QtWidgets.QPushButton(self.groupBox_2)
        self.tb_input.setMinimumSize(QtCore.QSize(50, 25))
        self.tb_input.setMaximumSize(QtCore.QSize(100, 25))
        self.tb_input.setObjectName("tb_input")
        self.horizontalLayout_7.addWidget(self.tb_input)
        self.tb_output = QtWidgets.QPushButton(self.groupBox_2)
        self.tb_output.setMinimumSize(QtCore.QSize(50, 25))
        self.tb_output.setMaximumSize(QtCore.QSize(100, 25))
        self.tb_output.setObjectName("tb_output")
        self.horizontalLayout_7.addWidget(self.tb_output)
        self.tb_add = QtWidgets.QPushButton(self.groupBox_2)
        self.tb_add.setMinimumSize(QtCore.QSize(50, 25))
        self.tb_add.setMaximumSize(QtCore.QSize(100, 25))
        self.tb_add.setObjectName("tb_add")
        self.horizontalLayout_7.addWidget(self.tb_add)
        self.tb_delete = QtWidgets.QPushButton(self.groupBox_2)
        self.tb_delete.setMinimumSize(QtCore.QSize(50, 25))
        self.tb_delete.setMaximumSize(QtCore.QSize(100, 25))
        self.tb_delete.setObjectName("tb_delete")
        self.horizontalLayout_7.addWidget(self.tb_delete)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        self.gridLayout_2.addLayout(self.verticalLayout_4, 0, 1, 1, 1)
        self.horizontalLayout_5.addWidget(self.groupBox_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "阵地工程"))
        self.groupBox_2.setTitle(_translate("Form", "目录查询"))
        self.pb_firstSelect.setText(_translate("Form", "查询"))
        self.tb_input.setText(_translate("Form", "导入"))
        self.tb_output.setText(_translate("Form", "导出"))
        self.tb_add.setText(_translate("Form", "新增"))
        self.tb_delete.setText(_translate("Form", "删除"))
