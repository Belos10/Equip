# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'select_set.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Widget_Select_Set(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1454, 698)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.chooseWidget = QtWidgets.QWidget(Form)
        self.chooseWidget.setObjectName("chooseWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.chooseWidget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cb_setChoose = QtWidgets.QComboBox(self.chooseWidget)
        self.cb_setChoose.setMinimumSize(QtCore.QSize(150, 0))
        self.cb_setChoose.setObjectName("cb_setChoose")
        self.cb_setChoose.addItem("")
        self.cb_setChoose.addItem("")
        self.horizontalLayout.addWidget(self.cb_setChoose)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pb_add = QtWidgets.QPushButton(self.chooseWidget)
        self.pb_add.setObjectName("pb_add")
        self.horizontalLayout.addWidget(self.pb_add)
        self.pb_update = QtWidgets.QPushButton(self.chooseWidget)
        self.pb_update.setObjectName("pb_update")
        self.horizontalLayout.addWidget(self.pb_update)
        self.pb_del = QtWidgets.QPushButton(self.chooseWidget)
        self.pb_del.setObjectName("pb_del")
        self.horizontalLayout.addWidget(self.pb_del)
        self.pb_input = QtWidgets.QPushButton(self.chooseWidget)
        self.pb_input.setObjectName("pb_input")
        self.horizontalLayout.addWidget(self.pb_input)
        self.pb_output = QtWidgets.QPushButton(self.chooseWidget)
        self.pb_output.setObjectName("pb_output")
        self.horizontalLayout.addWidget(self.pb_output)
        self.gridLayout_3.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.chooseWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.wg_directory = QtWidgets.QWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wg_directory.sizePolicy().hasHeightForWidth())
        self.wg_directory.setSizePolicy(sizePolicy)
        self.wg_directory.setObjectName("wg_directory")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.wg_directory)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.le_first = QtWidgets.QLineEdit(self.wg_directory)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(70)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_first.sizePolicy().hasHeightForWidth())
        self.le_first.setSizePolicy(sizePolicy)
        self.le_first.setObjectName("le_first")
        self.horizontalLayout_7.addWidget(self.le_first)
        self.pb_firstSelect = QtWidgets.QPushButton(self.wg_directory)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_firstSelect.sizePolicy().hasHeightForWidth())
        self.pb_firstSelect.setSizePolicy(sizePolicy)
        self.pb_firstSelect.setObjectName("pb_firstSelect")
        self.horizontalLayout_7.addWidget(self.pb_firstSelect)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.tw_first = QtWidgets.QTreeWidget(self.wg_directory)
        self.tw_first.setObjectName("tw_first")
        self.tw_first.headerItem().setText(0, "1")
        self.verticalLayout_2.addWidget(self.tw_first)
        self.horizontalLayout_6.addLayout(self.verticalLayout_2)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.le_second = QtWidgets.QLineEdit(self.wg_directory)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(70)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_second.sizePolicy().hasHeightForWidth())
        self.le_second.setSizePolicy(sizePolicy)
        self.le_second.setObjectName("le_second")
        self.horizontalLayout_8.addWidget(self.le_second)
        self.pb_secondSelect = QtWidgets.QPushButton(self.wg_directory)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_secondSelect.sizePolicy().hasHeightForWidth())
        self.pb_secondSelect.setSizePolicy(sizePolicy)
        self.pb_secondSelect.setObjectName("pb_secondSelect")
        self.horizontalLayout_8.addWidget(self.pb_secondSelect)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        self.tw_second = QtWidgets.QTreeWidget(self.wg_directory)
        self.tw_second.setObjectName("tw_second")
        self.tw_second.headerItem().setText(0, "1")
        self.verticalLayout_4.addWidget(self.tw_second)
        self.horizontalLayout_6.addLayout(self.verticalLayout_4)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_2.addWidget(self.wg_directory)
        self.selectWidget = QtWidgets.QWidget(Form)
        self.selectWidget.setObjectName("selectWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.selectWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tb_result = QtWidgets.QTableWidget(self.selectWidget)
        self.tb_result.setObjectName("tb_result")
        self.tb_result.setColumnCount(0)
        self.tb_result.setRowCount(0)
        self.verticalLayout.addWidget(self.tb_result)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setContentsMargins(0, -1, 0, -1)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lb_unitUper = QtWidgets.QLabel(self.selectWidget)
        self.lb_unitUper.setMaximumSize(QtCore.QSize(90, 16777215))
        self.lb_unitUper.setObjectName("lb_unitUper")
        self.gridLayout_2.addWidget(self.lb_unitUper, 1, 0, 1, 1)
        self.lb_equipName = QtWidgets.QLabel(self.selectWidget)
        self.lb_equipName.setMaximumSize(QtCore.QSize(90, 16777215))
        self.lb_equipName.setObjectName("lb_equipName")
        self.gridLayout_2.addWidget(self.lb_equipName, 1, 2, 1, 1)
        self.lb_equipUper = QtWidgets.QLabel(self.selectWidget)
        self.lb_equipUper.setMaximumSize(QtCore.QSize(90, 16777215))
        self.lb_equipUper.setObjectName("lb_equipUper")
        self.gridLayout_2.addWidget(self.lb_equipUper, 1, 4, 1, 1)
        self.le_unitAlias = QtWidgets.QLineEdit(self.selectWidget)
        self.le_unitAlias.setMinimumSize(QtCore.QSize(100, 0))
        self.le_unitAlias.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.le_unitAlias.setObjectName("le_unitAlias")
        self.gridLayout_2.addWidget(self.le_unitAlias, 1, 3, 1, 1)
        self.lb_inputType = QtWidgets.QLabel(self.selectWidget)
        self.lb_inputType.setMaximumSize(QtCore.QSize(90, 16777215))
        self.lb_inputType.setObjectName("lb_inputType")
        self.gridLayout_2.addWidget(self.lb_inputType, 0, 6, 1, 1)
        self.le_equipUnit = QtWidgets.QLineEdit(self.selectWidget)
        self.le_equipUnit.setMinimumSize(QtCore.QSize(100, 0))
        self.le_equipUnit.setObjectName("le_equipUnit")
        self.gridLayout_2.addWidget(self.le_equipUnit, 1, 7, 1, 1)
        self.le_equipName = QtWidgets.QLineEdit(self.selectWidget)
        self.le_equipName.setMinimumSize(QtCore.QSize(100, 0))
        self.le_equipName.setObjectName("le_equipName")
        self.gridLayout_2.addWidget(self.le_equipName, 0, 7, 1, 1)
        self.le_unitName = QtWidgets.QLineEdit(self.selectWidget)
        self.le_unitName.setMinimumSize(QtCore.QSize(100, 0))
        self.le_unitName.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.le_unitName.setObjectName("le_unitName")
        self.gridLayout_2.addWidget(self.le_unitName, 0, 3, 1, 1)
        self.lb_equipType = QtWidgets.QLabel(self.selectWidget)
        self.lb_equipType.setMaximumSize(QtCore.QSize(90, 16777215))
        self.lb_equipType.setObjectName("lb_equipType")
        self.gridLayout_2.addWidget(self.lb_equipType, 1, 6, 1, 1)
        self.le_equipID = QtWidgets.QLineEdit(self.selectWidget)
        self.le_equipID.setMinimumSize(QtCore.QSize(100, 0))
        self.le_equipID.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.le_equipID.setObjectName("le_equipID")
        self.gridLayout_2.addWidget(self.le_equipID, 0, 5, 1, 1)
        self.le_unitID = QtWidgets.QLineEdit(self.selectWidget)
        self.le_unitID.setMinimumSize(QtCore.QSize(100, 0))
        self.le_unitID.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.le_unitID.setObjectName("le_unitID")
        self.gridLayout_2.addWidget(self.le_unitID, 0, 1, 1, 1)
        self.lb_equipID = QtWidgets.QLabel(self.selectWidget)
        self.lb_equipID.setMaximumSize(QtCore.QSize(90, 16777215))
        self.lb_equipID.setObjectName("lb_equipID")
        self.gridLayout_2.addWidget(self.lb_equipID, 0, 4, 1, 1)
        self.lb_unitName = QtWidgets.QLabel(self.selectWidget)
        self.lb_unitName.setMaximumSize(QtCore.QSize(90, 16777215))
        self.lb_unitName.setObjectName("lb_unitName")
        self.gridLayout_2.addWidget(self.lb_unitName, 0, 2, 1, 1)
        self.lb_unitID = QtWidgets.QLabel(self.selectWidget)
        self.lb_unitID.setMaximumSize(QtCore.QSize(90, 16777215))
        self.lb_unitID.setObjectName("lb_unitID")
        self.gridLayout_2.addWidget(self.lb_unitID, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.selectWidget)
        self.label.setMaximumSize(QtCore.QSize(90, 16777215))
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 8, 1, 1)
        self.cb_equipType = QtWidgets.QComboBox(self.selectWidget)
        self.cb_equipType.setMinimumSize(QtCore.QSize(100, 0))
        self.cb_equipType.setObjectName("cb_equipType")
        self.cb_equipType.addItem("")
        self.cb_equipType.addItem("")
        self.cb_equipType.addItem("")
        self.gridLayout_2.addWidget(self.cb_equipType, 0, 9, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.selectWidget)
        self.label_2.setMaximumSize(QtCore.QSize(90, 16777215))
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 8, 1, 1)
        self.cb_inputType = QtWidgets.QComboBox(self.selectWidget)
        self.cb_inputType.setMinimumSize(QtCore.QSize(100, 0))
        self.cb_inputType.setObjectName("cb_inputType")
        self.cb_inputType.addItem("")
        self.cb_inputType.addItem("")
        self.cb_inputType.addItem("")
        self.gridLayout_2.addWidget(self.cb_inputType, 1, 9, 1, 1)
        self.cb_equipUper = QtWidgets.QComboBox(self.selectWidget)
        self.cb_equipUper.setMinimumSize(QtCore.QSize(100, 0))
        self.cb_equipUper.setObjectName("cb_equipUper")
        self.gridLayout_2.addWidget(self.cb_equipUper, 1, 5, 1, 1)
        self.cb_unitUper = QtWidgets.QComboBox(self.selectWidget)
        self.cb_unitUper.setMinimumSize(QtCore.QSize(100, 0))
        self.cb_unitUper.setObjectName("cb_unitUper")
        self.gridLayout_2.addWidget(self.cb_unitUper, 1, 1, 1, 1)
        self.gridLayout_2.setColumnMinimumWidth(0, 1)
        self.gridLayout_2.setColumnMinimumWidth(1, 1)
        self.gridLayout_2.setColumnMinimumWidth(2, 1)
        self.gridLayout_2.setColumnMinimumWidth(3, 1)
        self.gridLayout_2.setColumnMinimumWidth(4, 1)
        self.gridLayout_2.setColumnMinimumWidth(5, 1)
        self.gridLayout_2.setColumnMinimumWidth(6, 1)
        self.gridLayout_2.setColumnMinimumWidth(7, 1)
        self.gridLayout_2.setColumnMinimumWidth(8, 1)
        self.gridLayout_2.setColumnMinimumWidth(9, 1)
        self.gridLayout_2.setColumnStretch(1, 1)
        self.gridLayout_2.setColumnStretch(3, 1)
        self.gridLayout_2.setColumnStretch(5, 1)
        self.gridLayout_2.setColumnStretch(7, 1)
        self.gridLayout_2.setColumnStretch(9, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.horizontalLayout_2.addWidget(self.selectWidget)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.cb_setChoose.setItemText(0, _translate("Form", "设置单位目录"))
        self.cb_setChoose.setItemText(1, _translate("Form", "设置装备目录"))
        self.pb_add.setText(_translate("Form", "增加"))
        self.pb_update.setText(_translate("Form", "修改"))
        self.pb_del.setText(_translate("Form", "删除"))
        self.pb_input.setText(_translate("Form", "导入"))
        self.pb_output.setText(_translate("Form", "导出"))
        self.pb_firstSelect.setText(_translate("Form", "查询"))
        self.pb_secondSelect.setText(_translate("Form", "查询"))
        self.lb_unitUper.setText(_translate("Form", "上级单位号："))
        self.lb_equipName.setText(_translate("Form", "单位别名："))
        self.lb_equipUper.setText(_translate("Form", "上级装备号："))
        self.lb_inputType.setText(_translate("Form", "装备名字："))
        self.lb_equipType.setText(_translate("Form", "装备单位："))
        self.lb_equipID.setText(_translate("Form", "装备号："))
        self.lb_unitName.setText(_translate("Form", "单位名字："))
        self.lb_unitID.setText(_translate("Form", "单位号："))
        self.label.setText(_translate("Form", "装备类型："))
        self.cb_equipType.setItemText(0, _translate("Form", "空"))
        self.cb_equipType.setItemText(1, _translate("Form", "通用装备"))
        self.cb_equipType.setItemText(2, _translate("Form", "专用装备"))
        self.label_2.setText(_translate("Form", "装备录入类型："))
        self.cb_inputType.setItemText(0, _translate("Form", "空"))
        self.cb_inputType.setItemText(1, _translate("Form", "逐号录入信息"))
        self.cb_inputType.setItemText(2, _translate("Form", "逐批录入信息"))
