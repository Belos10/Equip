from widgets.alocatMange.rocketTransfer import Widget_Rocket_Transfer
import sys
from PyQt5.QtWidgets import QApplication,QWidget, QListWidgetItem, QComboBox, QTableWidgetItem, QDateEdit, QInputDialog
from database.alocatMangeSql import selectYearListAboutArmy, selectArmyTransferByYear, insertIntoArmyTransferYear, \
    insertIntoRocketTransferYear, selectYearListAboutRocket, selectRocketTransferByYear
from database.strengthDisturbSql import selectAllEndEquip
from sysManage.alocatMange.config import ArmyTransferReceiveUnit, ArmyTransferSendUnit

'''
   火箭军调拨单管理
'''
class rocketTransfer(QWidget, Widget_Rocket_Transfer):
    def __init__(self, parent=None):
        super(rocketTransfer, self).__init__(parent)
        self.setupUi(self)

        self.tw_result.horizontalHeader().setVisible(False)
        self.tw_result.verticalHeader().setVisible(False)

        self._initYearWidget_()
        self._initResultHeader_()

        self.signalConnect()

        self.currentResult = {}

    def signalConnect(self):
        self.lw_yearChoose.itemPressed.connect(self.slotSelectResult)
        self.pb_add.clicked.connect(self.addNewRow)
        self.tb_add.clicked.connect(self.slotAddNewYear)

    def slotAddNewYear(self):
        year = 0
        year, ok = QInputDialog.getInt(self, "Get year", "year:", 0, 0, 100000, 1)
        if year:
            insertIntoRocketTransferYear(year)
            self._initYearWidget_()

    def _initYearWidget_(self):
        self.yearList = []
        self.currentYear = ''
        self.lw_yearChoose.clear()
        self.yearList = ['全部']
        allYear = selectYearListAboutRocket()
        for year in allYear:
            self.yearList.append(year)

        for year in self.yearList:
            item = QListWidgetItem()
            item.setText(year)
            self.lw_yearChoose.addItem(item)

    def _initResultHeader_(self):
        self.orginRowCount = 0
        self.tw_result.clear()
        self.tw_result.setColumnCount(19)
        self.tw_result.setRowCount(2)
        item = QTableWidgetItem()
        item.setText('序号')
        self.tw_result.setItem(0, 0, item)
        item = QTableWidgetItem()
        item.setText('调拨单信息')
        self.tw_result.setItem(0, 1, item)
        item = QTableWidgetItem()
        item.setText('交装单位')
        self.tw_result.setItem(0, 8, item)
        item = QTableWidgetItem()
        item.setText('接装单位')
        self.tw_result.setItem(0, 11, item)
        item = QTableWidgetItem()
        item.setText('装备名称')
        self.tw_result.setItem(0, 14, item)
        item = QTableWidgetItem()
        item.setText('计量单位')
        self.tw_result.setItem(0, 15, item)
        item = QTableWidgetItem()
        item.setText('应发数')
        self.tw_result.setItem(0, 16, item)
        item = QTableWidgetItem()
        item.setText('备注')
        self.tw_result.setItem(0, 18, item)
        item = QTableWidgetItem()

        item.setText('调拨单号')
        self.tw_result.setItem(1, 1, item)
        item = QTableWidgetItem()
        item.setText('调拨日期')
        self.tw_result.setItem(1, 2, item)
        item = QTableWidgetItem()
        item.setText('调拨依据')
        self.tw_result.setItem(1, 3, item)
        item = QTableWidgetItem()
        item.setText('调拨')
        self.tw_result.setItem(1, 4, item)
        item = QTableWidgetItem()
        item.setText('调拨方式')
        self.tw_result.setItem(1, 5, item)
        item = QTableWidgetItem()
        item.setText('运输方式')
        self.tw_result.setItem(1, 6, item)
        item = QTableWidgetItem()
        item.setText('有效日期')
        self.tw_result.setItem(1, 7, item)
        item = QTableWidgetItem()
        item.setText('单位名称')
        self.tw_result.setItem(1, 8, item)
        item = QTableWidgetItem()
        item.setText('联系人')
        self.tw_result.setItem(1, 9, item)
        item = QTableWidgetItem()
        item.setText('联系电话')
        self.tw_result.setItem(1, 10, item)
        item = QTableWidgetItem()
        item.setText('单位名称')
        self.tw_result.setItem(1, 11, item)
        item = QTableWidgetItem()
        item.setText('联系人')
        self.tw_result.setItem(1, 12, item)
        item = QTableWidgetItem()
        item.setText('联系电话')
        self.tw_result.setItem(1, 13, item)
        item = QTableWidgetItem()
        item.setText('质量')
        self.tw_result.setItem(1, 16, item)
        item = QTableWidgetItem()
        item.setText('数量')
        self.tw_result.setItem(1, 17, item)

        self.tw_result.setSpan(0, 0, 2, 1)
        self.tw_result.setSpan(0, 1, 1, 7)
        self.tw_result.setSpan(0, 8, 1, 3)
        self.tw_result.setSpan(0, 11, 1, 3)
        self.tw_result.setSpan(0, 16, 1, 2)
        self.tw_result.setSpan(0, 14, 2, 1)
        self.tw_result.setSpan(0, 15, 2, 1)
        self.tw_result.setSpan(0, 18, 2, 1)
        self.equipTuple = selectAllEndEquip()

    def slotSelectResult(self):
        self._initResultHeader_()
        row = self.lw_yearChoose.currentRow()
        self.currentYear = self.lw_yearChoose.item(row).text()
        resultList = selectRocketTransferByYear(self.currentYear)
        self.tw_result.setRowCount(len(resultList) + 2)
        print(resultList)
        for i, rocketTransferInfo in enumerate(resultList):
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[0])
            self.tw_result.setItem(i + 2, 0, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[1])
            self.tw_result.setItem(i + 2, 1, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[2])
            self.tw_result.setItem(i + 2, 2, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[3])
            self.tw_result.setItem(i + 2, 3, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[4])
            self.tw_result.setItem(i + 2, 4, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[5])
            self.tw_result.setItem(i + 2, 5, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[6])
            self.tw_result.setItem(i + 2, 6, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[7])
            self.tw_result.setItem(i + 2, 7, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[9])
            self.tw_result.setItem(i + 2, 8, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[10])
            self.tw_result.setItem(i + 2, 9, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[11])
            self.tw_result.setItem(i + 2, 10, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[12])
            self.tw_result.setItem(i + 2, 11, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[13])
            self.tw_result.setItem(i + 2, 12, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[14])
            self.tw_result.setItem(i + 2, 13, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[16])
            self.tw_result.setItem(i + 2, 14, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[17])
            self.tw_result.setItem(i + 2, 15, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[18])
            self.tw_result.setItem(i + 2, 16, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[19])
            self.tw_result.setItem(i + 2, 17, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[20])
            self.tw_result.setItem(i + 2, 18, item)

    def addNewRow(self):
        currentRow = self.tw_result.rowCount()
        self.tw_result.setRowCount(currentRow + 1)

        for i in range(19):
            if i == 14:
                equipCombo = QComboBox()
                for equipInfo in self.equipTuple:
                    equipCombo.addItem(equipInfo[1])
                self.tw_result.setCellWidget(currentRow, i, equipCombo)
            elif i == 2:
                dateEdit = QDateEdit()
                self.tw_result.setCellWidget(currentRow, i, dateEdit)
            elif i == 7:
                dateEdit = QDateEdit()
                self.tw_result.setCellWidget(currentRow, i, dateEdit)
            elif i == 11:
                item = QTableWidgetItem()
                item.setText(ArmyTransferReceiveUnit['单位名称'])
                self.tw_result.setItem(currentRow, i, item)
            elif i == 12:
                item = QTableWidgetItem()
                item.setText(ArmyTransferReceiveUnit['联系人'])
                self.tw_result.setItem(currentRow, i, item)
            elif i == 13:
                item = QTableWidgetItem()
                item.setText(ArmyTransferReceiveUnit['联系电话'])
                self.tw_result.setItem(currentRow, i, item)
            elif i == 8:
                item = QTableWidgetItem()
                item.setText(ArmyTransferSendUnit['单位名称'])
                self.tw_result.setItem(currentRow, i, item)
            elif i == 9:
                item = QTableWidgetItem()
                item.setText(ArmyTransferSendUnit['联系人'])
                self.tw_result.setItem(currentRow, i, item)
            elif i == 10:
                item = QTableWidgetItem()
                item.setText(ArmyTransferSendUnit['联系电话'])
                self.tw_result.setItem(currentRow, i, item)
            else:
                item = QTableWidgetItem()
                item.setText("")
                self.tw_result.setItem(currentRow, i, item)