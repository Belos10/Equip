from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QTableWidgetItem, QAbstractItemView, \
    QMessageBox, QListWidgetItem,QInputDialog,QHeaderView,QLineEdit

from sysManage.component import getMessageBox
from utills.Search import selectUnit
from widgets.strengthDisturb.maintenMange import Widget_Mainten_Manage
from database.strengthDisturbSql import *
from PyQt5.Qt import Qt
from sysManage.userInfo import get_value
from PyQt5.Qt import QRegExp, QRegExpValidator,QKeyEvent

regx = QRegExp("[0-9]*")
'''
   编制数维护
'''
class maintenManage(QWidget, Widget_Mainten_Manage):
    def __init__(self, parent=None):
        super(maintenManage, self).__init__(parent)
        self.setupUi(self)
        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}

        self.tw_first.header().setVisible(False)
        self.tw_second.header().setVisible(False)

        self.signalConnect()
        self.userInfo = None
        self.currentInquiryResult = {}
        self.resultList = []
        self.unitList = []
        self.equipList = []
        self.year = '全部'
        self.currentYear = None
        self.tw_result.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def getUserInfo(self):
        self.userInfo = get_value("totleUserInfo")
        #self._initAll_()

    #初始化编制数维护界面
    def _initAll_(self):
        self.tw_first.clear()
        self.tw_second.clear()
        self.tw_result.clear()
        self.getUserInfo()
        self.first_treeWidget_dict = {}
        self.tw_first.clear()
        #self.startName = selectUnitNameByUnitID(self.userInfo[0][4])
        #item = QTreeWidgetItem(self.tw_first)
        #item.setText(0, self.startName)
        #item.setCheckState(0, Qt.Unchecked)
        #self.first_treeWidget_dict[self.userInfo[0][4]] = item
        self._initUnitTreeWidget("", self.tw_first)
        self._initStrenInquiry()
        self.tw_result.clear()
        self.tw_result.setRowCount(0)
        self.tw_result.setColumnCount(0)
        self.currentYear = None
        self.currentInquiryResult = {}
        self.resultList = []
        self.unitList = []
        self.equipList = []
        self.year = '全部'

    #信号连接
    def signalConnect(self):
        # 点击某个年份后显示单位和装备目录
        self.lw_year.clicked.connect(self.slotClickedInqury)

        # 当前单位目录被点击
        self.tw_first.itemClicked.connect(self.slotInquryStrengthResult)

        # 当前装备目录被点击
        self.tw_second.itemClicked.connect(self.slotInquryStrengthResult)

        # 当点击按装备展开时
        self.rb_equipShow.clicked.connect(self.slotClickedRB)

        # 当点击按单位展开时
        self.rb_unitShow.clicked.connect(self.slotClickedRB)

        #当前查询结果要修改时
        self.tw_result.itemChanged.connect(self.slotResultItemChange,Qt.UniqueConnection)

        #清除当前选中行的编制数
        self.pb_clearCheck.clicked.connect(self.slotClearCurrentRow)

        #清除当前页面的编制数
        self.pb_clearAll.clicked.connect(self.slotClearAllRow)

        #当点击展开到末级的时候
        self.cb_showLast.clicked.connect(self.slotClickedRB)

        self.pb_firstSelect.clicked.connect(self.slotSelectUnit)

        self.pb_secondSelect.clicked.connect(self.slotSelectEquip)

        # self.tw_second.itemChanged.connect(self.slotCheckedChange)
        # self.tw_first.itemChanged.connect(self.slotCheckedChange)

    def slotSelectUnit(self):
        selectUnit(self, self.le_first, self.first_treeWidget_dict, self.tw_first)


    def slotSelectEquip(self):
        selectUnit(self, self.le_second, self.second_treeWidget_dict, self.tw_second)


    #当前结果的值被修改
    def slotResultItemChange(self):
        self.currentRow = self.tw_result.currentRow()
        self.currentColumn = self.tw_result.currentColumn()

        if self.currentColumn == 3:
            for i, resultRowInfo in self.currentInquiryResult.items():
                if i == self.currentRow:
                    unitHaveChild = selectUnitIsHaveChild(resultRowInfo[0])
                    equipHaveChild = selectEquipIsHaveChild(resultRowInfo[1])
                    if isHavePulicEquip(resultRowInfo[0]):
                        getMessageBox('录入', '该单位或装备不是末级，无法修改', True, False)
                        self.tw_result.cellWidget(self.currentRow, 3).setText(str(resultRowInfo[5]))
                        return
                    if unitHaveChild or equipHaveChild:
                        getMessageBox('录入', '该单位或装备不是末级，无法修改', True, False)
                        self.tw_result.cellWidget(self.currentRow, 3).setText(str(resultRowInfo[5]))
                        return
                    else:
                        try:
                            weave = self.tw_result.cellWidget(self.currentRow, 3).text()
                            updataSuccess = updateWeaveNum(resultRowInfo[0], resultRowInfo[1],
                                                           self.tw_result.cellWidget(self.currentRow, 3).text(),
                                                           str(resultRowInfo[5]), self.year)
                            self._initTableWidgetByUnitListAndEquipList(self.unitList, self.equipList, self.year)
                            return

                        # try:
                        #     weave = self.tw_result.cellWidget(self.currentRow, 3).text()
                        #     reply = getMessageBox('修改', '是否修改当前装备、单位的编制数?', True, True)
                        #     if reply == QMessageBox.Ok:
                        #         updataSuccess = updateWeaveNum(resultRowInfo[0], resultRowInfo[1], self.tw_result.cellWidget(self.currentRow, 3).text(), str(resultRowInfo[5]), self.year)
                        #         if updataSuccess != True:
                        #             getMessageBox(self, "修改", str(updataSuccess) + "修改失败", True, False)
                        #             return
                        #
                        #         #updateOneEquipmentBalanceData(self.year, resultRowInfo[0],resultRowInfo[1])
                        #         self._initTableWidgetByUnitListAndEquipList(self.unitList, self.equipList, self.year)
                        #         return
                        #     else:
                        #         self.tw_result.cellWidget(self.currentRow, 3).setText(str(resultRowInfo[5]))
                        #         return
                        except ValueError:
                            getMessageBox('修改', '编制数只能修改为整数?', True, False)
                            self.tw_result.cellWidget(self.currentRow, 3).setText(str(resultRowInfo[5]))
                            self._initTableWidgetByUnitListAndEquipList(self.unitList, self.equipList, self.year)
                            return
        else:
            pass


    #清除当前页面的所有编制数
    def slotClearAllRow(self):
        if self.year == '全部':
            getMessageBox('清除', '只能某一年，清除失败', True, False)
            return
        reply = getMessageBox('清除', '是否清除当前页面所有行的编制数？', True, True)
        if reply == QMessageBox.Cancel:
            return

        for i, resultInfo in self.currentInquiryResult.items():
            Unit_ID = resultInfo[0]
            Equip_ID = resultInfo[1]
            orginNum = resultInfo[5]
            year = resultInfo[-1]
            unitHaveChild = selectUnitIsHaveChild(Unit_ID)
            equipHaveChild = selectEquipIsHaveChild(Equip_ID)

            if unitHaveChild or equipHaveChild:
                getMessageBox('清除', '第' + str(i) + "行清除失败，只能清除末级单位和装备编制数",True, False)
                continue
            else:
                updateSuccess = updateWeaveNum(Unit_ID, Equip_ID, "0", orginNum, year)
                if updateSuccess != True:
                    getMessageBox('清除', '第' + str(i) + "行清除失败, " + str(updateSuccess), True, False)
                    return
                updateOneEquipmentBalanceData(year, Equip_ID, Unit_ID)
                getMessageBox('成功', '第' + str(i) + "行清除成功", True, False)
                self._initTableWidgetByUnitListAndEquipList(self.unitList, self.equipList, self.year)

    #清除当前行的编制数
    def slotClearCurrentRow(self):
        currentRow = self.tw_result.currentRow()
        if currentRow < 0:
            return
        else:
            for i, resultInfo in self.currentInquiryResult.items():
                if i == currentRow:
                    Unit_ID = resultInfo[0]
                    Equip_ID = resultInfo[1]
                    orginNum = resultInfo[5]
                    year = resultInfo[7]
                    unitHaveChild = selectUnitIsHaveChild(Unit_ID)
                    equipHaveChild = selectEquipIsHaveChild(Equip_ID)
                    if unitHaveChild or equipHaveChild:
                        getMessageBox('清除', '只能清除末级单位和装备的编制数', True, False)
                        return
                    elif self.year == '全部':
                        getMessageBox( '清除', '只能某一年，清除失败', True, False)
                        return
                    else:
                        getMessageBox('清除', '是否清除当前行的编制数？', True, True)
                        updateWeaveNum(Unit_ID, Equip_ID, "0", orginNum, year)
                        self._initTableWidgetByUnitListAndEquipList(self.unitList, self.equipList, self.year)

    #当选择按单位展开或按装备展开或展开到末级按钮时
    def slotClickedRB(self):
        if len(self.unitList) < 1 or len(self.equipList) < 1:
            return
        self._initTableWidgetByUnitListAndEquipList(self.unitList, self.equipList, self.year)

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
        #        self.tb_inqury.setDisabled(True)
        #        self.tb_rechoose.setDisabled(False)

        self.currentYear = self.lw_year.currentItem().text()
        self.startInfo = selectUnitInfoByUnitID(self.userInfo[0][4])
        stack = []
        root = []
        if self.startInfo:
            stack.append(self.startInfo)
            root.append(self.tw_first)
            self.initUnitTreeWidget(stack, root)

        equipInfo = None
        equipInfo = selectEquipInfoByEquipUper("")
        stack = []
        root = []
        if equipInfo:
            stack.append(equipInfo[0])
            root.append(self.tw_second)
            self.initEquipTreeWidget(stack, root)
            # 从数据库中单位表中获取数据初始化单位目录，tableWidget显示所有的单位表
            # self._initUnitTreeWidget("", self.tw_first)

    '''
           功能：
               设置级目录联选中状态
    '''

    # def slotCheckedChange(self, item, num):
    #     # 如果是顶部节点，只考虑Child：
    #     if item.childCount() and not item.parent():  # 判断是顶部节点，也就是根节点
    #         if item.checkState(num) == 0:  # 规定点击根节点只有两态切换，没有中间态
    #             for i in range(item.childCount()):  # 遍历子节点进行状态切换
    #                 item.child(i).setCheckState(num, 0)
    #         elif item.checkState(num) == 2:
    #             for i in range(item.childCount()):
    #                 item.child(i).setCheckState(num, 2)
    #     # 如果是底部节点，只考虑Parent
    #     if item.parent() and not item.childCount():
    #         parent_item = item.parent()  # 获得父节点
    #         brother_item_num = parent_item.childCount()  # 获得兄弟节点的数目，包括自身在内
    #         checked_num = 0  # 设置计数器
    #         for i in range(brother_item_num):  # 根据三态不同状态值进行数值累计
    #             checked_num += parent_item.child(i).checkState(num)
    #         if checked_num == 0:  # 最终结果进行比较，决定父节点的三态
    #             parent_item.setCheckState(num, 0)
    #         elif checked_num / 2 == brother_item_num:
    #             parent_item.setCheckState(num, 2)
    #         else:
    #             parent_item.setCheckState(num, 1)
    #
    #         # 中间层需要全面考虑
    #     if item.parent() and item.childCount():
    #         if item.checkState(num) == 0:  # 规定点击根节点只有两态切换，没有中间态
    #             for i in range(item.childCount()):  # 遍历子节点进行状态切换
    #                 item.child(i).setCheckState(num, 0)
    #         elif item.checkState(num) == 2:
    #             for i in range(item.childCount()):
    #                 item.child(i).setCheckState(num, 2)
    #         parent_item = item.parent()  # 获得父节点
    #         brother_item_num = parent_item.childCount()  # 获得兄弟节点的数目，包括自身在内
    #         checked_num = 0  # 设置计数器
    #         for i in range(brother_item_num):  # 根据三态不同状态值进行数值累计
    #             checked_num += parent_item.child(i).checkState(num)
    #         if checked_num == 0:  # 最终结果进行比较，决定父节点的三态
    #             parent_item.setCheckState(num, 0)
    #         elif checked_num / 2 == brother_item_num:
    #             parent_item.setCheckState(num, 2)
    #         else:
    #             parent_item.setCheckState(num, 1)

    # def initEquipTreeWidget(self, stack, root):
    #     while stack:
    #         EquipInfo = stack.pop(0)
    #         item = QTreeWidgetItem(root.pop(0))
    #         item.setText(0, EquipInfo[1])
    #         item.setCheckState(0, Qt.Unchecked)
    #         self.second_treeWidget_dict[EquipInfo[0]] = item
    #         result = selectEquipInfoByEquipUper(EquipInfo[0])
    #         for resultInfo in result:
    #             stack.append(resultInfo)
    #             root.append(item)

    def initEquipTreeWidget(self, stack, root):
        while stack:
            EquipInfo = stack.pop(0)
            item = QTreeWidgetItem(root.pop(0))
            item.setFlags(
                Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsAutoTristate)
            item.setText(0, EquipInfo[1])
            item.setData(0, Qt.UserRole, QVariant(EquipInfo[0]))
            item.setCheckState(0, Qt.Unchecked)
            self.second_treeWidget_dict[EquipInfo[0]] = item
            result = selectEquipInfoByEquipUper(EquipInfo[0])
            for resultInfo in result:
                stack.append(resultInfo)
                root.append(item)

    '''
                功能：
                    单位目录的初始化，显示整个单位表
                    参数表：root为上级单位名字，mother为上级节点对象
        '''

    def initUnitTreeWidget(self, stack, root):
        while stack:
            UnitInfo = stack.pop(0)
            item = QTreeWidgetItem(root.pop(0))
            item.setFlags(
                Qt.ItemIsUserCheckable | Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsAutoTristate)
            item.setText(0, UnitInfo[1])
            item.setData(0, Qt.UserRole, QVariant(UnitInfo[0]))
            item.setCheckState(0, Qt.Unchecked)
            if UnitInfo:
                if UnitInfo[4]  == "是":
                    publicItem = QTreeWidgetItem(item)
                    publicEuip = selectPubilcEquipInfoByGroupID(UnitInfo[0])
                    if publicEuip:
                        publicItem.setText(0, "公用装备")
                        self.first_treeWidget_dict[publicEuip[0]] = publicItem
                        publicItem.setCheckState(0, Qt.Unchecked)
            self.first_treeWidget_dict[UnitInfo[0]] = item
            result = selectUnitInfoByDeptUper(UnitInfo[0])
            for resultInfo in result:
                stack.append(resultInfo)
                root.append(item)


    #查看当前被选中的单位和装备并初试化
    def slotInquryStrengthResult(self):
        self.currentCheckedUnitList = []
        self.currentCheckedEquipList = []
        # self.currentCheckedUnitList = self.get_checked(self.tw_first.topLevelItem(0))
        # self.currentCheckedEquipList = self.get_checked(self.tw_second.topLevelItem(0))
        for unitID, unitItem in self.first_treeWidget_dict.items():
            if unitItem.checkState(0) == Qt.Checked:
                self.currentCheckedUnitList.append(unitID)

        for equipID, equipItem in self.second_treeWidget_dict.items():
            if equipItem.checkState(0) == Qt.Checked:
                self.currentCheckedEquipList.append(equipID)

        # print("----------装备单位列表---------")
        # print(self.currentCheckedUnitList)
        # print(self.currentCheckedEquipList)
        # if self.currentCheckedUnitList == [] or self.currentCheckedEquipList == []:
        #     headerlist = ['单位名称', '装备名称', '计划数', '编制数', '现有数']
        #     self.tw_result.setHorizontalHeaderLabels(headerlist)
        #     self.currentInquiryResult.clear()
        #     self.tw_result.setColumnCount(len(headerlist))
        #     self.tw_result.setRowCount(0)
        #     return
        if len(self.currentCheckedUnitList) > 0 and len(self.currentCheckedUnitList) > 0:
            self._initTableWidgetByUnitListAndEquipList(self.currentCheckedUnitList, self.currentCheckedEquipList, self.currentYear)
        else:
            headerlist = ['单位名称', '装备名称', '计划数', '编制数', '现有数']
            self.tw_result.setHorizontalHeaderLabels(headerlist)
            self.tw_result.setColumnCount(len(headerlist))
            self.tw_result.setRowCount(0)
            # self.currentInquiryResult.clear()
            pass



    # 初始化tableWidget
    def _initTableWidgetByUnitListAndEquipList(self, UnitList, EquipList, year):
        self.tw_result.clear()
        self.tw_result.setRowCount(0)
        self.unitList = UnitList
        self.equipList = EquipList
        self.year = year
        self.resultList = []
        if self.rb_equipShow.isChecked():
            # 按装备展开
            self.resultList = selectAboutWeaveByEquipShow(UnitList, EquipList, year)
        elif self.rb_unitShow.isChecked():
            # 按单位展开
            self.resultList = selectAboutWeaveByUnitShow(UnitList, EquipList, year)
        else:
            self.resultList = selectAboutWeaveByUnitListAndEquipList(UnitList, EquipList, year)

        if self.cb_showLast.isChecked():
            self.resultList = selectAboutWeaveByLast(UnitList, EquipList, year)
            self.rb_unitShow.setCheckable(False)
            self.rb_equipShow.setCheckable(False)
            self.rb_equipShow.setDisabled(True)
            self.rb_unitShow.setDisabled(True)
        else:
            self.rb_unitShow.setCheckable(True)
            self.rb_equipShow.setCheckable(True)
            self.rb_equipShow.setDisabled(False)
            self.rb_unitShow.setDisabled(False)

        headerlist = ['单位名称', '装备名称', '计划数', '编制数', '现有数']
        self.tw_result.setHorizontalHeaderLabels(headerlist)
        self.currentInquiryResult.clear()
        self.tw_result.setColumnCount(len(headerlist))
        self.tw_result.setRowCount(len(self.resultList))

        i = 0
        for LineInfo in self.resultList:
            item = QTableWidgetItem(str(LineInfo[2]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i, 0, item)
            item = QTableWidgetItem(str(LineInfo[3]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i, 1, item)
            item = QTableWidgetItem(str(LineInfo[4]))
            self.tw_result.setItem(i, 2, item)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

            item = QTableWidgetItem(str(LineInfo[5]))
            # item.textChanged.connect(self.slotResultItemChange)
            # item.setStyleSheet("background:white;border-width:0;color:black")
            validator = QRegExpValidator(regx)
            # item.setValidator(validator)
            self.tw_result.setItem(i, 3, item)
            item = QTableWidgetItem(str(LineInfo[6]))

            self.tw_result.setItem(i, 4, item)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.currentInquiryResult[i] = LineInfo
            i = i + 1

        self.tw_result.setRowCount(i)

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

    '''
        功能：
            当选择年份时，设置当前可选项和不可选项,并初始化年份目录
    '''
    def _initStrenInquiry(self):
        self.tw_first.clear()
        self.tw_first.header().setVisible(False)
        self.tw_second.header().setVisible(False)
        self.le_first.setDisabled(True)
        self.le_second.setDisabled(True)
        self.tw_first.setDisabled(True)
        self.tw_second.setDisabled(True)
        # self.tb_inqury.setDisabled(False)
        # self.tb_rechoose.setDisabled(False)

        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}

        # 当前选中的单位列表和装备列表
        self.currentCheckedUnitList = []
        self.currentCheckedEquipList = []

        self.yearList = []

        # 初始化年份选择列表
        self._initSelectYear_()
        # self.cb_yearAll = QCheckBox(self.sa_yearChoose)

    #初始化年份listwidget
    def _initSelectYear_(self):
        self.currentYearListItem = {}
        self.yearList = []
        self.lw_year.clear()
        allyearList = []
        allyearList = selectAllDataAboutStrengthYear()

        for year in allyearList:
            self.yearList.append(year[1])

        for year in self.yearList:
            item = QListWidgetItem()
            item.setText(year)
            self.lw_year.addItem(item)
            self.currentYearListItem[year] = item

    #初始化单位目录
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
            if rowData[4] == '是':
                publicItem = QTreeWidgetItem(item)
                publicEquipID = selectGroupIDByPublicEquip(rowData[0])
                publicItem.setText(0, "公用装备")
                publicItem.setCheckState(0, Qt.Unchecked)
                self.first_treeWidget_dict[publicEquipID] = publicItem
            if rowData[0] != '':
                self._initUnitTreeWidget(rowData[0], item)

    def get_checked(self, node: QTreeWidgetItem) -> list:
        """ 得到当前节点选中的所有分支， 返回一个 list """
        temp_list = []
        # 此处看下方注释 1
        for item in node.takeChildren():
            # 判断是否选中
            if item.checkState(0) == Qt.Checked or item.checkState(0) == Qt.PartiallyChecked:
                temp_list.append(str(item.data(0, Qt.UserRole)))
                # 判断是否还有子分支
                if item.childCount():
                    temp_list.extend(self.get_checked(item))
            node.addChild(item)
        return temp_list