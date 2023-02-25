from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QAbstractItemView, QTreeWidgetItem

from database.alocatMangeSql import *
from database.positionEngneerSql import delDataInPosenginUnit
from sysManage.alocatMange.AddUnitChoose import *
from sysManage.component import getMessageBox
from sysManage.userInfo import *
from widgets.alocatMange.select_set import Widget_Dict_Set

# new
'''
    功能：
        目录管理
'''


class alocatDictSet(QWidget, Widget_Dict_Set):
    def __init__(self, parent=None):
        super(alocatDictSet, self).__init__(parent)
        self.setupUi(self)

        self.tw_first.clear()  # 删除单位目录所有数据显示
        self.tw_second.clear()  # 删除装备目录所有数据显示
        self.tw_first.header().setVisible(False)  # 不显示树窗口的title
        self.tw_second.header().setVisible(False)  # 不显示树窗口的title
        self.changeUnit = '0'  # 是否是修改单元的目录

        # QTableWidget设置整行选中
        self.tb_result.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tb_result.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tb_result.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.first_treeWidget_dict = {}  # 当前单位目录列表对象，结构为：{'行号':对应的item}
        self.second_treeWidget_dict = {}  # 当前装备目录列表对象，结构为：{'行号':对应的item}

        self.addUnitChoose = AddUnitChoose()
        self.signalConnect()

    '''
        功能：
            所有信号的连接
    '''

    def signalConnect(self):
        self.pb_add.clicked.connect(self.slotAddDict)  # 添加数据
        self.pb_update.clicked.connect(self.slotUpdate)  # 修改数据
        self.pb_del.clicked.connect(self.slotDelDict)  # 删除数据

        self.tb_result.itemClicked.connect(self.slotClickedRow)  # 选中当前tablewidget的某行

        self.pb_setUnit.clicked.connect(self.slotUnitDictInit)  # 设置单元目录

        self.pb_setEquip.clicked.connect(self.slotEquipDictInit)  # 设置装备目录
        self.pb_firstSelect.clicked.connect(self.slotSelectUnit)
        self.addUnitChoose.signal.connect(self.updateUnit)

    def slotSelectUnit(self):
        findText = self.le_first.text()
        for i, item in self.first_treeWidget_dict.items():
            if item.text(0) == findText:
                self.tw_first.setCurrentItem(item)
                break


    '''
            功能：
                所有信号的断开
    '''

    def slotDisconnect(self):
        self.pb_add.clicked.disconnect(self.slotAddDict)  # 添加数据
        self.pb_update.clicked.disconnect(self.slotUpdate)  # 修改数据
        self.pb_del.clicked.disconnect(self.slotDelDict)  # 删除数据

        self.tb_result.itemClicked.disconnect(self.slotClickedRow)  # 选中当前tablewidget的某行

        self.pb_setUnit.clicked.disconnect(self.slotUnitDictInit)  # 设置单元目录

        self.pb_setEquip.clicked.disconnect(self.slotEquipDictInit)  # 设置装备目录


    '''
        功能：
            清除所有数据
    '''

    def delAllData(self):
        self.tw_first.clear()  # 清除单元目录所有数据
        self.tw_second.clear()  # 清除装备目录所有数据
        self.tb_result.clear()  # 清除tableWidget中所有数据
        self.le_first.clear()
        self.le_second.clear()

    def getUserInfo(self):
        self.userInfo = get_value("totleUserInfo")
    '''
        功能：
            点击设置单元目录按钮后的初始化
    '''

    def slotUnitDictInit(self):
        self.delAllData()
        self.tb_result.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置tablewidget不能修改
        # 设置当前控件状态
        self.tw_second.setDisabled(True)  # 设置装备目录为灰色
        self.le_second.setDisabled(True)
        self.pb_secondSelect.setDisabled(True)  # 设置装备目录上面的查询为灰色
        self.tw_first.setDisabled(False)  # 设置单位目录为可选中
        self.le_first.setDisabled(False)
        self.pb_firstSelect.setDisabled(False)
        self.le_equipUnit.setDisabled(True)
        self.le_equipID.setDisabled(True)
        self.le_equipName.setDisabled(True)
        self.cb_equipType.setDisabled(True)
        self.cb_inputType.setDisabled(True)
        self.pb_add.setDisabled(1)
        self.pb_update.setDisabled(1)
        self.pb_del.setDisabled(1)
        self.cb_equipUper.setDisabled(True)
        self.pb_setUnit.setDisabled(True)
        self.pb_setEquip.setDisabled(False)
        # 从数据库中单位表中获取数据初始化单位目录，tableWidget显示所有的单位表
        self._initUnitTreeWidget("", self.tw_first)
        self._initUnitTableWidget()

        self.changeUnit = '1'  # 设置当前为修改单位状态

    '''
            功能：
                点击设置装备目录按钮后的初始化
    '''

    def slotEquipDictInit(self):
        self.getUserInfo()
        self.delAllData()
        self.tb_result.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置tablewidget不能修改
        # 设置当前控件状态
        self.tw_second.setDisabled(False)  # 设置装备目录为灰色
        self.le_second.setDisabled(False)
        self.pb_secondSelect.setDisabled(False)  # 设置装备目录上面的查询为灰色
        self.tw_first.setDisabled(True)  # 设置单位目录为可选中
        self.le_first.setDisabled(True)
        self.pb_firstSelect.setDisabled(True)
        self.le_equipID.setDisabled(False)
        self.le_equipName.setDisabled(False)
        self.cb_equipType.setDisabled(False)
        self.cb_inputType.setDisabled(False)
        self.pb_add.setDisabled(0)
        self.pb_update.setDisabled(0)
        self.cb_equipUper.setDisabled(False)
        self.le_equipUnit.setDisabled(False)
        self.pb_setUnit.setDisabled(False)
        self.pb_setEquip.setDisabled(True)

        self.cb_equipUper.clear()
        self.equipIDList = []

        self.equipIDList = selectAllIDFromEquip()
        self.equipIDList.append("")
        self.cb_equipUper.addItems(self.equipIDList)
        # 从数据库中单位表中获取数据初始化单位目录，tableWidget显示所有的单位表
        equipInfo = selectEquipInfoByEquipUper("")
        stack = []
        root = []
        if equipInfo:
            stack.append(equipInfo[0])
            root.append(self.tw_second)
            self.initEquipTreeWidget(stack, root)
            # 从数据库中单位表中获取数据初始化单位目录，tableWidget显示所有的单位表
            # self._initUnitTreeWidget("", self.tw_first)
            self._initEquipTableWidget()
        else:
            header = ['装备编号', '装备名称', '上级装备编号', '录入类型', '装备类型', '装备单位']
            self.tb_result.setColumnCount(len(header))
            self.tb_result.setRowCount(0)
            self.tb_result.setHorizontalHeaderLabels(header)

        self.changeUnit = '2'  # 设置当前为修改单位状态

    '''
        功能：
            单位目录的初始化，显示整个单位表
            参数表：root为上级单位名字，mother为上级节点对象
    '''

    def _initUnitTreeWidget(self, root, mother):
        if root == '':
            result = selectDisturbPlanUnitInfoByDeptUper('')
        else:
            result = selectDisturbPlanUnitInfoByDeptUper(root)

        # rowData: (单位编号，单位名称，上级单位编号)
        for rowData in result:
            item = QTreeWidgetItem(mother)
            item.setText(0, rowData[1])
            self.first_treeWidget_dict[rowData[0]] = item
            if rowData[0] != '':
                self._initUnitTreeWidget(rowData[0], item)

    '''
        功能：
            设置单元时的初始化tableWidget，显示整个单位表
    '''

    def _initUnitTableWidget(self):
        result = selectAllDataAboutDisturbPlanUnit()

        header = ['单位编号', '单位名称', '上级单位编号', '单位别名']
        self.tb_result.setColumnCount(len(header))
        self.tb_result.setRowCount(len(result))
        self.tb_result.setHorizontalHeaderLabels(header)

        for i, data in enumerate(result):
            item = QTableWidgetItem(data[0])
            self.tb_result.setItem(i, 0, item)
            item = QTableWidgetItem(data[1])
            self.tb_result.setItem(i, 1, item)
            item = QTableWidgetItem(data[2])
            self.tb_result.setItem(i, 2, item)
            item = QTableWidgetItem(data[3])
            self.tb_result.setItem(i, 3, item)

        # print(result)   #测试查找到的数据

    '''
        功能：
            装备目录的初始化，显示整个装备表
            参数表：root为上级装备名字，mother为上级节点对象
    '''
    def initEquipTreeWidget(self, stack, root):
        while stack:
            EquipInfo = stack.pop(0)
            item = QTreeWidgetItem(root.pop(0))
            item.setText(0, EquipInfo[1])
            self.second_treeWidget_dict[EquipInfo[0]] = item
            result = selectEquipInfoByEquipUper(EquipInfo[0])
            for resultInfo in result:
                stack.append(resultInfo)
                root.append(item)

    '''
        功能：
            设置装备时的初始化tableWidget，显示整个装备表
    '''

    def _initEquipTableWidget(self):
        self.result = []

        header = ['装备编号', '装备名称', '上级装备编号', '录入类型', '装备类型', '装备单位']
        self.tb_result.setColumnCount(len(header))
        self.tb_result.setHorizontalHeaderLabels(header)
        resultList = selectAllDataAboutEquip()
        if resultList:
            self.tb_result.setRowCount(len(resultList))
            for i, data in enumerate(resultList):
                item = QTableWidgetItem(data[0])
                self.tb_result.setItem(i, 0, item)
                item = QTableWidgetItem(data[1])
                self.tb_result.setItem(i, 1, item)
                item = QTableWidgetItem(data[2])
                self.tb_result.setItem(i, 2, item)
                item = QTableWidgetItem(data[3])
                self.tb_result.setItem(i, 3, item)
                item = QTableWidgetItem(data[4])
                self.tb_result.setItem(i, 4, item)
                item = QTableWidgetItem(data[5])
                self.tb_result.setItem(i, 5, item)
        else:
            self.tb_result.setRowCount(0)

        # print(result)   #测试查找到的数据

    '''
        功能：
            当选中tablewidget某行时，显示对应的lineedit
    '''

    def slotClickedRow(self):

        currentRow = self.tb_result.currentRow()
        if self.changeUnit == '1':
            pass
        elif self.changeUnit == '2':
            self.le_equipID.setText((self.tb_result.item(currentRow, 0).text()))
            self.le_equipName.setText((self.tb_result.item(currentRow, 1).text()))
            inputTypeList = ['空', '逐号录入信息', '逐批录入信息']
            equipTypeList = ['空', '通用装备', '专用装备']
            for i, equipID in enumerate(self.equipIDList):
                if equipID == self.tb_result.item(currentRow, 2).text():
                    self.cb_equipUper.setCurrentIndex(i)
                    break

            for i, inputType in enumerate(inputTypeList):
                if inputType == self.tb_result.item(currentRow, 3).text():
                    self.cb_inputType.setCurrentIndex(i)
                    break

            for i, equipType in enumerate(equipTypeList):
                if equipType == self.tb_result.item(currentRow, 4).text():
                    self.cb_equipType.setCurrentIndex(i)
                    break

            self.le_equipUnit.setText((self.tb_result.item(currentRow, 5).text()))


    '''
        功能：
            添加目录
    '''

    def slotAddDict(self):
        # 单位目录
        if self.changeUnit == '1':
            self.addUnitChoose.initWidget()
            self.addUnitChoose.tb_unitChoose.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.addUnitChoose.tb_unitChoose.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.addUnitChoose.setWindowFlags(Qt.Dialog|Qt.WindowCloseButtonHint)
            self.addUnitChoose.show()

        # 装备目录
        elif self.changeUnit == '2':
            if self.le_equipID.text() == "" or self.le_equipName.text() == "":
                getMessageBox('新增失败', '装备ID或装备名字为空，拒绝增加，请重新填写', True, False)
            else:
                Equip_ID = self.le_equipID.text()
                Equip_Name = self.le_equipName.text()
                haveEquipID = selectEquipInfoByEquipID(Equip_ID)
                if haveEquipID:
                    getMessageBox( '新增失败', '装备ID已存在, 请重新填写', True, False)
                    return
                Equip_Uper = self.cb_equipUper.currentText()
                Input_Type = self.cb_inputType.currentText()
                Equip_Type = self.cb_equipType.currentText()
                Equip_Unit = self.le_equipUnit.text()
                addSuccess = addDataIntoEquip(Equip_ID, Equip_Name, Equip_Uper, Input_Type, Equip_Type, Equip_Unit)
                if addSuccess == True:
                    getMessageBox('新增', '新增成功', True, False)
                    self.slotEquipDictInit()
                else:
                    getMessageBox('新增', str(addSuccess) + ',新增失败', True, False)
                    return

    def updateUnit(self):
        insertIntoDisturbPlanUnitFromList(self.addUnitChoose.currentUnitID)
        print("self.addUnitChoose.currentUnitID",self.addUnitChoose.currentUnitID)
        self.slotUnitDictInit()

    '''
        功能：
            修改目录
    '''

    def slotUpdate(self):
        if self.tb_result.currentRow() < 0:
            getMessageBox('修改失败', '请选中某行', True, False)
            return
        # 单位目录
        if self.changeUnit == '1':
            pass
        # 装备目录
        elif self.changeUnit == '2':
            if (self.tb_result.item(self.tb_result.currentRow(),
                                    0).text() != self.le_equipID.text()) or self.le_equipName.text() == "":
                getMessageBox('修改失败', '装备ID不能修改或装备名字为空，拒绝修改，请重新填写', True, False)
                self.le_equipID.setText(self.tb_result.item(self.tb_result.currentRow(), 0).text())
                return
            else:
                Equip_ID = self.le_equipID.text()
                Equip_Name = self.le_equipName.text()
                Equip_Uper = self.cb_equipUper.currentText()
                Input_Type = self.cb_inputType.currentText()
                Equip_Type = self.cb_equipType.currentText()
                Equip_Unit = self.le_equipUnit.text()
                updateSuccess = updateDataIntoEquip(Equip_ID, Equip_Name, Equip_Uper, Input_Type, Equip_Type,
                                                    Equip_Unit)
                if updateSuccess == True:
                    getMessageBox('修改', '修改成功', True, False)
                    self.slotEquipDictInit()
                else:
                    getMessageBox('修改', str(updateSuccess) + '，修改失败', True, False)
                    return

    '''
        功能：
            删除目录
    '''
    def slotDelDict(self):
        if self.tb_result.currentRow() < 0:
            getMessageBox('删除', '请选中某一行', True, False)
            return
        # 单位目录
        if self.changeUnit == '1':
            reply = getMessageBox('删除', '是否将下级单位以及所涉及的其他表关于该单位的信息一起删除？', True, False)
            if reply == QMessageBox.Ok:
                delDataInDisturbPlanUnit(self.le_unitID.text())
                delDataInPosenginUnit(self.le_unitID.text())
                getMessageBox('删除', '删除成功', True, False)
                self.slotUnitDictInit()

            else:
                getMessageBox('删除', '删除失败', True, False)
        # 装备目录
        elif self.changeUnit == '2':
            reply = getMessageBox('删除', '是否将下级装备以及所涉及的其他表关于该装备的信息一起删除？', True, True)
            if reply == QMessageBox.Ok:
                delSuccess = delDataInEquip(self.le_equipID.text())
                if delSuccess == True:
                    getMessageBox('删除', '删除成功', True, False)
                    self.slotEquipDictInit()
                else:
                    getMessageBox('删除', str(delSuccess) + ',删除失败', True, False)
                    return
            else:
                getMessageBox('删除', '删除失败', True, False)


'''
    功能：
        单元测试
'''
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = alocatDictSet()
    widget.show()
    sys.exit(app.exec_())