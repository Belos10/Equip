from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QTableWidgetItem, QAbstractItemView, QMessageBox, QListWidgetItem
from widgets.strengthDisturb.maintenMange import Widget_Mainten_Manage
from database.strengthDisturbSql import selectAllStrengthYearInfo, selectAllDataAboutUnit, \
    updateUnitIsGroupFromUnit, selectAllFromPulicEquip, selectUnitInfoByDeptUper, selectGroupIDByPublicEquip,\
    selectAllDataAboutWeaveYear, selectEquipInfoByEquipUper, selectAboutWeaveByUnitListAndEquipList, \
    selectAboutWeaveByEquipShow, selectAboutWeaveByUnitShow
from PyQt5.Qt import Qt

#new
class maintenManage(QWidget, Widget_Mainten_Manage):
    def __init__(self, parent=None):
        super(maintenManage, self).__init__(parent)
        self.setupUi(self)
        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}

        self.tw_first.header().setVisible(False)
        self.tw_second.header().setVisible(False)

        self._initAll_()
        self.signalConnect()

    def _initAll_(self):
        self.first_treeWidget_dict = {}
        self.tw_first.clear()
        self._initUnitTreeWidget('', self.tw_first)
        self._initStrenInquiry()
        self.currentYear = None
        self.currentInquiryResult = {}
        self.resultList = []
        self.unitList = []
        self.equipList = []
        self.year = '全部'

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
        self._initUnitTreeWidget("", self.tw_first)
        self._initEquipTreeWidget("", self.tw_second)

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
            pass
            #resultListEquip = selectAboutStrengthByEquipShow(UnitList, EquipList, year)
            #resultListUnit = selectAboutStrengthByUnitShow(UnitList, EquipList, year)
            #resultList = resultListEquip + resultListUnit

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
            self.tw_result.setItem(i, 1, item)
            item = QTableWidgetItem(LineInfo[4])
            self.tw_result.setItem(i, 2, item)
            item = QTableWidgetItem(LineInfo[5])
            self.tw_result.setItem(i, 3, item)
            item = QTableWidgetItem(LineInfo[6])
            self.tw_result.setItem(i, 4, item)
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
    def _initSelectYear_(self):
        self.currentYearListItem = {}
        self.yearList = ['全部']
        self.lw_year.clear()
        allyearList = selectAllDataAboutWeaveYear()

        for year in allyearList:
            self.yearList.append(year[1])

        for year in self.yearList:
            item = QListWidgetItem()
            item.setText(year)
            self.lw_year.addItem(item)
            self.currentYearListItem[year[1]] = item

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