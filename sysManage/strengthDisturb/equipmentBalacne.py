import xlwt
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QTableWidgetItem, QAbstractItemView, \
    QMessageBox, QListWidgetItem, QInputDialog, QHeaderView, QFileDialog
from database.SD_EquipmentBanlanceSql import findYear, getResultByYearAndEquipAndUnit, saveEquipmentBalanceByRow
from widgets.strengthDisturb.retirement import Widget_Retirement
from database.strengthDisturbSql import *
from PyQt5.Qt import Qt
from sysManage.userInfo import get_value

'''
   编制数维护
'''
class equipmentBalance(QWidget, Widget_Retirement):
    def __init__(self, parent=None):
        super(equipmentBalance, self).__init__(parent)
        self.setupUi(self)

        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}

        self.tw_first.header().setVisible(False)
        self.tw_second.header().setVisible(False)
        self.userInfo = None
        self._initAll_()
        self.signalConnect()

        # 初始化编制数维护界面
    def getUserInfo(self):
        self.userInfo = get_value("totleUserInfo")
    def _initAll_(self):
        self.tb_add.setDisabled(True)
        self.tb_add.setVisible(False)
        self.tb_del.setDisabled(True)
        self.tb_del.setVisible(False)
        self.tw_result.setRowCount(0)
        self.tw_result.setColumnCount(0)
        self.tw_first.clear()
        self.tw_second.clear()
        self.le_first.clear()
        self.le_second.clear()
    
        self.getUserInfo()
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
        self.tw_first.clicked.connect(self.slotInquryEquipmentBalanceResult)
        # 当前装备目录被点击
        self.tw_second.clicked.connect(self.slotInquryEquipmentBalanceResult)
        self.tw_second.itemChanged.connect(self.slotCheckedChange)
        self.pb_save.clicked.connect(self.slotSaveEquipmentBalance)
        self.pb_firstSelect.clicked.connect(self.slotSelectUnit)
        self.tw_result.itemChanged.connect(self.soltCheckData)
        self.pb_secondSelect.clicked.connect(self.slotSelectEquip)
        self.pb_outputToExcel.clicked.connect(self.slotOutputToExcel)

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

    '''
           功能：
               点击查询按钮时，设置当前可选项和不可选项，并初始化装备和单位目录
    '''
    def slotClickedInqury(self):
        self.getUserInfo()
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

    def initEquipTreeWidget(self, stack, root):
        while stack:
            EquipInfo = stack.pop(0)
            item = QTreeWidgetItem(root.pop(0))
            item.setText(0, EquipInfo[1])
            item.setData(0,Qt.UserRole,QVariant(EquipInfo[0]))
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
            item.setText(0, UnitInfo[1])
            #item.setCheckState(0, Qt.Unchecked)
            self.first_treeWidget_dict[UnitInfo[0]] = item
            result = selectUnitInfoByDeptUper(UnitInfo[0])
            for resultInfo in result:
                stack.append(resultInfo)
                root.append(item)

        # 查看当前被选中的单位和装备并初始化
    def slotInquryEquipmentBalanceResult(self):
        self.currentCheckedUnitList = []
        self.currentCheckedEquipList = []
        for unitID, unitItem in self.first_treeWidget_dict.items():
            if unitItem == self.tw_first.currentItem():
                self.currentCheckedUnitList.append(unitID)
                break

        # for equipID, equipItem in self.second_treeWidget_dict.items():
        #     if equipItem.checkState(0) == Qt.Checked or equipItem.checkState(0) == Qt.PartiallyChecked:
        self.currentCheckedEquipList = self.get_checked(self.tw_second.topLevelItem(0))
        # print('-----------------------------')
        # print(self.currentCheckedEquipList)

        if self.currentCheckedEquipList == [] or self.currentCheckedUnitList == []:
            self.tw_result.setRowCount(2)
            self.tw_result.horizontalHeader().setVisible(False)
            self.tw_result.verticalHeader().setVisible(False)
            return
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
        allyearList = findYear()

        if allyearList != None:
            for year in allyearList:
                self.yearList.append(year)

            for year in self.yearList:
                item = QListWidgetItem()
                item.setText(year)
                self.lw_year.addItem(item)
                self.currentYearListItem[year] = item

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
        self.tw_result.itemChanged.disconnect(self.soltCheckData)
        self.checkBoxListItems = {}
        self.pb_save.setDisabled(True)
        currentClass = 0
        self.tw_result.clear()
        self.tw_result.setRowCount(0)
        self.unitList = currentCheckedUnitList
        self.equipList = currentCheckedEquipList
        self.lenOfColumn = 67

        self.year = currentYear
        self.resultList = []
        self.tw_result.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tw_result.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tw_result.resizeColumnsToContents()
        self.tw_result.resizeRowsToContents()
        self.tw_result.horizontalHeader().setVisible(False)
        self.tw_result.verticalHeader().setVisible(False)
        self.currentInquiryResult.clear()
        self.tw_result.setColumnCount(67)
        self.tw_result.setRowCount(4)
        self._initTableHeader()
        self.resultList = getResultByYearAndEquipAndUnit(currentYear, currentCheckedEquipList,currentCheckedUnitList)
        #填表
        if self.resultList is not None and len(self.resultList) is not 0:
            self.tw_result.setRowCount(len(self.resultList) + 4)
            # print(self.resultList)
            for row in range(len(self.resultList)):
                if selectEquipIsHaveChild(self.resultList[row].get('Equip_ID')) == False:
                    self.resultList[row][' lastLevel'] = True
                else:
                    self.resultList[row][' lastLevel'] = False
                item = QTableWidgetItem(self.resultList[row].get('Equip_Name'))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tw_result.setItem(row + 4, 0,item)

                item = QTableWidgetItem(self.resultList[row].get('original_authorized_value'))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tw_result.setItem(row + 4, 1,item)

                item =  QTableWidgetItem(self.resultList[row].get('authorized_value'))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tw_result.setItem(row + 4, 2,item)

                item = QTableWidgetItem(self.resultList[row].get('authorized_value_increase'))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tw_result.setItem(row + 4, 3,item)

                item =  QTableWidgetItem(self.resultList[row].get('authorized_value_decrease'))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tw_result.setItem(row + 4, 4,item)

                item = QTableWidgetItem(self.resultList[row].get('original_value'))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tw_result.setItem(row + 4, 5,item)
                self.tw_result.setItem(row + 4, 6,
                                       QTableWidgetItem(self.resultList[row].get('issue_new_product', '0')))
                self.tw_result.setItem(row + 4, 7,
                                       QTableWidgetItem(self.resultList[row].get('issue_inferior_product', '0')))
                self.tw_result.setItem(row + 4, 8,
                                       QTableWidgetItem(self.resultList[row].get('issue_need_repaired', '0')))
                self.tw_result.setItem(row + 4, 9,
                                       QTableWidgetItem(self.resultList[row].get('issue_need_retire', '0')))
                self.tw_result.setItem(row + 4, 10,
                                       QTableWidgetItem(self.resultList[row].get('report_new_product', '0')))
                self.tw_result.setItem(row + 4, 11,
                                       QTableWidgetItem(self.resultList[row].get('report_inferior_product', '0')))
                self.tw_result.setItem(row + 4, 12,
                                       QTableWidgetItem(self.resultList[row].get('report_need_repaired', '0')))
                self.tw_result.setItem(row + 4, 13,
                                       QTableWidgetItem(self.resultList[row].get('report_need_retire', '0')))

                item = QTableWidgetItem(self.resultList[row].get('change_value'))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tw_result.setItem(row + 4, 14,item)
                item = QTableWidgetItem(self.resultList[row].get('existing_value'))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tw_result.setItem(row + 4, 15, item)

                self.tw_result.setItem(row + 4, 16,
                                       QTableWidgetItem(self.resultList[row].get('increase_count', '0')))
                self.tw_result.setItem(row + 4, 17,
                                       QTableWidgetItem(self.resultList[row].get('increase_superior_supplement','0')))

                self.tw_result.setItem(row + 4, 18,
                                       QTableWidgetItem(self.resultList[row].get('increase_model_change', '0')))
                self.tw_result.setItem(row + 4, 19,
                                       QTableWidgetItem(self.resultList[row].get('increase_missing_reports', '0')))
                self.tw_result.setItem(row + 4, 20,
                                       QTableWidgetItem(self.resultList[row].get('increase_self_purchase', '0')))
                self.tw_result.setItem(row + 4, 21,
                                       QTableWidgetItem(self.resultList[row].get('increase_transfer_in', '0')))
                self.tw_result.setItem(row + 4, 22,
                                       QTableWidgetItem(self.resultList[row].get('increase_other', '0')))
                self.tw_result.setItem(row + 4, 23,
                                       QTableWidgetItem(self.resultList[row].get('reduce_count', '0')))
                self.tw_result.setItem(row + 4, 24,
                                       QTableWidgetItem(self.resultList[row].get('reduce_model_change', '0')))
                self.tw_result.setItem(row + 4, 25,
                                       QTableWidgetItem(self.resultList[row].get('reduce_callout', '0')))
                self.tw_result.setItem(row + 4, 26,
                                       QTableWidgetItem(self.resultList[row].get('reduce_train_consumption', '0')))
                self.tw_result.setItem(row + 4, 27,
                                       QTableWidgetItem(self.resultList[row].get('reduce_restatement', '0')))

                item = QTableWidgetItem(self.resultList[row].get('reduce_retire'))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tw_result.setItem(row + 4, 28, item)

                self.tw_result.setItem(row + 4, 29,
                                       QTableWidgetItem(self.resultList[row].get('reduce_scrap', '0')))
                self.tw_result.setItem(row + 4, 30,
                                       QTableWidgetItem(self.resultList[row].get('reduce_other', '0')))
                self.tw_result.setItem(row + 4, 31,
                                       QTableWidgetItem(self.resultList[row].get('unprepared_value', '0')))
                self.tw_result.setItem(row + 4, 32,
                                       QTableWidgetItem(self.resultList[row].get('unmatched_value', '0')))
                self.tw_result.setItem(row + 4, 33,
                                       QTableWidgetItem(self.resultList[row].get('uncutdown_value', '0')))
                self.tw_result.setItem(row + 4, 34,
                                       QTableWidgetItem(self.resultList[row].get('carry_count', '0')))
                self.tw_result.setItem(row + 4, 35,
                                       QTableWidgetItem(self.resultList[row].get('carry_new_product', '0')))
                self.tw_result.setItem(row + 4, 36,
                                       QTableWidgetItem(self.resultList[row].get('carry_inferior_product', '0')))
                self.tw_result.setItem(row + 4, 37,
                                       QTableWidgetItem(self.resultList[row].get('carry_need_repaired', '0')))
                self.tw_result.setItem(row + 4, 38,
                                       QTableWidgetItem(self.resultList[row].get('carry_need_retire', '0')))
                self.tw_result.setItem(row + 4, 39,
                                       QTableWidgetItem(self.resultList[row].get('carry_unprepared_value', '0')))
                self.tw_result.setItem(row + 4, 40,
                                       QTableWidgetItem(self.resultList[row].get('carryUn_cutdown_value', '0')))
                self.tw_result.setItem(row + 4, 41,
                                       QTableWidgetItem(self.resultList[row].get('stock_count', '0')))
                self.tw_result.setItem(row + 4, 42,
                                       QTableWidgetItem(self.resultList[row].get('stock_new_product', '0')))
                self.tw_result.setItem(row + 4, 43,
                                       QTableWidgetItem(self.resultList[row].get('stock_inferior_product', '0')))
                self.tw_result.setItem(row + 4, 44,
                                       QTableWidgetItem(self.resultList[row].get('stock_need_repaired', '0')))
                self.tw_result.setItem(row + 4, 45,
                                       QTableWidgetItem(self.resultList[row].get('stock_need_retire', '0')))
                self.tw_result.setItem(row + 4, 46,
                                       QTableWidgetItem(self.resultList[row].get('stock_unprepared_value', '0')))
                self.tw_result.setItem(row + 4, 47,
                                       QTableWidgetItem(self.resultList[row].get('stockUn_cutdown_value', '0')))
                self.tw_result.setItem(row + 4, 48,
                                       QTableWidgetItem(self.resultList[row].get('authorized_rate', '0')))
                self.tw_result.setItem(row + 4, 49,
                                       QTableWidgetItem(self.resultList[row].get('matched_rate', '0')))
                self.tw_result.setItem(row + 4, 50,
                                       QTableWidgetItem(self.resultList[row].get('instock_rate', '0')))
                self.tw_result.setItem(row + 4, 51,
                                       QTableWidgetItem(self.resultList[row].get('prepared_rate', '0')))
                self.tw_result.setItem(row + 4, 52,
                                       QTableWidgetItem(self.resultList[row].get('intact_rate', '0')))
                self.tw_result.setItem(row + 4, 53,
                                       QTableWidgetItem(self.resultList[row].get('never_repair', '0')))
                self.tw_result.setItem(row + 4, 54,
                                       QTableWidgetItem(self.resultList[row].get('once', '0')))
                self.tw_result.setItem(row + 4, 55,
                                       QTableWidgetItem(self.resultList[row].get('twice', '0')))
                self.tw_result.setItem(row + 4, 56,
                                       QTableWidgetItem(self.resultList[row].get('three_times', '0')))
                self.tw_result.setItem(row + 4, 57,
                                       QTableWidgetItem(self.resultList[row].get('More_than_three', '0')))
                self.tw_result.setItem(row + 4, 58,
                                       QTableWidgetItem(self.resultList[row].get('before1970','0')))
                self.tw_result.setItem(row + 4, 59,
                                       QTableWidgetItem(self.resultList[row].get('between1971and1975','0')))
                self.tw_result.setItem(row + 4, 60,
                                       QTableWidgetItem(self.resultList[row].get('between1976and1980', '0')))
                self.tw_result.setItem(row + 4, 61,
                                       QTableWidgetItem(self.resultList[row].get('between1981and1985', '0')))
                self.tw_result.setItem(row + 4, 62,
                                       QTableWidgetItem(self.resultList[row].get('between1986and1990','0')))
                self.tw_result.setItem(row + 4, 63,
                                       QTableWidgetItem(self.resultList[row].get('between1991and1995', '0')))
                self.tw_result.setItem(row + 4, 64,
                                       QTableWidgetItem(self.resultList[row].get('between1996and2000', '0')))
                self.tw_result.setItem(row + 4, 65,
                                       QTableWidgetItem(self.resultList[row].get('between2001and2005', '0')))
                self.tw_result.setItem(row + 4, 66,
                                       QTableWidgetItem(self.resultList[row].get('after2006', '0')))
        else:
            pass
      
        self.tw_result.itemChanged.connect(self.soltCheckData)

    def slotSaveEquipmentBalance(self):
        item = self.tw_result.currentItem()
        reply = QMessageBox.question(self, '修改', '是否保存修改？', QMessageBox.Yes,QMessageBox.Cancel)
        if reply == QMessageBox.Cancel:
            self._initTableWidgetByUnitListAndEquipList(self.currentCheckedUnitList, self.currentCheckedEquipList,
                                                        self.currentYear)
            return
        itemList = []
        for row in range(4, len(self.equipList) + 4):
            for column in range(self.lenOfColumn):
                item = self.tw_result.item(row, column)
                if item is None:
                    itemList.append('')
                else:
                    if len(item.text()) == 0:
                        itemList.append('')
                    else:
                        itemList.append(item.text())
            saveEquipmentBalanceByRow(itemList,self.currentCheckedUnitList[0], self.currentYear)
            itemList.clear()
        self._initTableWidgetByUnitListAndEquipList(self.currentCheckedUnitList, self.currentCheckedEquipList,
                                                   self.currentYear)
        return

    def soltCheckData(self,item):
        self.pb_save.setDisabled(False)

    def get_checked(self, node: QTreeWidgetItem) -> list:
        """ 得到当前节点选中的所有分支， 返回一个 list """
        temp_list = []
        # 此处看下方注释 1
        for item in node.takeChildren():
            # 判断是否选中
            if item.checkState(0) == Qt.Checked or item.checkState(0) == Qt.PartiallyChecked:
                temp_list.append(str(item.data(0,Qt.UserRole)))
                # 判断是否还有子分支
                if item.childCount():
                    temp_list.extend(self.get_checked(item))
            node.addChild(item)
        return temp_list
    
    def _initTableHeader(self):

        item = QTableWidgetItem("%s年%s装备平衡表"%(self.currentYear,selectUnitNameByUnitID(self.currentCheckedUnitList[0])))
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(0, 0, item)
        self.tw_result.setSpan(0, 0, 1, 67)
        # 绘制表头
        item = QTableWidgetItem("装备名称")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 0, item)
        self.tw_result.setSpan(1, 0, 3, 1)

        item = QTableWidgetItem("原有编制数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 1, item)
        self.tw_result.setSpan(1, 1, 3, 1)

        item = QTableWidgetItem("编制数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 2, item)
        self.tw_result.setSpan(1, 2, 3, 1)

        item = QTableWidgetItem("编制增数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 3, item)
        self.tw_result.setSpan(1, 3, 3, 1)

        item = QTableWidgetItem("编制减数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 4, item)
        self.tw_result.setSpan(1, 4, 3, 1)

        item = QTableWidgetItem("原有数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 5, item)
        self.tw_result.setSpan(1, 5, 3, 1)

        item = QTableWidgetItem("质量状况")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 6, item)
        self.tw_result.setSpan(1, 6, 1, 8)

        item = QTableWidgetItem("下发")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 6, item)
        self.tw_result.setSpan(2, 6, 1, 4)

        item = QTableWidgetItem("上报")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 10, item)
        self.tw_result.setSpan(2, 10, 1, 4)

        item = QTableWidgetItem("新品")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 6, item)
        item = QTableWidgetItem("堪品")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 7, item)
        item = QTableWidgetItem("待修")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 8, item)
        item = QTableWidgetItem("待退役")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 9, item)

        item = QTableWidgetItem("新品")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 10, item)
        item = QTableWidgetItem("堪品")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 11, item)
        item = QTableWidgetItem("待修")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 12, item)
        item = QTableWidgetItem("待退役")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 13, item)

        item = QTableWidgetItem("变化数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 14, item)
        self.tw_result.setSpan(1, 14, 3, 1)

        item = QTableWidgetItem("现有数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 15, item)
        self.tw_result.setSpan(1, 15, 3, 1)

        item = QTableWidgetItem("变化项目（增）")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 16, item)
        self.tw_result.setSpan(1, 16, 2, 7)

        item = QTableWidgetItem("变化项目（减）")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 23, item)
        self.tw_result.setSpan(1, 23, 2, 8)

        item = QTableWidgetItem("合计")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 16, item)
        item = QTableWidgetItem("上级补充")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 17, item)
        item = QTableWidgetItem("型号更正")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 18, item)
        item = QTableWidgetItem("漏报")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 19, item)
        item = QTableWidgetItem("自购")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 20, item)
        item = QTableWidgetItem("调入")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 21, item)
        item = QTableWidgetItem("其他增加")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 22, item)

        item = QTableWidgetItem("合计")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 23, item)
        item = QTableWidgetItem("型号更正")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 24, item)
        item = QTableWidgetItem("调出")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 25, item)
        item = QTableWidgetItem("训练消耗")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 26, item)
        item = QTableWidgetItem("重报")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 27, item)
        item = QTableWidgetItem("退役")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 28, item)
        item = QTableWidgetItem("报废")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 29, item)
        item = QTableWidgetItem("其他减少")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 30, item)

        item = QTableWidgetItem("未到位数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 31, item)
        self.tw_result.setSpan(1, 31, 3, 1)

        item = QTableWidgetItem("未到配套数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 32, item)
        self.tw_result.setSpan(1, 32, 3, 1)

        item = QTableWidgetItem("未削减数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 33, item)
        self.tw_result.setSpan(1, 33, 3, 1)

        item = QTableWidgetItem("携带数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 34, item)
        self.tw_result.setSpan(1, 34, 2, 7)

        item = QTableWidgetItem("合计")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 34, item)
        item = QTableWidgetItem("携带新品数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 35, item)
        item = QTableWidgetItem("携带堪品数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 36, item)
        item = QTableWidgetItem("携带待修数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 37, item)
        item = QTableWidgetItem("携带退役数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 38, item)
        item = QTableWidgetItem("未到位数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 39, item)
        item = QTableWidgetItem("未削减数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 40, item)

        item = QTableWidgetItem("库存")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 41, item)
        self.tw_result.setSpan(1, 41, 2, 7)

        item = QTableWidgetItem("合计")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 41, item)
        item = QTableWidgetItem("新品")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 42, item)
        item = QTableWidgetItem("堪品")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 43, item)
        item = QTableWidgetItem("待修")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 44, item)
        item = QTableWidgetItem("带退役")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 45, item)
        item = QTableWidgetItem("未到位数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 46, item)
        item = QTableWidgetItem("未削减数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 47, item)

        item = QTableWidgetItem("管理情况")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 48, item)
        self.tw_result.setSpan(1, 48, 2, 5)

        item = QTableWidgetItem("满编率")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 48, item)
        item = QTableWidgetItem("配套率")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 49, item)
        item = QTableWidgetItem("入库率")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 50, item)
        item = QTableWidgetItem("到位率")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 51, item)
        item = QTableWidgetItem("完好率")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 52, item)

        item = QTableWidgetItem("大修次数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 53, item)
        self.tw_result.setSpan(1, 53, 2, 5)

        item = QTableWidgetItem("未修")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 53, item)
        item = QTableWidgetItem("一次")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 54, item)
        item = QTableWidgetItem("二次")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 55, item)
        item = QTableWidgetItem("三次")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 56, item)
        item = QTableWidgetItem("三次以上")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 57, item)

        item = QTableWidgetItem("出厂年限")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 58, item)
        self.tw_result.setSpan(1, 58, 2, 9)

        item = QTableWidgetItem("70年以前")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 58, item)
        item = QTableWidgetItem("71至75年")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 59, item)
        item = QTableWidgetItem("76至80年")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 60, item)
        item = QTableWidgetItem("81至85年")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 61, item)
        item = QTableWidgetItem("86至90年")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 62, item)
        item = QTableWidgetItem("91至95年")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 63, item)
        item = QTableWidgetItem("96至2000年")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 64, item)
        item = QTableWidgetItem("2001至2005年")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 65, item)
        item = QTableWidgetItem("2006年以后")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.tw_result.setItem(3, 66, item)

    '''
        功能：
            导出到Excel表格
    '''
    def slotOutputToExcel(self):
        if len(self.resultList) < 1:
            reply = QMessageBox.warning(self, '警告', '未选中任何数据，无法导出!', QMessageBox.Yes)
            return
        reply = QMessageBox.question(self, '修改导出Excel', '是否保存修改并导出Excel？', QMessageBox.Cancel, QMessageBox.Yes)
        if reply == QMessageBox.Cancel:
            self._initTableWidgetByUnitListAndEquipList(self.currentCheckedUnitList, self.currentCheckedEquipList,
                                                        self.currentYear)
            return
        itemList = []
        for row in range(4, len(self.equipList) + 4):
            for column in range(self.lenOfColumn):
                item = self.tw_result.item(row, column)
                if item is None:
                    itemList.append('')
                else:
                    if len(item.text()) == 0:
                        itemList.append('')
                    else:
                        itemList.append(item.text())
            saveEquipmentBalanceByRow(itemList, self.currentCheckedUnitList[0], self.currentYear)
            itemList.clear()

        self._initTableWidgetByUnitListAndEquipList(self.currentCheckedUnitList, self.currentCheckedEquipList,
                                                    self.currentYear)

        directoryPath = QFileDialog.getExistingDirectory(self, "请选择导出文件夹", "c:/")
        if len(directoryPath) > 0 and '.' not in directoryPath:
            workBook = xlwt.Workbook(encoding='utf-8')
            workSheet = workBook.add_sheet('Sheet1')

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
            for i in range(66):
                workSheet.col(0).width = 4000
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

            #画Excel表头
            workSheet.write_merge(0, 0, 0, 66, "%s年%s装备平衡表" % (self.year, selectUnitNameByUnitID(self.currentCheckedUnitList[0])), headTitleStyle)
            workSheet.write_merge(1, 3, 0, 0, "装备名称" , titileStyle)
            workSheet.write_merge(1, 3, 1, 1, "原有编制数", titileStyle)
            workSheet.write_merge(1, 3, 2, 2, "编制数", titileStyle)
            workSheet.write_merge(1, 3, 3, 3, "编制增数", titileStyle)
            workSheet.write_merge(1, 3, 4, 4, "编制减数", titileStyle)
            workSheet.write_merge(1, 3, 5, 5, "原有数", titileStyle)
            workSheet.write_merge(1, 1, 6, 13, "质量状况", titileStyle)
            workSheet.write_merge(2, 2, 6, 9, "下发", titileStyle)
            workSheet.write_merge(2, 2, 10, 13, "上报", titileStyle)
            workSheet.write(3, 6, "新品", titileStyle)
            workSheet.write(3, 7, "堪品", titileStyle)
            workSheet.write(3, 8, "待修", titileStyle)
            workSheet.write(3, 9, "待退役", titileStyle)
            workSheet.write(3, 10, "新品", titileStyle)
            workSheet.write(3, 11, "堪品", titileStyle)
            workSheet.write(3, 12, "待修", titileStyle)
            workSheet.write(3, 13, "待退役", titileStyle)
            workSheet.write_merge(1, 3, 14, 14, "变化数", titileStyle)
            workSheet.write_merge(1, 3, 15, 15, "现有数", titileStyle)
            workSheet.write_merge(1, 2, 16, 22, "变化项目（增）", titileStyle)
            workSheet.write_merge(1, 2, 23, 30, "变化项目（减）", titileStyle)
            workSheet.write(3, 16, "合计", titileStyle)
            workSheet.write(3, 17, "上级补充", titileStyle)
            workSheet.write(3, 18, "型号更正", titileStyle)
            workSheet.write(3, 19, "漏报", titileStyle)
            workSheet.write(3, 20, "自购", titileStyle)
            workSheet.write(3, 21, "调入", titileStyle)
            workSheet.write(3, 22, "其他增加", titileStyle)
            workSheet.write(3, 23, "合计", titileStyle)
            workSheet.write(3, 24, "型号更正", titileStyle)
            workSheet.write(3, 25, "调出", titileStyle)
            workSheet.write(3, 26, "训练消耗", titileStyle)
            workSheet.write(3, 27, "重报", titileStyle)
            workSheet.write(3, 28, "退役", titileStyle)
            workSheet.write(3, 29, "报废", titileStyle)
            workSheet.write(3, 30, "其他减少", titileStyle)
            workSheet.write_merge(1, 3, 31, 31, "未到位数", titileStyle)
            workSheet.write_merge(1, 3, 32, 32, "未到配套数", titileStyle)
            workSheet.write_merge(1, 3, 33, 33, "未削减数", titileStyle)
            workSheet.write_merge(1, 2, 34, 40, "携带数", titileStyle)
            workSheet.write(3, 34, "合计", titileStyle)
            workSheet.write(3, 35, "携带新品数", titileStyle)
            workSheet.write(3, 36, "携带堪品数", titileStyle)
            workSheet.write(3, 37, "携带待修数", titileStyle)
            workSheet.write(3, 38, "携带退役数", titileStyle)
            workSheet.write(3, 39, "未到位数", titileStyle)
            workSheet.write(3, 40, "未削减数", titileStyle)
            workSheet.write_merge(1, 2, 41, 47, "库存", titileStyle)
            workSheet.write(3, 41, "合计", titileStyle)
            workSheet.write(3, 42, "新品", titileStyle)
            workSheet.write(3, 43, "堪品", titileStyle)
            workSheet.write(3, 44, "待修", titileStyle)
            workSheet.write(3, 45, "带退役", titileStyle)
            workSheet.write(3, 46, "未到位数", titileStyle)
            workSheet.write(3, 47, "未削减数", titileStyle)
            workSheet.write_merge(1, 2, 48, 52, "管理情况", titileStyle)
            workSheet.write(3, 48, "满编率", titileStyle)
            workSheet.write(3, 49, "配套率", titileStyle)
            workSheet.write(3, 50, "入库率", titileStyle)
            workSheet.write(3, 51, "到位率", titileStyle)
            workSheet.write(3, 52, "完好率", titileStyle)
            workSheet.write_merge(1, 2, 53, 57, "大修次数", titileStyle)
            workSheet.write(3, 53, "未修", titileStyle)
            workSheet.write(3, 54, "一次", titileStyle)
            workSheet.write(3, 55, "二次", titileStyle)
            workSheet.write(3, 56, "三次", titileStyle)
            workSheet.write(3, 57, "三次以上", titileStyle)
            workSheet.write_merge(1, 2, 58, 66, "出厂年限", titileStyle)
            workSheet.write(3, 58, "70年以前", titileStyle)
            workSheet.write(3, 59, "71至75年", titileStyle)
            workSheet.write(3, 60, "76至80年", titileStyle)
            workSheet.write(3, 61, "81至85年", titileStyle)
            workSheet.write(3, 62, "86至90年", titileStyle)
            workSheet.write(3, 63, "91至95年", titileStyle)
            workSheet.write(3, 64, "96至2000年", titileStyle)
            workSheet.write(3, 65, "2001至2005年", titileStyle)
            workSheet.write(3, 66, "2006年以后", titileStyle)

            #填写表格
            for row in range(len(self.resultList)):
                workSheet.write(row + 4, 0, self.resultList[row].get('Equip_Name'), contentStyle)
                workSheet.write(row + 4, 1, self.resultList[row].get('original_authorized_value'), contentStyle)
                workSheet.write(row + 4, 2, self.resultList[row].get('authorized_value'), contentStyle)
                workSheet.write(row + 4, 3, self.resultList[row].get('authorized_value_increase'), contentStyle)
                workSheet.write(row + 4, 4, self.resultList[row].get('authorized_value_decrease'), contentStyle)
                workSheet.write(row + 4, 5, self.resultList[row].get('original_value'), contentStyle)
                workSheet.write(row + 4, 6, self.resultList[row].get('authorized_value'), contentStyle)
                workSheet.write(row + 4, 7, self.resultList[row].get('issue_inferior_product','0'), contentStyle)
                workSheet.write(row + 4, 8, self.resultList[row].get('issue_need_repaired','0'), contentStyle)
                workSheet.write(row + 4, 9, self.resultList[row].get('issue_need_retire','0'), contentStyle)
                workSheet.write(row + 4, 10, self.resultList[row].get('report_new_product','0'), contentStyle)
                workSheet.write(row + 4, 11, self.resultList[row].get('report_inferior_product','0'), contentStyle)
                workSheet.write(row + 4, 12, self.resultList[row].get('report_need_repaired','0'), contentStyle)
                workSheet.write(row + 4, 13, self.resultList[row].get('report_need_retire','0'), contentStyle)
                workSheet.write(row + 4, 14, self.resultList[row].get('change_value','0'), contentStyle)
                workSheet.write(row + 4, 15, self.resultList[row].get('existing_value','0'), contentStyle)
                workSheet.write(row + 4, 16, self.resultList[row].get('increase_count','0'), contentStyle)
                workSheet.write(row + 4, 17, self.resultList[row].get('increase_superior_supplement','0'), contentStyle)
                workSheet.write(row + 4, 18, self.resultList[row].get('increase_model_change','0'), contentStyle)
                workSheet.write(row + 4, 19, self.resultList[row].get('increase_missing_reports','0'), contentStyle)
                workSheet.write(row + 4, 20, self.resultList[row].get('increase_self_purchase','0'), contentStyle)
                workSheet.write(row + 4, 21, self.resultList[row].get('increase_transfer_in','0'), contentStyle)
                workSheet.write(row + 4, 22, self.resultList[row].get('increase_other','0'), contentStyle)
                workSheet.write(row + 4, 23, self.resultList[row].get('reduce_count','0'), contentStyle)
                workSheet.write(row + 4, 24, self.resultList[row].get('reduce_model_change','0'), contentStyle)
                workSheet.write(row + 4, 25, self.resultList[row].get('reduce_callout','0'), contentStyle)
                workSheet.write(row + 4, 26, self.resultList[row].get('reduce_train_consumption','0'), contentStyle)
                workSheet.write(row + 4, 27, self.resultList[row].get('reduce_train_consumption','0'), contentStyle)
                workSheet.write(row + 4, 28, self.resultList[row].get('reduce_retire','0'), contentStyle)
                workSheet.write(row + 4, 29, self.resultList[row].get('reduce_scrap','0'), contentStyle)
                workSheet.write(row + 4, 30, self.resultList[row].get('reduce_other','0'), contentStyle)
                workSheet.write(row + 4, 31, self.resultList[row].get('unprepared_value','0'), contentStyle)
                workSheet.write(row + 4, 32, self.resultList[row].get('unmatched_value','0'), contentStyle)
                workSheet.write(row + 4, 33, self.resultList[row].get('uncutdown_value','0'), contentStyle)
                workSheet.write(row + 4, 34, self.resultList[row].get('carry_count','0'), contentStyle)
                workSheet.write(row + 4, 35, self.resultList[row].get('carry_new_product','0'), contentStyle)
                workSheet.write(row + 4, 36, self.resultList[row].get('carry_inferior_product','0'), contentStyle)
                workSheet.write(row + 4, 37, self.resultList[row].get('carry_need_repaired','0'), contentStyle)
                workSheet.write(row + 4, 38, self.resultList[row].get('carry_need_retire','0'), contentStyle)
                workSheet.write(row + 4, 39, self.resultList[row].get('carry_unprepared_value','0'), contentStyle)
                workSheet.write(row + 4, 40, self.resultList[row].get('carryUn_cutdown_value','0'), contentStyle)
                workSheet.write(row + 4, 41, self.resultList[row].get('stock_count','0'), contentStyle)
                workSheet.write(row + 4, 42, self.resultList[row].get('stock_new_product','0'), contentStyle)
                workSheet.write(row + 4, 43, self.resultList[row].get('stock_inferior_product','0'), contentStyle)
                workSheet.write(row + 4, 44, self.resultList[row].get('stock_need_repaired','0'), contentStyle)
                workSheet.write(row + 4, 45, self.resultList[row].get('stock_need_retire','0'), contentStyle)
                workSheet.write(row + 4, 46, self.resultList[row].get('stock_unprepared_value','0'), contentStyle)
                workSheet.write(row + 4, 47, self.resultList[row].get('stockUn_cutdown_value','0'), contentStyle)
                workSheet.write(row + 4, 48, self.resultList[row].get('authorized_rate','0'), contentStyle)
                workSheet.write(row + 4, 49, self.resultList[row].get('matched_rate','0'), contentStyle)
                workSheet.write(row + 4, 50, self.resultList[row].get('instock_rate','0'), contentStyle)
                workSheet.write(row + 4, 51, self.resultList[row].get('prepared_rate','0'), contentStyle)
                workSheet.write(row + 4, 52, self.resultList[row].get('intact_rate','0'), contentStyle)
                workSheet.write(row + 4, 53, self.resultList[row].get('never_repair','0'), contentStyle)
                workSheet.write(row + 4, 54, self.resultList[row].get('once','0'), contentStyle)
                workSheet.write(row + 4, 55, self.resultList[row].get('twice','0'), contentStyle)
                workSheet.write(row + 4, 56, self.resultList[row].get('three_times','0'), contentStyle)
                workSheet.write(row + 4, 57, self.resultList[row].get('More_than_three','0'), contentStyle)
                workSheet.write(row + 4, 58, self.resultList[row].get('before1970','0'), contentStyle)
                workSheet.write(row + 4, 59, self.resultList[row].get('between1971and1975','0'), contentStyle)
                workSheet.write(row + 4, 60, self.resultList[row].get('between1976and1980','0'), contentStyle)
                workSheet.write(row + 4, 61, self.resultList[row].get('between1981and1985','0'), contentStyle)
                workSheet.write(row + 4, 62, self.resultList[row].get('between1986and1990','0'), contentStyle)
                workSheet.write(row + 4, 63, self.resultList[row].get('between1991and1995','0'), contentStyle)
                workSheet.write(row + 4, 64, self.resultList[row].get('between1996and2000','0'), contentStyle)
                workSheet.write(row + 4, 65, self.resultList[row].get('between2001and2005','0'), contentStyle)
                workSheet.write(row + 4, 66, self.resultList[row].get('after2006','0'), contentStyle)


            try:
                pathName = "%s/%s年%s装备平衡表.xls" % (directoryPath, self.year,selectUnitNameByUnitID(self.currentCheckedUnitList[0]))
                workBook.save(pathName)
                import win32api
                win32api.ShellExecute(0, 'open', pathName, '', '', 1)
                QMessageBox.about(self, "导出成功", "导出成功！")
                return
            except Exception as e:
                QMessageBox.about(self, "导出失败", "导出表格被占用，请关闭正在使用的Execl！")
                return
        else:
            QMessageBox.about(self, "选取文件夹失败！", "请选择正确的文件夹！")

