import xlrd
import xlwt
from PyQt5.QtWidgets import QWidget, QAbstractItemView, QTreeWidgetItem, QHeaderView, QInputDialog, QLineEdit, \
    QTableWidgetItem, QMessageBox, QFileDialog

from database.strengthDisturbSql import *
from sysManage.showInputResult import showInputResult
from widgets.strengthDisturb.select_setEquip import widget_Select_SetEquip
from sysManage.userInfo import get_value
from sysManage.component import getMessageBox

class select_setEquip(QWidget,widget_Select_SetEquip):
    def __init__(self,parent=None):
        super(select_setEquip, self).__init__(parent)
        self.setupUi(self)

        # self.tw_first.clear()  # 删除单位目录所有数据显示
        self.tw_second.clear()  # 删除装备目录所有数据显示
        # self.tw_first.header().setVisible(False)  # 不显示树窗口的title
        self.tw_second.header().setVisible(False)  # 不显示树窗口的title
        self.changeUnit = True  # 是否是修改单元的目录
        self.showInputResult = showInputResult(self)
        self.showInputResult.hide()
        # QTableWidget设置整行选中
        self.tb_result.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tb_result.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tb_result.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # self.first_treeWidget_dict = {}  # 当前单位目录列表对象，结构为：{'行号':对应的item}
        self.second_treeWidget_dict = {}  # 当前装备目录列表对象，结构为：{'行号':对应的item}
        self.currentUnitTableResult = []
        # self.unitIDList = []
        self.equipIDList = []
        self.inputEquipInfoList = []
        # self.cb_setChoose.setCurrentIndex(0)
        self.signalConnect()



    def getUserInfo(self):
        self.userInfo = get_value("totleUserInfo")

    '''
        功能：
            清除所有数据
    '''

    def delAllData(self):
        # self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}
        self.currentUnitTableResult = []
        # self.tw_first.clear()  # 清除单元目录所有数据
        self.tw_second.clear()  # 清除装备目录所有数据
        self.tb_result.clear()  # 清除tableWidget中所有数据
        # self.le_first.clear()  # 清除单位查询输入
        self.le_second.clear()
        self.le_equipID.clear()
        # self.le_unitID.clear()
        # self.le_unitName.clear()
        self.le_equipID.clear()
        self.le_equipName.clear()
        self.le_equipUnit.clear()
        self.le_equipUnitInfo.clear()
        self.cb_equipUper.clear()
        # self.le_unitAlias.clear()


    '''
        功能：
            所有信号的连接
    '''

    def signalConnect(self):
        self.pb_add.clicked.connect(self.slotAddDict)  # 添加数据
        self.pb_update.clicked.connect(self.slotUpdate)  # 修改数据
        self.pb_del.clicked.connect(self.slotDelDict)  # 删除数据
        self.tb_result.itemClicked.connect(self.slotClickedRow)  # 选中当前tablewidget的某行
        # self.pb_firstSelect.clicked.connect(self.slotSelectUnit)
        self.pb_secondSelect.clicked.connect(self.slotSelectEquip)
        self.pb_input.clicked.connect(self.slotInputDataByExcel)
        self.pb_output.clicked.connect(self.slotOutputDataIntoExcel)
        self.showInputResult.pb_confirm.clicked.connect(self.slotInputIntoMysql)
        self.showInputResult.pb_cancel.clicked.connect(self.slotCancelInputIntoMysql)

    '''
        功能：
            所有信号的断开
    '''

    def slotDisconnect(self):
        self.pb_add.clicked.disconnect(self.slotAddDict)  # 添加数据
        self.pb_update.clicked.disconnect(self.slotUpdate)  # 修改数据
        self.pb_del.clicked.disconnect(self.slotDelDict)  # 删除数据
        self.tb_result.itemClicked.disconnect(self.slotClickedRow)  # 选中当前tablewidget的某行



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


    def slotSelectEquip(self):
        findText = self.le_second.text()
        for i, item in self.second_treeWidget_dict.items():
            if item.text(0) == findText:
                self.tw_second.setCurrentItem(item)
                break


    # def slotSetEquipUnit(self):
    #     if self.tb_result.currentRow() == -1:
    #         return
    #     text, okPressed = QInputDialog.getText(self, "Get text", "装备单位为:", QLineEdit.Normal, "")
    #     if okPressed:
    #         print(text)
    #         updateEquipUnit(text, self.le_equipID.text())
    #     self.slotEquipDictInit()

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
        # self.tw_first.setDisabled(True)  # 设置单位目录为可选中
        # self.le_first.setDisabled(True)
        # self.pb_firstSelect.setDisabled(True)

        # self.le_unitID.setDisabled(True)
        # self.le_unitName.setDisabled(True)
        self.le_equipID.setDisabled(False)
        self.le_equipName.setDisabled(False)
        self.cb_equipType.setDisabled(False)

        # self.cb_unitUper.setDisabled(True)
        # self.le_unitAlias.setDisabled(True)
        self.cb_equipUper.setDisabled(False)
        self.le_equipUnit.setDisabled(False)
        self.cb_inputType.setDisabled(False)
        self.second_treeWidget_dict = {}
        self.cb_equipUper.clear()
        # self.cb_unitUper.clear()
        self.inputEquipInfoList = []
        self.equipIDList = []
        self.equipIDList = selectAllIDFromEquip()
        self.equipIDList.append("")
        self.cb_equipUper.addItems(self.equipIDList)

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
            header = ['装备编号', '装备名称', '单位','上级装备编号', '录入类型', '装备类型', '装备单位']
            self.tb_result.setColumnCount(len(header))
            self.tb_result.setRowCount(0)
            self.tb_result.setHorizontalHeaderLabels(header)


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
        header = ['装备编号', '装备名称', '单位', '上级装备编号', '录入类型', '装备类型', '装备单位']
        self.tb_result.setColumnCount(len(header))
        self.tb_result.setHorizontalHeaderLabels(header)
        self.equipResultList = []
        self.equipResultList = selectAllDataAboutEquip()
        if self.equipResultList:
            self.tb_result.setRowCount(len(self.equipResultList))
            for i, data in enumerate(self.equipResultList):
                equip_unit_info = selectEquipUnitInfo(data[0])
                print('equip_unit_info')
                print(equip_unit_info)
                item = QTableWidgetItem(data[0])
                self.tb_result.setItem(i, 0, item)
                item = QTableWidgetItem(data[1])
                self.tb_result.setItem(i, 1, item)
                item = QTableWidgetItem(equip_unit_info)
                self.tb_result.setItem(i, 2, item)
                item = QTableWidgetItem(data[2])
                self.tb_result.setItem(i, 3, item)
                item = QTableWidgetItem(data[3])
                self.tb_result.setItem(i, 4, item)
                item = QTableWidgetItem(data[4])
                self.tb_result.setItem(i, 5, item)
                item = QTableWidgetItem(data[5])
                self.tb_result.setItem(i, 6, item)
                self.equipResultList[i].append(equip_unit_info)
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
        self.le_equipID.setText((self.tb_result.item(currentRow, 0).text()))
        self.le_equipName.setText((self.tb_result.item(currentRow, 1).text()))
        inputTypeList = ['空', '逐号录入信息', '逐批录入信息']
        equipTypeList = ['空', '通用装备', '专用装备']
        for i, equipID in enumerate(self.equipIDList):
            if equipID == self.tb_result.item(currentRow, 3).text():
                self.cb_equipUper.setCurrentIndex(i)
                break

        for i, inputType in enumerate(inputTypeList):
            if inputType == self.tb_result.item(currentRow, 4).text():
                self.cb_inputType.setCurrentIndex(i)
                break

        for i, equipType in enumerate(equipTypeList):
            if equipType == self.tb_result.item(currentRow, 5).text():
                self.cb_equipType.setCurrentIndex(i)
                break
        self.le_equipUnitInfo.setText((self.tb_result.item(currentRow, 2).text()))
        self.le_equipUnit.setText((self.tb_result.item(currentRow, 6).text()))

    '''
        功能：
            添加目录
    '''

    def slotAddDict(self):
        if self.le_equipID.text() == "" or self.le_equipName.text() == "":
            getMessageBox('新增失败', '装备ID或装备名字为空，拒绝增加，请重新填写', True, False)
        else:
            Equip_ID = self.le_equipID.text()
            Equip_Name = self.le_equipName.text()
            haveEquipID = selectEquipInfoByEquipID(Equip_ID)
            if haveEquipID:
                getMessageBox('新增失败', '装备ID已存在, 请重新填写', True, False)
                return
            Equip_Uper = self.cb_equipUper.currentText()
            Input_Type = self.cb_inputType.currentText()
            Equip_Type = self.cb_equipType.currentText()
            Equip_Unit = self.le_equipUnit.text()
            Equip_Unit_Info = self.le_equipUnitInfo.text()
            addSuccess = addDataIntoEquip(Equip_ID, Equip_Name, Equip_Uper, Input_Type, Equip_Type, Equip_Unit)
            addEquipInfoSuccess = addDataIntoEquipUnitInfo(Equip_ID, Equip_Unit_Info)
            if addSuccess == True and addEquipInfoSuccess == True:
                getMessageBox('新增', '新增成功', True, False)
                self.slotEquipDictInit()
            else:
                getMessageBox('新增', '新增失败!', True, False)
                return

    '''
        功能：
            修改目录
    '''

    def slotUpdate(self):
        if self.tb_result.currentRow() < 0:
            getMessageBox('修改失败', '请选中某行', True, False)
            return
        # 装备目录
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
            Equip_Unit_Info = self.le_equipUnitInfo.text()
            updateSuccess = updateDataIntoEquip(Equip_ID, Equip_Name, Equip_Uper, Input_Type, Equip_Type,
                                                Equip_Unit)

            if updateSuccess == True and updateDataIntoEquipUnitInfo(Equip_ID, Equip_Unit_Info):
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


    def slotCancelInputIntoMysql(self):
        self.showInputResult.hide()
        self.setDisabled(False)


    def slotInputIntoMysql(self):
        print(self.inputEquipInfoList)
        self.inputEquipInfoList.insert(0, ['1', '装备', '', '空', '空', '', ''])
        for i in range(len(self.inputEquipInfoList)):
            try:
                isHaveEquipId = isHaveEquipment(self.inputEquipInfoList[i][0])
                if isHaveEquipId == False:
                    addSuccess = addDataIntoEquip(self.inputEquipInfoList[i][0], self.inputEquipInfoList[i][1],
                                                  self.inputEquipInfoList[i][2], self.inputEquipInfoList[i][3],
                                                  self.inputEquipInfoList[i][4], self.inputEquipInfoList[i][5])
                    addEquipInfoSuccess = addDataIntoEquipUnitInfo(self.inputEquipInfoList[i][0], self.inputEquipInfoList[i][6])

                else:
                    if i > 1:
                        getMessageBox("导入", "导入第%d数据失败,存在重复数据%d" % i, True, False)
            except Exception as e:
                print(e)
                getMessageBox("导入", "导入第%d数据失败" % i, True, False)
                continue
        getMessageBox('新增', '新增成功', True, False)

        self.slotEquipDictInit()
        self.setDisabled(False)
        self.showInputResult.hide()


    def slotInputDataByExcel(self):
        self.setDisabled(True)
        self.showInputResult.setDisabled(False)
        filename, _ = QFileDialog.getOpenFileName(self, "选中文件", '', "Excel Files (*.xls);;Excel Files (*.xlsx)")
        try:
            workBook = xlrd.open_workbook(filename)
            self.workSheet = workBook.sheet_by_index(0)
            self.inputEquipInfoList = []
            for r in range(1, self.workSheet.nrows):
                equipName = self.workSheet.cell(r, 1).value.strip()
                try:
                    equipId = str(int(self.workSheet.cell(r, 0).value))
                    equipUper = str(int(self.workSheet.cell(r, 3).value))
                except:
                    if equipId == '1' and equipName == '装备':
                        pass
                    else:
                        getMessageBox("读取失败", "读取第%d行数据失败，请检查装备编号或上级装备号是否正确！" % (r), True, False)
                    continue
                inputType = self.workSheet.cell(r, 4).value.strip()
                equipType = self.workSheet.cell(r, 5).value.strip()
                if len(equipType) <= 1:
                    continue
                equipUnit = self.workSheet.cell(r, 6).value.strip()
                equipUnitInfo = self.workSheet.cell(r, 2).value.strip()
                euipmentInfo = []
                euipmentInfo.append(equipId)
                euipmentInfo.append(equipName)
                euipmentInfo.append(equipUper)
                euipmentInfo.append(inputType)
                euipmentInfo.append(equipType)
                euipmentInfo.append(equipUnit)
                euipmentInfo.append(equipUnitInfo)
                self.inputEquipInfoList.append(euipmentInfo)

            self.showInputResult.setWindowTitle("导入Excel数据到数据库装备表中")
            title = ['装备编号', '装备名称', '单位','上级装备号', '录入类型', '装备类型', '装备单位']
            self.showInputResult.tw_result.setColumnCount(len(title))
            self.showInputResult.tw_result.setHorizontalHeaderLabels(title)
            self.showInputResult.tw_result.verticalHeader().setVisible(False)
            self.showInputResult.tw_result.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.showInputResult.tw_result.setRowCount(len(self.inputEquipInfoList))
            for r, list_item in enumerate(self.inputEquipInfoList):
                item = QTableWidgetItem(list_item[0])
                self.showInputResult.tw_result.setItem(r, 0, item)
                item = QTableWidgetItem(list_item[1])
                self.showInputResult.tw_result.setItem(r, 1, item)
                item = QTableWidgetItem(list_item[6])
                self.showInputResult.tw_result.setItem(r, 2, item)
                item = QTableWidgetItem(list_item[2])
                self.showInputResult.tw_result.setItem(r, 3, item)
                item = QTableWidgetItem(list_item[3])
                self.showInputResult.tw_result.setItem(r, 4, item)
                item = QTableWidgetItem(list_item[4])
                self.showInputResult.tw_result.setItem(r, 5, item)
                item = QTableWidgetItem(list_item[5])
                self.showInputResult.tw_result.setItem(r, 6, item)
            self.showInputResult.show()
            return
        except BaseException as e:
            print(e)
            getMessageBox("打开失败", "打开文件失败，请检查文件", True, False)
            self.setDisabled(False)



    '''
        功能：
            导出到excel表格中
    '''
    def slotOutputDataIntoExcel(self):
        # self.setDisabled(True)
        # self.showInputResult.setDisabled(False)
        directoryPath = QFileDialog.getExistingDirectory(self, "请选择导出文件夹", "c:/")
        if len(directoryPath) > 0:
            if len(self.equipResultList) > 0:
                workBook = xlwt.Workbook(encoding='utf-8')
                workSheet = workBook.add_sheet('Sheet1')
                titileStyle = xlwt.XFStyle()  # 初始化样式
                font = xlwt.Font()  # 为样式创建字体
                font.name = '宋体'
                font.bold = True
                font.height = 20 * 11  # 字体大小，11为字号，20为衡量单位
                alignment = xlwt.Alignment()  ## Create Alignment
                alignment.horz = xlwt.Alignment.HORZ_CENTER
                alignment.vert = xlwt.Alignment.VERT_CENTER
                borders = xlwt.Borders()
                borders.left = 2  # 设置为细实线
                borders.right = 2
                borders.top = 2
                borders.bottom = 2
                titileStyle.font = font  # 设定样式
                titileStyle.alignment = alignment
                titileStyle.borders = borders
                workSheet.col(0).width = 4000
                workSheet.col(1).width = 4000
                workSheet.col(2).width = 4000
                workSheet.col(3).width = 4000
                workSheet.col(4).width = 4000
                workSheet.col(5).width = 4000
                contentStyle = xlwt.XFStyle()  # 初始化样式
                font = xlwt.Font()  # 为样式创建字体
                font.name = '宋体'
                font.height = 20 * 11  # 字体大小，11为字号，20为衡量单位
                alignment = xlwt.Alignment()  ## Create Alignment
                alignment.horz = xlwt.Alignment.HORZ_CENTER
                alignment.vert = xlwt.Alignment.VERT_CENTER
                borders = xlwt.Borders()
                borders.left = 1  # 设置为细实线
                borders.right = 1
                borders.top = 1
                borders.bottom = 1
                contentStyle.font = font  # 设定样式
                contentStyle.alignment = alignment
                contentStyle.borders = borders

                workSheet.write(0, 0, '装备编号', titileStyle)
                workSheet.write(0, 1, '装备名称', titileStyle)
                workSheet.write(0, 2, '单位', titileStyle)
                workSheet.write(0, 3, '上级装备号', titileStyle)
                workSheet.write(0, 4, '录入类型', titileStyle)
                workSheet.write(0, 5, '装备类型', titileStyle)
                workSheet.write(0, 6, '装备单位', titileStyle)
                for i, item in enumerate(self.equipResultList):
                    workSheet.write(i + 1, 0, item[0],contentStyle)
                    workSheet.write(i + 1, 1, item[1],contentStyle)
                    workSheet.write(i + 1, 2, item[6],contentStyle)
                    workSheet.write(i + 1, 3, item[2],contentStyle)
                    workSheet.write(i + 1, 4, item[3],contentStyle)
                    workSheet.write(i + 1, 5, item[4],contentStyle)
                    workSheet.write(i + 1, 6, item[5],contentStyle)
                try:
                    workBook.save("%s/装备目录表.xls"%directoryPath)
                    import win32api
                    win32api.ShellExecute(0, 'open', '%s/装备目录表.xls' % directoryPath, '', '', 1)
                    getMessageBox("导出成功", "导出成功！", True, False)
                    return
                except Exception as e:
                    getMessageBox("导出失败", "导出表格被占用，请关闭正在使用的Execl！", True, False)
                    return
            else:
                getMessageBox("未选中任何数据", "导出失败！", True, False)
                return