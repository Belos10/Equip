# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'showRocketTransfer.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class widget_showRocket(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(521, 473)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tw_ditalModel = QtWidgets.QTableWidget(Dialog)
        self.tw_ditalModel.setObjectName("tw_ditalModel")
        self.tw_ditalModel.setColumnCount(0)
        self.tw_ditalModel.setRowCount(0)
        self.verticalLayout.addWidget(self.tw_ditalModel)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
