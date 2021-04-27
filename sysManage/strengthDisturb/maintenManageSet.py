from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QTableWidgetItem, QAbstractItemView, QMessageBox
from widgets.strengthDisturb.maintenManageSet import Widget_Mainten_Manage_Set
from database.strengthDisturbSql import selectAllStrengthYearInfo, selectAllDataAboutUnit, \
    updateUnitIsGroupFromUnit, selectAllFromPulicEquip, selectUnitInfoByDeptUper
from PyQt5.Qt import Qt


class maintenManageSet(QWidget, Widget_Mainten_Manage_Set):
    def __init__(self, parent=None):
        super(maintenManageSet, self).__init__(parent)
        self.setupUi(self)

        # 设置整行选中
        self.tw_unit.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 设置整行选中
        self.tw_publicEquip.setSelectionBehavior(QAbstractItemView.SelectRows)

        #初始化单元表
        self._initUnitTableWidget()

        #初始化公用装备表
        self._initPublicEquipTableWidget_()

        self.orignUnitResult = {}

        self.currentRow = None
        self.first_treeWidget_dict = {}
        self.tw_first.clear()
        self.tw_first.header().setVisible(False)
        self._initUnitTreeWidget("", self.tw_first)
        self.signalConnect()


    def signalConnect(self):
        self.tw_unit.clicked.connect(self.slotUnitTableClicked)

        self.pb_update.clicked.connect(self.slotUpdateIsGroup)

    def slotUnitTableClicked(self):
        self.currentRow = self.tw_unit.currentRow()
        unitID = self.tw_unit.item(self.tw_unit.currentRow(), 0).text()
        isGroup = self.tw_unit.item(self.tw_unit.currentRow(), 2).text()
        self.lb_unitID.setText(unitID)
        if isGroup == '是':
            self.cb_isGroup.setCurrentIndex(0)
        else:
            self.cb_isGroup.setCurrentIndex(1)

    def _initUnitTableWidget(self):
        self.orignUnitResult = {}
        self.tw_unit.clear()
        result = selectAllDataAboutUnit()
        header = ['单位编号', '单位名字', '是否为旅团']
        self.tw_unit.setColumnCount(len(header))
        self.tw_unit.setHorizontalHeaderLabels(header)

        self.tw_unit.setRowCount(len(result))

        for i, unitInfo in enumerate(result):
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

    def _initPublicEquipTableWidget_(self):
        self.tw_publicEquip.clear()
        header = ['装备编号', '旅团编号', '编制数']
        self.tw_publicEquip.setColumnCount(len(header))
        self.tw_publicEquip.setHorizontalHeaderLabels(header)

        result = selectAllFromPulicEquip()
        self.tw_publicEquip.setRowCount(len(result))
        for i, publicEquipInfo in enumerate(result):
            item = QTableWidgetItem()
            item.setText(publicEquipInfo[0])
            self.tw_publicEquip.setItem(i, 0, item)
            item = QTableWidgetItem()
            item.setText(publicEquipInfo[1])
            self.tw_publicEquip.setItem(i, 1, item)
            item = QTableWidgetItem()
            item.setText(publicEquipInfo[2])
            self.tw_publicEquip.setItem(i, 2, item)

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
            if rowData[4] == '是':
                publicItem = QTreeWidgetItem(item)
                publicItem.setText(0, "公用装备")
            if rowData[0] != '':
                self._initUnitTreeWidget(rowData[0], item)

    def slotUpdateIsGroup(self):
        if self.tw_unit.item(self.currentRow, 2).text() != self.cb_isGroup.currentText():
            updateUnitIsGroupFromUnit(self.lb_unitID.text(), self.cb_isGroup.currentText())
            self._initPublicEquipTableWidget_()
            self._initUnitTableWidget()
            self.first_treeWidget_dict = {}
            self.tw_first.clear()
            self._initUnitTreeWidget("", self.tw_first)