# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'select_set.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Widget_Select_Set(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1105, 628)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.chooseWidget = QtWidgets.QWidget(Form)
        self.chooseWidget.setObjectName("chooseWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.chooseWidget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cb_setChoose = QtWidgets.QComboBox(self.chooseWidget)
        self.cb_setChoose.setMinimumSize(QtCore.QSize(150, 0))
        self.cb_setChoose.setObjectName("cb_setChoose")
        self.cb_setChoose.addItem("")
        self.cb_setChoose.addItem("")
        self.horizontalLayout.addWidget(self.cb_setChoose)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.chooseWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.selectWidget = QtWidgets.QWidget(Form)
        self.selectWidget.setObjectName("selectWidget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.selectWidget)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.sw_select_set = QtWidgets.QStackedWidget(self.selectWidget)
        self.sw_select_set.setObjectName("sw_select_set")
        self.verticalLayout_6.addWidget(self.sw_select_set)
        self.horizontalLayout_2.addWidget(self.selectWidget)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)

        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.cb_setChoose.setItemText(0, _translate("Form", "设置单位目录"))
        self.cb_setChoose.setItemText(1, _translate("Form", "设置装备目录"))
