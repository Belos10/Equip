# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'alocatManageSet.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets, Qt


class Widget_Alocat_Manage_Set(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1056, 682)
        self.widget = QtWidgets.QWidget(MainWindow)
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.sw_setWidget = QtWidgets.QStackedWidget(self.widget)
        self.sw_setWidget.setObjectName("sw_setWidget")
        self.gridLayout.addWidget(self.sw_setWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.widget)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)

        self.tb_dictSet = QtWidgets.QToolButton(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/pict.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_dictSet.setIcon(icon1)
        self.tb_dictSet.setObjectName("tb_armyTransferYearSet")
        self.tb_dictSet.setToolButtonStyle(Qt.Qt.ToolButtonTextUnderIcon)
        self.toolBar.addWidget(self.tb_dictSet)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.tb_dictSet.setText(_translate("MainWindow", "目录设置"))