from PyQt5.QtCore import Qt, QStringListModel

from database.contractManagementSql import *
from sysManage.userInfo import get_value
from widgets.contractMangement.OrderManagementUI import OrderManagementUI
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidget, QHeaderView, QTableWidgetItem, QComboBox, \
    QMessageBox, QFileDialog, QListWidgetItem, QListView, QInputDialog


class OrderManagement(QWidget, OrderManagementUI):
    def __init__(self, parent=None):
        super(OrderManagement, self).__init__(parent)
        self.setupUi(self)
        self.selectedYear = ''
        self.contractName = ''
        self.contractNo = ''
        self.signalConnection()
        self.init()

    # 信号和槽连接
    def signalConnection(self):
        self.pb_select.clicked.connect(self.slotSelect)
        self.tb_input.clicked.connect(self.slotInput)
        self.pb_output.clicked.connect(self.slotOutput)
        self.tb_add.clicked.connect(self.slotAdd)
        self.tb_del.clicked.connect(self.slotDelete)
        self.lv_year.clicked.connect(self.displayDataByYear)
        self.pb_addYear.clicked.connect(self.soltAddContractYear)
        self.tb_outputToExcel.clicked.connect(self.slotOutputToExcel)
        self.tw_result.itemChanged.connect(self.slotAlterAndSava)


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
        print(self.yearList)
        listModel.setStringList(self.yearList)
        self.lv_year.setModel(listModel)
        if len(self.yearList) == 0:
            self.pb_output.setDisabled(True)
            self.pb_select.setDisabled(True)
            self.tb_add.setDisabled(True)
            self.tb_del.setDisabled(True)
            self.tb_outputToExcel.setDisabled(True)
            self.tw_result.setDisabled(True)
        else:
            self.pb_select.setDisabled(False)
            self.tb_add.setDisabled(False)
            self.tb_del.setDisabled(False)
            self.tb_outputToExcel.setDisabled(False)
            self.tw_result.setDisabled(False)
            self.pb_output.setDisabled(False)

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
        print(self.selectedYear, self.contractNo, self.contractName)
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
                print(dataList)
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

                item = QTableWidgetItem(dataList[i][9])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.tw_result.setItem(2 + i, 9, item)

                item = QTableWidgetItem(dataList[i][10])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
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
                        if (amount != 0):
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
            item = self.tw_result.item(row, i)
            if (item != None):
                if ( len(item.text()) > 0):
                    rowData.append(item.text())
            else:
                break
        if len(rowData) == self.tw_result.columnCount():
            if(insertOneDataInToContractOrder(rowData) == True):
                QMessageBox.warning(self, "注意", "插入成功！", QMessageBox.Yes, QMessageBox.Yes)
            else:
                QMessageBox.warning(self, "警告", "插入失败！", QMessageBox.Yes, QMessageBox.Yes)
            self.displayData()

    def alterRowData(self, row):
        # print("修改一行数据")
        rowData = []
        for i in range(1, self.tw_result.columnCount()):
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


    # 组件
    def slotInput(self):
        pass

    def slotOutput(self):
        pass

    '''
        功能：
            新增按钮槽函数
    '''

    def slotAdd(self):
        if self.tw_result.rowCount() <= 2 + len(self.result):
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
                deleteDataByContractOrderId(self.result[rowCount - 2][0])
                self.tw_result.removeRow(rowCount)
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
                workSheet.write_merge(2, 1 + len(dataList), 0, 0, self.selectedYear, contentStyle)
                for i in range(len(dataList)):
                    workSheet.write(2 + i, 1, str(dataList[i][0]) + '年', contentStyle)
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = OrderManagement()
    widget.show()
    sys.exit(app.exec_())
