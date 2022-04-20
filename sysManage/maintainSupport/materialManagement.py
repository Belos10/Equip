import sys
from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
from PyQt5.QtGui import QColor, QBrush,QFont


from database.serviceSupportSql import *
from widgets.serviceSupport.serviceSupportUI import Widget_ServiceSupport
from sysManage.userInfo import get_value

from database.serviceSupportSql import selectContentOfMaterialManagement
from widgets.serviceSupport.materialManagementUI import materialManagementUI

'''
    维修保障计划
'''
class materialManagement(QWidget, materialManagementUI):
    def __init__(self, parent=None):
        super(materialManagement, self).__init__(parent)
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
        self.tw_result.clear()
        self.initTableHeader()
        self.showContentOfMaterialManagement()


    '''
        功能：信号与槽连接
    '''
    def signalConnect(self):
        self.tb_add.clicked.connect(self.slotAdd)
        self.tb_del.clicked.connect(self.slotDelete)
        self.tw_result.itemChanged.connect(self.slotAlterAndSava)
        # self.tb_outputToExcel.clicked.connect(self.slotOutputToExcel)


    '''
        功能：信号与槽连接的断开
    '''
    def signalDisconnectSlot(self):
        self.tb_add.clicked.disconnect(self.slotAdd)
        self.tb_del.clicked.disconnect(self.slotDelete)
        self.tw_result.itemChanged.disconnect(self.slotAlterAndSava)
        # self.tb_outputToExcel.clicked.disconnect(self.slotOutputToExcel)

    def slotClickedInqury(self):
        self.first_treeWidget_dict = {}
        self.second_treeWidget_dict = {}
        self.currentYear = self.lw_yearChoose.currentItem().text()


    '''
        功能：画表头,行数有2行
    '''
    def initTableHeader(self):
        self.tw_result.setRowCount(3)
        self.tw_result.setColumnCount(12)
        self.tw_result.verticalHeader().setVisible(False)
        self.tw_result.horizontalHeader().setVisible(False)
        self.tw_result.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tw_result.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tw_result.resizeColumnsToContents()
        self.tw_result.resizeRowsToContents()

        # 绘制表头
        item = QTableWidgetItem("本级库存物资总账")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFont(QFont('微软雅黑', 12, QFont.Black))
        self.tw_result.setItem(0, 0, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setSpan(0, 0, 1, 12)

        item = QTableWidgetItem("序号")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 0, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setSpan(1, 0, 2, 1)

        item = QTableWidgetItem("凭证号")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 1, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setSpan(1, 1, 2, 1)

        item = QTableWidgetItem("资产名称")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 2, item)
        self.tw_result.setSpan(1, 2, 2, 1)

        item = QTableWidgetItem("合同号")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 3, item)
        self.tw_result.setSpan(1, 3, 2, 1)

        item = QTableWidgetItem("结算时间")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 4, item)
        self.tw_result.setSpan(1, 4, 2, 1)

        item = QTableWidgetItem("合同情况")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 5, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setSpan(1, 5, 1, 3)

        item = QTableWidgetItem("数量")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 5, item)

        item = QTableWidgetItem("合同单价")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 6, item)

        item = QTableWidgetItem("金额")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 7, item)

        item = QTableWidgetItem("财务计价核算数量和金额")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 8, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setSpan(1, 8, 1, 2)

        item = QTableWidgetItem("数量")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 8, item)

        item = QTableWidgetItem("金额")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 9, item)

        item = QTableWidgetItem("备注")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 10, item)
        self.tw_result.setSpan(1, 10, 2, 1)

        item = QTableWidgetItem("调拨情况")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 11, item)
        self.tw_result.setSpan(1, 11, 2, 1)


    '''
        功能：
           读取维修保障表数据并显示
    '''
    def showContentOfMaterialManagement(self):
        self.tw_result.itemChanged.disconnect(self.slotAlterAndSava)
        self.initTableHeader()
        data = selectContentOfMaterialManagement()
        # print("data:", data)
        self.currentLastRow = -1
        row = len(data)  # 取得记录个数，用于设置表格的行数
        vol = 12  # 取得字段数，用于设置表格的列数
        self.tw_result.setRowCount(row + 3)
        self.tw_result.setColumnCount(vol)
        self.datadict = {}

        for i in range(row):
            self.datadict[str(i+1)] = data[i]
        print(self.datadict)

        for i in range(row):
            for j in range(vol):
                if j == 0:
                    datadictKeysValue = list(self.datadict.keys())
                    # print(datadictKeysValue)
                    temp_data = datadictKeysValue[i]
                    datas = QTableWidgetItem(str(temp_data))
                    self.tw_result.setItem(i + 3, j, datas)
                    datas.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                else:
                    temp_data = data[i][j]
                    datas = QTableWidgetItem(str(temp_data))
                    self.tw_result.setItem(i + 3, j, datas)
                    datas.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.tw_result.itemChanged.connect(self.slotAlterAndSava)


    '''
        功能：新增一行的数据
    '''
    def slotAlterAndSava(self):
        selectRow = self.tw_result.selectedItems()
        if len(selectRow) != 0:
            currentRow = selectRow[0].row()
            if currentRow == self.currentLastRow:
                self.savaRowData(currentRow)
            else:
                self.alterRowData(currentRow)

    #保存一行数据
    def savaRowData(self, row):
        rowData = []
        for i in range(0, self.tw_result.columnCount()):
            item = self.tw_result.item(row, i)
            if item != None and len(item.text()) > 0:
                rowData.append(item.text())
            else:
                break
        if len(rowData) != self.tw_result.columnCount():
            return False
        else:
            insertContentOfMaterialManagement(rowData)
            QMessageBox.warning(self, "注意", "插入成功！", QMessageBox.Yes, QMessageBox.Yes)
            self.showContentOfMaterialManagement()


    #修改一行数据
    def alterRowData(self, row):
        rowData = []
        for i in range(self.tw_result.columnCount()):       # tw_result.columnCount()=12
            item = self.tw_result.item(row, i)
            rowData.append(item.text())

        if len(rowData) != self.tw_result.columnCount():
            return False
        else:
            QMessageBox.warning(self, "注意", "修改成功！", QMessageBox.Yes, QMessageBox.Yes)
            updateContentOfMaterialManagement(rowData)
            self.showContentOfMaterialManagement()
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
        rowCount = self.tw_result.rowCount()
        dataCount = len(self.datadict)
        numList = []
        for i in range(dataCount):
            temp_data = self.datadict[str(i+1)][0]
            numList.append(int(temp_data))

        if numList == []:
            self.bl = 1
        else:
            self.bl = int(max(numList)) + 1

        if self.tw_result.rowCount() <= 3 + rowCount:
            self.currentLastRow = rowCount
            self.tw_result.insertRow(rowCount)

            # 设置新增一行的序号为上一行序号+1
            if rowCount <= 3:
                currentRowNum = 1
                item = QTableWidgetItem(str(currentRowNum))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(rowCount, 0, item)
            else:
                LastRowNum = self.tw_result.item(rowCount - 1, 0).text()
                currentRowNum = int(LastRowNum) + 1
                item = QTableWidgetItem(str(currentRowNum))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(rowCount, 0, item)
        else:
            QMessageBox.warning(self, "注意", "请先将数据补充完整！", QMessageBox.Yes, QMessageBox.Yes)
            return


    '''
        功能： “删除计划” 按钮槽函数
    '''
    def slotDelete(self):
        rowCount = self.tw_result.currentRow()
        # print("rowCount000:", rowCount)
        if rowCount < 3:
            QMessageBox.warning(self, "注意", "请选中有效单元格！", QMessageBox.Yes, QMessageBox.Yes)
            return
        elif rowCount >= 3:
            # item = self.serviceSupportResult.item(rowCount, 0)
            #应该删除的是字典datadict中的 key = item.text()的值的第一个数据 对应的数据库中的值
            if self.datadict == {}:
                self.tw_result.removeRow(rowCount)
            else:
                currentRow = self.tw_result.currentRow()
                # print("currentRow:", currentRow)
                currentRowNum = currentRow -2
                # print("currentRowNum:", currentRowNum)
                currentRowNumKeyValue = self.datadict[str(currentRowNum)][0]
                # print("currentRowNumKeyValue:", currentRowNumKeyValue)
                deleteDataByMaterialManagementNum(int(currentRowNumKeyValue))
                self.tw_result.removeRow(rowCount)
                self.showContentOfMaterialManagement()



