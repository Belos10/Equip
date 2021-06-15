from widgets.alocatMange.rocketTransfer import Widget_Rocket_Transfer
from PyQt5.Qt import Qt
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QListWidgetItem, QComboBox, QTableWidgetItem, QDateEdit, \
    QInputDialog, QMessageBox, QFileDialog
from database.alocatMangeSql import selectYearListAboutArmy, selectArmyTransferByYear, insertIntoArmyTransferYear, \
    insertIntoRocketTransferYear, selectYearListAboutRocket, selectRocketTransferByYear
from database.alocatMangeSql import selectYearListAboutDisturbPlan
from database.strengthDisturbSql import selectAllEndEquip
from sysManage.alocatMange.config import ArmyTransferReceiveUnit, ArmyTransferSendUnit

'''
   火箭军调拨单管理
'''
class rocketTransfer(QWidget, Widget_Rocket_Transfer):
    def __init__(self, parent=None):
        super(rocketTransfer, self).__init__(parent)
        self.setupUi(self)

        self.tw_result.horizontalHeader().setVisible(False)
        self.tw_result.verticalHeader().setVisible(False)

        self._initYearWidget_()
        self._initResultHeader_()

        self.signalConnect()

        self.currentResult = {}

    def signalConnect(self):
        self.lw_yearChoose.itemPressed.connect(self.slotSelectResult)
        self.pb_outputToExcel.clicked.connect(self.slotOutputToExcel)

    def _initYearWidget_(self):
        self.yearList = []
        self.currentYear = ''
        self.lw_yearChoose.clear()
        self.yearList = []
        allYear = selectYearListAboutDisturbPlan()
        # print(allYear)
        for year in allYear:
            self.yearList.append(year)

        for year in self.yearList:
            item = QListWidgetItem()
            item.setText(year)
            self.lw_yearChoose.addItem(item)

    def _initResultHeader_(self):
        self.orginRowCount = 0
        self.tw_result.clear()
        self.tw_result.setColumnCount(19)
        self.tw_result.setRowCount(2)
        item = QTableWidgetItem()
        item.setText('序号')
        self.tw_result.setItem(0, 0, item)
        item = QTableWidgetItem()
        item.setText('调拨单信息')
        self.tw_result.setItem(0, 1, item)
        item = QTableWidgetItem()
        item.setText('交装单位')
        self.tw_result.setItem(0, 8, item)
        item = QTableWidgetItem()
        item.setText('接装单位')
        self.tw_result.setItem(0, 11, item)
        item = QTableWidgetItem()
        item.setText('装备名称')
        self.tw_result.setItem(0, 14, item)
        item = QTableWidgetItem()
        item.setText('计量单位')
        self.tw_result.setItem(0, 15, item)
        item = QTableWidgetItem()
        item.setText('应发数')
        self.tw_result.setItem(0, 16, item)
        item = QTableWidgetItem()
        item.setText('备注')
        self.tw_result.setItem(0, 18, item)
        item = QTableWidgetItem()

        item.setText('调拨单号')
        self.tw_result.setItem(1, 1, item)
        item = QTableWidgetItem()
        item.setText('调拨日期')
        self.tw_result.setItem(1, 2, item)
        item = QTableWidgetItem()
        item.setText('调拨依据')
        self.tw_result.setItem(1, 3, item)
        item = QTableWidgetItem()
        item.setText('调拨')
        self.tw_result.setItem(1, 4, item)
        item = QTableWidgetItem()
        item.setText('调拨方式')
        self.tw_result.setItem(1, 5, item)
        item = QTableWidgetItem()
        item.setText('运输方式')
        self.tw_result.setItem(1, 6, item)
        item = QTableWidgetItem()
        item.setText('有效日期')
        self.tw_result.setItem(1, 7, item)
        item = QTableWidgetItem()
        item.setText('单位名称')
        self.tw_result.setItem(1, 8, item)
        item = QTableWidgetItem()
        item.setText('联系人')
        self.tw_result.setItem(1, 9, item)
        item = QTableWidgetItem()
        item.setText('联系电话')
        self.tw_result.setItem(1, 10, item)
        item = QTableWidgetItem()
        item.setText('单位名称')
        self.tw_result.setItem(1, 11, item)
        item = QTableWidgetItem()
        item.setText('联系人')
        self.tw_result.setItem(1, 12, item)
        item = QTableWidgetItem()
        item.setText('联系电话')
        self.tw_result.setItem(1, 13, item)
        item = QTableWidgetItem()
        item.setText('质量')
        self.tw_result.setItem(1, 16, item)
        item = QTableWidgetItem()
        item.setText('数量')
        self.tw_result.setItem(1, 17, item)

        self.tw_result.setSpan(0, 0, 2, 1)
        self.tw_result.setSpan(0, 1, 1, 7)
        self.tw_result.setSpan(0, 8, 1, 3)
        self.tw_result.setSpan(0, 11, 1, 3)
        self.tw_result.setSpan(0, 16, 1, 2)
        self.tw_result.setSpan(0, 14, 2, 1)
        self.tw_result.setSpan(0, 15, 2, 1)
        self.tw_result.setSpan(0, 18, 2, 1)
        self.tw_result.setColumnWidth(3, 250)
        self.tw_result.setColumnWidth(8, 250)
        self.tw_result.setColumnWidth(11, 250)
        self.equipTuple = selectAllEndEquip()

    def slotSelectResult(self):
        self.currentResult = {}
        self._initResultHeader_()
        row = self.lw_yearChoose.currentRow()
        self.currentYear = self.lw_yearChoose.item(row).text()
        resultList = selectRocketTransferByYear(self.currentYear)
        self.tw_result.setRowCount(len(resultList) + 2)

        for i, rocketTransferInfo in enumerate(resultList):
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[0])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tw_result.setItem(i + 2, 0, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[1])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tw_result.setItem(i + 2, 1, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[2])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tw_result.setItem(i + 2, 2, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[3])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tw_result.setItem(i + 2, 3, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[4])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tw_result.setItem(i + 2, 4, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[5])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tw_result.setItem(i + 2, 5, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[6])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tw_result.setItem(i + 2, 6, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[7])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tw_result.setItem(i + 2, 7, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[9])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tw_result.setItem(i + 2, 8, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[10])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tw_result.setItem(i + 2, 9, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[11])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tw_result.setItem(i + 2, 10, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[12])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tw_result.setItem(i + 2, 11, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[13])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tw_result.setItem(i + 2, 12, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[14])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tw_result.setItem(i + 2, 13, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[16])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tw_result.setItem(i + 2, 14, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[17])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tw_result.setItem(i + 2, 15, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[18])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tw_result.setItem(i + 2, 16, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[19])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tw_result.setItem(i + 2, 17, item)
            item = QTableWidgetItem()
            item.setText(rocketTransferInfo[20])
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.tw_result.setItem(i + 2, 18, item)
            self.currentResult[i] = rocketTransferInfo



    def slotOutputToExcel(self):
        if len(self.currentResult) < 1:
            reply = QMessageBox.warning(self, '警告', '未选中任何数据，无法导出', QMessageBox.Yes)
            return
        reply = QMessageBox.question(self, '修改导出Excel', '是否保存修改并导出Excel？', QMessageBox.Cancel, QMessageBox.Yes)
        if reply == QMessageBox.Cancel:
            return

        directoryPath = QFileDialog.getExistingDirectory(self, "请选择导出文件夹", "c:/")
        if len(directoryPath) > 0 and '.' not in directoryPath:
            import xlwt
            workBook = xlwt.Workbook(encoding='utf-8')
            workSheet = workBook.add_sheet('Sheet1')
            headTitleStyle2 = xlwt.XFStyle()  # 初始化样式
            font = xlwt.Font()  # 为样式创建字体
            font.name = '宋体'
            font.bold = True
            font.height = 20 * 11  # 字体大小，11为字号，20为衡量单位
            alignment = xlwt.Alignment()  ## Create Alignment
            alignment.horz = xlwt.Alignment.HORZ_RIGHT
            alignment.vert = xlwt.Alignment.VERT_CENTER
            borders = xlwt.Borders()
            borders.left = 1  # 设置为细实线
            borders.right = 1
            borders.top = 1
            borders.bottom = 1
            headTitleStyle2.font = font  # 设定样式
            headTitleStyle2.alignment = alignment
            headTitleStyle2.borders = borders

            headTitleStyle = xlwt.XFStyle()  # 初始化样式
            font = xlwt.Font()  # 为样式创建字体
            font.name = '黑体'
            font.bold = True
            font.height = 20 * 10  # 字体大小，11为字号，20为衡量单位
            alignment = xlwt.Alignment()  ## Create Alignment
            alignment.horz = xlwt.Alignment.HORZ_CENTER
            alignment.vert = xlwt.Alignment.VERT_CENTER
            borders = xlwt.Borders()
            borders.left = 2  # 设置为3细实线
            borders.right = 2
            borders.top = 2
            borders.bottom = 2
            headTitleStyle.font = font  # 设定样式
            headTitleStyle.alignment = alignment
            headTitleStyle.borders = borders

            titileStyle = xlwt.XFStyle()  # 初始化样式
            font = xlwt.Font()  # 为样式创建字体
            font.name = '宋体'
            font.bold = True
            font.height = 20 * 10  # 字体大小，11为字号，20为衡量单位
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

            for i in range(19):
                workSheet.col(i).width = 5500
            workSheet.write_merge(0, 1, 0, 0, '序号', headTitleStyle)
            workSheet.write_merge(0, 0, 1, 7, '调拨单信息', headTitleStyle)
            workSheet.write_merge(0, 0, 8, 10, '交装单位', headTitleStyle)
            workSheet.write_merge(0, 0, 11, 13, '接装单位', headTitleStyle)
            workSheet.write_merge(0, 1, 14, 14, '装备名称', headTitleStyle)
            workSheet.write_merge(0, 1, 15, 15, '计量单位', headTitleStyle)
            workSheet.write_merge(0, 0, 16, 17, '应发数', headTitleStyle)
            workSheet.write_merge(0, 1, 18, 18, '备注', headTitleStyle)
            workSheet.write(1, 1, '调拨单号', headTitleStyle)
            workSheet.write(1, 2, '调拨日期', headTitleStyle)
            workSheet.write(1, 3, '调拨依据', headTitleStyle)
            workSheet.write(1, 4, '调拨性质', headTitleStyle)
            workSheet.write(1, 5, '调拨方式', headTitleStyle)
            workSheet.write(1, 6, '运输方式', headTitleStyle)
            workSheet.write(1, 7, '有效日期', headTitleStyle)
            workSheet.write(1, 8, '单位名称', headTitleStyle)
            workSheet.write(1, 9, '联系人', headTitleStyle)
            workSheet.write(1, 10, '联系电话', headTitleStyle)
            workSheet.write(1, 11, '单位名称', headTitleStyle)
            workSheet.write(1, 12, '联系人', headTitleStyle)
            workSheet.write(1, 13, '联系电话', headTitleStyle)
            workSheet.write(1, 16, '质量', headTitleStyle)
            workSheet.write(1, 17, '数量', headTitleStyle)

            for key in self.currentResult.keys():
                rowList = self.currentResult[key]
                workSheet.write(key + 2, 0, rowList[0], contentStyle)
                workSheet.write(key + 2, 1, rowList[1], contentStyle)
                workSheet.write(key + 2, 2, rowList[2], contentStyle)
                workSheet.write(key + 2, 3, rowList[3], contentStyle)
                workSheet.write(key + 2, 4, rowList[4], contentStyle)
                workSheet.write(key + 2, 5, rowList[5], contentStyle)
                workSheet.write(key + 2, 6, rowList[6], contentStyle)
                workSheet.write(key + 2, 7, rowList[7], contentStyle)
                workSheet.write(key + 2, 8, rowList[9], contentStyle)
                workSheet.write(key + 2, 9, rowList[10], contentStyle)
                workSheet.write(key + 2, 10, rowList[11], contentStyle)
                workSheet.write(key + 2, 11, rowList[12], contentStyle)
                workSheet.write(key + 2, 12, rowList[13], contentStyle)
                workSheet.write(key + 2, 13, rowList[14], contentStyle)
                workSheet.write(key + 2, 14, rowList[16], contentStyle)
                workSheet.write(key + 2, 15, rowList[17], contentStyle)
                workSheet.write(key + 2, 16, rowList[18], contentStyle)
                workSheet.write(key + 2, 17, rowList[19], contentStyle)
                workSheet.write(key + 2, 18, rowList[20], contentStyle)

            try:
                pathName = "%s/%s年火箭军调拨单.xls" % (directoryPath, self.currentYear)
                workBook.save(pathName)
                import win32api
                win32api.ShellExecute(0, 'open', pathName, '', '', 1)
                QMessageBox.about(self, "导出成功", "导出成功！")
                return
            except Exception as e:
                QMessageBox.about(self, "导出失败", "导出表格被占用，请关闭正在使用的Execl！")
                return
        else:
            QMessageBox.about(self, "选取文件夹失败！", "请选择正确的文件夹！")
        pass
        pass

