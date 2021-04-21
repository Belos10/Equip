from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QTableWidgetItem, QAbstractItemView, QMessageBox
from database.ConnectAndSql import Clicked, add_UnitDictDept, update_Unit_Dict, selectUnitDictByUper, del_Unit_Dict, \
    del_Unit_And_Child, add_UnitDictEquip, update_Equip_Dict, del_Equip_And_Child, del_Equip_Dict
from widgets.strengthDisturb.select_set import Widget_Select_Set


class strengthSelectSet(QWidget, Widget_Select_Set):
    def __init__(self, parent=None):
        super(strengthSelectSet, self).__init__(parent)
        self.setupUi(self)

        self.tw_first.clear()
        self.tw_second.clear()
        self.tw_first.header().setVisible(False)  # 不显示树窗口的title
        self.tw_second.header().setVisible(False)  # 不显示树窗口的title
        self.changeFirst = True  # 是否是修改单元的目录

        # QTableWidget设置整行选中
        self.tb_result.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tb_result.setSelectionMode(QAbstractItemView.SingleSelection)

        self.first_treeWidget_dict = {}  # 当前单位目录列表对象，结构为：{'行号':对应的item}
        self.second_treeWidget_dict = {}  # 当前装备目录列表对象，结构为：{'行号':对应的item}
        self.signalConnect()

    def signalConnect(self):
        self.pb_add.clicked.connect(self.slotAddDict)  # 添加数据
        self.tb_result.itemClicked.connect(self.slotClickedRow)  # 点击当前tablewidget
        self.pb_update.clicked.connect(self.slotUpdate)  # 修改数据
        self.pushButton.clicked.connect(self.slotFirstInit)  # 设置单元目录
        self.pb_del.clicked.connect(self.slotDelDict)  # 删除数据
        self.pushButton_2.clicked.connect(self.slotSecondInit)  # 设置装备目录
        self.tw_first.currentItemChanged.connect(self.slotSelectIndex)  # 将单位目录与装备目录相关联

    def slotDisconnect(self):
        self.pb_add.clicked.disconnect(self.slotAddDict)  # 添加数据
        self.tb_result.itemClicked.disconnect(self.slotClickedRow)  # 点击当前tablewidget
        self.pb_update.clicked.disconnect(self.slotUpdate)  # 修改数据
        self.pushButton.clicked.disconnect(self.slotFirstInit)  # 设置单元目录
        self.pb_del.clicked.disconnect(self.slotDelDict)  # 删除数据
        self.pushButton_2.clicked.disconnect(self.slotSecondInit)  # 设置装备目录
        self.tw_first.currentItemChanged.disconnect(self.slotSelectIndex)  # 将单位目录与装备目录相关联

    '''
        功能：
            更改当前状态为设置单元目录，并初始化单元目录以及tablewidget
    '''

    def slotFirstInit(self):
        self.tw_first.clear()
        self.tw_second.clear()
        self._initTreeWidget("", self.tw_first)
        self._initUnitTableWidget()
        self.pushButton.setDisabled(True)
        self.pushButton_2.setDisabled(False)
        self.changeFirst = True
        self.le_equipID.clear()
        self.le_equipName.clear()
        self.le_equipUper.clear()
        self.le_unitID.clear()
        self.le_equipID.setEnabled(0)
        self.le_equipName.setEnabled(0)
        self.le_equipUper.setEnabled(0)
        self.le_unitUper.setEnabled(1)
        self.le_unitName.setEnabled(1)

    '''
            功能：
                更改当前状态为设置装备目录，并初始化装备目录以及tablewidget
    '''

    def slotSecondInit(self):
        self.pushButton.setDisabled(False)
        self.pushButton_2.setDisabled(True)
        self.tw_first.clear()
        self.tw_second.clear()
        self._initSecondTreeWidget("", self.tw_second)
        self._initEquipTableWidget()
        self.changeFirst = False
        #self.tb_result.clear()
        #self.tb_result.setRowCount(0)
        self.le_equipID.setEnabled(1)
        self.le_equipName.setEnabled(1)
        self.le_equipUper.setEnabled(1)
        self.le_unitUper.clear()
        self.le_unitName.clear()
        self.le_unitID.clear()
        self.le_unitUper.setEnabled(0)
        self.le_unitName.setEnabled(0)

    '''
        功能：
            当设置单位目录时，初始化tableWidget
    '''

    def _initUnitTableWidget(self):
        sql = " select * from dept"
        result = Clicked(sql)

        header = ['单位编号', '单位名称', '上级单位编号']
        self.tb_result.setColumnCount(3)
        self.tb_result.setRowCount(len(result))
        self.tb_result.setHorizontalHeaderLabels(header)

        for i, data in enumerate(result):
            item = QTableWidgetItem(data[0])
            self.tb_result.setItem(i, 0, item)
            item = QTableWidgetItem(data[1])
            self.tb_result.setItem(i, 1, item)
            item = QTableWidgetItem(data[2])
            self.tb_result.setItem(i, 2, item)

        # print(result)   #测试查找到的数据

    '''
        功能：
            当设置装备目录时，初始化tableWidget
    '''

    def _initEquipTableWidget(self):
        # self.tb_result.clear()
        # self.tb_result.setRowCount(0)
        sql = " select * from equip "
        result = Clicked(sql)

        header = ['装备编号', '装备名称', '上级装备编号']
        self.tb_result.setColumnCount(3)
        self.tb_result.setRowCount(len(result))
        self.tb_result.setHorizontalHeaderLabels(header)

        for i, data in enumerate(result):
            item = QTableWidgetItem(data[0])
            self.tb_result.setItem(i, 0, item)
            item = QTableWidgetItem(data[1])
            self.tb_result.setItem(i, 1, item)
            item = QTableWidgetItem(data[2])
            self.tb_result.setItem(i, 2, item)

        # print(result)   #测试查找到的数据

    '''
        功能：
            当设置装备目录时，根据当前选中的单位查找对应的装备
    '''

    def slotSelectIndex(self):
        if self.changeFirst:
            pass
        else:
            # self.slotDisconnect()
            # 在clear前要现将该控件上的信号和槽的连接进行disconnect，不然会发生段错误
            self.tw_second.clear()

            for UnitID, item in self.first_treeWidget_dict.items():
                if item == self.tw_first.currentItem():
                    print(item)
                    self._initSecondTreeWidget("", self.tw_second)
                    self._initEquipTableWidget()
                    # break
            # self.signalConnect()

    '''
        功能：
            当设置装备目录时，初始化装备目录
    '''

    def _initSecondTreeWidget(self, root, mother):

        # if UnitID:
        #     sql = "select Equip_Name,Equip_ID from equip where Unit_ID ='" + UnitID + "'" + "AND Equip_Uper = ''"
        #     # print(sql)
        # else:

        sql = "select Equip_Name,Equip_ID from equip where Equip_Uper ='" + root + "'"
            # print(sql)
        result = Clicked(sql)
        for data in result:
            item = QTreeWidgetItem(mother)
            item.setText(0, data[0])
            self.second_treeWidget_dict[data[1]] = item
            if data[0] != '':
                self._initSecondTreeWidget(data[1], item)

    '''
        功能：
            当设置单位目录时，初始化单位目录
    '''

    def _initTreeWidget(self, root, mother):

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
                self._initTreeWidget(data[1], item)

    '''
        功能：
            当选中tablewidget某行时，显示对应的lineedit
    '''

    def slotClickedRow(self):
        print(self.tb_result.currentRow())
        currentRow = self.tb_result.currentRow()
        if self.changeFirst:
            self.le_unitID.setText(self.tb_result.item(currentRow, 0).text())
            self.le_unitName.setText(self.tb_result.item(currentRow, 1).text())
            self.le_unitUper.setText(self.tb_result.item(currentRow, 2).text())
        else:
            self.le_equipID.setText((self.tb_result.item(currentRow,0).text()))
            #self.le_unitID.setText((self.tb_result.item(currentRow, 1).text()))
            self.le_equipName.setText((self.tb_result.item(currentRow, 1).text()))
            self.le_equipUper.setText((self.tb_result.item(currentRow, 2).text()))

    '''
        功能：
            添加目录
    '''

    def slotAddDict(self):
        # 单位目录
        if self.changeFirst:
            if self.le_unitID.text() == "" or self.le_unitName.text() == "":
                reply = QMessageBox.question(self, '新增失败', '单位ID或单位名字为空，拒绝增加，请重新填写', QMessageBox.Yes,
                                             QMessageBox.Cancel)
            else:
                Unit_ID = self.le_unitID.text()
                Unit_Name = self.le_unitName.text()
                Unit_Uper = self.le_unitUper.text()
                add_UnitDictDept(Unit_ID, Unit_Name, Unit_Uper)
                self.slotDisconnect()
                self.tb_result.clear()
                self.tw_first.clear()
                self.tw_second.clear()
                self.tb_result.setRowCount(0)
                self.first_treeWidget_dict.clear()
                self.second_treeWidget_dict.clear()
                self._initUnitTableWidget()
                self._initTreeWidget("", self.tw_first)
                self.signalConnect()
        # 装备目录
        else:
            if self.le_equipID.text() == "" or self.le_equipName.text() == "":
                reply = QMessageBox.question(self, '新增失败', '单位ID或单位名字为空，拒绝增加，请重新填写', QMessageBox.Yes,
                                             QMessageBox.Cancel)
            else:
                # Equip_ID,Unit_ID, Equip_Name, Equip_Uper
                Equip_ID = self.le_equipID.text()
                #Unit_ID = self.le_unitID.text()
                Equip_Name = self.le_equipName.text()
                Equip_Uper = self.le_equipUper.text()
                add_UnitDictEquip(Equip_ID,Equip_Name,Equip_Uper)
                self.slotDisconnect()
                self.tb_result.clear()
                self.tw_first.clear()
                self.tw_second.clear()
                self.tb_result.setRowCount(0)
                self.first_treeWidget_dict.clear()
                self.second_treeWidget_dict.clear()
                self._initEquipTableWidget()
                self._initSecondTreeWidget("", self.tw_second)
                self.signalConnect()

    '''
        功能：
            修改目录
    '''

    def slotUpdate(self):
        # 单位目录
        if self.changeFirst:
            if (self.tb_result.item(self.tb_result.currentRow(),
                                    0).text() != self.le_unitID.text()) or self.le_unitName.text() == "":
                reply = QMessageBox.question(self, '修改失败', '单位ID不能修改或单位名字为空，拒绝修改，请重新填写', QMessageBox.Yes,
                                             QMessageBox.Cancel)
            else:
                Unit_ID = self.le_unitID.text()
                Unit_Name = self.le_unitName.text()
                Unit_Uper = self.le_unitUper.text()
                update_Unit_Dict(Unit_ID, Unit_Name, Unit_Uper)
                self.slotDisconnect()
                self.tb_result.clear()
                self.tw_first.clear()
                self.tw_second.clear()
                self.tb_result.setRowCount(0)
                self.first_treeWidget_dict = {}
                self.second_treeWidget_dict = {}
                self.signalConnect()
                self._initUnitTableWidget()
                self._initTreeWidget("", self.tw_first)
        # 装备目录
        else:
            if (self.tb_result.item(self.tb_result.currentRow(),
                                    0).text() != self.le_equipID.text()) or self.le_equipName.text() == "":
                reply = QMessageBox.question(self, '修改失败', '单位ID不能修改或单位名字为空，拒绝修改，请重新填写', QMessageBox.Yes,
                                             QMessageBox.Cancel)
            else:
                Equip_ID = self.le_equipID.text()
                #Unit_ID = self.le_unitID.text()
                Equip_Name = self.le_equipName.text()
                Equip_Uper = self.le_equipUper.text()
                update_Equip_Dict(Equip_ID,Equip_Name,Equip_Uper)
                self.slotDisconnect()
                self.tb_result.clear()
                self.tw_first.clear()
                self.tw_second.clear()
                self.tb_result.setRowCount(0)
                self.first_treeWidget_dict = {}
                self.second_treeWidget_dict = {}
                self.signalConnect()
                self._initEquipTableWidget()
                self._initSecondTreeWidget("", self.tw_second)


    '''
        功能：
            删除目录
    '''

    def slotDelDict(self):
        # 单位目录
        if self.changeFirst:
            haveChild = selectUnitDictByUper(self.le_unitID.text())
            if haveChild:
                print("have")
                reply = QMessageBox.question(self, '删除', '该单位有下级单位，是否将下级单位一起删除？', QMessageBox.Yes,
                                             QMessageBox.Cancel)
                if reply == QMessageBox.Yes:
                    del_Unit_And_Child(self.le_unitID.text())
                    reply = QMessageBox.question(self, '删除', '删除成功', QMessageBox.Yes)
                    self.slotDisconnect()
                    self.tb_result.clear()
                    self.tw_first.clear()
                    self.tw_second.clear()
                    self.tb_result.setRowCount(0)
                    self.first_treeWidget_dict = {}
                    self.second_treeWidget_dict = {}
                    self.signalConnect()
                    self._initUnitTableWidget()
                    self._initTreeWidget("", self.tw_first)
                else:
                    reply = QMessageBox.question(self, '删除', '删除失败', QMessageBox.Yes)
            else:
                reply = QMessageBox.question(self, '删除', '确定删除吗？', QMessageBox.Yes,
                                             QMessageBox.Cancel)
                if reply == QMessageBox.Yes:
                    Unit_ID=self.le_unitID.text()
                    del_Unit_Dict(self.le_unitID.text())
                    reply = QMessageBox.question(self, '删除', '删除成功', QMessageBox.Yes)
                    self.slotDisconnect()
                    self.tb_result.clear()
                    self.tw_first.clear()
                    self.tw_second.clear()
                    self.tb_result.setRowCount(0)
                    self.first_treeWidget_dict = {}
                    self.second_treeWidget_dict = {}
                    self.signalConnect()
                    self._initEquipTableWidget()
                    self._initSecondTreeWidget("", self.tw_first)
                else:
                    reply = QMessageBox.question(self, '删除', '删除失败', QMessageBox.Yes)
        # 装备目录
        else:
            haveChild = selectUnitDictByUper(self.le_equipID.text())
            if haveChild:
                print("have")
                reply = QMessageBox.question(self, '删除', '该单位有下级单位，是否将下级单位一起删除？', QMessageBox.Yes,
                                             QMessageBox.Cancel)
                if reply == QMessageBox.Yes:
                    Equip_ID = self.le_equipID.text()
                    Equip_Uper = self.le_equipUper.text()
                    del_Equip_And_Child(Equip_ID,Equip_Uper)
                    reply = QMessageBox.question(self, '删除', '删除成功', QMessageBox.Yes)
                    self.slotDisconnect()
                    self.tb_result.clear()
                    self.tw_first.clear()
                    self.tw_second.clear()
                    self.tb_result.setRowCount(0)
                    self.first_treeWidget_dict = {}
                    self.second_treeWidget_dict = {}
                    self.signalConnect()
                    self._initEquipTableWidget()
                    self._initSecondTreeWidget("", self.tw_second)
                else:
                    reply = QMessageBox.question(self, '删除', '删除失败', QMessageBox.Yes)
            else:
                reply = QMessageBox.question(self, '删除', '确定删除吗？', QMessageBox.Yes,
                                             QMessageBox.Cancel)
                if reply == QMessageBox.Yes:
                    Equip_ID = self.le_equipID.text()
                    del_Equip_Dict(Equip_ID)
                    reply = QMessageBox.question(self, '删除', '删除成功', QMessageBox.Yes)
                    self.slotDisconnect()
                    self.tb_result.clear()
                    self.tw_first.clear()
                    self.tw_second.clear()
                    self.tb_result.setRowCount(0)
                    self.first_treeWidget_dict = {}
                    self.second_treeWidget_dict = {}
                    self.signalConnect()
                    self._initEquipTableWidget()
                    self._initSecondTreeWidget("", self.tw_second)
                else:
                    reply = QMessageBox.question(self, '删除', '删除失败', QMessageBox.Yes)