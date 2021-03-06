import sys
from PyQt5.QtWidgets import *
from widgets.alocatMange.armySche import widget_armySchedule
from database.strengthDisturbSql import *
from PyQt5.Qt import Qt
from database.alocatMangeSql import *
from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication

class ArmySchedule(QDialog, widget_armySchedule ):
    signal=QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(ArmySchedule, self).__init__(parent)
        self.setupUi(self)
        # 设置tablewidget左侧栏以及头部不显示
        self.tw_result.horizontalHeader().setVisible(False)
        self.tw_result.verticalHeader().setVisible(False)
        self.currentYear = ''
        # 初始化当前界面
        self._initSelf_()
        # 存储当前结果，结构为：{i（行数）：一行数据}
        self.currentResult = {}
        self.pb_selectArmy.clicked.connect(self.selectArmy)

    def selectArmy(self):
        #print("self.tw_result.currentRow()",self.tw_result.currentRow())
        if self.tw_result.currentRow() != 0 and self.tw_result.currentRow()!= 1:
            self.signal.emit('1')
            self.close()

    def setYear(self, year):
        self.currentYear = year
        self.slotSelectResult()
        #print(self.currentYear)

    def returnID(self):
        if self.tw_result.currentRow() != 0 and self.tw_result.currentRow() != 1:
            return self.resultList[self.tw_result.currentRow()-2][0]


    '''
        初始化当前界面，设置当前查询结果界面为灰
    '''
    def _initSelf_(self):
        self.tw_result.clear()


    '''
        初始化结果tablewidget表头
    '''
    def _initResultHeader_(self):
        self.orginRowCount = 0
        self.tw_result.clear()
        self.tw_result.setColumnCount(19)
        self.tw_result.setRowCount(2)
        item = QTableWidgetItem()
        item.setText('序号')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(0, 0, item)
        item = QTableWidgetItem()
        item.setText('调拨单信息')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(0, 1, item)
        item = QTableWidgetItem()
        item.setText('交装单位')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(0, 8, item)
        item = QTableWidgetItem()
        item.setText('接装单位')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(0, 11, item)
        item = QTableWidgetItem()
        item.setText('装备名称')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(0, 14, item)
        item = QTableWidgetItem()
        item.setText('计量单位')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(0, 15, item)
        item = QTableWidgetItem()
        item.setText('应发数')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(0, 16, item)
        item = QTableWidgetItem()
        item.setText('备注')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(0, 18, item)
        item = QTableWidgetItem()

        item.setText('调拨单号')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 1, item)
        item = QTableWidgetItem()
        item.setText('调拨日期')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 2, item)
        item = QTableWidgetItem()
        item.setText('调拨依据')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 3, item)
        item = QTableWidgetItem()
        item.setText('调拨')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 4, item)
        item = QTableWidgetItem()
        item.setText('调拨方式')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 5, item)
        item = QTableWidgetItem()
        item.setText('运输方式')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 6, item)
        item = QTableWidgetItem()
        item.setText('有效日期')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 7, item)
        item = QTableWidgetItem()
        item.setText('单位名称')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 8, item)
        item = QTableWidgetItem()
        item.setText('联系人')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 9, item)
        item = QTableWidgetItem()
        item.setText('联系电话')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 10, item)
        item = QTableWidgetItem()
        item.setText('单位名称')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 11, item)
        item = QTableWidgetItem()
        item.setText('联系人')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 12, item)
        item = QTableWidgetItem()
        item.setText('联系电话')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 13, item)
        item = QTableWidgetItem()
        item.setText('质量')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 16, item)
        item = QTableWidgetItem()
        item.setText('数量')
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置当前item不能被修改
        self.tw_result.setItem(1, 17, item)
        self.tw_result.setSpan(0, 0, 2, 1)
        self.tw_result.setSpan(0, 1, 1, 7)
        self.tw_result.setSpan(0, 8, 1, 3)
        self.tw_result.setSpan(0, 11, 1, 3)
        self.tw_result.setSpan(0, 16, 1, 2)
        self.tw_result.setSpan(0, 14, 2, 1)
        self.tw_result.setSpan(0, 15, 2, 1)
        self.tw_result.setSpan(0, 18, 2, 1)
        self.tw_result.setSelectionBehavior(QAbstractItemView.SelectRows)


    '''
        查找当前要显示的数据并显示到tablewidget上
    '''
    def slotSelectResult(self):
        self.currentResult = {}
        self._initResultHeader_()
        self.resultList = selectArmyTransferByYear(self.currentYear)
        self.tw_result.setRowCount(len(self.resultList) + 2)
        for i, armyTransferInfo in enumerate(self.resultList):
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[0])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 0, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[1])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 1, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[2])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 2, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[3])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 3, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[4])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 4, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[5])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 5, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[6])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 6, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[7])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 7, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[9])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 8, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[10])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 9, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[11])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 10, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[12])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 11, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[13])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 12, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[14])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 13, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[16])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 14, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[17])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 15, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[18])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 16, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[19])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 17, item)
            item = QTableWidgetItem()
            item.setText(armyTransferInfo[20])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 18, item)

