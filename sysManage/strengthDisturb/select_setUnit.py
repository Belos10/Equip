import xlrd
import xlwt
from PyQt5.QtWidgets import QWidget, QAbstractItemView, QInputDialog, QLineEdit, QMessageBox, QTableWidgetItem, \
    QTreeWidgetItem, QHeaderView, QFileDialog
from database.strengthDisturbSql import *
from utills.Search import selectUnit
from widgets.strengthDisturb.select_setUnit import widget_Select_SetUnit
from sysManage.showInputResult import showInputResult
from sysManage.userInfo import get_value
from sysManage.component import getMessageBox, getTextInputDialog
'''
    目录设置-设置单位目录
'''

class select_setUnit(QWidget,widget_Select_SetUnit):
    def __init__(self,parent=None):
        super(select_setUnit, self).__init__(parent)
        self.setupUi(self)

        self.tw_first.clear()  # 删除单位目录所有数据显示
        # self.tw_second.clear()  # 删除装备目录所有数据显示
        self.tw_first.header().setVisible(False)  # 不显示树窗口的title
        # self.tw_second.header().setVisible(False)  # 不显示树窗口的title
        self.changeUnit = True  # 是否是修改单元的目录
        self.inputUnitInfoList = []
        self.showInputResult = showInputResult(self)
        self.showInputResult.hide()
        # QTableWidget设置整行选中
        self.tb_result.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tb_result.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tb_result.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.first_treeWidget_dict = {}  # 当前单位目录列表对象，结构为：{'行号':对应的item}
        # self.second_treeWidget_dict = {}  # 当前装备目录列表对象，结构为：{'行号':对应的item}
        self.currentUnitTableResult = []
        self.unitIDList = []
        # self.equipIDList = []
        self.signalConnect()

    def getUserInfo(self):
        self.userInfo = get_value("totleUserInfo")


    '''
        功能：
            所有信号的连接
    '''

    def signalConnect(self):
        self.pb_add.clicked.connect(self.slotAddDict)  # 添加数据
        self.pb_update.clicked.connect(self.slotUpdate)  # 修改数据
        self.pb_del.clicked.connect(self.slotDelDict)  # 删除数据
        self.tb_result.itemClicked.connect(self.slotClickedRow)  # 选中当前tablewidget的某行
        self.pb_firstSelect.clicked.connect(self.slotSelectUnit)
        # self.pb_secondSelect.clicked.connect(self.slotSelectEquip)
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


    '''
       功能：
           清除所有数据
    '''

    def delAllData(self):
        self.first_treeWidget_dict = {}
        # self.second_treeWidget_dict = {}
        self.currentUnitTableResult = []
        self.tw_first.clear()  # 清除单元目录所有数据
        # self.tw_second.clear()  # 清除装备目录所有数据
        # self.tb_result.clear()  # 清除tableWidget中所有数据
        self.le_first.clear()  # 清除单位查询输入
        # self.le_second.clear()
        # self.le_equipID.clear()
        self.le_unitID.clear()
        self.le_unitName.clear()
        # self.le_equipID.clear()
        # self.le_equipName.clear()
        # self.le_equipUnit.clear()
        # self.cb_equipUper.clear()
        self.le_unitAlias.clear()



    def slotUnitDictInit(self):
        self.getUserInfo()
        self.delAllData()
        self.tb_result.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 设置tablewidget不能修改
        # 设置当前控件状态
        # self.tw_second.setDisabled(True)  # 设置装备目录为灰色
        # self.le_second.setDisabled(True)
        # self.pb_secondSelect.setDisabled(True)  # 设置装备目录上面的查询为灰色
        self.tw_first.setDisabled(False)  # 设置单位目录为可选中
        self.le_first.setDisabled(False)
        self.pb_firstSelect.setDisabled(False)

        self.le_unitID.setDisabled(False)
        self.le_unitName.setDisabled(False)
        # self.le_equipID.setDisabled(True)
        # self.le_equipName.setDisabled(True)
        # self.cb_equipType.setDisabled(True)

        self.cb_unitUper.setDisabled(False)
        self.le_unitAlias.setDisabled(False)
        # self.cb_equipUper.setDisabled(True)
        # self.le_equipUnit.setDisabled(True)
        # self.cb_inputType.setDisabled(True)
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
                # 从数据库中单位表中获取数据初始化单位目录，tableWidget显示所有的单位表
                self._initUnitTableWidget()
            else:
                header = ['单位编号', '单位名称', '上级单位编号', '单位代号']
                self.tb_result.setColumnCount(len(header))
                self.tb_result.setRowCount(0)
                self.tb_result.setHorizontalHeaderLabels(header)


    def slotSetUnitAlias(self):
        if self.tb_result.currentRow() == -1:
            return
        # text, okPressed = QInputDialog.getText(self, "设置别名", "该单位代号为:", QLineEdit.Normal, "")
        okPressed, text = getTextInputDialog("设置别名", "该单位代号为:", True, True)
        if okPressed:
            print(text)
            updateUnitAlias(text, self.le_unitID.text())
        self.slotUnitDictInit()



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



    '''
        功能：
            设置单元时的初始化tableWidget，显示整个单位表
    '''

    def _initUnitTableWidget(self):
        header = ['单位编号', '单位名称', '上级单位编号', '单位代号']
        self.tb_result.setColumnCount(len(header))
        self.tb_result.setHorizontalHeaderLabels(header)
        self.resultList = []
        selectSuccess = selectAllDataAboutUnit(self.resultList)
        if selectSuccess != True:
            getMessageBox("初始化", "初始化单位表失败", True, False)
            return

        self.tb_result.setRowCount(len(self.resultList))
        for i, data in enumerate(self.resultList):
            item = QTableWidgetItem(data[0])
            self.tb_result.setItem(i, 0, item)
            item = QTableWidgetItem(data[1])
            self.tb_result.setItem(i, 1, item)
            item = QTableWidgetItem(data[2])
            self.tb_result.setItem(i, 2, item)
            item = QTableWidgetItem(data[3])
            self.tb_result.setItem(i, 3, item)

        # print(result)   #测试查找到的数据

    def slotSelectUnit(self):
        selectUnit(self, self.le_first, self.first_treeWidget_dict, self.tw_first)

    '''
            功能：
                当选中tablewidget某行时，显示对应的lineedit
        '''

    def slotClickedRow(self):
        currentRow = self.tb_result.currentRow()
        if currentRow < 0:
            return
        self.le_unitID.setText(self.tb_result.item(currentRow, 0).text())
        self.le_unitName.setText(self.tb_result.item(currentRow, 1).text())
        for i, unitID in enumerate(self.unitIDList):
            if self.tb_result.item(currentRow, 2).text() == unitID:
                self.cb_unitUper.setCurrentIndex(i)
                break
        self.le_unitAlias.setText(self.tb_result.item(currentRow, 3).text())

    '''
            功能：
                添加目录
        '''

    def slotAddDict(self):
        # 单位目录
        if self.le_unitID.text() == "" or self.le_unitName.text() == "":
            getMessageBox('新增失败', '单位ID或单位名字为空，拒绝增加，请重新填写', True, False)
        else:
            Unit_ID = self.le_unitID.text()
            Unit_Name = self.le_unitName.text()
            Unit_Uper = self.cb_unitUper.currentText()
            Unit_Alias = self.le_unitAlias.text()
            haveUnitID = selectUnitInfoByUnitID(Unit_ID)
            if haveUnitID:
                getMessageBox('新增失败', '单位ID已存在, 请重新填写', True, False)
                return

            addSuccess = addDataIntoUnit(Unit_ID, Unit_Name, Unit_Uper, Unit_Alias, "否")
            if addSuccess == True:
                getMessageBox('新增', '新增成功', True, False)
            else:
                getMessageBox('新增', str(addSuccess) + '，新增失败', True, False)
                return
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
        if (self.tb_result.item(self.tb_result.currentRow(),
                                0).text() != self.le_unitID.text()) or self.le_unitName.text() == "":
            getMessageBox('修改失败', '单位ID不能修改或单位名字为空，拒绝修改，请重新填写', True, False)
            self.le_unitID.setText(self.tb_result.item(self.tb_result.currentRow(), 0).text())
            return
        else:
            Unit_ID = self.le_unitID.text()
            Unit_Name = self.le_unitName.text()
            Unit_Uper = self.cb_unitUper.currentText()
            Unit_Alias = self.le_unitAlias.text()

            updateSuccess = updateDataIntoUnit(Unit_ID, Unit_Name, Unit_Uper, Unit_Alias)
            if updateSuccess == True:
                getMessageBox('修改', '修改成功', True, False)
                self.slotUnitDictInit()
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
        reply = getMessageBox('删除', '是否将下级单位以及所涉及的其他表关于该单位的信息一起删除？', True, True)
        if reply == QMessageBox.Ok:
            delSuccess = delDataInUnit(self.le_unitID.text())
            if delSuccess == True:
                getMessageBox('删除', '删除成功', True, False)
                self.slotUnitDictInit()
            else:
                getMessageBox('删除', str(delSuccess) + ',删除失败', True, False)
                return
        else:
            getMessageBox('删除', '删除失败', True, False)
            return

    def slotInputDataByExcel(self):
        self.setDisabled(True)
        self.showInputResult.setDisabled(False)

        filename, _ = QFileDialog.getOpenFileName(self, "选中文件", '', "Excel Files (*.xls);;Excel Files (*.xlsx)")
        if filename == '':
            self.setDisabled(False)
            return
        try:
            workBook = xlrd.open_workbook(filename)
            self.workSheet = workBook.sheet_by_index(0)
            self.inputUnitInfoList = []
            title = ['单位编号', '单位名称', '上级单位编号', '单位代号']
            cols = self.workSheet.ncols
            if cols != len(title):
                raise Exception("文件内容不匹配！")
            for i in range(0, cols):
                context = self.workSheet.cell(0, i).value
                if(title[i] != context):
                    raise Exception("文件内容不匹配！")
            for r in range(1, self.workSheet.nrows):
                Unit_Name = (self.workSheet.cell(r, 1).value).strip()
                Unit_Alias = self.workSheet.cell(r, 3).value
                Unit_ID = ''
                try:
                    Unit_ID = str(int(self.workSheet.cell(r, 0).value))
                    Unit_Uper = str(int(self.workSheet.cell(r, 2).value))
                except:
                    if Unit_Name == '火箭军' and Unit_ID == '1':
                        pass
                    else:
                        getMessageBox("读取失败", "读取第%d行数据失败，请检查单位或上级单位编号是否正确！"%(r), True, False)
                    continue
                unitInfo = []
                unitInfo.append(Unit_ID)
                unitInfo.append(Unit_Name)
                unitInfo.append(Unit_Uper)
                unitInfo.append(Unit_Alias)
                self.inputUnitInfoList.append(unitInfo)
            self.showInputResult.setWindowTitle("导入Excel数据到数据库单位表中")
            self.showInputResult.tw_result.setColumnCount(len(title))
            self.showInputResult.tw_result.setHorizontalHeaderLabels(title)
            self.showInputResult.tw_result.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.showInputResult.tw_result.setRowCount(len(self.inputUnitInfoList))
            self.showInputResult.tw_result.verticalHeader().setVisible(False)
            for r, list_item in enumerate(self.inputUnitInfoList):
                item = QTableWidgetItem(list_item[0])
                self.showInputResult.tw_result.setItem(r, 0, item)
                item = QTableWidgetItem(list_item[1])
                self.showInputResult.tw_result.setItem(r, 1, item)
                item = QTableWidgetItem(list_item[2])
                self.showInputResult.tw_result.setItem(r, 2, item)
                item = QTableWidgetItem(list_item[3])
                self.showInputResult.tw_result.setItem(r, 3, item)
            self.showInputResult.show()

        except BaseException as e:
            print(e)
            getMessageBox("导入失败", "请检查文件内容是否正确！", True, False)
            self.setDisabled(False)




    '''
        功能：
            导出到excel表格中
    '''
    def slotOutputDataIntoExcel(self):
        directoryPath = QFileDialog.getExistingDirectory(self, "请选择导出文件夹",  "c:/")
        if len(directoryPath)  > 0:
            if len(self.resultList) > 0:
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
                workSheet.write(0, 0, '单位编号', titileStyle)
                workSheet.write(0, 1, '单位名称', titileStyle)
                workSheet.write(0, 2, '上级单位编号', titileStyle)
                workSheet.write(0, 3, '单位代号', titileStyle)
                for i,item in enumerate(self.resultList):
                    workSheet.write(i + 1,0,item[0],contentStyle)
                    workSheet.write(i + 1, 1, item[1],contentStyle)
                    workSheet.write(i + 1, 2, item[2],contentStyle)
                    workSheet.write(i + 1, 3, item[3],contentStyle)
                try:
                    workBook.save("%s/单位目录表.xls"%directoryPath)
                    getMessageBox("导出成功", "导出成功！", True, False)
                    import win32api
                    win32api.ShellExecute(0, 'open', '%s/单位目录表.xls'%directoryPath, '', '', 1)

                    return
                except Exception as e:
                    getMessageBox("导出失败", "导出表格被占用，请关闭正在使用的Execl！", True, False)
                    return
            else:
                getMessageBox("未选中任何数据", "导出失败！", True, False)
                return

    def slotCancelInputIntoMysql(self):
        self.showInputResult.hide()
        self.setDisabled(False)


    def slotInputIntoMysql(self):
        print(self.inputUnitInfoList)
        inputSuccess = inputIntoUnitFromExcel(self.inputUnitInfoList)
        if inputSuccess != True:
            for error in inputSuccess:
                getMessageBox("导入", error, True, False)
                break
        self.slotUnitDictInit()
        self.setDisabled(False)
        self.showInputResult.hide()

