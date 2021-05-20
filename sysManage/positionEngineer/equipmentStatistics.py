from PyQt5.QtCore import Qt
from database.positionEngneerSql import *
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidget, QHeaderView, QTableWidgetItem, QComboBox, \
    QMessageBox, QTreeWidgetItem

from widgets.positionEngineer.posEngneerStatisticsUI import PosEngneerStatisticsUI


class EquipmentStatistics(QWidget, PosEngneerStatisticsUI):
    def __init__(self, parent=None):
        super(EquipmentStatistics, self).__init__(parent)
        self.setupUi(self)
        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}
        # 当前选中的单位列表和装备列表
        self.currentCheckedUnitList = []
        self.currentCheckedEquipList = []
        self.countOfPosition= 0
        self.rowAndCountIndex = {}
        self.signalConnectSlot()
        self._initEquipmentStatistics()


    # 信号与槽的连接
    def signalConnectSlot(self):
        # 当前单位目录被点击
        self.tw_first.itemChanged.connect(self.slotEquipmentStatisticsResult)
        # 当前装备目录被点击
        self.tw_second.itemChanged.connect(self.slotEquipmentStatisticsResult)

        # 新增某个年份
        self.tb_add.clicked.connect(self.slotAdd)

        self.tb_delete.clicked.connect(self.slotDelete)

        self.pb_firstSelect.clicked.connect(self.slotSelectUnit)

        self.pb_secondSelect.clicked.connect(self.slotSelectEquip)
        self.tb_output.clicked.connect(self.slotInput)
        self.tb_output.clicked.connect(self.slotOutput)


    #信号和槽断开
    def slotDisconnect(self):
        pass

    #定义初始化函数
    def _initEquipmentStatistics(self):
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
        # self.tw_second.setDisabled(False)
        # self.tw_second.setVisible(True)
        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}
        # 当前选中的单位列表和装备列表
        self.currentCheckedUnitList = []
        self.currentCheckedEquipList = []
        self._initUnitTreeWidget('', self.tw_first)
        self._initEquipTreeWidget('', self.tw_second)
        pass




    def initUserInfo(self, userInfo):
        self.userInfo = userInfo
        self._initEquipmentStatistics()


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
        #        self.tb_inqury.setDisabled(True)
        #        self.tb_rechoose.setDisabled(False)

        self.currentYear = self.lw_chooseYear.currentItem().text()
        print("currentYear :", self.currentYear)

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

        self._initTableWidgetByUnitListAndEquipList(self.currentCheckedUnitList,self.currentCheckedEquipList)

    '''
        功能：
            根据单位目录和装备目录初始化结果表格
    '''
    def _initTableWidgetByUnitListAndEquipList(self,unitList,equipList):
        info = []
        self.tw_result.clear()



        if len(unitList) > 0 and len(equipList) > 0:
            baseId = findBase(unitList[0]) #基地
            if baseId != None:
                brigades = findChildUnit(baseId) # 旅团
                if brigades != None:

                    lastEquipments = []

                    countOfPositions = 0
                    countOFEquipment = 0
                    for brigade in brigades:
                        temp = {}
                        positions = findChildUnit(brigade)
                        if positions != None :
                            countOfPositions = countOfPositions + len(positions)
                            temp[brigade] = positions
                            info.append(temp.copy())

                    for equip in equipList:
                        if isLastLevelEquipment(equip) == True:
                            lastEquipments.append(equip)
                    countOFEquipment = len(lastEquipments)

                    #画表头
                    self.tw_result.verticalHeader().setVisible(False)
                    self.tw_result.horizontalHeader().setVisible(False)
                    # self.tw_result.setEditTriggers(QTableWidget.NoEditTriggers)
                    self.tw_result.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
                    self.tw_result.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                    self.tw_result.resizeColumnsToContents()
                    self.tw_result.resizeRowsToContents()
                    rowCount = countOFEquipment + 4
                    columnCount = 2 * countOfPositions + 4
                    self.tw_result.setRowCount(rowCount)
                    self.tw_result.setColumnCount(columnCount)

                    item = QTableWidgetItem('%s阵地工程X生化防护装备统计表'%getUnitNameById(baseId))
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tw_result.setItem(0, 0, item)
                    self.tw_result.setSpan(0, 0, 1, columnCount)

                    item = QTableWidgetItem('序号')
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tw_result.setItem(1, 0, item)
                    self.tw_result.setSpan(1, 0, 3, 1)

                    item = QTableWidgetItem('名称')
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tw_result.setItem(1, 1, item)
                    self.tw_result.setSpan(1, 1, 3, 1)

                    item = QTableWidgetItem('单位')
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tw_result.setItem(1, 2, item)
                    self.tw_result.setSpan(1, 2, 3, 1)

                    item = QTableWidgetItem('合计')
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tw_result.setItem(1, 3, item)
                    self.tw_result.setSpan(1, 3, 3, 1)

                    fisrtPositionIndex = 4
                    for i in range(len(info)):
                        brigades = list(info[i].keys())  #旅团列表
                        for brigade in brigades:
                            brigadeSubPositions = info[i].get(brigade)
                            item = QTableWidgetItem(getUnitNameById(brigade))
                            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                            self.tw_result.setItem(1, fisrtPositionIndex, item)
                            self.tw_result.setSpan(1, fisrtPositionIndex, 1, 2 * len(brigadeSubPositions) )
                            for j in range(len(lastEquipments)):
                                rowIndex = 4 + j

                                item = QTableWidgetItem(str(j))
                                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                                self.tw_result.setItem(rowIndex, 0, item)

                                item = QTableWidgetItem(getEquipmentNameById(lastEquipments[j]))
                                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                                self.tw_result.setItem(rowIndex, 1, item)


                                unit = getEquipmentUnitName(lastEquipments[j])
                                if unit != None:
                                    item = QTableWidgetItem(getEquipmentNameById(lastEquipments[j]))
                                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                                    self.tw_result.setItem(rowIndex , 2, item)



                                for subPosition in brigadeSubPositions:
                                    item = QTableWidgetItem(getUnitNameById(subPosition))
                                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                                    self.tw_result.setItem(2, fisrtPositionIndex, item)
                                    self.tw_result.setSpan(2, fisrtPositionIndex, 1, 2)

                                    item = QTableWidgetItem('数量')
                                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                                    self.tw_result.setItem(3, fisrtPositionIndex, item)

                                    item = QTableWidgetItem('运行状态')
                                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                                    self.tw_result.setItem(3, fisrtPositionIndex + 1, item)
                                    result = getEquipmentStatisticsResultByUnitAndEquip(subPosition,lastEquipments[j])
                                    if result != None:
                                        item = QTableWidgetItem(str(result[0]))
                                        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                                        self.tw_result.setItem(rowIndex, fisrtPositionIndex, item)
                                        item = QTableWidgetItem(result[1])
                                        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                                        self.tw_result.setItem(rowIndex, fisrtPositionIndex + 1, item)
                                    fisrtPositionIndex = fisrtPositionIndex + 2
                                fisrtPositionIndex = 4


                else:
                    pass





        pass






    '''
        初始化单位目录
    '''
    def _initUnitTreeWidget(self, root, mother):
        if root == '':
            result = selectUnitInfoByDeptUper('')
        else:
            result = selectUnitInfoByDeptUper(root)

        # rowData: (单位编号，单位名称，上级单位编号)
        for rowData in result:
            item = QTreeWidgetItem(mother)
            item.setText(0, rowData[1])
            self.first_treeWidget_dict[rowData[0]] = item
            if rowData[0] != '':
                self._initUnitTreeWidget(rowData[0], item)

    '''
        功能：
            初始化装备目录
    '''

    def _initEquipTreeWidget(self, root, mother):
        if root == '':
            result = selectEquipInfoByEquipUper('')
        else:
            result = selectEquipInfoByEquipUper(root)

        # rowData: (装备编号，装备名称，上级装备编号, 录入类型, 装备类型)
        for rowData in result:
            item = QTreeWidgetItem(mother)
            item.setText(0, rowData[1])
            item.setCheckState(0, Qt.Unchecked)
            self.second_treeWidget_dict[rowData[0]] = item
            if rowData[0] != '':
                self._initEquipTreeWidget(rowData[0], item)


    def slotAdd(self):
        pass
    def slotDelete(self):
        pass

    def slotInput(self):
        pass
    def slotOutput(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = EquipmentStatistics()
    widget.show()
    sys.exit(app.exec_())