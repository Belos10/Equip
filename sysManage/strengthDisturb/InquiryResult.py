import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, QAbstractItemView, QMessageBox, QLineEdit,QHeaderView
from PyQt5.Qt import QRegExp, QRegExpValidator,QKeyEvent
from database.SD_EquipmentBanlanceSql import updateOneEquipmentBalanceData
from widgets.strengthDisturb.inquiry_result import Widget_Inquiry_Result
from database.strengthDisturbSql import *
from sysManage.strengthDisturb.chooseFactoryYear import chooseFactoryYear
from PyQt5.Qt import Qt

regx = QRegExp("[0-9]*")
#new
'''
    类功能：
        管理实力分布下实力查询结果界面，包含查询结果相关逻辑代码
'''
class Inquiry_Result(QWidget, Widget_Inquiry_Result):
    def __init__(self, parent=None):
        super(Inquiry_Result, self).__init__(parent)
        self.setupUi(self)

        #存储当前查询结果，结构为：{'行号':该行数据'}
        self.currentInquiryResult = {}
        self.unitList = []
        self.equipList = []
        self.year = None
        self.result = []
        self.chooseFactoryYear = chooseFactoryYear(self)
        self.chooseFactoryYear.hide()
        self.currentFactoryYear = ''
        #信号和槽连接
        self.signalConnect()
        self.startFactoryYear = None
        self.endFactoryYear = None
        headerlist = ['单位名称', '装备名称', '实力数', '编制数', '现有数', '偏差', '准备退役数', '未到位数', '提前退役', '待核查无实物', '待核查无实力', '单独建账',
                      '正常到位']
        self.tw_inquiryResult.setHorizontalHeaderLabels(headerlist)
        self.tw_inquiryResult.setColumnCount(len(headerlist))
        self.tw_inquiryResult.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    '''
        信号和槽连接
    '''
    def signalConnect(self):

        #当点击按装备展开时
        self.rb_equipShow.clicked.connect(self.slotClickedRB)

        #当点击按单位展开时
        self.rb_unitShow.clicked.connect(self.slotClickedRB)

        #当展开到末级被点击时
        self.cb_showLast.clicked.connect(self.slotClickedRB)

        #当只列存在偏差被点击时
        self.cb_showDistence.clicked.connect(self.slotClickedRB)

        #删除当前装备
        self.pb_clearCheck.clicked.connect(self.slotClearCurrentRow)

        #清除当前页面全部装备实力数
        self.pb_clearAll.clicked.connect(self.slotClearCurrentPage)

        #选择展示的出厂年份
        self.pb_factoryYear.clicked.connect(self.slotChooseFactoryYear)


        self.chooseFactoryYear.tb_cancel.clicked.connect(self.slotCancelChooseFactoryYear)

        self.chooseFactoryYear.tb_yes.clicked.connect(self.slotChangeSeeMethod)

    def slotChangeSeeMethod(self):
        if self.chooseFactoryYear.selectAll:
            self.currentFactoryYear = ""
            self._initTableWidgetByUnitListAndEquipList(self.unitList, self.equipList, self.year)
            self.lb_factoryYear.setText("当前查询出厂年份为：全部")
            self.chooseFactoryYear.hide()
        else:
            self.currentFactoryYear = "---"
            self.startFactoryYear = self.chooseFactoryYear.startFactoryYear
            self.endFactoryYear = self.chooseFactoryYear.endFactoryYear
            #print("===============0", self.startFactoryYear, self.endFactoryYear)
            if int(self.startFactoryYear) > int(self.endFactoryYear):
                reply = QMessageBox.information(self,"查询", "请重新选择，开始年份必须小于等于结束年份", QMessageBox.Yes)
                return
            else:
                self.lb_factoryYear.setText("当前查询出厂年份为：" + self.startFactoryYear + "年 至 " + self.endFactoryYear + "年")
                self._initTableWidgetByUnitListAndEquipList(self.unitList, self.equipList, self.year)
                self.chooseFactoryYear.hide()
    '''
        信号和槽连接断开
    '''
    def slotDisconnect(self):
        pass

    '''
       清除当前结果页面所有的实力数
    '''

    def slotChooseFactoryYear(self):
        self.chooseFactoryYear.initComBoxAboutYear()
        self.chooseFactoryYear.show()

    def slotClearCurrentPage(self):
        if self.currentFactoryYear != "":
            reply = QMessageBox.question(self, '清除', '清除失败,请将出厂年份设置为全部', QMessageBox.Yes)
            return
        if self.year == '全部':
            reply = QMessageBox.question(self, '清除', '只能某一年，清除失败', QMessageBox.Yes)
            return
        reply = QMessageBox.question(self, '清除', '是否清除当前页面所有行的实力数？', QMessageBox.Yes, QMessageBox.Cancel)
        if reply == QMessageBox.Cancel:
            return

        for i, resultInfo in self.currentInquiryResult.items():
            Unit_ID = resultInfo[1]
            Equip_ID = resultInfo[0]
            orginNum = resultInfo[4]
            year = resultInfo[15]
            unitHaveChild = selectUnitIsHaveChild(Unit_ID)
            equipHaveChild = selectEquipIsHaveChild(Equip_ID)
            if unitHaveChild or equipHaveChild:
                reply = QMessageBox.question(self, '清除', '第' + str(i) + "行清除失败，只能清除末级单位和装备实力数", QMessageBox.Yes)
                continue
            else:
                updateStrengthAboutStrengrh(Unit_ID, Equip_ID, year, "0", orginNum)
                self._initTableWidgetByUnitListAndEquipList(self.unitList, self.equipList, self.year)

    def changeCurrentFactoryYear(self):
        self.currentFactoryYear = self.chooseFactoryYear.cb_factoryYear.currentText()

        text = "当前显示的出厂年份：" + self.currentFactoryYear
        self.lb_factoryYear.setText(text)

        if self.currentFactoryYear == "全部":
            self.currentFactoryYear = ''
        self.chooseFactoryYear.hide()

        self._initTableWidgetByUnitListAndEquipList(self.unitList, self.equipList, self.year)


    def slotCancelChooseFactoryYear(self):
        self.chooseFactoryYear.hide()
    '''
        清除当前行的实力数
    '''
    def slotClearCurrentRow(self):
        currentRow = self.tw_inquiryResult.currentRow()
        if currentRow < 0:
            return
        else:
            for i, resultInfo in self.currentInquiryResult.items():
                if i == currentRow:
                    Unit_ID = resultInfo[1]
                    Equip_ID = resultInfo[0]
                    orginNum = resultInfo[4]
                    year = resultInfo[15]
                    unitHaveChild = selectUnitIsHaveChild(Unit_ID)
                    equipHaveChild = selectEquipIsHaveChild(Equip_ID)
                    if unitHaveChild or equipHaveChild:
                        reply = QMessageBox.question(self, '清除', '只能清除末级单位和装备的实力数', QMessageBox.Yes)
                        return
                    elif self.year == '全部':
                        reply = QMessageBox.question(self, '清除', '只能某一年，清除失败', QMessageBox.Yes)
                        return
                    else:
                        reply = QMessageBox.question(self, '清除', '是否清除当前行的实力数？', QMessageBox.Yes, QMessageBox.Cancel)
                        updateStrengthAboutStrengrh(Unit_ID, Equip_ID, year, "0", orginNum)
                        self._initTableWidgetByUnitListAndEquipList(self.unitList, self.equipList, self.year)
    '''
        功能：
            当前表格中某个值被修改
    '''
    def slotItemChange(self, item):
        currentRow = self.tw_inquiryResult.currentRow()
        currentColumn = self.tw_inquiryResult.currentColumn()
        if currentColumn == 2:
            for i, resultInfo in self.currentInquiryResult.items():
                if i == currentRow:
                    Unit_ID = resultInfo[1]
                    Equip_ID = resultInfo[0]
                    unitHaveChild = selectUnitIsHaveChild(Unit_ID)
                    equipHaveChild = selectEquipIsHaveChild(Equip_ID)
                    if self.tw_inquiryResult.cellWidget(currentRow, currentColumn).text() == str(resultInfo[4]):
                        return
                    if self.currentFactoryYear != "":
                        reply = QMessageBox.question(self, '清除', '清除失败,请将出厂年份设置为全部', QMessageBox.Yes)
                        self.tw_inquiryResult.cellWidget(currentRow, currentColumn).setText(resultInfo[4])
                        return
                    if unitHaveChild or equipHaveChild:
                        reply = QMessageBox.question(self, '修改', '只能修改末级实力数，修改失败', QMessageBox.Yes)
                        self.tw_inquiryResult.cellWidget(currentRow, currentColumn).setText(str(resultInfo[4]))
                        return
                    elif self.year == '全部':
                        reply = QMessageBox.question(self, '修改', '只能某一年，修改失败', QMessageBox.Yes)
                        self.tw_inquiryResult.cellWidget(currentRow, currentColumn).setText(resultInfo[4])
                        return
                    else:
                        if self.tw_inquiryResult.cellWidget(currentRow, currentColumn).text() != resultInfo[4]:
                            try:
                                updateSuccess = updateStrengthAboutStrengrh(Unit_ID, Equip_ID, self.year,
                                                            self.tw_inquiryResult.cellWidget(currentRow,
                                                                                       currentColumn).text(),
                                                            str(resultInfo[4]))
                                if updateSuccess != True:
                                    QMessageBox.information(self, "修改", str(updateSuccess) + "修改失败", QMessageBox.Yes)
                                QMessageBox.information(self, "修改", "修改成功！", QMessageBox.Yes)
                                self._initTableWidgetByUnitListAndEquipList(self.unitList, self.equipList, self.year)
                            except ValueError:
                                reply = QMessageBox.question(self, '修改失败', '只能修改为整数', QMessageBox.Yes)
                                self.tw_inquiryResult.cellWidget(currentRow, currentColumn).setText(str(resultInfo[4]))
                                return
        elif currentColumn == 0:
            for i, resultInfo in self.currentInquiryResult.items():
                if i == currentRow:
                    print(resultInfo)
                    self.tw_inquiryResult.item(currentRow, currentColumn).setText(resultInfo[3])
        elif currentColumn == 1:
            for i, resultInfo in self.currentInquiryResult.items():
                if i == currentRow:
                    print(resultInfo)
                    self.tw_inquiryResult.item(currentRow, currentColumn).setText(resultInfo[2])
        else:
            for i, resultInfo in self.currentInquiryResult.items():
                if i == currentRow:
                    print(resultInfo)
                    self.tw_inquiryResult.item(currentRow, currentColumn).setText(resultInfo[currentColumn + 2])

    #当某个单击按钮被选中时
    def slotClickedRB(self):
        self._initTableWidgetByUnitListAndEquipList(self.unitList, self.equipList, self.year)

    #初始化tableWidget
    def _initTableWidgetByUnitListAndEquipList(self, UnitList, EquipList, year):
        self.tw_inquiryResult.clear()
        self.tw_inquiryResult.setRowCount(0)
        self.unitList = UnitList
        self.equipList = EquipList
        self.year = year
        resultList = []
        headerlist = ['单位名称', '装备名称', '实力数', '编制数', '现有数', '偏差', '准备退役数', '未到位数', '提前退役', '待核查无实物', '待核查无实力', '单独建账',
                      '正常到位']
        self.tw_inquiryResult.setHorizontalHeaderLabels(headerlist)
        self.tw_inquiryResult.setColumnCount(len(headerlist))
        if self.rb_equipShow.isChecked():
            #按装备展开
            resultList = selectAboutStrengthByEquipShow(UnitList, EquipList, year, self.currentFactoryYear, self.startFactoryYear, self.endFactoryYear)
        elif self.rb_unitShow.isChecked():
            #按单位展开
            resultList = selectAboutStrengthByUnitShow(UnitList, EquipList, year, self.currentFactoryYear, self.startFactoryYear, self.endFactoryYear)
        else:
            resultList = selectAboutStrengthByUnitListAndEquipList(UnitList, EquipList, year, self.currentFactoryYear, self.startFactoryYear, self.endFactoryYear)

        if self.cb_showLast.isChecked():
            resultList = selectAboutStrengthByLast(UnitList, EquipList, year, self.currentFactoryYear, self.startFactoryYear, self.endFactoryYear)
            self.rb_unitShow.setCheckable(False)
            self.rb_equipShow.setCheckable(False)
            self.rb_equipShow.setDisabled(True)
            self.rb_unitShow.setDisabled(True)
        else:
            self.rb_unitShow.setCheckable(True)
            self.rb_equipShow.setCheckable(True)
            self.rb_equipShow.setDisabled(False)
            self.rb_unitShow.setDisabled(False)

        self.tw_inquiryResult.setRowCount(len(resultList))
        isMinyear = selectIsMinStrengthYear(year)
        i = 0
        for LineInfo in resultList:
            if self.cb_showDistence.isChecked():
                if int(LineInfo[7]) != 0:
                    item = QTableWidgetItem(LineInfo[3])
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.tw_inquiryResult.setItem(i, 0, item)

                    item = QTableWidgetItem(LineInfo[2])
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.tw_inquiryResult.setItem(i, 1, item)

                    item = QLineEdit()
                    item.setText(str(LineInfo[4]))
                    item.textChanged.connect(self.slotItemChange)
                    item.setStyleSheet("background:transparent;border-width:0")
                    validator = QRegExpValidator(regx)
                    item.setValidator(validator)
                    self.tw_inquiryResult.setCellWidget(i, 2, item)

                    item = QTableWidgetItem(str(LineInfo[5]))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.tw_inquiryResult.setItem(i, 3, item)
                    item = QTableWidgetItem(str(LineInfo[6]))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.tw_inquiryResult.setItem(i, 4, item)
                    item = QTableWidgetItem(str(LineInfo[7]))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.tw_inquiryResult.setItem(i, 5, item)
                    item = QTableWidgetItem(str(LineInfo[8]))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.tw_inquiryResult.setItem(i, 6, item)
                    item = QTableWidgetItem(str(LineInfo[9]))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.tw_inquiryResult.setItem(i, 7, item)
                    item = QTableWidgetItem(str(LineInfo[10]))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.tw_inquiryResult.setItem(i, 8, item)
                    item = QTableWidgetItem(str(LineInfo[11]))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.tw_inquiryResult.setItem(i, 9, item)
                    item = QTableWidgetItem(str(LineInfo[12]))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.tw_inquiryResult.setItem(i, 10, item)
                    item = QTableWidgetItem(str(LineInfo[13]))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.tw_inquiryResult.setItem(i, 11, item)
                    item = QTableWidgetItem(str(LineInfo[14]))
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.tw_inquiryResult.setItem(i, 12, item)

                    self.currentInquiryResult[i] = LineInfo
                    i = i + 1
                else:
                    pass
            else:
                item = QTableWidgetItem(LineInfo[3])
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tw_inquiryResult.setItem(i, 0, item)
                item = QTableWidgetItem(LineInfo[2])
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tw_inquiryResult.setItem(i, 1, item)

                item = QLineEdit()
                item.setText(str(LineInfo[4]))
                item.setStyleSheet("background:transparent;border-width:0")
                item.textChanged.connect(self.slotItemChange)
                validator = QRegExpValidator(regx)
                item.setValidator(validator)
                self.tw_inquiryResult.setCellWidget(i, 2, item)

                item = QTableWidgetItem(str(LineInfo[5]))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tw_inquiryResult.setItem(i, 3, item)
                item = QTableWidgetItem(str(LineInfo[6]))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tw_inquiryResult.setItem(i, 4, item)
                item = QTableWidgetItem(str(LineInfo[7]))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tw_inquiryResult.setItem(i, 5, item)
                item = QTableWidgetItem(str(LineInfo[8]))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tw_inquiryResult.setItem(i, 6, item)
                item = QTableWidgetItem(str(LineInfo[9]))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tw_inquiryResult.setItem(i, 7, item)
                item = QTableWidgetItem(str(LineInfo[10]))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tw_inquiryResult.setItem(i, 8, item)
                item = QTableWidgetItem(str(LineInfo[11]))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tw_inquiryResult.setItem(i, 9, item)
                item = QTableWidgetItem(str(LineInfo[12]))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tw_inquiryResult.setItem(i, 10, item)
                item = QTableWidgetItem(str(LineInfo[13]))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tw_inquiryResult.setItem(i, 11, item)
                item = QTableWidgetItem(str(LineInfo[14]))
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.tw_inquiryResult.setItem(i, 12, item)

                self.currentInquiryResult[i] = LineInfo
                i = i + 1
        self.tw_inquiryResult.setRowCount(i)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Inquiry_Result()
    widget.show()
    sys.exit(app.exec_())
