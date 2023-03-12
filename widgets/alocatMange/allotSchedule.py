# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'allotSchedule.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

from widgets.ComboCheckBox import ComboCheckBox


class widget_AllotSchedule(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1747, 1157)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.groupBox = QtWidgets.QGroupBox(Form)
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
        self.horizontalLayout_8.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.wg_directory = QtWidgets.QWidget(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wg_directory.sizePolicy().hasHeightForWidth())
        self.wg_directory.setSizePolicy(sizePolicy)
        self.wg_directory.setMinimumSize(QtCore.QSize(0, 0))
        self.wg_directory.setMaximumSize(QtCore.QSize(16777215, 16777215))
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
        self.tw_first.setMinimumSize(QtCore.QSize(300, 800))
        self.tw_first.setMaximumSize(QtCore.QSize(16777215, 16777215))
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
        self.tw_second.setMinimumSize(QtCore.QSize(350, 800))
        self.tw_second.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.tw_second.setObjectName("tw_second")
        self.verticalLayout_3.addWidget(self.tw_second)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        self.gridLayout_2.addWidget(self.wg_directory, 0, 2, 1, 1)
        self.horizontalLayout_8.addWidget(self.groupBox_2)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label = QtWidgets.QLabel(Form)
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        self.label.setObjectName("label")
        self.horizontalLayout_5.addWidget(self.label)
        # self.cb_schedule1 = QtWidgets.QComboBox(Form)
        self.cb_schedule = ComboCheckBox(Form)
        self.cb_schedule.setMinimumSize(QtCore.QSize(200, 0))
        self.cb_schedule.setObjectName("cb_schedule")
        # self.cb_schedule.addItem("")

        self.horizontalLayout_5.addWidget(self.cb_schedule)
        self.pb_multiyearComparison = QtWidgets.QPushButton(Form)
        self.pb_multiyearComparison.setObjectName("pb_multiyearComparison")
        self.horizontalLayout_5.addWidget(self.pb_multiyearComparison)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.txt_disturbPlanYear = QtWidgets.QTextBrowser(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_disturbPlanYear.sizePolicy().hasHeightForWidth())
        self.txt_disturbPlanYear.setSizePolicy(sizePolicy)
        self.txt_disturbPlanYear.setMinimumSize(QtCore.QSize(0, 30))
        self.txt_disturbPlanYear.setMaximumSize(QtCore.QSize(16777215, 40))
        self.txt_disturbPlanYear.setObjectName("txt_disturbPlanYear")
        self.verticalLayout_4.addWidget(self.txt_disturbPlanYear)
        self.tb_proof = QtWidgets.QTextBrowser(Form)
        self.tb_proof.setMinimumSize(QtCore.QSize(0, 30))
        self.tb_proof.setMaximumSize(QtCore.QSize(16777215, 30))
        self.tb_proof.setObjectName("tb_proof")
        self.verticalLayout_4.addWidget(self.tb_proof)
        self.disturbResult = QtWidgets.QTableWidget(Form)
        self.disturbResult.setObjectName("disturbResult")
        self.disturbResult.setColumnCount(0)
        self.disturbResult.setRowCount(0)
        self.verticalLayout_4.addWidget(self.disturbResult)
        self.horizontalLayout_8.addLayout(self.verticalLayout_4)
        self.horizontalLayout_8.setStretch(0, 1)
        self.horizontalLayout_8.setStretch(1, 4)
        self.horizontalLayout_8.setStretch(2, 8)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "年份筛选"))
        self.groupBox_2.setTitle(_translate("Form", "目录查询"))
        self.pb_firstSelect.setText(_translate("Form", "查询"))
        self.pb_secondSelect.setText(_translate("Form", "查询"))
        self.label.setText(_translate("Form", "调拨进度筛选："))
        self.cb_schedule.setItemText(0, _translate("Form", "全部"))
        self.pb_multiyearComparison.setText(_translate("Form", "数据对比"))
        self.txt_disturbPlanYear.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
