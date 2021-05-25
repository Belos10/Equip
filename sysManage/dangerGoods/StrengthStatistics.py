from PyQt5.QtCore import Qt
from database.danderGoodsSql import *
from sysManage.userInfo import get_value
from widgets.dangerGoods.dangerGoodsStatisticsUI import DangerGoodsStatisticsUI

import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidget, QHeaderView, QTableWidgetItem, QComboBox, \
    QMessageBox, QTreeWidgetItem


class StrengthStatistics(QWidget, DangerGoodsStatisticsUI):
    def __init__(self, parent=None):
        super(StrengthStatistics, self).__init__(parent)
        self.setupUi(self)
        self.startInfo = None
        self.dataLen = 0
        self.signalConnection()
        self.init()
    first_treeWidget_dict = {}
    currentLastRow = 0
    info = {}



    def initUserInfo(self):
        self.userInfo = get_value("totleUserInfo")
    #信号和槽连接
    def signalConnection(self):

        self.tb_input.clicked.connect(self.slotInput)
        self.tb_output.clicked.connect(self.slotOutput)
        self.tb_add.clicked.connect(self.slotAdd)
        self.tb_delete.clicked.connect(self.slotDelete)
        self.tw_result.itemChanged.connect(self.slotAlterAndSava)

        self.tw_first.itemClicked.connect(self.displayData)


    #信号和槽断开
    def slotDisconnect(self):
        pass

    #定义初始化函数
    def init(self):
        self.initUserInfo()
        self.tw_result.clear()
        self.tw_first.header().setVisible(False)

        self.first_treeWidget_dict = {}
        # 当前选中的单位列表和装备列表
        self.currentCheckedUnitList = []

        if self.userInfo:
            from database.strengthDisturbSql import selectUnitInfoByUnitID
            self.startInfo = selectUnitInfoByUnitID(self.userInfo[0][4])

        stack = []
        root = []
        if self.startInfo:
            stack.append(self.startInfo)
            root.append(self.tw_first)
            self._initUnitTreeWidget(stack, root)

        self.displayData()
        pass


    '''
        功能：
            将列表数据展示在表中
    '''
    def displayData(self):
        self.currentCheckedUnitList = []
        for unitID, unitItem in self.first_treeWidget_dict.items():
            if unitItem == self.tw_first.currentItem():
                self.currentCheckedUnitList.append(unitID)
        if len(self.currentCheckedUnitList) > 0:
            if gradeInUnit(self.currentCheckedUnitList[0]) == 3:
                self._initTableWidgetByUnit(self.currentCheckedUnitList[0])
                self.unit = self.currentCheckedUnitList[0]
            else:
                return

    '''
        功能：
            根据单位id获取数据并展示
    '''
    def _initTableWidgetByUnit(self,unit):

        self.rowCount =  2 + getCountOfUnit(unit)
        self.columnCount = 13
        self.currentLastRow = self.rowCount - 1
        self.initHeader()
        if self.rowCount > 2:
            trainResultCount = 0
            chemicalResultCount = 0
            trainResult = getDataByUnitAndType(unit,'训练用毒剂')
            if trainResult != None:
                self.diplayDataByType(2,trainResult,'训练用毒剂')
                trainResultCount = len(trainResult)
            else:
                trainResultCount = 0
            chemicalResult = getDataByUnitAndType(unit, '防化放射源')
            if chemicalResult != None:
                self.diplayDataByType(2 + trainResultCount, chemicalResult, '防化放射源')
                chemicalResultCount = len(chemicalResult)
            else:
                chemicalResultCount = 0
            explosionResult = getDataByUnitAndType(unit, '防化防爆弹药')
            if explosionResult != None:
                self.diplayDataByType(2 + trainResultCount + chemicalResultCount, explosionResult, '防化防爆弹药')
                self.dataLen = trainResultCount + chemicalResultCount + len(explosionResult)
            else:
                self.dataLen = trainResultCount + chemicalResultCount





    '''
        功能：
            展示数据
    '''
    def diplayDataByType(self,starIndex,typeData,type):
        item = QTableWidgetItem('%s'%type)
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(starIndex, 1, item)
        if len(typeData) != 1:
            self.tw_result.setSpan(starIndex, 1, len(typeData), 1)
        for i in range(len(typeData)):
            index = starIndex + i
            self.info[index] = typeData[i][0]
            #序号
            item = QTableWidgetItem(str(i + 1))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tw_result.setItem(starIndex + i, 0, item)

            #名称
            item = QTableWidgetItem(typeData[i][3])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tw_result.setItem(starIndex + i, 2, item)

            #单位
            item = QTableWidgetItem(typeData[i][4])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tw_result.setItem(starIndex + i, 3, item)

            #小计
            item = QTableWidgetItem(str(typeData[i][5]))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tw_result.setItem(starIndex + i, 5, item)

            #新堪品
            item = QTableWidgetItem(typeData[i][6])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tw_result.setItem(starIndex + i, 6, item)


            item = QTableWidgetItem(typeData[i][7])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tw_result.setItem(starIndex + i, 7, item)

            item = QTableWidgetItem(typeData[i][8])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tw_result.setItem(starIndex + i, 8, item)

            item = QTableWidgetItem(typeData[i][9])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tw_result.setItem(starIndex + i, 9, item)

            item = QTableWidgetItem(typeData[i][10])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tw_result.setItem(starIndex + i, 10, item)

            item = QTableWidgetItem(typeData[i][11])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tw_result.setItem(starIndex + i, 11, item)

            item = QTableWidgetItem(typeData[i][12])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tw_result.setItem(starIndex + i, 12, item)





    '''
                   功能：
                       单位目录的初始化，显示整个单位表
                       参数表：root为上级单位名字，mother为上级节点对象
       '''

    def _initUnitTreeWidget(self, stack, root):
        while stack:
            UnitInfo = stack.pop(0)
            item = QTreeWidgetItem(root.pop(0))
            item.setText(0, UnitInfo[1])
            # item.setCheckState(0, Qt.Unchecked)
            self.first_treeWidget_dict[UnitInfo[0]] = item
            result = selectUnitInfoByDeptUper(UnitInfo[0])
            for resultInfo in result:
                stack.append(resultInfo)
                root.append(item)


    '''
        功能：
            画表头,行数至少有3行
    '''

    # 初始化表头
    def initHeader(self):
        self.info.clear()
        self.tw_result.clear()
        self.tw_result.setRowCount(self.rowCount)
        self.tw_result.setColumnCount(self.columnCount)
        self.tw_result.verticalHeader().setVisible(False)
        self.tw_result.horizontalHeader().setVisible(False)
        # self.tw_result.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tw_result.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tw_result.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tw_result.resizeColumnsToContents()
        self.tw_result.resizeRowsToContents()

        # 绘制表头
        item = QTableWidgetItem("%s防化危险品实力统计" % getUnitNameById(self.currentCheckedUnitList[0]))
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(0, 0, item)
        self.tw_result.setSpan(0, 0, 1, self.columnCount)

        item = QTableWidgetItem("序号")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 0, item)

        item = QTableWidgetItem("类型")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 1, item)

        item = QTableWidgetItem("名称")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 2, item)

        item = QTableWidgetItem("单位")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 3, item)

        item = QTableWidgetItem("合计")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 4, item)

        item = QTableWidgetItem("小计")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 5, item)

        item = QTableWidgetItem("新堪品")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 6, item)

        item = QTableWidgetItem("废品")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 7, item)

        item = QTableWidgetItem("出场时间")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 8, item)

        item = QTableWidgetItem("入库时间")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 9, item)

        item = QTableWidgetItem("来源")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 10, item)

        item = QTableWidgetItem("放射性活度")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 11, item)

        item = QTableWidgetItem("备注")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 12, item)


        '''
            功能：
                新增一行的数据
        '''
    def slotAlterAndSava(self):
        selectRow = self.tw_result.selectedItems()
        if len(selectRow) == 0:
            return
        else:
            currentRow = selectRow[0].row()
            if currentRow == self.currentLastRow:
                self.savaRowData(currentRow)
            else:
                self.alterRowData(currentRow)
            pass


    def savaRowData(self,row):
        rowData = []
        rowData.append(self.unit)
        for i in range(1,self.tw_result.columnCount()):
            if i == 4:
                continue
            if i == 1 or i == 3 :
                item = self.tw_result.cellWidget(row,i)
                if item != None:
                    rowData.append(item.currentText())
            else:
                item = self.tw_result.item(row, i)
                if item != None and len(item.text()) > 0:
                    rowData.append(item.text())
                else:
                    break

        if len(rowData) < self.tw_result.columnCount() - 1:
            return False
        else:
            print(rowData)
            insertOneDataIntDangerGoods(rowData)
            QMessageBox.warning(self, "注意", "插入成功！", QMessageBox.Yes, QMessageBox.Yes)

    def alterRowData(self,row):

        rowData = []
        rowData.append(self.info[row])
        rowData.append(self.unit)
        for i in range(self.tw_result.columnCount()):
            if i == 0:
                continue
            if i == 3:
                continue
            item = self.tw_result.item(row, i)
            if item != None and len(item.text()) > 0:
                rowData.append(item.text())
            else:
                break

        print(rowData)
        if len(rowData) < self.tw_result.columnCount():
            return False
        else:
            if updataOneDataInDangerGood(rowData) == True:
                QMessageBox.warning(self, "注意", "修改成功！", QMessageBox.Yes, QMessageBox.Yes)
        pass





    #组件
    def slotInput(self):
        pass

    def slotOutput(self):
        pass
    '''
        功能：
            新增按钮槽函数
    '''
    def slotAdd(self):
        if self.tw_result.rowCount() < 3 + self.dataLen:
            rowCount =  self.tw_result.rowCount()
            self.currentLastRow = rowCount
            self.tw_result.insertRow(rowCount)
            comboBox = QComboBox()
            comboBox.addItems(['训练用毒剂', '防化放射源','防化防爆弹药'])
            self.tw_result.setCellWidget(rowCount, 1, comboBox)
            comboBox = QComboBox()
            comboBox.addItems(['千克', '块','瓶','枚'])
            self.tw_result.setCellWidget(rowCount, 3, comboBox)
        else:
            QMessageBox.warning(self, "注意", "请先将数据添加完成！", QMessageBox.Yes, QMessageBox.Yes)
            pass

    def slotDelete(self):
        selectedRow = self.tw_result.currentRow()
        if selectedRow < 2:
            QMessageBox.warning(self, "注意", "请选中有效单元格！", QMessageBox.Yes, QMessageBox.Yes)
        elif selectedRow >= 2 and selectedRow < self.dataLen + 2:
            goodsId = self.info[selectedRow]
            if deleteByDangerGoodsId(goodsId) == True:
                self.tw_result.removeRow(selectedRow)
        else:
            self.tw_result.removeRow(selectedRow)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = StrengthStatistics()
    widget.show()
    sys.exit(app.exec_())