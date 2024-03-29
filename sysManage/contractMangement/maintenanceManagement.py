import pickle
import sys

from PyQt5.QtCore import Qt, QStringListModel, QDate, QDateTime
from PyQt5.QtWidgets import QApplication, QWidget, QHeaderView, QTableWidgetItem, QMessageBox, QFileDialog, QPushButton, \
    QDateEdit, QAbstractItemView

from database.contractManagementSql import *
from sysManage.component import getMessageBox, getIntInputDialog
from sysManage.contractMangement.AttachmentDialog import AttachmentDialog
from sysManage.showInputResult import showInputResult
from sysManage.userInfo import get_value
from widgets.contractMangement.OrderManagementUI import OrderManagementUI


class MaintenanceManagement(QWidget, OrderManagementUI):
    def __init__(self, parent=None):
        super(MaintenanceManagement, self).__init__(parent)
        self.setupUi(self)
        self.selectedYear = ''
        self.contractName = ''
        self.contractNo = ''
        self.attachmentDialog = None
        self.inputList = []
        self.shutdown = True
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
        self.yearList = getYearsFromContractMaintenance()
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
            if isHaveContractMaintenanceYear(str(year)):
                getMessageBox("新增", "该年份已经存在，拒绝添加！", True, False)
                return
            else:
                insertSuccess = addContractMaintanceYear(year)
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
        self.contractName = self.le_contractName.text()
        self.contractNo =  self.le_contractNo.text()
        self.displayData()

    '''
        功能：
            将列表数据展示在表中
    '''

    def displayData(self):
        self.tw_result.itemChanged.disconnect(self.slotAlterAndSava)
        self.result = getResultFromContractMaintenance(self.selectedYear, self.contractNo, self.contractName)
        self.tw_result.clear()
        self.tw_result.setColumnCount(13)
        self.currentLastRow = 0
        dataList = self.result
        if dataList is None or len(dataList) == 0:
            self.tw_result.setRowCount(2)
            self.initTableHeader()
            self.tb_del.setDisabled(True)
            self.tb_outputToExcel.setDisabled(True)
        else:
            self.tb_del.setDisabled(False)
            self.tb_outputToExcel.setDisabled(False)

            self.tw_result.setRowCount(2 + len(dataList))
            self.initTableHeader()
            item = QTableWidgetItem(self.selectedYear + '年')
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(2, 0, item)
            self.tw_result.setSpan(2, 0, len(dataList),1)
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
                dataEdit.dateChanged.connect(self.slotAlterAndSava)
                self.tw_result.setCellWidget(2 + i, 9, dataEdit)

                date = dataList[i][10]
                parsedDateList = date.split('-')
                dataEdit = QDateEdit()
                dataEdit.setDisplayFormat("yyyy-MM-dd")
                dataEdit.setDate(QDate(int(parsedDateList[0]), int(parsedDateList[1]), int(parsedDateList[2])))
                dataEdit.dateChanged.connect(self.slotAlterAndSava)
                self.tw_result.setCellWidget(2 + i, 10, dataEdit)

                item = QTableWidgetItem(dataList[i][11])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.tw_result.setItem(2 + i, 11, item)
                ##未完
                pushButton = QPushButton("附件信息")
                pushButton.clicked.connect(self.soltDisplayAttachment)
                self.tw_result.setCellWidget(2 + i,12, pushButton)


        self.tw_result.itemChanged.connect(self.slotAlterAndSava)

    def soltDisplayAttachment(self):
        rowCount = self.tw_result.currentRow()
        if len(self.result) < 1:
            return
        maintenanceId = self.result[rowCount - 2][0]
        self.attachmentDialog = AttachmentDialog()
        self.attachmentDialog.initTableWidget(maintenanceId,self.selectedYear)
        self.attachmentDialog.show()



        pass

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
        item = QTableWidgetItem("维修保障--合同")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(0, 0, item)
        self.tw_result.setSpan(0, 0, 1, 13)

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

        item = QTableWidgetItem("签订时间")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 9, item)

        item = QTableWidgetItem("交付时间")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 10, item)

        item = QTableWidgetItem("备注")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 11, item)

        item = QTableWidgetItem("附件")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 12, item)

    '''
        功能：
            新增一行的数据
    '''

    def slotAlterAndSava(self):
        selectRow = self.tw_result.selectedItems()
        if self.shutdown:
            return
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
                            getMessageBox("注意", "请输入整数！", True, False)
                            item1.setText('')
                        try:
                            unit = float(item0.text())
                        except:
                            getMessageBox("注意", "请输入正确的数字！", True, False)
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
        else:
            currentRow = self.tw_result.currentIndex().row()
            print(currentRow)
            if currentRow == self.currentLastRow:
                self.savaRowData(currentRow)
            elif currentRow == -1:
                return
            else:
                self.alterRowData(currentRow)


    def savaRowData(self, row):
        rowData = []
        rowData.append(self.selectedYear)
        for i in range(1, self.tw_result.columnCount() - 1):
            if i == 9 or i == 10:
                item = self.tw_result.cellWidget(row, i)
                if item != None:
                    date = item.date().toString(Qt.ISODate)
                    rowData.append(date)
                else:
                    break
            elif i == 2:
                item = self.tw_result.item(row, i)
                if (item != None):
                    if (len(item.text()) > 0):
                        if checkedNo(item.text()):
                            rowData.append(item.text())
                        else:
                            getMessageBox("注意", "合同编号重复，请检查合同是否重复！", True, False)
                            return
                else:
                    break
            else:
                if i == 1:
                    continue
                item = self.tw_result.item(row, i)
                if (item != None):
                    if (len(item.text()) > 0):
                        rowData.append(item.text())
                else:
                    break

        if len(rowData) == self.tw_result.columnCount() - 2:
            if(insertOneDataInToContractMaintenance(rowData) == True):
                getMessageBox("注意", "插入成功！", True, False)
            else:
                getMessageBox("警告", "插入失败！", True, False)
            self.displayData()

    def alterRowData(self, row):
        rowData = []
        rowData.append(self.result[row - 2][0])
        rowData.append(self.selectedYear)
        for i in range(2, self.tw_result.columnCount() - 1):
            if i == 9 or i == 10:
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
            if (updataOneDataToContractMaintenance(rowData) == True):
                getMessageBox("注意", "修改成功！", True, False)
            else:
                getMessageBox("警告", "修改失败！", True, False)
            self.displayData()

    '''
        功能：
            新增按钮槽函数
    '''

    def slotAdd(self):
        self.shutdown = True
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

            deliveryDate = QDateEdit()
            deliveryDate.setDisplayFormat("yyyy-MM-dd")
            self.tw_result.setCellWidget(rowCount, 9, deliveryDate)

            deliveryDate = QDateEdit()
            deliveryDate.setDisplayFormat("yyyy-MM-dd")
            self.tw_result.setCellWidget(rowCount, 10, deliveryDate)

            pushButton = QPushButton("附件信息")
            pushButton.clicked.connect(self.soltDisplayAttachment)
            self.tw_result.setCellWidget(rowCount, 12, pushButton)

        else:
            getMessageBox("注意", "请先将数据补充完整！", True, False)
        self.shutdown = False

    def slotDelete(self):
        rowCount = self.tw_result.currentRow()
        resultCount = len(self.result)
        if rowCount < 2:
            getMessageBox("注意", "请选中有效单元格！", True, False)
        elif rowCount >= 2 and rowCount < 2 + resultCount:
            reply = getMessageBox('警告', '是否删除该行数据？', True, True)
            if reply == QMessageBox.Ok:
                deleteDataByContractMaintenance(self.result[rowCount - 2][0],self.selectedYear)
                self.tw_result.removeRow(rowCount)
            self.displayData()
        else:
            self.tw_result.removeRow(rowCount)


    #导出至Excel
    def slotOutputToExcel(self):
        if len(self.result) < 1:
            reply = getMessageBox('警告', '未选中任何数据，无法导出', True, False)
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
            workSheet.write(1, 9, "签订日期", titileStyle)
            workSheet.write(1, 10, "交付日期", titileStyle)
            workSheet.write(1, 11, "备注", titileStyle)


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
                    workSheet.write(2 + i, 11, dataList[i][11], contentStyle)

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
            dataList = []
            dataList.append("维修合同")
            for i, item in enumerate(self.result):
                attachInfo = getAttachmentInformation(item[0], item[1])
                if len(attachInfo) > 0:
                    attachInfo = attachInfo[0]
                else:
                    attachInfo = []
                print("attachInfo")
                print(attachInfo)
                saveInfo = []
                for i in range(1,len(item)):
                    saveInfo.append(item[i])
                attachUse = []
                if attachInfo != None and len(attachInfo) > 0:
                    attach = []
                    for j in range(1, len(attachInfo)):
                        attach.append(attachInfo[j])
                    attachUse.append(attach.copy())
                saveInfo.append(attachUse.copy())
                dataList.append(saveInfo.copy())
            print("维修合同")
            print(dataList)  #
            if dataList is None or len(dataList) == 1:
                return
            else:
                date = QDateTime.currentDateTime()
                installData = date.toString("yyyy年MM月dd日hh时mm分ss秒")  # hh:mm:ss
                pathName = "%s/%s%s年维修合同.nms" % (
                    directoryPath, installData, self.selectedYear)
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
                if self.inputList[0] != "维修合同":
                    raise Exception("数据格式错误！")
        except Exception as e:
            print(e)
            getMessageBox("加载文件失败！", "请检查文件格式及内容格式！", True, False)
            return
        headerlist = ['年度', '合同编号', '合同名称', '甲方', '乙方', '单价（万元）', '数量/单位', '金额（万元）', '签订时间', '交付时间', '备注']
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
            item = QTableWidgetItem(LineInfo[0])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 0, item)
            item = QTableWidgetItem(LineInfo[1])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 1, item)
            item = QTableWidgetItem(LineInfo[2])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 2, item)

            item = QTableWidgetItem(LineInfo[3])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 3, item)
            item = QTableWidgetItem(LineInfo[4])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 4, item)
            item = QTableWidgetItem(str(LineInfo[5]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 5, item)
            item = QTableWidgetItem(str(LineInfo[6]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 6, item)
            item = QTableWidgetItem(str(LineInfo[7]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 7, item)
            item = QTableWidgetItem(LineInfo[8])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 8, item)
            item = QTableWidgetItem(LineInfo[9])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 9, item)
            item = QTableWidgetItem(LineInfo[10])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 10, item)

    def slotCancelInputIntoDatabase(self):
        self.showInputResult.hide()
        self.setDisabled(False)

    def slotInputIntoDatabase(self):
        for i, lineInfo in enumerate(self.inputList):
            if i == 0:
                continue
            try:
                if inputOneDataIntoContractMaintenance(lineInfo):
                    pass
            except Exception as e:
                print(e)
                getMessageBox("导入失败", "导入第%d数据失败！" % (i), True, False)

        self.showInputResult.hide()
        self.setDisabled(False)
        self.displayData()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MaintenanceManagement()
    widget.show()
    sys.exit(app.exec_())
