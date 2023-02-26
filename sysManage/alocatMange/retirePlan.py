import sys
from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
from PyQt5.QtGui import QColor, QBrush, QFont

from sysManage.component import getIntInputDialog, getMessageBox
from widgets.alocatMange.retirePlan import retirePlan_Form
from sysManage.userInfo import get_value
from sysManage.alocatMange.InputProof_Retire import InputProof
from database.SD_EquipmentBanlanceSql import updateOneEquipmentBalanceData, deleteByYear
from database.alocatMangeSql import *
from utills.Search import selectUnit

'''
    退役报废计划
'''


class retirePlan(QWidget, retirePlan_Form):
    def __init__(self, parent=None):
        super(retirePlan, self).__init__(parent)
        self.setupUi(self)
        self.unitFlag = 0
        self.initAll()
        self.inputProof = InputProof()
        self.signalConnect()

    def initAll(self):
        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}
        # self.currentUnitDisturbPlanNum = {}
        self.unitRetirePlanList = {}
        self.tw_first.header().setVisible(False)
        self.tw_second.header().setVisible(False)
        self.le_first.setDisabled(1)
        self.le_second.setDisabled(1)
        self.tw_first.setDisabled(1)
        self.tw_second.setDisabled(1)
        self.tw_first.clear()
        self.tw_second.clear()
        self.txt_retirePlanYear.clear()
        self.retirePlanResult.clear()
        self._initYearWidget_()


    def signalConnect(self):
        # 点击选择年份后刷新页面 初始化，点击年份之后一共做了这两件事情
        self.lw_yearChoose.itemClicked.connect(self.slotClickedInqury)
        self.lw_yearChoose.itemClicked.connect(self.setRetirePlanTitle)
        # 点击第一目录结果
        self.tw_first.itemClicked.connect(self.slotRetireStrengthResult)
        self.tw_second.itemChanged.connect(self.slotCheckedChange)
        # 点击第二目录结果
        self.tw_second.itemClicked.connect(self.slotRetireStrengthResult)
        # 新增年份
        self.tb_add.clicked.connect(self.slotAddNewYear)
        # 删除年份
        self.tb_del.clicked.connect(self.slotDelYear)
        # 修改分配数与备注
        self.retirePlanResult.itemChanged.connect(self.slotItemChange)
        # 修改查询依据
        self.pb_firstSelect.clicked.connect(self.slotSelectUnit)
        self.pb_secondSelect.clicked.connect(self.slotSelectEquip)
        self.pb_outputToExcel.clicked.connect(self.slotOutputToExcel)

    def slotSelectUnit(self):
        selectUnit(self, self.le_first, self.first_treeWidget_dict, self.tw_first)


    def slotSelectEquip(self):
        selectUnit(self, self.le_second, self.second_treeWidget_dict, self.tw_second)


    # 信号与槽连接的断开
    def signalDisconnectSlot(self):
        # 点击选择年份后刷新页面 初始化
        self.lw_yearChoose.itemClicked.disconnect(self.slotClickedInqury)
        self.lw_yearChoose.itemClicked.disconnect(self.setRetirePlanTitle)

        # 点击第一目录结果
        self.tw_first.itemClicked.disconnect(self.slotRetireStrengthResult)

        self.tw_second.itemChanged.disconnect(self.slotCheckedChange)

        # 点击第二目录结果
        self.tw_second.itemClicked.disconnect(self.slotRetireStrengthResult)
        # 新增年份
        self.tb_add.clicked.disconnect(self.slotAddNewYear)
        # 删除年份
        self.tb_del.clicked.disconnect(self.slotDelYear)
        # 修改分配数与备注
        self.retirePlanResult.itemChanged.disconnect(self.slotItemChange)

        self.pb_firstSelect.clicked.disconnect(self.slotSelectUnit)

        self.pb_secondSelect.clicked.disconnect(self.slotSelectEquip)

    # 新增年份
    def slotAddNewYear(self):
        year = 0

        ok, year = getIntInputDialog("新增年份", "年份:", 0, 100000, 1, True, True)
        if ok:
            haveYear = False
            allyear = selectYearListAboutRetirePlan()
            for yearInfo in allyear:
                if str(year) == yearInfo:
                    haveYear = True
            if haveYear == True:
                getMessageBox('添加', '添加失败，该年份已存在', True, False)
                return

            insertIntoRetirePlanYear(year)
            self._initYearWidget_()
            return

    # 删除年份
    def slotDelYear(self):
        reply = getMessageBox("删除", "是否删除所选？",True, True)
        if reply == QMessageBox.Ok:
            currentYear = self.lw_yearChoose.currentItem()
            deleteRetirePlanYear(currentYear.text())
            deleteByYear(currentYear.text())
            self._initYearWidget_()

    # 初始化年份
    def _initYearWidget_(self):
        self.yearList = []
        self.currentYear = None
        self.lw_yearChoose.clear()
        allYear = selectYearListAboutRetirePlan()
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
        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}
        self.currentYear = self.lw_yearChoose.currentItem().text()

        startInfo = selectRetirePlanUnitInfoByUnitID(self.userInfo[0][4])
        stack = []
        root = []
        if startInfo:
            stack.append(startInfo)
            root.append(self.tw_first)
            self._initUnitTreeWidget(stack, root)

        equipInfo = findUperEquipIDByName("通用装备")
        stack = []
        root = []
        if equipInfo:
            stack.append(equipInfo[0])
            root.append(self.tw_second)
            self._initEquipTreeWidget(stack, root, 0)

    def initUserInfo(self):
        self.userInfo = get_value("totleUserInfo")

    def _initUnitTreeWidget(self, stack, root):
        while stack:
            UnitInfo = stack.pop(0)
            item = QTreeWidgetItem(root.pop(0))
            item.setText(0, UnitInfo[1])
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
                self._initEquipTreeWidget(stack, root, count + 1)

    '''
        查询结果
    '''

    def slotRetireStrengthResult(self):
        self.yearList = []
        self.currentEquipdict = {}
        self.currentEquipdictTab = {}
        self.currentUnitChilddict = {}
        self.unitFlag = 0
        self.retirePlanResult.clear()
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
        self._initRetirePlanByUnitListAndEquipList()


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
        初始化退役报废计划结果
    '''

    def _initRetirePlanByUnitListAndEquipList(self):
        self.retirePlanResult.clear()
        self.retirePlanResult.setRowCount(0)
        self.lenCurrentUnitChilddict = len(self.currentUnitChilddict)
        self.lenCurrentEquipdict = len(self.currentEquipdict)

        # 选择机关或其他
        if self.unitFlag == 1:
            headerlist = ['装备名称及规格型号', '单位', '退役报废合计数']
            if len(self.currentUnitChilddict):
                for i in self.currentUnitChilddict.values():
                    headerlist.append(i[1])
            headerlist.append('备注')
            self.lenHeaderList = len(headerlist)
            self.retirePlanResult.setColumnCount(self.lenHeaderList)
            self.retirePlanResult.setRowCount(len(self.currentEquipdict))
            self.retirePlanResult.setHorizontalHeaderLabels(headerlist)
            self.retirePlanResult.setColumnWidth(0, 200)
            i = 0
            for LineInfo in self.currentEquipdictTab.values():
                currentRowResult = []
                item = QTableWidgetItem(LineInfo[1])
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                currentRowResult.append(item)
                self.retirePlanResult.setItem(i, 0, item)
                item = QTableWidgetItem("")
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                currentRowResult.append(item)
                self.retirePlanResult.setItem(i, 1, item)
                item = QTableWidgetItem("")
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                currentRowResult.append(item)
                self.retirePlanResult.setItem(i, 2, item)
                # item = QTableWidgetItem("")
                # item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                # currentRowResult.append(item)
                # self.retirePlanResult.setItem(i, 3, item)
                for x in range(0, self.lenCurrentUnitChilddict):
                    item = QTableWidgetItem("")
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    self.retirePlanResult.setItem(i, x + 3, item)
                    currentRowResult.append(item)
                item = QTableWidgetItem("")
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.retirePlanResult.setItem(i, 3 + self.lenCurrentUnitChilddict, item)
                currentRowResult.append(item)
                i = i + 1
        # 选择各基地
        elif self.unitFlag == 2:
            headerlist = ['装备名称及规格型号', '单位', '退役报废合计数']
            if len(self.currentUnitChilddict):
                for i in self.currentUnitChilddict.values():
                    headerlist.append(i[1])
            headerlist.append('备注')
            self.lenHeaderList = len(headerlist)
            self.retirePlanResult.setColumnCount(self.lenHeaderList)
            self.retirePlanResult.setRowCount(len(self.currentEquipdict))
            self.retirePlanResult.setHorizontalHeaderLabels(headerlist)
            self.retirePlanResult.setColumnWidth(0, 200)
            i = 0
            for LineInfo in self.currentEquipdictTab.values():
                currentRowResult = []
                item = QTableWidgetItem(LineInfo[1])
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                currentRowResult.append(item)
                self.retirePlanResult.setItem(i, 0, item)
                item = QTableWidgetItem("")
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                currentRowResult.append(item)
                self.retirePlanResult.setItem(i, 1, item)
                item = QTableWidgetItem("")
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                currentRowResult.append(item)
                self.retirePlanResult.setItem(i, 2, item)
                for x in range(0, self.lenCurrentUnitChilddict):
                    item = QTableWidgetItem("")
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    self.retirePlanResult.setItem(i, x + 3, item)
                    currentRowResult.append(item)
                item = QTableWidgetItem("")
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.retirePlanResult.setItem(i, 3 + self.lenCurrentUnitChilddict, item)
                currentRowResult.append(item)
                i = i + 1
        self.retirePlanResult.setColumnWidth(2, 150)
        if self.currentEquipdict and self.currentUnitChilddict:
            self.initRetirePlanNum()
            self.initRetirePlanNote()
            self.initRetirePlanOther()
            self.ifEquipHaveChild()

    # 读取初始退役计划数
    def initRetirePlanNum(self):

        self.unitRetirePlanList = selectRetirePlanNumByList(self.currentUnitChilddict,
                                                            self.currentEquipdict, self.currentYear)
        # print("self.unitRetirePlanList", self.unitRetirePlanList)
        # 显示每个单位分配计划数
        num = 0
        for i in range(0, len(self.currentUnitChilddict)):
            for j in range(0, len(self.currentEquipdict)):
                item = self.retirePlanResult.item(j, 3 + i)
                if self.unitRetirePlanList[num] != '':
                    item.setText(self.unitRetirePlanList[num])
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)
                num = num + 1
        self.initRetirePlanSum()

    # 初始化此次分配数
    def initRetirePlanSum(self):
        # 显示此次分配计划数
        sum = 0
        for i in self.currentEquipdict:
            if not selectEquipIsHaveChild(self.currentEquipdict[i][0]):
                for j in range(0, len(self.currentUnitChilddict)):
                    num = self.retirePlanResult.item(i, 3 + j).text()
                    if num == '':
                        sum = sum + 0
                    else:
                        sum = sum + int(num)
                self.retirePlanResult.item(i, 2).setText(str(sum))
            sum = 0
        for row in reversed(range(len(self.currentEquipdict))):
            sum = 0
            for childRow in reversed(range(len(self.currentEquipdict))):
                # 第0个字段是EquipID,第二个字段是Equip_Uper
                if self.currentEquipdict[row][0] == self.currentEquipdict[childRow][2]:
                    num = self.retirePlanResult.item(childRow, 2).text()
                    if num != '':
                        sum = sum + int(num)
            if sum != 0:
                self.retirePlanResult.item(row, 2).setText(str(sum))
        for i in range(0, len(self.currentUnitChilddict)):
            for row in reversed(range(len(self.currentEquipdict))):
                sum = 0
                for childRow in reversed(range(len(self.currentEquipdict))):
                    # 第0个字段是EquipID,第二个字段是Equip_Uper
                    if self.currentEquipdict[row][0] == self.currentEquipdict[childRow][2]:
                        num = self.retirePlanResult.item(childRow, 3 + i).text()
                        if num != '':
                            sum = sum + int(num)
                if sum != 0:
                    self.retirePlanResult.item(row, 3 + i).setText(str(sum))

    # 若装备含子装备，则该行不可选中
    def ifEquipHaveChild(self):
        # print("self.currentEquipdict", self.currentEquipdict)
        for i in self.currentEquipdict:
            if selectEquipIsHaveChild(self.currentEquipdict[i][0]):
                for j in range(1, self.retirePlanResult.columnCount()):
                    item = self.retirePlanResult.item(i, j)
                    # item.setText("")
                    # item.setBackground(QBrush(QColor(240, 240, 240)))
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
        改变分配计划数与备注
    '''

    def slotItemChange(self):
        self.currentRow = self.retirePlanResult.currentRow()
        self.currentColumn = self.retirePlanResult.currentColumn()
        if 3 <= self.currentColumn <= self.lenHeaderList - 2:
            try:
                num = self.retirePlanResult.item(self.currentRow, self.currentColumn).text()
                self.initRetirePlanSum()
                originRetirePlanNum = selectRetirePlanNumByList({0: self.currentUnitChilddict[self.currentColumn - 3]},
                                                                {0: self.currentEquipdict[self.currentRow]}, self.currentYear)
                originStrengthNum = selectStrengthNum(self.currentUnitChilddict[self.currentColumn - 3][0],
                                                      self.currentEquipdict[self.currentRow][0], self.currentYear)
                # print("originRetirePlanNum", originRetirePlanNum, "originStrengthNum", originStrengthNum)
                if originStrengthNum[0] != '':
                    updateRetirePlanNum(self.currentEquipdict[self.currentRow][0],
                                        self.currentUnitChilddict[self.currentColumn - 3][0],
                                        self.currentYear, num, originRetirePlanNum[0])
                    updateOneEquipmentBalanceData(self.currentYear, self.currentEquipdict[self.currentRow][0],
                                                  self.currentUnitChilddict[self.currentColumn - 3][0])
                else:
                    getMessageBox("提示", "未填写实力数", True, False)
            except ValueError:
                getMessageBox("提示", "请输入数字", True, False)
                self.retirePlanResult.item(self.currentRow, self.currentColumn).setText("")
        if self.currentColumn == self.lenHeaderList - 1:
            updateRetirePlanNote(self.currentEquipdict[self.currentRow][0], self.currentYear,
                                 self.retirePlanResult.item(self.currentRow, self.currentColumn).text())

    # 初始化分配计划年份
    def setRetirePlanTitle(self):
        txt = str(self.currentYear) + "年退役报废计划"
        self.txt_retirePlanYear.setFont(QFont("Microsoft YaHei"))
        self.txt_retirePlanYear.setAlignment(Qt.AlignCenter)
        self.txt_retirePlanYear.setTextInteractionFlags(Qt.NoTextInteraction)
        self.txt_retirePlanYear.setFontPointSize(15)
        self.txt_retirePlanYear.setText(txt)

    # 读取初始分配计划备注
    def initRetirePlanNote(self):
        self.unitRetirePlanNoteList = selectRetirePlanNote(self.currentEquipdict, self.currentYear)
        for i in range(0, len(self.currentEquipdict)):
            item = self.retirePlanResult.item(i, self.lenHeaderList - 1)
            if self.unitRetirePlanNoteList[i] is not None:
                item.setText(str(self.unitRetirePlanNoteList[i]))
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable)

    # 读取机关计划数与装备单位
    def initRetirePlanOther(self):
        for i in range(0, len(self.currentEquipdict)):
            item = self.retirePlanResult.item(i, 1)
            item.setText(str(self.currentEquipdict[i][5]))


    '''
        功能
            导出数据到Excel
    '''
    def slotOutputToExcel(self):
        self.retirePlanList = {}
        if self.retirePlanResult.rowCount() <= 0:
            getMessageBox('警告', '未选中任何数据，无法导出', True, False)
            return
        reply = getMessageBox('导出Excel', '是否保存修改并导出Excel？', True, False)
        if reply == QMessageBox.Cancel:
            self._initRetirePlanByUnitListAndEquipList()
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

            #画表头
            if self.unitFlag == 1:
                headerlist = ['装备名称及规格型号', '单位', '退役报废合计数']
                if len(self.currentUnitChilddict):
                    for i in self.currentUnitChilddict.values():
                        headerlist.append(i[1])
                headerlist.append('备注')
            elif self.unitFlag == 2:
                headerlist = ['装备名称及规格型号', '单位', '退役报废合计数']
                if len(self.currentUnitChilddict):
                    for i in self.currentUnitChilddict.values():
                        headerlist.append(i[1])
                headerlist.append('备注')

            for i in range(len(headerlist)):
                workSheet.col(i).width = 5500
            workSheet.write_merge(0, 0, 0, len(headerlist) - 1, "%s年退役报废计划" % str(self.currentYear), headTitleStyle)
            for i in range(len(headerlist)):
                workSheet.write(1, i, headerlist[i], titileStyle)
            #填表数据
            for i in range(self.retirePlanResult.rowCount()):
                columnList = []
                for j in range(self.retirePlanResult.columnCount()):
                    columnList.append(self.retirePlanResult.item(i, j).text())
                self.retirePlanList[i] = columnList
            for key in self.retirePlanList.keys():
                for index in range(len(headerlist)):
                    rowData = self.retirePlanList.get(key)
                    workSheet.write(2 + key, index, rowData[index], contentStyle)

            try:
                pathName = "%s/%s年通用装备退役报废计划.xls" % (directoryPath, str(self.currentYear))
                workBook.save(pathName)
                import win32api
                win32api.ShellExecute(0, 'open', pathName, '', '', 1)
                getMessageBox( "导出成功", "导出成功！", True, False)
                return
            except Exception as e:
                getMessageBox("导出失败", "导出表格被占用，请关闭正在使用的Execl！", True, False)
                return
        else:
            getMessageBox("选取文件夹失败！", "请选择正确的文件夹！", True, False)