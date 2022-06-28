import pickle

from PyQt5.QtCore import Qt, QDateTime

from database.agentRoomSql import getResultByAgentId
from sysManage.showInputResult import showInputResult
from widgets.dictSelect.factorySet import Widget_Factory_Set
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidgetItem, QHeaderView, QAbstractItemView, \
    QMessageBox, QFileDialog
from PyQt5.Qt import QRegExp, QRegExpValidator
from database.dictSelect.factorySetSql import *
from sysManage.component import getMessageBox

#new
regx = QRegExp("[0-9]*")
class factorySet(QWidget, Widget_Factory_Set):
    def __init__(self, parent=None):
        super(factorySet, self).__init__(parent)
        self.setupUi(self)
        self.result = []
        self.agentRoomDate = []
        self.inputList = []
        self.showInputResult = showInputResult(self)
        self.showInputResult.hide()
        self.tw_result.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tw_result.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tw_result.setSelectionMode(QAbstractItemView.SingleSelection)
        self.signalConnect()
        validator = QRegExpValidator(regx)
        self.le_tel1.setValidator(validator)
        self.le_tel2.setValidator(validator)
        self.le_tel2.setEnabled(False)
        self.le_represent.setEnabled(False)


    def initWidget(self):
        self.le_name.clear()
        self.le_id.clear()
        self.le_address.clear()
        self.le_tel1.clear()
        self.le_connect.clear()
        self.le_represent.clear()
        self.le_tel2.clear()
        self.tw_result.clear()
        self.cb_agentRoom.clear()
        self.agentRoomDate.clear()
        self.agentRoomDate.append([-1,''])
        self.agentRoomDate.extend(getAgentRoomComboxDate())
        for item in self.agentRoomDate:
            self.cb_agentRoom.addItem(item[1],item[0])
        self.initTableWidget()

    def initTableWidget(self):
        title = ["厂家编号", '厂家名字', '厂家地址','厂家联系人', '厂家联系方式', '代表室','军代表', '军代表联系方式']
        self.tw_result.setColumnCount(len(title))
        self.tw_result.setHorizontalHeaderLabels(title)
        self.result = selectAllDataAboutFactory()
        if self.result:
            self.tw_result.setRowCount(len(self.result))
            for i, resultInfo in enumerate(self.result):
                item = QTableWidgetItem(resultInfo[0])
                self.tw_result.setItem(i, 0, item)
                item = QTableWidgetItem(resultInfo[1])
                self.tw_result.setItem(i, 1, item)
                item = QTableWidgetItem(resultInfo[2])
                self.tw_result.setItem(i, 2, item)
                item = QTableWidgetItem(resultInfo[3])
                self.tw_result.setItem(i, 3, item)
                item = QTableWidgetItem(resultInfo[4])
                self.tw_result.setItem(i, 4, item)
                item = QTableWidgetItem(resultInfo[5])
                self.tw_result.setItem(i, 5, item)
                item = QTableWidgetItem(resultInfo[6])
                self.tw_result.setItem(i, 6, item)
                item = QTableWidgetItem(resultInfo[7])
                self.tw_result.setItem(i, 7, item)
        else:
            self.tw_result.setRowCount(0)

    def signalConnect(self):
        self.tw_result.clicked.connect(self.slotClickedTableWidget)
        self.pb_add.clicked.connect(self.slotAddFactoryInfo)
        self.pb_update.clicked.connect(self.slotUpdateFactoryInfo)
        self.pb_del.clicked.connect(self.slotDelFactoryInfo)
        self.cb_agentRoom.currentIndexChanged.connect(self.ajustContext)
        self.pb_input.clicked.connect(self.soltInput)
        self.pb_output.clicked.connect(self.soltOutput)
        self.showInputResult.pb_confirm.clicked.connect(self.slotInputIntoDatabase)
        self.showInputResult.pb_cancel.clicked.connect(self.slotCancelInputIntoDatabase)

    # 新增厂家
    def slotAddFactoryInfo(self):
        if haveFactoryID(self.le_id.text()) == True:
            getMessageBox("新增", "新增失败，该厂家编号已存在", True, False)
            return
        else:
            ID = self.le_id.text()
            name = self.le_name.text()
            agentRoomId = self.cb_agentRoom.currentData()
            if name == "":
                getMessageBox("新增", "新增失败，厂家名字不能为空", True, False)
                return
            if haveFactoryName(name) == True:
                getMessageBox("新增", "新增失败，厂家名字不能重复", True, False)
                return
            if agentRoomId == -1:
                getMessageBox("新增", "新增失败，代表室不能为空！", True, False)
                return
            address = self.le_address.text()
            connect = self.le_connect.text()
            tel1 = self.le_tel1.text()

            addSuccess = addInfoIntoFactory(ID, name, address, connect, tel1,agentRoomId)
            if addSuccess == True:
                getMessageBox("新增", "新增成功", True, False)
                self.initTableWidget()
                return
            else:
                getMessageBox("新增", str(addSuccess) + ",新增失败", True, False)
                return

    # 修改厂家
    def slotUpdateFactoryInfo(self):
        if self.tw_result.currentRow() < 0:
            return
        else:
            row = self.tw_result.currentRow()
            if self.tw_result.item(row, 0):
                if self.tw_result.item(row, 0).text() != self.le_id.text():
                    getMessageBox("修改", "修改失败, 厂家编号不可修改", True, False)
                    return
            ID = self.le_id.text()
            name = self.le_name.text()
            if name != self.tw_result.item(row, 1).text():
                getMessageBox("修改", "修改失败，厂家名字不能修改", True, False)
                return
            address = self.le_address.text()
            connect = self.le_connect.text()
            tel1 = self.le_tel1.text()
            agentRoomId = self.cb_agentRoom.currentData()
            if agentRoomId == -1:
                getMessageBox("修改", "修改失败，代表室不能为空", True, False)
                return


            addSuccess = updateInfoIntoFactory(ID, name, address, connect, tel1, agentRoomId)
            if addSuccess == True:
                getMessageBox("修改", "修改成功", True, False)
                self.initTableWidget()
                return
            else:
                getMessageBox("修改", str(addSuccess) + ",修改失败", True, False)
                return
    # 删除厂家
    def slotDelFactoryInfo(self):
        if self.tw_result.currentRow() < 0:
            return
        else:
            #row = self.tw_result.currentRow()
            ID = self.le_id.text()
            addSuccess = delInfoFromFactory(ID)
            if addSuccess == True:
                getMessageBox("删除", "删除成功", True, False)
                self.initTableWidget()
                self.le_id.clear()
                self.le_represent.clear()
                self.le_tel2.clear()
                self.le_address.clear()
                self.le_connect.clear()
                self.cb_agentRoom.setCurrentIndex(0)
                self.le_tel1.clear()
                self.le_name.clear()
                return
            else:
                getMessageBox("删除", str(addSuccess) + ",删除失败", True, False)
                return

    def slotClickedTableWidget(self):
        row = self.tw_result.currentRow()
        if row < 0:
            return
        else:
            id = self.tw_result.item(row, 0).text()
            name = self.tw_result.item(row, 1).text()
            address = self.tw_result.item(row, 2).text()
            connect = self.tw_result.item(row, 3).text()
            tel1 = self.tw_result.item(row, 4).text()

            self.le_id.setText(id)
            self.le_name.setText(name)
            self.le_address.setText(address)
            self.le_connect.setText(connect)
            self.le_tel1.setText(tel1)
            rowDate = self.result[row]
            for i in range(len(self.agentRoomDate)):
                if self.agentRoomDate[i][0] == rowDate[8]:
                    self.cb_agentRoom.setCurrentIndex(i)
                    self.le_represent.setText(self.agentRoomDate[i][2])
                    self.le_tel2.setText(self.agentRoomDate[i][3])
                    break

    def ajustContext(self,index):
        agentRoomId = self.cb_agentRoom.currentData()
        if agentRoomId == -1 or len(self.agentRoomDate) == 1:
            self.le_represent.clear()
            self.le_tel2.clear()
        else:
            self.le_represent.setText(self.agentRoomDate[index][2])
            self.le_tel2.setText(self.agentRoomDate[index][3])
        pass

    def soltInput(self):
        self.inputList = []
        filename, _ = QFileDialog.getOpenFileName(self, "选中文件", '', "Excel Files (*.nms);;Excel Files (*.nms)")
        if len(filename) < 2:
            return
        try:
            with open(filename, "rb") as file:
                self.inputList = pickle.load(file)
                if self.inputList[0] != '厂家目录':
                    raise Exception("数据格式错误！")
        except Exception as e:
            print(e)
            getMessageBox("加载文件失败！", "请检查文件格式及内容格式！", True, False)
            return

        self.showInputResult.setWindowTitle("导入数据")
        self.showInputResult.show()
        title = ['厂家编号', '厂家名称', '厂家地址', '厂家联系人', '厂家联系方式', '代表室', '军代表', '军代表联系方式']
        # QTableWidget设置整行选中
        self.showInputResult.tw_result.setColumnCount(len(title))
        self.showInputResult.tw_result.setHorizontalHeaderLabels(title)
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

            item = QTableWidgetItem(LineInfo[5][0])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 4, item)
            item = QTableWidgetItem(LineInfo[5][1])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 5, item)
            item = QTableWidgetItem(LineInfo[5][2])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 6, item)
            item = QTableWidgetItem(LineInfo[5][3])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.showInputResult.tw_result.setItem(i, 7, item)




    def soltOutput(self):
        if len(self.result) < 1:
            getMessageBox('警告', '未选中任何数据，无法导出', True, False)
            return
        reply = getMessageBox('导出数据包', '是否保存修改并导出数据包？', True, True)
        if reply == QMessageBox.Cancel:
            self.initTableWidget()
            return
        self.initTableWidget()
        directoryPath = QFileDialog.getExistingDirectory(self, "请选择导出文件夹", "c:/")
        if len(directoryPath) > 0:
            # 填表数据
            dataList = ['厂家目录']
            for i, lineInfo in enumerate(self.result):
                rowData = []
                for i in range(len(lineInfo)):
                    if i < 5:
                        rowData.append(lineInfo[i])
                    if i == 8:
                        rowData.append(getResultByAgentId(lineInfo[8])[0])
                dataList.append(rowData.copy())

            if dataList is None or len(dataList) == 1:
                return
            else:
                print(dataList)
                date = QDateTime.currentDateTime()
                installData = date.toString("yyyy年MM月dd日hh时mm分ss秒")  # hh:mm:ss
                pathName = "%s/%s厂家目录.nms" % (directoryPath,installData)
                with open(pathName, "wb") as file:
                    pickle.dump(dataList, file)
                getMessageBox("导出成功", "导出数据包成功！", True, False)
        pass

    def slotCancelInputIntoDatabase(self):
        self.showInputResult.hide()
        self.setDisabled(False)
        self.initTableWidget()

    def slotInputIntoDatabase(self):
        for i, lineInfo in enumerate(self.inputList):
            if i == 0:
                continue
            try:
                if insertOneDataFatorySet(lineInfo):
                    pass
            except Exception as e:
                print(e)
                getMessageBox("导入失败", "导入第%d数据失败！" % (i), True, False)

        self.showInputResult.hide()
        self.setDisabled(False)
        self.initTableWidget()
