# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'attachmentDialogUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon


class AttachmentDialogUI(object):
    def setupUi(self, dl_attachment):
        dl_attachment.setObjectName("dl_attachment")
        dl_attachment.resize(997, 684)
        dl_attachment.setMinimumSize(QtCore.QSize(1200, 800))
        self.verticalLayout = QtWidgets.QVBoxLayout(dl_attachment)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tw_result = QtWidgets.QTableWidget(dl_attachment)
        self.tw_result.setMinimumSize(QtCore.QSize(800, 600))
        self.tw_result.setObjectName("tw_result")
        self.tw_result.setColumnCount(0)
        self.tw_result.setRowCount(0)
        self.verticalLayout.addWidget(self.tw_result)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pb_add = QtWidgets.QPushButton(dl_attachment)
        self.pb_add.setObjectName("pb_add")
        self.horizontalLayout.addWidget(self.pb_add)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pb_delete = QtWidgets.QPushButton(dl_attachment)
        self.pb_delete.setObjectName("pb_delete")
        self.horizontalLayout.addWidget(self.pb_delete)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(dl_attachment)
        QtCore.QMetaObject.connectSlotsByName(dl_attachment)

    def retranslateUi(self, dl_attachment):
        _translate = QtCore.QCoreApplication.translate
        dl_attachment.setWindowTitle(_translate("dl_attachment", "附件信息"))
        self.pb_add.setText(_translate("dl_attachment", "新增"))
        self.pb_delete.setText(_translate("dl_attachment", "删除"))