#删除一行数据之后，如果再新增一行数据，序号为前一行加1，则读入的时候是读入的当前的序号值，
# 如果序号值与数据库中已经存在的逐渐num重复了，则插入不进去，应该有一个唯一标识，每次点击新增的时候就加1，使存入数据库的num值一直保持增加，但是如果程序关闭了，该值又得刷新

    # '''
    # 功能：导出至Excel
    # '''
    # def slotOutputToExcel(self):
    #     currentRowCount = self.tw_result.rowCount()
    #     currentColumnCount = 14
    #     dataExcelList = []
    #     for i in range(2, currentRowCount):            #从（行2，列0）开始读数据
    #         dataRowList = []
    #         for j in range(currentColumnCount):
    #             item = self.tw_result.item(i, j)
    #             dataRowList.append(item.text())
    #
    #         dataExcelList.append(dataRowList)
    #     # print("dataExcelList:", dataExcelList)
    #
    #     if len(dataExcelList) < 1:
    #         reply = QMessageBox.warning(self, '警告', '没有任何数据，无法导出', QMessageBox.Yes)
    #         return
    #     reply = QMessageBox.question(self, '将内容导出Excel', '是否保存数据并导出至Excel？', QMessageBox.Cancel, QMessageBox.Yes)
    #
    #     if reply == QMessageBox.Cancel:
    #         return
    #
    #     directoryPath = QFileDialog.getExistingDirectory(self, "请选择导出文件夹", "c:/")
    #     if len(directoryPath) > 0:
    #         import xlwt
    #         workBook = xlwt.Workbook(encoding='utf-8')
    #         workSheet = workBook.add_sheet('Sheet1')
    #         titileStyle = xlwt.XFStyle()  # 初始化样式
    #         font = xlwt.Font()  # 为样式创建字体
    #         font.name = '宋体'
    #         font.bold = True
    #         font.height = 20 * 11  # 字体大小，11为字号，20为衡量单位
    #         alignment = xlwt.Alignment()  ## Create Alignment
    #         alignment.horz = xlwt.Alignment.HORZ_CENTER
    #         alignment.vert = xlwt.Alignment.VERT_CENTER
    #         borders = xlwt.Borders()
    #         borders.left = 2  # 设置为细实线
    #         borders.right = 2
    #         borders.top = 2
    #         borders.bottom = 2
    #         titileStyle.font = font  # 设定样式
    #         titileStyle.alignment = alignment
    #         titileStyle.borders = borders
    #         for i in range(14):
    #             workSheet.col(i).width = 5000
    #         contentStyle = xlwt.XFStyle()  # 初始化样式
    #         font = xlwt.Font()  # 为样式创建字体
    #         font.name = '宋体'
    #         font.height = 20 * 11  # 字体大小，11为字号，20为衡量单位
    #         alignment = xlwt.Alignment()  ## Create Alignment
    #         alignment.horz = xlwt.Alignment.HORZ_CENTER
    #         alignment.vert = xlwt.Alignment.VERT_CENTER
    #         borders = xlwt.Borders()
    #         borders.left = 1  # 设置为细实线
    #         borders.right = 1
    #         borders.top = 1
    #         borders.bottom = 1
    #         contentStyle.font = font  # 设定样式
    #         contentStyle.alignment = alignment
    #         contentStyle.borders = borders
    #
    #         workSheet.write_merge(0, 0, 0, 11, "本级库存物资总账", titileStyle)
    #         workSheet.write_merge(1, 2, 0, 0,'序号', titileStyle)
    #         workSheet.write_merge(1, 2, 1, 1, '凭证号', titileStyle)
    #         workSheet.write_merge(1, 2, 2, 2, '资产名称', titileStyle)
    #         workSheet.write_merge(1, 2, 3, 3, '合同号', titileStyle)
    #         workSheet.write_merge(1, 1, 4, 6, '结算时间', titileStyle)
    #         workSheet.write(2, 4, "单价", titileStyle)
    #         workSheet.write(2, 5, "数量", titileStyle)
    #         workSheet.write(2, 6, "金额", titileStyle)
    #         workSheet.write_merge(1, 1, 7, 8, '单位', titileStyle)
    #         workSheet.write(2, 7, "分配（送修）", titileStyle)
    #         workSheet.write(2, 8, "供货（承修）", titileStyle)
    #         workSheet.write_merge(1, 1, 9, 11, '计价挂账进度', titileStyle)
    #         workSheet.write(2, 9, "确定技术状态", titileStyle)
    #         workSheet.write(2, 10, "签订合同", titileStyle)
    #         workSheet.write(2, 11, "支付", titileStyle)
    #         workSheet.write_merge(1, 2, 12, 12, '年份/时间', titileStyle)
    #         workSheet.write_merge(1, 2, 13, 13, '备注', titileStyle)
    #
    #         #填表数据
    #         if dataExcelList is None or len(dataExcelList) == 0:
    #             self.serviceSupportResult.setRowCount(3)
    #             self.initTableHeader()
    #         else:
    #             for i in range(len(dataExcelList)):
    #                 workSheet.write(3 + i, 0, dataExcelList[i][0], contentStyle)
    #                 workSheet.write(3 + i, 1, dataExcelList[i][1], contentStyle)
    #                 workSheet.write(3 + i, 2, dataExcelList[i][2], contentStyle)
    #                 workSheet.write(3 + i, 3, dataExcelList[i][3], contentStyle)
    #                 workSheet.write(3 + i, 4, dataExcelList[i][4], contentStyle)
    #                 workSheet.write(3 + i, 5, dataExcelList[i][5], contentStyle)
    #                 workSheet.write(3 + i, 6, dataExcelList[i][6], contentStyle)
    #                 workSheet.write(3 + i, 7, dataExcelList[i][7], contentStyle)
    #                 workSheet.write(3 + i, 8, dataExcelList[i][8], contentStyle)
    #                 workSheet.write(3 + i, 9, dataExcelList[i][9], contentStyle)
    #                 workSheet.write(3 + i, 10, dataExcelList[i][10], contentStyle)
    #                 workSheet.write(3 + i, 11, dataExcelList[i][11], contentStyle)
    #                 workSheet.write(3 + i, 12, dataExcelList[i][12], contentStyle)
    #                 workSheet.write(3 + i, 13, dataExcelList[i][13], contentStyle)
    #         try:
    #             pathName = "%s/核化装备维修保障计划及预算明细表.xls" % (directoryPath)
    #             workBook.save(pathName)
    #             import win32api
    #             win32api.ShellExecute(0, 'open', pathName, '', '', 1)
    #             QMessageBox.about(self, "导出成功", "导出成功！")
    #             return
    #         except Exception as e:
    #             QMessageBox.about(self, "导出失败", "导出表格被占用，请关闭正在使用的Execl！")
    #             return




if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = materialManagement()
    widget.show()
    sys.exit(app.exec_())