import sys
from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
from PyQt5.QtGui import QColor, QBrush,QFont
from conda_verify import const

from database.serviceSupportSql import *
from widgets.serviceSupport.yearServiceSupport import Widget_ServiceSupport
from sysManage.userInfo import get_value

'''
    维修保障
'''
class yearServiceSupport(QDialog, Widget_ServiceSupport):
    def __init__(self, parent=None):
        super(yearServiceSupport,self).__init__(parent)
        self.setupUi(self)
        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}
        self.currentUnitDisturbPlanNum = {}
        self.unitDisturbPlanList = {}
        self.unitFlag = 0
        self.signalConnect()
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

        # 新增年份
        self.tb_add.clicked.connect(self.slotAddNewYear)
        # 删除年份
        self.tb_del.clicked.connect(self.slotDelYear)


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
        self.save_data.clicked.disconnect(self.saveContentOfserviceSupport)
        self.showAllYearData.clicked.disconnect(self.showAllYearServiceSupportData)
        # self.serviceSupportResult.itemChanged.disconnect(self.updateChangeDataOfServiceSupport)
        self.serviceSupportResult.itemChanged.disconnect(self.slotAlterAndSava)

        # 新增年份
        self.tb_add.clicked.disconnect(self.slotAddNewYear)
        # 删除年份
        self.tb_del.clicked.disconnect(self.slotDelYear)


    def slotClickedInqury(self):
        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}
        self.currentYear = self.lw_yearChoose.currentItem().text()



    '''
        功能：点击显示所有年份的维修保障计划数据
    '''
    def showAllYearServiceSupportData(self):
        self.initServiceSupportTitle()
        self.showContentOfServiceSupport()



    '''
        功能：新增年份
    '''
    def slotAddNewYear(self):
        year = 0
        year, ok = QInputDialog.getInt(self, "Get year", "year:", 0, 0, 100000, 1)
        if ok:
            haveYear = False
            allyear = selectYearListAboutServiceSupport()
            for yearInfo in allyear:
                if str(year) == yearInfo:
                    haveYear = True
            if haveYear == True:
                reply = QMessageBox.information(self, '添加', '添加失败，该年份已存在', QMessageBox.Yes)
                return

            insertIntoServiceSupportYear(year)
            self._initYearWidget_()
            return


    '''
        功能：删除年份
    '''
    def slotDelYear(self):
        reply = QMessageBox.question(self, "删除", "是否删除所选？", QMessageBox.Yes, QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            currentYear = self.lw_yearChoose.currentItem()
            # print("currentYear.text()",currentYear.text())
            deleteServiceSupportYear(currentYear.text())
            # deleteByYear(currentYear.text())
            self._initYearWidget_()


    '''
        功能：初始化显示所有年份
    '''
    def _initYearWidget_(self):
        self.yearList = []
        self.currentYear = None
        self.lw_yearChoose.clear()
        # self.yearList = ['全部']
        allYear = selectYearListAboutServiceSupport()
        # print(allYear)

        for year in allYear:
            self.yearList.append(year)

        for year in self.yearList:
            item = QListWidgetItem()
            item.setText(year)
            self.lw_yearChoose.addItem(item)

        self.initServiceSupportTitle()
        # self.setServiceSupportTitle()
        self.showContentOfServiceSupport()


    '''
        功能：初始化维修保障计划显示所有
    '''
    def initServiceSupportTitle(self):
        txt = "所有年度核化装备维修保障计划及预算明细表"
        # self.txt_serviceSupportYear.setFont(QFont("Microsoft YaHei"))
        self.txt_serviceSupportYear.setAlignment(Qt.AlignHCenter)
        self.txt_serviceSupportYear.setTextInteractionFlags(Qt.NoTextInteraction)
        self.txt_serviceSupportYear.setFontPointSize(18)
        self.txt_serviceSupportYear.setText(txt)


    '''
        功能：初始化维修保障计划表的表头
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
        功能：画表头,行数有2行
    '''
    def initTableHeader(self):
        self.serviceSupportResult.setRowCount(2)
        self.serviceSupportResult.setColumnCount(13)
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

        item = QTableWidgetItem("项目名称")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(0, 1, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.serviceSupportResult.setSpan(0, 1, 2, 1)

        item = QTableWidgetItem("计量单位")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(0, 2, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.serviceSupportResult.setSpan(0, 2, 2, 1)

        item = QTableWidgetItem("审核")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(0, 3, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.serviceSupportResult.setSpan(0, 3, 1, 3)

        item = QTableWidgetItem("单价")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(1, 3, item)
        item.setFlags(Qt.ItemIsEnabled)

        item = QTableWidgetItem("数量")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(1, 4, item)
        item.setFlags(Qt.ItemIsEnabled)

        item = QTableWidgetItem("金额")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(1, 5, item)
        item.setFlags(Qt.ItemIsEnabled)

        item = QTableWidgetItem("单位")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(0, 6, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.serviceSupportResult.setSpan(0, 6, 1, 2)

        item = QTableWidgetItem("分配（送修）")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(1, 6, item)
        item.setFlags(Qt.ItemIsEnabled)

        item = QTableWidgetItem("供货（承修）")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(1, 7, item)
        item.setFlags(Qt.ItemIsEnabled)

        item = QTableWidgetItem("计价挂账进度")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(0, 8, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.serviceSupportResult.setSpan(0, 8, 1, 3)

        # item = QTableWidgetItem("进度")
        # item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        # self.serviceSupportResult.setItem(1, 8, item)
        # item.setFlags(Qt.ItemIsEnabled)
        # self.serviceSupportResult.setSpan(1, 8, 1, 3)

        item = QTableWidgetItem("确定技术状态")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(1, 8, item)
        item.setFlags(Qt.ItemIsEnabled)

        item = QTableWidgetItem("签订合同")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(1, 9, item)
        item.setFlags(Qt.ItemIsEnabled)

        item = QTableWidgetItem("支付")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(1, 10, item)
        item.setFlags(Qt.ItemIsEnabled)

        item = QTableWidgetItem("年份/时间")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(0, 11, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.serviceSupportResult.setSpan(0, 11, 2, 1)

        item = QTableWidgetItem("备注")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.serviceSupportResult.setItem(0, 12, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.serviceSupportResult.setSpan(0, 12, 2, 1)



    '''
        功能：
           读取维修保障表数据并显示
    '''
    def showContentOfServiceSupport(self):
        self.serviceSupportResult.itemChanged.disconnect(self.slotAlterAndSava)
        self.initTableHeader()
        data = selectContentOfServiceSupport()
        self.currentLastRow = -1
        row = len(data)  # 取得记录个数，用于设置表格的行数
        vol = 13  # 取得字段数，用于设置表格的列数
        # print(row)
        # print(vol)
        self.serviceSupportResult.setRowCount(row+2)
        self.serviceSupportResult.setColumnCount(vol)

        for i in range(row):
            for j in range(vol):
                if j==1:
                    temp_data = data[i][j]  # 临时记录，不能直接插入表格
                    comboBox = QComboBox()
                    comboBox.addItems(['(一)装备大修', '(二)装备中修', '(三)维修器材购置', '(四)修理能力建设'])
                    self.serviceSupportResult.setCellWidget(i+2, 1, comboBox)
                    comboBox.setCurrentText(temp_data)
                if j==8 or j==9 or j==10:
                    temp_data = data[i][j]  # 临时记录，不能直接插入表格
                    comboBox = QComboBox()
                    comboBox.addItems(['不涉及', '是', '否'])
                    self.serviceSupportResult.setCellWidget(i+2, j, comboBox)
                    comboBox.setCurrentText(temp_data)
                else:
                    temp_data = data[i][j]  # 临时记录，不能直接插入表格
                    datas = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                    self.serviceSupportResult.setItem(i+2, j, datas)
        self.serviceSupportResult.itemChanged.connect(self.slotAlterAndSava)



    '''
        功能：
            读取相应年份的维修保障表数据并显示
    '''
    def showYearContentOfServiceSupport(self):
        currentYear = self.lw_yearChoose.currentItem()
        data = selectYearContentOfServiceSupport(currentYear.text())
        row = len(data)  # 取得记录个数，用于设置表格的行数
        vol = 13  # 取得字段数，用于设置表格的列数
        self.serviceSupportResult.setRowCount(row + 2)
        self.serviceSupportResult.setColumnCount(vol)

        for i in range(row):
            for j in range(vol):
                if j == 1:
                    temp_data = data[i][j]  # 临时记录，不能直接插入表格
                    comboBox = QComboBox()
                    comboBox.addItems(['(一)装备大修', '(二)装备中修', '(三)维修器材购置', '(四)修理能力建设'])
                    self.serviceSupportResult.setCellWidget(i + 2, 1, comboBox)
                    comboBox.setCurrentText(temp_data)
                if j == 8 or j == 9 or j == 10:
                    temp_data = data[i][j]  # 临时记录，不能直接插入表格
                    comboBox = QComboBox()
                    comboBox.addItems(['不涉及', '是', '否'])
                    self.serviceSupportResult.setCellWidget(i + 2, j, comboBox)
                    comboBox.setCurrentText(temp_data)
                else:
                    temp_data = data[i][j]  # 临时记录，不能直接插入表格
                    datas = QTableWidgetItem(str(temp_data))  # 转换后可插入表格
                    self.serviceSupportResult.setItem(i + 2, j, datas)



    '''
        功能：新增一行的数据
    '''
    def slotAlterAndSava(self):
        selectRow = self.serviceSupportResult.selectedItems()
        if len(selectRow) != 0:
            currentRow = selectRow[0].row()
            currentColumn = selectRow[0].column()
            if (currentColumn == 3 or currentColumn == 4 and currentRow >= 2):
                item0 = self.serviceSupportResult.item(currentRow, 3)
                item1 = self.serviceSupportResult.item(currentRow, 4)
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
                        # print("amount")
                        # print(amount)
                        if (amount != 0):
                            item = self.serviceSupportResult.item(currentRow, 5)
                            if (item != None):
                                item.setText(str(amount))
                                item.setFlags(Qt.ItemIsEnabled)
                            else:
                                item = QTableWidgetItem(str(amount))
                                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                                item.setFlags(Qt.ItemIsEnabled)
                                self.serviceSupportResult.setItem(currentRow, 5, item)
                        self.serviceSupportResult.itemChanged.connect(self.slotAlterAndSava)
            if currentRow == self.currentLastRow:
                self.savaRowData(currentRow)
            else:
                self.alterRowData(currentRow)

    #保存一行数据
    def savaRowData(self, row):
        rowData = []
        for i in range(0, self.serviceSupportResult.columnCount()):
            if i == 1 or i == 8 or i == 9 or i == 10:
                item = self.serviceSupportResult.cellWidget(row, i).currentText()
                rowData.append(item)
            elif i == 12:
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

    #修改一行数据
    def alterRowData(self, row):
        rowData = []
        for i in range(self.serviceSupportResult.columnCount()):
            if i == 1 or i == 8 or i == 9 or i == 10:
                item = self.serviceSupportResult.cellWidget(row, i).currentText()
                if item != None:
                    rowData.append(item)
                else:
                    return
            elif i == 12:
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
        pass

    # 组件
    def slotInput(self):
        pass

    def slotOutput(self):
        pass



    '''
        功能：新增按钮槽函数
    '''
    def slotAdd(self):
        rowCount = self.serviceSupportResult.rowCount()
        # print(rowCount)
        if self.serviceSupportResult.rowCount() <= 2 + rowCount:
            self.currentLastRow = rowCount
            self.serviceSupportResult.insertRow(rowCount)

            if rowCount <= 2:
                currentRowNum = 1
                item = QTableWidgetItem(str(currentRowNum))
                self.serviceSupportResult.setItem(rowCount, 0, item)
            else:
                # 设置新增一行的序号为上一行序号+1
                LastRowNum = self.serviceSupportResult.item(rowCount - 1, 0).text()
                # print(type(LastRowNum))
                # print(LastRowNum)
                currentRowNum = int(LastRowNum) + 1
                # print(type(currentRowNum))
                # print(currentRowNum)
                item = QTableWidgetItem(str(currentRowNum))
                self.serviceSupportResult.setItem(rowCount, 0, item)

            comboBox = QComboBox()
            comboBox.addItems(['(一)装备大修', '(二)装备中修', '(三)维修器材购置', '(四)修理能力建设'])
            self.serviceSupportResult.setCellWidget(rowCount, 1, comboBox)

            comboBox = QComboBox()
            comboBox.addItems(['不涉及', '是', '否'])
            self.serviceSupportResult.setCellWidget(rowCount, 8, comboBox)
            comboBox = QComboBox()
            comboBox.addItems(['不涉及', '是', '否'])
            self.serviceSupportResult.setCellWidget(rowCount, 9, comboBox)
            comboBox = QComboBox()
            comboBox.addItems(['不涉及', '是', '否'])
            self.serviceSupportResult.setCellWidget(rowCount, 10, comboBox)

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
            self.serviceSupportResult.setItem(rowCount, 11, item)
            item = QTableWidgetItem("")
            self.serviceSupportResult.setItem(rowCount, 12, item)

        else:
            QMessageBox.warning(self, "注意", "请先将数据补充完整！", QMessageBox.Yes, QMessageBox.Yes)

    def slotDelete(self):
        rowCount = self.serviceSupportResult.currentRow()
        # print(rowCount)
        if rowCount < 2:
            QMessageBox.warning(self, "注意", "请选中有效单元格！", QMessageBox.Yes, QMessageBox.Yes)
            return
        elif rowCount >= 2:
            item = self.serviceSupportResult.item(rowCount, 0)
            deleteDataByServiceSupportNum(item.text())
            self.serviceSupportResult.removeRow(rowCount)





if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = yearServiceSupport()
    widget.show()
    sys.exit(app.exec_())