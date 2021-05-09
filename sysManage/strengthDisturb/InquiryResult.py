import sys
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, QAbstractItemView, QMessageBox
from widgets.strengthDisturb.inquiry_result import Widget_Inquiry_Result
from database.strengthDisturbSql import selectAboutStrengthByUnitListAndEquipList, selectUnitIsHaveChild, selectEquipIsHaveChild,\
    selectAboutStrengthByEquipShow,selectAboutStrengthByUnitShow, updateStrengthAboutStrengrh,updateStrengthAboutStrengrh
from PyQt5.Qt import Qt
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
        #信号和槽连接
        self.signalConnect()

    '''
        信号和槽连接
    '''
    def signalConnect(self):
        #当前表格中某个值被修改
        self.tw_inquiryResult.itemChanged.connect(self.slotItemChange)

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

        #清除选中状态
        self.pb_delState.clicked.connect(self.slotChangeCheckState)
    '''
        信号和槽连接断开
    '''
    def slotDisconnect(self):
        pass

    '''
        功能：
            清除单选按钮选中状态
    '''
    def slotChangeCheckState(self):
        if self.rb_unitShow.isChecked():
            self.rb_unitShow.setChecked(False)

    '''
       清除当前结果页面所有的实力数
    '''
    def slotClearCurrentPage(self):
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
                    if unitHaveChild or equipHaveChild:
                        reply = QMessageBox.question(self, '修改', '只能修改末级实力数，修改失败', QMessageBox.Yes)
                        self.tw_inquiryResult.item(currentRow, currentColumn).setText(resultInfo[4])
                        return
                    elif self.year == '全部':
                        reply = QMessageBox.question(self, '修改', '只能某一年，修改失败', QMessageBox.Yes)
                        self.tw_inquiryResult.item(currentRow, currentColumn).setText(resultInfo[4])
                        return
                    else:
                        if self.tw_inquiryResult.item(currentRow, currentColumn).text() != resultInfo[4]:
                            reply = QMessageBox.question(self, '修改', '是否修改当前实力数？', QMessageBox.Yes,
                                                         QMessageBox.Cancel)
                            if reply == QMessageBox.Yes:
                                updateStrengthAboutStrengrh(Unit_ID, Equip_ID, self.year, self.tw_inquiryResult.item(currentRow, currentColumn).text(),resultInfo[4])
                                self._initTableWidgetByUnitListAndEquipList(self.unitList, self.equipList, self.year)
                            else:
                                self.tw_inquiryResult.item(currentRow, currentColumn).setText(resultInfo[4])
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

        if self.rb_equipShow.isChecked():
            #按装备展开
            resultList = selectAboutStrengthByEquipShow(UnitList, EquipList, year, '')
        elif self.rb_unitShow.isChecked():
            #按单位展开
            resultList = selectAboutStrengthByUnitShow(UnitList, EquipList, year, '')
        else:
            resultList = selectAboutStrengthByUnitListAndEquipList(UnitList, EquipList, year, '')

        if self.cb_showLast.isChecked():
            resultListEquip = selectAboutStrengthByEquipShow(UnitList, EquipList, year, '')
            resultListUnit = selectAboutStrengthByUnitShow(UnitList, EquipList, year, '')
            resultList = resultListEquip + resultListUnit
            self.rb_unitShow.setCheckable(False)
            self.rb_equipShow.setCheckable(False)
            self.rb_equipShow.setDisabled(True)
            self.rb_unitShow.setDisabled(True)
        else:
            self.rb_unitShow.setCheckable(True)
            self.rb_equipShow.setCheckable(True)
            self.rb_equipShow.setDisabled(False)
            self.rb_unitShow.setDisabled(False)

        headerlist = ['单位名称', '装备名称', '实力数', '编制数', '现有数', '偏差', '准备退役数', '未到位数', '提前退役', '待核查无实物', '待核查无实力', '单独建账',
                      '正常到位']
        self.tw_inquiryResult.setHorizontalHeaderLabels(headerlist)
        self.currentInquiryResult.clear()
        self.tw_inquiryResult.setColumnCount(len(headerlist))
        self.tw_inquiryResult.setRowCount(len(resultList))

        i = 0
        for LineInfo in resultList:
            if self.cb_showDistence.isChecked():
                if int(LineInfo[7]) != 0:
                    item = QTableWidgetItem(LineInfo[3])
                    item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                    self.tw_inquiryResult.setItem(i, 0, item)
                    item = QTableWidgetItem(LineInfo[2])
                    self.tw_inquiryResult.setItem(i, 1, item)
                    item = QTableWidgetItem(LineInfo[4])
                    self.tw_inquiryResult.setItem(i, 2, item)
                    item = QTableWidgetItem(LineInfo[5])
                    self.tw_inquiryResult.setItem(i, 3, item)
                    item = QTableWidgetItem(LineInfo[6])
                    self.tw_inquiryResult.setItem(i, 4, item)
                    item = QTableWidgetItem(LineInfo[7])
                    self.tw_inquiryResult.setItem(i, 5, item)
                    item = QTableWidgetItem(LineInfo[8])
                    self.tw_inquiryResult.setItem(i, 6, item)
                    item = QTableWidgetItem(LineInfo[9])
                    self.tw_inquiryResult.setItem(i, 7, item)
                    item = QTableWidgetItem(LineInfo[10])
                    self.tw_inquiryResult.setItem(i, 8, item)
                    item = QTableWidgetItem(LineInfo[11])
                    self.tw_inquiryResult.setItem(i, 9, item)
                    item = QTableWidgetItem(LineInfo[12])
                    self.tw_inquiryResult.setItem(i, 10, item)
                    item = QTableWidgetItem(LineInfo[13])
                    self.tw_inquiryResult.setItem(i, 11, item)
                    item = QTableWidgetItem(LineInfo[14])
                    self.tw_inquiryResult.setItem(i, 12, item)

                    self.currentInquiryResult[i] = LineInfo
                    i = i + 1
                else:
                    pass
            else:
                item = QTableWidgetItem(LineInfo[3])
                self.tw_inquiryResult.setItem(i, 0, item)
                item = QTableWidgetItem(LineInfo[2])
                self.tw_inquiryResult.setItem(i, 1, item)
                item = QTableWidgetItem(LineInfo[4])
                self.tw_inquiryResult.setItem(i, 2, item)
                item = QTableWidgetItem(LineInfo[5])
                self.tw_inquiryResult.setItem(i, 3, item)
                item = QTableWidgetItem(LineInfo[6])
                self.tw_inquiryResult.setItem(i, 4, item)
                item = QTableWidgetItem(LineInfo[7])
                self.tw_inquiryResult.setItem(i, 5, item)
                item = QTableWidgetItem(LineInfo[8])
                self.tw_inquiryResult.setItem(i, 6, item)
                item = QTableWidgetItem(LineInfo[9])
                self.tw_inquiryResult.setItem(i, 7, item)
                item = QTableWidgetItem(LineInfo[10])
                self.tw_inquiryResult.setItem(i, 8, item)
                item = QTableWidgetItem(LineInfo[11])
                self.tw_inquiryResult.setItem(i, 9, item)
                item = QTableWidgetItem(LineInfo[12])
                self.tw_inquiryResult.setItem(i, 10, item)
                item = QTableWidgetItem(LineInfo[13])
                self.tw_inquiryResult.setItem(i, 11, item)
                item = QTableWidgetItem(LineInfo[14])
                self.tw_inquiryResult.setItem(i, 12, item)

                self.currentInquiryResult[i] = LineInfo
                i = i + 1
        self.tw_inquiryResult.setRowCount(i)
    '''
        功能：
            根据查询到的结果初始化tablewidget
    '''
    def _initTableWidgetBySelectResult(self, result):
        #print(result)
        self.tw_inquiryResult.clear()
        self.result = result

        self.result_num = len(result)
        self.tw_inquiryResult.setRowCount(self.result_num)
        self.tw_inquiryResult.setColumnCount(13)
        headerlist = ['单位名称', '装备名称', '实力数', '编制数', '现有数', '偏差', '准备退役数', '未到位数', '提前退役', '待核查无实物', '待核查无实力', '单独建账',
                      '正常到位']
        self.tw_inquiryResult.setHorizontalHeaderLabels(headerlist)
        self.currentInquiryResult.clear()
        for i, data in enumerate(self.result):
            if self.cb_showDistence.isChecked():
                if int(data[7]) != 0:
                    item = QTableWidgetItem(data[3])
                    self.tw_inquiryResult.setItem(i, 0, item)
                    item = QTableWidgetItem(data[2])
                    self.tw_inquiryResult.setItem(i, 1, item)
                    item = QTableWidgetItem(data[4])
                    self.tw_inquiryResult.setItem(i, 2, item)
                    item = QTableWidgetItem(data[5])
                    self.tw_inquiryResult.setItem(i, 3, item)
                    item = QTableWidgetItem(data[6])
                    self.tw_inquiryResult.setItem(i, 4, item)
                    item = QTableWidgetItem(data[7])
                    self.tw_inquiryResult.setItem(i, 5, item)
                    item = QTableWidgetItem(data[8])
                    self.tw_inquiryResult.setItem(i, 6, item)
                    item = QTableWidgetItem(data[9])
                    self.tw_inquiryResult.setItem(i, 7, item)
                    item = QTableWidgetItem(data[10])
                    self.tw_inquiryResult.setItem(i, 8, item)
                    item = QTableWidgetItem(data[11])
                    self.tw_inquiryResult.setItem(i, 9, item)
                    item = QTableWidgetItem(data[12])
                    self.tw_inquiryResult.setItem(i, 10, item)
                    item = QTableWidgetItem(data[13])
                    self.tw_inquiryResult.setItem(i, 11, item)
                    item = QTableWidgetItem(data[14])
                    self.tw_inquiryResult.setItem(i, 12, item)

                    self.currentInquiryResult[i] = data
                else:
                    pass
            else:
                item = QTableWidgetItem(data[3])
                self.tw_inquiryResult.setItem(i, 0, item)
                item = QTableWidgetItem(data[2])
                self.tw_inquiryResult.setItem(i, 1, item)
                item = QTableWidgetItem(data[4])
                self.tw_inquiryResult.setItem(i, 2, item)
                item = QTableWidgetItem(data[5])
                self.tw_inquiryResult.setItem(i, 3, item)
                item = QTableWidgetItem(data[6])
                self.tw_inquiryResult.setItem(i, 4, item)
                item = QTableWidgetItem(data[7])
                self.tw_inquiryResult.setItem(i, 5, item)
                item = QTableWidgetItem(data[8])
                self.tw_inquiryResult.setItem(i, 6, item)
                item = QTableWidgetItem(data[9])
                self.tw_inquiryResult.setItem(i, 7, item)
                item = QTableWidgetItem(data[10])
                self.tw_inquiryResult.setItem(i, 8, item)
                item = QTableWidgetItem(data[11])
                self.tw_inquiryResult.setItem(i, 9, item)
                item = QTableWidgetItem(data[12])
                self.tw_inquiryResult.setItem(i, 10, item)
                item = QTableWidgetItem(data[13])
                self.tw_inquiryResult.setItem(i, 11, item)
                item = QTableWidgetItem(data[14])
                self.tw_inquiryResult.setItem(i, 12, item)

                self.currentInquiryResult[i] = data


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Inquiry_Result()
    widget.show()
    sys.exit(app.exec_())
