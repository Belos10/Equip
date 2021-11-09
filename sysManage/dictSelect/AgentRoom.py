import os
import pickle
import sys
import zipfile

from PyQt5 import QtCore
from PyQt5.QtCore import QStringListModel, Qt, QDateTime
from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog, QApplication, QHeaderView, QTableWidget, \
    QTableWidgetItem, QAbstractItemView, QCheckBox, QHBoxLayout

from database.agentRoomSql import getResultFromAgentRoom, deleteDataById, updateOneData, \
    insertOneDataAgentRoom
from sysManage.showInputResult import showInputResult
from widgets.dictSelect.agentRoomUI import AgentRoomUI



class AgentRoom(QWidget, AgentRoomUI):
    def __init__(self, parent=None):
        super(AgentRoom, self).__init__(parent)
        self.setupUi(self)
        self.currentLastRow = -1
        self.inputList = []
        self.showInputResult = showInputResult(self)
        self.showInputResult.hide()
        self.signalConnect()
        self.init()

    def signalConnect(self):
        self.pb_input.clicked.connect(self.soltInput)
        self.pb_output.clicked.connect(self.soltOutput)
        self.pb_search.clicked.connect(self.soltSearch)
        self.pb_delete.clicked.connect(self.slotDelete)
        self.pb_add.clicked.connect(self.soltAdd)
        self.tw_result.itemChanged.connect(self.slotAlterAndSava)
        self.showInputResult.pb_confirm.clicked.connect(self.slotInputIntoDatabase)
        self.showInputResult.pb_cancel.clicked.connect(self.slotCancelInputIntoDatabase)

    def init(self):
        self.pb_delete.setDisabled(False)
        self.tw_result.clear()
        self.result = []
        self.displayData()
    def displayData(self):
        self.tw_result.itemChanged.disconnect(self.slotAlterAndSava)
        agentRoomName = self.le_agentName.text()
        manufacturerName = self.le_manufacturer.text()
        self.result = getResultFromAgentRoom(agentRoomName,manufacturerName)
        self.tw_result.setColumnCount(6)
        if len(self.result) != 0:
            self.pb_output.setDisabled(False)
        self.tw_result.setRowCount(len(self.result))
        header = ['序号','代表室名称','厂家名称','军代表','军代表联系方式','行政区']
        self.tw_result.verticalHeader().setVisible(False)
        self.tw_result.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tw_result.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tw_result.resizeColumnsToContents()
        self.tw_result.resizeRowsToContents()
        self.tw_result.setHorizontalHeaderLabels(header)
        for i,info in enumerate(self.result):
            item = QTableWidgetItem(str(i + 1))
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tw_result.setItem(i,0,item)

            item = QTableWidgetItem(info[1])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            # item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tw_result.setItem(i, 1, item)

            item = QTableWidgetItem(info[2])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            # item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tw_result.setItem(i, 2, item)

            item = QTableWidgetItem(info[3])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            # item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tw_result.setItem(i, 3, item)

            item = QTableWidgetItem(info[4])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            # item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tw_result.setItem(i, 4, item)

            item = QTableWidgetItem(info[5])
            item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            # item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.tw_result.setItem(i, 5, item)
        self.tw_result.itemChanged.connect(self.slotAlterAndSava)

        if len(self.result) == 0:
            self.pb_output.setDisabled(True)
            self.pb_delete.setDisabled(True)
        else:
            self.pb_output.setDisabled(False)
            self.pb_delete.setDisabled(False)


    def soltSearch(self):
        self.init()

    def soltInput(self):
        self.inputList = []
        filename, _ = QFileDialog.getOpenFileName(self, "选中文件", '', "Excel Files (*.nms);;Excel Files (*.nms)")
        if len(filename) < 2:
            return
        try:
            with open(filename, "rb") as file:
                self.inputList = pickle.load(file)
                if self.inputList[0] != '代表室目录':
                    raise Exception("数据格式错误！")
        except Exception as e:
            print(e)
            QMessageBox.warning(self, "加载文件失败！", "请检查文件格式及内容格式！", QMessageBox.Yes)
            return

        self.showInputResult.setWindowTitle("导入数据")
        self.showInputResult.show()
        title = ['代表室名称', '厂家名称', '军代表', '军代表联系方式', '行政区']
        # QTableWidget设置整行选中
        self.showInputResult.tw_result.setColumnCount(len(title))
        self.showInputResult.tw_result.setHorizontalHeaderLabels(title)
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




    def soltOutput(self):
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
                dataList.insert(0,'代表室目录')
                print(dataList)
                date = QDateTime.currentDateTime()
                installData = date.toString("yyyy年MM月dd日hh时mm分ss秒")  # hh:mm:ss
                pathName = "%s/%s代表室目录.nms" % (directoryPath,installData)
                with open(pathName, "wb") as file:
                    pickle.dump(dataList, file)
                QMessageBox.about(self, "导出成功", "导出数据包成功！")
        pass

    def slotCancelInputIntoDatabase(self):
        self.showInputResult.hide()
        self.setDisabled(False)
        self.displayData()

    def slotInputIntoDatabase(self):
        for i, lineInfo in enumerate(self.inputList):
            if i == 0:
                continue
            try:
                if insertOneDataAgentRoom(lineInfo[1:]):
                    pass
            except Exception as e:
                print(e)
                QMessageBox.warning(self, "导入失败", "导入第%d数据失败！" % (i), QMessageBox.Yes)

        self.showInputResult.hide()
        self.setDisabled(False)
        self.displayData()



    def savaRowData(self, row):
        # print('保存一行')
        rowData = []
        for i in range(1, self.tw_result.columnCount()):
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
        if len(rowData) < self.tw_result.columnCount() - 1:
            return False
        else:
            if insertOneDataAgentRoom(rowData) == True:
                self.currentLastRow = -1
                QMessageBox.warning(self, "注意", "插入成功！", QMessageBox.Yes, QMessageBox.Yes)
            else:
                QMessageBox.warning(self, "注意", "插入失败！", QMessageBox.Yes, QMessageBox.Yes)
            self.init()

    def alterRowData(self, row):
        print("修改一行数据")
        rowData = []
        rowData.append(self.result[row][0])
        for i in range(1,self.tw_result.columnCount()):
            item = self.tw_result.item(row, i)
            if item != None:
                if i == 5:
                    rowData.append(item.text())
                else:
                    if len(item.text()) > 0:
                        rowData.append(item.text())
                    else:
                        break
            else:
                break
        print(rowData)
        if len(rowData) < self.tw_result.columnCount() - 1:
            return False
        else:
            if (updateOneData(rowData) == True):
                QMessageBox.warning(self, "修改成功", "修改成功！", QMessageBox.Yes, QMessageBox.Yes)
            else:
                QMessageBox.warning(self, "警告", "修改失败！", QMessageBox.Yes, QMessageBox.Yes)
            self.init()

    def soltAdd(self):
        if self.tw_result.rowCount() <= len(self.result):
            self.tw_result.itemChanged.disconnect(self.slotAlterAndSava)
            rowCount = self.tw_result.rowCount()
            self.currentLastRow = rowCount
            self.tw_result.insertRow(rowCount)

            if (rowCount + 1 == 1):
                item = QTableWidgetItem('1')
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.tw_result.setItem(0, 0, item)
            else:
                lastNo = int(self.tw_result.item(rowCount - 1, 0).text())
                item = QTableWidgetItem(str(lastNo + 1))
                item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item.setFlags(Qt.ItemIsEnabled)
                self.tw_result.setItem(rowCount, 0, item)
            self.tw_result.itemChanged.connect(self.slotAlterAndSava)
        else:
            QMessageBox.warning(self, "注意", "请先将数据补充完整！", QMessageBox.Yes, QMessageBox.Yes)

    def slotAlterAndSava(self):
        selectRow = self.tw_result.selectedItems()
        if len(selectRow) != 0:
            currentRow = selectRow[0].row()
            if currentRow == self.currentLastRow:
                self.savaRowData(currentRow)
            else:
                self.alterRowData(currentRow)

    def slotDelete(self):
        rowCount = self.tw_result.currentRow()
        if self.result == None:
            resultCount = 0
        else:
            resultCount = len(self.result)

        if rowCount < 0:
            QMessageBox.warning(self, "注意", "请选中有效单元格！", QMessageBox.Yes, QMessageBox.Yes)
        elif rowCount >= 0 and rowCount < resultCount:
            reply = QMessageBox.question(self, '警告', '是否删除该行数据？', QMessageBox.Cancel, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                deleteDataById(self.result[rowCount][0])
                self.tw_result.removeRow(rowCount)
            else:
                return

        else:
            self.tw_result.removeRow(rowCount)
        self.init()

