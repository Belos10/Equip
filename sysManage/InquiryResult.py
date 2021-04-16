from PyQt5.QtWidgets import QMainWindow
from widgets.manage_widget import Widget_Manage_Widgets
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidgetItem, QAbstractItemView
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
from widgets.inquiry_result import Widget_Inquiry_Result
from database.ConnectAndSql import Clicked, delete_Inquiry_Clicked

'''
    类功能：
        管理实力分布下实力查询结果界面，包含查询结果相关逻辑代码
'''


class Inquiry_Result(QWidget, Widget_Inquiry_Result):
    def __init__(self, parent=None):
        super(Inquiry_Result, self).__init__(parent)
        self.setupUi(self)
        self.currentInquiryResult = {}
        self.tw_inquiryResult.setEditTriggers(QAbstractItemView.CurrentChanged)
        self.pb_insert.setText("信息展示及修改")
        self.pb_insert.clicked.connect(self.slotStateChange)

    def slotStateChange(self):
        if self.tw_inquiryResult.editTriggers() == QAbstractItemView.CurrentChanged:
            self.tw_inquiryResult.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.pb_insert.setText("信息录入")
        else:
            self.tw_inquiryResult.setEditTriggers(QAbstractItemView.CurrentChanged)
            self.pb_insert.setText("信息展示及修改")

    def findEquipId(self, EquipID, EquipIDList):
        sql = "select Equip_ID from equip where Equip_Uper = '" + EquipID + "'"
        FindEquipID = Clicked(sql)
        EquipIDList.append(EquipID)
        for id in FindEquipID:
            sql = "select Equip_ID from equip where Equip_Uper = '" + id[0] + "'"
            # print(sql)
            haveChild = Clicked(sql)
            for child in haveChild:
                self.findEquipId(child[0], EquipIDList)
            EquipIDList.append(id[0])

    '''
        QTableWidget显示查询结果
    '''

    def InquiryResult(self, UnitID, EquipID, isRoot):
        self.tw_inquiryResult.clear()
        EquipIDList = []
        # EquipIDList.append(EquipID)
        sql = "select Dept_Name from dept where Dept_ID = '" + UnitID + "'"
        # print(sql)
        UnitName = Clicked(sql)
        inquiry_result = []
        result_num = 0
        if isRoot:
            self.findEquipId(EquipID, EquipIDList)
        else:
            EquipIDList.append(EquipID)

        for id in EquipIDList:
            sql = "select * from equipandunit where Equip_ID = '" + id + "' and Unit_ID = '" + UnitID + "'"
            result = Clicked(sql)
            for row in result:
                inquiry_result.append(row)
            result_num += len(result)

        self.tw_inquiryResult.setRowCount(result_num)
        self.tw_inquiryResult.setColumnCount(13)
        headerlist = ['单位名称', '装备名称', '实力数', '编制数', '现有数', '偏差', '准备退役数', '未到位数', '提前退役', '待核查无实物', '待核查无实力', '单独建账',
                      '正常到位']
        self.tw_inquiryResult.setHorizontalHeaderLabels(headerlist)
        for i, data in enumerate(inquiry_result):
            item = QTableWidgetItem(data[3])
            self.tw_inquiryResult.setItem(i, 0, item)
            item = QTableWidgetItem(data[2])
            self.tw_inquiryResult.setItem(i, 1, item)
            item = QTableWidgetItem(data[4])
            self.tw_inquiryResult.setItem(i, 2, item)
            item = QTableWidgetItem(data[5])
            self.tw_inquiryResult.setItem(i, 3, item)
            item = QTableWidgetItem(data[6])
            self.tw_inquiryResult.setItem(i, 4, item)
            item = QTableWidgetItem(data[7])
            self.tw_inquiryResult.setItem(i, 5, item)
            item = QTableWidgetItem(data[8])
            self.tw_inquiryResult.setItem(i, 6, item)
            item = QTableWidgetItem(data[9])
            self.tw_inquiryResult.setItem(i, 7, item)
            item = QTableWidgetItem(data[10])
            self.tw_inquiryResult.setItem(i, 8, item)
            item = QTableWidgetItem(data[11])
            self.tw_inquiryResult.setItem(i, 9, item)
            item = QTableWidgetItem(data[12])
            self.tw_inquiryResult.setItem(i, 10, item)
            item = QTableWidgetItem(data[13])
            self.tw_inquiryResult.setItem(i, 11, item)
            item = QTableWidgetItem(data[14])
            self.tw_inquiryResult.setItem(i, 12, item)

            self.currentInquiryResult[i] = data
            # print(self.currentInquryResult)

    # 删除选中装备
    def deleteInquiryResult(self):
        item = self.tw_inquiryResult.selectedItems()
        if len(item) == 0:
            return
        i = self.tw_inquiryResult.currentRow()
        UnitID = self.currentInquiryResult[i][1]
        EquipID = self.currentInquiryResult[i][0]
        delete_Inquiry_Clicked(UnitID, EquipID)
        self.InquiryResult(UnitID, EquipID, 1)

    # 删除所有装备
    def deleteAllInquiryResult(self):
        for i in range(0, self.tw_inquiryResult.rowCount()):
            UnitID = self.currentInquiryResult[i][1]
            EquipID = self.currentInquiryResult[i][0]
            delete_Inquiry_Clicked(UnitID, EquipID)
        self.InquiryResult(UnitID, EquipID, 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Inquiry_Result()
    widget.show()
    sys.exit(app.exec_())
