# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'StrengthDisturb.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets,Qt

#new
from PyQt5.QtCore import QSize


class Strength_Disturb_Widget(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 700)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.gridLayout.addWidget(self.stackedWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.toolBar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.tb_strengthSelect = QtWidgets.QToolButton(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pic/select.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_strengthSelect.setIcon(icon)
        self.tb_strengthSelect.setIconSize(QSize(10,10))
        self.tb_strengthSelect.setObjectName("tb_strengthSelect")
        self.tb_strengthSelect.setToolButtonStyle(Qt.Qt.ToolButtonTextUnderIcon)

        self.tb_maintenMange = QtWidgets.QToolButton(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/pic/wave.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_maintenMange.setIcon(icon1)
        self.tb_maintenMange.setIconSize(QSize(10, 10))
        self.tb_maintenMange.setObjectName("tb_maintenMange")
        self.tb_maintenMange.setToolButtonStyle(Qt.Qt.ToolButtonTextUnderIcon)

        self.tb_equipBalance = QtWidgets.QToolButton(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/pic/equip.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_equipBalance.setIcon(icon2)
        self.tb_equipBalance.setObjectName("tb_equipBalance")
        self.tb_equipBalance.setToolButtonStyle(Qt.Qt.ToolButtonTextUnderIcon)

        self.tb_applyRetire = QtWidgets.QToolButton(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/pic/retire.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_applyRetire.setIcon(icon3)
        self.tb_applyRetire.setObjectName("tb_applyRetire")
        self.tb_applyRetire.setToolButtonStyle(Qt.Qt.ToolButtonTextUnderIcon)

        self.tb_strengthDisturbSet = QtWidgets.QToolButton(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/pic/set.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_strengthDisturbSet.setIcon(icon4)
        self.tb_strengthDisturbSet.setObjectName("tb_strengthDisturbSet")
        self.tb_strengthDisturbSet.setToolButtonStyle(Qt.Qt.ToolButtonTextUnderIcon)

        self.toolBar.addWidget(self.tb_strengthSelect)
        self.toolBar.addWidget(self.tb_maintenMange)
        self.toolBar.addWidget(self.tb_equipBalance)
        self.toolBar.addWidget(self.tb_applyRetire)
        self.toolBar.addWidget(self.tb_strengthDisturbSet)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.tb_strengthSelect.setText(_translate("MainWindow", "实力查询"))
        self.tb_maintenMange.setText(_translate("MainWindow", "编制数维护"))
        self.tb_equipBalance.setText(_translate("MainWindow", "装备平衡表"))
        self.tb_applyRetire.setText(_translate("MainWindow", "申请退役"))
        self.tb_strengthDisturbSet.setText(_translate("MainWindow", "目录设置"))
import icons.resource_rc
