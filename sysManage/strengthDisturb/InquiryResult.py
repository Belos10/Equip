import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, QAbstractItemView
from widgets.strengthDisturb.inquiry_result import Widget_Inquiry_Result
from database.ConnectAndSql import Clicked, delete_Inquiry_Clicked

'''
    类功能：
        管理实力分布下实力查询结果界面，包含查询结果相关逻辑代码
'''


class Inquiry_Result(QWidget, Widget_Inquiry_Result):
    def __init__(self, parent=None):
        super(Inquiry_Result, self).__init__(parent)
        self.setupUi(self)

        #存储当前查询结果，结构为：{'行号':该行数据'}
        self.currentInquiryResult = {}

        #tableWidget可编辑
        self.tw_inquiryResult.setEditTriggers(QAbstractItemView.CurrentChanged)

        self.pb_insert.setText("信息展示及修改")
        self.result = []

        #信号和槽连接
        self.signalConnect()

    '''
        信号和槽连接
    '''
    def signalConnect(self):
        #当前是否可以修改TableWidget数据
        self.pb_insert.clicked.connect(self.slotStateChange)

        #清除单选按钮选中状态
        self.pb_delState.clicked.connect(self.slotChangeCheckState)

        self.cb_showDistence.clicked.connect(self.slotClickedDistence)
    '''
        信号和槽连接断开
    '''
    def slotDisconnect(self):
        self.pb_insert.clicked.disconnect(self.slotStateChange)
        self.pb_delState.clicked.disconnect(self.slotChangeCheckState)


    '''
        功能：
            清除单选按钮选中状态
    '''
    def slotChangeCheckState(self):
        if self.rb_unitShow.isChecked():
            self.rb_unitShow.setChecked(False)

        if self.rb_equipShow.isChecked():
            self.rb_equipShow.setChecked(False)

    '''
        功能：
            当前是否可以修改TableWidget数据
    '''
    def slotStateChange(self):
        if self.tw_inquiryResult.editTriggers() == QAbstractItemView.CurrentChanged:
            self.tw_inquiryResult.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.pb_insert.setText("信息录入")
        else:
            self.tw_inquiryResult.setEditTriggers(QAbstractItemView.CurrentChanged)
            self.pb_insert.setText("信息展示及修改")

    def slotClickedDistence(self):
        self.tw_inquiryResult.clear()
        self.tw_inquiryResult.setRowCount(0)
        self.result_num = len(self.result)
        self.tw_inquiryResult.setRowCount(self.result_num)
        self.tw_inquiryResult.setColumnCount(13)
        headerlist = ['单位名称', '装备名称', '实力数', '编制数', '现有数', '偏差', '准备退役数', '未到位数', '提前退役', '待核查无实物', '待核查无实力', '单独建账',
                      '正常到位']
        self.tw_inquiryResult.setHorizontalHeaderLabels(headerlist)
        self.currentInquiryResult.clear()
        i = 0
        for data in self.result:
            if self.cb_showDistence.isChecked():
                if int(data[7]) != 0:
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
                    i = i + 1
                else:
                    pass
            else:
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
                i = i + 1
        self.tw_inquiryResult.setRowCount(i)
    '''
        功能：
            根据查询到的结果初始化tablewidget
    '''
    def _initTableWidget(self, result):
        #print(result)
        self.tw_inquiryResult.clear()
        self.result = result

        self.result_num = len(result)
        self.tw_inquiryResult.setRowCount(self.result_num)
        self.tw_inquiryResult.setColumnCount(13)
        headerlist = ['单位名称', '装备名称', '实力数', '编制数', '现有数', '偏差', '准备退役数', '未到位数', '提前退役', '待核查无实物', '待核查无实力', '单独建账',
                      '正常到位']
        self.tw_inquiryResult.setHorizontalHeaderLabels(headerlist)
        self.currentInquiryResult.clear()
        for i, data in enumerate(self.result):
            if self.cb_showDistence.isChecked():
                if int(data[7]) != 0:
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
                else:
                    pass
            else:
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

    # 删除选中装备
    def deleteInquiryResult(self):
        item = self.tw_inquiryResult.selectedItems()
        if len(item) == 0:
            return
        i = self.tw_inquiryResult.currentRow()
        UnitID = self.currentInquiryResult[i][1]
        EquipID = self.currentInquiryResult[i][0]
        print("UnitID=",UnitID,"EquipId=",EquipID)
        delete_Inquiry_Clicked(UnitID, EquipID)
        EquipIDList1=[]
        a=[e for e in range(self.result_num) if e != i]
        for j in a:
            EquipIDList1.append(self.currentInquiryResult[j][0])
        self.showInquiryResult(UnitID, EquipIDList1)

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