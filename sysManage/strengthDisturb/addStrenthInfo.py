from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QComboBox, QMessageBox, QLineEdit,QHeaderView,QAbstractItemView
from PyQt5.Qt import QRegExp,QRegExpValidator, Qt
from widgets.strengthDisturb.add_strenth_info import Add_Strenth_Info
from database.strengthDisturbSql import *
from database.dictSelect.factorySetSql import *
from sysManage.strengthDisturb.chooseFactoryYear import chooseFactoryYear
from database.alocatMangeSql import *

regx = QRegExp("[0-9]*")
allFactoryYearInt = list(range(1970, 2022))
allFactoryYear = [str(x) for x in allFactoryYearInt]
equipState = ['新品','堪用品','待修品','废品']
isArrive = ['是', '否']
'''
    类功能：
        信息录入界面管理
'''
class AddStrenthInfo(QWidget, Add_Strenth_Info):
    def __init__(self, parent=None):
        super(AddStrenthInfo, self).__init__(parent)
        self.setupUi(self)
        self.currentResult = {}
        self.orginRowNum = 0
        self.strgenthInfo = None
        self.isChange = False
        self.unitID = None
        self.equipID = None
        self.isMutilInput = None
        self.allYear = None
        self.lineEdit.setAlignment(Qt.AlignCenter)

        self.chooseFactoryYear = chooseFactoryYear(self)
        self.chooseFactoryYear.initComBoxAboutYear()
        self.chooseFactoryYear.hide()

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.lineEdit.setFocusPolicy(Qt.NoFocus)
        self.lb_factorYear.setText("当前查询出厂年份为：全部")
        self.factoryYear = ""
        self.startFactoryYear = ""
        self.endFactoryYear = ""
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.signalConnect()

    def signalConnect(self):
        #新增按钮
        self.pb_Increase.clicked.connect(self.slotAddSingle)

        #查看数据是否修改
        #self.tableWidget.itemChanged.connect(self.slotItemChanged)

        #删除某行数据
        self.pb_Delete.clicked.connect(self.deleteNote)

        self.pb_chooseFactoryYear.clicked.connect(self.slotChooseFactoryYear)

        self.chooseFactoryYear.tb_cancel.clicked.connect(self.slotCancelChoose)

        self.chooseFactoryYear.tb_yes.clicked.connect(self.slotChangeSeeMethod)

    def slotChangeSeeMethod(self):
        if self.chooseFactoryYear.selectAll:
            self.factoryYear = ""
            self._initTableWidget_(self.RowData, self.yearList)
            self.lb_factorYear.setText("当前查询出厂年份为：全部")
            self.chooseFactoryYear.hide()
            self.setDisabled(False)
        else:
            self.factoryYear = "---"
            self.startFactoryYear = self.chooseFactoryYear.startFactoryYear
            self.endFactoryYear = self.chooseFactoryYear.endFactoryYear
            #print("===============0", self.startFactoryYear, self.endFactoryYear)
            if int(self.startFactoryYear) > int(self.endFactoryYear):
                reply = QMessageBox.information(self,"查询", "请重新选择，开始年份必须小于等于结束年份", QMessageBox.Yes)
                return
            else:
                self.lb_factorYear.setText("当前查询出厂年份为：" + self.startFactoryYear + "年 至 " + self.endFactoryYear + "年")
                self._initTableWidget_(self.RowData, self.yearList)
                self.chooseFactoryYear.hide()
                self.setDisabled(False)

    def slotCancelChoose(self):
        self.setDisabled(False)
        self.chooseFactoryYear.hide()

    def slotDisconnect(self):
        self.pb_Increase.clicked.disconnect(self.slotAddSingle)
        # 查看数据是否修改
        self.tableWidget.itemChanged.disconnect(self.slotItemChanged)

    def slotChooseFactoryYear(self):
        self.chooseFactoryYear.show()
        self.setDisabled(True)
        self.chooseFactoryYear.setDisabled(False)

    #初始化录入信息界面以及tablewidget
    def _initTableWidget_(self, RowData, yearList):
        self.RowData = RowData
        print("test:                 ", self.RowData)
        self.unitID = RowData[1]
        self.equipID = RowData[0]
        if findEquipUnitByEquipID(self.equipID):
            self.equipUnit = findEquipUnitByEquipID(self.equipID)[0][0]
        else:
            self.equipUnit = ""
        self.label_MeasureUnit.setText(self.equipUnit)

        print(self.unitID, self.equipID)
        self.allYear = selectAllStrengthYear()
        self.yearList = yearList
        self.tableWidget.setRowCount(0)
        self.strgenthInfo = RowData
        self.now, self.strength= selectNowNumAndStrengthNum(RowData[1], RowData[0], self.yearList, self.factoryYear)
        self.now, self.strength = str(self.now), str(self.strength)
        self.label_UnitName.setText(RowData[3])
        self.label_EquipName.setText(RowData[2])
        self.label_ExistNumber.setText(self.now)
        self.label_PowerNumber.setText(self.strength)
        if self.isMutilInput:
            self.lineEdit.setText("逐批信息录入")
            self.header = ['批次号', '数量', '出厂年份', '生产厂家', '装备状态', '是否到位', '文件凭证', '备注']
            self.tableWidget.setColumnCount(len(self.header))
            self.tableWidget.setHorizontalHeaderLabels(self.header)
            self.currentResult = selectInfoAboutInput(RowData[1], RowData[0], self.yearList, self.factoryYear, self.startFactoryYear, self.endFactoryYear)
            self.tableWidget.setRowCount(len(self.currentResult))
            self.orginRowNum = len(self.currentResult)
            self.now = 0

            for i, data in enumerate(self.currentResult):
                item = QTableWidgetItem(data[2])
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tableWidget.setItem(i, 0, item)
                item = QTableWidgetItem(data[3])
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tableWidget.setItem(i, 1, item)
                item = QTableWidgetItem(data[4])
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tableWidget.setItem(i, 2, item)
                item = QTableWidgetItem(data[5])
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tableWidget.setItem(i, 3, item)
                item = QTableWidgetItem(data[6])
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tableWidget.setItem(i, 4, item)
                item = QTableWidgetItem(data[7])
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tableWidget.setItem(i, 5, item)
                item = QTableWidgetItem(data[8])
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tableWidget.setItem(i, 6, item)
                item = QTableWidgetItem(data[9])
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tableWidget.setItem(i, 7, item)
                self.currentResult[i] = data
                self.now = self.now + int(data[3])
            self.label_ExistNumber.setText(str(self.now))
        else:
            self.lineEdit.setText("逐号信息录入")
            self.header = ['批次号', '出厂年份', '生产厂家', '装备状态', '是否到位', '文件凭证', '备注']
            self.tableWidget.setColumnCount(len(self.header))
            self.tableWidget.setHorizontalHeaderLabels(self.header)
            self.currentResult = selectInfoAboutInput(RowData[1], RowData[0], self.yearList, self.factoryYear, self.startFactoryYear, self.endFactoryYear)
            self.tableWidget.setRowCount(len(self.currentResult))
            self.orginRowNum = len(self.currentResult)
            self.now = self.orginRowNum
            self.label_ExistNumber.setText(str(self.now))
            #print("结果为：", self.currentResult)
            for i, data in enumerate(self.currentResult):
                item = QTableWidgetItem(data[2])
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tableWidget.setItem(i, 0, item)
                item = QTableWidgetItem(data[4])
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tableWidget.setItem(i, 1, item)
                item = QTableWidgetItem(data[5])
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tableWidget.setItem(i, 2, item)
                item = QTableWidgetItem(data[6])
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tableWidget.setItem(i, 3, item)
                item = QTableWidgetItem(data[7])
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tableWidget.setItem(i, 4, item)
                item = QTableWidgetItem(data[8])
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tableWidget.setItem(i, 5, item)
                item = QTableWidgetItem(data[9])
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tableWidget.setItem(i, 6, item)
                self.currentResult[i] = data
        self.isChange = False

    # 信息录入界面新增按钮
    def slotAddSingle(self):
        #yearList = selectAllStrengthYear()
        validator = QRegExpValidator(regx)
        if self.isMutilInput:
            row = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(row + 1)
            item = QTableWidgetItem("")
            self.tableWidget.setItem(row, 0, item)
            line = QLineEdit()
            line.setValidator(validator)
            self.tableWidget.setCellWidget(row, 1, line)
            item = QComboBox()
            item.addItems(allFactoryYear)
            self.tableWidget.setCellWidget(row, 2, item)
            factoryInfoNameList = selectAllNameAboutFactory()
            item = QComboBox()
            item.addItems(factoryInfoNameList)
            self.tableWidget.setCellWidget(row, 3, item)
            item = QComboBox()
            item.addItems(equipState)
            self.tableWidget.setCellWidget(row, 4, item)
            item = QComboBox()
            item.addItems(isArrive)
            self.tableWidget.setCellWidget(row, 5, item)
            item = QComboBox()
            alocteYearList = selectYearListAboutDisturbPlan()
            confirm = [x + "年分配调整计划" for x in alocteYearList]
            item.addItems(confirm)
            self.tableWidget.setCellWidget(row, 6, item)
            item = QTableWidgetItem("")
            self.tableWidget.setItem(row, 7, item)
        else:
            row = self.tableWidget.rowCount()
            self.tableWidget.setRowCount(row + 1)
            item = QTableWidgetItem("")
            self.tableWidget.setItem(row, 0, item)
            item = QComboBox()
            item.addItems(allFactoryYear)
            self.tableWidget.setCellWidget(row, 1, item)
            factoryInfoNameList = selectAllNameAboutFactory()
            item = QComboBox()
            item.addItems(factoryInfoNameList)
            self.tableWidget.setCellWidget(row, 2, item)
            item = QComboBox()
            item.addItems(equipState)
            self.tableWidget.setCellWidget(row, 3, item)
            item = QComboBox()
            item.addItems(isArrive)
            self.tableWidget.setCellWidget(row, 4, item)
            item = QComboBox()
            alocteYearList = selectYearListAboutDisturbPlan()
            confirm = [x + "年分配调整计划" for x in alocteYearList]
            item.addItems(confirm)
            self.tableWidget.setCellWidget(row, 5, item)
            item = QTableWidgetItem("")
            self.tableWidget.setItem(row, 6, item)

    # 信息录入界面删除按钮
    def deleteNote(self):
        currentRow = self.tableWidget.currentRow()
        if (currentRow >= len(self.currentResult)) and currentRow != -1:
            self.tableWidget.removeRow(currentRow)
            return
        if currentRow < 0:
            return
        else:
            reply = QMessageBox.question(self, '删除', '是否删除当前行？', QMessageBox.Yes, QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                for i, resultInfo in enumerate(self.currentResult):
                    if i == currentRow:
                        year = resultInfo[4]
                        delSuccess = delFromInputInfo(resultInfo[0], resultInfo[1], resultInfo[2], resultInfo[3], resultInfo[4], self.yearList)
                        if delSuccess != True:
                            reply = QMessageBox.question(self, '删除', str(delSuccess) + '删除失败！', QMessageBox.Yes)
                            return
                        reply = QMessageBox.question(self, '删除', '删除成功！', QMessageBox.Yes)
                        self._initTableWidget_(self.RowData, self.yearList)
                        return
