import sys
from PyQt5.QtWidgets import *
from widgets.alocatMange.yearListForm import yearList_Form
from database.strengthDisturbSql import *
from PyQt5.Qt import Qt
from PyQt5.QtGui import QColor, QBrush
from database.alocatMangeSql import *


class DisturbPlan(QWidget, yearList_Form):
    def __init__(self, parent=None):
        super(DisturbPlan, self).__init__(parent)
        # Stren_Inquiry._initUnitTreeWidget()
        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}
        self.currentDisturbPlan = {}
        self.currentUnitDisturbPlanNum = {}
        self.unitDisturbPlanList = {}
        self.setupUi(self)
        self.signalConnect()
        self.signalDisconnectSlot()
        self.tw_first.header().setVisible(False)
        self.tw_second.header().setVisible(False)
        self.le_first.setDisabled(1)
        self.le_second.setDisabled(1)
        self.tw_first.setDisabled(1)
        self.tw_second.setDisabled(1)
        self._initYearWidget_()
        # initDisturbPlanDatabase()



    def signalConnect(self):
        # 点击选择年份后刷新页面 初始化
        self.lw_yearChoose.doubleClicked.connect(self.slotClickedInqury)
        # 点击第一目录结果
        self.tw_first.itemChanged.connect(self.slotDisturbStrengthResult)

        self.tw_second.itemChanged.connect(self.slotCheckedChange)

        # 点击第二目录结果
        self.tw_second.itemChanged.connect(self.slotDisturbStrengthResult)

        self.tb_add.clicked.connect(self.slotAddNewYear)
        # 修改分配数
        self.disturbResult.itemChanged.connect(self.slotItemChange)



    # 信号与槽连接的断开
    def signalDisconnectSlot(self):
        pass



    # 新增年份
    def slotAddNewYear(self):
        year = 0
        year, ok = QInputDialog.getInt(self, "Get year", "year:", 0, 0, 100000, 1)
        if year:
            insertIntoArmyTransferYear(year)
            self._initYearWidget_()



    # 初始化年份
    def _initYearWidget_(self):
        self.yearList = []
        self.currentYear = None
        self.lw_yearChoose.clear()
        # self.yearList = ['全部']
        allYear = selectYearListAboutArmy()
        for year in allYear:
            self.yearList.append(year)

        for year in self.yearList:
            item = QListWidgetItem()
            item.setText(year)
            self.lw_yearChoose.addItem(item)



    def slotClickedInqury(self):
        self.tw_first.clear()
        self.tw_second.clear()
        self.tw_first.header().setVisible(False)
        self.tw_second.header().setVisible(False)
        self.le_first.setDisabled(False)
        self.le_second.setDisabled(False)
        self.tw_first.setDisabled(False)
        self.tw_second.setDisabled(False)
        self.currentYear = self.lw_yearChoose.currentItem().text()
        self._initUnitTreeWidget("", self.tw_first)
        self._initEquipTreeWidget("", self.tw_second)



    def _initUnitTreeWidget(self, root, mother):
        if root == '':
            result = selectUnitInfoByDeptUper('')
        else:
            result = selectUnitInfoByDeptUper(root)

        # rowData: (单位编号，单位名称，上级单位编号)
        for rowData in result:
            item = QTreeWidgetItem(mother)
            item.setText(0, rowData[1])
            item.setCheckState(0, Qt.Unchecked)
            self.first_treeWidget_dict[rowData[0]] = item
            if rowData[0] != '':
                self._initUnitTreeWidget(rowData[0], item)
        # print("...", self.first_treeWidget_dict)



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



    '''
        查询结果
    '''
    def slotDisturbStrengthResult(self):
        self.yearList = []
        self.currentCheckedUnitChildNameList = []
        self.currentCheckedEquipList = []
        self.currentCheckedEquipNameList = []
        # 获取子单位名
        for unitID, unitItem in self.first_treeWidget_dict.items():
            if unitItem.checkState(0) == Qt.Checked:
                # print("len(findUnitChildName(unitID))",len(findUnitChildName(unitID)))
                if len(findUnitChildName(unitID)):
                    for i in findUnitChildName(unitID)[0]:
                        self.currentCheckedUnitChildNameList.append(i)
                else:
                    print("unitID", unitID)
                    self.currentCheckedUnitChildNameList.append(findUnitNameFromID(unitID)[0][0])
        # 获取当前装备名
        for equipID, equipItem in self.second_treeWidget_dict.items():
            if equipItem.checkState(0) == Qt.Checked:
                self.currentCheckedEquipList.append(equipID)
                self.currentCheckedEquipNameList.append(equipItem.text(0))
            elif equipItem.checkState(0) == Qt.PartiallyChecked:
                self.currentCheckedEquipList.append(equipID)
                self.currentCheckedEquipNameList.append(equipItem.text(0))
                # findChildEquip(equipID,self.currentCheckedEquipList,None)

        # 将装备列表、单位子列表、选中年份传入
        self._initDisturbPlanByUnitListAndEquipList(self.currentCheckedUnitChildNameList,
                                                    self.currentCheckedEquipList, self.currentYear)



    '''
        初始化分配计划结果
    '''
    def _initDisturbPlanByUnitListAndEquipList(self, UnitList, EquipList, YearList):
        self.disturbResult.clear()
        self.disturbResult.setRowCount(0)
        # 存放数据
        #disturbPlanList = selectDisturbPlan(UnitList, EquipList, YearList)

        headerlist = ['装备名称及规格型号', '单位', '军委分配计划数', '此次分配合计数']
        if len(self.currentCheckedUnitChildNameList):
            for i in self.currentCheckedUnitChildNameList:
                headerlist.append(i)
        headerlist.append('备注')
        self.disturbResult.setColumnCount(len(headerlist))
        self.disturbResult.setRowCount(len(self.currentCheckedEquipNameList))
        self.disturbResult.setHorizontalHeaderLabels(headerlist)
        self.currentDisturbPlan.clear()
        self.disturbResult.setColumnWidth(0, 200)
        print("self.currentCheckedEquipNameList", self.currentCheckedEquipNameList)
        i = 0
        for LineInfo in self.currentCheckedEquipNameList:
            item = QTableWidgetItem(LineInfo)
            self.disturbResult.setItem(i, 0, item)
            i = i + 1
            self.currentDisturbPlan[i] = LineInfo
        #self.disturbResult.setRowCount(n)
        self.initDisturbPlanNum()

    def initDisturbPlanNum(self):
        self.unitDisturbPlanList = selectDisturbPlanNum(self.currentCheckedUnitChildNameList,
                                                        self.currentCheckedEquipList, self.currentYear)
        #print("self.unitDisturbPlanList", self.unitDisturbPlanList)

        num=0
        for i in range(0,len(self.currentCheckedUnitChildNameList)):
            for j in range(0,len(self.currentCheckedEquipNameList)):

                if self.unitDisturbPlanList[num]!='-1':
                    item = QTableWidgetItem(self.unitDisturbPlanList[num])
                    self.disturbResult.setItem(j, 4 + i, item)
                elif self.unitDisturbPlanList[num]!='None':
                    item = QTableWidgetItem("")
                    self.disturbResult.setItem(j, 4 + i, item)
                else:
                    item = QTableWidgetItem("")
                    item.setFlags(Qt.NoItemFlags)
                    item.setBackground(QBrush(QColor(240,240,240)))
                    self.disturbResult.setItem(j, 4 + i, item)
                num=num+1

    '''
        功能：
            设置级目录联选中状态
    '''

    def slotCheckedChange(self, item, num):
        # 如果是顶部节点，只考虑Child：
        if item.childCount() and not item.parent():  # 判断是顶部节点，也就是根节点
            if item.checkState(num) == 0:  # 规定点击根节点只有两态切换，没有中间态
                for i in range(item.childCount()):  # 遍历子节点进行状态切换
                    item.child(i).setCheckState(num, 0)
            elif item.checkState(num) == 2:
                for i in range(item.childCount()):
                    item.child(i).setCheckState(num, 2)
        # 如果是底部节点，只考虑Parent
        if item.parent() and not item.childCount():
            parent_item = item.parent()  # 获得父节点
            brother_item_num = parent_item.childCount()  # 获得兄弟节点的数目，包括自身在内
            checked_num = 0  # 设置计数器
            for i in range(brother_item_num):  # 根据三态不同状态值进行数值累计
                checked_num += parent_item.child(i).checkState(num)
            if checked_num == 0:  # 最终结果进行比较，决定父节点的三态
                parent_item.setCheckState(num, 0)
            elif checked_num / 2 == brother_item_num:
                parent_item.setCheckState(num, 2)
            else:
                parent_item.setCheckState(num, 1)

            # 中间层需要全面考虑
        if item.parent() and item.childCount():
            if item.checkState(num) == 0:  # 规定点击根节点只有两态切换，没有中间态
                for i in range(item.childCount()):  # 遍历子节点进行状态切换
                    item.child(i).setCheckState(num, 0)
            elif item.checkState(num) == 2:
                for i in range(item.childCount()):
                    item.child(i).setCheckState(num, 2)
            parent_item = item.parent()  # 获得父节点
            brother_item_num = parent_item.childCount()  # 获得兄弟节点的数目，包括自身在内
            checked_num = 0  # 设置计数器
            for i in range(brother_item_num):  # 根据三态不同状态值进行数值累计
                checked_num += parent_item.child(i).checkState(num)
            if checked_num == 0:  # 最终结果进行比较，决定父节点的三态
                parent_item.setCheckState(num, 0)
            elif checked_num / 2 == brother_item_num:
                parent_item.setCheckState(num, 2)
            else:
                parent_item.setCheckState(num, 1)



    '''
        改变分配计划数
    '''
    def slotItemChange(self):
        currentRow = self.disturbResult.currentRow()
        currentColumn = self.disturbResult.currentColumn()
        #print("currentRow",currentRow,"currentColumn",currentColumn)
        currentRowInfo=self.currentCheckedEquipNameList[currentRow]
        currentColumnInfo=""
        if self.disturbResult.horizontalHeaderItem(currentColumn)!= None:
            currentColumnInfo=self.disturbResult.horizontalHeaderItem(currentColumn).text()
        print("currentRowInfo",currentRowInfo,"currentColumnInfo",currentColumnInfo)


        i = 0
        for a in self.unitDisturbPlanList:
            self.currentUnitDisturbPlanNum[i] = a
            i = i + 1
        if currentColumn == 4:
            for i, resultInfo in self.currentUnitDisturbPlanNum.items():
                if i == currentRow:
                    Unit_ID = resultInfo[2]
                    Equip_ID = resultInfo[0]
                    if self.disturbResult.item(currentRow, currentColumn).text() != resultInfo[4]:
                        reply = QMessageBox.question(self, '修改', '是否修改当前分配数？', QMessageBox.Yes,
                                                     QMessageBox.Cancel)
                        if reply == QMessageBox.Yes:
                            #
                            updateUnitDisturbPlanNum(Unit_ID, Equip_ID, self.currentYear,
                                                     self.disturbResult.item(currentRow,
                                                                             currentColumn).text(),
                                                     resultInfo[4])
                            self._initDisturbPlanByUnitListAndEquipList(self.unitList, self.equipList, self.year)
                        else:
                            self.disturbResult.item(currentRow, currentColumn).setText(resultInfo[4])
                    return
        else:
            for i, resultInfo in self.currentUnitDisturbPlanNum.items():
                if i == currentRow:
                    print("resultInfo", resultInfo)
                    self.disturbResult.item(currentRow, currentColumn).setText(resultInfo[currentColumn + 4])

    '''
        分配计划保存
    '''
