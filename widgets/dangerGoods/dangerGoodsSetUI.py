# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dangerGoodsSetUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class DangerGoodsSetUI(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1186, 824)
        self.gridLayout_5 = QtWidgets.QGridLayout(Form)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setSpacing(0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.chooseWidget = QtWidgets.QWidget(Form)
        self.chooseWidget.setObjectName("chooseWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.chooseWidget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout.addLayout(self.horizontalLayout_3)
        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.chooseWidget, 0, 0, 1, 1)
        self.selectWidget = QtWidgets.QWidget(Form)
        self.selectWidget.setObjectName("selectWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.selectWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.wg_directory = QtWidgets.QWidget(self.selectWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wg_directory.sizePolicy().hasHeightForWidth())
        self.wg_directory.setSizePolicy(sizePolicy)
        self.wg_directory.setObjectName("wg_directory")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.wg_directory)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.le_first = QtWidgets.QLineEdit(self.wg_directory)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(70)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_first.sizePolicy().hasHeightForWidth())
        self.le_first.setSizePolicy(sizePolicy)
        self.le_first.setObjectName("le_first")
        self.horizontalLayout_7.addWidget(self.le_first)
        self.pb_firstSelect = QtWidgets.QPushButton(self.wg_directory)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_firstSelect.sizePolicy().hasHeightForWidth())
        self.pb_firstSelect.setSizePolicy(sizePolicy)
        self.pb_firstSelect.setObjectName("pb_firstSelect")
        self.horizontalLayout_7.addWidget(self.pb_firstSelect)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.tw_first = QtWidgets.QTreeWidget(self.wg_directory)
        self.tw_first.setObjectName("tw_first")
        self.tw_first.headerItem().setText(0, "1")
        self.verticalLayout_2.addWidget(self.tw_first)
        self.horizontalLayout_6.addLayout(self.verticalLayout_2)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.pb_secondSelect = QtWidgets.QPushButton(self.wg_directory)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_secondSelect.sizePolicy().hasHeightForWidth())
        self.pb_secondSelect.setSizePolicy(sizePolicy)
        self.pb_secondSelect.setObjectName("pb_secondSelect")
        self.horizontalLayout_8.addWidget(self.pb_secondSelect)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_6.addLayout(self.verticalLayout_4)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_9.addWidget(self.wg_directory)
        self.tb_result = QtWidgets.QTableWidget(self.selectWidget)
        self.tb_result.setObjectName("tb_result")
        self.tb_result.setColumnCount(0)
        self.tb_result.setRowCount(0)
        self.horizontalLayout_9.addWidget(self.tb_result)
        self.gridLayout.addLayout(self.horizontalLayout_9, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.selectWidget, 1, 0, 1, 1)
        self.inputWidget = QtWidgets.QWidget(Form)
        self.inputWidget.setObjectName("inputWidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.inputWidget)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setContentsMargins(0, -1, 0, -1)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.pb_del = QtWidgets.QPushButton(self.inputWidget)
        self.pb_del.setMaximumSize(QtCore.QSize(150, 25))
        self.pb_del.setObjectName("pb_del")
        self.horizontalLayout_4.addWidget(self.pb_del)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.pb_add = QtWidgets.QPushButton(self.inputWidget)
        self.pb_add.setMaximumSize(QtCore.QSize(150, 25))
        self.pb_add.setObjectName("pb_add")
        self.horizontalLayout_4.addWidget(self.pb_add)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.pb_update = QtWidgets.QPushButton(self.inputWidget)
        self.pb_update.setMaximumSize(QtCore.QSize(150, 25))
        self.pb_update.setObjectName("pb_update")
        self.horizontalLayout_4.addWidget(self.pb_update)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 0, 5, 1, 1)
        self.lb_unitName = QtWidgets.QLabel(self.inputWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_unitName.sizePolicy().hasHeightForWidth())
        self.lb_unitName.setSizePolicy(sizePolicy)
        self.lb_unitName.setObjectName("lb_unitName")
        self.gridLayout_2.addWidget(self.lb_unitName, 0, 2, 1, 1)
        self.lb_unitUper = QtWidgets.QLabel(self.inputWidget)
        self.lb_unitUper.setObjectName("lb_unitUper")
        self.gridLayout_2.addWidget(self.lb_unitUper, 1, 0, 1, 1)
        self.le_unitUper = QtWidgets.QLineEdit(self.inputWidget)
        self.le_unitUper.setMaximumSize(QtCore.QSize(150, 16777215))
        self.le_unitUper.setObjectName("le_unitUper")
        self.gridLayout_2.addWidget(self.le_unitUper, 1, 1, 1, 1)
        self.le_unitID = QtWidgets.QLineEdit(self.inputWidget)
        self.le_unitID.setMaximumSize(QtCore.QSize(150, 16777215))
        self.le_unitID.setObjectName("le_unitID")
        self.gridLayout_2.addWidget(self.le_unitID, 0, 1, 1, 1)
        self.lb_unitID = QtWidgets.QLabel(self.inputWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_unitID.sizePolicy().hasHeightForWidth())
        self.lb_unitID.setSizePolicy(sizePolicy)
        self.lb_unitID.setObjectName("lb_unitID")
        self.gridLayout_2.addWidget(self.lb_unitID, 0, 0, 1, 1)
        self.le_unitName = QtWidgets.QLineEdit(self.inputWidget)
        self.le_unitName.setMinimumSize(QtCore.QSize(150, 0))
        self.le_unitName.setMaximumSize(QtCore.QSize(150, 16777215))
        self.le_unitName.setObjectName("le_unitName")
        self.gridLayout_2.addWidget(self.le_unitName, 0, 3, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 5, 2, 1)
        self.gridLayout_4.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.inputWidget, 2, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "阵地工程"))
        self.pb_firstSelect.setText(_translate("Form", "查询"))
        self.pb_secondSelect.setText(_translate("Form", "查询"))
        self.pb_del.setText(_translate("Form", "删除"))
        self.pb_add.setText(_translate("Form", "增加"))
        self.pb_update.setText(_translate("Form", "修改"))
        self.lb_unitName.setText(_translate("Form", "单位名字："))
        self.lb_unitUper.setText(_translate("Form", "上级单位号："))
        self.lb_unitID.setText(_translate("Form", "单位号："))
