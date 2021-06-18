# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'orderManage.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets,Qt


class widget_orderManage(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.Order_stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.Order_stackedWidget.setObjectName("Order_stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.Order_stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.Order_stackedWidget.addWidget(self.page_2)
        self.gridLayout.addWidget(self.Order_stackedWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.tb_orderPlan = QtWidgets.QToolButton(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(""), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_orderPlan.setIcon(icon1)
        self.tb_orderPlan.setObjectName("tb_orderPlan")
        self.tb_orderPlan.setToolButtonStyle(Qt.Qt.ToolButtonTextUnderIcon)

        self.tb_adjustOrder = QtWidgets.QToolButton(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(""), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_adjustOrder.setIcon(icon2)
        self.tb_adjustOrder.setObjectName("tb_adjustOrder")
        self.tb_adjustOrder.setToolButtonStyle(Qt.Qt.ToolButtonTextUnderIcon)

        self.tb_orderAllotPlan = QtWidgets.QToolButton(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(""), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_orderAllotPlan.setIcon(icon3)
        self.tb_orderAllotPlan.setObjectName("tb_orderAllotPlan")
        self.tb_orderAllotPlan.setToolButtonStyle(Qt.Qt.ToolButtonTextUnderIcon)

        self.tb_orderSchedule = QtWidgets.QToolButton(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(""), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_orderSchedule.setIcon(icon4)
        self.tb_orderSchedule.setObjectName("tb_orderSchedule")
        self.tb_orderSchedule.setToolButtonStyle(Qt.Qt.ToolButtonTextUnderIcon)

        self.tb_retirePlan = QtWidgets.QToolButton(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(""), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tb_retirePlan.setIcon(icon5)
        self.tb_retirePlan.setObjectName("tb_retirePlan")
        self.tb_retirePlan.setToolButtonStyle(Qt.Qt.ToolButtonTextUnderIcon)


        self.toolBar.addWidget(self.tb_orderPlan)
        self.toolBar.addWidget(self.tb_adjustOrder)
        self.toolBar.addWidget(self.tb_orderAllotPlan)
        self.toolBar.addWidget(self.tb_orderSchedule)
        self.toolBar.addWidget(self.tb_retirePlan)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.tb_orderPlan.setText("")
        self.tb_adjustOrder.setText("计划调整")
        self.tb_orderAllotPlan.setText("分配计划")
        self.tb_orderSchedule.setText("分配进度")
        self.tb_retirePlan.setText("退役计划")
