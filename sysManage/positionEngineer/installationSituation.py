import base64
import pickle

from PyQt5.QtCore import Qt, QDate, QDateTime
from database.positionEngneerSql import *
from sysManage.showInputResult import showInputResult
from sysManage.userInfo import get_value
from widgets.positionEngineer.posEngneerInstallationUI import PosEngneerInstallationUI
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidget, QHeaderView, QTableWidgetItem, QComboBox, \
    QMessageBox, QFileDialog, QDateEdit, QCheckBox


class InstallationSituation(QWidget, PosEngneerInstallationUI):
    def __init__(self, parent=None):
        super(InstallationSituation, self).__init__(parent)
        self.setupUi(self)
        self.startInfo = None
        self.infoDict = {}
        self.baseNames = []
        self.inputList = []
        self.showInputResult = showInputResult(self)
        self.showInputResult.hide()
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
        self.pb_output.clicked.connect(self.slotOutput)
        self.tb_add.clicked.connect(self.slotAdd)
        self.tb_del.clicked.connect(self.slotDelete)
        self.tw_result.itemChanged.connect(self.slotAlterAndSava)
        self.tb_outputToExcel.clicked.connect(self.slotOutputToExcel)
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

        if len(self.le_designation.text()) > 0:
            if len(self.designation) == 0:
                self.designation.append(self.le_designation.text())
            else:
                self.designation[0] = self.le_designation.text()

        if len(self.le_positionCode.text()) > 0:
            if len(self.positionCode) == 0:
                self.positionCode.append(self.le_positionCode.text())
            else:
                self.positionCode[0] = self.le_positionCode.text()

        if len(self.cb_prepare.currentText()) > 0:
            if len(self.prepare) == 0:
                self.prepare.append(self.cb_prepare.currentText())
            else:
                self.prepare[0] = self.cb_prepare.currentText()

        print(self.base, self.designation,self.positionCode,self.prepare)
        self.displayData()

    '''
        功能：
            将列表数据展示在表中
    '''

    def displayData(self):
        self.tw_result.itemChanged.disconnect(self.slotAlterAndSava)
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
                item = QTableWidgetItem(str(i + 1))
                item.setFlags(Qt.ItemIsEnabled)
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 0, item)

                item = QTableWidgetItem(getUnitNameById(dataList[i][1]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
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
                    comboBox.addItems(['是'])

                else:
                    comboBox = QComboBox()
                    comboBox.addItems(['否'])
                comboBox.setEnabled(False)
                self.tw_result.setCellWidget(3 + i, 5, comboBox)

                item = QTableWidgetItem(dataList[i][6])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 6, item)

                item = QTableWidgetItem(dataList[i][7])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.tw_result.setItem(3 + i, 7, item)
                # parsedDateList = date.split('-')
                # dataEdit = QDateEdit()
                # dataEdit.setDisplayFormat("yyyy-MM-dd")
                # dataEdit.setDate(QDate(int(parsedDateList[0]), int(parsedDateList[1]), int(parsedDateList[2])))
                # self.tw_result.setCellWidget(3 + i, 7, dataEdit)

                date = dataList[i][8]
                item = QTableWidgetItem(dataList[i][8])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.tw_result.setItem(3 + i, 8, item)
                # parsedDateList = date.split('-')
                # dataEdit = QDateEdit()
                # dataEdit.setDisplayFormat("yyyy-MM-dd")
                # dataEdit.setDate(QDate(int(parsedDateList[0]), int(parsedDateList[1]), int(parsedDateList[2])))
                # self.tw_result.setCellWidget(3 + i, 8, dataEdit)


                item = QTableWidgetItem(str(dataList[i][9]))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 9, item)

                if dataList[i][10] == '已到位':
                    comboBox = QComboBox()
                    comboBox.addItems(['已到位'])
                else:
                    comboBox = QComboBox()
                    comboBox.addItems(['未到位'])
                comboBox.setEnabled(False)
                self.tw_result.setCellWidget(3 + i, 10, comboBox)

                item = QTableWidgetItem(dataList[i][11])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 11, item)

                item = QTableWidgetItem(dataList[i][12])
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                self.tw_result.setItem(3 + i, 12, item)
        self.tw_result.itemChanged.connect(self.slotAlterAndSava)

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
            elif i == 7 or i == 8:
                item = self.tw_result.cellWidget(row, i)
                if item != None:
                    date = item.date().toString(Qt.ISODate)
                    rowData.append(date)
            else:
                item = self.tw_result.item(row, i)
                if item != None:
                    if i == 12:
                        rowData.append(item.text())
                    if i == 1:
                        if getUnitIdbyName(item.text()) != None:
                            rowData.append(getUnitIdbyName(item.text()))
                        else:
                            QMessageBox.warning(self, "注意", "该基地名称尚未加入基地目录！", QMessageBox.Yes, QMessageBox.Yes)
                            break
                    else:
                        if len(item.text()) > 0:
                            rowData.append(item.text())
                        else:
                            break
                else:
                    break
        if len(rowData) < self.tw_result.columnCount() - 1:
            return False
        else:
            insertOneDataIntInstallation(rowData)
            self.currentLastRow = -1
            QMessageBox.warning(self, "注意", "插入成功！", QMessageBox.Yes, QMessageBox.Yes)
            self.displayData()

    def alterRowData(self, row):
        print("修改一行数据")
        rowData = []
        rowData.append(self.result[row - 3][0])
        for i in range(2,self.tw_result.columnCount()):
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
            else:
                item = self.tw_result.item(row, i)
                if item != None:
                    if i == 12:
                        rowData.append(item.text())
                    else:
                        if len(item.text()) > 0:
                            rowData.append(item.text())
                        else:
                            break
                else:
                    break
        print(rowData)
        if len(rowData) < self.tw_result.columnCount() - 2:
            return False
        else:
            if (updataOneDataIntInstallation(rowData) == True):
                QMessageBox.warning(self, "修改成功", "修改成功！", QMessageBox.Yes, QMessageBox.Yes)
            else:
                QMessageBox.warning(self, "警告", "插入失败！", QMessageBox.Yes, QMessageBox.Yes)
            self.displayData()

    def slotCancelInputIntoDatabase(self):
        self.showInputResult.hide()
        self.setDisabled(False)
        self.displayData()

    def slotInputIntoDatabase(self):
        for i, lineInfo in enumerate(self.inputList):
            if i == 0:
                continue
            try:
                #(6, '4', '2', '2', '2', 1, '3', '2000-01-01', '2000-01-01', 3, '已到位', '2', '2')
                if insertOneDataIntInstallation(lineInfo[1:]):
                    pass
            except Exception as e:
                print(e)
                QMessageBox.warning(self, "导入失败", "导入第%d数据失败！" % (i), QMessageBox.Yes)

        self.showInputResult.hide()
        self.setDisabled(False)
        self.displayData()
    # 组件
    def slotInput(self):
        self.inputList = []
        filename, _ = QFileDialog.getOpenFileName(self, "选中文件", '', "Excel Files (*.nms);;Excel Files (*.nms)")
        if len(filename) < 2:
            return
        try:
            with open(filename, "rb") as file:
                self.inputList = pickle.load(file)
                if self.inputList[0] != '防护安装情况':
                    raise Exception("数据格式错误！")
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "加载文件失败！", "请检查文件格式及内容格式！", QMessageBox.Yes)
            return

        self.showInputResult.setWindowTitle("导入数据")
        self.showInputResult.show()
        title = ['基地','番号','阵地代号','具体位置','是否具备安装最新型装备条件','目前安装情况','安装时间','计划安装时间','数量（套）','装备到位情况','装备运行情况','备注']
        # QTableWidget设置整行选中
        self.showInputResult.tw_result.setColumnCount(len(title))
        self.showInputResult.tw_result.setHorizontalHeaderLabels(title)
        self.showInputResult.tw_result.setRowCount(len(self.inputList) - 1)
        for i, LineInfo in enumerate(self.inputList):
            if i == 0:
                continue
            i = i - 1
            item = QTableWidgetItem(getUnitNameById(LineInfo[1]))
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
            if LineInfo[5] == 1:
                item = QTableWidgetItem('是')
            else:
                item = QTableWidgetItem('否')
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 4, item)

            item = QTableWidgetItem(LineInfo[6])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 5, item)
            item = QTableWidgetItem(LineInfo[7])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 6, item)
            item = QTableWidgetItem(LineInfo[8])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 7, item)
            item = QTableWidgetItem(str(LineInfo[9]))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 8, item)
            item = QTableWidgetItem(LineInfo[10])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 9, item)
            item = QTableWidgetItem(LineInfo[11])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 10, item)
            item = QTableWidgetItem(LineInfo[12])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 11, item)



    def slotOutput(self):
        if len(self.result) < 1:
            reply = QMessageBox.warning(self, '警告', '未选中任何数据，无法导出', QMessageBox.Yes)
            return
        reply = QMessageBox.question(self, '导出数据包', '是否保存修改并导出数据包？', QMessageBox.Cancel, QMessageBox.Yes)
        if reply == QMessageBox.Cancel:
            self.displayData()
            return
        self.displayData()
        directoryPath = QFileDialog.getExistingDirectory(self, "请选择导出文件夹", "c:/")
        if len(directoryPath) > 0:
            # 填表数据
            dataList = self.result
            if dataList is None or len(dataList) == 0:
                return
            else:
                dataList.insert(0,'防护安装情况')
                print(dataList)
                date = QDateTime.currentDateTime()
                installData = date.toString("yyyy年MM月dd日hh时mm分ss秒")  # hh:mm:ss
                pathName = "%s/%s阵地工程x生化防护装备安装情况.nms" % (directoryPath,installData)
                with open(pathName, "wb") as file:
                    pickle.dump(dataList, file)
                QMessageBox.about(self, "导出成功", "导出数据包成功！")



    '''
        功能：
            新增按钮槽函数
    '''

    def slotAdd(self):
        if self.tw_result.rowCount() <= 3 + len(self.result):
            self.tw_result.itemChanged.disconnect(self.slotAlterAndSava)
            rowCount = self.tw_result.rowCount()
            self.currentLastRow = rowCount
            self.tw_result.insertRow(rowCount)

            if (rowCount + 1 == 4):
                item = QTableWidgetItem('1')
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.tw_result.setItem(3, 0, item)
            else:
                lastNo = int(self.tw_result.item(rowCount - 1, 0).text())
                item = QTableWidgetItem(str(lastNo + 1))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.tw_result.setItem(rowCount, 0, item)


            comboBox = QComboBox()
            comboBox.addItems(self.baseNames)
            self.tw_result.setCellWidget(rowCount, 1, comboBox)
            comboBox = QComboBox()
            comboBox.addItems(['是', '否'])
            self.tw_result.setCellWidget(rowCount, 5, comboBox)
            comboBox = QComboBox()
            comboBox.addItems(['已到位', '未到位'])
            self.tw_result.setCellWidget(rowCount, 10, comboBox)

            installDate = QDateEdit()
            installDate.setDisplayFormat("yyyy-MM-dd")
            self.tw_result.setCellWidget(rowCount, 7, installDate)

            plenDate = QDateEdit()
            plenDate.setDisplayFormat("yyyy-MM-dd")
            self.tw_result.setCellWidget(rowCount, 8, plenDate)
            self.tw_result.itemChanged.connect(self.slotAlterAndSava)
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
            reply = QMessageBox.question(self, '警告', '是否删除该行数据？', QMessageBox.Cancel, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                deleteDataByInstallationId(self.result[rowCount - 3][0])
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

            workSheet.write_merge(0, 0, 0, 12, "阵地工程x生化防护装备安装情况",titileStyle)
            workSheet.write_merge(1, 2, 0, 0,'序号', titileStyle)
            workSheet.write_merge(1, 1, 1, 2, '单位', titileStyle)
            workSheet.write(2, 1, "基地", titileStyle)
            workSheet.write(2, 2, "番号", titileStyle)
            workSheet.write_merge(1, 2, 3, 3, '阵地代号', titileStyle)
            workSheet.write_merge(1, 2, 4, 4, '具体位置', titileStyle)
            workSheet.write_merge(1, 2, 5, 5, '是否具备安装新型装备条件', titileStyle)
            workSheet.write_merge(1, 1, 6, 10, '安装情况', titileStyle)
            workSheet.write(2, 6, "目前安装情况", titileStyle)
            workSheet.write(2, 7, "安装时间", titileStyle)
            workSheet.write(2, 8, "计划安装时间", titileStyle)
            workSheet.write(2, 9, "数量（套）", titileStyle)
            workSheet.write(2, 10, "装备到位情况", titileStyle)
            workSheet.write_merge(1, 2, 11, 11, '装备运行状态', titileStyle)
            workSheet.write_merge(1, 2, 12, 12, '备注', titileStyle)

            #填表数据
            dataList = self.result
            if dataList is None or len(dataList) == 0:
                return
            else:
                for i in range(len(dataList)):
                    workSheet.write(3 + i, 0, str(dataList[i][0]), contentStyle)
                    workSheet.write(3 + i, 1, getUnitNameById(dataList[i][1]), contentStyle)
                    workSheet.write(3 + i, 2, dataList[i][2], contentStyle)
                    workSheet.write(3 + i, 3, dataList[i][3], contentStyle)
                    workSheet.write(3 + i, 4, dataList[i][4], contentStyle)
                    if dataList[i][5] == 1:
                        workSheet.write(3 + i, 5, '是', contentStyle)
                    else:
                        workSheet.write(3 + i, 5, '否', contentStyle)
                    workSheet.write(3 + i, 6, dataList[i][6], contentStyle)
                    workSheet.write(3 + i, 7, dataList[i][7], contentStyle)
                    workSheet.write(3 + i, 8, dataList[i][8], contentStyle)
                    workSheet.write(3 + i, 9, dataList[i][9], contentStyle)
                    workSheet.write(3 + i, 10, dataList[i][10], contentStyle)
                    workSheet.write(3 + i, 11, dataList[i][11], contentStyle)
                    workSheet.write(3 + i, 12, dataList[i][12], contentStyle)

            try:
                pathName = "%s/阵地工程x生化防护装备安装情况.xls" % (directoryPath)
                workBook.save(pathName)
                import win32api
                win32api.ShellExecute(0, 'open', pathName, '', '', 1)
                QMessageBox.about(self, "导出成功", "导出成功！")
                return
            except Exception as e:
                QMessageBox.about(self, "导出失败", "导出表格被占用，请关闭正在使用的Execl！")
                return

if __name__ == "__main__":
    arr = ['1dads','2','3',[2]]
    with open("test.nms","wb") as file:
        pickle.dump(arr,file)

    with open("test.nms","rb") as file:
        arr1 = pickle.load(file)
    print(arr1)

