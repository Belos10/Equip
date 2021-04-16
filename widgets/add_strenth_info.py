# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_strenth_info.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Add_Strenth_Info(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1133, 789)
        Form.setWindowOpacity(1.0)
        Form.setStyleSheet("QWidget {background-color:rgb(240, 240, 240)}")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.textBrowser = QtWidgets.QTextBrowser(self.frame)
        self.textBrowser.setMaximumSize(QtCore.QSize(16777215, 50))
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setEnabled(True)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1085, 561))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.tableWidget = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setKerning(True)
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(120)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.horizontalLayout_9.addWidget(self.tableWidget)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pb_Increase = QtWidgets.QPushButton(self.frame)
        self.pb_Increase.setMaximumSize(QtCore.QSize(75, 23))
        self.pb_Increase.setObjectName("pb_Increase")
        self.horizontalLayout.addWidget(self.pb_Increase)
        self.pb_Save = QtWidgets.QPushButton(self.frame)
        self.pb_Save.setMaximumSize(QtCore.QSize(75, 23))
        self.pb_Save.setObjectName("pb_Save")
        self.horizontalLayout.addWidget(self.pb_Save)
        self.pb_Export = QtWidgets.QPushButton(self.frame)
        self.pb_Export.setMaximumSize(QtCore.QSize(75, 23))
        self.pb_Export.setObjectName("pb_Export")
        self.horizontalLayout.addWidget(self.pb_Export)
        self.pb_BulkImport = QtWidgets.QPushButton(self.frame)
        self.pb_BulkImport.setMaximumSize(QtCore.QSize(75, 23))
        self.pb_BulkImport.setObjectName("pb_BulkImport")
        self.horizontalLayout.addWidget(self.pb_BulkImport)
        self.pb_DownloadMode = QtWidgets.QPushButton(self.frame)
        self.pb_DownloadMode.setMaximumSize(QtCore.QSize(75, 23))
        self.pb_DownloadMode.setObjectName("pb_DownloadMode")
        self.horizontalLayout.addWidget(self.pb_DownloadMode)
        self.pb_Delete = QtWidgets.QPushButton(self.frame)
        self.pb_Delete.setMaximumSize(QtCore.QSize(75, 23))
        self.pb_Delete.setObjectName("pb_Delete")
        self.horizontalLayout.addWidget(self.pb_Delete)
        self.pb_back = QtWidgets.QPushButton(self.frame)
        self.pb_back.setMaximumSize(QtCore.QSize(75, 23))
        self.pb_back.setObjectName("pb_back")
        self.horizontalLayout.addWidget(self.pb_back)
        spacerItem1 = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.label_UnitName = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_UnitName.sizePolicy().hasHeightForWidth())
        self.label_UnitName.setSizePolicy(sizePolicy)
        self.label_UnitName.setMinimumSize(QtCore.QSize(334, 20))
        self.label_UnitName.setText("")
        self.label_UnitName.setObjectName("label_UnitName")
        self.horizontalLayout_3.addWidget(self.label_UnitName)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.label_EquipName = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_EquipName.sizePolicy().hasHeightForWidth())
        self.label_EquipName.setSizePolicy(sizePolicy)
        self.label_EquipName.setMinimumSize(QtCore.QSize(334, 20))
        self.label_EquipName.setText("")
        self.label_EquipName.setObjectName("label_EquipName")
        self.horizontalLayout_4.addWidget(self.label_EquipName)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_5.addWidget(self.label_3)
        self.label_StasticalMethod = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_StasticalMethod.sizePolicy().hasHeightForWidth())
        self.label_StasticalMethod.setSizePolicy(sizePolicy)
        self.label_StasticalMethod.setMinimumSize(QtCore.QSize(334, 20))
        self.label_StasticalMethod.setText("")
        self.label_StasticalMethod.setObjectName("label_StasticalMethod")
        self.horizontalLayout_5.addWidget(self.label_StasticalMethod)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        spacerItem2 = QtWidgets.QSpacerItem(200, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(100, -1, -1, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_6.addWidget(self.label_4)
        self.label_ExistNumber = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_ExistNumber.sizePolicy().hasHeightForWidth())
        self.label_ExistNumber.setSizePolicy(sizePolicy)
        self.label_ExistNumber.setMinimumSize(QtCore.QSize(200, 0))
        self.label_ExistNumber.setText("")
        self.label_ExistNumber.setObjectName("label_ExistNumber")
        self.horizontalLayout_6.addWidget(self.label_ExistNumber)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_7.addWidget(self.label_6)
        self.label_PowerNumber = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_PowerNumber.sizePolicy().hasHeightForWidth())
        self.label_PowerNumber.setSizePolicy(sizePolicy)
        self.label_PowerNumber.setMinimumSize(QtCore.QSize(200, 0))
        self.label_PowerNumber.setText("")
        self.label_PowerNumber.setObjectName("label_PowerNumber")
        self.horizontalLayout_7.addWidget(self.label_PowerNumber)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_8.addWidget(self.label_5)
        self.label_MeasureUnit = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_MeasureUnit.sizePolicy().hasHeightForWidth())
        self.label_MeasureUnit.setSizePolicy(sizePolicy)
        self.label_MeasureUnit.setMinimumSize(QtCore.QSize(200, 0))
        self.label_MeasureUnit.setText("")
        self.label_MeasureUnit.setObjectName("label_MeasureUnit")
        self.horizontalLayout_8.addWidget(self.label_MeasureUnit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        spacerItem3 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.frame)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.textBrowser.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">逐号信息录入</p></body></html>"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "批次号"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "数量"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "出厂年份"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "生产厂家"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "装备状态"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("Form", "是否到位"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("Form", "文件凭证"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("Form", "备注"))
        self.pb_Increase.setText(_translate("Form", "新增"))
        self.pb_Save.setText(_translate("Form", "保存"))
        self.pb_Export.setText(_translate("Form", "调出"))
        self.pb_BulkImport.setText(_translate("Form", "批量导入"))
        self.pb_DownloadMode.setText(_translate("Form", "下载模板"))
        self.pb_Delete.setText(_translate("Form", "删除"))
        self.pb_back.setText(_translate("Form", "返回"))
        self.label.setText(_translate("Form", "单位名称："))
        self.label_2.setText(_translate("Form", "装备名称："))
        self.label_3.setText(_translate("Form", "统计方式："))
        self.label_4.setText(_translate("Form", "现有数："))
        self.label_6.setText(_translate("Form", "实力数："))
        self.label_5.setText(_translate("Form", "计量单位："))
