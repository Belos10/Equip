# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_OrderPlan.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Widget_OrderPlan(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1123, 678)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setMaximumSize(QtCore.QSize(110, 16777215))
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setContentsMargins(0, 0, 5, 0)
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
        self.verticalLayout.addWidget(self.lw_yearChoose)
        self.tb_add = QtWidgets.QToolButton(self.groupBox)
        self.tb_add.setObjectName("tb_add")
        self.verticalLayout.addWidget(self.tb_add)
        self.tb_del = QtWidgets.QToolButton(self.groupBox)
        self.tb_del.setObjectName("tb_del")
        self.verticalLayout.addWidget(self.tb_del)
        self.horizontalLayout_6.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(300, 0))
        self.groupBox_2.setMaximumSize(QtCore.QSize(450, 16777215))
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.wg_directory = QtWidgets.QWidget(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wg_directory.sizePolicy().hasHeightForWidth())
        self.wg_directory.setSizePolicy(sizePolicy)
        self.wg_directory.setMinimumSize(QtCore.QSize(300, 0))
        self.wg_directory.setMaximumSize(QtCore.QSize(450, 16777215))
        self.wg_directory.setObjectName("wg_directory")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.wg_directory)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.le_first = QtWidgets.QLineEdit(self.wg_directory)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
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
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.tw_first = QtWidgets.QTreeWidget(self.wg_directory)
        self.tw_first.setObjectName("tw_first")
        self.verticalLayout_2.addWidget(self.tw_first)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.le_second = QtWidgets.QLineEdit(self.wg_directory)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
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
        self.verticalLayout_3.addWidget(self.tw_second)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        self.gridLayout_2.addWidget(self.wg_directory, 0, 2, 1, 1)
        self.horizontalLayout_6.addWidget(self.groupBox_2)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.txt_orderPlanYear = QtWidgets.QTextBrowser(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_orderPlanYear.sizePolicy().hasHeightForWidth())
        self.txt_orderPlanYear.setSizePolicy(sizePolicy)
        self.txt_orderPlanYear.setMinimumSize(QtCore.QSize(0, 30))
        self.txt_orderPlanYear.setMaximumSize(QtCore.QSize(16777215, 40))
        self.txt_orderPlanYear.setObjectName("txt_orderPlanYear")
        self.verticalLayout_4.addWidget(self.txt_orderPlanYear)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.tb_proof = QtWidgets.QTextBrowser(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_proof.sizePolicy().hasHeightForWidth())
        self.tb_proof.setSizePolicy(sizePolicy)
        self.tb_proof.setMinimumSize(QtCore.QSize(0, 30))
        self.tb_proof.setMaximumSize(QtCore.QSize(16777215, 30))
        self.tb_proof.setObjectName("tb_proof")
        self.horizontalLayout_5.addWidget(self.tb_proof)
        self.pb_proof = QtWidgets.QPushButton(Dialog)
        self.pb_proof.setMinimumSize(QtCore.QSize(0, 30))
        self.pb_proof.setMaximumSize(QtCore.QSize(16777215, 30))
        self.pb_proof.setObjectName("pb_proof")
        self.horizontalLayout_5.addWidget(self.pb_proof)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.orderResult = QtWidgets.QTableWidget(Dialog)
        self.orderResult.setObjectName("orderResult")
        self.orderResult.setColumnCount(0)
        self.orderResult.setRowCount(0)
        self.verticalLayout_4.addWidget(self.orderResult)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem)
        self.pb_input = QtWidgets.QPushButton(Dialog)
        self.pb_input.setObjectName("pb_input")
        self.horizontalLayout_8.addWidget(self.pb_input)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem1)
        self.pb_output = QtWidgets.QPushButton(Dialog)
        self.pb_output.setObjectName("pb_output")
        self.horizontalLayout_8.addWidget(self.pb_output)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem2)
        self.pb_outputToExcel = QtWidgets.QPushButton(Dialog)
        self.pb_outputToExcel.setObjectName("pb_outputToExcel")
        self.horizontalLayout_8.addWidget(self.pb_outputToExcel)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_6.addLayout(self.verticalLayout_4)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "年份筛选"))
        self.tb_add.setText(_translate("Dialog", "新增"))
        self.tb_del.setText(_translate("Dialog", "删除"))
        self.groupBox_2.setTitle(_translate("Dialog", "目录查询"))
        self.pb_firstSelect.setText(_translate("Dialog", "查询"))
        self.pb_secondSelect.setText(_translate("Dialog", "查询"))
        self.txt_orderPlanYear.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.pb_proof.setText(_translate("Dialog", "设置调拨依据"))
        self.pb_input.setText(_translate("Dialog", "导入数据包"))
        self.pb_output.setText(_translate("Dialog", "导出数据包"))
        self.pb_outputToExcel.setText(_translate("Dialog", "导出至Excel"))
