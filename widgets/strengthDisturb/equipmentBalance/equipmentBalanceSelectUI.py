# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'equipmentBalanceSelectUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class EquipmentBalanceSelectUI(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1545, 1011)
        self.gridLayout_3 = QtWidgets.QGridLayout(Form)
        self.gridLayout_3.setContentsMargins(-1, 0, -1, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.gridLayout_3.addWidget(self.label_4, 1, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.le_first = QtWidgets.QLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(70)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_first.sizePolicy().hasHeightForWidth())
        self.le_first.setSizePolicy(sizePolicy)
        self.le_first.setObjectName("le_first")
        self.horizontalLayout_2.addWidget(self.le_first)
        self.pb_firstSelect = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_firstSelect.sizePolicy().hasHeightForWidth())
        self.pb_firstSelect.setSizePolicy(sizePolicy)
        self.pb_firstSelect.setMaximumSize(QtCore.QSize(50, 50))
        self.pb_firstSelect.setObjectName("pb_firstSelect")
        self.horizontalLayout_2.addWidget(self.pb_firstSelect)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tw_first = QtWidgets.QTreeWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tw_first.sizePolicy().hasHeightForWidth())
        self.tw_first.setSizePolicy(sizePolicy)
        self.tw_first.setMaximumSize(QtCore.QSize(256, 16777215))
        self.tw_first.setObjectName("tw_first")
        item_0 = QtWidgets.QTreeWidgetItem(self.tw_first)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        self.verticalLayout.addWidget(self.tw_first)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.le_second = QtWidgets.QLineEdit(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(70)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_second.sizePolicy().hasHeightForWidth())
        self.le_second.setSizePolicy(sizePolicy)
        self.le_second.setObjectName("le_second")
        self.horizontalLayout_4.addWidget(self.le_second)
        self.pb_secondSelect = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_secondSelect.sizePolicy().hasHeightForWidth())
        self.pb_secondSelect.setSizePolicy(sizePolicy)
        self.pb_secondSelect.setMaximumSize(QtCore.QSize(50, 50))
        self.pb_secondSelect.setObjectName("pb_secondSelect")
        self.horizontalLayout_4.addWidget(self.pb_secondSelect)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.tw_second = QtWidgets.QTreeWidget(Form)
        self.tw_second.setMaximumSize(QtCore.QSize(256, 16777215))
        self.tw_second.setObjectName("tw_second")
        item_0 = QtWidgets.QTreeWidgetItem(self.tw_second)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_2 = QtWidgets.QTreeWidgetItem(item_1)
        self.verticalLayout_3.addWidget(self.tw_second)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tb_result = QtWidgets.QTableWidget(Form)
        self.tb_result.setObjectName("tb_result")
        self.tb_result.setColumnCount(0)
        self.tb_result.setRowCount(0)
        self.verticalLayout_2.addWidget(self.tb_result)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pb_output = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_output.sizePolicy().hasHeightForWidth())
        self.pb_output.setSizePolicy(sizePolicy)
        self.pb_output.setObjectName("pb_output")
        self.gridLayout_2.addWidget(self.pb_output, 1, 0, 1, 1)
        self.pb_sava = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_sava.sizePolicy().hasHeightForWidth())
        self.pb_sava.setSizePolicy(sizePolicy)
        self.pb_sava.setObjectName("pb_sava")
        self.gridLayout_2.addWidget(self.pb_sava, 1, 1, 1, 1)
        self.pb_return = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_return.sizePolicy().hasHeightForWidth())
        self.pb_return.setSizePolicy(sizePolicy)
        self.pb_return.setObjectName("pb_return")
        self.gridLayout_2.addWidget(self.pb_return, 1, 2, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.horizontalLayout_5.addLayout(self.verticalLayout_2)
        self.gridLayout_3.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pb_firstSelect.setText(_translate("Form", "查询"))
        __sortingEnabled = self.tw_first.isSortingEnabled()
        self.tw_first.setSortingEnabled(False)
        self.tw_first.topLevelItem(0).setText(0, _translate("Form", "火箭军"))
        self.tw_first.topLevelItem(0).child(0).setText(0, _translate("Form", "火箭军基地"))
        self.tw_first.topLevelItem(0).child(0).child(0).setText(0, _translate("Form", "New Subitem"))
        self.tw_first.topLevelItem(0).child(0).child(1).setText(0, _translate("Form", "New Subitem"))
        self.tw_first.topLevelItem(0).child(1).setText(0, _translate("Form", "火箭军院校"))
        self.tw_first.topLevelItem(0).child(1).child(0).setText(0, _translate("Form", "New Subitem"))
        self.tw_first.topLevelItem(0).child(2).setText(0, _translate("Form", "火箭军直属部队"))
        self.tw_first.topLevelItem(0).child(2).child(0).setText(0, _translate("Form", "New Subitem"))
        self.tw_first.topLevelItem(0).child(3).setText(0, _translate("Form", "火箭军机关"))
        self.tw_first.topLevelItem(0).child(3).child(0).setText(0, _translate("Form", "New Subitem"))
        self.tw_first.topLevelItem(0).child(4).setText(0, _translate("Form", "火箭军研究院、所"))
        self.tw_first.topLevelItem(0).child(4).child(0).setText(0, _translate("Form", "New Subitem"))
        self.tw_first.topLevelItem(0).child(5).setText(0, _translate("Form", "库存"))
        self.tw_first.setSortingEnabled(__sortingEnabled)
        self.pb_secondSelect.setText(_translate("Form", "查询"))
        __sortingEnabled = self.tw_second.isSortingEnabled()
        self.tw_second.setSortingEnabled(False)
        self.tw_second.topLevelItem(0).setText(0, _translate("Form", "装备"))
        self.tw_second.topLevelItem(0).child(0).setText(0, _translate("Form", "防化车辆"))
        self.tw_second.topLevelItem(0).child(0).child(0).setText(0, _translate("Form", "防化团指挥车"))
        self.tw_second.setSortingEnabled(__sortingEnabled)
        self.pb_output.setText(_translate("Form", "导出"))
        self.pb_sava.setText(_translate("Form", "保存"))
        self.pb_return.setText(_translate("Form", "返回"))
