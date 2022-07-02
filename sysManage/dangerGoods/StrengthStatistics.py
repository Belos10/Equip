from PyQt5.QtCore import Qt, QDate
from database.danderGoodsSql import *
from sysManage.userInfo import get_value
from widgets.dangerGoods.dangerGoodsStatisticsUI import DangerGoodsStatisticsUI
from sysManage.component import getMessageBox
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidget, QHeaderView, QTableWidgetItem, QComboBox, \
    QMessageBox, QTreeWidgetItem, QDateEdit


class StrengthStatistics(QWidget, DangerGoodsStatisticsUI):
    def __init__(self, parent=None):
        super(StrengthStatistics, self).__init__(parent)
        self.setupUi(self)
        self.startInfo = None
        self.dataLen = 0
        self.currentLastRow = -1
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
        self.pb_firstSelect.clicked.connect(self.slotSelectUnit)
        self.tw_first.itemClicked.connect(self.displayData)


    def slotSelectUnit(self):
        findText = self.le_first.text()
        for i, item in self.first_treeWidget_dict.items():
            if item.text(0) == findText:
                self.tw_first.setCurrentItem(item)
                break
    #信号和槽断开
    def slotDisconnect(self):
        pass

    #定义初始化函数
    def init(self):
        self.initUserInfo()
        self.tw_result.clear()
        self.tw_first.header().setVisible(False)
        self.tb_input.setDisabled(True)
        self.tb_input.setVisible(False)
        self.tb_output.setDisabled(True)
        self.tb_output.setVisible(False)

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
        self.tw_result.itemChanged.disconnect(self.slotAlterAndSava)
        self.rowCount =  2 + getCountOfUnit(unit)
        self.columnCount = 13
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
        self.tw_result.itemChanged.connect(self.slotAlterAndSava)





    '''
        功能：
            展示数据
    '''
    def diplayDataByType(self,starIndex,typeData,type):
        item = QTableWidgetItem('%s'%type)
        item.setFlags(Qt.ItemIsEnabled)
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(starIndex, 1, item)
        if len(typeData) != 1:
            self.tw_result.setSpan(starIndex, 1, len(typeData), 1)
        for i in range(len(typeData)):
            index = starIndex + i
            self.info[index] = typeData[i][0]
            #序号
            item = QTableWidgetItem(str(i + 1))
            item.setFlags(Qt.ItemIsEnabled)
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

            # 合计
            item = QTableWidgetItem(str(typeData[i][5]))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tw_result.setItem(starIndex + i, 4, item)

            #小计
            item = QTableWidgetItem(str(typeData[i][6]))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tw_result.setItem(starIndex + i, 5, item)

            #新堪品
            item = QTableWidgetItem(typeData[i][7])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tw_result.setItem(starIndex + i, 6, item)

            item = QTableWidgetItem(typeData[i][8])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tw_result.setItem(starIndex + i, 7, item)

            date = typeData[i][9]
            item = QTableWidgetItem(date)
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(starIndex + i, 8, item)


            # parsedDateList = date.split('-')
            # dataEdit = QDateEdit()
            # dataEdit.setDisplayFormat("yyyy-MM-dd")
            # dataEdit.setDate(QDate(int(parsedDateList[0]), int(parsedDateList[1]), int(parsedDateList[2])))
            # self.tw_result.setCellWidget(2 + i, 8, dataEdit)
            # dataEdit.dateChanged.connect(self.slotAlterAndSava)

            date = typeData[i][10]
            item = QTableWidgetItem(date)
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(starIndex + i, 9, item)
            # parsedDateList = date.split('-')
            # dataEdit = QDateEdit()
            # dataEdit.setDisplayFormat("yyyy-MM-dd")
            # dataEdit.setDate(QDate(int(parsedDateList[0]), int(parsedDateList[1]), int(parsedDateList[2])))
            # self.tw_result.setCellWidget(2 + i, 9, dataEdit)
            # dataEdit.dateChanged.connect(self.slotAlterAndSava)

            item = QTableWidgetItem(typeData[i][11])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tw_result.setItem(starIndex + i, 10, item)

            item = QTableWidgetItem(typeData[i][12])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tw_result.setItem(starIndex + i, 11, item)

            item = QTableWidgetItem(typeData[i][13])
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
        self.tw_first.expandAll()


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
        print('selectRow',selectRow)
        if len(selectRow) == 0:
            return
        else:
            currentRow = selectRow[0].row()
            if currentRow == self.currentLastRow:
                self.savaRowData(currentRow)
            else:
                self.alterRowData(currentRow)




    def savaRowData(self,row):
        rowData = []
        rowData.append(self.unit)
        for i in range(1,self.tw_result.columnCount()):

            if i == 1 or i == 3 :
                item = self.tw_result.cellWidget(row,i)
                if item != None:
                    rowData.append(item.currentText())
            elif i == 8 or i == 9:
                item = self.tw_result.cellWidget(row, i)
                if item != None:
                    date = item.date().toString(Qt.ISODate)
                    rowData.append(date)
            else:
                item = self.tw_result.item(row, i)

                if item != None and len(item.text()) > 0:
                    rowData.append(item.text())
                else:
                    break

        if len(rowData) < self.tw_result.columnCount():
            return False
        else:
            insertOneDataIntDangerGoods(rowData)
            self.currentLastRow = -1
            self._initTableWidgetByUnit(self.unit)
            getMessageBox("注意", "插入成功！", True, False)

    def alterRowData(self,row):

        rowData = []
        rowData.append( self.info[row])
        for i in range(2, self.tw_result.columnCount()):
            item = self.tw_result.item(row, i)
            if i == 12:
                if item != None:
                    rowData.append(item.text())
                else:
                    break
            else:
                if item != None and len(item.text()) > 0:
                    rowData.append(item.text())
                else:
                    break
        print(rowData)
        if len(rowData) == self.tw_result.columnCount() - 1:
            if (updataOneDataInDangerGood(rowData) == True):
                getMessageBox("注意", "修改成功！", True, False)
                self._initTableWidgetByUnit(self.unit)
            else:
                getMessageBox("警告", "修改失败！", True, False)






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
        if self.tw_result.rowCount() <= 2 + self.dataLen:
            self.tw_result.itemChanged.disconnect(self.slotAlterAndSava)
            rowCount =  self.tw_result.rowCount()
            self.currentLastRow = rowCount
            self.tw_result.insertRow(rowCount)
            if (rowCount + 1 == 3):
                item = QTableWidgetItem('1')
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.tw_result.setItem(2, 0, item)
            else:
                lastNo = int(self.tw_result.item(rowCount - 1,0).text())
                item = QTableWidgetItem(str(lastNo + 1))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.tw_result.setItem(rowCount, 0, item)

            comboBox = QComboBox()
            comboBox.addItems(['训练用毒剂', '防化放射源','防化防爆弹药'])
            self.tw_result.setCellWidget(rowCount, 1, comboBox)
            comboBox = QComboBox()
            comboBox.addItems(['千克', '块','瓶','枚'])
            self.tw_result.setCellWidget(rowCount, 3, comboBox)

            deliveryDate = QDateEdit()
            deliveryDate.setDisplayFormat("yyyy-MM-dd")
            self.tw_result.setCellWidget(rowCount, 8, deliveryDate)
            storeDate = QDateEdit()
            storeDate.setDisplayFormat("yyyy-MM-dd")
            self.tw_result.setCellWidget(rowCount, 9, storeDate)
            self.tw_result.itemChanged.connect(self.slotAlterAndSava)
        else:
            getMessageBox("注意", "请先将数据添加完成！", True, False)
            pass

    def slotDelete(self):
        selectedRow = self.tw_result.currentRow()
        if selectedRow < 2:
            getMessageBox("注意", "请选中有效单元格！", True, False)
        elif selectedRow >= 2 and selectedRow < self.dataLen + 2:
            reply = getMessageBox('警告', '是否删除该行数据？', True, True)
            if reply == QMessageBox.Ok:
                goodsId = self.info[selectedRow]
                if deleteByDangerGoodsId(goodsId) == True:
                    self.tw_result.removeRow(selectedRow)
            else:
                return
        else:
            self.tw_result.removeRow(selectedRow)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = StrengthStatistics()
    widget.show()
    sys.exit(app.exec_())