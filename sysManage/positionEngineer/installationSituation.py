from PyQt5.QtCore import Qt
from database.positionEngneerSql import *
from sysManage.userInfo import get_value
from widgets.positionEngineer.posEngneerInstallationUI import PosEngneerInstallationUI
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidget, QHeaderView, QTableWidgetItem, QComboBox, \
    QMessageBox


class InstallationSituation(QWidget, PosEngneerInstallationUI):
    def __init__(self, parent=None):
        super(InstallationSituation, self).__init__(parent)
        self.setupUi(self)
        self.startInfo = None
        self.infoDict = {}
        self.baseNames = []
        self.signalConnection()
        self.init()

    result = []
    base = []
    designation = []
    positionCode = []
    prepare = []
    currentLastRow = 0

    # 信号和槽连接
    def signalConnection(self):
        self.pb_select.clicked.connect(self.slotSelect)
        self.tb_input.clicked.connect(self.slotInput)
        self.tb_output.clicked.connect(self.slotOutput)
        self.tb_add.clicked.connect(self.slotAdd)
        self.tb_del.clicked.connect(self.slotDelete)
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

        stack = []
        if self.startInfo:
            stack.append(self.startInfo)
            self.initUnitComboxs(stack)

        self.displayData()
        pass

    '''
                功能：
                    单位目录的初始化，显示整个单位表
                    参数表：root为上级单位名字，mother为上级节点对象
    '''

    def initUnitComboxs(self, stack):
        self.cb_base.clear()
        unitId = stack.pop()
        bases = findBases(unitId[0])
        self.baseNames = []
        for base in bases:
            unitName = getUnitNameByIdInUnit(base)
            self.infoDict[unitName] = base
            self.baseNames.append(unitName)
        self.cb_base.addItems(self.baseNames)

    '''
        功能：
            根据下拉列表框以及文本框的内容，筛选数据。
    '''

    def slotSelect(self):
        self.base = []
        self.designation = []
        self.positionCode = []
        self.prepare = []

        self.base = self.cb_base.getCheckItem()
        # 更新对应基地名字的id
        for i in range(len(self.base)):
            self.base[i] = getUnitIdbyName(self.base[i])

        if len(self.le_designation.text()) > 1:
            if len(self.designation) == 0:
                self.designation.append(self.le_designation.text())
            else:
                self.designation[0] = self.le_designation.text()

        if len(self.le_positionCode.text()) > 1:
            if len(self.positionCode) == 0:
                self.positionCode.append(self.le_positionCode.text())
            else:
                self.positionCode[0] = self.le_positionCode.text()

        if len(self.cb_prepare.currentText()) > 1:
            if len(self.prepare) == 0:
                self.prepare.append(self.cb_prepare.currentText())
            else:
                self.prepare[0] = self.cb_prepare.currentText()

        self.displayData()

    '''
        功能：
            将列表数据展示在表中
    '''

    def displayData(self):
        self.result = getResult(self.base, self.designation, self.positionCode, self.prepare)
        self.tw_result.clear()
        self.tw_result.setColumnCount(13)
        dataList = self.result
        if dataList is None or len(dataList) == 0:
            self.tw_result.setRowCount(3)
            self.initTableHeader()
        else:
            self.tw_result.setRowCount(3 + len(dataList))
            self.initTableHeader()
            for i in range(len(dataList)):
                item = QTableWidgetItem(str(dataList[i][0]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 0, item)

                item = QTableWidgetItem(getUnitNameById(dataList[i][1]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 1, item)

                item = QTableWidgetItem(dataList[i][2])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 2, item)

                item = QTableWidgetItem(dataList[i][3])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 3, item)

                item = QTableWidgetItem(dataList[i][4])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 4, item)

                if dataList[i][5] == 1:
                    comboBox = QComboBox()
                    comboBox.addItems(['是', '否'])

                else:
                    comboBox = QComboBox()
                    comboBox.addItems(['否', '是'])
                self.tw_result.setCellWidget(3 + i, 5, comboBox)

                item = QTableWidgetItem(dataList[i][6])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 6, item)

                item = QTableWidgetItem(dataList[i][7])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 7, item)

                item = QTableWidgetItem(dataList[i][8])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 8, item)

                item = QTableWidgetItem(str(dataList[i][9]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 9, item)

                if dataList[i][10] == '已到位':
                    comboBox = QComboBox()
                    comboBox.addItems(['已到位', '未到位'])
                else:
                    comboBox = QComboBox()
                    comboBox.addItems(['未到位', '已到位'])
                self.tw_result.setCellWidget(3 + i, 10, comboBox)

                item = QTableWidgetItem(dataList[i][11])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 11, item)

                item = QTableWidgetItem(dataList[i][12])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 12, item)

    pass

    '''
        功能：
            画表头,行数至少有3行
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
        item = QTableWidgetItem("阵地工程XXX防护装备安装情况")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(0, 0, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setSpan(0, 0, 1, 13)

        item = QTableWidgetItem("序号")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 0, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setSpan(1, 0, 2, 1)

        item = QTableWidgetItem("单位")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.tw_result.setItem(1, 1, item)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setSpan(1, 1, 1, 2)

        item = QTableWidgetItem("基地")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 1, item)

        item = QTableWidgetItem("番号")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 2, item)

        item = QTableWidgetItem("阵地代号")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 3, item)
        self.tw_result.setSpan(1, 3, 2, 1)

        item = QTableWidgetItem("具体位置")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 4, item)
        self.tw_result.setSpan(1, 4, 2, 1)

        item = QTableWidgetItem("是否具备安装新型装备条件")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 5, item)
        self.tw_result.setSpan(1, 5, 2, 1)

        item = QTableWidgetItem("安装情况")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 6, item)
        self.tw_result.setSpan(1, 6, 1, 5)

        item = QTableWidgetItem("目前安装情况")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 6, item)
        item = QTableWidgetItem("安装时间")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 7, item)
        item = QTableWidgetItem("计划安装时间")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 8, item)
        item = QTableWidgetItem("数量（套）")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 9, item)
        item = QTableWidgetItem("装备到位情况")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(2, 10, item)

        item = QTableWidgetItem("装备运行状态")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 11, item)
        self.tw_result.setSpan(1, 11, 2, 1)

        item = QTableWidgetItem("备注")
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        item.setFlags(Qt.ItemIsEnabled)
        self.tw_result.setItem(1, 12, item)
        self.tw_result.setSpan(1, 12, 2, 1)

    '''
        功能：
            新增一行的数据
    '''

    def slotAlterAndSava(self):
        selectRow = self.tw_result.selectedItems()
        if len(selectRow) != 0:
            currentRow = selectRow[0].row()
            if currentRow == self.currentLastRow:
                self.savaRowData(currentRow)
            else:
                self.alterRowData(currentRow)

    def savaRowData(self, row):
        # print('保存一行')
        rowData = []
        for i in range(1, self.tw_result.columnCount()):
            if i == 5:
                item = self.tw_result.cellWidget(row, i)
                if item.currentText() == '是':
                    rowData.append(1)
                else:
                    rowData.append(0)
            elif i == 10:
                item = self.tw_result.cellWidget(row, i)
                rowData.append(item.currentText())
            elif i == 1:
                item = self.tw_result.cellWidget(row, i)
                if item != None:
                    rowData.append(getUnitIdbyName(item.currentText()))
            else:
                item = self.tw_result.item(row, i)
                if item != None and len(item.text()) > 0:
                    rowData.append(item.text())
                else:
                    break
        if len(rowData) < self.tw_result.columnCount() - 1:
            return False
        else:
            insertOneDataIntInstallation(rowData)
            QMessageBox.warning(self, "注意", "插入成功！", QMessageBox.Yes, QMessageBox.Yes)
            self.displayData()

    def alterRowData(self, row):
        # print("修改一行数据")
        rowData = []
        for i in range(self.tw_result.columnCount()):
            if i == 5:
                item = self.tw_result.cellWidget(row, i)
                if item != None:
                    if item.currentText() == '是':
                        rowData.append(1)
                    else:
                        rowData.append(0)
                else:
                    return
            elif i == 10:
                item = self.tw_result.cellWidget(row, i)
                if item != None:
                    rowData.append(item.currentText())
                else:
                    return
            elif i == 1:
                item = self.tw_result.cellWidget(row, i)
                if item != None:
                    rowData.append(getUnitIdbyName(item.currentText()))
                else:
                    return

            else:
                item = self.tw_result.item(row, i)
                if item != None and len(item.text()) > 0:
                    if i == 1:
                        if getUnitIdbyName(item.text()) != None:
                            rowData.append(getUnitIdbyName(item.text()))
                        else:
                            QMessageBox.warning(self, "注意", "该基地名称尚未加入基地目录！", QMessageBox.Yes, QMessageBox.Yes)
                            break
                    else:
                        rowData.append(item.text())
                else:
                    break
        if len(rowData) < self.tw_result.columnCount():
            return False
        else:
            updataOneDataIntInstallation(rowData)
        pass

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
        if self.tw_result.rowCount() <= 3 + len(self.result):
            rowCount = self.tw_result.rowCount()
            self.currentLastRow = rowCount
            self.tw_result.insertRow(rowCount)
            comboBox = QComboBox()
            comboBox.addItems(self.baseNames)
            self.tw_result.setCellWidget(rowCount, 1, comboBox)
            comboBox = QComboBox()
            comboBox.addItems(['是', '否'])
            self.tw_result.setCellWidget(rowCount, 5, comboBox)
            comboBox = QComboBox()
            comboBox.addItems(['已到位', '未到位'])
            self.tw_result.setCellWidget(rowCount, 10, comboBox)
        else:
            QMessageBox.warning(self, "注意", "请先将数据补充完整！", QMessageBox.Yes, QMessageBox.Yes)

    def slotDelete(self):

        rowCount = self.tw_result.currentRow()
        if self.result == None:
            resultCount = 0
        else:
            resultCount = len(self.result)

        if rowCount < 3:
            QMessageBox.warning(self, "注意", "请选中有效单元格！", QMessageBox.Yes, QMessageBox.Yes)
        elif rowCount >= 3 and rowCount < 3 + resultCount:
            item = self.tw_result.item(rowCount, 0)
            if item != None and int(item.text()) > 0:
                deleteDataByInstallationId(item.text())
                self.tw_result.removeRow(rowCount)
        else:
            self.tw_result.removeRow(rowCount)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = InstallationSituation()
    widget.show()
    sys.exit(app.exec_())
