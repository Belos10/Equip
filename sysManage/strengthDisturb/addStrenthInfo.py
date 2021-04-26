from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from widgets.strengthDisturb.add_strenth_info import Add_Strenth_Info
from database.strengthDisturbSql import selectEquipInputType, selectInfoAboutInput, selectNowNumAndStrengthNum

'''
    类功能：
        信息录入界面管理
'''
#更新
class AddStrenthInfo(QWidget, Add_Strenth_Info):
    def __init__(self, parent=None):
        super(AddStrenthInfo, self).__init__(parent)
        self.setupUi(self)
        self.currentResult = {}
        self.orginRowNum = 0
        self.strgenthInfo = None
        self.isChange = False
        self.unitID = None
        self.equipID = None

        self.signalConnect()

    def signalConnect(self):
        #新增按钮
        self.pb_Increase.clicked.connect(self.slotAddSingle)

        #查看数据是否修改
        self.tableWidget.itemChanged.connect(self.slotItemChanged)


    def slotDisconnect(self):
        self.pb_Increase.clicked.disconnect(self.slotAddSingle)

    def slotItemChanged(self, item):
        row = item.row()
        for i, resultRow in enumerate(self.currentResult):
            if i == row:
                self.tableWidget.item(row, 0).setText(resultRow[2])
    '''
        功能：
            初始化录入信息界面以及tablewidget
    '''
    def _initTableWidget_(self, RowData, yearList):
        self.yearList = yearList
        self.tableWidget.setRowCount(0)
        self.strgenthInfo = RowData
        self.now, self.strength= selectNowNumAndStrengthNum(RowData[1], RowData[0])
        self.label_UnitName.setText(RowData[3])
        self.label_EquipName.setText(RowData[2])
        self.label_ExistNumber.setText(self.now)
        self.label_PowerNumber.setText(self.strength)
        isMutilInput = selectEquipInputType(RowData[0]) #查看是否是逐批信息录入
        if isMutilInput:
            self.textBrowser.setText("逐批信息录入")
            self.header = ['批次号', '数量', '出厂年份', '生产厂家', '装备状态', '是否到位', '文件凭证', '备注']
            self.tableWidget.setColumnCount(len(self.header))
            self.tableWidget.setHorizontalHeaderLabels(self.header)
            self.currentResult = selectInfoAboutInput(RowData[1], RowData[0])
            self.tableWidget.setRowCount(len(self.currentResult))
            self.orginRowNum = len(self.currentResult)
            for i, data in enumerate(self.currentResult):
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
                self.currentResult[i] = data
        else:
            self.textBrowser.setText("逐号信息录入")
            self.header = ['批次号', '出厂年份', '生产厂家', '装备状态', '是否到位', '文件凭证', '备注']
            self.tableWidget.setColumnCount(len(self.header))
            self.tableWidget.setHorizontalHeaderLabels(self.header)
            self.currentResult = selectInfoAboutInput(RowData[1], RowData[0])
            self.orginRowNum = len(self.currentResult)
            for i, data in enumerate(self.currentResult):
                item = QTableWidgetItem(data[2])
                self.tableWidget.setItem(i, 0, item)
                item = QTableWidgetItem(data[4])
                self.tableWidget.setItem(i, 1, item)
                item = QTableWidgetItem(data[5])
                self.tableWidget.setItem(i, 2, item)
                item = QTableWidgetItem(data[6])
                self.tableWidget.setItem(i, 3, item)
                item = QTableWidgetItem(data[7])
                self.tableWidget.setItem(i, 4, item)
                item = QTableWidgetItem(data[8])
                self.tableWidget.setItem(i, 5, item)
                item = QTableWidgetItem(data[9])
                self.tableWidget.setItem(i, 6, item)
                self.currentResult[i] = data
        self.isChange = False

    # 信息录入界面新增按钮
    def slotAddSingle(self):
        row = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(row + 1)
        item = QTableWidgetItem("")
        self.tableWidget.setItem(row + 1, 0, item)
        item = QTableWidgetItem("")
        self.tableWidget.setItem(row + 1, 1, item)
        item = QTableWidgetItem("")
        self.tableWidget.setItem(row + 1, 2, item)
        item = QTableWidgetItem("")
        self.tableWidget.setItem(row + 1, 3, item)
        item = QTableWidgetItem("")
        self.tableWidget.setItem(row + 1, 4, item)
        item = QTableWidgetItem("")
        self.tableWidget.setItem(row + 1, 5, item)
        item = QTableWidgetItem("")
        self.tableWidget.setItem(row + 1, 6, item)
        item = QTableWidgetItem("")
        self.tableWidget.setItem(row + 1, 7, item)


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
        self._initTableWidget(self.data)
