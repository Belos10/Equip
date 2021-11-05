# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'inquiry_result.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Widget_Inquiry_Result(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1146, 829)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setObjectName("widget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.rb_equipShow = QtWidgets.QRadioButton(self.widget)
        self.rb_equipShow.setObjectName("rb_equipShow")
        self.horizontalLayout_3.addWidget(self.rb_equipShow)
        self.rb_unitShow = QtWidgets.QRadioButton(self.widget)
        self.rb_unitShow.setObjectName("rb_unitShow")
        self.horizontalLayout_3.addWidget(self.rb_unitShow)
        self.cb_showLast = QtWidgets.QCheckBox(self.widget)
        self.cb_showLast.setObjectName("cb_showLast")
        self.horizontalLayout_3.addWidget(self.cb_showLast)
        self.cb_showDistence = QtWidgets.QCheckBox(self.widget)
        self.cb_showDistence.setObjectName("cb_showDistence")
        self.horizontalLayout_3.addWidget(self.cb_showDistence)
        self.cb_showValue0 = QtWidgets.QCheckBox(self.widget)
        self.cb_showValue0.setObjectName("cb_showValue0")
        self.horizontalLayout_3.addWidget(self.cb_showValue0)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.pushButton)
        spacerItem = QtWidgets.QSpacerItem(12, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lb_factoryYear = QtWidgets.QLabel(self.widget)
        self.lb_factoryYear.setObjectName("lb_factoryYear")
        self.horizontalLayout_2.addWidget(self.lb_factoryYear)
        self.pb_factoryYear = QtWidgets.QPushButton(self.widget)
        self.pb_factoryYear.setObjectName("pb_factoryYear")
        self.horizontalLayout_2.addWidget(self.pb_factoryYear)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.pb_clearCheck = QtWidgets.QPushButton(self.widget)
        self.pb_clearCheck.setObjectName("pb_clearCheck")
        self.horizontalLayout_3.addWidget(self.pb_clearCheck)
        self.pb_clearAll = QtWidgets.QPushButton(self.widget)
        self.pb_clearAll.setObjectName("pb_clearAll")
        self.horizontalLayout_3.addWidget(self.pb_clearAll)
        self.pb_updateStrength = QtWidgets.QPushButton(self.widget)
        self.pb_updateStrength.setObjectName("pb_updateStrength")
        self.horizontalLayout_3.addWidget(self.pb_updateStrength)
        self.verticalLayout.addWidget(self.widget)
        self.tw_inquiryResult = QtWidgets.QTableWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tw_inquiryResult.sizePolicy().hasHeightForWidth())
        self.tw_inquiryResult.setSizePolicy(sizePolicy)
        self.tw_inquiryResult.setObjectName("tw_inquiryResult")
        self.tw_inquiryResult.setColumnCount(0)
        self.tw_inquiryResult.setRowCount(0)
        self.verticalLayout.addWidget(self.tw_inquiryResult)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pb_input = QtWidgets.QPushButton(Form)
        self.pb_input.setObjectName("pb_input")
        self.horizontalLayout.addWidget(self.pb_input)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.pb_output = QtWidgets.QPushButton(Form)
        self.pb_output.setObjectName("pb_output")
        self.horizontalLayout.addWidget(self.pb_output)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.pb_outputToExcel = QtWidgets.QPushButton(Form)
        self.pb_outputToExcel.setObjectName("pb_outputToExcel")
        self.horizontalLayout.addWidget(self.pb_outputToExcel)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.rb_equipShow.setText(_translate("Form", "按装备展开显示"))
        self.rb_unitShow.setText(_translate("Form", "按单位展开显示"))
        self.cb_showLast.setText(_translate("Form", "展开到末级"))
        self.cb_showDistence.setText(_translate("Form", "只列存在偏差"))
        self.cb_showValue0.setText(_translate("Form", "不显示0值"))
        self.pushButton.setText(_translate("Form", "表头筛选"))
        self.lb_factoryYear.setText(_translate("Form", "当前显示的出厂年份：全部"))
        self.pb_factoryYear.setText(_translate("Form", "选择显示出厂年份"))
        self.pb_clearCheck.setText(_translate("Form", "清除选中装备"))
        self.pb_clearAll.setText(_translate("Form", "清除全部装备"))
        self.pb_updateStrength.setText(_translate("Form", "编辑实力数"))
        self.pb_input.setText(_translate("Form", "导入数据包"))
        self.pb_output.setText(_translate("Form", "导出数据包"))
        self.pb_outputToExcel.setText(_translate("Form", "导出至Excel"))
