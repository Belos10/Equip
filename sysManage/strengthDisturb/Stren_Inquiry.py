from widgets.strengthDisturb.stren_inquiry import Widget_Stren_Inquiry
from PyQt5.QtWidgets import QWidget, QTreeWidgetItemIterator, QTreeWidgetItem, QMessageBox
from PyQt5 import QtWidgets
from sysManage.strengthDisturb.InquiryResult import Inquiry_Result
from sysManage.strengthDisturb.addStrenthInfo import AddStrenthInfo
from database.ConnectAndSql import Clicked, insert_Clicked, select_Equip_And_Unit, EquipNotHaveChild\
    , UnitNotHaveChild, insert_Strength, select_Equip_And_Unit_ByUnit, select_Equip_And_Unit_ByEquip

'''
    类功能：
        管理查询结果界面，包含查询结果相关逻辑代码
'''

first_treeWidget_dict = {}
second_treeWidget_dict = {}


class Stren_Inquiry(QWidget, Widget_Stren_Inquiry):
    # signalInquiry = pyqtSignal(str, str, name="signalInquiry")
    def __init__(self, parent=None):
        super(Stren_Inquiry, self).__init__(parent)
        self.setupUi(self)

        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}

        self.inquiry_result = Inquiry_Result()      #右边显示查询结果
        self.add_strenth_info = AddStrenthInfo()    #录入数据

        # 将查询结果界面和录入数据界面嵌入stackWidget
        self.sw_strenSelectMan.addWidget(self.inquiry_result)
        self.sw_strenSelectMan.addWidget(self.add_strenth_info)

        #设置当前显示查询结果界面
        self.sw_strenSelectMan.setCurrentIndex(0)

        # 初始化单位和装备目录
        self._initAllDict()

        #信号连接
        self.signalConnectSlot()

    def _initAllDict(self):
        # 初始化单位和装备目录
        self.tw_first.clear()
        self.tw_second.clear()
        self.tw_first.header().setVisible(False)
        self.tw_second.header().setVisible(False)
        self._initUnitTreeWidget("", self.tw_first)
        self._initEquipTreeWidget("", self.tw_second)

    # 信号与槽的连接
    def signalConnectSlot(self):
        # 按查询按钮时第一个目录的查询
        self.pb_firstSelect.clicked.connect(self.slotFilterFirstTreeWidget)
        # 按查询按钮时第二个目录的查询
        self.pb_secondSelect.clicked.connect(self.slotFilterSecondTreeWidget)

        # 按搜索框更改第一个目录的查询
        self.le_first.textChanged.connect(self.slotFilterFirstTreeWidget)
        # 按搜索框更改第二个目录的查询
        self.le_second.textChanged.connect(self.slotFilterSecondTreeWidget)

        #第一个目录更改后重新查询并显示结果
        self.tw_first.currentItemChanged.connect(self.slotReInqury)

        # 第二个目录选定后进行查询并显示结果
        self.tw_second.currentItemChanged.connect(self.slotInqury)

        # 从录入数据界面点击返回按钮返回查询界面
        self.add_strenth_info.pb_back.clicked.connect(self.slotBack)

        #从查询结果界面处双击进入录入界面
        self.inquiry_result.tw_inquiryResult.itemDoubleClicked.connect(self.slotDoubleClickedTableItem)

        #录入界面保存
        self.add_strenth_info.pb_Save.clicked.connect(self.slotSaveAddInfo)

        #录入界面删除
        self.add_strenth_info.pb_Delete.clicked.connect(self.add_strenth_info.deleteNote)

        #查询结果删除
        self.inquiry_result.pb_clearCheck.clicked.connect(self.inquiry_result.deleteInquiryResult)
        self.inquiry_result.pb_clearAll.clicked.connect(self.inquiry_result.deleteAllInquiryResult)

        #点击按单位展开按钮
        self.inquiry_result.rb_unitShow.clicked.connect(self.slotShowByUnit)

        #点击按装备展开按钮
        self.inquiry_result.rb_equipShow.clicked.connect(self.slotShowByEquip)

    # 信号与槽连接的断开
    def signalDisconnectSlot(self):
        # 按查询按钮时第一个目录的查询
        self.pb_firstSelect.clicked.disconnect(self.slotFilterFirstTreeWidget)
        # 按查询按钮时第二个目录的查询
        self.pb_secondSelect.clicked.disconnect(self.slotFilterSecondTreeWidget)

        # 按搜索框更改第一个目录的查询
        self.le_first.textChanged.disconnect(self.slotFilterFirstTreeWidget)
        # 按搜索框更改第二个目录的查询
        self.le_second.textChanged.disconnect(self.slotFilterSecondTreeWidget)

        # 第一个目录更改后重新查询并显示结果
        self.tw_first.currentItemChanged.disconnect(self.slotReInqury)

        # 第二个目录选定后进行查询并显示结果
        self.tw_second.currentItemChanged.disconnect(self.slotInqury)

        # 从录入数据界面点击返回按钮返回查询界面
        self.add_strenth_info.pb_back.clicked.disconnect(self.slotBack)

        # 从查询结果界面处双击进入录入界面
        self.inquiry_result.tw_inquiryResult.itemDoubleClicked.disconnect(self.slotDoubleClickedTableItem)

        # 录入界面保存
        self.add_strenth_info.pb_Save.clicked.disconnect(self.slotSaveAddInfo)

        # 录入界面删除
        self.add_strenth_info.pb_Delete.clicked.disconnect(self.add_strenth_info.deleteNote)

        # 查询结果删除
        self.inquiry_result.pb_clearCheck.clicked.disconnect(self.inquiry_result.deleteInquiryResult)
        self.inquiry_result.pb_clearAll.clicked.disconnect(self.inquiry_result.deleteAllInquiryResult)

        # 点击按单位展开按钮
        self.inquiry_result.rb_unitShow.clicked.disconnect(self.slotShowByUnit)

    def slotBack(self, event):
        reply = QtWidgets.QMessageBox.question(self, '提示', '是否退出信息录入?',
                                               QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.sw_strenSelectMan.setCurrentIndex(0)
            self.tw_first.setEnabled(1)
            self.tw_second.setEnabled(1)

    def slotSaveAddInfo(self):
        addNum = 0
        OrignNum = self.add_strenth_info.OrignNum
        #print(self.add_strenth_info.OrignNum, self.add_strenth_info.tableWidget.rowCount())
        self.tw_first.setEnabled(1)
        self.tw_second.setEnabled(1)
        if self.add_strenth_info.OrignNum == self.add_strenth_info.tableWidget.rowCount():
            self.sw_strenSelectMan.setCurrentIndex(0)
            return
        Unit_ID = self.add_strenth_info.UnitID
        Equip_ID = self.add_strenth_info.EquipID
        for i in range(self.add_strenth_info.row_num - OrignNum):
            ID = self.add_strenth_info.tableWidget.item(i + OrignNum, 0).text()
            num = self.add_strenth_info.tableWidget.item(i + OrignNum, 1).text()
            year = self.add_strenth_info.tableWidget.item(i + OrignNum, 2).text()
            shop = self.add_strenth_info.tableWidget.item(i + OrignNum, 3).text()
            state = self.add_strenth_info.tableWidget.item(i + OrignNum, 4).text()
            arrive = self.add_strenth_info.tableWidget.item(i + OrignNum, 5).text()
            confirm = self.add_strenth_info.tableWidget.item(i + OrignNum, 6).text()
            other = self.add_strenth_info.tableWidget.item(i + OrignNum, 7).text()
            #print(ID, num, year, shop, state, arrive, confirm, other)
            addNum += int(num)
            insert_Clicked(Unit_ID, Equip_ID, ID, num, year, shop, state, arrive, confirm, other)
        insert_Strength(Unit_ID, Equip_ID, addNum)
        self.sw_strenSelectMan.setCurrentIndex(0)

    def slotShowByEquip(self):
        unitRow = self.tw_first.currentIndex().row()
        euqipRow = self.tw_second.currentIndex().row()
        currentUnitID = ""
        currentEquipID = ""
        if unitRow == -1 or euqipRow == -1:
            reply = QMessageBox.question(self, '查询', '请同时选中单位和装备', QMessageBox.Yes)
        else:
            #按装备展开
            if self.inquiry_result.rb_equipShow.isChecked():
                for unitID, unitItem in self.first_treeWidget_dict.items():
                    if self.tw_first.currentItem() == unitItem:
                        currentUnitID = unitID
                for equipID, equipItem in self.second_treeWidget_dict.items():
                    if self.tw_second.currentItem() == equipItem:
                        currentEquipID = equipID
                result = select_Equip_And_Unit_ByEquip(currentUnitID, currentEquipID)
                self.inquiry_result._initTableWidget(result)
    '''
        功能：
            点击按单位展开按钮
    '''
    def slotShowByUnit(self):
        unitRow = self.tw_first.currentIndex().row()
        euqipRow = self.tw_second.currentIndex().row()
        currentUnitID = ""
        currentEquipID = ""
        if unitRow == -1 or euqipRow == -1:
            reply = QMessageBox.question(self, '查询', '请同时选中单位和装备', QMessageBox.Yes)
        else:
            # 按装备展开
            if self.inquiry_result.rb_unitShow.isChecked():
                for unitID, unitItem in self.first_treeWidget_dict.items():
                    if self.tw_first.currentItem() == unitItem:
                        currentUnitID = unitID
                for equipID, equipItem in self.second_treeWidget_dict.items():
                    if self.tw_second.currentItem() == equipItem:
                        currentEquipID = equipID
                result = select_Equip_And_Unit_ByUnit(currentUnitID, currentEquipID)
                self.inquiry_result._initTableWidget(result)
    '''
        功能：
            双击某行数据后进入录入界面
    '''
    def slotDoubleClickedTableItem(self):
        currentRow = self.inquiry_result.tw_inquiryResult.currentRow()

        for row, data in self.inquiry_result.currentInquiryResult.items():
            if row == currentRow:
                #print(data)
                equipNotHaveChild = EquipNotHaveChild(data[0])
                unitNotHaveChild = UnitNotHaveChild(data[1])
                if equipNotHaveChild and unitNotHaveChild:
                    self.add_strenth_info._initWeight(data)
                    self.tw_first.setEnabled(False)
                    self.tw_second.setEnabled(False)
                    self.sw_strenSelectMan.setCurrentIndex(1)
                else:
                    reply = QMessageBox.question(self, '录入', '只能通过最基本的信息进行录入', QMessageBox.Yes)
                break

    '''
        初始化单位目录
    '''

    def _initUnitTreeWidget(self, root, mother):
        if root == '':
            sql = 'select Dept_Name,Dept_ID from dept where Dept_Uper = ""'
        else:
            sql = " select Dept_Name,Dept_ID from dept where Dept_Uper='" + root + "'"

        result = Clicked(sql)
        for data in result:
            item = QTreeWidgetItem(mother)
            item.setText(0, data[0])
            self.first_treeWidget_dict[data[1]] = item
            if data[0] != '':
                self._initUnitTreeWidget(data[1], item)

    '''
        功能：
            初始化装备目录
    '''
    def _initEquipTreeWidget(self, root, mother):
        if root == '':
            sql = 'select Equip_Name,Equip_ID from equip where Equip_Uper = ""'
        else:
            sql = "select Equip_Name,Equip_ID from equip where Equip_Uper='" + root + "'"

        result = Clicked(sql)
        for data in result:
            item = QTreeWidgetItem(mother)
            item.setText(0, data[0])
            self.second_treeWidget_dict[data[1]] = item
            if data[0] != '':
                self._initEquipTreeWidget(data[1], item)

    '''
        功能：
            让第一个目录进行过滤筛选出想选择的项目
    '''
    def slotFilterFirstTreeWidget(self):
        """以text开头作为过滤条件示例"""
        find = False
        text = self.le_first.text()

        cursor = QTreeWidgetItemIterator(self.tw_first)
        while cursor.value():
            item = cursor.value()
            if item.text(0).startswith(text):
                self.tw_first.setCurrentItem(item)
                find = True
                # 需要让父节点也显示,不然子节点显示不出来
                try:
                    self.tw_first.setCurrentItem(item)
                    find = True
                except Exception:
                    pass
            else:
                pass

            cursor = cursor.__iadd__(1)

    '''
        功能：
            让第二个目录进行过滤筛选出想选择的项目
    '''

    def slotFilterSecondTreeWidget(self):
        """以text开头作为过滤条件示例"""
        text = self.le_second.text()
        find = False
        cursor = QTreeWidgetItemIterator(self.tw_second)
        while cursor.value():
            item = cursor.value()
            if item.text(0).startswith(text):
                self.tw_second.setCurrentItem(item)
                # 需要让父节点也显示,不然子节点显示不出来
                try:
                    self.tw_second.setCurrentItem(item)
                except Exception:
                    pass
            else:
                pass

            cursor = cursor.__iadd__(1)

    '''
        功能：
            第一个TreeWidget选中后查询想要查询的结果并显示
    '''
    def slotReInqury(self):
        unitRow = self.tw_first.currentIndex().row()
        euqipRow = self.tw_second.currentIndex().row()
        currentUnitID = ""
        currentEquipID = ""
        if unitRow == -1 or euqipRow == -1:
            reply = QMessageBox.question(self, '查询', '请同时选中单位和装备', QMessageBox.Yes)
        else:
            #按装备展开
            if self.inquiry_result.rb_equipShow.isChecked():
                for unitID, unitItem in self.first_treeWidget_dict.items():
                    if self.tw_first.currentItem() == unitItem:
                        currentUnitID = unitID
                for equipID, equipItem in self.second_treeWidget_dict.items():
                    if self.tw_second.currentItem() == equipItem:
                        currentEquipID = equipID
                result = select_Equip_And_Unit_ByEquip(currentUnitID, currentEquipID)
                self.inquiry_result._initTableWidget(result)
            #按照单位展开
            elif self.inquiry_result.rb_unitShow.isChecked():
                for unitID, unitItem in self.first_treeWidget_dict.items():
                    if self.tw_first.currentItem() == unitItem:
                        currentUnitID = unitID
                for equipID, equipItem in self.second_treeWidget_dict.items():
                    if self.tw_second.currentItem() == equipItem:
                        currentEquipID = equipID
                result = select_Equip_And_Unit_ByUnit(currentUnitID, currentEquipID)
                self.inquiry_result._initTableWidget(result)
            else:
                for unitID, unitItem in self.first_treeWidget_dict.items():
                    if self.tw_first.currentItem() == unitItem:
                        currentUnitID = unitID
                for equipID, equipItem in self.second_treeWidget_dict.items():
                    if self.tw_second.currentItem() == equipItem:
                        currentEquipID = equipID

                result = select_Equip_And_Unit(currentUnitID, currentEquipID)
                self.inquiry_result._initTableWidget(result)

    '''
        功能：
            第二个TreeWidget选中后查询想要查询的结果并显示
    '''

    def slotInqury(self):
        unitRow = self.tw_first.currentIndex().row()
        euqipRow = self.tw_second.currentIndex().row()
        currentUnitID = ""
        currentEquipID = ""
        if unitRow == -1 or euqipRow == -1:
            reply = QMessageBox.question(self, '查询', '请同时选中单位和装备', QMessageBox.Yes)
        else:
            if self.inquiry_result.rb_equipShow.isChecked():
                for unitID, unitItem in self.first_treeWidget_dict.items():
                    if self.tw_first.currentItem() == unitItem:
                        currentUnitID = unitID
                for equipID, equipItem in self.second_treeWidget_dict.items():
                    if self.tw_second.currentItem() == equipItem:
                        currentEquipID = equipID
                result = select_Equip_And_Unit_ByEquip(currentUnitID, currentEquipID)
                self.inquiry_result._initTableWidget(result)
            elif self.inquiry_result.rb_unitShow.isChecked():
                for unitID, unitItem in self.first_treeWidget_dict.items():
                    if self.tw_first.currentItem() == unitItem:
                        currentUnitID = unitID
                for equipID, equipItem in self.second_treeWidget_dict.items():
                    if self.tw_second.currentItem() == equipItem:
                        currentEquipID = equipID
                result = select_Equip_And_Unit_ByUnit(currentUnitID, currentEquipID)
                self.inquiry_result._initTableWidget(result)
            else:
                for unitID, unitItem in self.first_treeWidget_dict.items():
                    if self.tw_first.currentItem() == unitItem:
                        currentUnitID = unitID
                for equipID, equipItem in self.second_treeWidget_dict.items():
                    if self.tw_second.currentItem() == equipItem:
                        currentEquipID = equipID

                result = select_Equip_And_Unit(currentUnitID, currentEquipID)
                self.inquiry_result._initTableWidget(result)
