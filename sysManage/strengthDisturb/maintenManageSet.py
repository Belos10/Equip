import sys

from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QTableWidgetItem, QAbstractItemView, QHeaderView

from database.strengthDisturbSql import *
from sysManage.component import getMessageBox
from sysManage.userInfo import get_value
from widgets.strengthDisturb.maintenManageSet import Widget_Mainten_Manage_Set

sys.setrecursionlimit(100000)
'''
   编制数维护目录设置
'''
class maintenManageSet(QWidget, Widget_Mainten_Manage_Set):
    def __init__(self, parent=None):
        super(maintenManageSet, self).__init__(parent)
        self.setupUi(self)

        # 设置整行选中
        self.tw_unit.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 设置整行选中
        self.tw_publicEquip.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tw_publicEquip.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tw_unit.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.signalConnect()
        self.result = []
        self.startInfo = None
        self.currentUnitTableResult = []
        self.orignUnitResult = {}

        self.tw_publicEquip.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tw_unit.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def _initAll_(self):
        self.orignUnitResult = {}
        self.getUserInfo()
        self.currentUnitTableResult = []

        self.currentRow = None
        self.first_treeWidget_dict = {}
        self.tw_first.clear()
        self.tw_first.header().setVisible(False)
        self.currentPublicInfo = []

        # 初始化单元表
        self.startInfo = selectUnitInfoByUnitID(self.userInfo[0][4])
        stack = []
        root = []
        if self.startInfo:
            stack.append(self.startInfo)
            root.append(self.tw_first)
            self.initUnitTreeWidget(stack, root)
            # 从数据库中单位表中获取数据初始化单位目录，tableWidget显示所有的单位表
            self._initUnitTableWidget()
            self._initPublicEquipTableWidget_()

    '''
               功能：
                   单位目录的初始化，显示整个单位表
                   参数表：root为上级单位名字，mother为上级节点对象
       '''

    def initUnitTreeWidget(self, stack, root):
        while stack:
            UnitInfo = stack.pop(0)
            self.currentUnitTableResult.append(UnitInfo)
            item = QTreeWidgetItem(root.pop(0))
            item.setText(0, UnitInfo[1])
            self.first_treeWidget_dict[UnitInfo[0]] = item
            result = selectUnitInfoByDeptUper(UnitInfo[0])
            for resultInfo in result:
                stack.append(resultInfo)
                root.append(item)
            if UnitInfo:
                if UnitInfo[4] == "是":
                    publicItem = QTreeWidgetItem(item)
                    publicEuip = selectPubilcEquipInfoByGroupID(UnitInfo[0])
                    if publicEuip:
                        publicItem.setText(0, "公用装备")
                        self.first_treeWidget_dict[publicEuip[0]] = publicItem
                        self.currentPublicInfo.append(publicEuip)

    def signalConnect(self):
        #当前单位结果界面某行被选中
        self.tw_unit.clicked.connect(self.slotUnitTableClicked)

        #更新当前单位是否为旅团
        self.pb_update.clicked.connect(self.slotUpdateIsGroup)
        self.pb_firstSelect.clicked.connect(self.slotSelectUnit)

    def getUserInfo(self):
        self.userInfo = get_value("totleUserInfo")


    def slotSelectUnit(self):
        findText = self.le_first.text()
        for i, item in self.first_treeWidget_dict.items():
            if item.text(0) == findText:
                self.tw_first.setCurrentItem(item)
                break

    '''
       当前单位被选中
    '''
    def slotUnitTableClicked(self):
        self.currentRow = self.tw_unit.currentRow()
        unitID = self.tw_unit.item(self.tw_unit.currentRow(), 0).text()
        isGroup = self.tw_unit.item(self.tw_unit.currentRow(), 2).text()
        self.lb_unitID.setText(unitID)
        if isGroup == '是':
            self.cb_isGroup.setCurrentIndex(0)
        else:
            self.cb_isGroup.setCurrentIndex(1)

    def getTableUnitInfo(self, root):
        if root[0] == '':
            result = selectUnitInfoByDeptUper('')
        else:
            result = selectUnitInfoByDeptUper(root[0])

            # rowData: (单位编号，单位名称，上级单位编号)
        for rowData in result:
            self.unitDictInfo.append(rowData)
            if rowData[0] != '':
                self.getTableUnitInfo(rowData[0])
            else:
                return None
    '''
        初始化界面
    '''
    def _initUnitTableWidget(self):
        self.tw_unit.clear()
        header = ['单位编号', '单位名字', '是否为旅团']
        self.tw_unit.setColumnCount(len(header))
        self.tw_unit.setHorizontalHeaderLabels(header)

        self.tw_unit.setRowCount(len(self.currentUnitTableResult))

        for i, unitInfo in enumerate(self.currentUnitTableResult):
            item = QTableWidgetItem()
            item.setText(unitInfo[0])
            self.tw_unit.setItem(i, 0, item)
            item = QTableWidgetItem()
            item.setText(unitInfo[1])
            self.tw_unit.setItem(i, 1, item)
            item = QTableWidgetItem()
            item.setText(unitInfo[4])
            self.tw_unit.setItem(i, 2, item)
            self.orignUnitResult[i] = unitInfo

    '''
        初始化公共装备tablewidget
    '''
    def _initPublicEquipTableWidget_(self):
        self.tw_publicEquip.clear()
        header = ['装备编号', '旅团编号']
        self.tw_publicEquip.setColumnCount(len(header))
        self.tw_publicEquip.setHorizontalHeaderLabels(header)

        self.tw_publicEquip.setRowCount(len(self.currentPublicInfo))
        #print("================== currentPublicInfo ======================", self.currentPublicInfo)
        for i, publicEquipInfo in enumerate(self.currentPublicInfo):
            item = QTableWidgetItem()
            item.setText(publicEquipInfo[0])
            self.tw_publicEquip.setItem(i, 0, item)
            item = QTableWidgetItem()
            item.setText(publicEquipInfo[1])
            self.tw_publicEquip.setItem(i, 1, item)



    '''
        更新当前是否为旅团
    '''
    def slotUpdateIsGroup(self):
        if self.tw_unit.currentRow() < 0:
            return
        if self.tw_unit.item(self.currentRow, 2).text() != self.cb_isGroup.currentText():
            updateSuccess = updateUnitIsGroupFromUnit(self.lb_unitID.text(), self.cb_isGroup.currentText())
            if updateSuccess != True:
                getMessageBox("更新", str(updateSuccess) + '，更新失败', True, False)
                return
            self.first_treeWidget_dict = {}
            self.tw_first.clear()
            self._initAll_()