from PyQt5.QtCore import Qt
from database.positionEngneerSql import *
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidget, QHeaderView, QTableWidgetItem, QComboBox, \
    QMessageBox, QTreeWidgetItem

from widgets.positionEngineer.posEngneerStatisticsUI import PosEngneerStatisticsUI


class EquipmentStatistics(QWidget, PosEngneerStatisticsUI):
    def __init__(self, parent=None):
        super(EquipmentStatistics, self).__init__(parent)
        self.setupUi(self)
        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}
        # 当前选中的单位列表和装备列表
        self.currentCheckedUnitList = []
        self.currentCheckedEquipList = []
        self.countOfPosition= 0
        self.signalConnectSlot()
        self._initEquipmentStatistics()


    # 信号与槽的连接
    def signalConnectSlot(self):
        # 当前单位目录被点击
        self.tw_first.itemChanged.connect(self.slotEquipmentStatisticsResult)
        # 当前装备目录被点击
        self.tw_second.itemChanged.connect(self.slotEquipmentStatisticsResult)

        # 新增某个年份
        self.tb_add.clicked.connect(self.slotAdd)

        self.tb_delete.clicked.connect(self.slotDelete)

        self.pb_firstSelect.clicked.connect(self.slotSelectUnit)

        self.pb_secondSelect.clicked.connect(self.slotSelectEquip)
        self.tb_output.clicked.connect(self.slotInput)
        self.tb_output.clicked.connect(self.slotOutput)


    #信号和槽断开
    def slotDisconnect(self):
        pass

    #定义初始化函数
    def _initEquipmentStatistics(self):
        self.tw_first.clear()
        self.tw_second.clear()
        self.tw_first.header().setVisible(False)
        self.tw_second.header().setVisible(False)
        self.le_first.setDisabled(False)
        self.le_second.setDisabled(False)
        self.tw_first.setDisabled(False)
        self.tw_first.setVisible(True)
        self.pb_firstSelect.setVisible(False)
        self.pb_firstSelect.setDisabled(False)
        self.le_first.setVisible(False)
        self.le_second.setVisible(False)
        self.tw_second.setDisabled(False)
        self.tw_second.setVisible(True)
        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}
        # 当前选中的单位列表和装备列表
        self.currentCheckedUnitList = []
        self.currentCheckedEquipList = []
        self._initUnitTreeWidget('', self.tw_first)
        self._initEquipTreeWidget('', self.tw_second)
        pass




    def initUserInfo(self, userInfo):
        self.userInfo = userInfo
        self._initEquipmentStatistics()


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
        self.inquiry_result.setDisabled(False)
        #        self.tb_inqury.setDisabled(True)
        #        self.tb_rechoose.setDisabled(False)

        self.currentYear = self.lw_chooseYear.currentItem().text()
        print("currentYear :", self.currentYear)

        self.startName = selectUnitNameByUnitID(self.userInfo[0][4])
        item = QTreeWidgetItem(self.tw_first)
        item.setText(0, self.startName)
        item.setCheckState(0, Qt.Unchecked)
        self.first_treeWidget_dict[self.userInfo[0][4]] = item
        self._initUnitTreeWidget(self.userInfo[0][4], item)
        self._initEquipTreeWidget("", self.tw_second)


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
            查询实力结果
    '''
    def slotEquipmentStatisticsResult(self):
        self.currentCheckedUnitList = []
        self.currentCheckedEquipList = []
        for equipID, equipItem in self.second_treeWidget_dict.items():
            if equipItem.checkState(0) == Qt.Checked:
                self.currentCheckedEquipList.append(equipID)

        for unitID, unitItem in self.first_treeWidget_dict.items():
            if unitItem == self.tw_first.currentItem():
                self.currentCheckedUnitList.append(unitID)

        self._initTableWidgetByUnitListAndEquipList(self.currentCheckedUnitList,self.currentCheckedEquipList)

    '''
        功能：
            根据单位目录和装备目录初始化结果表格
    '''
    def _initTableWidgetByUnitListAndEquipList(self,unitList,equipList):

        pass






    '''
        初始化单位目录
    '''
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
            if rowData[0] != '':
                self._initUnitTreeWidget(rowData[0], item)

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
            画表头
    '''
    def initHeader(self):
        self.tw_result.verticalHeader().setVisible(False)
        self.tw_result.horizontalHeader().setVisible(False)
        # self.tw_result.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tw_result.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tw_result.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tw_result.resizeColumnsToContents()
        self.tw_result.resizeRowsToContents()

        if self.tw_result.columnCount() == 4:
            item = QTableWidgetItem("阵地工程XXX防护装备安装情况")
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tw_result.setItem(0, 0, item)
            self.tw_result.setSpan(0, 0, 1, 13)
            pass
        else:
            pass
        # 绘制表头
        item = QTableWidgetItem("阵地工程XXX防护装备安装情况")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(0, 0, item)
        self.tw_result.setSpan(0, 0, 1, 13)

    def slotAdd(self):
        pass
    def slotDelete(self):
        pass

    def slotInput(self):
        pass
    def slotOutput(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = EquipmentStatistics()
    widget.show()
    sys.exit(app.exec_())