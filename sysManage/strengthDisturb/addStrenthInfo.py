from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QComboBox, QMessageBox
from widgets.strengthDisturb.add_strenth_info import Add_Strenth_Info
from database.strengthDisturbSql import *

'''
    类功能：
        信息录入界面管理
'''
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
        self.isMutilInput = None
        self.allYear = None

        self.signalConnect()

    def signalConnect(self):
        #新增按钮
        self.pb_Increase.clicked.connect(self.slotAddSingle)

        #查看数据是否修改
        self.tableWidget.itemChanged.connect(self.slotItemChanged)

        #删除某行数据
        self.pb_Delete.clicked.connect(self.deleteNote)


    def slotDisconnect(self):
        self.pb_Increase.clicked.disconnect(self.slotAddSingle)
        # 查看数据是否修改
        self.tableWidget.itemChanged.disconnect(self.slotItemChanged)

    '''
        当前有行的数据被改变
    '''
    def slotItemChanged(self, item):
        haveYear = False
        row = item.row()
        if row + 1 > self.orginRowNum:
            return
        else:
            currentColumn = self.tableWidget.currentColumn()
            if self.isMutilInput:
                for i, resultRow in enumerate(self.currentResult):
                    if i == row:
                        if currentColumn == 0:
                            self.tableWidget.item(row, 0).setText(resultRow[2])
                        elif currentColumn == 1:
                            reply = QMessageBox.question(self, '修改', '是否修改当前行的值？', QMessageBox.Yes,
                                                         QMessageBox.Cancel)
                            if reply == QMessageBox.Yes:
                                updateNumMutilInput(resultRow[0], resultRow[1], resultRow[2],
                                                    self.tableWidget.item(row, 1).text(), resultRow[3], resultRow[4])
                                self._initTableWidget_(self.RowData, self.yearList)
                        else:
                            reply = QMessageBox.question(self, '修改', '是否修改当前行的值？', QMessageBox.Yes,
                                                         QMessageBox.Cancel)
                            if reply == QMessageBox.Yes:
                                if currentColumn == 2:
                                    year = self.tableWidget.item(row, 2).text()
                                    for y in self.allYear:
                                        if year == y:
                                            haveYear = True
                                    if haveYear == False:
                                        reply = QMessageBox.question(self, '修改', '当前年份不存在， 修改失败', QMessageBox.Yes)
                                        self.tableWidget.item(row, currentColumn).setText(resultRow[currentColumn + 2])
                                        return
                                ID = self.tableWidget.item(row, 0).text()
                                num = self.tableWidget.item(row, 1).text()
                                year = self.tableWidget.item(row, 2).text()
                                shop = self.tableWidget.item(row, 3).text()
                                state = self.tableWidget.item(row, 4).text()
                                arrive = self.tableWidget.item(row, 5).text()
                                confirm = self.tableWidget.item(row, 6).text()
                                other = self.tableWidget.item(row, 7).text()
                                print(self.unitID, self.equipID, ID, num, year, shop, state, arrive, confirm, other)
                                updateInputInfo(self.unitID, self.equipID, ID, num, year, shop, state, arrive, confirm, other, self.yearList)
                            else:
                                self.tableWidget.item(row, currentColumn).setText(resultRow[currentColumn + 2])
            else:
                for i, resultRow in enumerate(self.currentResult):
                    if i == row:
                        if currentColumn == 0:
                            self.tableWidget.item(row, 0).setText(resultRow[2])
                        else:
                            reply = QMessageBox.question(self, '修改', '是否修改当前行的值？', QMessageBox.Yes,
                                                         QMessageBox.Cancel)
                            if reply == QMessageBox.Yes:
                                if currentColumn == 1:
                                    year = self.tableWidget.item(row, 2).text()
                                    for y in self.allYear:
                                        if year == y:
                                            haveYear = True
                                    if haveYear == False:
                                        reply = QMessageBox.question(self, '修改', '当前年份不存在， 修改失败', QMessageBox.Yes,
                                                                 QMessageBox.Cancel)
                                        self.tableWidget.item(row, currentColumn).setText(resultRow[currentColumn + 2])
                                        return
                                ID = self.tableWidget.item(row, 0).text()
                                year = self.tableWidget.item(row, 1).text()
                                shop = self.tableWidget.item(row, 2).text()
                                state = self.tableWidget.item(row, 3).text()
                                arrive = self.tableWidget.item(row, 4).text()
                                confirm = self.tableWidget.item(row, 5).text()
                                other = self.tableWidget.item(row, 6).text()
                                updateInputInfo(self.unitID, self.equipID, ID, "1", year, shop, state, arrive, confirm,
                                                other)
                            else:
                                self.tableWidget.item(row, currentColumn).setText(resultRow[currentColumn + 2])

    '''
        功能：
            初始化录入信息界面以及tablewidget
    '''
    def _initTableWidget_(self, RowData, yearList, factoryYear):
        if factoryYear == "全部":
            self.factoryYear = ""
        else:
            self.factoryYear = factoryYear
        self.RowData = RowData
        print("test:                 ", self.RowData)
        self.tableWidget.itemChanged.disconnect(self.slotItemChanged)
        self.unitID = RowData[1]
        self.equipID = RowData[0]
        #self.factoryYear = factoryYear
        if findEquipUnitByEquipID(self.equipID):
            self.equipUnit = findEquipUnitByEquipID(self.equipID)[0][0]
        else:
            self.equipUnit = ""
        self.label_MeasureUnit.setText(self.equipUnit)

        print(self.unitID, self.equipID)
        self.allYear = selectAllStrengthYear()
        self.yearList = yearList
        self.tableWidget.setRowCount(0)
        self.strgenthInfo = RowData
        self.now, self.strength= selectNowNumAndStrengthNum(RowData[1], RowData[0], self.yearList, self.factoryYear)
        self.label_UnitName.setText(RowData[3])
        self.label_EquipName.setText(RowData[2])
        self.label_ExistNumber.setText(self.now)
        self.label_PowerNumber.setText(self.strength)
        self.isMutilInput = selectEquipInputType(RowData[0]) #查看是否是逐批信息录入
        if self.isMutilInput:
            self.textBrowser.setText("逐批信息录入")
            self.header = ['批次号', '数量', '出厂年份', '生产厂家', '装备状态', '是否到位', '文件凭证', '备注']
            self.tableWidget.setColumnCount(len(self.header))
            self.tableWidget.setHorizontalHeaderLabels(self.header)
            self.currentResult = selectInfoAboutInput(RowData[1], RowData[0], self.yearList, self.factoryYear)
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
            self.currentResult = selectInfoAboutInput(RowData[1], RowData[0], self.yearList, self.factoryYear)
            self.tableWidget.setRowCount(len(self.currentResult))
            self.orginRowNum = len(self.currentResult)
            #print("结果为：", self.currentResult)
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
        self.tableWidget.itemChanged.connect(self.slotItemChanged)

    # 信息录入界面新增按钮
    def slotAddSingle(self):
        #yearList = selectAllStrengthYear()
        if self.isMutilInput:
            row = self.tableWidget.rowCount()
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
            self.tableWidget.setRowCount(row + 1)
        else:
            row = self.tableWidget.rowCount()
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
            self.tableWidget.setRowCount(row + 1)

    # 信息录入界面删除按钮
    def deleteNote(self):
        currentRow = self.tableWidget.currentRow()
        if currentRow < 0:
            return
        else:
            reply = QMessageBox.question(self, '删除', '是否删除当前行？', QMessageBox.Yes, QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                for i, resultInfo in enumerate(self.currentResult):
                    if i == currentRow:
                        year = resultInfo[4]
                        delFromInputInfo(resultInfo[0], resultInfo[1], resultInfo[2], resultInfo[3], resultInfo[4], self.yearList)
                        inputInfo = selectDataFromInputByYear(year)
                        if inputInfo:
                            pass
                        else:
                            delFactoryYear(year)
                        reply = QMessageBox.question(self, '删除', '删除成功！', QMessageBox.Yes)
                        self._initTableWidget_(self.RowData, self.yearList, self.factoryYear)
                        return
