# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'factorySet.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Widget_Factory_Set(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1014, 611)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tw_result = QtWidgets.QTableWidget(self.groupBox)
        self.tw_result.setObjectName("tw_result")
        self.tw_result.setColumnCount(0)
        self.tw_result.setRowCount(0)
        self.horizontalLayout.addWidget(self.tw_result)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(Form)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.le_id = QtWidgets.QLineEdit(self.groupBox_2)
        self.le_id.setObjectName("le_id")
        self.horizontalLayout_2.addWidget(self.le_id)
        self.horizontalLayout_10.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.le_name = QtWidgets.QLineEdit(self.groupBox_2)
        self.le_name.setObjectName("le_name")
        self.horizontalLayout_3.addWidget(self.le_name)
        self.horizontalLayout_10.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.le_address = QtWidgets.QLineEdit(self.groupBox_2)
        self.le_address.setObjectName("le_address")
        self.horizontalLayout_4.addWidget(self.le_address)
        self.horizontalLayout_10.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_5.addWidget(self.label_4)
        self.le_connect = QtWidgets.QLineEdit(self.groupBox_2)
        self.le_connect.setObjectName("le_connect")
        self.horizontalLayout_5.addWidget(self.le_connect)
        self.horizontalLayout_10.addLayout(self.horizontalLayout_5)
        self.verticalLayout.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_6.addWidget(self.label_5)
        self.le_tel1 = QtWidgets.QLineEdit(self.groupBox_2)
        self.le_tel1.setObjectName("le_tel1")
        self.horizontalLayout_6.addWidget(self.le_tel1)
        self.horizontalLayout_11.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_7.addWidget(self.label_6)
        self.le_represent = QtWidgets.QLineEdit(self.groupBox_2)
        self.le_represent.setObjectName("le_represent")
        self.horizontalLayout_7.addWidget(self.le_represent)
        self.horizontalLayout_11.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_8.addWidget(self.label_7)
        self.le_tel2 = QtWidgets.QLineEdit(self.groupBox_2)
        self.le_tel2.setObjectName("le_tel2")
        self.horizontalLayout_8.addWidget(self.le_tel2)
        self.horizontalLayout_11.addLayout(self.horizontalLayout_8)
        self.verticalLayout.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem)
        self.pb_add = QtWidgets.QPushButton(self.groupBox_2)
        self.pb_add.setObjectName("pb_add")
        self.horizontalLayout_9.addWidget(self.pb_add)
        self.pb_update = QtWidgets.QPushButton(self.groupBox_2)
        self.pb_update.setObjectName("pb_update")
        self.horizontalLayout_9.addWidget(self.pb_update)
        self.pb_del = QtWidgets.QPushButton(self.groupBox_2)
        self.pb_del.setObjectName("pb_del")
        self.horizontalLayout_9.addWidget(self.pb_del)
        self.pb_input = QtWidgets.QPushButton(self.groupBox_2)
        self.pb_input.setObjectName("pb_input")
        self.horizontalLayout_9.addWidget(self.pb_input)
        self.pb_output = QtWidgets.QPushButton(self.groupBox_2)
        self.pb_output.setObjectName("pb_output")
        self.horizontalLayout_9.addWidget(self.pb_output)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "厂家目录"))
        self.groupBox_2.setTitle(_translate("Form", "设置"))
        self.label.setText(_translate("Form", "厂家编号："))
        self.label_2.setText(_translate("Form", "厂家名字："))
        self.label_3.setText(_translate("Form", "厂家地址："))
        self.label_4.setText(_translate("Form", "厂家联系人："))
        self.label_5.setText(_translate("Form", "厂家联系方式："))
        self.label_6.setText(_translate("Form", "军代表："))
        self.label_7.setText(_translate("Form", "军代表联系方式："))
        self.pb_add.setText(_translate("Form", "新增"))
        self.pb_update.setText(_translate("Form", "修改"))
        self.pb_del.setText(_translate("Form", "删除"))
        self.pb_input.setText(_translate("Form", "导入"))
        self.pb_output.setText(_translate("Form", "导出"))