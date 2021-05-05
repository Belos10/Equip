import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QTableWidgetItem, QTableWidget, QTreeWidgetItem, \
    QHeaderView
from database.SD_EquipmentBanlanceSql import *
from database.strengthDisturbSql import *
from widgets.strengthDisturb.equipmentBalance.equipmentBalanceSelectUI import EquipmentBalanceSelectUI

first_treeWidget_dict = {}
second_treeWidget_dict = {}
class Equip_Balance_Select(QWidget, EquipmentBalanceSelectUI):
    def __init__(self, parent=None):
        super(Equip_Balance_Select, self).__init__(parent)
        self.setupUi(self)
        # 当前选中的单位列表和装备列表
        self.currentCheckedUnitList = []
        self.currentCheckedEquipList = []
        # 设置当前查询的年份
        self.currentYear = 0
        self.currentInquiryResult = {}
        self.unitList = []
        self.equipList = []
        self.year = None
        self.result = []
        # 初始化界面
        self._initEquipmentBlanceSelect()
        # 信号连接
        self.signalConnectSlot()




    # 信号与槽的连接
    def signalConnectSlot(self):
        # 当前单位目录被点击
        # self.tw_first.itemChanged.connect(self.slotSelectedResult)

        # 当前装备目录被点击
        self.tw_second.itemChanged.connect(self.slotSelectedResult)
        #
        self.pb_firstSelect.clicked.connect(self.slotClickedInqury)
        self.pb_secondSelect.clicked.connect(self.slotClickedInqury)

    # 信号与槽连接的断开
    def signalDisconnectSlot(self):
        pass




    def _initEquipmentBlanceSelect(self):
        self.tw_first.clear()
        self.tw_second.clear()
        self.tw_first.header().setVisible(False)
        self.tw_second.header().setVisible(False)
        self.le_first.setDisabled(False)
        self.le_second.setDisabled(False)
        self.tw_first.setDisabled(True)
        self.tw_first.setVisible(False)
        self.pb_firstSelect.setVisible(False)
        self.pb_firstSelect.setDisabled(True)
        self.le_first.setVisible(False)
        self.le_first.setDisabled(True)
        self.tw_second.setDisabled(False)
        self.tb_result.setDisabled(False)
        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}
        # 当前选中的单位列表和装备列表
        self.currentCheckedUnitList = []
        self.currentCheckedEquipList = []
        # self._initUnitTreeWidget("", self.tw_first)
        self._initEquipTreeWidget("", self.tw_second)
        self._initTableHeader()


    def slotClickedInqury(self):
        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}
        self.tw_first.clear()
        self.tw_second.clear()
        self.tw_first.setVisible(False)
        self.tw_first.header().setVisible(False)
        self.tw_second.header().setVisible(False)
        self.le_first.setDisabled(False)
        self.le_second.setDisabled(False)
        self.tw_first.setDisabled(False)
        self.tw_second.setDisabled(False)
        self.tb_result.setDisabled(False)

        self._initUnitTreeWidget("", self.tw_first)
        self._initEquipTreeWidget("", self.tw_second)




    # def slotSaveUpdate(self):


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
        功能：
            查询实力结果
    '''
    def slotSelectedResult(self):
        self.currentCheckedEquipList = []
        for equipID, equipItem in self.second_treeWidget_dict.items():
            if equipItem.checkState(0) == Qt.Checked:
                self.currentCheckedEquipList.append(equipID)
        #初始化单位和装备目录
        self._initTableWidgetByUnitListAndEquipList(self.currentCheckedEquipList, self.currentYear)

    # 初始化tableWidget
    def _initTableWidgetByUnitListAndEquipList(self, EquipList, year):
        self.tb_result.clear()
        self._initTableHeader()
        self.tb_result.setRowCount(3)
        self.equipList = EquipList
        self.currentInquiryResult.clear()
        self.lenOfColumn = 66
        self.tb_result.setColumnCount(self.lenOfColumn)
        resultList = getResultByYearAndEquip(year,self.equipList)
        print(resultList)
        if resultList is not None and len(resultList) is not 0:
            self.tb_result.setRowCount(len(resultList) + 3)
            for row in range(len(resultList)):
                print(row)

                print(resultList[row]['Equip_Name'])
                self.tb_result.setItem(row + 3, 0,
                                       QTableWidgetItem(resultList[row]['Equip_Name']))
                self.tb_result.setItem(row + 3,  1,
                                       QTableWidgetItem(resultList[row]['original_authorized_value']))
                self.tb_result.setItem(row + 3,  2,
                                       QTableWidgetItem(resultList[row]['authorized_value']))
                self.tb_result.setItem(row + 3,  3,
                                       QTableWidgetItem(resultList[row]['authorized_value_change']))
                self.tb_result.setItem(row + 3,  4,
                                       QTableWidgetItem(resultList[row]['original_value']))
                self.tb_result.setItem(row + 3,  5,
                                       QTableWidgetItem(resultList[row]['issue_new_product']))
                self.tb_result.setItem(row + 3,  6,
                                       QTableWidgetItem(resultList[row]['issue_inferior_product']))
                self.tb_result.setItem(row + 3,  7,
                                       QTableWidgetItem(resultList[row]['issue_need_repaired']))
                self.tb_result.setItem(row + 3,  8,
                                       QTableWidgetItem(resultList[row]['issue_need_retire']))
                self.tb_result.setItem(row + 3, 9,
                                       QTableWidgetItem(resultList[row]['report_new_product']))
                self.tb_result.setItem(row + 3, 10,
                                       QTableWidgetItem(resultList[row]['report_inferior_product']))
                self.tb_result.setItem(row + 3, 11,
                                       QTableWidgetItem(resultList[row]['report_need_repaired']))
                self.tb_result.setItem(row + 3, 12,
                                       QTableWidgetItem(resultList[row]['report_need_retire']))
                self.tb_result.setItem(row + 3, 13,
                                       QTableWidgetItem(resultList[row]['change_value']))
                self.tb_result.setItem(row + 3, 14,
                                       QTableWidgetItem(resultList[row]['existing_value']))
                self.tb_result.setItem(row + 3, 15,
                                       QTableWidgetItem(resultList[row]['increase_count']))
                self.tb_result.setItem(row + 3, 16,
                                       QTableWidgetItem(resultList[row]['increase_superior_supplement']))
                self.tb_result.setItem(row + 3, 17,
                                       QTableWidgetItem(resultList[row]['increase_model_change']))
                self.tb_result.setItem(row + 3, 18,
                                       QTableWidgetItem(resultList[row]['increase_missing_reports']))
                self.tb_result.setItem(row + 3, 19,
                                       QTableWidgetItem(resultList[row]['increase_self_purchase']))
                self.tb_result.setItem(row + 3, 20,
                                       QTableWidgetItem(resultList[row]['increase_transfer_in']))
                self.tb_result.setItem(row + 3, 21,
                                       QTableWidgetItem(resultList[row]['increase_other']))
                self.tb_result.setItem(row + 3, 22,
                                       QTableWidgetItem(resultList[row]['reduce_count']))
                self.tb_result.setItem(row + 3, 23,
                                       QTableWidgetItem(resultList[row]['reduce_model_change']))
                self.tb_result.setItem(row + 3, 24,
                                       QTableWidgetItem(resultList[row]['reduce_callout']))
                self.tb_result.setItem(row + 3, 25,
                                       QTableWidgetItem(resultList[row]['reduce_train_consumption']))
                self.tb_result.setItem(row + 3, 26,
                                       QTableWidgetItem(resultList[row]['reduce_restatement']))
                self.tb_result.setItem(row + 3, 27,
                                       QTableWidgetItem(resultList[row]['reduce_retire']))
                self.tb_result.setItem(row + 3, 28,
                                       QTableWidgetItem(resultList[row]['reduce_scrap']))
                self.tb_result.setItem(row + 3, 29,
                                       QTableWidgetItem(resultList[row]['reduce_other']))
                self.tb_result.setItem(row + 3, 30,
                                       QTableWidgetItem(resultList[row]['unprepared_value']))
                self.tb_result.setItem(row + 3, 31,
                                       QTableWidgetItem(resultList[row]['unmatched_value']))
                self.tb_result.setItem(row + 3, 32,
                                       QTableWidgetItem(resultList[row]['uncutdown_value']))
                self.tb_result.setItem(row + 3, 33,
                                       QTableWidgetItem(resultList[row]['carry_count']))
                self.tb_result.setItem(row + 3, 34,
                                       QTableWidgetItem(resultList[row]['carry_new_product']))
                self.tb_result.setItem(row + 3, 35,
                                       QTableWidgetItem(resultList[row]['carry_inferior_product']))
                self.tb_result.setItem(row + 3, 36,
                                       QTableWidgetItem(resultList[row]['carry_need_repaired']))
                self.tb_result.setItem(row + 3, 37,
                                       QTableWidgetItem(resultList[row]['carry_need_retire']))
                self.tb_result.setItem(row + 3, 38,
                                       QTableWidgetItem(resultList[row]['carry_unprepared_value']))
                self.tb_result.setItem(row + 3, 39,
                                       QTableWidgetItem(resultList[row]['carryUn_cutdown_value']))
                self.tb_result.setItem(row + 3, 40,
                                       QTableWidgetItem(resultList[row]['stock_count']))
                self.tb_result.setItem(row + 3, 41,
                                       QTableWidgetItem(resultList[row]['stock_new_product']))
                self.tb_result.setItem(row + 3, 42,
                                       QTableWidgetItem(resultList[row]['stock_inferior_product']))
                self.tb_result.setItem(row + 3, 43,
                                       QTableWidgetItem(resultList[row]['stock_need_repaired']))
                self.tb_result.setItem(row + 3, 44,
                                       QTableWidgetItem(resultList[row]['stock_need_retire']))
                self.tb_result.setItem(row + 3, 45,
                                       QTableWidgetItem(resultList[row]['stock_unprepared_value']))
                self.tb_result.setItem(row + 3, 46,
                                       QTableWidgetItem(resultList[row]['stockUn_cutdown_value']))
                self.tb_result.setItem(row + 3, 47,
                                       QTableWidgetItem(resultList[row]['authorized_rate']))
                self.tb_result.setItem(row + 3, 48,
                                       QTableWidgetItem(resultList[row]['matched_rate']))
                self.tb_result.setItem(row + 3, 49,
                                       QTableWidgetItem(resultList[row]['instock_rate']))
                self.tb_result.setItem(row + 3, 50,
                                       QTableWidgetItem(resultList[row]['prepared_rate']))
                self.tb_result.setItem(row + 3, 51,
                                       QTableWidgetItem(resultList[row]['intact_rate']))
                self.tb_result.setItem(row + 3, 52,
                                       QTableWidgetItem(resultList[row]['never_repair']))
                self.tb_result.setItem(row + 3, 53,
                                       QTableWidgetItem(resultList[row]['once']))
                self.tb_result.setItem(row + 3, 54,
                                       QTableWidgetItem(resultList[row]['twice']))
                self.tb_result.setItem(row + 3, 55,
                                       QTableWidgetItem(resultList[row]['three_times']))
                self.tb_result.setItem(row + 3, 56,
                                       QTableWidgetItem(resultList[row]['More_than_three']))
                self.tb_result.setItem(row + 3, 57,
                                       QTableWidgetItem(resultList[row]['before1970']))
                self.tb_result.setItem(row + 3, 58,
                                       QTableWidgetItem(resultList[row]['between1971and1975']))
                self.tb_result.setItem(row + 3, 59,
                                       QTableWidgetItem(resultList[row]['between1976and1980']))
                self.tb_result.setItem(row + 3, 60,
                                       QTableWidgetItem(resultList[row]['between1981and1985']))
                self.tb_result.setItem(row + 3, 61,
                                       QTableWidgetItem(resultList[row]['between1986and1990']))
                self.tb_result.setItem(row + 3, 62,
                                       QTableWidgetItem(resultList[row]['between1991and1995']))
                self.tb_result.setItem(row + 3, 63,
                                       QTableWidgetItem(resultList[row]['between1996and2000']))
                self.tb_result.setItem(row + 3, 64,
                                       QTableWidgetItem(resultList[row]['between2001and2005']))
                self.tb_result.setItem(row + 3, 65,
                                       QTableWidgetItem(resultList[row]['after2006']))
        else:
            pass


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


    def _initTableHeader(self):
        self.tb_result.verticalHeader().setVisible(False)
        self.tb_result.horizontalHeader().setVisible(False)
        self.tb_result.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tb_result.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tb_result.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tb_result.resizeColumnsToContents()
        self.tb_result.resizeRowsToContents()

        # 绘制表头
        item = QTableWidgetItem("装备名称")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(0, 0, item)
        self.tb_result.setSpan(0, 0, 3, 1)

        item = QTableWidgetItem("原有编制数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(0, 1, item)
        self.tb_result.setSpan(0, 1, 3, 1)

        item = QTableWidgetItem("编制数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(0, 2, item)
        self.tb_result.setSpan(0, 2, 3, 1)

        item = QTableWidgetItem("编制增减数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(0, 3, item)
        self.tb_result.setSpan(0, 3, 3, 1)

        item = QTableWidgetItem("原有数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(0, 4, item)
        self.tb_result.setSpan(0, 4, 3, 1)

        item = QTableWidgetItem("质量状况")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(0, 5, item)
        self.tb_result.setSpan(0, 5, 3, 8)

        item = QTableWidgetItem("下发")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(1, 5, item)
        self.tb_result.setSpan(1, 5, 3, 4)

        item = QTableWidgetItem("上报")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(1, 9, item)
        self.tb_result.setSpan(1, 9, 3, 4)

        item = QTableWidgetItem("新品")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 5, item)
        item = QTableWidgetItem("堪品")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 6, item)
        item = QTableWidgetItem("待修")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 7, item)
        item = QTableWidgetItem("待退役")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 8, item)

        item = QTableWidgetItem("新品")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 9, item)
        item = QTableWidgetItem("堪品")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 10, item)
        item = QTableWidgetItem("待修")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 11, item)
        item = QTableWidgetItem("待退役")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 12, item)

        item = QTableWidgetItem("变化数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(0, 13, item)
        self.tb_result.setSpan(0, 13, 3, 1)

        item = QTableWidgetItem("现有数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(0, 14, item)
        self.tb_result.setSpan(0, 14, 3, 1)

        item = QTableWidgetItem("变化项目（增）")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(0, 15, item)
        self.tb_result.setSpan(0, 15, 2, 7)

        item = QTableWidgetItem("变化项目（减）")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(0, 22, item)
        self.tb_result.setSpan(0, 22, 2, 8)

        item = QTableWidgetItem("合计")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 15, item)
        item = QTableWidgetItem("上级补充")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 16, item)
        item = QTableWidgetItem("型号更正")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 17, item)
        item = QTableWidgetItem("漏报")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 18, item)
        item = QTableWidgetItem("自购")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 19, item)
        item = QTableWidgetItem("调入")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 20, item)
        item = QTableWidgetItem("其他增加")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 21, item)

        item = QTableWidgetItem("合计")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 22, item)
        item = QTableWidgetItem("型号更正")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 23, item)
        item = QTableWidgetItem("调出")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 24, item)
        item = QTableWidgetItem("训练消耗")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 25, item)
        item = QTableWidgetItem("重报")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 26, item)
        item = QTableWidgetItem("退役")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 27, item)
        item = QTableWidgetItem("报废")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 28, item)
        item = QTableWidgetItem("其他减少")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 29, item)

        item = QTableWidgetItem("未到位数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(0, 30, item)
        self.tb_result.setSpan(0, 30, 3, 1)

        item = QTableWidgetItem("未到配套数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(0, 31, item)
        self.tb_result.setSpan(0, 31, 3, 1)

        item = QTableWidgetItem("未削减数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(0, 32, item)
        self.tb_result.setSpan(0, 32, 3, 1)

        item = QTableWidgetItem("携带数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(0, 33, item)
        self.tb_result.setSpan(0, 33, 2, 7)

        item = QTableWidgetItem("合计")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 33, item)
        item = QTableWidgetItem("携带新品数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 34, item)
        item = QTableWidgetItem("携带堪品数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 35, item)
        item = QTableWidgetItem("携带待修数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 36, item)
        item = QTableWidgetItem("携带退役数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 37, item)
        item = QTableWidgetItem("未到位数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 38, item)
        item = QTableWidgetItem("未削减数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 39, item)

        item = QTableWidgetItem("库存")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(0, 40, item)
        self.tb_result.setSpan(0, 40, 2, 7)

        item = QTableWidgetItem("合计")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 40, item)
        item = QTableWidgetItem("新品")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 41, item)
        item = QTableWidgetItem("堪品")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 42, item)
        item = QTableWidgetItem("待修")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 43, item)
        item = QTableWidgetItem("带退役")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 44, item)
        item = QTableWidgetItem("未到位数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 45, item)
        item = QTableWidgetItem("未削减数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 46, item)

        item = QTableWidgetItem("管理情况")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(0, 47, item)
        self.tb_result.setSpan(0, 47, 2, 5)

        item = QTableWidgetItem("满编率")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 47, item)
        item = QTableWidgetItem("配套率")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 48, item)
        item = QTableWidgetItem("入库率")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 49, item)
        item = QTableWidgetItem("到位率")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 50, item)
        item = QTableWidgetItem("完好率")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 51, item)

        item = QTableWidgetItem("大修次数")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(0, 52, item)
        self.tb_result.setSpan(0, 52, 2, 5)

        item = QTableWidgetItem("未修")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 52, item)
        item = QTableWidgetItem("一次")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 53, item)
        item = QTableWidgetItem("二次")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 54, item)
        item = QTableWidgetItem("三次")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 55, item)
        item = QTableWidgetItem("三次以上")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 56, item)

        item = QTableWidgetItem("出场年限")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(0, 57, item)
        self.tb_result.setSpan(0, 57, 2, 9)

        item = QTableWidgetItem("70年以前")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 57, item)
        item = QTableWidgetItem("71至75年")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 58, item)
        item = QTableWidgetItem("76至80年")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 59, item)
        item = QTableWidgetItem("81至85年")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 60, item)
        item = QTableWidgetItem("86至90年")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 61, item)
        item = QTableWidgetItem("91至95年")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 62, item)
        item = QTableWidgetItem("96至2000年")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 63, item)
        item = QTableWidgetItem("2001至2005年")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 64, item)
        item = QTableWidgetItem("2006年以后")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 65, item)















if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Equip_Balance_Select()
    widget.show()
    sys.exit(app.exec_())