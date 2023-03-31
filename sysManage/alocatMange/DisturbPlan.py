import sys
import pickle
from PyQt5.QtWidgets import *
# new
from database.SD_EquipmentBanlanceSql import updateOneEquipmentBalanceData, deleteByYear
from sysManage.component import getIntInputDialog, getMessageBox
from widgets.alocatMange.yearListForm import yearList_Form
from database.strengthDisturbSql import *
from PyQt5.Qt import Qt, QRegExpValidator, QRegExp
from PyQt5.QtGui import QColor, QBrush, QFont
from database.alocatMangeSql import *
from sysManage.userInfo import get_value
from sysManage.alocatMange.InputProof_Disturb import InputProof
from sysManage.showInputResult import showInputResult
from PyQt5.QtCore import QDateTime
from utills.Search import selectUnit

'''
    分配调整计划
'''


class DisturbPlan(QWidget, yearList_Form):
    def __init__(self, parent=None):
        super(DisturbPlan, self).__init__(parent)
        # Stren_Inquiry._initUnitTreeWidget()
        self.setupUi(self)
        self.initAll()
        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}
        self.unitDisturbPlanList = {}
        self.unitFlag = 0
        self.inputProof = InputProof()
        self.signalConnect()

    def initAll(self):
        self.pb_firstSelect.setDisabled(1)
        self.pb_secondSelect.setDisabled(1)
        self.tw_first.header().setVisible(False)
        self.tw_second.header().setVisible(False)
        self.le_first.setDisabled(1)
        self.le_second.setDisabled(1)
        self.tw_first.setDisabled(1)
        self.tw_second.setDisabled(1)
        self.pb_proof.setDisabled(1)
        self.tw_first.clear()
        self.tw_second.clear()
        self.tb_proof.clear()
        self.txt_disturbPlanYear.clear()
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
        # 新增年份
        self.tb_add.clicked.connect(self.slotAddNewYear)
        # 删除年份
        self.tb_del.clicked.connect(self.slotDelYear)
        # 修改分配数与备注
        self.disturbResult.itemChanged.connect(self.slotItemChange)
        # 修改调拨依据
        self.pb_proof.clicked.connect(self.slotProofChange)
        self.pb_firstSelect.clicked.connect(self.slotSelectUnit)
        self.pb_secondSelect.clicked.connect(self.slotSelectEquip)
        self.inputProof.signal.connect(self.initDisturbPlanProof)
        self.pb_outputToExcel.clicked.connect(self.slotOutputToExcel)
        self.pb_input.clicked.connect(self.slotInputData)
        self.pb_output.clicked.connect(self.slotOutputData)
        # self.showInputResult.pb_confirm.clicked.connect(self.slotInputIntoDatabase)
        # self.showInputResult.pb_cancel.clicked.connect(self.slotCancelInputIntoDatabase)

    # 查询单位
    def slotSelectUnit(self):
        selectUnit(self, self.le_first, self.first_treeWidget_dict, self.tw_first)


    # 查询装备
    def slotSelectEquip(self):
        selectUnit(self, self.le_second, self.second_treeWidget_dict, self.tw_second)



    # 信号与槽连接的断开
    def signalDisconnectSlot(self):
        # 点击选择年份后刷新页面 初始化
        self.lw_yearChoose.itemClicked.disconnect(self.slotClickedInqury)
        self.lw_yearChoose.itemClicked.disconnect(self.setDisturbPlanTitle)
        self.lw_yearChoose.itemClicked.disconnect(self.initDisturbPlanProof)

        # 点击第一目录结果
        self.tw_first.itemClicked.disconnect(self.slotDisturbStrengthResult)

        self.tw_second.itemChanged.disconnect(self.slotCheckedChange)

        # 点击第二目录结果
        self.tw_second.itemClicked.disconnect(self.slotDisturbStrengthResult)
        # 新增年份
        self.tb_add.clicked.disconnect(self.slotAddNewYear)
        # 删除年份
        self.tb_del.clicked.disconnect(self.slotDelYear)
        # 修改分配数与备注
        self.disturbResult.itemChanged.disconnect(self.slotItemChange)
        # 修改调拨依据
        self.pb_proof.clicked.disconnect(self.slotProofChange)

        self.pb_firstSelect.clicked.disconnect(self.slotSelectUnit)

        self.pb_secondSelect.clicked.disconnect(self.slotSelectEquip)

        self.inputProof.signal.disconnect(self.initDisturbPlanProof)

    # 新增年份
    def slotAddNewYear(self):
        year = 0
        ok, year = getIntInputDialog("新增年份", "年份:", 0, 100000, 1, True, True)
        if ok:
            haveYear = False
            allyear = selectYearListAboutDisturbPlan()
            for yearInfo in allyear:
                if str(year) == yearInfo:
                    haveYear = True
            if haveYear == True:
                getMessageBox('添加', '添加失败，该年份已存在', True, False)
                return

            insertIntoDisturbPlanYear(year)
            if not selectIfExistsStrengthYear(year):
                insertIntoStrengthYear(year)
            self._initYearWidget_()
            return

    # 删除年份
    def slotDelYear(self):
        reply = getMessageBox("删除", "是否删除该年份及其数据？", True, False)
        if reply == QMessageBox.Ok:
            currentYear = self.lw_yearChoose.currentItem()
            # print("currentYear.text()",currentYear.text())
            deleteDisturbPlanYear(currentYear.text())
            deleteByYear(currentYear.text())
            delStrengthYearByYear(currentYear.text())
            self._initYearWidget_()

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

    # 点击年份后 初始化装备与单位列表
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
        self.pb_proof.setDisabled(0)
        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}
        self.pb_firstSelect.setDisabled(0)
        self.pb_secondSelect.setDisabled(0)
        self.currentYear = self.lw_yearChoose.currentItem().text()
        # startEquipIDInfo = findUperEquipIDByName("通用装备")
        startInfo = selectDisturbPlanUnitInfoByUnitID(self.userInfo[0][4])
        stack = []
        root = []
        if startInfo:
            stack.append(startInfo)
            root.append(self.tw_first)
            self._initUnitTreeWidget(stack, root)

        # equipInfo = 通用装备一行的所有信息
        equipInfo = findUperEquipIDByName("通用装备")
        stack = []
        root = []
        if equipInfo:
            # stack 传入 通用装备ID
            stack.append(equipInfo[0])
            root.append(self.tw_second)
            self._initEquipTreeWidget(stack, root,0)

    def initUserInfo(self):
        self.userInfo = get_value("totleUserInfo")

    def _initUnitTreeWidget(self, stack, root):
        while stack:
            UnitInfo = stack.pop(0)
            item = QTreeWidgetItem(root.pop(0))
            item.setText(0, UnitInfo[1])
            # item.setCheckState(0, Qt.Unchecked)
            self.first_treeWidget_dict[UnitInfo[0]] = item
            result = selectDisturbPlanUnitInfoByDeptUper(UnitInfo[0])
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
                self._initEquipTreeWidget(stack,root,count+1)
        # print("first_treeWidget_dict", self.first_treeWidget_dict)

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


    '''
        查询结果
    '''
    def slotDisturbStrengthResult(self):
        self.yearList = []
        # self.currentEquipdict.clear()
        self.currentEquipdict = {}
        self.currentEquipdictTab = {}
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
        print("self.currentUnitChilddict", self.currentUnitChilddict)
        # 获取当前装备名
        j = 0
        for equipID, equipItem in self.second_treeWidget_dict.items():
            if equipItem.checkState(0) == Qt.Checked:
                equipInfo = findEquipInfo(equipID)
                self.currentEquipdict[j] = equipInfo[0]
                equipInfo = self.addTab(equipInfo)
                self.currentEquipdictTab[j] = equipInfo[0]
                j = j + 1
            elif equipItem.checkState(0) == Qt.PartiallyChecked:
                equipInfo = findEquipInfo(equipID)
                self.currentEquipdict[j] = equipInfo[0]
                equipInfo = self.addTab(equipInfo)
                self.currentEquipdictTab[j] = equipInfo[0]
                j = j + 1
        print("self.currentEquipdict", self.currentEquipdict)
        self._initDisturbPlanByUnitListAndEquipList()

    '''
        初始化分配计划结果
    '''
    def _initDisturbPlanByUnitListAndEquipList(self):
        self.disturbResult.clear()
        self.disturbResult.setRowCount(0)
        self.lenCurrentUnitChilddict = len(self.currentUnitChilddict)   # 选择单位个数
        self.lenCurrentEquipdict = len(self.currentEquipdict)   # 选择装备个数
        # 选择机关或其他
        if self.unitFlag == 1:
            headerlist = ['装备名称及规格型号', '单位', '陆军调拨单开具数', '机关分配计划数', '此次分配合计数']
            if len(self.currentUnitChilddict):
                for i in self.currentUnitChilddict.values():
                    headerlist.append(i[1])
            headerlist.append('备注')
            self.lenHeaderList = len(headerlist)
            self.disturbResult.setColumnCount(self.lenHeaderList)
            self.disturbResult.setRowCount(len(self.currentEquipdict))
            self.disturbResult.setHorizontalHeaderLabels(headerlist)
            self.disturbResult.setColumnWidth(0, 200)
            i = 0
            for LineInfo in self.currentEquipdictTab.values():
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
                self.disturbResult.setItem(i, 5 + self.lenCurrentUnitChilddict, item)
                currentRowResult.append(item)
                i = i + 1
        # 选择各基地
        elif self.unitFlag == 2:
            headerlist = ['装备名称及规格型号', '单位', '火箭军调拨单开具数', '此次机关分配数', '此次分配合计数']
            if len(self.currentUnitChilddict):
                for i in self.currentUnitChilddict.values():
                    headerlist.append(i[1])
            headerlist.append('备注')
            self.lenHeaderList = len(headerlist)
            self.disturbResult.setColumnCount(self.lenHeaderList)
            self.disturbResult.setRowCount(len(self.currentEquipdict))
            self.disturbResult.setHorizontalHeaderLabels(headerlist)
            self.disturbResult.setColumnWidth(0, 200)
            i = 0
            for LineInfo in self.currentEquipdictTab.values():
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
                self.disturbResult.setItem(i, 5 + self.lenCurrentUnitChilddict, item)
                currentRowResult.append(item)
                i = i + 1
        self.disturbResult.setColumnWidth(2, 150)
        if self.currentEquipdict and self.currentUnitChilddict:
            self.initDisturbPlanNum()
            self.initDisturbPlanNote()
            self.initDisturbPlanInputNum()
            self.initDisturbPlanOther()
            self.ifEquipHaveChild()

    # 初始化调拨依据
    def initDisturbPlanProof(self):
        proof = selectDisturbPlanProof(self.currentYear)
        self.tb_proof.setText(proof[0][0])

    # 改变调拨依据
    def slotProofChange(self):
        self.inputProof.setYear(self.currentYear)
        self.inputProof.show()

    # 读取初始分配计划数
    def initDisturbPlanNum(self):
        print("currentYear:", self.currentYear)
        self.unitDisturbPlanList = selectDisturbPlanNumByList(self.currentUnitChilddict,
                                                              self.currentEquipdict, self.currentYear)
        print("self.unitDisturbPlanList", self.unitDisturbPlanList)
        # 显示每个单位分配计划数
        num = 0
        for i in range(0, len(self.currentUnitChilddict)):
            for j in range(0, len(self.currentEquipdict)):
                item = self.disturbResult.item(j, 5 + i)
                # print("self.unitDisturbPlanList",self.unitDisturbPlanList,"num",num)
                if self.unitDisturbPlanList[num] != '':
                    item.setText(self.unitDisturbPlanList[num])
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
                num = num + 1
        self.initDisturbPlanSum()
        self.updateDisturbPlanSumEachUnit()

    # 初始化此次分配数
    def initDisturbPlanSum(self):
        # 显示此次分配计划数
        # if flag1 == '1':
        sum = 0
        for i in self.currentEquipdict:
            if not selectEquipIsHaveChild(self.currentEquipdict[i][0]):
                for j in range(0, len(self.currentUnitChilddict)):
                    num = self.disturbResult.item(i, 5 + j).text()
                    if num == '':
                        sum = sum + 0
                    else:
                        sum = sum + int(num)
                if sum!=0:
                    self.disturbResult.item(i, 4).setText(str(sum))
            sum = 0
        # 此次分配数的上层装备合计数
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
    def updateDisturbPlanSumEachUnit(self):
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

    # 若装备含子装备，则该行不可选中
    def ifEquipHaveChild(self):
        for i in self.currentEquipdict:
            if selectEquipIsHaveChild(self.currentEquipdict[i][0]):
                for j in range(1, self.disturbResult.columnCount()):
                    item = self.disturbResult.item(i, j)
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

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
        改变 分配计划数、备注、自定义计划数
    '''
    def slotItemChange(self):
        self.currentRow = self.disturbResult.currentRow()
        self.currentColumn = self.disturbResult.currentColumn()
        if 5 <= self.currentColumn <= self.lenHeaderList - 2:
            try:
                num = self.disturbResult.item(self.currentRow, self.currentColumn).text()
                # self.initDisturbPlanSum()
                # self.updateDisturbPlanSumEachUnit()
                originDisturbPlanNum = selectDisturbPlanNumByList({0: self.currentUnitChilddict[self.currentColumn - 5]},
                                                                  {0: self.currentEquipdict[self.currentRow]},
                                                                  self.currentYear)
                originStrengthNum = selectStrengthNum(self.currentUnitChilddict[self.currentColumn - 5][0],
                                                      self.currentEquipdict[self.currentRow][0], self.currentYear)
                print("originDisturbPlanNum", originDisturbPlanNum, "originStrengthNum", originStrengthNum)
                if originDisturbPlanNum[0] != '' and len(originStrengthNum) > 0 and originStrengthNum[0] != '' and originStrengthNum[0] != 0:
                    updateDisturbPlanNum(self.currentEquipdict[self.currentRow][0],
                                         self.currentUnitChilddict[self.currentColumn - 5][0],
                                         self.currentYear, num, originDisturbPlanNum[0])
                    updateOneEquipmentBalanceData(self.currentYear, self.currentEquipdict[self.currentRow][0],
                                                  self.currentUnitChilddict[self.currentColumn - 5][0])
                    self.initDisturbPlanSum()
                    self.updateDisturbPlanSumEachUnit()
                else:
                    getMessageBox("提示", "未填写实力数", True, False)
                    self._initDisturbPlanByUnitListAndEquipList()
                    # self.disturbResult.item(self.currentRow, self.currentColumn).setText("")
            except ValueError:
                getMessageBox("提示", "请输入数字", True, False)
                self._initDisturbPlanByUnitListAndEquipList()
            except IndexError:
                getMessageBox("提示", "操作有误", True, False)
                self._initDisturbPlanByUnitListAndEquipList()


        # 备注
        if self.currentColumn == self.lenHeaderList - 1:
            updateDisturbPlanNote(self.currentEquipdict[self.currentRow][0], self.currentYear,
                                  self.disturbResult.item(self.currentRow, self.currentColumn).text())

        # 自定义计划数
        if self.currentColumn == 3:
            if self.disturbResult.item(self.currentRow, self.currentColumn).text() == '':
                num = 0
            else:
                num = self.disturbResult.item(self.currentRow, self.currentColumn).text()
            if self.unitFlag == 1:
                updateDisturbPlanInputNumUpmost(self.currentEquipdict[self.currentRow][0], self.currentYear, num)
            elif self.unitFlag == 2:
                updateDisturbPlanInputNumBase(self.currentEquipdict[self.currentRow][0], self.currentYear, num)

    # 初始化分配计划年份
    def setDisturbPlanTitle(self):
        txt = str(self.currentYear) + "年分配计划"
        self.txt_disturbPlanYear.setFont(QFont("Microsoft YaHei"))
        self.txt_disturbPlanYear.setAlignment(Qt.AlignCenter)
        self.txt_disturbPlanYear.setTextInteractionFlags(Qt.NoTextInteraction)
        self.txt_disturbPlanYear.setFontPointSize(15)
        self.txt_disturbPlanYear.setText(txt)

    # 初始化自定义计划数
    def initDisturbPlanInputNum(self):
        if self.unitFlag == 1:
            unitDisturbPlanInputNumList = selectDisturbPlanInputNumUpmost(self.currentEquipdict, self.currentYear)
            for i in range(0, len(self.currentEquipdict)):
                item = self.disturbResult.item(i, 3)
                if unitDisturbPlanInputNumList[i] is not None:
                    item.setText(str(unitDisturbPlanInputNumList[i]))
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
        elif self.unitFlag == 2:
            unitDisturbPlanInputNumList = selectDisturbPlanInputNumBase(self.currentEquipdict, self.currentYear)
            for i in range(0, len(self.currentEquipdict)):
                item = self.disturbResult.item(i, 3)
                if unitDisturbPlanInputNumList[i] is not None:
                    item.setText(str(unitDisturbPlanInputNumList[i]))
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)


    # 读取初始分配计划备注
    def initDisturbPlanNote(self):
        self.unitDisturbPlanNoteList = selectDisturbPlanNote(self.currentEquipdict, self.currentYear)

        for i in range(0, len(self.currentEquipdict)):
            item = self.disturbResult.item(i, self.lenHeaderList - 1)
            if self.unitDisturbPlanNoteList[i] is not None:
                item.setText(str(self.unitDisturbPlanNoteList[i]))
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)


    # 读取调拨单开具数计划数与装备单位
    def initDisturbPlanOther(self):
        unitDisturbPlanOtherList = selectDisturbPlanOther(self.currentEquipdict, self.currentYear)
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
                        result = selectDisturbPlanNumByList({0: [unitID]}, self.currentEquipdict, self.currentYear)
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


    # 导出到Excel表格
    def slotOutputToExcel(self):
        self.disturbPlanList = {}
        if self.disturbResult.rowCount() <= 0:
            getMessageBox('警告', '未选中任何数据，无法导出',True, False)
            return
        reply = getMessageBox('修改导出Excel', '是否保存修改并导出Excel？',True, True)
        if reply == QMessageBox.Cancel:
            self._initDisturbPlanByUnitListAndEquipList()
            return

        directoryPath = QFileDialog.getExistingDirectory(self, "请选择导出文件夹", "c:/")
        if len(directoryPath) > 0 and '.' not in directoryPath:
            import xlwt
            workBook = xlwt.Workbook(encoding='utf-8')
            workSheet = workBook.add_sheet('Sheet1')

            headTitleStyle2 = xlwt.XFStyle()  # 初始化样式
            font = xlwt.Font()  # 为样式创建字体
            font.name = '宋体'
            font.bold = True
            font.height = 20 * 11  # 字体大小，11为字号，20为衡量单位
            alignment = xlwt.Alignment()  ## Create Alignment
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            alignment.vert = xlwt.Alignment.VERT_CENTER
            borders = xlwt.Borders()
            borders.left = 1  # 设置为细实线
            borders.right = 1
            borders.top = 1
            borders.bottom = 1
            headTitleStyle2.font = font  # 设定样式
            headTitleStyle2.alignment = alignment
            headTitleStyle2.borders = borders

            headTitleStyle = xlwt.XFStyle()  # 初始化样式
            font = xlwt.Font()  # 为样式创建字体
            font.name = '宋体'
            font.bold = True
            font.height = 20 * 20  # 字体大小，11为字号，20为衡量单位
            alignment = xlwt.Alignment()  ## Create Alignment
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            alignment.vert = xlwt.Alignment.VERT_CENTER
            borders = xlwt.Borders()
            borders.left = 3  # 设置为细实线
            borders.right = 3
            borders.top = 3
            borders.bottom = 3
            headTitleStyle.font = font  # 设定样式
            headTitleStyle.alignment = alignment
            headTitleStyle.borders = borders

            titileStyle = xlwt.XFStyle()  # 初始化样式
            font = xlwt.Font()  # 为样式创建字体
            font.name = '宋体'
            font.bold = True
            font.height = 20 * 11  # 字体大小，11为字号，20为衡量单位
            alignment = xlwt.Alignment()  ## Create Alignment
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            alignment.vert = xlwt.Alignment.VERT_CENTER
            borders = xlwt.Borders()
            borders.left = 2  # 设置为细实线
            borders.right = 2
            borders.top = 2
            borders.bottom = 2
            titileStyle.font = font  # 设定样式
            titileStyle.alignment = alignment
            titileStyle.borders = borders
            contentStyle = xlwt.XFStyle()  # 初始化样式
            font = xlwt.Font()  # 为样式创建字体
            font.name = '宋体'
            font.height = 20 * 11  # 字体大小，11为字号，20为衡量单位
            alignment = xlwt.Alignment()  ## Create Alignment
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            alignment.vert = xlwt.Alignment.VERT_CENTER
            borders = xlwt.Borders()
            borders.left = 1  # 设置为细实线
            borders.right = 1
            borders.top = 1
            borders.bottom = 1
            contentStyle.font = font  # 设定样式
            contentStyle.alignment = alignment
            contentStyle.borders = borders

            # 画Excel表头
            if self.unitFlag == 1:
                headerlist = ['装备名称及规格型号', '单位', '陆军调拨单开具数', '机关分配计划数', '此次分配合计数']
                if len(self.currentUnitChilddict):
                    for i in self.currentUnitChilddict.values():
                        headerlist.append(i[1])
                headerlist.append('备注')
            elif self.unitFlag == 2:
                headerlist = ['装备名称及规格型号', '单位', '火箭军调拨单开具数', '此次机关分配数', '此次分配合计数']
                if len(self.currentUnitChilddict):
                    for i in self.currentUnitChilddict.values():
                        headerlist.append(i[1])
                headerlist.append('备注')
            for i in range(len(headerlist)):
                workSheet.col(i).width = 5500
            workSheet.write_merge(0, 0, 0, len(headerlist) - 1, "%s年分配调整计划" % (self.currentYear), headTitleStyle)
            proof = selectDisturbPlanProof(self.currentYear)
            proofText = proof[0][0]
            workSheet.write_merge(1, 1, 0, len(headerlist) - 1, proofText, headTitleStyle2)
            # 画表头
            for i in range(len(headerlist)):
                workSheet.write(2, i, headerlist[i], titileStyle)
            # 获取表数据
            for i in range(self.disturbResult.rowCount()):
                columnList = []
                for j in range(self.disturbResult.columnCount()):
                    columnList.append(self.disturbResult.item(i, j).text())
                self.disturbPlanList[i] = columnList
            # 填表
            for key in self.disturbPlanList.keys():
                for index in range(len(headerlist)):
                    rowData = self.disturbPlanList.get(key)
                    workSheet.write(3 + key, index, rowData[index], contentStyle)
            try:
                pathName = "%s/%s年通用装备分配调整计划.xls" % (directoryPath, self.currentYear)
                workBook.save(pathName)
                import win32api
                win32api.ShellExecute(0, 'open', pathName, '', '', 1)
                getMessageBox("导出成功", "导出成功！", True, False)
                return
            except Exception as e:
                getMessageBox("导出失败", "导出表格被占用，请关闭正在使用的Execl！", True, False)
                return
        else:
            getMessageBox("选取文件夹失败！", "请选择正确的文件夹！", True, False)


    # 导出分配调整计划数据
    def slotOutputData(self):
        self.disturbPlanList = {}
        if self.disturbResult.rowCount() <= 0:
            getMessageBox('警告', '未选中任何数据，无法导出',True, False)
            return
        reply = getMessageBox('导出数据包', '是否导出数据包？', True, True)
        if reply == QMessageBox.Cancel:
            self._initDisturbPlanByUnitListAndEquipList()
            return
        self.disturbPlanList["currentUnit"] = self.currentUnitChilddict
        self.disturbPlanList["currentYear"] = self.currentYear
        self.disturbPlanList["currentEquip"] = self.currentEquipdict
        self.disturbPlanList["disturbPlanListFlag"]="分配调整计划数据"
        self.disturbPlanList["unitFlag"]=self.unitFlag
        # 获取表数据
        for i,equipInfo in self.currentEquipdict.items():
            inputNum = self.disturbResult.item(i, 3).text()
            note = self.disturbResult.item(i, 5+self.lenCurrentUnitChilddict).text()
            numList = []
            for unitInfo in self.currentUnitChilddict.values():
                numList.append(selectDisturbPlanNum(unitInfo[0],equipInfo[0],self.currentYear))
            self.disturbPlanList[i] = (equipInfo[0], equipInfo[1], equipInfo[5],inputNum,note,tuple(numList))

        directoryPath = QFileDialog.getExistingDirectory(self, "请选择导出文件夹", "c:/")
        if len(directoryPath) > 0:
            print("导出数据包dataList",self.disturbPlanList)  # ['实力查询数据'， ['5', '10', 'A车', '六十一旅团一阵地', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '2000']]
            if self.disturbPlanList is None or len(self.disturbPlanList) == 1:
                return
            else:
                date = QDateTime.currentDateTime()
                installData = date.toString("yyyy年MM月dd日hh时mm分ss秒")  # hh:mm:ss
                pathName = "%s/%s分配调整计划.nms" % (directoryPath, installData)
                with open(pathName, "wb") as file:
                    pickle.dump(self.disturbPlanList, file)
                getMessageBox("导出成功", "导出成功！", True, False)
        else:
            getMessageBox("导出数据失败！", "请选择正确的文件夹！", True, False)



    # 导入分配调整计划数据
    def slotInputData(self):
        self.inputDict = {}
        filename, _ = QFileDialog.getOpenFileName(self, "选中文件", '', "Excel Files (*.nms);;Excel Files (*.nms)")
        if len(filename) < 2:
            return
        try:
            # 拿到上述数据文件
            with open(filename, "rb") as file:
                self.inputDict = pickle.load(file)
                if self.inputDict["disturbPlanListFlag"] != "分配调整计划数据":
                    raise Exception("数据格式错误！")
        except Exception as e:
            print(e)
            getMessageBox("加载文件失败！", "请检查文件格式及内容格式！", True, False)
            return
        print("导入数据self.inputDict", self.inputDict)
        self.showInputResult = showInputResult(self)
        self.showInputResult.hide()
        headerlist = ['装备名称及规格型号', '单位', '机关分配计划数']
        self.showInputResult.setWindowTitle("导入数据")
        self.showInputResult.show()
        lenEquip = len(self.inputDict["currentEquip"])
        lenUnit = len(self.inputDict["currentUnit"])
        if lenUnit:
            for i in self.inputDict["currentUnit"].values():
                headerlist.append(i[1])
        headerlist.append('备注')
        # QTableWidget设置整行选中
        self.showInputResult.tw_result.setColumnCount(len(headerlist))
        self.showInputResult.tw_result.setHorizontalHeaderLabels(headerlist)
        self.showInputResult.tw_result.setRowCount(lenEquip)
        self.showInputResult.tw_result.setColumnWidth(0, 200)
        for i, LineInfo in self.inputDict.items():
            if not isinstance(i, int):
                continue
            item = QTableWidgetItem(LineInfo[1])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.showInputResult.tw_result.setItem(i, 0, item)
            item = QTableWidgetItem(LineInfo[2])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.showInputResult.tw_result.setItem(i, 1, item)
            item = QTableWidgetItem(LineInfo[3])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.showInputResult.tw_result.setItem(i, 2, item)
            for x in range(0, lenUnit):
                item = QTableWidgetItem(LineInfo[-1][x])
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.showInputResult.tw_result.setItem(i, x + 3, item)
            item = QTableWidgetItem(LineInfo[4])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.showInputResult.tw_result.setItem(i, 3 + lenUnit, item)
            i = i + 1
        self.showInputResult.tw_result.setColumnWidth(2, 150)

    def slotCancelInputIntoDatabase(self):
        self.showInputResult.hide()
        self.setDisabled(False)

    def slotInputIntoDatabase(self):
        for dataIndex, dataInfo in self.inputDict.items():
            if not (isinstance(i, int) and EquipNotHaveChild(self.inputDict["currentEquip"][dataIndex])):
                continue
            try:
                for unitIndex, unitInfo in self.inputDict["currentUnit"].items():
                    # insertOrUpdateOneDataIntoDisturbPlan(unitInfo, equipInfo, year, num)
                    insertOrUpdateOneDataIntoDisturbPlan(unitInfo,
                                                         self.inputDict["currentEquip"][dataIndex],
                                                         self.inputDict["currentYear"],
                                                         dataInfo[-1][unitIndex])
                    # insertOrUpdateOneDataIntoDisturbPlanNote(equipInfo, year, inputNum, note, unitFlag)
                    insertOrUpdateOneDataIntoDisturbPlanNote(self.inputDict["currentEquip"][dataIndex],
                                                             self.inputDict["currentYear"],
                                                             dataInfo[3],
                                                             dataInfo[4],
                                                             self.inputDict["unitFlag"])
            except Exception as e:
                print(e)
                getMessageBox("导入失败", "导入第%d数据失败！" % (i), True, False)
        self.showInputResult.hide()
        self.setDisabled(False)