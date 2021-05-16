from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QTableWidgetItem, QAbstractItemView, \
    QMessageBox, QListWidgetItem,QInputDialog
from widgets.strengthDisturb.maintenMange import Widget_Mainten_Manage
from database.strengthDisturbSql import *
from PyQt5.Qt import Qt

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


    def getUserInfo(self, userInfo):
        self.userInfo = userInfo
        self._initAll_()

    #初始化编制数维护界面
    def _initAll_(self):
        self.first_treeWidget_dict = {}
        self.tw_first.clear()
        self.startName = selectUnitNameByUnitID(self.userInfo[0][4])
        item = QTreeWidgetItem(self.tw_first)
        item.setText(0, self.startName)
        item.setCheckState(0, Qt.Unchecked)
        self.first_treeWidget_dict[self.userInfo[0][4]] = item
        self._initUnitTreeWidget(self.userInfo[0][4], item)
        self._initStrenInquiry()
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
        self.tw_first.itemChanged.connect(self.slotInquryStrengthResult)

        # 当前装备目录被点击
        self.tw_second.itemChanged.connect(self.slotInquryStrengthResult)

        # 当点击按装备展开时
        self.rb_equipShow.clicked.connect(self.slotClickedRB)

        # 当点击按单位展开时
        self.rb_unitShow.clicked.connect(self.slotClickedRB)

        #当前查询结果要修改时
        self.tw_result.itemChanged.connect(self.slotResultItemChange)

        #清除当前选中行的编制数
        self.pb_clearCheck.clicked.connect(self.slotClearCurrentRow)

        #清除当前页面的编制数
        self.pb_clearAll.clicked.connect(self.slotClearAllRow)

        #当点击展开到末级的时候
        self.cb_showLast.clicked.connect(self.slotClickedRB)

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

    #当前结果的值被修改
    def slotResultItemChange(self):
        self.currentRow = self.tw_result.currentRow()
        self.currentColumn = self.tw_result.currentColumn()

        if self.currentColumn == 3:
            for i, resultRowInfo in self.currentInquiryResult.items():
                if i == self.currentRow:
                    unitHaveChild = selectUnitIsHaveChild(resultRowInfo[0])
                    equipHaveChild = selectEquipIsHaveChild(resultRowInfo[1])
                    if unitHaveChild or equipHaveChild:
                        reply = QMessageBox.question(self, '录入', '该单位或装备不是末级，无法修改', QMessageBox.Yes)
                        self.tw_result.item(self.currentRow, 3).setText(resultRowInfo[5])
                    else:
                        reply = QMessageBox.question(self, '修改', '是否修改当前装备、单位的编制数?', QMessageBox.Yes, QMessageBox.Cancel)
                        if reply == QMessageBox.Yes:
                            updateWeaveNum(resultRowInfo[0], resultRowInfo[1], self.tw_result.item(self.currentRow, 3).text(), resultRowInfo[5], self.year)
                            self._initTableWidgetByUnitListAndEquipList(self.unitList, self.equipList, self.year)
                        else:
                            self.tw_result.item(self.currentRow, 3).setText(resultRowInfo[5])
                    break
        else:
            pass


    #清除当前页面的所有编制数
    def slotClearAllRow(self):
        if self.year == '全部':
            reply = QMessageBox.question(self, '清除', '只能某一年，清除失败', QMessageBox.Yes)
            return
        reply = QMessageBox.question(self, '清除', '是否清除当前页面所有行的编制数？', QMessageBox.Yes, QMessageBox.Cancel)
        if reply == QMessageBox.Cancel:
            return

        for i, resultInfo in self.currentInquiryResult.items():
            Unit_ID = resultInfo[0]
            Equip_ID = resultInfo[1]
            orginNum = resultInfo[5]
            year = resultInfo[7]
            unitHaveChild = selectUnitIsHaveChild(Unit_ID)
            equipHaveChild = selectEquipIsHaveChild(Equip_ID)
            if unitHaveChild or equipHaveChild:
                reply = QMessageBox.question(self, '清除', '第' + str(i) + "行清除失败，只能清除末级单位和装备编制数", QMessageBox.Yes)
                continue
            else:
                updateWeaveNum(Unit_ID, Equip_ID, year, "0", orginNum)
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
                        reply = QMessageBox.question(self, '清除', '只能清除末级单位和装备的编制数', QMessageBox.Yes)
                        return
                    elif self.year == '全部':
                        reply = QMessageBox.question(self, '清除', '只能某一年，清除失败', QMessageBox.Yes)
                        return
                    else:
                        reply = QMessageBox.question(self, '清除', '是否清除当前行的编制数？', QMessageBox.Yes, QMessageBox.Cancel)
                        updateWeaveNum(Unit_ID, Equip_ID, "0", orginNum, year)
                        self._initTableWidgetByUnitListAndEquipList(self.unitList, self.equipList, self.year)

    #当选择按单位展开或按装备展开或展开到末级按钮时
    def slotClickedRB(self):
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
        self.startName = selectUnitNameByUnitID(self.userInfo[0][4])
        item = QTreeWidgetItem(self.tw_first)
        item.setText(0, self.startName)
        item.setCheckState(0, Qt.Unchecked)
        self.first_treeWidget_dict[self.userInfo[0][4]] = item
        self._initUnitTreeWidget(self.userInfo[0][4], item)
        self._initEquipTreeWidget("", self.tw_second)

    #查看当前被选中的单位和装备并初试化
    def slotInquryStrengthResult(self):
        self.currentCheckedUnitList = []
        self.currentCheckedEquipList = []
        for unitID, unitItem in self.first_treeWidget_dict.items():
            if unitItem.checkState(0) == Qt.Checked:
                self.currentCheckedUnitList.append(unitID)

        for equipID, equipItem in self.second_treeWidget_dict.items():
            if equipItem.checkState(0) == Qt.Checked:
                self.currentCheckedEquipList.append(equipID)

        self._initTableWidgetByUnitListAndEquipList(self.currentCheckedUnitList, self.currentCheckedEquipList, self.currentYear)

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
            self.resultListEquip = selectAboutWeaveByEquipShow(UnitList, EquipList, year)
            self.resultListUnit = selectAboutWeaveByUnitShow(UnitList, EquipList, year)
            self.resultList = self.resultListEquip + self.resultListUnit
            self.rb_unitShow.setCheckable(False)
            self.rb_equipShow.setCheckable(False)
            self.rb_equipShow.setDisabled(True)
            self.rb_unitShow.setDisabled(True)
        else:
            self.rb_unitShow.setCheckable(True)
            self.rb_equipShow.setCheckable(True)
            self.rb_equipShow.setDisabled(False)
            self.rb_unitShow.setDisabled(False)

        headerlist = ['单位名称', '装备名称', '实力数', '编制数', '现有数']
        self.tw_result.setHorizontalHeaderLabels(headerlist)
        self.currentInquiryResult.clear()
        self.tw_result.setColumnCount(len(headerlist))
        self.tw_result.setRowCount(len(self.resultList))

        i = 0
        for LineInfo in self.resultList:
            item = QTableWidgetItem(LineInfo[2])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i, 0, item)
            item = QTableWidgetItem(LineInfo[3])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i, 1, item)
            item = QTableWidgetItem(LineInfo[4])
            self.tw_result.setItem(i, 2, item)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            item = QTableWidgetItem(LineInfo[5])
            self.tw_result.setItem(i, 3, item)
            item = QTableWidgetItem(LineInfo[6])
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
        allyearList = selectAllDataAboutStrengthYear()

        for year in allyearList:
            self.yearList.append(year[1])

        for year in self.yearList:
            item = QListWidgetItem()
            item.setText(year)
            self.lw_year.addItem(item)
            self.currentYearListItem[year[1]] = item

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