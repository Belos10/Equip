from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from widgets.strengthDisturb.add_strenth_info import Add_Strenth_Info
from database.ConnectAndSql import Clicked, delete_Clicked

'''
    类功能：
        信息录入界面管理
'''

class AddStrenthInfo(QWidget, Add_Strenth_Info):
    def __init__(self, parent=None):
        super(AddStrenthInfo, self).__init__(parent)
        self.setupUi(self)

        self.data = None
        self.UnitID = None
        self.EquipID = None
        self.OrignNum = 0

    def signalConnect(self):
        self.pb_Increase.clicked.connect(self.slotAddSingle)

    def slotDisconnect(self):
        self.pb_Increase.clicked.disconnect(self.slotAddSingle)

    def _initWidget(self):
        sql = "select * from inputinfo where Unit_ID = '" + self.UnitID + \
              "' and Equip_ID = '" + self.EquipID + "'"
        print("_initweight", sql)
        currentInfo = Clicked(sql)
        self.tableWidget.setRowCount(len(currentInfo))
        self.OrignNum = len(currentInfo)
        for i, data in enumerate(currentInfo):
            item = QTableWidgetItem(data[2])
            self.tableWidget.setItem(i, 0, item)
            item = QTableWidgetItem(data[3])
            self.tableWidget.setItem(i, 1, item)
            item = QTableWidgetItem(data[4])
            self.tableWidget.setItem(i, 2, item)
            item = QTableWidgetItem(data[5])
            self.tableWidget.setItem(i, 3, item)
            item = QTableWidgetItem(data[6])
            self.tableWidget.setItem(i, 4, item)
            item = QTableWidgetItem(data[7])
            self.tableWidget.setItem(i, 5, item)
            item = QTableWidgetItem(data[8])
            self.tableWidget.setItem(i, 6, item)
            item = QTableWidgetItem(data[9])
            self.tableWidget.setItem(i, 7, item)

    def _initWeight(self, data):
        # print(data)
        self.tableWidget.clear()
        header = ['批次号', '数量', '出厂年份', '生产厂家', '装备状态', '是否到位', '文件凭证', '备注']
        self.tableWidget.setColumnCount(len(header))
        self.tableWidget.setHorizontalHeaderLabels(header)
        self.label_UnitName.setText(data[3])
        self.label_EquipName.setText(data[2])
        self.label_PowerNumber.setText(data[4])
        self.label_ExistNumber.setText(data[6])
        self.UnitID = data[1]
        self.EquipID = data[0]
        self.data = data
        self._initWidget()

    # 信息录入界面新增按钮
    def slotAddSingle(self):
        row_num = self.tableWidget.rowCount()
        # print("row num",row_num)
        clomn_num = self.tableWidget.columnCount()
        self.tableWidget.insertRow(row_num)
        self.row_num = row_num + 1

    # 信息录入界面删除按钮
    def deleteNote(self):
        item = self.tableWidget.selectedItems()
        if len(item) == 0:
            return
        Unit_ID = self.UnitID
        Equip_ID = self.EquipID
        i = self.tableWidget.currentRow()
        ID = self.tableWidget.item(i, 0).text()
        num = self.tableWidget.item(i, 1).text()
        year = self.tableWidget.item(i, 2).text()
        shop = self.tableWidget.item(i, 3).text()
        state = self.tableWidget.item(i, 4).text()
        arrive = self.tableWidget.item(i, 5).text()
        confirm = self.tableWidget.item(i, 6).text()
        other = self.tableWidget.item(i, 7).text()
        # print(ID, num, year, shop, state, arrive, confirm, other)
        delete_Clicked(Unit_ID, Equip_ID, ID, num, year, shop, state, arrive, confirm, other)
        self._initWidget()
