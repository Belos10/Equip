from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
from PyQt5.QtGui import QColor, QBrush, QFont
from PyQt5 import QtCore
from database.alocatMangeSql import *
from widgets.alocatMange.MultiyearComparisonForm import Widget_MultiyearComparison


class MultiyearComparison(QWidget, Widget_MultiyearComparison):
    def __init__(self, parent=None):
        super(MultiyearComparison, self).__init__(parent)
        self.setupUi(self)
        self.initAll()
        self.currentUnitChilddict = {}
        self.currentEquipdict = {}
        self.allEquipDict = {}
        self.yearList = []
        self.signalConnect()

    def initAll(self):
        self.lw_yearChoose.clear()
        self.disturbResult.clear()
        self.disturbResult.setRowCount(0)
        self.disturbResult.setColumnCount(0)
        self.initYearWidget()

    def signalConnect(self):
        self.lw_yearChoose.itemClicked.connect(self.getYearList)

    def getYearList(self):
        self.yearChooseList = []
        for i in range(self.lw_yearChoose.count()):
            if self.lw_yearChoose.item(i).checkState() == QtCore.Qt.Checked:
                self.yearChooseList.append(self.yearList[i])
        print(self.yearChooseList)
        self.initDisturbPlanByUnitListAndEquipList()

    # 设置装备 单位
    def setUnitAndEquip(self, currentUnitChilddict, currentEquipdict, currentRow, unitFlag):
        self.currentUnitChilddict = currentUnitChilddict
        # self.currentEquipdict = currentEquipdict
        self.equipRow = currentRow
        self.unitFlag = unitFlag
        self.allEquipDict = currentEquipdict
        self.currentEquipdict[0] = currentEquipdict[currentRow]
        print("currentUnitChilddict==", self.currentUnitChilddict)
        print("currentEquipdict==", self.currentEquipdict)

    # 初始化年份
    def initYearWidget(self):
        self.yearList = []
        # self.currentYear = None
        self.lw_yearChoose.clear()
        allYear = selectYearListAboutDisturbPlan()
        for year in allYear:
            self.yearList.append(year)

        for year in self.yearList:
            item = QListWidgetItem()
            item.setText(year)
            item.setCheckState(0)
            self.lw_yearChoose.addItem(item)

    # 显示界面
    def initDisturbPlanByUnitListAndEquipList(self):
        self.disturbResult.clear()
        self.disturbResult.setRowCount(0)
        self.lenCurrentUnitChilddict = len(self.currentUnitChilddict)
        self.lenCurrentEquipdict = len(self.currentEquipdict)
        # 选择机关或其他
        if self.unitFlag == 1:
            headerlist = ['年份', '装备名称及规格型号', '单位', '陆军调拨单开具数', '机关分配计划数', '此次分配合计数']
            if len(self.currentUnitChilddict):
                for i in self.currentUnitChilddict.values():
                    headerlist.append(i[1])
            headerlist.append('陆军调拨单进度')
            headerlist.append('接装条件')
            headerlist.append('火箭军调拨单进度')
            headerlist.append('完成接装')
            headerlist.append('备注')
            self.lenHeaderList = len(headerlist)
            self.disturbResult.setColumnCount(self.lenHeaderList)
            self.disturbResult.setRowCount(len(self.yearChooseList))
            self.disturbResult.setHorizontalHeaderLabels(headerlist)
            # self.currentDisturbPlan.clear()
            self.disturbResult.setColumnWidth(1, 200)
            i = 0
            for LineInfo in self.yearChooseList:
                currentRowResult = []
                item = QTableWidgetItem(LineInfo)
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                currentRowResult.append(item)
                self.disturbResult.setItem(i, 0, item)
                item = QTableWidgetItem(self.currentEquipdict[0][1])
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                currentRowResult.append(item)
                self.disturbResult.setItem(i, 1, item)
                item = QTableWidgetItem("")
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                currentRowResult.append(item)
                self.disturbResult.setItem(i, 2, item)
                item = QTableWidgetItem("")
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                currentRowResult.append(item)
                self.disturbResult.setItem(i, 3, item)
                item = QTableWidgetItem("")
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                currentRowResult.append(item)
                self.disturbResult.setItem(i, 4, item)
                item = QTableWidgetItem("")
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                currentRowResult.append(item)
                self.disturbResult.setItem(i, 5, item)
                for x in range(0, self.lenCurrentUnitChilddict):
                    item = QTableWidgetItem("")
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    flag = selectIfUnitScheduleFinish(self.currentUnitChilddict[x][0],
                                                      self.currentEquipdict[0][0],
                                                      LineInfo)
                    if flag[0][0] == 'TRUE':
                        item.setForeground(QBrush(QColor(87, 102, 144)))
                    else:
                        item.setForeground(QBrush(QColor(219, 125, 116)))
                    self.disturbResult.setItem(i, x + 6, item)
                    currentRowResult.append(item)
                item = QTableWidgetItem("")
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.disturbResult.setItem(i, 10 + self.lenCurrentUnitChilddict, item)
                currentRowResult.append(item)
                i = i + 1
        # 选择各基地
        elif self.unitFlag == 2:
            headerlist = ['年份', '装备名称及规格型号', '单位', '火箭军调拨单开具数', '机关分配计划数', '此次分配合计数']
            if len(self.currentUnitChilddict):
                for i in self.currentUnitChilddict.values():
                    headerlist.append(i[1])
            # headerlist.append('陆军调拨单进度')
            headerlist.append('火箭军调拨单进度')
            headerlist.append('接装条件')
            headerlist.append('完成接装')
            headerlist.append('备注')
            self.lenHeaderList = len(headerlist)
            self.disturbResult.setColumnCount(self.lenHeaderList)
            self.disturbResult.setRowCount(len(self.yearChooseList))
            self.disturbResult.setHorizontalHeaderLabels(headerlist)
            self.disturbResult.setColumnWidth(1, 200)
            i = 0
            for LineInfo in self.yearChooseList:
                currentRowResult = []
                item = QTableWidgetItem(LineInfo)
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                currentRowResult.append(item)
                self.disturbResult.setItem(i, 0, item)
                item = QTableWidgetItem(self.currentEquipdict[0][1])
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                currentRowResult.append(item)
                self.disturbResult.setItem(i, 1, item)
                item = QTableWidgetItem("")
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                currentRowResult.append(item)
                self.disturbResult.setItem(i, 2, item)
                item = QTableWidgetItem("")
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                currentRowResult.append(item)
                self.disturbResult.setItem(i, 3, item)
                item = QTableWidgetItem("")
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                currentRowResult.append(item)
                self.disturbResult.setItem(i, 4, item)
                item = QTableWidgetItem("")
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                currentRowResult.append(item)
                self.disturbResult.setItem(i, 5, item)
                for x in range(0, self.lenCurrentUnitChilddict):
                    item = QTableWidgetItem("")
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    flag = selectIfUnitScheduleFinish(self.currentUnitChilddict[x][0],
                                                      self.currentEquipdict[0][0],
                                                      self.currentYear)
                    if flag[0][0] == 'TRUE':
                        item.setForeground(QBrush(QColor(87, 102, 144)))
                    else:
                        item.setForeground(QBrush(QColor(219, 125, 116)))
                    self.disturbResult.setItem(i, x + 6, item)
                    currentRowResult.append(item)
                item = QTableWidgetItem("")
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.disturbResult.setItem(i, 9 + self.lenCurrentUnitChilddict, item)
                currentRowResult.append(item)
                i = i + 1
        self.disturbResult.setColumnWidth(2, 150)
        if self.currentUnitChilddict and self.currentEquipdict:
            self.initDisturbPlanNum()
            self.initDisturbPlanNote()
            self.initDisturbPlanInputNum()
            self.initDisturbPlanOther()
            self.ifEquipHaveChild()


    # 读取初始分配计划数
    def initDisturbPlanNum(self):
        j = 0
        for year in self.yearChooseList:
            unitDisturbPlanList = selectDisturbPlanNumByList(self.currentUnitChilddict,
                                                             self.currentEquipdict, year)
            # 显示每个单位分配计划数
            num = 0
            for i in range(0, len(self.currentUnitChilddict)):
                item = self.disturbResult.item(j, 6 + i)
                if unitDisturbPlanList[num] != '-1':
                    item.setText(unitDisturbPlanList[num])
                num = num + 1
            j = j + 1
        self.initDisturbPlanSum()


    # 初始化此次分配合计数
    def initDisturbPlanSum(self):
        # 显示此次分配计划数
        for i in range(len(self.yearChooseList)):
            sum = 0
            # if not selectEquipIsHaveChild(self.currentEquipdict[0][0]):
            for j in range(0, len(self.currentUnitChilddict)):
                num = self.disturbResult.item(i, 6 + j).text()
                if num == '':
                    sum = sum + 0
                else:
                    sum = sum + int(num)
            self.disturbResult.item(i, 5).setText(str(sum))



    # 读取初始分配计划备注
    def initDisturbPlanNote(self):
        for i in range(len(self.yearChooseList)):
            unitDisturbPlanNoteList = selectDisturbPlanNote(self.currentEquipdict, self.yearChooseList[i])
            # print("self.unitDisturbPlanNoteList", unitDisturbPlanNoteList)
            item = self.disturbResult.item(i, self.lenHeaderList - 1)
            if unitDisturbPlanNoteList[0] is not None:
                item.setText(str(unitDisturbPlanNoteList[0]))


    # 初始化自定义计划数
    def initDisturbPlanInputNum(self):
        for i in range(len(self.yearChooseList)):
            if self.unitFlag == 1:
                unitDisturbPlanInputNumList = selectDisturbPlanInputNumUpmost(self.currentEquipdict, self.yearChooseList[i])
                item = self.disturbResult.item(i, 4)
                if unitDisturbPlanInputNumList[0] is not None:
                    item.setText(str(unitDisturbPlanInputNumList[0]))
            elif self.unitFlag == 2:
                unitDisturbPlanInputNumList = selectDisturbPlanInputNumBase(self.currentEquipdict, self.yearChooseList[i])
                item = self.disturbResult.item(i, 4)
                if unitDisturbPlanInputNumList[0] is not None:
                    item.setText(str(unitDisturbPlanInputNumList[0]))


    # 初始化机关单位数与装备单位
    def initDisturbPlanOther(self):
        for i in range(len(self.yearChooseList)):
        # 装备单位
            item = self.disturbResult.item(i, 2)
            item.setText(str(self.currentEquipdict[0][5]))
            equipId = self.currentEquipdict[0][0]
            year = self.yearChooseList[i]
            if self.unitFlag == 1:
                if not selectEquipIsHaveChild(equipId):
                    unitDisturbPlanOtherList = selectDisturbPlanOther_single(equipId, year)
                    item = self.disturbResult.item(i, 3)
                    if unitDisturbPlanOtherList[0]:
                        item.setText(str(unitDisturbPlanOtherList[0][0][1]))
                    else:
                        item.setText("")
                else:
                    item = self.disturbResult.item(i, 3)
                    item.setText(str(self.findAllKidsArmySum(equipId, year)))
            elif self.unitFlag == 2:
                item = self.disturbResult.item(i, 3)
                result = selectDisturbPlanNumByList({0: [self.currentUnitChilddict[0]]}, equipId, year)
                if result:
                    item.setText(str(result[i]))
                else:
                    item.setText("")
                # for row in reversed(range(len(self.currentEquipdict))):
                #     sum = 0
                #     for childRow in reversed(range(len(self.currentEquipdict))):
                #         # 第0个字段是EquipID,第二个字段是Equip_Uper
                #         if self.currentEquipdict[row][0] == self.currentEquipdict[childRow][2]:
                #             num = self.disturbResult.item(childRow, 3).text()
                #             if num != '':
                #                 sum = sum + int(num)
                #     if sum != 0:
                #         self.disturbResult.item(row, 3).setText(str(sum))

    # 某装备的所有陆军调拨单值(子项)
    def findAllKidsArmySum(self, equipId, year):
        if not selectEquipIsHaveChild(equipId):
            unitDisturbPlanOtherList = selectDisturbPlanOther_single(equipId, year)
            if unitDisturbPlanOtherList[0]:
                return int(unitDisturbPlanOtherList[0][0][1])
            else:
                return 0
        else:
            sum = 0
            childEquipList = []
            findChildEquipIDList(equipId, childEquipList)
            for i in range(len(childEquipList)):
                if i == 0:
                    continue
                id = childEquipList[i]
                if not selectEquipIsHaveChild(id):
                    unitDisturbPlanOtherList = selectDisturbPlanOther_single(id, year)
                    if unitDisturbPlanOtherList[0]:
                        sum += int(unitDisturbPlanOtherList[0][0][1])
                else:
                    sum += self.findAllKidsArmySum(id, year)
            return sum


    # 各进度
    def ifEquipHaveChild(self):
        # 选择机关或其他
        if self.unitFlag == 1:
            for i in range(len(self.yearChooseList)):
                if not selectEquipIsHaveChild(self.currentEquipdict[0][0]):
                    item1 = QTableWidgetItem("")
                    # 陆军调拨单进度
                    flag1 = selectArmySchedule(self.currentEquipdict[0][0], self.yearChooseList[i])
                    if flag1[0][0] != '0':
                        item1.setText(str(flag1[0][0]))
                    else:
                        item1.setText("未完成")
                    self.disturbResult.setItem(i, 6 + self.lenCurrentUnitChilddict, item1)

                    item2 = QTableWidgetItem("")
                    # 是否具备接装条件
                    flag2 = selectAllotConditionUper(self.currentEquipdict[0][0], self.yearChooseList[i])
                    if int(flag2[0][0]):
                        item2.setText("已完成")
                    else:
                        item2.setText("未完成")
                    self.disturbResult.setItem(i, 7 + self.lenCurrentUnitChilddict, item2)

                    item3 = QTableWidgetItem("")
                    # 火箭军调拨单进度
                    flag3 = selectRocketScheduleUper(self.currentEquipdict[0][0], self.yearChooseList[i])
                    if int(flag3[0][0]):
                        item3.setText("已完成")
                    else:
                        item3.setText("未完成")
                    self.disturbResult.setItem(i, 8 + self.lenCurrentUnitChilddict, item3)

                    item4 = QTableWidgetItem("")
                    # 是否完成接装
                    flag4 = selectIfScheduleFinishUper(self.currentEquipdict[0][0], self.yearChooseList[i])
                    if flag4[0][0] != '0':
                        item4.setText("已完成")
                    else:
                        item4.setText("未完成")
                    self.disturbResult.setItem(i, 9 + self.lenCurrentUnitChilddict, item4)
        # 选择基地
        elif self.unitFlag == 2:
            for i in self.yearChooseList:
                if not selectEquipIsHaveChild(self.currentEquipdict[0][0]):
                    item2 = QTableWidgetItem("")
                    # 火箭军调拨单进度
                    flag2 = selectRocketScheduleBase(self.currentEquipdict[0][0], self.yearChooseList[i])
                    if int(flag2[0][0]):
                        item2.setText("已完成")
                    else:
                        item2.setText("未完成")
                    self.disturbResult.setItem(i, 6 + self.lenCurrentUnitChilddict, item2)

                    item3 = QTableWidgetItem("")
                    # 是否具备接装条件
                    flag3 = selectAllotConditionBase(self.currentEquipdict[0][0], self.yearChooseList[i])
                    if int(flag3[0][0]):
                        item3.setText("已完成")
                    else:
                        item3.setText("未完成")
                    self.disturbResult.setItem(i, 7 + self.lenCurrentUnitChilddict, item3)


                    item4 = QTableWidgetItem("")
                    # 是否完成接装
                    flag4 = selectIfScheduleFinishBase(self.currentEquipdict[0][0], self.yearChooseList[i])
                    if flag4[0][0] != '0':
                        item4.setText("已完成")
                    else:
                        item4.setText("未完成")
                    self.disturbResult.setItem(i, 8 + self.lenCurrentUnitChilddict, item4)
