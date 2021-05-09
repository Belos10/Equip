import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QTableWidgetItem, QTableWidget, QTreeWidgetItem, \
    QHeaderView
from database.SD_EquipmentBanlanceSql import *
from database.strengthDisturbSql import *
from widgets.strengthDisturb.applyRetirement.applyRetirementSelectUI import ApplyRetirementSelectUI

first_treeWidget_dict = {}
second_treeWidget_dict = {}
class Apply_Retirement_Select(QWidget, ApplyRetirementSelectUI):
    def __init__(self, parent=None):
        super(Apply_Retirement_Select, self).__init__(parent)
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
        self._initApplyRetirementSelect()
        # 信号连接
        self.signalConnectSlot()




    # 信号与槽的连接
    def signalConnectSlot(self):
        # 当前单位目录被点击
        self.tw_first.itemChanged.connect(self.slotSelectedResult)

        # 当前装备目录被点击
        self.tw_second.itemChanged.connect(self.slotSelectedResult)
        #
        self.pb_firstSelect.clicked.connect(self.slotClickedInqury)
        self.pb_secondSelect.clicked.connect(self.slotClickedInqury)

    # 信号与槽连接的断开
    def signalDisconnectSlot(self):
        pass




    def _initApplyRetirementSelect(self):
        self.tw_first.clear()
        self.tw_second.clear()
        self.tw_first.header().setVisible(False)
        self.tw_second.header().setVisible(False)
        self.le_first.setDisabled(False)
        self.le_second.setDisabled(False)
        self.tw_first.setDisabled(False)
        self.tw_first.setVisible(True)
        self.pb_firstSelect.setVisible(True)
        self.pb_firstSelect.setDisabled(False)
        self.le_first.setVisible(True)
        self.le_first.setDisabled(False)
        self.tw_second.setDisabled(False)
        self.tb_result.setDisabled(False)
        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}
        # 当前选中的单位列表和装备列表
        self.currentCheckedUnitList = []
        self.currentCheckedEquipList = []
        self._initUnitTreeWidget("",self.tw_first)
        self._initEquipTreeWidget("", self.tw_second)



    def slotClickedInqury(self):
        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}
        self.tw_first.clear()
        self.tw_second.clear()
        self.tw_first.setVisible(True)
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
            查询结果
    '''
    def slotSelectedResult(self):
        # self.yearList = ['2001']
        self.currentCheckedUnitList = []
        self.currentCheckedEquipList = []
        for unitID, unitItem in self.first_treeWidget_dict.items():
            if unitItem.checkState(0) == Qt.Checked:
                self.currentCheckedUnitList.append(unitID)

        for equipID, equipItem in self.second_treeWidget_dict.items():
            if equipItem.checkState(0) == Qt.Checked:
                self.currentCheckedEquipList.append(equipID)

        self._initTableWidgetByUnitListAndEquipList(self.currentCheckedUnitList, self.currentCheckedEquipList)

    # 初始化tableWidget
    def _initTableWidgetByUnitListAndEquipList(self, UnitList, EquipList):
        self.tb_result.clear()
        self.equipList = EquipList
        self.unitList = UnitList
        self.currentInquiryResult.clear()
        self.displayData()



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
            if rowData[0] != '':
                self._initUnitTreeWidget(rowData[0], item)


    def displayData(self):

        if len(self.equipList) == 0 or len(self.unitList) == 0:
            self.tb_result.setRowCount(0)
            self.tb_result.setColumnCount(0)
            self.tb_result.clearContents()
            return
        self.resultRowLength = len(self.equipList) + 3
        self.resultColumnLength = len(self.unitList) * 5 + 2
        self.tb_result.setColumnCount(self.resultColumnLength)
        self.tb_result.setRowCount(self.resultRowLength)
        self.tb_result.horizontalHeader().setVisible(False)
        self.tb_result.verticalHeader().setVisible(False)
        self.tb_result.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tb_result.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents) #ResizeToContents
        self.tb_result.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tb_result.resizeColumnsToContents()
        self.tb_result.resizeRowsToContents()
        item = QTableWidgetItem("%s年度装备补充及退役需求表" % self.currentYear)
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(0, 0, item)
        self.tb_result.setSpan(0, 0, 1, self.resultColumnLength)
        #绘制表头
        item = QTableWidgetItem("装备名称")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 0, item)
        item = QTableWidgetItem("单位")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tb_result.setItem(2, 1, item)
        self.unitList.sort()
        self.equipList.sort()

        for i in range(len(self.equipList)):
            rowIndex = 3 + i
            item = QTableWidgetItem(getEquipmentNameByID(self.equipList[i]))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tb_result.setItem(rowIndex, 0, item)
            item = QTableWidgetItem(getEquipmentTypeByID(self.equipList[i]))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tb_result.setItem(rowIndex, 1, item)
            for j in range(len(self.unitList)):
                data = getDataByUnitIdAndEquipmentId(self.currentYear, self.unitList[j], self.equipList[i])
                columnIndex = 2 + 5 * j
                if(data is not None):
                    item = QTableWidgetItem(data['Unit_Name'])
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tb_result.setItem(1, columnIndex, item)
                    self.tb_result.setSpan(1, columnIndex, 1, 5)
                    item = QTableWidgetItem('编制数')
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tb_result.setItem(2,columnIndex, item)
                    item = QTableWidgetItem(data['authorized_value'])
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tb_result.setItem(rowIndex, columnIndex, item)
                    item = QTableWidgetItem('拟退役数')
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tb_result.setItem(2, columnIndex + 1, item)
                    item = QTableWidgetItem(data['plan_to_retire'])
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tb_result.setItem(rowIndex, columnIndex + 1, item)
                    item = QTableWidgetItem('现有数')
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tb_result.setItem(2, columnIndex + 2, item)
                    item = QTableWidgetItem(data['existing_value'])
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tb_result.setItem(rowIndex, columnIndex + 2, item)
                    item = QTableWidgetItem('申请需求')
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tb_result.setItem(2, columnIndex + 3, item)
                    item = QTableWidgetItem(data['apply_demand'])
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tb_result.setItem(rowIndex, columnIndex + 3,  item)
                    item = QTableWidgetItem('备注')
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tb_result.setItem(2, columnIndex + 4,  item)
                    item = QTableWidgetItem(data['note'])
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tb_result.setItem(rowIndex, columnIndex + 4, item)
                else:
                    item = QTableWidgetItem(getUnitNameByID(self.unitList[j]))
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tb_result.setItem(1, columnIndex, item)
                    self.tb_result.setSpan(1, columnIndex, 1, 5)
                    item = QTableWidgetItem('编制数')
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tb_result.setItem(2, columnIndex, item)

                    item = QTableWidgetItem('拟退役数')
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tb_result.setItem(2, columnIndex + 1, item)

                    item = QTableWidgetItem('现有数')
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tb_result.setItem(2, columnIndex + 2, item)

                    item = QTableWidgetItem('申请需求')
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tb_result.setItem(2, columnIndex + 3, item)

                    item = QTableWidgetItem('备注')
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.tb_result.setItem(2, columnIndex + 4, item)




























if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Apply_Retirement_Select()
    widget.show()
    sys.exit(app.exec_())