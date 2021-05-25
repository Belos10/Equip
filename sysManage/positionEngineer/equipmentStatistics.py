from PyQt5.QtCore import Qt

from database.danderGoodsSql import getBrigadesByBaseId, getpositionsByPositionId, getUnit
from database.positionEngneerSql import *
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidget, QHeaderView, QTableWidgetItem, QComboBox, \
    QMessageBox, QTreeWidgetItem
from widgets.positionEngineer.posEngneerStatisticsUI import PosEngneerStatisticsUI
from sysManage.userInfo import get_value


class EquipmentStatistics(QWidget, PosEngneerStatisticsUI):
    def __init__(self, parent=None):
        super(EquipmentStatistics, self).__init__(parent)
        self.setupUi(self)
        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}
        # 当前选中的单位列表和装备列表
        self.currentCheckedUnitList = []
        self.currentCheckedEquipList = []
        self.countOfPosition = 0
        self.rowAndCountIndex = {}
        self.startInfo = None
        self.userInfo = None
        self.info = {}
        self.signalConnectSlot()
        self.initEquipmentStatistics()


    # 信号与槽的连接
    def signalConnectSlot(self):
        # 当前单位目录被点击
        self.tw_first.itemChanged.connect(self.slotEquipmentStatisticsResult)
        # 当前装备目录被点击
        self.tw_second.itemChanged.connect(self.slotEquipmentStatisticsResult)

        # #新增某个年份
        # self.tb_add.clicked.connect(self.slotAdd)

        # self.tb_delete.clicked.connect(self.slotDelete)
        self.pb_firstSelect.clicked.connect(self.slotSelectUnit)
        self.pb_secondSelect.clicked.connect(self.slotSelectEquip)
        self.tb_output.clicked.connect(self.slotInput)
        self.tb_output.clicked.connect(self.slotOutput)
        self.tw_result.itemChanged.connect(self.slotAlterAndSava)

    # 信号和槽断开
    def slotDisconnect(self):
        pass

    def initUserInfo(self):
        self.userInfo = get_value("totleUserInfo")
    # 定义初始化函数
    def initEquipmentStatistics(self):
        self.initUserInfo()
        self.tw_first.clear()
        self.tw_second.clear()
        self.tw_first.header().setVisible(False)
        self.tw_second.header().setVisible(False)
        self.le_first.setDisabled(False)
        self.le_second.setDisabled(False)
        self.tw_first.setDisabled(False)
        self.tw_first.setVisible(True)
        self.pb_firstSelect.setVisible(False)
        self.pb_firstSelect.setDisabled(False)
        self.le_first.setVisible(False)
        self.le_second.setVisible(False)
        self.tb_add.setDisabled(True)
        self.tb_add.setVisible(False)
        self.tb_delete.setDisabled(True)
        self.tb_delete.setVisible(False)



        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}
        # 当前选中的单位列表和装备列表
        self.currentCheckedUnitList = []
        self.currentCheckedEquipList = []

        if self.userInfo:
            from database.strengthDisturbSql import selectUnitInfoByUnitID
            self.startInfo = selectUnitInfoByUnitID(self.userInfo[0][4])

        stack = []
        root = []
        if self.startInfo:
            stack.append(self.startInfo)
            root.append(self.tw_first)
            self._initUnitTreeWidget(stack, root)

        equipInfo = None
        equipInfo = selectEquipInfoByEquipUper("")
        stack = []
        root = []
        if equipInfo:
            stack.append(equipInfo[0])
            root.append(self.tw_second)
            self._initEquipTreeWidget(stack, root)

        pass

    def slotSelectUnit(self):
        findText = self.le_first.text()
        for i, item in self.first_treeWidget_dict.items():
            if item.text(0) == findText:
                self.tw_first.setCurrentItem(item)
                break

    def slotSelectEquip(self):
        findText = self.le_second.text()
        for i, item in self.second_treeWidget_dict.items():
            if item.text(0) == findText:
                self.tw_second.setCurrentItem(item)
                break

    '''
        功能：
            点击查询按钮时，设置当前可选项和不可选项，并初始化装备和单位目录
    '''

    def slotClickedInqury(self):
        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}
        self.tw_first.clear()
        self.tw_second.clear()
        self.tw_first.header().setVisible(False)
        self.tw_second.header().setVisible(False)
        self.le_first.setDisabled(False)
        self.le_second.setDisabled(False)
        self.tw_first.setDisabled(False)
        self.tw_second.setDisabled(False)
        self.inquiry_result.setDisabled(False)


        self.startName = selectUnitNameByUnitID(self.userInfo[0][4])
        item = QTreeWidgetItem(self.tw_first)
        item.setText(0, self.startName)
        item.setCheckState(0, Qt.Unchecked)
        self.first_treeWidget_dict[self.userInfo[0][4]] = item
        self._initUnitTreeWidget(self.userInfo[0][4], item)
        self._initEquipTreeWidget("", self.tw_second)

    def slotSelectUnit(self):
        findText = self.le_first.text()
        for i, item in self.first_treeWidget_dict.items():
            if item.text(0) == findText:
                self.tw_first.setCurrentItem(item)
                break

    def slotSelectEquip(self):
        findText = self.le_second.text()
        for i, item in self.second_treeWidget_dict.items():
            if item.text(0) == findText:
                self.tw_second.setCurrentItem(item)
                break

    '''
        功能：
            查询实力结果
    '''

    def slotEquipmentStatisticsResult(self):
        self.currentCheckedUnitList = []
        self.currentCheckedEquipList = []
        for equipID, equipItem in self.second_treeWidget_dict.items():
            if equipItem.checkState(0) == Qt.Checked:
                self.currentCheckedEquipList.append(equipID)

        for unitID, unitItem in self.first_treeWidget_dict.items():
            if unitItem == self.tw_first.currentItem():
                self.currentCheckedUnitList.append(unitID)
        if len(self.currentCheckedUnitList) == 1 and len(self.currentCheckedEquipList) > 0:
            if gradeInUnit(self.currentCheckedUnitList[0]) == 3:
                lastEquiplist = []
                for item in self.currentCheckedEquipList:
                    if isLastLevelEquipment(item) == True:
                        lastEquiplist.append(item)
                if len(lastEquiplist) > 0:
                    print(self.currentCheckedUnitList, lastEquiplist)
                    self._initTableWidgetByUnitListAndEquipList(self.currentCheckedUnitList, lastEquiplist)

    '''
        功能：
            根据单位目录和装备目录初始化结果表格
    '''

    def _initTableWidgetByUnitListAndEquipList(self, unitList, equipList):
        self.info = {}
        brigades = []
        brigade = {}
        positions = []
        position = {}
        positionCount = 0
        self.base = {}
        self.tw_result.clear()
        self.base['Unit_ID'] =  unitList[0]
        self.base['Unit_Name'] = getUnit(self.base['Unit_ID'])['Unit_Name']
        brigadeIds = getBrigadesByBaseId(self.base['Unit_ID'])
        if len(brigadeIds) < 1:
            return
        for item in brigadeIds:
            brigade['Unit_ID'] = item['Unit_ID']
            brigade['Unit_Name'] = item['Unit_Name']
            positionIds = getpositionsByPositionId(brigade['Unit_ID'])
            positions = []
            for element in positionIds:
                position['Unit_ID'] = element['Unit_ID']
                position['Unit_Name'] = element['Unit_Name']
                positionCount = positionCount + 1
                positions.append(position.copy())
            brigade['Positions'] = positions.copy()
            brigades.append(brigade.copy())
        self.base['brigades'] = brigades

        # 画表头
        self.rowCount = len(equipList) + 4
        self.columnCount = 4 + 2 * positionCount
        self.tw_result.setRowCount(self.rowCount)
        self.tw_result.setColumnCount(self.columnCount)
        self.tw_result.verticalHeader().setVisible(False)
        self.tw_result.horizontalHeader().setVisible(False)
        # self.tw_result.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tw_result.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tw_result.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tw_result.resizeColumnsToContents()
        self.tw_result.resizeRowsToContents()
        item = QTableWidgetItem("%s阵地工程X生化防护装备统计表" % self.base['Unit_Name'])
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(0, 0, item)
        self.tw_result.setSpan(0, 0, 1, self.columnCount)
        item = QTableWidgetItem("序号")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 0, item)
        self.tw_result.setSpan(1, 0, 3, 1)
        item = QTableWidgetItem("名称")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 1, item)
        self.tw_result.setSpan(1, 1, 3, 1)
        item = QTableWidgetItem("单位")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 2, item)
        self.tw_result.setSpan(1, 2, 3, 1)
        item = QTableWidgetItem("合计")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 3, item)
        self.tw_result.setSpan(1, 3, 3, 1)

        for i in range(len(equipList)):
            item = QTableWidgetItem(str(i))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(4 + i, 0, item)

            item = QTableWidgetItem("%s"%getEquipmentNameById(equipList[i]))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(4 + i, 1, item)

            item = QTableWidgetItem("%s" % getEquipmentTypeById(equipList[i]))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(4 + i, 2, item)

            if self.columnCount > 4:
                brigadeStartColumn = 4
                positionStartColum = 4
                currentRow = 4 + i
                currentColumn = 4
                for aBrigade in self.base['brigades']:
                    item = QTableWidgetItem("%s"%aBrigade['Unit_Name'])
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tw_result.setItem(1, brigadeStartColumn, item)
                    self.tw_result.setSpan(1, brigadeStartColumn, 1, 2 * len(aBrigade['Positions']))
                    for aPosition in aBrigade['Positions']:
                        item = QTableWidgetItem("%s" % aPosition['Unit_Name'])
                        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                        self.tw_result.setItem(2, positionStartColum, item)
                        self.tw_result.setSpan(2, positionStartColum, 1, 2 )

                        item = QTableWidgetItem("数量")
                        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                        self.tw_result.setItem(3, positionStartColum, item)

                        item = QTableWidgetItem("运行状态")
                        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                        self.tw_result.setItem(3, positionStartColum + 1, item)
                       # info['%d,%d'%(currentRow,currentColumn)] = aPosition['Unit_ID']
                        data = getStatictsResult(aPosition['Unit_ID'],equipList[i])
                        if len(data) > 0:
                            item = QTableWidgetItem("%d"%data[3])
                            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                            self.tw_result.setItem(currentRow, positionStartColum, item)

                            item = QTableWidgetItem("%s" % data[4])
                            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                            self.tw_result.setItem(currentRow, positionStartColum + 1, item)
                            self.info['%d,%d' % (currentRow, currentColumn)] = data[0]
                            self.info['%d,%d' % (currentRow, currentColumn + 1)] = data[0]
                        else:
                            self.info['%d,%d' % (currentRow, currentColumn)] = [equipList[i],aPosition['Unit_ID']]
                            self.info['%d,%d' % (currentRow, currentColumn + 1)] = [equipList[i],aPosition['Unit_ID']]
                        positionStartColum = positionStartColum + 2
                        currentColumn = positionStartColum
                    brigadeStartColumn = positionStartColum
        #设置前三行为不可编辑
        for i in range(3):
            for j in range(self.columnCount):
                item = self.tw_result.item(i,j)
                if item != None:
                    item.setFlags(Qt.ItemIsEnabled)


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
            初始化装备目录
    '''

    def _initEquipTreeWidget(self, stack, root):
        while stack:
            EquipInfo = stack.pop(0)
            item = QTreeWidgetItem(root.pop(0))
            item.setText(0, EquipInfo[1])
            item.setCheckState(0, Qt.Unchecked)
            self.second_treeWidget_dict[EquipInfo[0]] = item
            result = selectEquipInfoByEquipUper(EquipInfo[0])
            for resultInfo in result:
                stack.append(resultInfo)
                root.append(item)

    def slotAlterAndSava(self):
        currentRow = self.tw_result.currentRow()
        currentColumn = self.tw_result.currentColumn()
        if currentRow > 3 and currentColumn > 3:
            index = self.info.get('%s,%s'%(currentRow,currentColumn))
            if type(index) == int:
                if currentColumn % 2 == 0:
                    itemData = self.tw_result.item(currentRow,currentColumn)
                    if itemData != None:
                        text1 = itemData.text()
                    else:
                        text1 = ''
                    itemData = self.tw_result.item(currentRow, currentColumn + 1)
                    if itemData != None:
                        text2 = itemData.text()
                    else:
                        text2 = ''
                    if len(text1) > 0 and len(text2) > 0:
                        count = int(text1)
                        status = text2
                        if alterData(index,count,status) == True:
                            QMessageBox.warning(self, "注意", "修改成功！", QMessageBox.Yes, QMessageBox.Yes)
                    elif len(text1) == 0 and len(text2) == 0:
                       if deleteData(index) == True:
                           QMessageBox.warning(self, "注意", "清除成功！", QMessageBox.Yes, QMessageBox.Yes)
                else:
                    itemData = self.tw_result.item(currentRow, currentColumn - 1)
                    if itemData != None:
                        text1 = itemData.text()
                    else:
                        text1 = ''
                    itemData = self.tw_result.item(currentRow, currentColumn)
                    if itemData != None:
                        text2 = itemData.text()
                    else:
                        text2 = ''
                    if len(text1) > 0 and len(text2) > 0:
                        count = int(text1)
                        status = text2
                        if alterData(index,count,status) == True:
                            QMessageBox.warning(self, "注意", "修改成功！", QMessageBox.Yes, QMessageBox.Yes)
                    elif len(text1) == 0 and len(text2) == 0:
                       if deleteData(index) == True:
                           QMessageBox.warning(self, "注意", "清除成功！", QMessageBox.Yes, QMessageBox.Yes)
            elif type(index) == list:
                if currentColumn % 2 == 0:
                    itemData = self.tw_result.item(currentRow, currentColumn)
                    if itemData != None:
                        text1 = itemData.text()
                    else:
                        text1 = ''
                    itemData = self.tw_result.item(currentRow, currentColumn + 1)
                    if itemData != None:
                        text2 = itemData.text()
                    else:
                        text2 = ''
                    if len(text1) > 0 and len(text2) > 0:
                        count = int(text1)
                        status = text2
                        if insertData(index[0],index[1],count,status) == True:
                            QMessageBox.warning(self, "注意", "增加成功！", QMessageBox.Yes, QMessageBox.Yes)
                else:
                    itemData = self.tw_result.item(currentRow, currentColumn - 1)
                    if itemData != None:
                        text1 = itemData.text()
                    else:
                        text1 = ''
                    itemData = self.tw_result.item(currentRow, currentColumn)
                    if itemData != None:
                        text2 = itemData.text()
                    else:
                        text2 = ''
                    if len(text1) > 0 and len(text2) > 0:
                        count = int(text1)
                        status = text2
                        if insertData(index[0], index[1], count, status) == True:
                            QMessageBox.warning(self, "注意", "增加成功！", QMessageBox.Yes, QMessageBox.Yes)
            self.slotEquipmentStatisticsResult()











    def slotInput(self):
        pass

    def slotOutput(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = EquipmentStatistics()
    widget.show()
    sys.exit(app.exec_())
