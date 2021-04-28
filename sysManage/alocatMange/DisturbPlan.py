import sys
from PyQt5.QtWidgets import QWidget, QTreeWidgetItemIterator, QTreeWidgetItem, QMessageBox, QCheckBox
from widgets.alocatMange.yearListForm import yearList_Form
from sysManage.strengthDisturb.Stren_Inquiry import Stren_Inquiry
from database.strengthDisturbSql import *
from PyQt5.Qt import Qt


class DisturbPlan(QWidget, yearList_Form):
    def __init__(self, parent=None):
        super(DisturbPlan, self).__init__(parent)
        # Stren_Inquiry._initUnitTreeWidget()
        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}
        self.setupUi(self)
        self.signalConnect()
        self.signalDisconnectSlot()

    def signalConnect(self):
        # 点击选择年份后刷新页面 初始化
        self.lw_yearChoose.doubleClicked.connect(self.slotClickedInqury)
        # 按查询按钮时第一个目录的查询

        # 点击第一目录结果
        self.tw_first.itemChanged.connect(self.slotDisturbStrengthResult)
        # 按查询按钮时第二个目录的查询

        # 点击第二目录结果
        self.tw_second.itemChanged.connect(self.slotDisturbStrengthResult)
        # 按搜索框更改第一个目录的查询

        # 按搜索框更改第二个目录的查询

        # 将第一个目录和第二个目录进行关联
        # self.tw_first.currentItemChanged.connect(Stren_Inquiry.slotSelectIndex)
        # 第二个目录选定后进行查询并显示结果
        # self.tw_second.currentItemChanged.connect(Stren_Inquiry.slotInquiry)

    # 信号与槽连接的断开
    def signalDisconnectSlot(self):
        pass

    def slotClickedInqury(self):
        self.tw_first.clear()
        self.tw_second.clear()
        self.tw_first.header().setVisible(False)
        self.tw_second.header().setVisible(False)
        self.le_first.setDisabled(False)
        self.le_second.setDisabled(False)
        self.tw_first.setDisabled(False)
        self.tw_second.setDisabled(False)
        self._initUnitTreeWidget("", self.tw_first)
        self._initEquipTreeWidget("", self.tw_second)

    '''
        功能：
            设置级目录联选中状态0
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
            if rowData[0] != '':
                self._initUnitTreeWidget(rowData[0], item)

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
        self.yearList = ['2001']
        self.currentCheckedUnitChildList = []
        self.currentCheckedEquipList = []
        for unitID, unitItem in self.first_treeWidget_dict.items():
            if unitItem.checkState(0) == Qt.Checked:
                # self.currentCheckedUnitList.append(unitID)
                for i in findUnitChildName(unitID):
                    self.currentCheckedUnitChildList.append(i)

        for equipID, equipItem in self.second_treeWidget_dict.items():
            if equipItem.checkState(0) == Qt.Checked:
                self.currentCheckedEquipList.append(equipID)

        self._initDisturbPlanByUnitListAndEquipList(self.currentCheckedUnitChildList,
                                                    self.currentCheckedEquipList, self.yearList)

    def _initDisturbPlanByUnitListAndEquipList(self, UnitList, EquipList, YearList):
        self.disturbResult.clear()
        self.disturbResult.setRowCount(0)
        self.unitList = UnitList
        self.equipList = EquipList
        self.yearList = YearList
        ######################获取数据库数据
        disturbPlanList = selectDisturbPlan(UnitList, EquipList, YearList)

        headerlist = ['装备名称及规格型号', '单位', '军委分配计划数', '此次分配合计数']
        # unitList 返回选中unit子列表
        for i in unitList:
            headerlist.append(i)
        headerlist.append('库存')
        headerlist.append('备注')
        self.disturbResult.setHorizontalHeaderLabels(headerlist)
        self.currentInquiryResult.clear()
        self.disturbResult.setColumnCount(len(headerlist))
        self.disturbResult.setRowCount(len(resultList))

        i = 0
        n = len(unitList)
        for LineInfo in disturbPlanList:
            item = QTableWidgetItem(LineInfo[3])
            self.disturbResult.setItem(i, 0, item)
            item = QTableWidgetItem(LineInfo[2])
            self.disturbResult.setItem(i, 1, item)
            item = QTableWidgetItem(LineInfo[4])
            self.disturbResult.setItem(i, 2, item)
            item = QTableWidgetItem(LineInfo[5])
            self.disturbResult.setItem(i, 3, item)
            item = QTableWidgetItem(LineInfo[6])
            self.disturbResult.setItem(i, 4, item)
            item = QTableWidgetItem(LineInfo[7])
            self.disturbResult.setItem(i, 5, item)
            item = QTableWidgetItem(LineInfo[8])
            self.disturbResult.setItem(i, 6, item)
            item = QTableWidgetItem(LineInfo[9])
            self.disturbResult.setItem(i, 7, item)
            item = QTableWidgetItem(LineInfo[10])
            self.disturbResult.setItem(i, 8, item)
            item = QTableWidgetItem(LineInfo[11])
            self.disturbResult.setItem(i, 9, item)
            item = QTableWidgetItem(LineInfo[12])
            self.disturbResult.setItem(i, 10, item)
            item = QTableWidgetItem(LineInfo[13])
            self.disturbResult.setItem(i, 11, item)
            item = QTableWidgetItem(LineInfo[14])
            self.disturbResult.setItem(i, 12, item)

            self.currentInquiryResult[i] = LineInfo
            i = i + 1
        self.disturbResult.setRowCount(i)
