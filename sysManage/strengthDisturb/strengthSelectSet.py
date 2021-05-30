from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QTableWidgetItem, \
    QAbstractItemView, QMessageBox,QInputDialog,QLineEdit,QFileDialog,QHeaderView
from database.strengthDisturbSql import *
from widgets.strengthDisturb.select_set import Widget_Select_Set
from sysManage.strengthDisturb.equipUnitSet import equipUnitSet
from sysManage.showInputResult import showInputResult
from PyQt5.Qt import Qt
import xlrd
from sysManage.userInfo import get_value
#new
class strengthSelectSet(QWidget, Widget_Select_Set):
    def __init__(self, parent=None):
        super(strengthSelectSet, self).__init__(parent)
        self.setupUi(self)

        self.tw_first.clear()           #删除单位目录所有数据显示
        self.tw_second.clear()          #删除装备目录所有数据显示
        self.tw_first.header().setVisible(False)  # 不显示树窗口的title
        self.tw_second.header().setVisible(False)  # 不显示树窗口的title
        self.changeUnit = True  # 是否是修改单元的目录
        self.showInputResult = showInputResult(self)
        self.showInputResult.hide()
        # QTableWidget设置整行选中
        self.tb_result.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tb_result.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tb_result.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.first_treeWidget_dict = {}  # 当前单位目录列表对象，结构为：{'行号':对应的item}
        self.second_treeWidget_dict = {}  # 当前装备目录列表对象，结构为：{'行号':对应的item}
        self.currentUnitTableResult = []
        self.unitIDList = []
        self.equipIDList = []
        self.cb_setChoose.setCurrentIndex(0)
        self.signalConnect()

    def getUserInfo(self):
        self.userInfo = get_value("totleUserInfo")

    '''
           功能：
               清除所有数据
       '''
    def delAllData(self):
        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}
        self.currentUnitTableResult = []
        self.tw_first.clear()  # 清除单元目录所有数据
        self.tw_second.clear()  # 清除装备目录所有数据
        self.tb_result.clear()  # 清除tableWidget中所有数据
        self.le_first.clear()   #清除单位查询输入
        self.le_second.clear()
        self.le_equipID.clear()
        self.le_unitID.clear()
        self.le_unitName.clear()
        self.le_equipID.clear()
        self.le_equipName.clear()
        self.le_equipUnit.clear()
        self.cb_equipUper.clear()
        self.le_unitAlias.clear()
        self.cb_equipUper.clear()
    '''
        功能：
            所有信号的连接
    '''
    def signalConnect(self):
        self.cb_setChoose.currentIndexChanged.connect(self.slotChangeSet)

        self.pb_add.clicked.connect(self.slotAddDict)  # 添加数据

        self.pb_update.clicked.connect(self.slotUpdate)  # 修改数据
        self.pb_del.clicked.connect(self.slotDelDict)  # 删除数据
        self.tb_result.itemClicked.connect(self.slotClickedRow)  # 选中当前tablewidget的某行
        self.pb_firstSelect.clicked.connect(self.slotSelectUnit)
        self.pb_secondSelect.clicked.connect(self.slotSelectEquip)
        self.pb_input.clicked.connect(self.slotInputDataByExcel)
        self.showInputResult.pb_confirm.clicked.connect(self.slotInputIntoMysql)
        self.showInputResult.pb_cancel.clicked.connect(self.slotCancelInputIntoMysql)

    def slotCancelInputIntoMysql(self):
        self.showInputResult.hide()
        self.setDisabled(False)

    def slotInputIntoMysql(self):
        if self.cb_setChoose.currentIndex() == 0:
            print(self.inputUnitInfoList)
            inputSuccess = inputIntoUnitFromExcel(self.inputUnitInfoList)
            if inputSuccess != True:
                for error in inputSuccess:
                    QMessageBox.information(self, "导入", error, QMessageBox.Yes)
            self.slotUnitDictInit()
            self.setDisabled(False)
            self.showInputResult.hide()


    def slotChangeSet(self):
        if self.cb_setChoose.currentIndex() == 0:
            self.slotUnitDictInit()
        else:
            self.slotEquipDictInit()

    def slotSelectUnit(self):
        findText = self.le_first.text()
        for i, item in self.first_treeWidget_dict.items():
            if item.text(0) == findText:
                self.tw_first.setCurrentItem(item)
                break

    def slotInputDataByExcel(self):
        self.setDisabled(True)
        self.showInputResult.setDisabled(False)
        if self.cb_setChoose.currentIndex() == 0:
            filename, _ = QFileDialog.getOpenFileName(self, "选中文件", '', "Excel files(*.xlsx, *.xls)")
            print(filename)
            try:
                self.rdfile = xlrd.open_workbook(filename)
                self.tablename = "unit"
                self.sheet = self.rdfile.sheet_by_name("unit")
                self.inputUnitInfoList = []
                self.showInputResult.setWindowTitle("导入Excel数据到数据库Unit表中")
                self.showInputResult.show()
                title = ['单位编号', '单位名称', '上级单位编号', '单位别名', '是否为旅团']

                self.showInputResult.tw_result.setColumnCount(self.sheet.ncols)
                self.showInputResult.tw_result.setHorizontalHeaderLabels(title)
                self.showInputResult.tw_result.setRowCount(self.sheet.nrows - 1)
                for r in range(1, self.sheet.nrows):
                    Unit_ID = self.sheet.cell(r,0).value
                    Unit_Name = self.sheet.cell(r,1).value
                    Unit_Uper = self.sheet.cell(r,2).value
                    Unit_Alias = self.sheet.cell(r,3).value
                    Is_Group = self.sheet.cell(r, 4).value
                    item = QTableWidgetItem(Unit_ID)
                    self.showInputResult.tw_result.setItem(r-1, 0, item)
                    item = QTableWidgetItem(Unit_Name)
                    self.showInputResult.tw_result.setItem(r - 1, 1, item)
                    item = QTableWidgetItem(Unit_Uper)
                    self.showInputResult.tw_result.setItem(r - 1, 2, item)
                    item = QTableWidgetItem(Unit_Alias)
                    self.showInputResult.tw_result.setItem(r - 1, 3, item)
                    item = QTableWidgetItem(Is_Group)
                    self.showInputResult.tw_result.setItem(r - 1, 4, item)
                    unitInfo = []
                    unitInfo.append(Unit_ID)
                    unitInfo.append(Unit_Name)
                    unitInfo.append(Unit_Uper)
                    unitInfo.append(Unit_Alias)
                    unitInfo.append(Is_Group)
                    self.inputUnitInfoList.append(unitInfo)
                return
            except BaseException as e:
                print(e)
                QMessageBox.about(self, "打开失败", "打开文件失败，请检查文件")
                self.setDisabled(False)
        else:
            pass

    def slotSelectEquip(self):
        findText = self.le_second.text()
        for i, item in self.second_treeWidget_dict.items():
            if item.text(0) == findText:
                self.tw_second.setCurrentItem(item)
                break

    def slotSetUnitAlias(self):
        if self.tb_result.currentRow() == -1:
            return
        text, okPressed = QInputDialog.getText(self, "设置别名", "该单位别名为:", QLineEdit.Normal, "")
        if okPressed:
            print(text)
            updateUnitAlias(text, self.le_unitID.text())
        self.slotUnitDictInit()


    def slotSetEquipUnit(self):
        if self.tb_result.currentRow() == -1:
            return
        text, okPressed = QInputDialog.getText(self, "Get text", "装备单位为:", QLineEdit.Normal, "")
        if okPressed:
            print(text)
            updateEquipUnit(text, self.le_equipID.text())
        self.slotEquipDictInit()

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
            点击设置单元目录按钮后的初始化
    '''
    def slotUnitDictInit(self):
        self.getUserInfo()
        self.delAllData()
        self.tb_result.setEditTriggers(QAbstractItemView.NoEditTriggers)        #设置tablewidget不能修改
        #设置当前控件状态
        self.tw_second.setDisabled(True)     #设置装备目录为灰色
        self.le_second.setDisabled(True)
        self.pb_secondSelect.setDisabled(True)   #设置装备目录上面的查询为灰色
        self.tw_first.setDisabled(False)    #设置单位目录为可选中
        self.le_first.setDisabled(False)
        self.pb_firstSelect.setDisabled(False)

        self.le_unitID.setDisabled(False)
        self.le_unitName.setDisabled(False)
        self.le_equipID.setDisabled(True)
        self.le_equipName.setDisabled(True)
        self.cb_equipType.setDisabled(True)

        self.cb_unitUper.setDisabled(False)
        self.le_unitAlias.setDisabled(False)
        self.cb_equipUper.setDisabled(True)
        self.le_equipUnit.setDisabled(True)
        self.cb_inputType.setDisabled(True)
        self.first_treeWidget_dict = {}
        self.unitIDList = []

        self.cb_unitUper.clear()
        self.unitIDList = selectAllIDFromUnit()
        self.unitIDList.append("")
        self.cb_unitUper.addItems(self.unitIDList)
        if self.userInfo:
            self.startInfo = selectUnitInfoByUnitID(self.userInfo[0][4])
            stack = []
            root = []
            if self.startInfo:
                stack.append(self.startInfo)
                root.append(self.tw_first)
                self.initUnitTreeWidget(stack, root)
                #从数据库中单位表中获取数据初始化单位目录，tableWidget显示所有的单位表
                self._initUnitTableWidget()
            else:
                header = ['单位编号', '单位名称', '上级单位编号', '单位别名']
                self.tb_result.setColumnCount(len(header))
                self.tb_result.setRowCount(0)
                self.tb_result.setHorizontalHeaderLabels(header)
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

        self.le_unitID.setDisabled(True)
        self.le_unitName.setDisabled(True)
        self.le_equipID.setDisabled(False)
        self.le_equipName.setDisabled(False)
        self.cb_equipType.setDisabled(False)

        self.cb_unitUper.setDisabled(True)
        self.le_unitAlias.setDisabled(True)
        self.cb_equipUper.setDisabled(False)
        self.le_equipUnit.setDisabled(False)
        self.cb_inputType.setDisabled(False)
        self.second_treeWidget_dict = {}
        self.cb_equipUper.clear()
        self.cb_unitUper.clear()
        self.equipIDList = []

        self.equipIDList = selectAllIDFromEquip()
        self.equipIDList.append("")
        self.cb_equipUper.addItems(self.equipIDList)
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
            self._initEquipTableWidget()
        else:
            header = ['装备编号', '装备名称', '上级装备编号', '录入类型', '装备类型', '装备单位']
            self.tb_result.setColumnCount(len(header))
            self.tb_result.setRowCount(0)
            self.tb_result.setHorizontalHeaderLabels(header)
    '''
        功能：
            设置单元时的初始化tableWidget，显示整个单位表
    '''
    def _initUnitTableWidget(self):
        header = ['单位编号', '单位名称', '上级单位编号','单位别名']
        self.tb_result.setColumnCount(len(header))
        self.tb_result.setHorizontalHeaderLabels(header)
        resultList = []
        selectSuccess = selectAllDataAboutUnit(resultList)
        if selectSuccess != True:
            QMessageBox.information(self, "初始化", "初始化单位表失败", QMessageBox.Yes)
            return

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


        # print(result)   #测试查找到的数据

    '''
        功能：
            装备目录的初始化，显示整个装备表
            参数表：root为上级装备名字，mother为上级节点对象
    '''
    def _initEquipTreeWidget(self, root, mother):
        if root == '':
            result = selectEquipInfoByEquipUper('')
        else:
            result = selectEquipInfoByEquipUper(root)

        #rowData: (装备编号，装备名称，上级装备编号, 录入类型, 装备类型)
        for rowData in result:
            item = QTreeWidgetItem(mother)
            item.setText(0, rowData[1])
            self.second_treeWidget_dict[rowData[0]] = item
            if rowData[0] != '':
                self._initEquipTreeWidget(rowData[0], item)
            else:
                return

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
        if currentRow < 0:
            return

        if self.cb_setChoose.currentIndex() == 0:
            self.le_unitID.setText(self.tb_result.item(currentRow, 0).text())
            self.le_unitName.setText(self.tb_result.item(currentRow, 1).text())
            for i, unitID in enumerate(self.unitIDList):
                if self.tb_result.item(currentRow, 2).text() == unitID:
                    self.cb_unitUper.setCurrentIndex(i)
                    break
            self.le_unitAlias.setText(self.tb_result.item(currentRow, 3).text())
        else:
            self.le_equipID.setText((self.tb_result.item(currentRow,0).text()))
            self.le_equipName.setText((self.tb_result.item(currentRow, 1).text()))
            inputTypeList = ['空','逐号录入信息', '逐批录入信息']
            equipTypeList = ['空', '通用装备','专用装备']
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
        if self.cb_setChoose.currentIndex() == 0:
            if self.le_unitID.text() == "" or self.le_unitName.text() == "":
                reply = QMessageBox.question(self, '新增失败', '单位ID或单位名字为空，拒绝增加，请重新填写', QMessageBox.Yes)
            else:
                Unit_ID = self.le_unitID.text()
                Unit_Name = self.le_unitName.text()
                Unit_Uper = self.cb_unitUper.currentText()
                Unit_Alias = self.le_unitAlias.text()
                haveUnitID = selectUnitInfoByUnitID(Unit_ID)
                if haveUnitID:
                    reply = QMessageBox.information(self, '新增失败', '单位ID已存在, 请重新填写', QMessageBox.Yes)
                    return

                addSuccess = addDataIntoUnit(Unit_ID, Unit_Name, Unit_Uper, Unit_Alias, "否")
                if addSuccess == True:
                    reply = QMessageBox.information(self, '新增', '新增成功', QMessageBox.Yes)
                else:
                    reply = QMessageBox.information(self, '新增', str(addSuccess) + '，新增失败', QMessageBox.Yes)
                    return
                self.slotUnitDictInit()
        # 装备目录
        elif self.cb_setChoose.currentIndex() == 1:
            if self.le_equipID.text() == "" or self.le_equipName.text() == "":
                reply = QMessageBox.information(self, '新增失败', '装备ID或装备名字为空，拒绝增加，请重新填写', QMessageBox.Yes)
            else:
                Equip_ID = self.le_equipID.text()
                Equip_Name = self.le_equipName.text()
                haveEquipID = selectEquipInfoByEquipID(Equip_ID)
                if haveEquipID:
                    reply = QMessageBox.information(self, '新增失败', '装备ID已存在, 请重新填写', QMessageBox.Yes)
                    return
                Equip_Uper = self.cb_equipUper.currentText()
                Input_Type = self.cb_inputType.currentText()
                Equip_Type = self.cb_equipType.currentText()
                Equip_Unit = self.le_equipUnit.text()
                addSuccess = addDataIntoEquip(Equip_ID, Equip_Name, Equip_Uper, Input_Type, Equip_Type, Equip_Unit)
                if addSuccess == True:
                    reply = QMessageBox.information(self, '新增', '新增成功', QMessageBox.Yes)
                    self.slotEquipDictInit()
                else:
                    reply = QMessageBox.information(self, '新增', str(addSuccess) + ',新增失败', QMessageBox.Yes)
                    return
    '''
        功能：
            修改目录
    '''
    def slotUpdate(self):
        # 单位目录
        if self.tb_result.currentRow() < 0:
            reply = QMessageBox.question(self, '修改失败', '请选中某行', QMessageBox.Yes)
            return
        if self.cb_setChoose.currentIndex() == 0:
            if (self.tb_result.item(self.tb_result.currentRow(),
                                    0).text() != self.le_unitID.text()) or self.le_unitName.text() == "":
                reply = QMessageBox.question(self, '修改失败', '单位ID不能修改或单位名字为空，拒绝修改，请重新填写', QMessageBox.Yes)
                self.le_unitID.setText(self.tb_result.item(self.tb_result.currentRow(),0).text())
                return
            else:
                Unit_ID = self.le_unitID.text()
                Unit_Name = self.le_unitName.text()
                Unit_Uper = self.cb_unitUper.currentText()
                Unit_Alias = self.le_unitAlias.text()

                updateSuccess = updateDataIntoUnit(Unit_ID, Unit_Name, Unit_Uper,Unit_Alias)
                if updateSuccess == True:
                    reply = QMessageBox.question(self, '修改', '修改成功', QMessageBox.Yes)
                    self.slotUnitDictInit()
                else:
                    reply = QMessageBox.question(self, '修改', str(updateSuccess) + '，修改失败', QMessageBox.Yes)
                    return
        # 装备目录
        elif self.cb_setChoose.currentIndex() == 1:
            if (self.tb_result.item(self.tb_result.currentRow(),
                                    0).text() != self.le_equipID.text()) or self.le_equipName.text() == "":
                reply = QMessageBox.question(self, '修改失败', '装备ID不能修改或装备名字为空，拒绝修改，请重新填写', QMessageBox.Yes,
                                             QMessageBox.Cancel)
                self.le_equipID.setText(self.tb_result.item(self.tb_result.currentRow(),0).text())
                return
            else:
                Equip_ID = self.le_equipID.text()
                Equip_Name = self.le_equipName.text()
                Equip_Uper = self.cb_equipUper.currentText()
                Input_Type = self.cb_inputType.currentText()
                Equip_Type = self.cb_equipType.currentText()
                Equip_Unit = self.le_equipUnit.text()
                updateSuccess = updateDataIntoEquip(Equip_ID, Equip_Name, Equip_Uper, Input_Type, Equip_Type, Equip_Unit)
                if updateSuccess == True:
                    reply = QMessageBox.question(self, '修改', '修改成功', QMessageBox.Yes)
                    self.slotEquipDictInit()
                else:
                    reply = QMessageBox.question(self, '修改', str(updateSuccess) + '，修改失败', QMessageBox.Yes)
                    return
    '''
        功能：
            删除目录
    '''

    def slotDelDict(self):
        # 单位目录
        if self.tb_result.currentRow() < 0:
            reply = QMessageBox.question(self, '删除', '请选中某一行', QMessageBox.Yes)
            return
        if self.cb_setChoose.currentIndex() == 0:
            reply = QMessageBox.question(self, '删除', '是否将下级单位以及所涉及的其他表关于该单位的信息一起删除？', QMessageBox.Yes,
                                             QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                delSuccess = delDataInUnit(self.le_unitID.text())
                if delSuccess == True:
                    reply = QMessageBox.question(self, '删除', '删除成功', QMessageBox.Yes)
                    self.slotUnitDictInit()
                else:
                    reply = QMessageBox.question(self, '删除', str(delSuccess) + ',删除失败', QMessageBox.Yes)
                    return
            else:
                reply = QMessageBox.question(self, '删除', '删除失败', QMessageBox.Yes)
                return
        #装备目录
        elif self.cb_setChoose.currentIndex() == 1:
            reply = QMessageBox.question(self, '删除', '是否将下级装备以及所涉及的其他表关于该装备的信息一起删除？', QMessageBox.Yes,
                                         QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                delSuccess = delDataInEquip(self.le_equipID.text())
                if delSuccess == True:
                    reply = QMessageBox.question(self, '删除', '删除成功', QMessageBox.Yes)
                    self.slotEquipDictInit()
                else:
                    reply = QMessageBox.question(self, '删除', str(delSuccess) + ',删除失败', QMessageBox.Yes)
                    return
            else:
                reply = QMessageBox.question(self, '删除', '删除失败', QMessageBox.Yes)

'''
    功能：
        单元测试
'''
if __name__ == '__main__':
    pass