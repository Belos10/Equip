# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'strengthDisturbSet.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets, Qt


class Widget_Strength_Disturb_Set(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(982, 659)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.sw_setManage = QtWidgets.QStackedWidget(self.centralwidget)
        self.sw_setManage.setObjectName("sw_setManage")
        self.gridLayout.addWidget(self.sw_setManage, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.tb_setProj = QtWidgets.QToolBar(MainWindow)
        self.tb_setProj.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.tb_setProj.setObjectName("tb_setProj")
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.tb_setProj)

        self.tb_selectSet = QtWidgets.QToolButton(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pic/selectSet.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_selectSet.setIcon(icon)
        self.tb_selectSet.setObjectName("tb_selectSet")
        self.tb_selectSet.setToolButtonStyle(Qt.Qt.ToolButtonTextUnderIcon)
        self.tb_setProj.addWidget(self.tb_selectSet)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tb_setProj.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.tb_selectSet.setText(_translate("MainWindow", "查询目录设置"))
import icons.resource_rc