import sys
from PyQt5.QtWidgets import *
#new
from database.SD_EquipmentBanlanceSql import initEquipmentBalance, updateOneEquipmentBalanceData
from widgets.alocatMange.allotSchedule import widget_AllotSchedule
from database.strengthDisturbSql import *
from PyQt5.Qt import Qt
from PyQt5.QtGui import QColor, QBrush,QFont
from database.alocatMangeSql import *
from sysManage.alocatMange.ArmySchedule import ArmySchedule
from sysManage.alocatMange.armyTransfer import armyTransfer
from sysManage.alocatMange.ScheduleFinish import ScheduleFisish
from sysManage.alocatMange.transferModel import transferModel
from sysManage.userInfo import get_value

class AllotSchedule(QWidget,widget_AllotSchedule):
    def __init__(self,parent=None):
        super(AllotSchedule, self).__init__(parent)
        self.setupUi(self)
        self.initAll()
        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}
        self.currentDisturbPlan = {}
        self.currentUnitDisturbPlanNum = {}
        self.unitDisturbPlanList = {}
        self.currentEquipdict = {}
        self.armySchedule = ArmySchedule(self)
        self.scheduleFinish = ScheduleFisish(self)
        self.fileName = ""
        self.unitFlag = 0
        self.rocketSchedule = transferModel(self)
        self.signalConnect()


    def initAll(self):
        self.tw_first.header().setVisible(False)
        self.tw_second.header().setVisible(False)
        self.le_first.setDisabled(1)
        self.le_second.setDisabled(1)
        self.tw_first.setDisabled(1)
        self.tw_second.setDisabled(1)
        self.tw_first.clear()
        self.tw_second.clear()
        self.txt_disturbPlanYear.clear()
        self.cb_schedule.setDisabled(1)
        self.tb_proof.clear()
        self.disturbResult.clear()
        self._initYearWidget_()



    def signalConnect(self):
        # 点击选择年份后刷新页面 初始化
        self.lw_yearChoose.itemClicked.connect(self.slotClickedInqury)
        self.lw_yearChoose.itemClicked.connect(self.setDisturbPlanTitle)
        self.lw_yearChoose.itemClicked.connect(self.initDisturbPlanProof)
        # 点击第一目录结果
        self.tw_first.itemClicked.connect(self.slotDisturbStrengthResult)
        # 点击第二目录结果
        self.tw_second.itemClicked.connect(self.slotDisturbStrengthResult)
        self.tw_second.itemChanged.connect(self.slotCheckedChange)
        self.cb_schedule.activated.connect(self.selectSchedule)



    # 信号与槽连接的断开
    def signalDisconnectSlot(self):
        pass


    # 初始化年份
    def _initYearWidget_(self):
        self.yearList = []
        self.currentYear = None
        self.lw_yearChoose.clear()
        # self.yearList = ['全部']
        allYear = selectYearListAboutDisturbPlan()
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
        self.cb_schedule.setDisabled(0)
        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}
        self.initUserInfo()
        self.currentYear = self.lw_yearChoose.currentItem().text()
        self._initUnitTreeWidget("", self.tw_first)
        startInfo = selectDisturbPlanUnitInfoByUnitID(self.userInfo[0][4])
        stack = []
        root = []
        if startInfo:
            stack.append(startInfo)
            root.append(self.tw_first)
            self._initUnitTreeWidget(stack, root)

        equipInfo =  findUperEquipIDByName("通用装备")
        stack = []
        root = []
        if equipInfo:
            stack.append(equipInfo[0])
            root.append(self.tw_second)
            self._initEquipTreeWidget(stack, root)
        # startEquipIDInfo = findUperEquipIDByName("通用装备")
        # for startEquipInfo in startEquipIDInfo:
        #     # self.second_treeWidget_dict[0] = startEquipInfo
        #     item = QTreeWidgetItem(self.tw_second)
        #     item.setText(0, startEquipInfo[1])
        #     item.setCheckState(0, Qt.Unchecked)
        #     self.second_treeWidget_dict[startEquipInfo[0]] = item
        #     self._initEquipTreeWidget(startEquipInfo[0], item)
        #     break

    def initUserInfo(self):
        self.userInfo = get_value("totleUserInfo")


    def _initUnitTreeWidget(self, stack,root):
        # if root == '':
        #     result = selectDisturbPlanUnitInfoByDeptUper('')
        # else:
        #     result = selectDisturbPlanUnitInfoByDeptUper(root)
        #
        # # rowData: (单位编号，单位名称，上级单位编号)
        # for rowData in result:
        #     item = QTreeWidgetItem(mother)
        #     item.setText(0, rowData[1])
        #     #item.setCheckState(0, Qt.Unchecked)
        #     self.first_treeWidget_dict[rowData[0]] = item
        #     if rowData[0] != '':
        #         self._initUnitTreeWidget(rowData[0], item)
        #     else:
        #         return
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




    def _initEquipTreeWidget(self, stack,root):
        # if root == '':
        #     result = selectEquipInfoByEquipUper('')
        # else:
        #     result = selectEquipInfoByEquipUper(root)
        # # rowData: (装备编号，装备名称，上级装备编号, 录入类型, 装备类型)
        # for rowData in result:
        #     item = QTreeWidgetItem(mother)
        #     item.setText(0, rowData[1])
        #     item.setCheckState(0, Qt.Unchecked)
        #     self.second_treeWidget_dict[rowData[0]] = item
        #     if rowData[0] != '':
        #         self._initEquipTreeWidget(rowData[0], item)
        #     else:
        #         return
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



    '''
        查询结果
    '''
    def slotDisturbStrengthResult(self):
        self.yearList = []
        self.originalEquipDict={}
        self.currentUnitChilddict = {}
        self.unitFlag = 0
        self.disturbResult.clear()
        # 获取子单位名
        j = 0
        for unitID, unitItem in self.first_treeWidget_dict.items():
            if unitItem == self.tw_first.currentItem():
                if selectUnitIfBase(unitID):
                    self.unitFlag = 2
                    result = findDisturbPlanUnitChildInfo(unitID)
                else:
                    self.unitFlag = 1
                    result = selectDisturbPlanChooseUnit()
                for resultInfo in result:
                    self.currentUnitChilddict[j] = resultInfo
                    j = j + 1
        #print("unit", self.currentUnitChilddict)
        # 获取当前装备名
        j = 0
        for equipID, equipItem in self.second_treeWidget_dict.items():
            if equipItem.checkState(0) == Qt.Checked:
                equipInfo = findEquipInfo(equipID)
                self.originalEquipDict[j]= equipInfo[0]
                j=j+1
            elif equipItem.checkState(0) == Qt.PartiallyChecked:
                equipInfo = findEquipInfo(equipID)
                self.originalEquipDict[j] = equipInfo[0]
                j=j+1
        #print("self.originalEquipDict",self.originalEquipDict)
        self._initDisturbPlanByUnitListAndEquipList(self.originalEquipDict)


    '''
        初始化分配计划结果
    '''
    def _initDisturbPlanByUnitListAndEquipList(self,equipDict):
        self.disturbResult.clear()
        self.disturbResult.setRowCount(0)
        self.currentEquipdict = equipDict
        self.lenCurrentUnitChilddict = len(self.currentUnitChilddict)
        self.lenCurrentEquipdict = len(self.currentEquipdict)
        # 选择机关或其他
        if self.unitFlag == 1:
            headerlist = ['装备名称及规格型号', '单位', '陆军调拨单开具数', '机关分配计划数', '此次分配合计数']
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
            self.disturbResult.setRowCount(len(self.currentEquipdict))
            self.disturbResult.setHorizontalHeaderLabels(headerlist)
            self.currentDisturbPlan.clear()
            self.disturbResult.setColumnWidth(0, 200)
            i = 0
            for LineInfo in self.currentEquipdict.values():
                currentRowResult = []
                item = QTableWidgetItem(LineInfo[1])
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                currentRowResult.append(item)
                self.disturbResult.setItem(i, 0, item)
                item = QTableWidgetItem("")
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
                for x in range(0, self.lenCurrentUnitChilddict):
                    item = QTableWidgetItem("")
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    self.disturbResult.setItem(i, x + 5, item)
                    currentRowResult.append(item)
                item = QTableWidgetItem("")
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.disturbResult.setItem(i, 9 + self.lenCurrentUnitChilddict, item)
                currentRowResult.append(item)
                i = i + 1
        # 选择各基地
        elif self.unitFlag == 2:
            headerlist = ['装备名称及规格型号', '单位', '火箭军调拨单开具数', '此次机关分配数', '此次分配合计数']
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
            self.disturbResult.setRowCount(len(self.currentEquipdict))
            self.disturbResult.setHorizontalHeaderLabels(headerlist)
            self.disturbResult.setColumnWidth(0, 200)
            i = 0
            for LineInfo in self.currentEquipdict.values():
                currentRowResult = []
                item = QTableWidgetItem(LineInfo[1])
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                currentRowResult.append(item)
                self.disturbResult.setItem(i, 0, item)
                item = QTableWidgetItem("")
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
                for x in range(0, self.lenCurrentUnitChilddict):
                    item = QTableWidgetItem("")
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    self.disturbResult.setItem(i, x + 5, item)
                    currentRowResult.append(item)
                item = QTableWidgetItem("")
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.disturbResult.setItem(i, 9 + self.lenCurrentUnitChilddict, item)
                currentRowResult.append(item)
                i = i + 1
        self.disturbResult.setColumnWidth(2, 150)
        self.initDisturbPlanNum()
        self.initDisturbPlanNote()
        self.initDisturbPlanInputNum()
        self.initDisturbPlanOther()
        self.ifEquipHaveChild()

    # 初始化自定义计划数
    def initDisturbPlanInputNum(self):
        if self.unitFlag == 1:
            unitDisturbPlanInputNumList = selectDisturbPlanInputNumUpmost(self.currentEquipdict, self.currentYear)
            for i in range(0, len(self.currentEquipdict)):
                item = self.disturbResult.item(i, 3)
                if unitDisturbPlanInputNumList[i] is not None:
                    item.setText(str(unitDisturbPlanInputNumList[i]))
                # item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
        elif self.unitFlag == 2:
            unitDisturbPlanInputNumList = selectDisturbPlanInputNumBase(self.currentEquipdict, self.currentYear)
            for i in range(0, len(self.currentEquipdict)):
                item = self.disturbResult.item(i, 3)
                if unitDisturbPlanInputNumList[i] is not None:
                    item.setText(str(unitDisturbPlanInputNumList[i]))
                # item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)

    '''
        若装备不含子装备，则设置按钮
    '''
    def ifEquipHaveChild(self):
        for i in self.currentEquipdict:
            if not selectEquipIsHaveChild(self.currentEquipdict[i][0]):
                # 陆军调拨单进度
                flag1 = selectArmySchedule(self.currentEquipdict[i][0],self.currentYear)
                item = QPushButton("设置进度")
                item.clicked.connect(self.setArmySchedule)
                if flag1[0][0] != '0':
                    item = QPushButton("已完成")
                self.disturbResult.setCellWidget(i, 5 + self.lenCurrentUnitChilddict, item)

                # 是否具备接装条件

                flag2 = selectAllotCondition(self.currentEquipdict[i][0],self.currentYear)
                item = QPushButton("设置进度")
                item.clicked.connect(self.setCondition)
                if int(flag2[0][0]):
                    item = QPushButton("已完成")
                self.disturbResult.setCellWidget(i, 6 + self.lenCurrentUnitChilddict, item)

                # 火箭军调拨单进度
                flag3 = selectRocketSchedule(self.currentEquipdict[i][0], self.currentYear)
                item = QPushButton("设置进度")
                item.clicked.connect(self.setRocketSchedule)
                if int(flag3[0][0]):
                    item = QPushButton("已完成")
                self.disturbResult.setCellWidget(i, 7 + self.lenCurrentUnitChilddict, item)


                # 是否完成接装
                flag4 = selectIfScheduleFinish(self.currentEquipdict[i][0], self.currentYear)
                print("flag4",flag4)
                item = QPushButton("设置进度")
                item.clicked.connect(self.setScheduleFinish)
                if flag4[0][0] != '0':
                    item = QPushButton("已完成")
                self.disturbResult.setCellWidget(i, 8 + self.lenCurrentUnitChilddict, item)

    # 初始化调拨依据
    def initDisturbPlanProof(self):
        proof = selectDisturbPlanProof(self.currentYear)
        self.tb_proof.setText(proof[0][0])
        #self..setTextInteractionFlags(Qt.TextSelectableByMouse|Qt.TextSelectableByKeyboard)



    # 读取初始分配计划数
    def initDisturbPlanNum(self):
        #print("currentYear:", self.currentYear)
        self.unitDisturbPlanList = selectDisturbPlanNum(self.currentUnitChilddict,
                                                        self.currentEquipdict, self.currentYear)
        print("self.unitDisturbPlanList", self.unitDisturbPlanList)
        # 显示每个单位分配计划数
        num = 0
        for i in range(0, len(self.currentUnitChilddict)):
            for j in range(0, len(self.currentEquipdict)):
                item = self.disturbResult.item(j, 5 + i)
                if self.unitDisturbPlanList[num] != '-1':
                    item.setText(self.unitDisturbPlanList[num])
                num = num + 1
        self.initDisturbPlanSum()


    # 初始化此次分配数
    def initDisturbPlanSum(self):
        # 显示此次分配计划数
        sum = 0
        for i in self.currentEquipdict:
            if not selectEquipIsHaveChild(self.currentEquipdict[i][0]):
                for j in range(0, len(self.currentUnitChilddict)):
                    num = self.disturbResult.item(i, 5 + j).text()
                    if num == '-1' or num == '':
                        sum = sum + 0
                    else:
                        sum = sum + int(num)
                self.disturbResult.item(i, 4).setText(str(sum))
            sum = 0



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



    # 初始化分配计划年份
    def setDisturbPlanTitle(self):
        txt=str(self.currentYear)+"年分配计划"
        self.txt_disturbPlanYear.setFont(QFont("Microsoft YaHei"))
        self.txt_disturbPlanYear.setAlignment(Qt.AlignCenter)
        self.txt_disturbPlanYear.setTextInteractionFlags(Qt.NoTextInteraction)
        self.txt_disturbPlanYear.setFontPointSize(15)
        self.txt_disturbPlanYear.setText(txt)


    # 读取初始分配计划备注
    def initDisturbPlanNote(self):
        self.unitDisturbPlanNoteList = selectDisturbPlanNote(self.currentEquipdict, self.currentYear)
        #print("self.unitDisturbPlanNoteList", self.unitDisturbPlanNoteList)
        for i in range(0,len(self.currentEquipdict)):
            item=self.disturbResult.item(i,self.lenHeaderList-1)
            if self.unitDisturbPlanNoteList[i] is not None:
                item.setText(str(self.unitDisturbPlanNoteList[i]))

    # 初始化机关单位数与装备单位
    def initDisturbPlanOther(self):
        self.unitDisturbPlanOtherList = selectDisturbPlanOther(self.currentEquipdict, self.currentYear)
        unitRocketOther = selectRocketOther(self.currentEquipdict, self.currentYear)
        # 装备单位
        for i in range(0, len(self.currentEquipdict)):
            item = self.disturbResult.item(i, 1)
            if self.unitDisturbPlanOtherList[i]:
                item.setText(str(self.unitDisturbPlanOtherList[i][0]))
            else:
                item.setText("")
        if self.unitFlag == 1:
            # 陆军调拨单开具数
            for unitID, unitItem in self.first_treeWidget_dict.items():
                if unitItem == self.tw_first.currentItem():
                    # if selectUnitIfUppermost(unitID):
                    for i in range(0, len(self.currentEquipdict)):
                        item = self.disturbResult.item(i, 2)
                        if self.unitDisturbPlanOtherList[i]:
                            item.setText(str(self.unitDisturbPlanOtherList[i][1]))
                        else:
                            item.setText("0")
                    for childRow, equipInfo in self.currentEquipdict.items():
                        uperInfoList = selectUperInfoByEquipID(equipInfo[0])
                        childNum = self.disturbResult.item(childRow, 2).text()
                        for uperInfo in uperInfoList:
                            for row, uperInfoRow in self.currentEquipdict.items():
                                if uperInfo[0] == uperInfoRow[0]:
                                    num = self.disturbResult.item(row, 2).text()
                                    totalNum = int(childNum) + int(num)
                                    self.disturbResult.item(row, 2).setText(str(totalNum))
                    # else:
                    #     for i in self.currentEquipdict:
                    #         item = self.disturbResult.item(i, 2)
                    #         result = selectDisturbPlanNum({0: [unitID]}, self.currentEquipdict, self.currentYear)
                    #         if result:
                    #             item.setText(str(result[i]))
                    #         else:
                    #             item.setText("0")
        elif self.unitFlag == 2:
            # 火箭军调拨单分配数
            for unitID, unitItem in self.first_treeWidget_dict.items():
                if unitItem == self.tw_first.currentItem():
                    # if selectUnitIfUppermost(unitID):
                    for i in range(0, len(self.currentEquipdict)):
                        item = self.disturbResult.item(i, 2)
                        if unitRocketOther[i]:
                            item.setText(str(unitRocketOther[i][1]))
                        else:
                            item.setText("0")
                    for childRow, equipInfo in self.currentEquipdict.items():
                        uperInfoList = selectUperInfoByEquipID(equipInfo[0])
                        childNum = self.disturbResult.item(childRow, 2).text()
                        for uperInfo in uperInfoList:
                            for row, uperInfoRow in self.currentEquipdict.items():
                                if uperInfo[0] == uperInfoRow[0]:
                                    num = self.disturbResult.item(row, 2).text()
                                    totalNum = int(childNum) + int(num)
                                    self.disturbResult.item(row, 2).setText(str(totalNum))
                    # else:
                    #     for i in self.currentEquipdict:
                    #         item = self.disturbResult.item(i, 2)
                    #         result = selectDisturbPlanNum({0: [unitID]}, self.currentEquipdict, self.currentYear)
                    #         if result:
                    #             item.setText(str(result[i]))
                    #         else:
                    #             item.setText("0")


    def setArmySchedule(self):
        self.armySchedule.setYear(self.currentYear)
        self.armySchedule.setWindowTitle("陆军调拨单选择")
        self.armySchedule.setWindowFlags(Qt.Dialog|Qt.WindowCloseButtonHint)
        self.armySchedule._initSelf_()
        self.armySchedule.show()
        self.armySchedule.signal.connect(self.updateArmy)

    def setRocketSchedule(self):
        row = self.disturbResult.currentRow()
        currentColomn = self.disturbResult.currentColumn()
        if row < 0 or currentColomn < 0:
            return
        if currentColomn - 1 < 0:
            return
        if self.disturbResult.cellWidget(row, currentColomn - 1).text() != "已完成":
            QMessageBox.information(self, "设置接装条件", "上一级未完成", QMessageBox.Yes)
            return
        currentUnit=[]
        for i in self.currentUnitChilddict.values():
            currentUnit.append(i)
        if row != -1:
            # 存放质量和陆军单号
            result1 = selectQuaAndID(self.currentEquipdict[row][0],self.currentYear)
            if result1:
                info1=[result1[0][0],self.disturbResult.item(row,4).text()]
                for i in range(0,self.lenCurrentUnitChilddict):
                    info1.append(self.disturbResult.item(row,5+i).text())
                info1.append(self.tb_proof.toPlainText())
                info1.append(result1[0][1])
                self.rocketSchedule.getUnitIDList(currentUnit,self.currentEquipdict[self.disturbResult.currentRow()],self.currentYear,info1)
            else:
                self.rocketSchedule.getUnitIDList("", "",
                                                  "", "")
            self.rocketSchedule.setWindowFlags(Qt.Dialog|Qt.WindowCloseButtonHint)
            self.rocketSchedule.show()
            self.rocketSchedule.signal.connect(self.updateRocket)

    def updateRocket(self):
        currentRow = self.disturbResult.currentRow()
        item = QPushButton("已完成")
        self.disturbResult.setCellWidget(currentRow, 7 + self.lenCurrentUnitChilddict, item)
        updateRocketSchedule(self.currentEquipdict[currentRow][0], self.currentYear)


    def updateArmy(self):
        currentRow = self.disturbResult.currentRow()
        item = QPushButton("已完成")
        self.disturbResult.setCellWidget(currentRow, 5 + self.lenCurrentUnitChilddict, item)
        updateArmySchedule(self.currentEquipdict[currentRow][0], self.currentYear)


    def setCondition(self):
        currentRow=self.disturbResult.currentRow()
        currentColomn = self.disturbResult.currentColumn()
        if currentRow < 0 or currentColomn <0:
            return
        if currentColomn - 1 < 0:
            return
        if self.disturbResult.cellWidget(currentRow, currentColomn - 1).text() != "已完成":
            QMessageBox.information(self, "设置接装条件", "上一级未完成", QMessageBox.Yes)
            return
        reply = QMessageBox.question(self,"设置接装条件","是否具备接装条件？",QMessageBox.Yes,QMessageBox.Cancel)
        if reply==QMessageBox.Yes:
            item = QPushButton("已完成")
            self.disturbResult.setCellWidget(currentRow, 6 + self.lenCurrentUnitChilddict, item)
            updateAllotCondition(self.currentEquipdict[currentRow][0],self.currentYear)

    def setScheduleFinish(self):
        currentRow = self.disturbResult.currentRow()
        currentColomn = self.disturbResult.currentColumn()
        if currentRow < 0 or currentColomn < 0:
            return
        if currentColomn - 1 < 0:
            return
        if self.disturbResult.cellWidget(currentRow, currentColomn - 1).text() != "已完成":
            QMessageBox.information(self, "设置接装条件", "上一级未完成", QMessageBox.Yes)
            return
        self.scheduleFinish.setWindowFlags(Qt.Dialog|Qt.WindowCloseButtonHint)
        self.scheduleFinish.show()
        self.scheduleFinish.signal.connect(self.updateFinish)


    def updateFinish(self):
        currentRow = self.disturbResult.currentRow()
        fileName = self.scheduleFinish.returnFileName()
        print("fileName", fileName)
        if fileName != "":
            item = QPushButton("已完成")
            self.disturbResult.setCellWidget(currentRow, 8 + self.lenCurrentUnitChilddict, item)
            updateScheduleFinish(self.currentEquipdict[currentRow][0], self.currentYear,fileName)

    # 筛选调拨进度
    def selectSchedule(self):
        index = self.cb_schedule.currentIndex()
        # 未选择状态
        if index == 0:
            self._initDisturbPlanByUnitListAndEquipList(self.originalEquipDict)

        # 完成进度一
        elif index == 1:
            equipDict={}
            j = 0
            for equipID, equipItem in self.second_treeWidget_dict.items():
                flag1 = selectArmySchedule(equipID, self.currentYear)
                if flag1[0][0] != '0':
                    if equipItem.checkState(0) == Qt.Checked:
                        equipInfo = findEquipInfo(equipID)
                        equipDict[j] = equipInfo[0]
                        j = j + 1
                    elif equipItem.checkState(0) == Qt.PartiallyChecked:
                        equipInfo = findEquipInfo(equipID)
                        equipDict[j] = equipInfo[0]
                        j = j + 1
            self._initDisturbPlanByUnitListAndEquipList(equipDict)

        # 完成进度二
        elif index == 2:
            equipDict = {}
            j = 0
            for equipID, equipItem in self.second_treeWidget_dict.items():
                flag2 = selectAllotCondition(equipID, self.currentYear)
                if int(flag2[0][0]):
                    if equipItem.checkState(0) == Qt.Checked:
                        equipInfo = findEquipInfo(equipID)
                        equipDict[j] = equipInfo[0]
                        j = j + 1
                    elif equipItem.checkState(0) == Qt.PartiallyChecked:
                        equipInfo = findEquipInfo(equipID)
                        equipDict[j] = equipInfo[0]
                        j = j + 1
            self._initDisturbPlanByUnitListAndEquipList(equipDict)

        # 完成进度三
        elif index == 3:
            equipDict = {}
            j = 0
            for equipID, equipItem in self.second_treeWidget_dict.items():
                flag3 = selectRocketSchedule(equipID, self.currentYear)
                if int(flag3[0][0]):
                    if equipItem.checkState(0) == Qt.Checked:
                        equipInfo = findEquipInfo(equipID)
                        equipDict[j] = equipInfo[0]
                        j = j + 1
                    elif equipItem.checkState(0) == Qt.PartiallyChecked:
                        equipInfo = findEquipInfo(equipID)
                        equipDict[j] = equipInfo[0]
                        j = j + 1
            self._initDisturbPlanByUnitListAndEquipList(equipDict)

        # 完成进度四
        elif index == 4:
            equipDict = {}
            j = 0
            for equipID, equipItem in self.second_treeWidget_dict.items():
                flag4 = selectIfScheduleFinish(equipID, self.currentYear)
                if flag4[0][0] != '0':
                    if equipItem.checkState(0) == Qt.Checked:
                        equipInfo = findEquipInfo(equipID)
                        equipDict[j] = equipInfo[0]
                        j = j + 1
                    elif equipItem.checkState(0) == Qt.PartiallyChecked:
                        equipInfo = findEquipInfo(equipID)
                        equipDict[j] = equipInfo[0]
                        j = j + 1
            self._initDisturbPlanByUnitListAndEquipList(equipDict)
