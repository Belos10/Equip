import pickle

from PyQt5.QtCore import Qt, QStringListModel, QDate, QDateTime

from database.contractManagementSql import *
from sysManage.showInputResult import showInputResult
from sysManage.userInfo import get_value
from widgets.contractMangement.OrderManagementUI import OrderManagementUI
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidget, QHeaderView, QTableWidgetItem, QComboBox, \
    QMessageBox, QFileDialog, QListWidgetItem, QListView, QInputDialog, QDateEdit, QAbstractItemView


class OrderManagement(QWidget, OrderManagementUI):
    def __init__(self, parent=None):
        super(OrderManagement, self).__init__(parent)
        self.setupUi(self)
        self.selectedYear = ''
        self.contractName = ''
        self.contractNo = ''
        self.inputList = []
        self.showInputResult = showInputResult(self)
        self.showInputResult.hide()
        self.signalConnection()
        self.init()

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
        pass

    '''
                功能：
                    初始化年份列表
    '''

    def initYearList(self):
        self.yearList = []
        self.yearList = getYearsFromContractOrder()
        listModel = QStringListModel()
        listModel.setStringList(self.yearList)
        self.lv_year.setModel(listModel)
        self.lv_year.setEditTriggers(QAbstractItemView.NoEditTriggers)


    '''
        新增年份
    '''
    def soltAddContractYear(self):
        year = 0
        year, ok = QInputDialog.getInt(self, "Get year", "year:", 0, 0, 100000, 1)
        if ok:
            if isHaveContractOrderYear(str(year)):
                QMessageBox.information(self, "新增", "该年份已经存在，拒绝添加！", QMessageBox.Yes)
                return
            else:
                insertSuccess = addContractOrderYear(year)
                if insertSuccess == True:
                    QMessageBox.information(self, "新增", "新增成功！", QMessageBox.Yes)
                else:
                    QMessageBox.information(self, "新增", "新增失败！", QMessageBox.Yes)
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
        self.contractName = self.le_contractName.text()
        self.contractNo =  self.le_contractNo.text()
        self.displayData()

    '''
        功能：
            将列表数据展示在表中
    '''

    def displayData(self):
        self.tw_result.itemChanged.disconnect(self.slotAlterAndSava)
        self.result = getResult(self.selectedYear, self.contractNo, self.contractName)
        self.tw_result.clear()
        self.tw_result.setColumnCount(11)
        self.currentLastRow = 0
        dataList = self.result
        if dataList is None or len(dataList) == 0:
            self.tw_result.setRowCount(2)
            self.initTableHeader()
        else:
            self.tw_result.setRowCount(2 + len(dataList))
            self.initTableHeader()
            item = QTableWidgetItem(self.selectedYear + '年')
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(2, 0, item)
            self.tw_result.setSpan(2,0,len(dataList),1)
            for i in range(len(dataList)):
                item = QTableWidgetItem(str(i + 1))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.tw_result.setItem(2 + i, 1, item)

                item = QTableWidgetItem(dataList[i][2])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(2 + i, 2, item)

                item = QTableWidgetItem(dataList[i][3])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(2 + i, 3, item)

                item = QTableWidgetItem(dataList[i][4])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(2 + i, 4, item)

                item = QTableWidgetItem(dataList[i][5])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(2 + i, 5, item)

                item = QTableWidgetItem(str(dataList[i][6]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(2 + i, 6, item)

                item = QTableWidgetItem(str(dataList[i][7]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(2 + i, 7, item)

                item = QTableWidgetItem(str(dataList[i][8]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.tw_result.setItem(2 + i, 8, item)

                date = dataList[i][9]
                parsedDateList = date.split('-')
                dataEdit = QDateEdit()
                dataEdit.setDisplayFormat("yyyy-MM-dd")
                dataEdit.setDate(QDate(int(parsedDateList[0]), int(parsedDateList[1]), int(parsedDateList[2])))
                dataEdit.setEnabled(False)
                self.tw_result.setCellWidget(2 + i, 9, dataEdit)


                item = QTableWidgetItem(dataList[i][10])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                # item.setFlags(Qt.ItemIsEnabled)
                self.tw_result.setItem(2 + i, 10, item)
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
        item = QTableWidgetItem("订购计划--合同")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(0, 0, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setSpan(0, 0, 1, 11)

        item = QTableWidgetItem("年度")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 0, item)
        item.setFlags(Qt.ItemIsEnabled)


        item = QTableWidgetItem("序号")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 1, item)
        item.setFlags(Qt.ItemIsEnabled)

        item = QTableWidgetItem("合同编号")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 2, item)

        item = QTableWidgetItem("合同名称")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 3, item)

        item = QTableWidgetItem("（甲方）")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 4, item)


        item = QTableWidgetItem("（乙方）")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 5, item)


        item = QTableWidgetItem("单价（万元）")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 6, item)


        item = QTableWidgetItem("数量/单位")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 7, item)

        item = QTableWidgetItem("金额（万元）")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 8, item)

        item = QTableWidgetItem("交付时间")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 9, item)

        item = QTableWidgetItem("备注")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 10, item)

    '''
        功能：
            新增一行的数据
    '''

    def slotAlterAndSava(self):
        selectRow = self.tw_result.selectedItems()
        if len(selectRow) != 0:
            currentRow = selectRow[0].row()
            currentColumn = selectRow[0].column()
            if (currentColumn == 6 or currentColumn == 7 and currentRow >= 2):
                item0 = self.tw_result.item(currentRow, 6)
                item1 = self.tw_result.item(currentRow, 7)
                if (item1 != None and item0 != None):
                    if (len(item0.text()) > 0 and len(item1.text()) > 0):
                        self.tw_result.itemChanged.disconnect(self.slotAlterAndSava)
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
                        item = self.tw_result.item(currentRow,8)
                        if(item != None):
                            item.setText(str(amount))
                            item.setFlags(Qt.ItemIsEnabled)
                        else:
                            item = QTableWidgetItem(str(amount))
                            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                            item.setFlags(Qt.ItemIsEnabled)
                            self.tw_result.setItem(currentRow, 8, item)
                        self.tw_result.itemChanged.connect(self.slotAlterAndSava)

            if currentRow == self.currentLastRow:
                self.savaRowData(currentRow)
            else:
                self.alterRowData(currentRow)


    def savaRowData(self, row):
        # print('保存一行')
        rowData = []
        rowData.append(self.selectedYear)
        for i in range(1, self.tw_result.columnCount()):
            if i == 1:
                continue
            if i == 9:
                item = self.tw_result.cellWidget(row, i)
                if item != None:
                    date = item.date().toString(Qt.ISODate)
                    rowData.append(date)
                else:
                    break
            else:
                item = self.tw_result.item(row, i)
                if (item != None):
                    if (len(item.text()) > 0):
                        rowData.append(item.text())
                else:
                    break
        if len(rowData) == self.tw_result.columnCount() - 1:
            if(insertOneDataInToContractOrder(rowData) == True):
                QMessageBox.warning(self, "注意", "插入成功！", QMessageBox.Yes, QMessageBox.Yes)
            else:
                QMessageBox.warning(self, "警告", "插入失败！", QMessageBox.Yes, QMessageBox.Yes)
            self.displayData()

    def alterRowData(self, row):
        # print("修改一行数据")
        rowData = []
        rowData.append(self.result[row - 2][0])
        for i in range(1, self.tw_result.columnCount()):
            if i == 1:
                continue
            if i == 9:
                item = self.tw_result.cellWidget(row, i)
                if item != None:
                    date = item.date().toString(Qt.ISODate)
                    rowData.append(date)
                else:
                    break
            else:
                item = self.tw_result.item(row, i)
                if (item != None):
                    if (len(item.text()) > 0):
                        rowData.append(item.text())
                else:
                    break
        if len(rowData) == self.tw_result.columnCount() - 1:
            if (updataOneDataToContractOrder(rowData) == True):
                QMessageBox.warning(self, "注意", "修改成功！", QMessageBox.Yes, QMessageBox.Yes)
            else:
                QMessageBox.warning(self, "警告", "修改失败！", QMessageBox.Yes, QMessageBox.Yes)
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
            item = QTableWidgetItem(self.selectedYear + '年')
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(2, 0, item)
            self.tw_result.setSpan(2, 0, rowCount + 1, 1)
            if (rowCount + 1 == 3):
                item = QTableWidgetItem('1')
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.tw_result.setItem(2, 1, item)
            else:
                lastNo = int(self.tw_result.item(rowCount - 1,1).text())
                item = QTableWidgetItem(str(lastNo + 1))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.tw_result.setItem(rowCount, 1, item)
            item = QTableWidgetItem('')
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(rowCount, 8, item)
            deliveryDate = QDateEdit()
            deliveryDate.setDisplayFormat("yyyy-MM-dd")
            self.tw_result.setCellWidget(rowCount, 9, deliveryDate)
            self.tw_result.itemChanged.connect(self.slotAlterAndSava)

        else:
            QMessageBox.warning(self, "注意", "请先将数据补充完整！", QMessageBox.Yes, QMessageBox.Yes)

    def slotDelete(self):

        rowCount = self.tw_result.currentRow()
        resultCount = len(self.result)
        if rowCount < 2:
            QMessageBox.warning(self, "注意", "请选中有效单元格！", QMessageBox.Yes, QMessageBox.Yes)
        elif rowCount >= 2 and rowCount < 2 + resultCount:
            reply = QMessageBox.question(self, '警告', '是否删除该行数据？', QMessageBox.Cancel, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                deleteDataByContractOrderIdAndYear(self.result[rowCount - 2][0],self.selectedYear)
                self.tw_result.removeRow(rowCount)
            else:
                return
        else:
            self.tw_result.removeRow(rowCount)


    #导出至Excel
    def slotOutputToExcel(self):
        if len(self.result) < 1:
            reply = QMessageBox.warning(self, '警告', '未选中任何数据，无法导出', QMessageBox.Yes)
            return
        reply = QMessageBox.question(self, '修改导出Excel', '是否保存修改并导出Excel？', QMessageBox.Cancel, QMessageBox.Yes)
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
            for i in range(11):
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
            workSheet.write_merge(0, 0, 0, 10, "订购计划--合同",titileStyle)
            workSheet.write(1, 0, "年度", titileStyle)
            workSheet.write(1, 1, "序号", titileStyle)
            workSheet.write(1, 2, "合同编号", titileStyle)
            workSheet.write(1, 3, "合同名称", titileStyle)
            workSheet.write(1, 4, "（甲方）", titileStyle)
            workSheet.write(1, 5, "（乙方）", titileStyle)
            workSheet.write(1, 6, "单价（万元）", titileStyle)
            workSheet.write(1, 7, "数量/单位i额", titileStyle)
            workSheet.write(1, 8, "金额（万元）", titileStyle)
            workSheet.write(1, 9, "交付日期", titileStyle)
            workSheet.write(1, 10, "备注", titileStyle)


            #填表数据
            dataList = self.result
            if len(dataList) > 0:
                workSheet.write_merge(2, 1 + len(dataList), 0, 0, self.selectedYear + '年', contentStyle)
                for i in range(len(dataList)):
                    workSheet.write(2 + i, 1, str(dataList[i][0]), contentStyle)
                    workSheet.write(2 + i, 2, dataList[i][2], contentStyle)
                    workSheet.write(2 + i, 3, dataList[i][3], contentStyle)
                    workSheet.write(2 + i, 4, dataList[i][4], contentStyle)
                    workSheet.write(2 + i, 5, dataList[i][5], contentStyle)
                    workSheet.write(2 + i, 6, str(dataList[i][6]), contentStyle)
                    workSheet.write(2 + i, 7, str(dataList[i][7]), contentStyle)
                    workSheet.write(2 + i, 8, str(dataList[i][8]), contentStyle)
                    workSheet.write(2 + i, 9, dataList[i][9], contentStyle)
                    workSheet.write(2 + i, 10, dataList[i][10], contentStyle)

            try:
                pathName = "%s/%s年订购计划--合同.xls" % (directoryPath,self.selectedYear)
                workBook.save(pathName)
                import win32api
                win32api.ShellExecute(0, 'open', pathName, '', '', 1)
                QMessageBox.about(self, "导出成功", "导出成功！")
                return
            except Exception as e:
                QMessageBox.about(self, "导出失败", "导出表格被占用，请关闭正在使用的Execl！")
                return

        pass

        # 导出数据包

    def slotOutputData(self):
        if len(self.result) < 1:
            reply = QMessageBox.warning(self, '警告', '未选中任何数据，无法导出', QMessageBox.Yes)
            return
        reply = QMessageBox.question(self, '导出数据包', '是否保存修改并导出数据包？', QMessageBox.Cancel, QMessageBox.Yes)
        if reply == QMessageBox.Cancel:
            self.displayData()
            return
        directoryPath = QFileDialog.getExistingDirectory(self, "请选择导出文件夹", "c:/")
        if len(directoryPath) > 0:
            # 填表数据
            dataList = self.result
            dataList.insert(0, "订单合同")
            print("订单合同")
            print(dataList)  # ['实力查询数据'， ['5', '10', 'A车', '六十一旅团一阵地', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, '2000']]
            if dataList is None or len(dataList) == 1:
                return
            else:
                date = QDateTime.currentDateTime()
                installData = date.toString("yyyy年MM月dd日hh时mm分ss秒")  # hh:mm:ss
                pathName = "%s/%s%s年订购计划合同.nms" % (
                directoryPath, installData, self.selectedYear)
                with open(pathName, "wb") as file:
                    pickle.dump(dataList, file)
                QMessageBox.warning(self, "导出数据成功！", "导出成功！", QMessageBox.Yes)
            pass
        else:
            QMessageBox.warning(self, "导出数据失败！", "请选择正确的文件夹！", QMessageBox.Yes)
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
                if self.inputList[0] != "订单合同":
                    raise Exception("数据格式错误！")
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "加载文件失败！", "请检查文件格式及内容格式！", QMessageBox.Yes)
            return
        headerlist = ['年度', '序号', '合同编号', '合同名称', '甲方', '乙方', '单价（万元）', '数量/单位', '金额（万元）', '交付时间', '备注']
        self.showInputResult.setWindowTitle("导入数据")
        self.showInputResult.show()
        # QTableWidget设置整行选中
        self.showInputResult.tw_result.setColumnCount(len(headerlist))
        self.showInputResult.tw_result.setHorizontalHeaderLabels(headerlist)
        self.showInputResult.tw_result.setRowCount(len(self.inputList) - 1)


        for i, LineInfo in enumerate(self.inputList):
            if i == 0:
                continue
            i = i - 1
            item = QTableWidgetItem(LineInfo[1])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 0, item)
            item = QTableWidgetItem(LineInfo[2])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 1, item)
            item = QTableWidgetItem(LineInfo[3])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 2, item)

            item = QTableWidgetItem(LineInfo[4])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 3, item)
            item = QTableWidgetItem(str(LineInfo[5]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 4, item)
            item = QTableWidgetItem(str(LineInfo[6]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 5, item)
            item = QTableWidgetItem(str(LineInfo[7]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 6, item)
            item = QTableWidgetItem(str(LineInfo[8]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 7, item)
            item = QTableWidgetItem(LineInfo[9])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 8, item)
            item = QTableWidgetItem(LineInfo[10])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 9, item)

    def slotCancelInputIntoDatabase(self):
        self.showInputResult.hide()
        self.setDisabled(False)

    def slotInputIntoDatabase(self):
        for i, lineInfo in enumerate(self.inputList):
            if i == 0:
                continue
            try:
                if insertOneDataIntoContractOrder(lineInfo):
                    pass
            except Exception as e:
                print(e)
                QMessageBox.warning(self, "导入失败", "导入第%d数据失败！" % (i), QMessageBox.Yes)

        self.showInputResult.hide()
        self.setDisabled(False)
        self.displayData()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = OrderManagement()
    widget.show()
    sys.exit(app.exec_())
