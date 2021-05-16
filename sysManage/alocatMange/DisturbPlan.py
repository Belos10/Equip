import sys
from PyQt5.QtWidgets import *

from database.SD_EquipmentBanlanceSql import initEquipmentBalance, updateOneEquipmentBalanceData
from widgets.alocatMange.yearListForm import yearList_Form
from database.strengthDisturbSql import *
from PyQt5.Qt import Qt
from PyQt5.QtGui import QColor, QBrush,QFont
from database.alocatMangeSql import *

'''
    分配调整计划
'''
class DisturbPlan(QWidget, yearList_Form):
    def __init__(self, parent=None):
        super(DisturbPlan, self).__init__(parent)
        # Stren_Inquiry._initUnitTreeWidget()
        self.setupUi(self)
        self.initAll()
        # initDisturbPlanDatabase()


    def initAll(self):
        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}
        self.currentDisturbPlan = {}
        self.currentUnitDisturbPlanNum = {}
        self.unitDisturbPlanList = {}
        self.signalConnect()
        self.signalDisconnectSlot()
        self.tw_first.header().setVisible(False)
        self.tw_second.header().setVisible(False)
        self.le_first.setDisabled(1)
        self.le_second.setDisabled(1)
        self.tw_first.setDisabled(1)
        self.tw_second.setDisabled(1)
        self._initYearWidget_()

    def signalConnect(self):
        # 点击选择年份后刷新页面 初始化
        self.lw_yearChoose.itemDoubleClicked.connect(self.slotClickedInqury)
        self.lw_yearChoose.itemDoubleClicked.connect(self.setDisturbPlanTitle)
        self.lw_yearChoose.itemDoubleClicked.connect(self.initDisturbPlanProof)

        # 点击第一目录结果
        self.tw_first.itemClicked.connect(self.slotDisturbStrengthResult)

        self.tw_second.itemChanged.connect(self.slotCheckedChange)

        # 点击第二目录结果
        self.tw_second.itemClicked.connect(self.slotDisturbStrengthResult)
        # 新增年份
        self.tb_add.clicked.connect(self.slotAddNewYear)
        # 删除年份
        self.tb_del.clicked.connect(self.slotDelYear)
        # 修改分配数与备注
        self.disturbResult.itemChanged.connect(self.slotItemChange)
        # 修改调拨依据
        self.te_proof.textChanged.connect(self.slotProofChange)

        self.pb_firstSelect.clicked.connect(self.slotSelectUnit)

        self.pb_secondSelect.clicked.connect(self.slotSelectEquip)

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


    # 信号与槽连接的断开
    def signalDisconnectSlot(self):
        pass



    # 新增年份
    def slotAddNewYear(self):
        #year = 0
        year, ok = QInputDialog.getInt(self, "Get year", "year:", 0, 0, 100000, 1)
        if year:
            insertIntoDisturbPlanYear(year)
            self._initYearWidget_()


    # 删除年份
    def slotDelYear(self):
        currentYear=self.lw_yearChoose.currentItem()
        #print(currentYear.text())
        deleteDisturbPlanYear(currentYear.text())
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



    def slotClickedInqury(self):
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
        self._initUnitTreeWidget("", self.tw_first)
        self._initEquipTreeWidget("", self.tw_second)



    def _initUnitTreeWidget(self, root, mother):
        if root == '':
            result = selectDisturbPlanUnitInfoByDeptUper('')
        else:
            result = selectDisturbPlanUnitInfoByDeptUper(root)

        # rowData: (单位编号，单位名称，上级单位编号)
        for rowData in result:
            item = QTreeWidgetItem(mother)
            item.setText(0, rowData[1])
            #item.setCheckState(0, Qt.Unchecked)
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
        self.currentEquipdict={}
        self.currentUnitChilddict = {}
        # 获取子单位名
        j = 0
        for unitID, unitItem in self.first_treeWidget_dict.items():
            if unitItem == self.tw_first.currentItem():
                if selectUnitIfUppermost(unitID):
                    result = selectAllDataAboutDisturbPlanUnitExceptFirst()
                else:
                    result = findDisturbPlanUnitChildInfo(unitID)
                for resultInfo in result:
                    self.currentUnitChilddict[j] = resultInfo
                    j=j+1
        print("unit", self.currentUnitChilddict)
        # 获取当前装备名
        j = 0
        for equipID, equipItem in self.second_treeWidget_dict.items():
            if equipItem.checkState(0) == Qt.Checked:
                equipInfo = findEquipInfo(equipID)
                self.currentEquipdict[j]= equipInfo[0]
            elif equipItem.checkState(0) == Qt.PartiallyChecked:
                equipInfo = findEquipInfo(equipID)
                self.currentEquipdict[j] = equipInfo[0]
            j=j+1
        # print("self.currentEquipdict",self.currentEquipdict)

        self._initDisturbPlanByUnitListAndEquipList()



    '''
        初始化分配计划结果
    '''
    def _initDisturbPlanByUnitListAndEquipList(self):
        self.disturbResult.clear()
        self.disturbResult.setRowCount(0)
        self.lenCurrentUnitChilddict=len(self.currentUnitChilddict)
        self.lenCurrentEquipdict=len(self.currentEquipdict)

        headerlist = ['装备名称及规格型号', '单位', '机关分配计划数', '此次分配合计数']
        if len(self.currentUnitChilddict):
            for i in self.currentUnitChilddict.values():
                headerlist.append(i[1])
        headerlist.append('备注')
        self.lenHeaderList=len(headerlist)
        self.disturbResult.setColumnCount(self.lenHeaderList)
        self.disturbResult.setRowCount(len(self.currentEquipdict))
        self.disturbResult.setHorizontalHeaderLabels(headerlist)
        self.currentDisturbPlan.clear()
        self.disturbResult.setColumnWidth(0, 200)
        i = 0
        for LineInfo in self.currentEquipdict.values():
            item = QTableWidgetItem(LineInfo[1])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.disturbResult.setItem(i, 0, item)
            item = QTableWidgetItem("")
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.disturbResult.setItem(i, 1, item)
            item = QTableWidgetItem("")
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.disturbResult.setItem(i, 2, item)
            item = QTableWidgetItem("")
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.disturbResult.setItem(i, 3, item)
            for x in range(0, self.lenCurrentUnitChilddict):
                item = QTableWidgetItem("")
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.disturbResult.setItem(i, x + 4, item)
            item = QTableWidgetItem("")
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.disturbResult.setItem(i, 4 + self.lenCurrentUnitChilddict, item)
            i = i + 1
            self.currentDisturbPlan[i] = LineInfo

        #self.disturbResult.setRowCount(n)
        self.initDisturbPlanNum()
        self.initDisturbPlanNote()
        self.initDisturbPlanOther()
        self.ifEquipHaveChild()

    # 初始化调拨依据
    def initDisturbPlanProof(self):
        proof = selectDisturbPlanProof(self.currentYear)
        print(proof)
        self.te_proof.setText(proof[0][0])
        if proof[0][0] == "":
            self.te_proof.setPlaceholderText("请输入调拨依据")

    # 改变调拨依据
    def slotProofChange(self):
        #print("self.te_proof.toPlainText()",self.te_proof.toPlainText())
        updateDisturbPlanProof(self.currentYear,self.te_proof.toPlainText())

    # 读取初始分配计划数
    def initDisturbPlanNum(self):
        self.unitDisturbPlanList = selectDisturbPlanNum(self.currentUnitChilddict,
                                                        self.currentEquipdict, self.currentYear)
        print("self.unitDisturbPlanList", self.unitDisturbPlanList)
        # 显示每个单位分配计划数
        num=0
        for i in range(0,len(self.currentUnitChilddict)):
            for j in range(0,len(self.currentEquipdict)):
                item = self.disturbResult.item(j, 4 + i)
                if self.unitDisturbPlanList[num]!='-1':
                    item.setText(self.unitDisturbPlanList[num])
                item.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable|Qt.ItemIsEditable)
                num=num+1
        self.initDisturbPlanSum()


    # 初始化此次分配数
    def initDisturbPlanSum(self):
        # 显示此次分配计划数
        sum = 0
        for i in self.currentEquipdict:
            if not selectEquipIsHaveChild(self.currentEquipdict[i][0]):
                for j in range(0, len(self.currentUnitChilddict)):
                    num = self.disturbResult.item(i, 4 + j).text()
                    if num == '-1' or num == '':
                        sum = sum + 0
                    else:
                        sum = sum + int(num)
                self.disturbResult.item(i,3).setText(str(sum))
            sum = 0


    # 若装备含子装备，则该行不可选中
    def ifEquipHaveChild(self):
        print("self.currentEquipdict",self.currentEquipdict)
        for i in self.currentEquipdict:
            if selectEquipIsHaveChild(self.currentEquipdict[i][0]):
                for j in range(1,self.disturbResult.columnCount()):
                    item = self.disturbResult.item(i,j)
                    item.setText("")
                    # item.setBackground(QBrush(QColor(240, 240, 240)))
                    item.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable)


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
        self.currentRow = self.disturbResult.currentRow()
        self.currentColumn = self.disturbResult.currentColumn()
        if 4 <= self.currentColumn <= self.lenHeaderList-2:
            updateDisturbPlanNum(self.currentEquipdict[self.currentRow][0],self.currentUnitChilddict[self.currentColumn-4][0],
                                 self.currentYear,self.disturbResult.item(self.currentRow,self.currentColumn).text())
            updateOneEquipmentBalanceData(self.currentYear,self.currentEquipdict[self.currentRow][0],self.currentUnitChilddict[self.currentColumn-4][0])
            self.initDisturbPlanSum()
        if self.currentColumn == self.lenHeaderList-1:
            updateDisturbPlanNote(self.currentEquipdict[self.currentRow][0],self.currentYear,self.disturbResult.item(self.currentRow,self.currentColumn).text())

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
        for i in range(0,len(self.unitDisturbPlanNoteList)):
            item=self.disturbResult.item(i,self.lenHeaderList-1)
            if self.unitDisturbPlanNoteList[i] is not None:
                item.setText(str(self.unitDisturbPlanNoteList[i]))
            item.setFlags(Qt.ItemIsEnabled|Qt.ItemIsSelectable|Qt.ItemIsEditable)


    # 读取机关计划数与装备单位
    def initDisturbPlanOther(self):
        self.unitDisturbPlanOtherList = selectDisturbPlanOther(self.currentEquipdict, self.currentYear)

        for i in range(0, len(self.unitDisturbPlanOtherList)):
                item=self.disturbResult.item(i,1)
                item.setText(str(self.unitDisturbPlanOtherList[i][0]))

        for unitID, unitItem in self.first_treeWidget_dict.items():
            if unitItem == self.tw_first.currentItem():
                if selectUnitIfUppermost(unitID):
                    for i in range(0, len(self.unitDisturbPlanOtherList)):
                        item = self.disturbResult.item(i, 2)
                        item.setText(str(self.unitDisturbPlanOtherList[i][1]))
                else:
                    for i in self.currentEquipdict:
                        item = self.disturbResult.item(i,2)
                        result = selectDisturbPlanNum({0:[unitID]},self.currentEquipdict,self.currentYear)
                        item.setText(str(result[i]))

