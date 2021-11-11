import sys
from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
from PyQt5.QtGui import QColor, QBrush,QFont
from conda_verify import const

from database.serviceSupportSql import *
from widgets.serviceSupport.serviceSupportUI import Widget_ServiceSupport
from sysManage.userInfo import get_value

'''
    维修保障计划
'''
class serviceSupport(QDialog, Widget_ServiceSupport):
    def __init__(self, parent=None):
        super(serviceSupport,self).__init__(parent)
        self.setupUi(self)
        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}
        self.currentUnitDisturbPlanNum = {}
        self.unitDisturbPlanList = {}
        self.unitFlag = 0
        self.signalConnect()
        self.datadict = {}
        self.bl = 0
        self.initAll()



    def initAll(self):
        self.txt_serviceSupportYear.clear()
        self.serviceSupportResult.clear()
        self._initYearWidget_()


    '''
        功能：信号与槽连接
    '''
    def signalConnect(self):
        # 点击选择年份后刷新页面 初始化
        self.lw_yearChoose.itemClicked.connect(self.slotClickedInqury)
        self.lw_yearChoose.itemClicked.connect(self.setServiceSupportTitle)
        self.lw_yearChoose.itemClicked.connect(self.showYearContentOfServiceSupport)
        self.add_data.clicked.connect(self.slotAdd)
        self.delete_data.clicked.connect(self.slotDelete)
        # self.save_data.clicked.connect(self.saveContentOfserviceSupport)
        self.showAllYearData.clicked.connect(self.showAllYearServiceSupportData)
        # self.serviceSupportResult.itemChanged.connect(self.updateChangeDataOfServiceSupport)
        self.serviceSupportResult.itemChanged.connect(self.slotAlterAndSava)
        self.selectButton.clicked.connect(self.selectDataAboutProjectType)
        self.selectButton.clicked.connect(self.setTypeServiceSupportTitle)
        self.pb_outputToExcel.clicked.connect(self.slotOutputToExcel)




    '''
        功能：信号与槽连接的断开
    '''
    def signalDisconnectSlot(self):
        # 点击选择年份后刷新页面 初始化
        self.lw_yearChoose.itemClicked.disconnect(self.slotClickedInqury)
        self.lw_yearChoose.itemClicked.disconnect(self.setServiceSupportTitle)
        self.lw_yearChoose.itemClicked.disconnect(self.showYearContentOfServiceSupport)
        self.add_data.clicked.disconnect(self.slotAdd)
        self.delete_data.clicked.disconnect(self.slotDelete)
        # self.save_data.clicked.disconnect(self.saveContentOfserviceSupport)
        self.showAllYearData.clicked.disconnect(self.showAllYearServiceSupportData)
        # self.serviceSupportResult.itemChanged.disconnect(self.updateChangeDataOfServiceSupport)
        self.serviceSupportResult.itemChanged.disconnect(self.slotAlterAndSava)
        self.selectButton.clicked.disconnect(self.selectDataAboutProjectType)
        self.selectButton.clicked.disconnect(self.setTypeServiceSupportTitle)
        self.pb_outputToExcel.clicked.disconnect(self.slotOutputToExcel)

        # # 新增年份
        # self.tb_add.clicked.disconnect(self.slotAddNewYear)
        # # 删除年份
        # self.tb_del.clicked.disconnect(self.slotDelYear)


    def slotClickedInqury(self):
        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}
        self.currentYear = self.lw_yearChoose.currentItem().text()



    '''
        功能：点击显示所有年份的维修保障计划数据
    '''
    def showAllYearServiceSupportData(self):
        self.selectContentBox.setCurrentIndex(0)
        self.initServiceSupportTitle()
        self.showContentOfServiceSupport()



    '''
        功能：初始化显示所有年份
    '''
    def _initYearWidget_(self):
        self.yearList = []
        self.currentYear = None
        self.lw_yearChoose.clear()
        # self.yearList = ['全部']
        allYear = selectYearListAboutServiceSupport()
        # print("allYear:", allYear)

        for year in allYear:
            self.yearList.append(year)

        for year in self.yearList:
            # print("year:", year)
            item = QListWidgetItem()
            # print("item:", item)
            item.setText(str(year))
            # print("str(year):", str(year))
            self.lw_yearChoose.addItem(item)

        self.initServiceSupportTitle()
        # self.setServiceSupportTitle()
        self.showContentOfServiceSupport()


    '''
        功能：初始化“所有年度”维修保障计划显示所有
    '''
    def initServiceSupportTitle(self):
        txt = "所有年度核化装备维修保障计划及预算明细表"
        # self.txt_serviceSupportYear.setFont(QFont("Microsoft YaHei"))
        self.txt_serviceSupportYear.setAlignment(Qt.AlignHCenter)
        self.txt_serviceSupportYear.setTextInteractionFlags(Qt.NoTextInteraction)
        self.txt_serviceSupportYear.setFontPointSize(18)
        self.txt_serviceSupportYear.setText(txt)


    '''
        功能：更新展示“相应年份”维修保障计划表的表头
    '''
    def setServiceSupportTitle(self):
        # print(self.currentYear)
        txt = str(self.currentYear)+"年度核化装备维修保障计划及预算明细表"
        # self.txt_serviceSupportYear.setFont(QFont("Microsoft YaHei"))
        self.txt_serviceSupportYear.setAlignment(Qt.AlignHCenter)
        self.txt_serviceSupportYear.setTextInteractionFlags(Qt.NoTextInteraction)
        self.txt_serviceSupportYear.setFontPointSize(18)
        self.txt_serviceSupportYear.setText(txt)


    '''
        功能：更新展示“相应类型”维修保障计划表的表头
    '''
    def setTypeServiceSupportTitle(self):
        # print(self.currentYear)
        item = self.selectContentBox.currentText()
        txt = str(item)+"--核化装备维修保障计划及预算明细表"
        # self.txt_serviceSupportYear.setFont(QFont("Microsoft YaHei"))
        self.txt_serviceSupportYear.setAlignment(Qt.AlignHCenter)
        self.txt_serviceSupportYear.setTextInteractionFlags(Qt.NoTextInteraction)
        self.txt_serviceSupportYear.setFontPointSize(18)
        self.txt_serviceSupportYear.setText(txt)


    '''
        功能：画表头,行数有2行
    '''
    def initTableHeader(self):
        self.serviceSupportResult.setRowCount(2)
        self.serviceSupportResult.setColumnCount(14)
        self.serviceSupportResult.verticalHeader().setVisible(False)
        self.serviceSupportResult.horizontalHeader().setVisible(False)
        # self.serviceSupportResult.setEditTriggers(QTableWidget.NoEditTriggers)
        self.serviceSupportResult.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.serviceSupportResult.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.serviceSupportResult.resizeColumnsToContents()
        self.serviceSupportResult.resizeRowsToContents()
        # self.serviceSupportResult.setSelectionBehavior(QAbstractItemView.SelectRows)

        #绘制表 第一行
        item = QTableWidgetItem("序号")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(0, 0, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.serviceSupportResult.setSpan(0, 0, 2, 1)
        self.serviceSupportResult.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.serviceSupportResult.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

        item = QTableWidgetItem("项目类型")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(0, 1, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.serviceSupportResult.setSpan(0, 1, 2, 1)

        item = QTableWidgetItem("项目名称")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(0, 2, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.serviceSupportResult.setSpan(0, 2, 2, 1)

        item = QTableWidgetItem("计量单位")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(0, 3, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.serviceSupportResult.setSpan(0, 3, 2, 1)

        item = QTableWidgetItem("审核")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(0, 4, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.serviceSupportResult.setSpan(0, 4, 1, 3)

        item = QTableWidgetItem("单价")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(1, 4, item)
        item.setFlags(Qt.ItemIsEnabled)

        item = QTableWidgetItem("数量")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(1, 5, item)
        item.setFlags(Qt.ItemIsEnabled)

        item = QTableWidgetItem("金额")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(1, 6, item)
        item.setFlags(Qt.ItemIsEnabled)

        item = QTableWidgetItem("单位")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(0, 7, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.serviceSupportResult.setSpan(0, 7, 1, 2)

        item = QTableWidgetItem("分配（送修）")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(1, 7, item)
        item.setFlags(Qt.ItemIsEnabled)

        item = QTableWidgetItem("供货（承修）")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(1, 8, item)
        item.setFlags(Qt.ItemIsEnabled)

        item = QTableWidgetItem("计价挂账进度")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(0, 9, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.serviceSupportResult.setSpan(0, 9, 1, 3)

        item = QTableWidgetItem("确定技术状态")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(1, 9, item)
        item.setFlags(Qt.ItemIsEnabled)

        item = QTableWidgetItem("签订合同")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(1, 10, item)
        item.setFlags(Qt.ItemIsEnabled)

        item = QTableWidgetItem("支付")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(1, 11, item)
        item.setFlags(Qt.ItemIsEnabled)

        item = QTableWidgetItem("年份/时间")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(0, 12, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.serviceSupportResult.setSpan(0, 12, 2, 1)

        item = QTableWidgetItem("备注")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(0, 13, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.serviceSupportResult.setSpan(0, 13, 2, 1)



    '''
        功能：
           读取维修保障表数据并显示
    '''
    def showContentOfServiceSupport(self):
        self.serviceSupportResult.itemChanged.disconnect(self.slotAlterAndSava)
        self.initTableHeader()
        data = selectContentOfServiceSupport()
        # print("data:",data)
        self.currentLastRow = -1
        row = len(data)  # 取得记录个数，用于设置表格的行数
        vol = 14  # 取得字段数，用于设置表格的列数
        self.serviceSupportResult.setRowCount(row+2)
        self.serviceSupportResult.setColumnCount(vol)
        self.datadict = {}
        dataTypeOne = []
        dataTypeTwo = []
        dataTypeThree = []
        dataTypeFour = []

        #遍历数据并分类
        for i in range(row):
            self.datadict[str(i+1)] = data[i]
            for j in range(vol):
                if j == 0:
                    temp_data = i+1
                    datas = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                    self.serviceSupportResult.setItem(i + 2, j, datas)
                elif j == 1:
                    #print(data[i][1])   #(一)装备大修
                    #print(data[i])     #(1, '(一)装备大修', '1', '1', 1.0, 1, 1.0, '1', '1', '不涉及', '不涉及', '不涉及', '2024', '')
                    dataType = data[i][1]
                    if dataType == '(一)装备大修':
                        dataTypeOne.append(data[i])
                    elif dataType == '(二)装备中修':
                        dataTypeTwo.append(data[i])
                    elif dataType == '(三)维修器材购置':
                        dataTypeThree.append(data[i])
                    elif dataType == '(四)修理能力建设':
                        dataTypeFour.append(data[i])
                else:
                    pass

        dataTypeOneRow = len(dataTypeOne)
        dataTypeTwoRow = len(dataTypeTwo)
        dataTypeThreeRow = len(dataTypeThree)
        dataTypeFourRow = len(dataTypeFour)
        m = 1
        number = 0
        for k in range(dataTypeOneRow):
            m = m + 1
            number = number +1
            for l in range(vol):
                if l == 0:
                    temp_data = number
                    datas = QTableWidgetItem(str(temp_data))
                    self.serviceSupportResult.setItem(k + 2, 0, datas)
                else:
                    temp_data = dataTypeOne[k][l]  # 临时记录，不能直接插入表格
                    datas = QTableWidgetItem(str(temp_data))  # 转换后可插入表格

                    self.serviceSupportResult.setItem(k + 2, l, datas)
            if k == 0 and dataTypeOneRow > 1:
                self.serviceSupportResult.setSpan(m, 1, dataTypeOneRow, 1)  # 要合并的单元格的位置，需要合并的行数，需要合并的列数
        # print("m1:", m)

        for k in range(dataTypeTwoRow):
            m = m + 1
            number = number + 1
            for l in range(vol):
                if l == 0:
                    temp_data = number
                    datas = QTableWidgetItem(str(temp_data))
                    self.serviceSupportResult.setItem(k + 2 + dataTypeOneRow, 0, datas)
                else:
                    temp_data = dataTypeTwo[k][l]  # 临时记录，不能直接插入表格
                    datas = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                    self.serviceSupportResult.setItem(k + 2 + dataTypeOneRow, l, datas)
            if k == 0 and dataTypeTwoRow > 1:
                self.serviceSupportResult.setSpan(m, 1, dataTypeTwoRow, 1)
        # print("m2:", m)

        for k in range(dataTypeThreeRow):
            m = m + 1
            number = number + 1
            for l in range(vol):
                if l == 0:
                    temp_data = number
                    datas = QTableWidgetItem(str(temp_data))
                    self.serviceSupportResult.setItem(k + 2 + dataTypeOneRow + dataTypeTwoRow, 0, datas)
                else:
                    temp_data = dataTypeThree[k][l]  # 临时记录，不能直接插入表格
                    datas = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                    self.serviceSupportResult.setItem(k + 2 + dataTypeOneRow + dataTypeTwoRow, l, datas)
            if k == 0 and dataTypeThreeRow > 1:
                self.serviceSupportResult.setSpan(m, 1, dataTypeThreeRow, 1)
        # print("m3:", m)

        for k in range(dataTypeFourRow):
            m = m + 1
            number = number + 1
            for l in range(vol):
                if l == 0:
                    temp_data = number
                    datas = QTableWidgetItem(str(temp_data))
                    self.serviceSupportResult.setItem(k + 2 + dataTypeOneRow + dataTypeTwoRow + dataTypeThreeRow, 0, datas)
                else:
                    temp_data = dataTypeFour[k][l]  # 临时记录，不能直接插入表格
                    datas = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                    self.serviceSupportResult.setItem(k + 2 + dataTypeOneRow + dataTypeTwoRow + dataTypeThreeRow, l, datas)
            if k == 0 and dataTypeFourRow > 1:
                self.serviceSupportResult.setSpan(m, 1, dataTypeFourRow, 1)
        # print("m4:", m)

        # print("dataTypeOne:", dataTypeOne)
        # print("dataTypeTwo:", dataTypeTwo)
        # print("dataTypeThree:", dataTypeThree)
        # print("dataTypeFour:", dataTypeFour)
        # print("datadict:",self.datadict)

        self.serviceSupportResult.itemChanged.connect(self.slotAlterAndSava)



    '''
        功能：
            读取相应年份的维修保障表数据并显示
    '''
    def showYearContentOfServiceSupport(self):
        currentYear = self.lw_yearChoose.currentItem()
        data = selectYearContentOfServiceSupport(currentYear.text())
        # print(data)
        row = len(data)  # 取得记录个数，用于设置表格的行数
        vol = 14  # 取得字段数，用于设置表格的列数
        self.serviceSupportResult.setRowCount(row + 2)
        self.serviceSupportResult.setColumnCount(vol)

        for i in range(row):
            for j in range(vol):
                if j == 0:
                    temp_data = i + 1
                    datas = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                    self.serviceSupportResult.setItem(i + 2, j, datas)
                else:
                    temp_data = data[i][j]  # 临时记录，不能直接插入表格
                    datas = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                    self.serviceSupportResult.setItem(i + 2, j, datas)
            if i == 0 and row > 1:
                self.serviceSupportResult.setSpan(2, 1, row, 1)
                self.serviceSupportResult.setSpan(2, 12, row, 1)



    '''
        功能：新增一行的数据
    '''
    def slotAlterAndSava(self):
        selectRow = self.serviceSupportResult.selectedItems()
        if len(selectRow) != 0:
            currentRow = selectRow[0].row()
            currentColumn = selectRow[0].column()

            #设置金额=单价*数量
            if (currentColumn == 4 or currentColumn == 5 and currentRow >= 2):
                item0 = self.serviceSupportResult.item(currentRow, 4)
                item1 = self.serviceSupportResult.item(currentRow, 5)
                if (item1 != None and item0 != None):
                    if (len(item0.text()) > 0 and len(item1.text()) > 0):
                        self.serviceSupportResult.itemChanged.disconnect(self.slotAlterAndSava)
                        count = 0
                        unit = 0
                        try:
                            count = int(item1.text())
                        except ValueError:
                            QMessageBox.warning(self, "注意", "请输入整数！", QMessageBox.Yes, QMessageBox.Yes)
                            item1.setText('')
                        try:
                            unit = float(item0.text())
                        except:
                            QMessageBox.warning(self, "注意", "请输入正确的数字！", QMessageBox.Yes, QMessageBox.Yes)
                            item0.setText('')
                        amount = round(count * unit, 4)
                        if (amount != 0):
                            item = self.serviceSupportResult.item(currentRow, 6)
                            if (item != None):
                                item.setText(str(amount))
                                item.setFlags(Qt.ItemIsEnabled)
                            else:
                                item = QTableWidgetItem(str(amount))
                                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                                item.setFlags(Qt.ItemIsEnabled)
                                self.serviceSupportResult.setItem(currentRow, 6, item)
                        self.serviceSupportResult.itemChanged.connect(self.slotAlterAndSava)
            if currentRow == self.currentLastRow:
                self.savaRowData(currentRow)
            else:
                self.alterRowData(currentRow)

    #保存一行数据
    def savaRowData(self, row):
        rowData = []
        for i in range(0, self.serviceSupportResult.columnCount()):
            if i == 0:
                item = str(self.bl)
                rowData.append(item)
            elif i == 1 or i == 9 or i == 10 or i == 11:
                item = self.serviceSupportResult.cellWidget(row, i).currentText()
                rowData.append(item)
            elif i == 13:
                item = self.serviceSupportResult.item(row, i)
                if item != None:
                    rowData.append(item.text())
                else:
                    rowData.append('')
            else:
                item = self.serviceSupportResult.item(row, i)
                if item != None and len(item.text()) > 0:
                    rowData.append(item.text())
                else:
                    break
        if len(rowData) != self.serviceSupportResult.columnCount():
            return False
        else:
            insertContentOfServiceSupport(rowData)
            QMessageBox.warning(self, "注意", "插入成功！", QMessageBox.Yes, QMessageBox.Yes)
            self.showContentOfServiceSupport()
            self._initYearWidget_()

    #修改一行数据
    def alterRowData(self, row):
        rowData = []
        for i in range(self.serviceSupportResult.columnCount()):
            if i == 0:
                currentRow = self.serviceSupportResult.currentRow()
                currentRowNum = currentRow - 1
                currentRowNumKeyValue = self.datadict[str(currentRowNum)][0]
                rowData.append(str(currentRowNumKeyValue))
                # print("111111",rowData)
            elif i == 13:
                item = self.serviceSupportResult.item(row, i)
                if item != None:
                    rowData.append(item.text())
                else:
                    rowData.append('')
            else:
                item = self.serviceSupportResult.item(row, i)
                if item != None and len(item.text()) > 0:
                    rowData.append(item.text())
                else:
                    break
        if len(rowData) != self.serviceSupportResult.columnCount():
            return False
        else:
            QMessageBox.warning(self, "注意", "修改成功！", QMessageBox.Yes, QMessageBox.Yes)
            updateContentOfServiceSupport(rowData)
            self._initYearWidget_()
        pass

    # 组件
    def slotInput(self):
        pass

    def slotOutput(self):
        pass



    '''
        功能： “新增计划” 按钮槽函数
    '''
    def slotAdd(self):
        rowCount = self.serviceSupportResult.rowCount()
        dataCount = len(self.datadict)
        numList = []
        # print("dataCount:", dataCount)
        for i in range(dataCount):
            temp_data = self.datadict[str(i+1)][0]
            numList.append(int(temp_data))
            # print(numList)

        if numList == []:
            self.bl = 1
        else:
            self.bl = int(max(numList)) + 1
        # print("self.bl:", self.bl)

        if self.serviceSupportResult.rowCount() <= 2 + rowCount:
            self.currentLastRow = rowCount
            self.serviceSupportResult.insertRow(rowCount)

            # 设置新增一行的序号为上一行序号+1
            if rowCount <= 2:
                currentRowNum = 1
                item = QTableWidgetItem(str(currentRowNum))
                self.serviceSupportResult.setItem(rowCount, 0, item)
            else:
                LastRowNum = self.serviceSupportResult.item(rowCount - 1, 0).text()
                currentRowNum = int(LastRowNum) + 1
                item = QTableWidgetItem(str(currentRowNum))
                self.serviceSupportResult.setItem(rowCount, 0, item)

            comboBox = QComboBox()
            comboBox.addItems(['(一)装备大修', '(二)装备中修', '(三)维修器材购置', '(四)修理能力建设'])
            self.serviceSupportResult.setCellWidget(rowCount, 1, comboBox)
            comboBox.currentIndexChanged.connect(self.projectTypeConnectProgress)

            comboBox = QComboBox()
            comboBox.addItems(['不涉及', '是', '否'])
            self.serviceSupportResult.setCellWidget(rowCount, 9, comboBox)
            comboBox = QComboBox()
            comboBox.addItems(['不涉及', '是', '否'])
            self.serviceSupportResult.setCellWidget(rowCount, 10, comboBox)
            comboBox = QComboBox()
            comboBox.addItems(['不涉及', '是', '否'])
            self.serviceSupportResult.setCellWidget(rowCount, 11, comboBox)

            item = QTableWidgetItem("")
            self.serviceSupportResult.setItem(rowCount, 2, item)
            item = QTableWidgetItem("")
            self.serviceSupportResult.setItem(rowCount, 3, item)
            item = QTableWidgetItem("")
            self.serviceSupportResult.setItem(rowCount, 4, item)
            item = QTableWidgetItem("")
            self.serviceSupportResult.setItem(rowCount, 5, item)
            item = QTableWidgetItem("")
            self.serviceSupportResult.setItem(rowCount, 6, item)
            item = QTableWidgetItem("")
            self.serviceSupportResult.setItem(rowCount, 7, item)
            item = QTableWidgetItem("")
            self.serviceSupportResult.setItem(rowCount, 8, item)
            item = QTableWidgetItem("")
            self.serviceSupportResult.setItem(rowCount, 12, item)
            item = QTableWidgetItem("")
            self.serviceSupportResult.setItem(rowCount, 13, item)

        else:
            QMessageBox.warning(self, "注意", "请先将数据补充完整！", QMessageBox.Yes, QMessageBox.Yes)



    '''
        功能： “删除计划” 按钮槽函数
    '''
    def slotDelete(self):
        rowCount = self.serviceSupportResult.currentRow()
        if rowCount < 2:
            QMessageBox.warning(self, "注意", "请选中有效单元格！", QMessageBox.Yes, QMessageBox.Yes)
            return
        elif rowCount >= 2:
            # item = self.serviceSupportResult.item(rowCount, 0)
            #应该删除的是字典datadict中的 key = item.text()的值的第一个数据 对应的数据库中的值
            if self.datadict=={}:
                self.serviceSupportResult.removeRow(rowCount)
            else:
                currentRow = self.serviceSupportResult.currentRow()
                currentRowNum = currentRow -1
                currentRowNumKeyValue = self.datadict[str(currentRowNum)][0]
                deleteDataByServiceSupportNum(int(currentRowNumKeyValue))
                self.serviceSupportResult.removeRow(rowCount)
                self._initYearWidget_()
                # deleteDataByServiceSupportNum(item.text())
                # self.serviceSupportResult.removeRow(rowCount)



    '''
        功能：根据项目类型进行筛选
    '''
    def selectDataAboutProjectType(self):
        item = self.selectContentBox.currentText()
        data = selectProjectTypeOfServiceSupport(item)
        self.currentLastRow = -1
        row = len(data)  # 取得记录个数，用于设置表格的行数
        vol = 14  # 取得字段数，用于设置表格的列数
        self.serviceSupportResult.setRowCount(row + 2)
        self.serviceSupportResult.setColumnCount(vol)
        for i in range(row):
            for j in range(vol):
                if j == 0:
                    temp_data = i + 1      # 临时记录，不能直接插入表格
                    datas = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                    self.serviceSupportResult.setItem(i + 2, 0, datas)
                else:
                    temp_data = data[i][j]  # 临时记录，不能直接插入表格
                    datas = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                    self.serviceSupportResult.setItem(i + 2, j, datas)
            if i == 0 and row > 1:
                self.serviceSupportResult.setSpan(2, 1, row, 1)



    '''
        功能：设置项目类型关联后面计价挂账进度值
    '''
    def projectTypeConnectProgress(self):
        # print(111111111111111)判断有没有进入该函数
        currentRow = self.serviceSupportResult.currentRow()
        currentColumn = self.serviceSupportResult.currentColumn()

        #设置项目类型关联后面计价挂账进度值
        if (currentColumn == 1):
            item = self.serviceSupportResult.cellWidget(currentRow, 1).currentIndex()
            if item == 0 or item == 1:
                comboBox = QComboBox()
                comboBox.addItems(['不涉及'])
                self.serviceSupportResult.setCellWidget(currentRow, 9, comboBox)
                comboBox = QComboBox()
                comboBox.addItems(['不涉及'])
                self.serviceSupportResult.setCellWidget(currentRow, 10, comboBox)
                comboBox = QComboBox()
                comboBox.addItems(['不涉及'])
                self.serviceSupportResult.setCellWidget(currentRow, 11, comboBox)

                # self.serviceSupportResult.cellWidget(currentRow, 9).setCurrentIndex(0)
                # self.serviceSupportResult.cellWidget(currentRow, 10).setCurrentIndex(0)
                # self.serviceSupportResult.cellWidget(currentRow, 11).setCurrentIndex(0)
            else:
                comboBox = QComboBox()
                comboBox.addItems(['是','否'])
                self.serviceSupportResult.setCellWidget(currentRow, 9, comboBox)
                comboBox = QComboBox()
                comboBox.addItems(['是','否'])
                self.serviceSupportResult.setCellWidget(currentRow, 10, comboBox)
                comboBox = QComboBox()
                comboBox.addItems(['是','否'])
                self.serviceSupportResult.setCellWidget(currentRow, 11, comboBox)

                # self.serviceSupportResult.cellWidget(currentRow, 9).setCurrentIndex(1)
                # self.serviceSupportResult.cellWidget(currentRow, 10).setCurrentIndex(1)
                # self.serviceSupportResult.cellWidget(currentRow, 11).setCurrentIndex(1)


#删除一行数据之后，如果再新增一行数据，序号为前一行加1，则读入的时候是读入的当前的序号值，
# 如果序号值与数据库中已经存在的逐渐num重复了，则插入不进去，应该有一个唯一标识，每次点击新增的时候就加1，使存入数据库的num值一直保持增加，但是如果程序关闭了，该值又得刷新

    '''
    功能：导出至Excel
    '''
    def slotOutputToExcel(self):
        currentRowCount = self.serviceSupportResult.rowCount()
        currentColumnCount = 14
        dataExcelList = []
        for i in range(2, currentRowCount):            #从（行2，列0）开始读数据
            dataRowList = []
            for j in range(currentColumnCount):
                item = self.serviceSupportResult.item(i, j)
                dataRowList.append(item.text())

            dataExcelList.append(dataRowList)
        # print("dataExcelList:", dataExcelList)

        if len(dataExcelList) < 1:
            reply = QMessageBox.warning(self, '警告', '没有任何数据，无法导出', QMessageBox.Yes)
            return
        reply = QMessageBox.question(self, '将内容导出Excel', '是否保存数据并导出至Excel？', QMessageBox.Cancel, QMessageBox.Yes)

        if reply == QMessageBox.Cancel:
            return

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
            for i in range(14):
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

            workSheet.write_merge(0, 0, 0, 13, "核化装备维修保障计划及预算明细表", titileStyle)
            workSheet.write_merge(1, 2, 0, 0,'序号', titileStyle)
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
            if dataExcelList is None or len(dataExcelList) == 0:
                self.serviceSupportResult.setRowCount(3)
                self.initTableHeader()
            else:
                for i in range(len(dataExcelList)):
                    workSheet.write(3 + i, 0, dataExcelList[i][0], contentStyle)
                    workSheet.write(3 + i, 1, dataExcelList[i][1], contentStyle)
                    workSheet.write(3 + i, 2, dataExcelList[i][2], contentStyle)
                    workSheet.write(3 + i, 3, dataExcelList[i][3], contentStyle)
                    workSheet.write(3 + i, 4, dataExcelList[i][4], contentStyle)
                    workSheet.write(3 + i, 5, dataExcelList[i][5], contentStyle)
                    workSheet.write(3 + i, 6, dataExcelList[i][6], contentStyle)
                    workSheet.write(3 + i, 7, dataExcelList[i][7], contentStyle)
                    workSheet.write(3 + i, 8, dataExcelList[i][8], contentStyle)
                    workSheet.write(3 + i, 9, dataExcelList[i][9], contentStyle)
                    workSheet.write(3 + i, 10, dataExcelList[i][10], contentStyle)
                    workSheet.write(3 + i, 11, dataExcelList[i][11], contentStyle)
                    workSheet.write(3 + i, 12, dataExcelList[i][12], contentStyle)
                    workSheet.write(3 + i, 13, dataExcelList[i][13], contentStyle)
            try:
                pathName = "%s/核化装备维修保障计划及预算明细表.xls" % (directoryPath)
                workBook.save(pathName)
                import win32api
                win32api.ShellExecute(0, 'open', pathName, '', '', 1)
                QMessageBox.about(self, "导出成功", "导出成功！")
                return
            except Exception as e:
                QMessageBox.about(self, "导出失败", "导出表格被占用，请关闭正在使用的Execl！")
                return




if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = serviceSupport()
    widget.show()
    sys.exit(app.exec_())