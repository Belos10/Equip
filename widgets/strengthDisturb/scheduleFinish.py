# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scheduleFinish.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class widget_ScheduleFinish(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.w1_vbox = QtWidgets.QWidget(Form)
        self.w1_vbox.setObjectName("w1_vbox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.w1_vbox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pb_chooseFile = QtWidgets.QPushButton(self.w1_vbox)
        self.pb_chooseFile.setObjectName("pb_chooseFile")
        self.horizontalLayout.addWidget(self.pb_chooseFile)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.pb_openFile = QtWidgets.QPushButton(self.w1_vbox)
        self.pb_openFile.setObjectName("pb_openFile")
        self.horizontalLayout_2.addWidget(self.pb_openFile)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addWidget(self.w1_vbox)
        self.w2_hbox = QtWidgets.QWidget(Form)
        self.w2_hbox.setObjectName("w2_hbox")
        self.verticalLayout.addWidget(self.w2_hbox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pb_chooseFile.setText(_translate("Form", "选取文件"))
        self.pb_openFile.setText(_translate("Form", "查看文件"))
