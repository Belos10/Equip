# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'inquiry_result.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Widget_Inquiry_Result(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(850, 777)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.rb_equipShow = QtWidgets.QRadioButton(self.widget)
        self.rb_equipShow.setObjectName("rb_equipShow")
        self.horizontalLayout_2.addWidget(self.rb_equipShow)
        self.rb_unitShow = QtWidgets.QRadioButton(self.widget)
        self.rb_unitShow.setObjectName("rb_unitShow")
        self.horizontalLayout_2.addWidget(self.rb_unitShow)
        self.cb_showLast = QtWidgets.QCheckBox(self.widget)
        self.cb_showLast.setObjectName("cb_showLast")
        self.horizontalLayout_2.addWidget(self.cb_showLast)
        self.cb_showDistence = QtWidgets.QCheckBox(self.widget)
        self.cb_showDistence.setObjectName("cb_showDistence")
        self.horizontalLayout_2.addWidget(self.cb_showDistence)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pb_insert = QtWidgets.QPushButton(self.widget)
        self.pb_insert.setObjectName("pb_insert")
        self.horizontalLayout_2.addWidget(self.pb_insert)
        self.pb_clearCheck = QtWidgets.QPushButton(self.widget)
        self.pb_clearCheck.setObjectName("pb_clearCheck")
        self.horizontalLayout_2.addWidget(self.pb_clearCheck)
        self.pb_clearAll = QtWidgets.QPushButton(self.widget)
        self.pb_clearAll.setObjectName("pb_clearAll")
        self.horizontalLayout_2.addWidget(self.pb_clearAll)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.tw_inquiryResult = QtWidgets.QTableWidget(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tw_inquiryResult.sizePolicy().hasHeightForWidth())
        self.tw_inquiryResult.setSizePolicy(sizePolicy)
        self.tw_inquiryResult.setObjectName("tw_inquiryResult")
        self.tw_inquiryResult.setColumnCount(0)
        self.tw_inquiryResult.setRowCount(0)
        self.verticalLayout_2.addWidget(self.tw_inquiryResult)
        self.verticalLayout.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.rb_equipShow.setText(_translate("Form", "按装备展开显示"))
        self.rb_unitShow.setText(_translate("Form", "按单位展开显示"))
        self.cb_showLast.setText(_translate("Form", "展开到末级"))
        self.cb_showDistence.setText(_translate("Form", "只列存在偏差"))
        self.pb_insert.setText(_translate("Form", "信息录入"))
        self.pb_clearCheck.setText(_translate("Form", "清除选中装备"))
        self.pb_clearAll.setText(_translate("Form", "清除全部装备"))
