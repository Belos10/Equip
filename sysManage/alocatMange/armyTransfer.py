from widgets.alocatMange.armyTransfer import Widget_Army_Transfer
import sys
from PyQt5.QtWidgets import QApplication,QWidget, QListWidgetItem, QComboBox, QTableWidgetItem
from database.alocatMangeSql import selectYearListAboutArmy, selectArmyTransferByYear
from database.strengthDisturbSql import selectAllEndEquip
from sysManage.alocatMange.config import ArmyTransferReceiveUnit, ArmyTransferSendUnit

class armyTransfer(QWidget, Widget_Army_Transfer):
    def __init__(self, parent=None):
        super(armyTransfer, self).__init__(parent)
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

    def _initYearWidget_(self):
        self.yearList = []
        self.currentYear = ''
        self.lw_yearChoose.clear()
        self.yearList = ['全部']
        allYear = selectYearListAboutArmy()
        for year in allYear:
            self.yearList.append(year)

        for year in self.yearList:
            item = QListWidgetItem()
            item.setText(year)
            self.lw_yearChoose.addItem(item)

    def _initResultHeader_(self):
        self.orginRowCount = 0
        self.tw_result.setColumnCount(19)
        self.tw_result.setRowCount(2)
        self.firstHeader = ['序号', '调拨单信息', '交装单位', '接装单位', '装备名称', '计量单位',
                            '应发数', '备注']
        self.secondHeader = ['调拨单号', '调拨日期', '调拨依据', '调拨', '调拨方式', '运输方式',
                             '有效日期', '单位名称', '联系人', '联系电话', '单位名称', '联系人', '联系电话',
                             '质量', '数量']
        self.tw_result.setRowCount(2)
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
        row = self.lw_yearChoose.currentRow()
        self.currentYear = self.lw_yearChoose.item(row).text()
        resultList = selectArmyTransferByYear(self.currentYear)

    def addNewRow(self):
        currentRow = self.tw_result.rowCount()
        self.tw_result.setRowCount(currentRow + 1)

        for i in range(19):
            if i == 14:
                equipCombo = QComboBox()
                for equipInfo in self.equipTuple:
                    equipCombo.addItem(equipInfo[1])
                self.tw_result.setCellWidget(currentRow, i, equipCombo)
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