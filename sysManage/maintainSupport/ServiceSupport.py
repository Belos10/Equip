import pickle
import sys

from PyQt5.QtCore import Qt, QStringListModel, QDateTime
from PyQt5.QtWidgets import QApplication, QWidget, QHeaderView, QTableWidgetItem, QComboBox, \
    QMessageBox, QFileDialog, QAbstractItemView

from database.serviceSupportSql import *
from sysManage.component import getMessageBox, getIntInputDialog
from sysManage.showInputResult import showInputResult
from sysManage.userInfo import get_value
from widgets.serviceSupport.ServiceSupportNewUI import ServiceSupportNewUI


class ServiceSupport(QWidget, ServiceSupportNewUI):
    def __init__(self, parent=None):
        super(ServiceSupport, self).__init__(parent)
        self.setupUi(self)
        self.selectedYear = ''
        self.maintanceType = '全选'
        self.inputList = []
        self.showInputResult = showInputResult(self)
        self.showInputResult.hide()
        self.signalConnection()
        self.init()
        self.maintanceTypeEnem = {
            0 : '装备大修',
            1 : '装备中修',
            2 : '维修器材购置',
            3 : '修理能力建设'
        }
        self.maintanceTypeReverseEnem = {
            '装备大修' : 0,
            '装备中修' : 1,
            '维修器材购置' : 2,
            '修理能力建设' : 3
        }
        self.technologyStateEnem = {
            0 : '不涉及',
            1 : '是',
            2 : '否'
        }
        self.technologyStateReverseEnem = {
            '不涉及' : 0,
            '是' : 1,
            '否' : 2
        }
        self.contractEnem = {
            0 : '不涉及',
            1 : '是',
            2 : '否'
        }
        self.contractReverseEnem = {
            '不涉及' : 0,
            '是' : 1,
            '否' : 2
        }
        self.payingEnem = {
            0: '不涉及',
            1: '是',
            2: '否'
        }
        self.payingReverseEnem = {
            '不涉及' : 0,
            '是' : 1,
            '否' : 2
        }

    # 信号和槽连接
    def signalConnection(self):
        self.pb_select.clicked.connect(self.slotSelect)
        self.tb_add.clicked.connect(self.slotAdd)
        self.tb_del.clicked.connect(self.slotDelete)
        self.lv_year.clicked.connect(self.displayDataByYear)
        self.pb_addYear.clicked.connect(self.soltAddContractYear)
        self.tb_outputToExcel.clicked.connect(self.slotOutputToExcel)
        self.tw_result.itemChanged.connect(self.slotAlterAndSava)
        
        self.tb_input.clicked.connect(self.slotInputData)
        self.pb_output.clicked.connect(self.slotOutputData)
        self.showInputResult.pb_confirm.clicked.connect(self.slotInputIntoDatabase)
        self.showInputResult.pb_cancel.clicked.connect(self.slotCancelInputIntoDatabase)



    def initUserInfo(self):
        self.userInfo = get_value("totleUserInfo")

    # 信号和槽断开
    def slotDisconnect(self):
        pass

    # 定义初始化函数
    def init(self):
        self.initUserInfo()
        if self.userInfo:
            from database.strengthDisturbSql import selectUnitInfoByUnitID
            self.startInfo = selectUnitInfoByUnitID(self.userInfo[0][4])

        self.pb_output.setDisabled(True)
        self.pb_select.setDisabled(True)
        self.tb_add.setDisabled(True)
        self.tb_del.setDisabled(True)
        self.tb_outputToExcel.setDisabled(True)
        self.tw_result.setDisabled(True)
        self.tb_input.setDisabled(True)
        #初始化年份列表
        self.initYearList()
        self.cb_selectedType.clear()
        self.cb_selectedType.addItems(['全选', '装备大修', '装备中修', '维修器材购置', '修理能力建设'])
                                            #    0            1           2             3
        pass

    '''
                功能：
                    初始化年份列表
    '''

    def initYearList(self):
        self.yearList = []
        self.yearList = getYearsFromServiceSupportYear()
        listModel = QStringListModel()
        listModel.setStringList(self.yearList)
        self.lv_year.setModel(listModel)
        self.lv_year.setEditTriggers(QAbstractItemView.NoEditTriggers)


    '''
        新增年份
    '''
    def soltAddContractYear(self):
        year = 0
        ok, year = getIntInputDialog("新增年份", "年份:", 0, 100000, 1, True, True)
        if ok:
            if isHaveServiceSupportYear(str(year)):
                getMessageBox("新增", "该年份已经存在，拒绝添加！", True, False)
                return
            else:
                insertSuccess = addServiceSupportYear(year)
                if insertSuccess == True:
                    getMessageBox("新增", "新增成功！", True, False)
                else:
                    getMessageBox("新增", "新增失败！", True, False)
                self.init()



    def displayDataByYear(self,item):
        if (len(self.yearList) != 0):
            self.selectedYear = self.yearList[item.row()]
            if len(self.selectedYear) != 0:
                self.pb_select.setDisabled(False)
                self.tb_add.setDisabled(False)
                self.tb_del.setDisabled(False)
                self.tb_outputToExcel.setDisabled(False)
                self.tw_result.setDisabled(False)
                self.pb_output.setDisabled(False)
                self.tb_input.setDisabled(False)
            self.displayData()


    '''
        功能：
            根据下拉列表框以及文本框的内容，筛选数据。
    '''

    def slotSelect(self):
        self.maintanceType = self.cb_selectedType.currentText()
        self.displayData()

    '''
        功能：
            将列表数据展示在表中
    '''

    def displayData(self):
        self.tw_result.itemChanged.disconnect(self.slotAlterAndSava)
        self.result = getResult(self.selectedYear, self.maintanceType)
        self.tw_result.clear()
        self.tw_result.setColumnCount(14)
        self.currentLastRow = 0
        dataList = self.result
        if dataList is None or len(dataList) == 0:
            self.tw_result.setRowCount(2)
            self.initTableHeader()
        else:
            self.tw_result.setRowCount(2 + len(dataList))
            self.initTableHeader()
            for i in range(len(dataList)):
                item = QTableWidgetItem(str(i + 1))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.tw_result.setItem(2 + i, 0, item)

                item = QTableWidgetItem(self.maintanceTypeEnem[dataList[i][1]])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.tw_result.setItem(2 + i, 1, item)

                item = QTableWidgetItem(dataList[i][2])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(2 + i, 2, item)

                item = QTableWidgetItem(dataList[i][3])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(2 + i, 3, item)

                item = QTableWidgetItem(str(dataList[i][4]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(2 + i, 4, item)

                item = QTableWidgetItem(str(dataList[i][5]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(2 + i, 5, item)

                item = QTableWidgetItem(str(dataList[i][6]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(2 + i, 6, item)

                item = QTableWidgetItem(dataList[i][7])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(2 + i, 7, item)

                item = QTableWidgetItem(dataList[i][8])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(2 + i, 8, item)

                comboBox = QComboBox()
                comboBoxItem = []
                if dataList[i][1] == 0 or dataList[i][1] == 1:
                    comboBoxItem = ['不涉及']
                else:

                    if dataList[i][9] == 1:
                        comboBoxItem = ['是', '否']
                    else:
                        comboBoxItem = ['否', '是']
                comboBox.addItems(comboBoxItem)
                comboBox.setEditable(False)
                comboBox.activated.connect(self.slotAlterAndSava)
                self.tw_result.setCellWidget(2 + i, 9, comboBox)

                comboBox = QComboBox()
                comboBoxItem = []
                if dataList[i][10] == 0:
                    comboBoxItem = ['不涉及']
                else:

                    maintanceContractNos = getMaintanceContractNos()
                    print('maintanceContractNos')
                    print(maintanceContractNos)
                    if dataList[i][10] == 1:
                        #关联数据
                        comboBoxItem.append(dataList[i][11])
                        comboBoxItem.append('否')
                        for j in range(len(maintanceContractNos)):
                            if maintanceContractNos[j][0] == dataList[i][11]:
                                continue
                            else:
                                comboBoxItem.append(maintanceContractNos[j][0])
                    else:
                        comboBoxItem.append('否')
                        for j in range(len(maintanceContractNos)):
                            comboBoxItem.append(maintanceContractNos[j][0])
                print(comboBoxItem)
                comboBox.addItems(comboBoxItem)
                comboBox.setEditable(False)
                comboBox.activated.connect(self.slotAlterAndSava)
                self.tw_result.setCellWidget(2 + i, 10, comboBox)

                comboBox = QComboBox()
                comboBoxItem = []
                if dataList[i][12] == 0:
                    comboBoxItem = ['不涉及']
                else:

                    if dataList[i][12] == 1:
                        comboBoxItem = ['是', '否']
                    else:
                        comboBoxItem = ['否', '是']
                comboBox.addItems(comboBoxItem)
                comboBox.setEditable(False)
                comboBox.activated.connect(self.slotAlterAndSava)
                self.tw_result.setCellWidget(2 + i, 11, comboBox)

                item = QTableWidgetItem(dataList[i][13])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.tw_result.setItem(2 + i, 12, item)

                item = QTableWidgetItem(dataList[i][14])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(2 + i, 13, item)

        self.tw_result.itemChanged.connect(self.slotAlterAndSava)
        

    '''
        功能：
            画表头,行数至少有2行
    '''

    def initTableHeader(self):
        self.tw_result.verticalHeader().setVisible(False)
        self.tw_result.horizontalHeader().setVisible(False)
        # self.tw_result.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tw_result.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tw_result.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tw_result.resizeColumnsToContents()
        self.tw_result.resizeRowsToContents()

        # 绘制表头
        item = QTableWidgetItem("序号")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(0, 0, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setSpan(0, 0, 2, 1)

        item = QTableWidgetItem("项目类型")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(0, 1, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setSpan(0, 1, 2, 1)

        item = QTableWidgetItem("项目名称")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(0, 2, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setSpan(0, 2, 2, 1)

        item = QTableWidgetItem("计量单位")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(0, 3, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setSpan(0, 3, 2, 1)

        item = QTableWidgetItem("审核")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(0, 4, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setSpan(0, 4, 1, 3)

        item = QTableWidgetItem("单价")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 4, item)
        item.setFlags(Qt.ItemIsEnabled)

        item = QTableWidgetItem("数量")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 5, item)
        item.setFlags(Qt.ItemIsEnabled)

        item = QTableWidgetItem("金额")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 6, item)
        item.setFlags(Qt.ItemIsEnabled)

        item = QTableWidgetItem("单位")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(0, 7, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setSpan(0, 7, 1, 2)

        item = QTableWidgetItem("分配（送修）")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 7, item)
        item.setFlags(Qt.ItemIsEnabled)

        item = QTableWidgetItem("供货（承修）")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 8, item)
        item.setFlags(Qt.ItemIsEnabled)

        item = QTableWidgetItem("计价挂账进度")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(0, 9, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setSpan(0, 9, 1, 3)

        item = QTableWidgetItem("确定技术状态")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 9, item)
        item.setFlags(Qt.ItemIsEnabled)

        item = QTableWidgetItem("签订合同")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 10, item)
        item.setFlags(Qt.ItemIsEnabled)

        item = QTableWidgetItem("支付")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 11, item)
        item.setFlags(Qt.ItemIsEnabled)

        item = QTableWidgetItem("年份/时间")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(0, 12, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setSpan(0, 12, 2, 1)

        item = QTableWidgetItem("备注")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(0, 13, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setSpan(0, 13, 2, 1)



    '''
        功能：
            新增一行的数据
    '''
    def slotAlterAndSava(self, index):
        print('修改保存')
        selectRow = self.tw_result.selectedItems()
        if len(selectRow) != 0:
            currentRow = selectRow[0].row()
            currentColumn = selectRow[0].column()
            if (currentColumn == 4 or currentColumn == 5 and currentRow >= 2):
                item0 = self.tw_result.item(currentRow, 4)
                item1 = self.tw_result.item(currentRow, 5)
                if (item1 != None and item0 != None):
                    if (len(item0.text()) > 0 and len(item1.text()) > 0):
                        self.tw_result.itemChanged.disconnect(self.slotAlterAndSava)
                        count = 0
                        unit = 0
                        try:
                             count = int(item1.text())
                        except ValueError:
                            getMessageBox("注意", "请输入整数！", True, False)
                            item1.setText('')
                        try:
                            unit = float(item0.text())
                        except:
                            getMessageBox("注意", "请输入正确的数字！", True, False)
                            item0.setText('')
                        amount = round(count * unit, 4)
                        item = self.tw_result.item(currentRow,6)
                        if(item != None):
                            item.setText(str(amount))
                            item.setFlags(Qt.ItemIsEnabled)
                        else:
                            item = QTableWidgetItem(str(amount))
                            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                            item.setFlags(Qt.ItemIsEnabled)
                            self.tw_result.setItem(currentRow, 6, item)
                        self.tw_result.itemChanged.connect(self.slotAlterAndSava)
                        

            if currentRow == self.currentLastRow:
                self.savaRowData(currentRow)
            else:
                self.alterRowData(currentRow)
        else:

            currentRow = self.tw_result.currentIndex().row()
            if currentRow == self.currentLastRow:
                self.savaRowData(currentRow)
            else:
                self.alterRowData(currentRow)

    def savaRowData(self, row):
        # print('保存一行')
        rowData = []
        for i in range(1, self.tw_result.columnCount()):
            if i == 1 or i == 9 or i == 10 or i == 11:
                item = self.tw_result.cellWidget(row, i)
                if item != None:
                    text = item.currentText()
                    if len(text) > 0:
                        if i == 1:
                            rowData.append(self.maintanceTypeReverseEnem[text])
                        elif i == 9:
                            rowData.append(self.technologyStateReverseEnem[text])
                        elif i == 10:
                            if text == '否' or text == '不涉及':
                                rowData.append(self.contractReverseEnem[text])
                                rowData.append('null')
                            else:
                                rowData.append(self.payingReverseEnem['是'])
                                rowData.append(text)
                        elif i == 11:
                                rowData.append(self.payingReverseEnem[text])
            else:
                item = self.tw_result.item(row, i)
                if (item != None):
                    if (len(item.text()) > 0):
                        rowData.append(item.text())
                else:
                    break
        if len(rowData) == self.tw_result.columnCount():
            if(insertOneDataInToServiceSuppot(rowData) == True):
                getMessageBox("注意", "插入成功！", True, False)
            else:
                getMessageBox("警告", "插入失败！", True, False)
            self.displayData()

    def alterRowData(self, row):
        # print("修改一行数据")
        rowData = []
        rowData.append(self.result[row - 2][0])
        for i in range(1, self.tw_result.columnCount()):
            if i == 9 or i == 10 or i == 11:
                item = self.tw_result.cellWidget(row, i)
                if item != None:
                    text = item.currentText()
                    if i == 9:
                        rowData.append(self.technologyStateReverseEnem[text])
                    elif i == 10:
                        if text == '否' or text == '不涉及':
                            rowData.append(self.contractReverseEnem[text])
                            rowData.append('null')
                        else:
                            rowData.append(self.payingReverseEnem['是'])
                            rowData.append(text)
                    elif i == 11:
                        rowData.append(self.payingReverseEnem[text])

                else:
                    break
            else:
                item = self.tw_result.item(row, i)
                if (item != None):
                    text = item.text()
                    if (len(text) > 0):
                        if i == 1:
                            rowData.append(self.maintanceTypeReverseEnem[text])
                        else:
                            rowData.append(text)
                    else:
                        break
                else:
                    break
        if len(rowData) == self.tw_result.columnCount() + 1:
            if (updataOneDataToServiceSuppot(rowData) == True):
                getMessageBox("注意", "修改成功！", True, False)
            else:
                getMessageBox("警告", "修改失败！", True, False)
            self.displayData()



    '''
        功能：
            新增按钮槽函数
    '''

    def slotAdd(self):
        if self.tw_result.rowCount() <= 2 + len(self.result):
            self.tw_result.itemChanged.disconnect(self.slotAlterAndSava)
            rowCount = self.tw_result.rowCount()
            self.currentLastRow = rowCount
            self.tw_result.insertRow(rowCount)

            if (rowCount + 1 == 3):
                item = QTableWidgetItem('1')
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.tw_result.setItem(2, 0, item)
            else:
                item = QTableWidgetItem(str(rowCount - 1 ))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.tw_result.setItem(rowCount, 0, item)

            combox = QComboBox()
            comboxItems = ['装备大修', '装备中修', '维修器材购置', '修理能力建设']
            combox.addItems(comboxItems)
            combox.setEditable(False)
            combox.activated.connect(self.changeCombox)
            self.tw_result.setCellWidget(rowCount, 1, combox)

            combox = QComboBox()
            comboxItems = ['不涉及']
            combox.addItems(comboxItems)
            combox.setEditable(False)
            combox.activated.connect(self.slotAlterAndSava)
            self.tw_result.setCellWidget(rowCount, 9, combox)

            combox = QComboBox()
            comboxItems = ['不涉及']
            combox.addItems(comboxItems)
            combox.setEditable(False)
            combox.activated.connect(self.slotAlterAndSava)
            self.tw_result.setCellWidget(rowCount, 10, combox)

            combox = QComboBox()
            comboxItems = ['不涉及']
            combox.addItems(comboxItems)
            combox.setEditable(False)
            self.tw_result.setCellWidget(rowCount, 11, combox)

            item = QTableWidgetItem(self.selectedYear)
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(rowCount, 12, item)

            self.tw_result.itemChanged.connect(self.slotAlterAndSava)
            

        else:
            getMessageBox("注意", "请先将数据补充完整！", True, False)

    def changeCombox(self, index):
        print('index')
        print(index)
        row = self.tw_result.rowCount()
        item = self.tw_result.cellWidget(row -1,1)
        if item != None:
            if index == 0 or index == 1:
                pass
            else:
                combox = QComboBox()
                comboxItems = ['是', '否']
                combox.addItems(comboxItems)
                combox.setEditable(False)
                self.tw_result.setCellWidget(row - 1, 9, combox)

                combox = QComboBox()
                comboxItems = ['否']
                maintanceContractNos = getMaintanceContractNos()
                print('maintanceContractNos')
                print(maintanceContractNos)
                for i in range(len(maintanceContractNos)):
                    comboxItems.append(maintanceContractNos[i][0])

                print(comboxItems)
                combox.addItems(comboxItems)
                combox.setEditable(False)
                self.tw_result.setCellWidget(row - 1, 10, combox)
                combox = QComboBox()
                comboxItems = ['是', '否']
                combox.addItems(comboxItems)
                combox.setEditable(False)
                self.tw_result.setCellWidget(row - 1, 11, combox)


    def slotDelete(self):

        rowCount = self.tw_result.currentRow()
        resultCount = len(self.result)
        if rowCount < 2:
            getMessageBox("注意", "请选中有效单元格！", True, False)
        elif rowCount >= 2 and rowCount < 2 + resultCount:
            reply = getMessageBox('警告', '是否删除该行数据？', True, True)
            if reply == QMessageBox.Ok:
                deleteDataByServiceSuppotIdAndYear(self.result[rowCount - 2][0],self.selectedYear)
                self.tw_result.removeRow(rowCount)
            else:
                return
        else:
            self.tw_result.removeRow(rowCount)


    #导出至Excel
    def slotOutputToExcel(self):
        if len(self.result) < 1:
            getMessageBox('警告', '未选中任何数据，无法导出', True, False)
            return
        reply = getMessageBox('修改导出Excel', '是否保存修改并导出Excel？', True, True)
        if reply == QMessageBox.Cancel:
            self.displayData()
            return
        self.displayData()
        directoryPath = QFileDialog.getExistingDirectory(self, "请选择导出文件夹", "c:/")
        if len(directoryPath) > 0:
            import xlwt
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
            for i in range(13):
                workSheet.col(i).width = 5000
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

            #画表头
            workSheet.write_merge(0, 0, 0, 13, "核化装备维修保障计划及预算明细表", titileStyle)
            workSheet.write_merge(1, 2, 0, 0, '序号', titileStyle)
            workSheet.write_merge(1, 2, 1, 1, '项目类型', titileStyle)
            workSheet.write_merge(1, 2, 2, 2, '项目名称', titileStyle)
            workSheet.write_merge(1, 2, 3, 3, '计量单位', titileStyle)
            workSheet.write_merge(1, 1, 4, 6, '审核', titileStyle)
            workSheet.write(2, 4, "单价", titileStyle)
            workSheet.write(2, 5, "数量", titileStyle)
            workSheet.write(2, 6, "金额", titileStyle)
            workSheet.write_merge(1, 1, 7, 8, '单位', titileStyle)
            workSheet.write(2, 7, "分配（送修）", titileStyle)
            workSheet.write(2, 8, "供货（承修）", titileStyle)
            workSheet.write_merge(1, 1, 9, 11, '计价挂账进度', titileStyle)
            workSheet.write(2, 9, "确定技术状态", titileStyle)
            workSheet.write(2, 10, "签订合同", titileStyle)
            workSheet.write(2, 11, "支付", titileStyle)
            workSheet.write_merge(1, 2, 12, 12, '年份/时间', titileStyle)
            workSheet.write_merge(1, 2, 13, 13, '备注', titileStyle)


            #填表数据
            dataList = self.result
            if len(dataList) > 0:
                for i in range(len(self.result)):
                    workSheet.write(3 + i, 0, str(i + 1), contentStyle)
                    print('self.result[i][1]')
                    print(self.result[i][1])
                    workSheet.write(3 + i, 1, self.maintanceTypeEnem[self.result[i][1]], contentStyle)
                    workSheet.write(3 + i, 2, self.result[i][2], contentStyle)
                    workSheet.write(3 + i, 3, self.result[i][3], contentStyle)
                    workSheet.write(3 + i, 4, str(self.result[i][4]), contentStyle)
                    workSheet.write(3 + i, 5, str(self.result[i][5]), contentStyle)
                    workSheet.write(3 + i, 6, str(self.result[i][6]), contentStyle)
                    workSheet.write(3 + i, 7, self.result[i][7], contentStyle)
                    workSheet.write(3 + i, 8, self.result[i][8], contentStyle)
                    workSheet.write(3 + i, 9, self.technologyStateEnem[self.result[i][9]], contentStyle)
                    if self.result[i][10] == 1:
                        workSheet.write(3 + i, 10, self.result[i][11], contentStyle)
                    else:
                        workSheet.write(3 + i, 10, self.contractEnem[self.result[i][10]], contentStyle)
                    workSheet.write(3 + i, 11, self.payingEnem[self.result[i][12]], contentStyle)
                    workSheet.write(3 + i, 12, self.result[i][13], contentStyle)
                    workSheet.write(3 + i, 13, self.result[i][14], contentStyle)

            try:
                pathName = "%s/%s年订购计划--合同.xls" % (directoryPath,self.selectedYear)
                workBook.save(pathName)
                import win32api
                win32api.ShellExecute(0, 'open', pathName, '', '', 1)
                getMessageBox("导出成功", "导出成功！", True, False)
                return
            except Exception as e:
                getMessageBox("导出失败", "导出表格被占用，请关闭正在使用的Execl！", True, False)
                return

        pass

        # 导出数据包

    def slotOutputData(self):
        if len(self.result) < 1:
            getMessageBox('警告', '未选中任何数据，无法导出', True, False)
            return
        reply = getMessageBox('导出数据包', '是否保存修改并导出数据包？', True, True)
        if reply == QMessageBox.Cancel:
            self.displayData()
            return
        directoryPath = QFileDialog.getExistingDirectory(self, "请选择导出文件夹", "c:/")
        if len(directoryPath) > 0:
            # 填表数据
            dataList = ['维修计划']
            for _,element in enumerate(self.result):
                rowData = []
                contractInof = []
                for i in range(len(element)):
                    if i == 0 or i == 11:
                        continue
                    elif i == 10:
                        rowData.append(element[10])
                        rowData.append(element[11])
                        if element[10] == 1:
                            contractInof = getMaintanceContractInfo(element[11])
                            contractInof = contractInof[1:]
                    else:
                        rowData.append(element[i])
                rowData.append(contractInof)
                dataList.append(rowData.copy())
            if len(dataList) == 1:
                return
            else:
                date = QDateTime.currentDateTime()
                installData = date.toString("yyyy年MM月dd日hh时mm分ss秒")  # hh:mm:ss
                pathName = "%s/%s%s年维修计划.nms" % (
                directoryPath, installData, dataList[1][-3])
                with open(pathName, "wb") as file:
                    pickle.dump(dataList, file)
                getMessageBox("导出数据成功！", "导出成功！", True, False)
            pass
        else:
            getMessageBox("导出数据失败！", "请选择正确的文件夹！", True, False)
        pass

        # 导入数据包

    def slotInputData(self):
        self.inputList = []
        filename, _ = QFileDialog.getOpenFileName(self, "选中文件", '', "Excel Files (*.nms);;Excel Files (*.nms)")
        if len(filename) < 2:
            return
        try:
            with open(filename, "rb") as file:
                self.inputList = pickle.load(file)
                if self.inputList[0] != "维修计划":
                    raise Exception("数据格式错误！")
        except Exception as e:
            print(e)
            getMessageBox("加载文件失败！", "请检查文件格式及内容格式！", True, False)
            return
        headerlist = ['项目类型', '项目名称', '计量单位', '单价', '数量', '金额', '分配（送修）', '供货（承修）', '技术状态', '签订合同', '支付', '年份', '备注' ]
        self.showInputResult.setWindowTitle("导入数据")
        self.showInputResult.show()
        # QTableWidget设置整行选中
        self.showInputResult.tw_result.setColumnCount(len(headerlist))
        self.showInputResult.tw_result.setHorizontalHeaderLabels(headerlist)
        self.showInputResult.tw_result.setRowCount(len(self.inputList) - 1)


        for i, LineInfo in enumerate(self.inputList):
            print(LineInfo)
            if i == 0:
                continue
            i = i - 1
            #[2, '2', '2', 2.0, 3, 6.0, '2', '3', 1, 1, '23', 1, '2001', '2',('2021', '23', '2', '2', '2', 2.0, 2, 2.0, 2, '2')]

            item = QTableWidgetItem(self.maintanceTypeEnem[LineInfo[0]])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 0, item)
            item = QTableWidgetItem(LineInfo[1])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 1, item)
            item = QTableWidgetItem(LineInfo[2])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 2, item)

            item = QTableWidgetItem(str(LineInfo[3]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 3, item)
            item = QTableWidgetItem(str(LineInfo[4]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 4, item)
            item = QTableWidgetItem(str(LineInfo[5]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 5, item)
            item = QTableWidgetItem(LineInfo[6])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 6, item)
            item = QTableWidgetItem(LineInfo[7])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 7, item)
            item = QTableWidgetItem(self.technologyStateEnem[LineInfo[8]])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 8, item)

            if LineInfo[9] != 1:
                item = QTableWidgetItem(self.contractEnem[LineInfo[9]])
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.showInputResult.tw_result.setItem(i, 9, item)
            else:
                item = QTableWidgetItem(LineInfo[10])
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.showInputResult.tw_result.setItem(i, 9, item)

            item = QTableWidgetItem(self.payingEnem[LineInfo[11]])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 10, item)


            item = QTableWidgetItem(LineInfo[12])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 11, item)

            item = QTableWidgetItem(LineInfo[13])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 12, item)

    def slotCancelInputIntoDatabase(self):
        self.showInputResult.hide()
        self.setDisabled(False)

    def slotInputIntoDatabase(self):
        for i, lineInfo in enumerate(self.inputList):
            if i == 0:
                continue
            try:
                if inputOneDataIntoServiceSuppot(lineInfo):
                    pass
            except Exception as e:
                print(e)
                getMessageBox("导入失败", "导入第%d数据失败！" % (i), True, False)

        self.showInputResult.hide()
        self.setDisabled(False)
        self.displayData()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = OrderManagement()
    widget.show()
    sys.exit(app.exec_())
