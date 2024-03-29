# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'StrengthDisturb.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets,Qt

#new
class Position_Engineer_Widget(object):
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

        self.tb_installation = QtWidgets.QToolButton(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/pic/install.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_installation.setIcon(icon)
        self.tb_installation.setObjectName("tb_installation")
        self.tb_installation.setToolButtonStyle(Qt.Qt.ToolButtonTextUnderIcon)

        self.tb_equipmentStatistics = QtWidgets.QToolButton(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/pic/statistics.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_equipmentStatistics.setIcon(icon1)
        self.tb_equipmentStatistics.setObjectName("tb_equipmentStatistics")
        self.tb_equipmentStatistics.setToolButtonStyle(Qt.Qt.ToolButtonTextUnderIcon)


        # self.tb_directoryMaintenance = QtWidgets.QPushButton(MainWindow)
        # icon2 = QtGui.QIcon()
        # icon2.addPixmap(QtGui.QPixmap(":/pic/set.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        # self.tb_directoryMaintenance.setIcon(icon2)
        # self.tb_directoryMaintenance.setObjectName("tb_directoryMaintenance")
        # self.tb_directoryMaintenance.setToolButtonStyle(Qt.Qt.ToolButtonTextUnderIcon)
        self.toolBar.addWidget(self.tb_installation)
        self.toolBar.addWidget(self.tb_equipmentStatistics)
        # self.toolBar.addWidget(self.tb_directoryMaintenance)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.tb_installation.setText(_translate("MainWindow", "防护安装情况"))
        self.tb_equipmentStatistics.setText(_translate("MainWindow", "防护质量统计"))
        # self.tb_directoryMaintenance.setText(_translate("MainWindow", "阵地目录维护"))

import icons.resource_rc
