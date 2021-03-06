import sys
from PyQt5.QtWidgets import *
from database.OrderManageSql import selectDataFromContractOrder
from widgets.orderManage.Widget_SelectCont import widget_selectCont
from database.strengthDisturbSql import *
from PyQt5.Qt import Qt
from database.alocatMangeSql import *
from PyQt5 import QtCore

class SelectCont(QDialog, widget_selectCont):
    signal=QtCore.pyqtSignal(str)
    def __init__(self, parent=None):
        super(SelectCont, self).__init__(parent)
        self.setupUi(self)
        self.currentYear = ''
        # 初始化当前界面
        self._initSelf_()
        self.pb_selectCont.clicked.connect(self.selectCont)


    def selectCont(self):
        self.row = self.seltCont.currentRow()
        if self.seltCont.currentRow() >= 0:
            self.signal.emit('1')
            self.close()


    def returnNo(self):
        return self.contData[self.row][2]

    def setYear(self, year):
        self.currentYear = year
        self.slotSelectResult()


    # 初始化当前界面，设置当前查询结果界面为灰
    def _initSelf_(self):
        self.seltCont.clear()


    # 查找当前要显示的数据并显示到tablewidget上
    def slotSelectResult(self):
        self.seltCont.clear()
        self.contData = selectDataFromContractOrder(self.currentYear)
        headerlist = ['年份', '序号', '合同编号', '合同名称', '甲方', '乙方', '单价(万元)', '数量/单位','金额(万元)','交付时间','备注']
        self.lenHeaderList = len(headerlist)
        self.seltCont.setColumnCount(self.lenHeaderList)
        self.seltCont.setRowCount(len(self.contData))
        self.seltCont.setHorizontalHeaderLabels(headerlist)
        i = 0
        for contDataInfo in self.contData:
            item = QTableWidgetItem()
            item.setText(contDataInfo[1])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.seltCont.setItem(i, 0, item)
            item = QTableWidgetItem()
            item.setText(str(contDataInfo[0]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.seltCont.setItem(i, 1, item)
            item = QTableWidgetItem()
            item.setText(contDataInfo[2])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.seltCont.setItem(i, 2, item)
            item = QTableWidgetItem()
            item.setText(contDataInfo[3])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.seltCont.setItem(i, 3, item)
            item = QTableWidgetItem()
            item.setText(contDataInfo[4])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.seltCont.setItem(i, 4, item)
            item = QTableWidgetItem()
            item.setText(contDataInfo[5])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.seltCont.setItem(i, 5, item)
            item = QTableWidgetItem()
            item.setText(str(contDataInfo[6]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.seltCont.setItem(i, 6, item)
            item = QTableWidgetItem()
            item.setText(str(contDataInfo[7]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.seltCont.setItem(i, 7, item)
            item = QTableWidgetItem()
            item.setText(str(contDataInfo[8]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.seltCont.setItem(i, 8, item)
            item = QTableWidgetItem()
            item.setText(str(contDataInfo[9]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.seltCont.setItem(i, 9, item)
            item = QTableWidgetItem()
            item.setText(contDataInfo[10])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.seltCont.setItem(i, 10, item)
        self.seltCont.setSelectionBehavior(QAbstractItemView.SelectRows)

