from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QTableWidgetItem, QAbstractItemView, \
    QMessageBox, QListWidgetItem,QInputDialog
from widgets.strengthDisturb.retirement import Widget_Retirement
from database.strengthDisturbSql import selectEquipInfoByEquipUper,selectUnitInfoByDeptUper,\
    selectAllRetirementYearInfo,selectAboutWeaveByEquipShow,selectAboutWeaveByEquipShow,\
    selectAboutRetireByEquipShow, isSecondDict,updateRetireAboutRetire,insertIntoRetireYear,delRetireYearByYear
from PyQt5.Qt import Qt

'''
   编制数维护
'''
class retirement(QWidget, Widget_Retirement):
    def __init__(self, parent=None):
        super(retirement, self).__init__(parent)
        self.setupUi(self)

        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}

        self.tw_first.header().setVisible(False)
        self.tw_second.header().setVisible(False)

        self._initAll_()
        self.signalConnect()

        # 初始化编制数维护界面

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
        self.groupBox_2.setDisabled(True)
        self.groupBox_3.setDisabled(True)

        # 信号连接
    def signalConnect(self):
        # 点击某个年份后显示单位和装备目录
        self.lw_year.clicked.connect(self.slotClickedInqury)

        # 当前单位目录被点击
        self.tw_first.clicked.connect(self.slotInquryStrengthResult)

        # 当前装备目录被点击
        self.tw_second.itemChanged.connect(self.slotInquryStrengthResult)
        self.tw_second.itemChanged.connect(self.slotCheckedChange)

        self.pb_save.clicked.connect(self.slotSaveRetire)
        self.tb_add.clicked.connect(self.slotAddNewYear)
        self.tb_del.clicked.connect(self.slotDelYear)

    def slotDelYear(self):
        currentRow = self.lw_year.currentRow()
        if currentRow == 0:
            reply = QMessageBox.question(self, '删除', '是否删除所有年份以及年份下所有数据？', QMessageBox.Yes, QMessageBox.Cancel)
            if QMessageBox.Cancel:
                return
        if currentRow < 0:
            reply = QMessageBox.question(self, '删除', '请选中某年进行删除', QMessageBox.Yes)
        else:
            currentYear = self.lw_year.currentItem().text()
            reply = QMessageBox.question(self, '删除', '是否删除当前年份以及当前年份下所有数据？', QMessageBox.Yes, QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                delRetireYearByYear(currentYear)
                self._initSelectYear_()
            else:
                return

    def slotAddNewYear(self):
        year = 0
        year, ok = QInputDialog.getInt(self, "Get year", "year:", 0, 0, 100000, 1)
        if year:
            insertIntoRetireYear(year)
            self._initSelectYear_()

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
        self.groupBox_2.setDisabled(False)
        self.groupBox_3.setDisabled(False)
        self.pb_save.setDisabled(True)
        #        self.tb_inqury.setDisabled(True)
        #        self.tb_rechoose.setDisabled(False)

        self.currentYear = self.lw_year.currentItem().text()
        self._initUnitTreeWidget("", self.tw_first)
        self._initEquipTreeWidget("", self.tw_second)

        # 查看当前被选中的单位和装备并初试化
    def slotInquryStrengthResult(self):
        self.currentCheckedUnitList = []
        self.currentCheckedEquipList = []
        for unitID, unitItem in self.first_treeWidget_dict.items():
            if unitItem == self.tw_first.currentItem():
                self.currentCheckedUnitList.append(unitID)
                break

        for equipID, equipItem in self.second_treeWidget_dict.items():
            if equipItem.checkState(0) == Qt.Checked or equipItem.checkState(0) == Qt.PartiallyChecked:
                self.currentCheckedEquipList.append(equipID)

        if self.currentCheckedUnitList == [] or self.currentCheckedEquipList == []:
            return
        else:
            self.pb_save.setDisabled(False)
            self._initTableWidgetByUnitListAndEquipList(self.currentCheckedUnitList, self.currentCheckedEquipList,
                                                        self.currentYear)
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

    # 初始化年份listwidget
    def _initSelectYear_(self):
        self.currentYearListItem = {}
        self.yearList = []
        self.lw_year.clear()
        allyearList = selectAllRetirementYearInfo()

        for year in allyearList:
            self.yearList.append(year[1])

        for year in self.yearList:
            item = QListWidgetItem()
            item.setText(year)
            self.lw_year.addItem(item)
            self.currentYearListItem[year[1]] = item

    # 初始化单位目录
    def _initUnitTreeWidget(self, root, mother):
        if root == '':
            result = selectUnitInfoByDeptUper('')
        else:
            result = selectUnitInfoByDeptUper(root)

            # rowData: (单位编号，单位名称，上级单位编号)
        for rowData in result:
            item = QTreeWidgetItem(mother)
            item.setText(0, rowData[1])
            self.first_treeWidget_dict[rowData[0]] = item
            self._initUnitTreeWidget(rowData[0], item)

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

    def _initTableWidgetByUnitListAndEquipList(self, currentCheckedUnitList, currentCheckedEquipList,currentYear):
        print(currentCheckedUnitList, currentCheckedEquipList, currentYear)
        currentClass = 0
        self.tw_result.clear()
        self.tw_result.setRowCount(0)
        self.unitList = currentCheckedUnitList
        self.equipList = currentCheckedEquipList
        self.year = currentYear
        self.resultList = []
        self.tw_result.horizontalHeader().setVisible(False)
        self.tw_result.verticalHeader().setVisible(False)
        self.currentInquiryResult.clear()

        self.tw_result.setColumnCount(9)
        self.tw_result.setRowCount(2)
        item = QTableWidgetItem()
        item.setText(currentYear + "年装备补充及退役需求表")
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(0, 0, item)
        self.tw_result.setSpan(0, 0, 1, 9)

        item = QTableWidgetItem()
        item.setText("序号")
        self.tw_result.setItem(1, 0, item)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        item = QTableWidgetItem()
        item.setText("装备名称")
        self.tw_result.setItem(1, 1, item)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        item = QTableWidgetItem()
        item.setText("单位")
        self.tw_result.setItem(1, 2, item)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        item = QTableWidgetItem()
        item.setText("编制数")
        self.tw_result.setItem(1, 3, item)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        item = QTableWidgetItem()
        item.setText("拟退役数")
        self.tw_result.setItem(1, 4, item)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        item = QTableWidgetItem()
        item.setText("现有数")
        self.tw_result.setItem(1, 5, item)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        item = QTableWidgetItem()
        item.setText("超/缺编制数")
        self.tw_result.setItem(1, 6, item)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        item = QTableWidgetItem()
        item.setText("申请需求")
        self.tw_result.setItem(1, 7, item)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        item = QTableWidgetItem()
        item.setText("备注")
        self.tw_result.setItem(1, 8, item)
        self.resultList = selectAboutRetireByEquipShow(currentCheckedUnitList, currentCheckedEquipList, currentYear)

        self.tw_result.setRowCount(len(self.resultList) + 2)
        classID = 1

        for i, LineInfo in enumerate(self.resultList):
            m_isSecond = isSecondDict(LineInfo[2])
            if m_isSecond:
                currentClass = currentClass + 1
                ID = chinese[currentClass]
                classID = 1
            else:
                ID = str(classID)
                classID = classID + 1
            item = QTableWidgetItem(ID)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 0, item)
            item = QTableWidgetItem(LineInfo[3])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 1, item)
            item = QTableWidgetItem(LineInfo[4])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.tw_result.setItem(i + 2, 2, item)
            item = QTableWidgetItem(LineInfo[5])
            self.tw_result.setItem(i + 2, 3, item)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            item = QTableWidgetItem(LineInfo[6])
            self.tw_result.setItem(i + 2, 4, item)
            item = QTableWidgetItem(LineInfo[7])
            self.tw_result.setItem(i + 2, 5, item)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            item = QTableWidgetItem(LineInfo[8])
            self.tw_result.setItem(i + 2, 6, item)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            item = QTableWidgetItem(LineInfo[9])
            self.tw_result.setItem(i + 2, 7, item)
            item = QTableWidgetItem(LineInfo[10])
            self.tw_result.setItem(i + 2, 8, item)
            self.currentInquiryResult[i] = LineInfo

    def slotSaveRetire(self):
        reply = QMessageBox.question(self, '修改', '是否保存修改？', QMessageBox.Cancel, QMessageBox.Yes)
        if reply == QMessageBox.Cancel:
            self._initTableWidgetByUnitListAndEquipList(self.currentCheckedUnitList, self.currentCheckedEquipList,
                                                        self.currentYear)
            return
        for i, result in self.currentInquiryResult.items():
            num = self.tw_result.item(i + 2, 4).text()
            apply = self.tw_result.item(i + 2, 7).text()
            other = self.tw_result.item(i + 2, 8).text()
            updateRetireAboutRetire(num, apply, other, result)

        reply = QMessageBox.question(self, '修改', '修改成功', QMessageBox.Yes)
        return



chinese = ['', '(一)', '(二)', '(三)', '(四)', '(五)','(六)','(七)']