# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'maintenMange.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Widget_Mainten_Manage(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1456, 1154)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.gridLayout_3 = QtWidgets.QGridLayout(Form)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setMinimumSize(QtCore.QSize(85, 0))
        self.groupBox.setMaximumSize(QtCore.QSize(85, 16777215))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.lw_year = QtWidgets.QListWidget(self.groupBox)
        self.lw_year.setObjectName("lw_year")
        self.gridLayout_4.addWidget(self.lw_year, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)
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
        self.tw_first.setMinimumSize(QtCore.QSize(300, 0))
        self.tw_first.setObjectName("tw_first")
        self.tw_first.headerItem().setText(0, "1")
        self.verticalLayout.addWidget(self.tw_first)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
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
        self.tw_second.setMinimumSize(QtCore.QSize(300, 0))
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
        self.gridLayout_2.setContentsMargins(5, 5, 5, 5)
        self.gridLayout_2.setSpacing(5)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(15)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.rb_equipShow = QtWidgets.QRadioButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rb_equipShow.sizePolicy().hasHeightForWidth())
        self.rb_equipShow.setSizePolicy(sizePolicy)
        self.rb_equipShow.setObjectName("rb_equipShow")
        self.horizontalLayout_5.addWidget(self.rb_equipShow)
        self.rb_unitShow = QtWidgets.QRadioButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rb_unitShow.sizePolicy().hasHeightForWidth())
        self.rb_unitShow.setSizePolicy(sizePolicy)
        self.rb_unitShow.setObjectName("rb_unitShow")
        self.horizontalLayout_5.addWidget(self.rb_unitShow)
        self.cb_showLast = QtWidgets.QCheckBox(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_showLast.sizePolicy().hasHeightForWidth())
        self.cb_showLast.setSizePolicy(sizePolicy)
        self.cb_showLast.setMinimumSize(QtCore.QSize(0, 40))
        self.cb_showLast.setObjectName("cb_showLast")
        self.horizontalLayout_5.addWidget(self.cb_showLast)
        spacerItem = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.pb_clearCheck = QtWidgets.QPushButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_clearCheck.sizePolicy().hasHeightForWidth())
        self.pb_clearCheck.setSizePolicy(sizePolicy)
        self.pb_clearCheck.setMinimumSize(QtCore.QSize(0, 30))
        self.pb_clearCheck.setMaximumSize(QtCore.QSize(200, 16777215))
        self.pb_clearCheck.setObjectName("pb_clearCheck")
        self.horizontalLayout_5.addWidget(self.pb_clearCheck)
        self.pb_clearAll = QtWidgets.QPushButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_clearAll.sizePolicy().hasHeightForWidth())
        self.pb_clearAll.setSizePolicy(sizePolicy)
        self.pb_clearAll.setMinimumSize(QtCore.QSize(0, 30))
        self.pb_clearAll.setMaximumSize(QtCore.QSize(200, 16777215))
        self.pb_clearAll.setObjectName("pb_clearAll")
        self.horizontalLayout_5.addWidget(self.pb_clearAll)
        self.gridLayout_2.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)
        self.tw_result = QtWidgets.QTableWidget(self.groupBox_3)
        self.tw_result.setObjectName("tw_result")
        self.tw_result.setColumnCount(0)
        self.tw_result.setRowCount(0)
        self.gridLayout_2.addWidget(self.tw_result, 1, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_3, 0, 2, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "年份筛选"))
        self.groupBox_2.setTitle(_translate("Form", "目录查询"))
        self.pb_firstSelect.setText(_translate("Form", "查询"))
        self.pb_secondSelect.setText(_translate("Form", "查询"))
        self.groupBox_3.setTitle(_translate("Form", "查询结果"))
        self.rb_equipShow.setText(_translate("Form", "按装备展开显示"))
        self.rb_unitShow.setText(_translate("Form", "按单位展开显示"))
        self.cb_showLast.setText(_translate("Form", "展开到末级"))
        self.pb_clearCheck.setText(_translate("Form", "清除选中装备"))
        self.pb_clearAll.setText(_translate("Form", "清除全部装备"))
