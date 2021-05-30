import sys
from widgets.alocatMange.addUnitChoose import Widget_AddUnitChoose
from database.strengthDisturbSql import *
from database.alocatMangeSql import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
from PyQt5 import QtCore


class AddChoose(QDialog, Widget_AddUnitChoose):
    signal=QtCore.pyqtSignal(str)
    def __init__(self,parent=None):
        super(AddChoose, self).__init__(parent)
        self.setupUi(self)
        self.signalConnect()
        self.unitAllList={}
        self.unitDisturbList={}
        self.initWidget()
        self.currentUnit=[]
        self.unitAllList = []

    def signalConnect(self):
        self.pb_Yes.clicked.connect(self.getCreaseUnit)
        self.pb_cancel.clicked.connect(self.close)

    def initWidget(self):
        self.tb_unitChoose.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.initUnitList()

    # 获取装备列表
    def initUnitList(self):
        header = ['单位编号', '单位名称', '上级单位编号', '单位别名']
        self.tb_unitChoose.setColumnCount(len(header))
        self.tb_unitChoose.setRowCount(len(self.unitAllList))
        self.tb_unitChoose.setHorizontalHeaderLabels(header)

        for i,unitInfo in enumerate(self.unitAllList):
            item = QTableWidgetItem(unitInfo[0])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tb_unitChoose.setItem(i, 0, item)
            item = QTableWidgetItem(unitInfo[1])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tb_unitChoose.setItem(i, 1, item)
            item = QTableWidgetItem(unitInfo[2])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tb_unitChoose.setItem(i, 2, item)
            item = QTableWidgetItem(unitInfo[3])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tb_unitChoose.setItem(i, 3, item)
        self.getCreaseUnit()

    # def getUsefulUnit(self,):
    #     self.unitDisturbList = selectAllDataAboutDisturbPlanUnit()
    #     for unitID in self.unitDisturbList:
    #         for i in range(self.tb_unitChoose.rowCount()):
    #             if unitID[0] == self.tb_unitChoose.item(i,0).text():
    #                 for j in range(self.tb_unitChoose.columnCount()):
    #                     self.tb_unitChoose.item(i,j).setFlags(Qt.NoItemFlags)


    def getCreaseUnit(self):
        self.currentUnit = []
        for i in self.tb_unitChoose.selectedRanges():
            for j in range(i.topRow(),i.bottomRow()+1):
                unitId = self.tb_unitChoose.item(j,0).text()
                name = self.tb_unitChoose.item(j,1).text()
                upper = self.tb_unitChoose.item(j,2).text()
                otherName = self.tb_unitChoose.item(j,3).text()
                unit = [unitId,name,upper,otherName]
                self.currentUnit.append(unit.copy())
        self.signal.emit('1')
        self.close()