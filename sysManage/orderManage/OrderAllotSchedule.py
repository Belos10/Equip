from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *

from database.OrderManageSql import *
from sysManage.alocatMange.transferModel import transferModel
from sysManage.orderManage.OrderScheduleFinish import OrderScheduleFinish
from sysManage.orderManage.selectCont import SelectCont
from sysManage.orderManage.selectQua import SelectQua
from sysManage.userInfo import get_value
from utills.Search import selectUnit
from widgets.orderManage.Widget_OrderAllotSchedule import widget_OrderAllotSchedule
from sysManage.component import getMessageBox


class OrderAllotSchedule(QWidget, widget_OrderAllotSchedule):
    def __init__(self,parent=None):
        super(OrderAllotSchedule, self).__init__(parent)
        self.setupUi(self)
        self.initAll()
        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}
        self.currentDisturbPlan = {}
        self.currentUnitDisturbPlanNum = {}
        self.unitDisturbPlanList = {}
        self.currentEquipdict = {}
        self.contractSchedule = SelectCont(self)
        self.scheduleFinish = OrderScheduleFinish(self)
        self.fileName = ""
        self.unitFlag = 0
        self.rocketSchedule = transferModel(self)
        self.selectQua = SelectQua()
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
        self.disturbResult.setRowCount(0)
        self.disturbResult.setColumnCount(0)
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
        self.pb_firstSelect.clicked.connect(self.slotSelectUnit)
        self.pb_secondSelect.clicked.connect(self.slotSelectEquip)




    def slotSelectUnit(self):
        selectUnit(self, self.le_first, self.first_treeWidget_dict, self.tw_first)


    def slotSelectEquip(self):
        selectUnit(self, self.le_second, self.second_treeWidget_dict, self.tw_second)



    # 信号与槽连接的断开
    def signalDisconnectSlot(self):
        pass


    # 初始化年份
    def _initYearWidget_(self):
        self.yearList = []
        self.currentYear = None
        self.lw_yearChoose.clear()
        # self.yearList = ['全部']
        allYear = selectYearListAboutOrderPlan()
        for year in allYear:
            self.yearList.append(year)

        for year in self.yearList:
            item = QListWidgetItem()
            item.setText(year)
            self.lw_yearChoose.addItem(item)



    def slotClickedInqury(self):
        self.initUserInfo()
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
        self.currentYear = self.lw_yearChoose.currentItem().text()
        # self._initUnitTreeWidget("", self.tw_first)
        startInfo = selectUnitInfoByUnitID(self.userInfo[0][4])
        stack = []
        root = []
        if startInfo:
            stack.append(startInfo)
            root.append(self.tw_first)
            self._initUnitTreeWidget(stack, root)

        equipInfo = findUperEquipIDByName("专用装备")
        stack = []
        root = []
        if equipInfo:
            stack.append(equipInfo[0])
            root.append(self.tw_second)
            self._initEquipTreeWidget(stack, root, 0)

    def initUserInfo(self):
        self.userInfo = get_value("totleUserInfo")


    def _initUnitTreeWidget(self, stack,root):
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

    def _initEquipTreeWidget(self, stack, root, count):
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
                self._initEquipTreeWidget(stack, root, count + 1)

    def addTab(self, result):
        count = selectLevelForEquip(result[0][0])
        Name = count * '    ' + result[0][1]
        result1 = []
        for i,value in enumerate(result[0]):
            if i != 1:
                result1.append(result[0][i])
            else:
                result1.append(Name)
        result[0] = tuple(result1)
        return result

    def initcbschedule(self):
        self.cb_schedule.clear()
        if self.unitFlag == 1:
            self.cb_schedule.addItem("全部",0)
            self.cb_schedule.addItem("完成进度1",1)
            self.cb_schedule.addItem("完成进度2", 2)
            self.cb_schedule.addItem("完成进度3", 3)
            self.cb_schedule.addItem("完成全部进度", 4)
        elif self.unitFlag == 2:
            self.cb_schedule.addItem("全部", 0)
            self.cb_schedule.addItem("完成进度1", 1)
            self.cb_schedule.addItem("完成进度2", 2)
            self.cb_schedule.addItem("完成全部进度", 3)



    '''
        查询结果
    '''
    def slotDisturbStrengthResult(self):
        self.yearList = []
        self.originalEquipDict = {}
        self.originalEquipDictTab = {}
        self.currentUnitChilddict = {}
        self.unitFlag = 0
        self.disturbResult.clear()
        self.cb_schedule.setCurrentIndex(0)
        # 获取子单位名
        j = 0
        for unitID, unitItem in self.first_treeWidget_dict.items():
            if unitItem == self.tw_first.currentItem():
                if selectUnitIfBase(unitID):
                    self.unitFlag = 2
                    result = findUnitChildInfo(unitID)
                    self.initcbschedule()
                else:
                    self.unitFlag = 1
                    result = selectOrderPlanChooseUnit()
                    self.initcbschedule()
                for resultInfo in result:
                    self.currentUnitChilddict[j] = resultInfo
                    j = j + 1
        #print("unit", self.currentUnitChilddict)
        # 获取当前装备名
        j = 0
        for equipID, equipItem in self.second_treeWidget_dict.items():
            if equipItem.checkState(0) == Qt.Checked:
                equipInfo = findEquipInfo(equipID)
                self.originalEquipDict[j] = equipInfo[0]
                equipInfo = self.addTab(equipInfo)
                self.originalEquipDictTab[j] = equipInfo[0]
                j = j + 1
            elif equipItem.checkState(0) == Qt.PartiallyChecked:
                equipInfo = findEquipInfo(equipID)
                self.originalEquipDict[j] = equipInfo[0]
                equipInfo = self.addTab(equipInfo)
                self.originalEquipDictTab[j] = equipInfo[0]
                j = j + 1
        #print("self.originalEquipDict",self.originalEquipDict)
        self._initDisturbPlanByUnitListAndEquipList(self.originalEquipDict,self.originalEquipDictTab)


    '''
        初始化分配计划结果
    '''
    def _initDisturbPlanByUnitListAndEquipList(self,equipDict,equipDictTab={}):
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
            headerlist.append('合同进度')
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
            for LineInfo in equipDictTab.values():
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
            headerlist = ['装备名称及规格型号', '单位', '火箭军调拨单开具数', '机关分配计划数', '此次分配合计数']
            if len(self.currentUnitChilddict):
                for i in self.currentUnitChilddict.values():
                    headerlist.append(i[1])
            headerlist.append('火箭军调拨单进度')
            headerlist.append('接装条件')
            headerlist.append('完成接装')
            headerlist.append('备注')
            self.lenHeaderList = len(headerlist)
            self.disturbResult.setColumnCount(self.lenHeaderList)
            self.disturbResult.setRowCount(len(self.currentEquipdict))
            self.disturbResult.setHorizontalHeaderLabels(headerlist)
            self.disturbResult.setColumnWidth(0, 200)
            i = 0
            for LineInfo in equipDictTab.values():
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
                self.disturbResult.setItem(i, 8 + self.lenCurrentUnitChilddict, item)
                currentRowResult.append(item)
                i = i + 1
        self.disturbResult.setColumnWidth(2, 150)
        if self.currentUnitChilddict and self.currentEquipdict:
            self.initDisturbPlanNum()
            self.initDisturbPlanNote()
            self.initDisturbPlanInputNum()
            self.initDisturbPlanOther()
            self.ifEquipHaveChild()

    # 初始化自定义计划数
    def initDisturbPlanInputNum(self):
        if self.unitFlag == 1:
            unitDisturbPlanInputNumList = selectOrderPlanInputNumUpmost(self.currentEquipdict, self.currentYear)
            for i in range(0, len(self.currentEquipdict)):
                item = self.disturbResult.item(i, 3)
                if unitDisturbPlanInputNumList[i] is not None:
                    item.setText(str(unitDisturbPlanInputNumList[i]))
                # item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
        elif self.unitFlag == 2:
            unitDisturbPlanInputNumList = selectOrderPlanInputNumBase(self.currentEquipdict, self.currentYear)
            for i in range(0, len(self.currentEquipdict)):
                item = self.disturbResult.item(i, 3)
                if unitDisturbPlanInputNumList[i] is not None:
                    item.setText(str(unitDisturbPlanInputNumList[i]))
                # item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)

    '''
        若装备不含子装备，则设置按钮
    '''
    def ifEquipHaveChild(self):
        # 选择机关或其他
        if self.unitFlag == 1:
            for i in self.currentEquipdict:
                if not selectEquipIsHaveChild(self.currentEquipdict[i][0]):
                    # 陆军调拨单进度
                    flag1 = selectContractSchedule(self.currentEquipdict[i][0],self.currentYear)
                    item = QPushButton("设置进度")
                    item.clicked.connect(self.setContractSchedule)
                    if flag1[0][0] != '':
                        item = QPushButton(flag1[0][0])
                    self.disturbResult.setCellWidget(i, 5 + self.lenCurrentUnitChilddict, item)

                    # 是否具备接装条件
                    flag2 = selectAllotConditionUper(self.currentEquipdict[i][0], self.currentYear)
                    item = QPushButton("设置进度")
                    item.clicked.connect(self.setCondition)
                    if int(flag2[0][0]):
                        item = QPushButton("已完成")
                    self.disturbResult.setCellWidget(i, 6 + self.lenCurrentUnitChilddict, item)

                    # 火箭军调拨单进度
                    flag3 = selectRocketScheduleUper(self.currentEquipdict[i][0], self.currentYear)
                    item = QPushButton("设置进度")
                    item.clicked.connect(self.setQua)
                    if int(flag3[0][0]):
                        # txt = selectRocketTransID(self.currentEquipdict[i][0], self.currentYear)
                        # item = QPushButton(txt[0][0])
                        item = QPushButton("已完成")
                        item.clicked.connect(self.showRocket)
                    self.disturbResult.setCellWidget(i, 7 + self.lenCurrentUnitChilddict, item)

                    # 是否完成接装
                    flag4 = selectIfScheduleFinishUper(self.currentEquipdict[i][0], self.currentYear)
                    print("flag4",flag4)
                    item = QPushButton("设置进度")
                    item.clicked.connect(self.setScheduleFinish)
                    if flag4[0][0] != 'FALSE':
                        item = QPushButton("已完成")
                    self.disturbResult.setCellWidget(i, 8 + self.lenCurrentUnitChilddict, item)
        # 选择基地
        elif self.unitFlag == 2:
            for i in self.currentEquipdict:
                if not selectEquipIsHaveChild(self.currentEquipdict[i][0]):
                    # # 合同进度
                    # flag1 = selectContractSchedule(self.currentEquipdict[i][0], self.currentYear)
                    # item = QPushButton("设置进度")
                    # item.clicked.connect(self.setContractSchedule)
                    # if flag1[0][0] != '':
                    #     item = QPushButton(flag1[0][0])
                    # self.disturbResult.setCellWidget(i, 5 + self.lenCurrentUnitChilddict, item)

                    # 火箭军调拨单进度
                    flag2 = selectRocketScheduleBase(self.currentEquipdict[i][0], self.currentYear)
                    item = QPushButton("设置进度")
                    item.clicked.connect(self.setQua)
                    if int(flag2[0][0]):
                        # txt = selectRocketTransID(self.currentEquipdict[i][0], self.currentYear)
                        # item = QPushButton(txt[0][0])
                        item = QPushButton("已完成")
                        item.clicked.connect(self.showRocket)
                    self.disturbResult.setCellWidget(i, 5 + self.lenCurrentUnitChilddict, item)

                    # 是否具备接装条件
                    flag3 = selectAllotConditionBase(self.currentEquipdict[i][0], self.currentYear)
                    item = QPushButton("设置进度")
                    item.clicked.connect(self.setCondition)
                    if int(flag3[0][0]):
                        item = QPushButton("已完成")
                    self.disturbResult.setCellWidget(i, 6 + self.lenCurrentUnitChilddict, item)

                    # 是否完成接装
                    flag4 = selectIfScheduleFinishBase(self.currentEquipdict[i][0], self.currentYear)
                    print("flag4", flag4)
                    item = QPushButton("设置进度")
                    item.clicked.connect(self.setScheduleFinish)
                    if flag4[0][0] != 'FALSE':
                        item = QPushButton("已完成")
                    self.disturbResult.setCellWidget(i, 7 + self.lenCurrentUnitChilddict, item)

    # 初始化调拨依据
    def initDisturbPlanProof(self):
        proof = selectOrderPlanProof(self.currentYear)
        self.tb_proof.setText(proof[0][0])
        # self.setTextInteractionFlags(Qt.TextSelectableByMouse|Qt.TextSelectableByKeyboard)



    # 读取初始分配计划数
    def initDisturbPlanNum(self):
        # print("currentYear:", self.currentYear)
        self.unitDisturbPlanList = selectOrderAllotPlanNumByList(self.currentUnitChilddict,
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
                    if num == '':
                        sum = sum + 0
                    else:
                        sum = sum + int(num)
                self.disturbResult.item(i, 4).setText(str(sum))
            sum = 0
        for row in reversed(range(len(self.currentEquipdict))):
            sum = 0
            for childRow in reversed(range(len(self.currentEquipdict))):
                # 第0个字段是EquipID,第二个字段是Equip_Uper
                if self.currentEquipdict[row][0] == self.currentEquipdict[childRow][2]:
                    num = self.disturbResult.item(childRow, 4).text()
                    if num != '':
                        sum = sum + int(num)
            if sum != 0:
                self.disturbResult.item(row, 4).setText(str(sum))
        # 每个单位的上层装备合计数
        for i in range(0, len(self.currentUnitChilddict)):
            for row in reversed(range(len(self.currentEquipdict))):
                sum = 0
                for childRow in reversed(range(len(self.currentEquipdict))):
                    # 第0个字段是EquipID,第二个字段是Equip_Uper
                    if self.currentEquipdict[row][0] == self.currentEquipdict[childRow][2]:
                        num = self.disturbResult.item(childRow, 5 + i).text()
                        if num != '':
                            sum = sum + int(num)
                if sum != 0:
                    self.disturbResult.item(row, 5 + i).setText(str(sum))

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
        unitDisturbPlanNoteList = selectOrderPlanNote(self.currentEquipdict, self.currentYear)
        # print("self.unitDisturbPlanNoteList", self.unitDisturbPlanNoteList)
        for i in range(0,len(self.currentEquipdict)):
            item=self.disturbResult.item(i,self.lenHeaderList-1)
            if unitDisturbPlanNoteList[i] is not None:
                item.setText(str(unitDisturbPlanNoteList[i]))

    # 初始化机关单位数与装备单位
    def initDisturbPlanOther(self):
        unitDisturbPlanOtherList = selectOrderPlanOther(self.currentEquipdict, self.currentYear)
        # 装备单位
        for i in range(0, len(self.currentEquipdict)):
            item = self.disturbResult.item(i, 1)
            item.setText(str(self.currentEquipdict[i][5]))
        if self.unitFlag == 1:
            # 陆军调拨单开具数
            for unitID, unitItem in self.first_treeWidget_dict.items():
                if unitItem == self.tw_first.currentItem():
                    # if selectUnitIfUppermost(unitID):
                    for i in range(0, len(self.currentEquipdict)):
                        item = self.disturbResult.item(i, 2)
                        if unitDisturbPlanOtherList[i]:
                            item.setText(str(unitDisturbPlanOtherList[i][0][1]))
                        else:
                            item.setText("")

                    for row in reversed(range(len(self.currentEquipdict))):
                        sum = 0
                        for childRow in reversed(range(len(self.currentEquipdict))):
                            # 第0个字段是EquipID,第二个字段是Equip_Uper
                            if self.currentEquipdict[row][0] == self.currentEquipdict[childRow][2]:
                                num = self.disturbResult.item(childRow, 2).text()
                                if num != '':
                                    sum = sum + int(num)
                        if sum != 0:
                            self.disturbResult.item(row, 2).setText(str(sum))
        elif self.unitFlag == 2:
            # 火箭军调拨单分配数
            for unitID, unitItem in self.first_treeWidget_dict.items():
                if unitItem == self.tw_first.currentItem():
                    for i in self.currentEquipdict:
                        item = self.disturbResult.item(i, 2)
                        result = selectOrderAllotPlanNumByList({0: [unitID]}, self.currentEquipdict, self.currentYear)
                        if result:
                            item.setText(str(result[i]))
                        else:
                            item.setText("")

                    for row in reversed(range(len(self.currentEquipdict))):
                        sum = 0
                        for childRow in reversed(range(len(self.currentEquipdict))):
                            # 第0个字段是EquipID,第二个字段是Equip_Uper
                            if self.currentEquipdict[row][0] == self.currentEquipdict[childRow][2]:
                                num = self.disturbResult.item(childRow, 2).text()
                                if num != '':
                                    sum = sum + int(num)
                        if sum != 0:
                            self.disturbResult.item(row, 2).setText(str(sum))


    # 进度1 合同
    def setContractSchedule(self):
        self.contractSchedule._initSelf_()
        self.contractSchedule.setYear(self.currentYear)
        self.contractSchedule.setWindowTitle("合同选择")
        self.contractSchedule.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        self.contractSchedule.show()
        self.contractSchedule.signal.connect(self.updateContract)

    # 更新进度1 合同
    def updateContract(self):
        txt = self.contractSchedule.returnNo()
        currentRow = self.disturbResult.currentRow()
        item = QPushButton(txt)
        self.disturbResult.setCellWidget(currentRow, 5 + self.lenCurrentUnitChilddict, item)
        updateContractSchedule(self.currentEquipdict[currentRow][0], self.currentYear,txt)

    # 进度2 接装条件
    def setCondition(self):
        currentRow = self.disturbResult.currentRow()
        currentColumn = self.disturbResult.currentColumn()
        if currentRow < 0 or currentColumn <0:
            return
        if currentColumn - 1 < 0:
            return
        if self.disturbResult.cellWidget(currentRow, currentColumn - 1).text() == "设置进度":
            getMessageBox("设置接装条件", "上一级未完成", True, False)
            return
        reply = getMessageBox("设置接装条件","是否具备接装条件？", True, True)
        if reply==QMessageBox.Ok:
            item = QPushButton("已完成")
            self.disturbResult.setCellWidget(currentRow, 6 + self.lenCurrentUnitChilddict, item)
            if self.unitFlag == 1:
                updateAllotConditionUper(self.currentEquipdict[currentRow][0], self.currentYear)
            elif self.unitFlag == 2:
                updateAllotConditionBase(self.currentEquipdict[currentRow][0], self.currentYear)

    # 设置装备质量
    def setQua(self):
        self.selectQua._init()
        self.selectQua.show()
        self.selectQua.signal.connect(self.setRocketSchedule)


    # 进度3 火箭军调拨
    def setRocketSchedule(self):
        QuaTxt = self.selectQua.returnQua()
        row = self.disturbResult.currentRow()
        column = self.disturbResult.currentColumn()
        if row < 0 or column < 0:
            return
        if column - 1 < 0:
            return
        if self.unitFlag == 1:
            if self.disturbResult.cellWidget(row, column - 1).text() == "设置进度":
                getMessageBox("设置接装条件", "上一级未完成", True, False)
                return
        currentUnit=[]
        for i in self.currentUnitChilddict.values():
            currentUnit.append(i)
        if row != -1:
            self.selectQua.show()
            # 存放质量和合同单号
            Notxt = selectContractSchedule(self.currentEquipdict[row][0],self.currentYear)
            if Notxt[0][0] != '':
                info1=[QuaTxt, self.disturbResult.item(row,4).text()]
                for i in range(0,self.lenCurrentUnitChilddict):
                    info1.append(self.disturbResult.item(row,5+i).text())
                info1.append(self.tb_proof.toPlainText())
                info1.append(Notxt[0][0])
                # 单位Info 当前选中装备Info 当前年份 [质量 此次分配合计数 各单位分配数 依据 陆军单号]
                self.rocketSchedule.getUnitIDList(currentUnit,self.currentEquipdict[self.disturbResult.currentRow()],self.currentYear,info1)
            else:
                self.rocketSchedule.getUnitIDList("", "",
                                                  "", "")
            self.rocketSchedule.setWindowFlags(Qt.Dialog|Qt.WindowCloseButtonHint)
            self.rocketSchedule.show()
            self.rocketSchedule.signal.connect(self.updateRocket)

    # 更新进度3 火箭军调拨
    def updateRocket(self):
        currentRow = self.disturbResult.currentRow()
        item = QPushButton("已完成")
        if self.unitFlag == 1:
            self.disturbResult.setCellWidget(currentRow, 7 + self.lenCurrentUnitChilddict, item)
            updateRocketScheduleUper(self.currentEquipdict[currentRow][0], self.currentYear)
            item.clicked.connect(self.showRocket)
        elif self.unitFlag == 2:
            self.disturbResult.setCellWidget(currentRow, 5 + self.lenCurrentUnitChilddict, item)
            updateRocketScheduleBase(self.currentEquipdict[currentRow][0], self.currentYear)
            item.clicked.connect(self.showRocket)

    def showRocket(self):
        row = self.disturbResult.currentRow()
        currentColumn = self.disturbResult.currentColumn()
        ShowRocket = transferModel()
        if row < 0 or currentColumn < 0:
            return
        if currentColumn - 1 < 0:
            return
        # if self.unitFlag == 1:
        #     if self.disturbResult.cellWidget(row, currentColumn - 1).text() == "设置进度":
        #         QMessageBox.information(self, "设置接装条件", "上一级未完成", QMessageBox.Yes)
        #         return
        currentUnit = []
        for i in self.currentUnitChilddict.values():
            currentUnit.append(i)
        if row != -1:
            # 存放质量和陆军单号
            QuaTxt = selectRocketQua(self.currentEquipdict[row][0], self.currentYear)
            txt = selectContractSchedule(self.currentEquipdict[row][0], self.currentYear)
            if txt[0][0] != '':
                info1 = [QuaTxt[0][0], self.disturbResult.item(row, 4).text()]
                for i in range(0, self.lenCurrentUnitChilddict):
                    info1.append(self.disturbResult.item(row, 5 + i).text())
                info1.append(self.tb_proof.toPlainText())
                info1.append(txt[0][0])
                ShowRocket.getUnitIDList(currentUnit, self.currentEquipdict[self.disturbResult.currentRow()],
                                                  self.currentYear, info1)
            else:
                ShowRocket.getUnitIDList("", "", "", "")
            ShowRocket.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
            ShowRocket.pb_output.setDisabled(1)
            ShowRocket.pb_input.setDisabled(1)
            ShowRocket.pb_confirm.setDisabled(1)
            ShowRocket.pb_saveSingle.setDisabled(1)
            ShowRocket.pb_saveTotal.setDisabled(1)
            # ShowRocket.tw_transferModel.set
            #ShowRocket.setDisabled(1)
            ShowRocket.show()
            ShowRocket.exec_()

    # 进度4 是否完成
    def setScheduleFinish(self):
        currentRow = self.disturbResult.currentRow()
        currentColumn = self.disturbResult.currentColumn()
        if currentRow < 0 or currentColumn < 0:
            return
        if currentColumn - 1 < 0:
            return
        if self.disturbResult.cellWidget(currentRow, currentColumn - 1).text() == "设置进度":
            getMessageBox("设置接装条件", "上一级未完成", True, False)
            return
        self.scheduleFinish.setWindowFlags(Qt.Dialog|Qt.WindowCloseButtonHint)
        self.scheduleFinish.fileName = ""
        self.scheduleFinish.initDict(self.currentUnitChilddict,
                                     self.currentEquipdict[currentRow][0], self.currentYear, self.unitFlag)
        self.scheduleFinish.init1()
        self.scheduleFinish.show()
        self.scheduleFinish.signal.connect(self.updateFinish)

    # 更新进度4 是否完成
    def updateFinish(self):
        currentRow = self.disturbResult.currentRow()
        fileName, file, fileWay = self.scheduleFinish.returnFileName()
        print("fileName", fileName)
        if fileName != "":
            item = QPushButton("已完成")
            if self.unitFlag == 1:
                self.disturbResult.setCellWidget(currentRow, 8 + self.lenCurrentUnitChilddict, item)
                updateIfScheduleFinishUper(self.currentEquipdict[currentRow][0], self.currentYear)
            elif self.unitFlag == 2:
                self.disturbResult.setCellWidget(currentRow, 7 + self.lenCurrentUnitChilddict, item)
                updateIfScheduleFinishBase(self.currentEquipdict[currentRow][0], self.currentYear)


    # 筛选调拨进度
    def selectSchedule(self):
        if self.unitFlag == 1:
            index = self.cb_schedule.currentIndex()
            # 未选择状态
            if index == 0:
                self._initDisturbPlanByUnitListAndEquipList(self.originalEquipDict,self.originalEquipDictTab)

            # 完成进度一
            elif index == 1:
                equipDict={}
                equipDictTab = {}
                j = 0
                for equipID, equipItem in self.second_treeWidget_dict.items():
                    flag1 = selectContractSchedule(equipID, self.currentYear)
                    if flag1[0][0] != '0':
                        if equipItem.checkState(0) == Qt.Checked:
                            equipInfo = findEquipInfo(equipID)
                            equipDict[j] = equipInfo[0]
                            equipInfo = self.addTab(equipInfo)
                            equipDictTab[j] = equipInfo[0]
                            j = j + 1
                        elif equipItem.checkState(0) == Qt.PartiallyChecked:
                            equipInfo = findEquipInfo(equipID)
                            equipDict[j] = equipInfo[0]
                            equipInfo = self.addTab(equipInfo)
                            equipDictTab[j] = equipInfo[0]
                            j = j + 1
                self._initDisturbPlanByUnitListAndEquipList(equipDict,equipDictTab)

            # 完成进度二
            elif index == 2:
                equipDict = {}
                equipDictTab = {}
                j = 0
                for equipID, equipItem in self.second_treeWidget_dict.items():
                    flag2 = selectAllotConditionUper(equipID, self.currentYear)
                    if int(flag2[0][0]):
                        if equipItem.checkState(0) == Qt.Checked:
                            equipInfo = findEquipInfo(equipID)
                            equipDict[j] = equipInfo[0]
                            equipInfo = self.addTab(equipInfo)
                            equipDictTab[j] = equipInfo[0]
                            j = j + 1
                        elif equipItem.checkState(0) == Qt.PartiallyChecked:
                            equipInfo = findEquipInfo(equipID)
                            equipDict[j] = equipInfo[0]
                            equipInfo = self.addTab(equipInfo)
                            equipDictTab[j] = equipInfo[0]
                            j = j + 1
                self._initDisturbPlanByUnitListAndEquipList(equipDict,equipDictTab)

            # 完成进度三
            elif index == 3:
                equipDict = {}
                equipDictTab = {}
                j = 0
                for equipID, equipItem in self.second_treeWidget_dict.items():
                    flag3 = selectRocketScheduleUper(equipID, self.currentYear)
                    if int(flag3[0][0]):
                        if equipItem.checkState(0) == Qt.Checked:
                            equipInfo = findEquipInfo(equipID)
                            equipDict[j] = equipInfo[0]
                            equipInfo = self.addTab(equipInfo)
                            equipDictTab[j] = equipInfo[0]
                            j = j + 1
                        elif equipItem.checkState(0) == Qt.PartiallyChecked:
                            equipInfo = findEquipInfo(equipID)
                            equipDict[j] = equipInfo[0]
                            equipInfo = self.addTab(equipInfo)
                            equipDictTab[j] = equipInfo[0]
                            j = j + 1
                self._initDisturbPlanByUnitListAndEquipList(equipDict,equipDictTab)

            # 完成进度四
            elif index == 4:
                equipDict = {}
                equipDictTab = {}
                j = 0
                for equipID, equipItem in self.second_treeWidget_dict.items():
                    flag4 = selectIfScheduleFinishUper(equipID, self.currentYear)
                    if flag4[0][0] != 'FALSE':
                        if equipItem.checkState(0) == Qt.Checked:
                            equipInfo = findEquipInfo(equipID)
                            equipDict[j] = equipInfo[0]
                            equipInfo = self.addTab(equipInfo)
                            equipDictTab[j] = equipInfo[0]
                            j = j + 1
                        elif equipItem.checkState(0) == Qt.PartiallyChecked:
                            equipInfo = findEquipInfo(equipID)
                            equipDict[j] = equipInfo[0]
                            equipInfo = self.addTab(equipInfo)
                            equipDictTab[j] = equipInfo[0]
                            j = j + 1
                self._initDisturbPlanByUnitListAndEquipList(equipDict,equipDictTab)
        elif self.unitFlag == 2:
            index = self.cb_schedule.currentIndex()
            # 未选择状态
            if index == 0:
                self._initDisturbPlanByUnitListAndEquipList(self.originalEquipDict,self.originalEquipDictTab)
            # 完成进度二
            elif index == 2:
                equipDict = {}
                equipDictTab = {}
                j = 0
                for equipID, equipItem in self.second_treeWidget_dict.items():
                    flag2 = selectAllotConditionBase(equipID, self.currentYear)
                    if int(flag2[0][0]):
                        if equipItem.checkState(0) == Qt.Checked:
                            equipInfo = findEquipInfo(equipID)
                            equipDict[j] = equipInfo[0]
                            equipInfo = self.addTab(equipInfo)
                            equipDictTab[j] = equipInfo[0]
                            j = j + 1
                        elif equipItem.checkState(0) == Qt.PartiallyChecked:
                            equipInfo = findEquipInfo(equipID)
                            equipDict[j] = equipInfo[0]
                            equipInfo = self.addTab(equipInfo)
                            equipDictTab[j] = equipInfo[0]
                            j = j + 1
                self._initDisturbPlanByUnitListAndEquipList(equipDict,equipDictTab)

            # 完成进度一
            elif index == 1:
                equipDict = {}
                equipDictTab = {}
                j = 0
                for equipID, equipItem in self.second_treeWidget_dict.items():
                    flag3 = selectRocketScheduleBase(equipID, self.currentYear)
                    if int(flag3[0][0]):
                        if equipItem.checkState(0) == Qt.Checked:
                            equipInfo = findEquipInfo(equipID)
                            equipDict[j] = equipInfo[0]
                            equipInfo = self.addTab(equipInfo)
                            equipDictTab[j] = equipInfo[0]
                            j = j + 1
                        elif equipItem.checkState(0) == Qt.PartiallyChecked:
                            equipInfo = findEquipInfo(equipID)
                            equipDict[j] = equipInfo[0]
                            equipInfo = self.addTab(equipInfo)
                            equipDictTab[j] = equipInfo[0]
                            j = j + 1
                self._initDisturbPlanByUnitListAndEquipList(equipDict,equipDictTab)

            # 完成进度三
            elif index == 3:
                equipDict = {}
                equipDictTab = {}
                j = 0
                for equipID, equipItem in self.second_treeWidget_dict.items():
                    flag4 = selectIfScheduleFinishBase(equipID, self.currentYear)
                    if flag4[0][0] != 'FALSE':
                        if equipItem.checkState(0) == Qt.Checked:
                            equipInfo = findEquipInfo(equipID)
                            equipDict[j] = equipInfo[0]
                            equipInfo = self.addTab(equipInfo)
                            equipDictTab[j] = equipInfo[0]
                            j = j + 1
                        elif equipItem.checkState(0) == Qt.PartiallyChecked:
                            equipInfo = findEquipInfo(equipID)
                            equipDict[j] = equipInfo[0]
                            equipInfo = self.addTab(equipInfo)
                            equipDictTab[j] = equipInfo[0]
                            j = j + 1
                self._initDisturbPlanByUnitListAndEquipList(equipDict,equipDictTab)
