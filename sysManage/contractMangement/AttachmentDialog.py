from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QHeaderView, QTableWidgetItem, QMessageBox, QDateEdit
from sysManage.component import getMessageBox

from database.contractManagementSql import *
from widgets.contractMangement.attachmentDialogUI import AttachmentDialogUI


class AttachmentDialog(QDialog, AttachmentDialogUI):
    def __init__(self, parent=None):
        super(AttachmentDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon(":/pic/system.png"))
        self.resultList = []
        self.maintenanceId = -1
        self.currentLastRow = -1
        self.year = ''
        self.signalConnection()



    def signalConnection(self):
        self.pb_add.clicked.connect(self.soltAdd)
        self.pb_delete.clicked.connect(self.soltDelete)
        self.tw_result.itemChanged.connect(self.slotAlterAndSava)

    def initTableWidget(self, maintenanceId,year):
        self.maintenanceId = maintenanceId
        self.year = year
        self.resultList = getAttachmentInformation(maintenanceId,year)
        self.initHeader()
        if len(self.resultList) != 0:
            self.displayData()

    def initHeader(self):
        self.tw_result.setRowCount(2 + len(self.resultList))
        self.tw_result.setColumnCount(18)
        self.tw_result.verticalHeader().setVisible(False)
        self.tw_result.horizontalHeader().setVisible(False)
        # self.tw_result.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tw_result.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tw_result.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tw_result.resizeColumnsToContents()
        self.tw_result.resizeRowsToContents()
        # 绘制表头
        item = QTableWidgetItem("XX装备维修免税清单明细表")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(0, 0, item)
        self.tw_result.setSpan(0, 0, 1, 18)

        item = QTableWidgetItem("序号")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 0, item)

        item = QTableWidgetItem("合同号")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 1, item)

        item = QTableWidgetItem("合同名称")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 2, item)

        item = QTableWidgetItem("计划项目")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 3, item)

        item = QTableWidgetItem("预算金额")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 4, item)

        item = QTableWidgetItem("单价（万元）")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 5, item)

        item = QTableWidgetItem("数量/（单位）")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 6, item)

        item = QTableWidgetItem("预算（万元）")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 7, item)

        item = QTableWidgetItem("当年应付")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 8, item)

        item = QTableWidgetItem("签订日期")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 9, item)

        item = QTableWidgetItem("甲方单位")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 10, item)

        item = QTableWidgetItem("单位性质")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 11, item)

        item = QTableWidgetItem("纳税人识别号")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 12, item)

        item = QTableWidgetItem("乙方单位")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 13, item)

        item = QTableWidgetItem("付款单位")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 14, item)

        item = QTableWidgetItem("计划文件")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 15, item)

        item = QTableWidgetItem("交付日期")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 16, item)

        item = QTableWidgetItem("备注")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 17, item)


    def displayData(self):
        self.tw_result.itemChanged.disconnect(self.slotAlterAndSava)
        self.resultList = getAttachmentInformation(self.maintenanceId, self.year)
        for i in range(len(self.resultList)):
            item = QTableWidgetItem(str(self.resultList[i][1]))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(2 + i, 0, item)

            item = QTableWidgetItem(self.resultList[i][2]) #no
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            #item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(2 + i, 1, item)

            item = QTableWidgetItem(self.resultList[i][3]) #name
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            #item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(2 + i, 2, item)

            item = QTableWidgetItem(self.resultList[i][4])  # plan_project
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            #item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(2 + i, 3, item)

            item = QTableWidgetItem(str(self.resultList[i][5]))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            #item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(2 + i, 4, item)

            item = QTableWidgetItem(str(self.resultList[i][6]))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            #item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(2 + i, 5, item)

            item = QTableWidgetItem(str(self.resultList[i][7]))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            #item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(2 + i, 6, item)

            item = QTableWidgetItem(str(self.resultList[i][8]))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(2 + i, 7, item)

            item = QTableWidgetItem(str(self.resultList[i][9]))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            #item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(2 + i, 8, item)

            date = self.resultList[i][10]
            parsedDateList = date.split('-')
            dataEdit = QDateEdit()
            dataEdit.setDisplayFormat("yyyy-MM-dd")
            dataEdit.setDate(QDate(int(parsedDateList[0]), int(parsedDateList[1]), int(parsedDateList[2])))
            dataEdit.setEnabled(False)
            self.tw_result.setCellWidget(2 + i, 9, dataEdit)

            item = QTableWidgetItem(self.resultList[i][11])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            #item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(2 + i, 10, item)

            item = QTableWidgetItem(self.resultList[i][12])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            #item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(2 + i, 11, item)

            item = QTableWidgetItem(self.resultList[i][13])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            #item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(2 + i, 12, item)

            item = QTableWidgetItem(self.resultList[i][14])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            #item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(2 + i, 13, item)

            item = QTableWidgetItem(self.resultList[i][15])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            #item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(2 + i, 14, item)

            item = QTableWidgetItem(self.resultList[i][16])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            #item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(2 + i, 15, item)

            date = self.resultList[i][17]
            parsedDateList = date.split('-')
            dataEdit = QDateEdit()
            dataEdit.setDisplayFormat("yyyy-MM-dd")
            dataEdit.setDate(QDate(int(parsedDateList[0]),int(parsedDateList[1]),int(parsedDateList[2])))
            dataEdit.setEnabled(False)
            self.tw_result.setCellWidget(2 + i, 16, dataEdit)

            item = QTableWidgetItem(self.resultList[i][18])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            #item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(2 + i, 17, item)
        self.tw_result.itemChanged.connect(self.slotAlterAndSava)


    def slotAlterAndSava(self):
        selectRow = self.tw_result.selectedItems()
        if len(selectRow) != 0:
            currentRow = selectRow[0].row()
            currentColumn = selectRow[0].column()
            if (currentColumn == 8 or currentColumn == 4 or currentColumn == 5 or currentColumn == 6 and currentRow >= 2):
                item0 = self.tw_result.item(currentRow, 5)
                item1 = self.tw_result.item(currentRow, 6)
                item2 = self.tw_result.item(currentRow, 4)
                item3 = self.tw_result.item(currentRow, 8)
                if (item1 != None and item0 != None and item2 != None and item3 != None):
                    if (len(item0.text()) > 0 and len(item1.text()) > 0 and len(item2.text()) > 0 and len(item3.text()) > 0):
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
                            item0.setText('')
                            getMessageBox("注意", "请输入正确的数字！", True, False)

                        try:
                            float(item2.text())
                        except:
                            item2.setText('')
                            getMessageBox("注意", "请输入正确的数字！", True, False)

                        try:
                            float(item3.text())
                        except:
                            item3.setText('')
                            getMessageBox("注意", "请输入正确的数字！", True, False)

                        amount = round(count * unit, 6)
                        if (amount != 0):
                            item = self.tw_result.item(currentRow, 7)
                            if (item != None):
                                item.setText(str(amount))
                                item.setFlags(Qt.ItemIsEnabled)
                            else:
                                item = QTableWidgetItem(str(amount))
                                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                                item.setFlags(Qt.ItemIsEnabled)
                                self.tw_result.setItem(currentRow, 7, item)
                        self.tw_result.itemChanged.connect(self.slotAlterAndSava)

            if currentRow == self.currentLastRow:
                self.savaRowData(currentRow)
            else:
                self.alterRowData(currentRow)



    def savaRowData(self,row):
        rowData = []
        rowData.append(str(self.maintenanceId))
        for i in range(self.tw_result.columnCount()):
            if i == 9 or i == 16:
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
        rowData.append(self.year)
        if len(rowData) == self.tw_result.columnCount() + 2:
            if (insertOneDataInToContractAttachment(rowData) == True):
                getMessageBox("注意", "插入成功！", True, False)
                self.currentLastRow = -1
            else:
                getMessageBox("警告", "插入失败！", True, False)
            self.displayData()

    def alterRowData(self, row):
        rowData = [str(self.maintenanceId)]
        for i in range(self.tw_result.columnCount()):
            if i == 9 or i == 16:
                item = self.tw_result.cellWidget(row,i)
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
        rowData.append(self.year)
        if len(rowData) == self.tw_result.columnCount() + 2:
            if (updataOneDataToContractAttachment(rowData) == True):
                getMessageBox("注意", "修改成功！", True, False)
            else:
                getMessageBox("警告", "修改失败！", True, False)
            self.displayData()

    def soltAdd(self):
        if self.tw_result.rowCount() <= 2 + len(self.resultList):
            self.tw_result.itemChanged.disconnect(self.slotAlterAndSava)
            maintenceData = getContractMaintenanceInfoByMaintanceId(self.maintenanceId)
            rowCount = self.tw_result.rowCount()
            self.currentLastRow = rowCount
            self.tw_result.insertRow(rowCount)
            if (rowCount + 1 == 3):
                item = QTableWidgetItem('1')
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.tw_result.setItem(2, 0, item)
            else:
                lastNo = int(self.tw_result.item(rowCount - 1,0).text())
                item = QTableWidgetItem(str(lastNo + 1))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.tw_result.setItem(rowCount, 0, item)

            #合同号
            item = QTableWidgetItem(maintenceData[2])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(rowCount, 1, item)

            #合同名称
            item = QTableWidgetItem(maintenceData[3])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(rowCount, 2, item)

            #预算金额
            # 合同名称
            item = QTableWidgetItem("")
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(rowCount, 7, item)

            #签订日期
            date = maintenceData[9]
            parsedDateList = date.split('-')
            dataEdit = QDateEdit()
            dataEdit.setDisplayFormat("yyyy-MM-dd")
            dataEdit.setDate(QDate(int(parsedDateList[0]), int(parsedDateList[1]), int(parsedDateList[2])))
            dataEdit.setEnabled(False)
            self.tw_result.setCellWidget(rowCount, 9, dataEdit)

            #甲方
            item = QTableWidgetItem(maintenceData[4])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(rowCount, 10, item)

            # 乙方
            item = QTableWidgetItem(maintenceData[5])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(rowCount, 13, item)

            date = maintenceData[-2]
            parsedDateList = date.split('-')
            dataEdit = QDateEdit()
            dataEdit.setDisplayFormat("yyyy-MM-dd")
            dataEdit.setDate(QDate(int(parsedDateList[0]), int(parsedDateList[1]), int(parsedDateList[2])))
            dataEdit.setEnabled(False)
            self.tw_result.setCellWidget(rowCount, 16, dataEdit)

            item = QTableWidgetItem(maintenceData[-1])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(Qt.ItemIsEnabled)
            self.tw_result.setItem(rowCount, 17, item)

            self.tw_result.itemChanged.connect(self.slotAlterAndSava)
        else:
            getMessageBox("注意", "请先将数据补充完整！", True, False)






    def soltDelete(self):
        rowCount = self.tw_result.currentRow()
        resultCount = len(self.resultList)
        if rowCount < 2:
            getMessageBox("注意", "请选中有效单元格！", True, False)
        elif rowCount >= 2 and rowCount < 2 + resultCount:
            reply = getMessageBox('警告', '是否删除该行数据？', True, True)
            if reply == QMessageBox.Ok:
                print(self.resultList[rowCount - 2][0], self.resultList[rowCount - 2][1],self.year)
                deleteDataByContractAttachmentId(self.resultList[rowCount - 2][0], self.resultList[rowCount - 2][1],self.year)
                self.tw_result.removeRow(rowCount)
        else:
            self.tw_result.removeRow(rowCount)
